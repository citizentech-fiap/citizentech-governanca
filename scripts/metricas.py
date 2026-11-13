"""Recalcula os Metric Contracts (artefatos/metric_contracts/MC-*.yaml) sobre a versão entregue.

Os números vêm dos resultados versionados em cada módulo e, no painel, do código do próprio painel.
Saída: evidencias/metricas.md e evidencias/metricas.json.

    python scripts/metricas.py
"""
import operator
import sys

import pandas as pd
import yaml

import comum

OPERADORES = {">": operator.gt, ">=": operator.ge, "<": operator.lt, "<=": operator.le, "==": operator.eq}


def _sim(valor):
    return str(valor).strip().lower() in {"true", "1", "sim"}


def genai(pasta):
    teste = pd.read_csv(pasta / "eval/resultados/ponta_a_ponta/gemini/sentence_transformers/v3_verificacao/"
                                "revisao_independente.csv", encoding="utf-8-sig")
    validacao = pd.read_csv(pasta / "eval/resultados/validacao/ponta_a_ponta/revisao_independente.csv",
                            encoding="utf-8-sig")
    validacao = validacao[validacao.variante.eq("v3_verificacao")]
    seguranca = pd.read_csv(pasta / "eval/resultados/seguranca/gemini/seguranca.csv", encoding="utf-8-sig")

    def corretas(quadro):
        resp = quadro[quadro.categoria.isin(["respondivel", "multi_turno"])]
        return resp.julgamento.eq("correta").mean(), int(resp.julgamento.eq("correta").sum()), len(resp)

    t, t_ok, t_n = corretas(teste)
    v, v_ok, v_n = corretas(validacao)
    abst = teste[teste.categoria.isin(["sem_resposta", "fora_escopo"])]
    ligada = seguranca[seguranca.protecao_ligada.map(_sim)]
    return {
        "corretas_respondiveis_teste": t,
        "corretas_respondiveis_validacao": v,
        "abstencao_correta": abst.julgamento.eq("abstencao_correta").mean(),
        "afirmacoes_sem_suporte": int(teste.sustentada.astype(str).str.lower().isin(["não", "nao"]).sum()),
        "vazamentos_protecao_ligada": int(ligada.vazou_saida_final.map(_sim).sum()),
        "_detalhe": {"teste": f"{t_ok} de {t_n}", "validacao": f"{v_ok} de {v_n}",
                     "abstencao": f"{int(abst.julgamento.eq('abstencao_correta').sum())} de {len(abst)}",
                     "cenarios_protecao_ligada": len(ligada)},
    }


def rpa(pasta):
    res = pd.read_csv(pasta / "eval/resultados_robo.csv")
    labels = pd.read_csv(pasta / "data/synthetic/labels.csv")
    # Mesma regra de eval/avaliar_robo.py: em pedido ambíguo, os dois serviços plausíveis valem.
    alt = labels.set_index("request_id")["observacao"].astype(str).str.extract(r"alternativa=(\w+)")[0]
    aceitos = res.apply(lambda r: {r.servico_real} | ({alt[r.request_id]} if isinstance(alt.get(r.request_id), str)
                                                      else set()), axis=1)
    servico_ok = pd.Series([p in a for p, a in zip(res.servico_previsto, aceitos)], index=res.index)
    cls = res.categoria.isin(["tipico", "docs_faltando", "ilegivel", "ambiguo"])
    resolvidos = res.decisao.eq("resolvido")
    graves = resolvidos & (~servico_ok | res.categoria.eq("fora_escopo"))
    seguros = res.decisao.eq("revisao_humana") & res.decisao_esperada.eq("resolvido")
    return {
        "decisao_correta": res.decisao_ok.map(_sim).mean(),
        "erro_grave": int(graves.sum()),
        "acuracia_classificacao": servico_ok[cls].mean(),
        "taxa_revisao_humana": res.decisao.eq("revisao_humana").mean(),
        "revisao_desnecessaria": int(seguros.sum()),
        "_detalhe": {"pedidos": len(res), "respostas_automaticas": int(resolvidos.sum()),
                     "classificados": int(cls.sum())},
    }


def dashboard(placar):
    milho, feijao = placar["milho"], placar["feijao"]
    faixa = all(0 <= c["perda_min"] and c["perda_max"] <= 100 for c in placar.values())
    return {
        "acuracia_milho": milho["acuracia"],
        "acuracia_feijao": feijao["acuracia"],
        "spearman_milho": milho["spearman"],
        "sensibilidade_milho": milho["sensibilidade"],
        "sensibilidade_feijao": feijao["sensibilidade"],
        "especificidade_milho": milho["especificidade"],
        "invariante_faixa": int(faixa),
        "_detalhe": {c: f"{v['pares']} pares municipio-safra; perda entre {comum.num(v['perda_min'], 1)} e "
                        f"{comum.num(v['perda_max'], 1)}" for c, v in placar.items()},
    }


def avaliar_limite(valor, limite):
    if not isinstance(limite, str) or limite.strip() == "informativo":
        return None
    op, alvo = limite.split()
    return OPERADORES[op](valor, float(alvo))


def contratos():
    return [yaml.safe_load(p.read_text(encoding="utf-8"))
            for p in sorted((comum.ARTEFATOS / "metric_contracts").glob("MC-*.yaml"))]


def calcular(dados_versoes=None):
    dados_versoes = dados_versoes or comum.versoes()
    valores = {"genai": genai(comum.pasta("genai", dados_versoes)),
               "rpa": rpa(comum.pasta("rpa", dados_versoes)),
               "dashboard": dashboard(comum.placar_dashboard(dados_versoes))}
    resultado = []
    for mc in contratos():
        v = valores[mc["modulo"]]
        ind = mc["indicador"]
        atual = v[ind.get("chave_controle", ind["chave"])]
        qualidade = [dict(q, valor=v[q["chave"]], ok=avaliar_limite(v[q["chave"]], q["limite"]))
                     for q in mc["qualidade"]]
        disparados = [a for a in mc["alertas"] if OPERADORES[a["operador"]](v[a["metrica"]], a["valor"])]
        resultado.append(dict(id=mc["id"], nome=mc["nome"], versao=mc["versao"], modulo=mc["modulo"],
                              indicador=dict(ind, valor=atual, atinge_meta=atual >= ind["meta"]),
                              qualidade=qualidade, alertas=disparados, detalhe=v["_detalhe"]))
    return resultado


def formatar(valor, chave=""):
    if isinstance(valor, float) and not chave.startswith("spearman"):
        return comum.pct(valor) if 0 <= valor <= 1 else comum.num(valor)
    if isinstance(valor, float):
        return comum.num(valor)
    return str(valor)


def formatar_limite(limite, chave):
    if not isinstance(limite, str) or limite == "informativo":
        return str(limite)
    op, alvo = limite.split()
    alvo = float(alvo)
    texto = formatar(alvo, chave) if (alvo != int(alvo) or chave.startswith("spearman")) else str(int(alvo))
    return f"{op.replace('>=', '≥').replace('<=', '≤')} {texto}"


def relatorio(resultado, dados_versoes=None):
    linhas = comum.cabecalho("Metric Contracts recalculados", dados_versoes)
    for mc in resultado:
        ind = mc["indicador"]
        base = formatar(ind["baseline"]) if ind["baseline"] is not None else "não medido"
        linhas += [f"## {mc['id']} {mc['nome']} (v{mc['versao']})", "",
                   "| Indicador | Valor | Baseline | Meta | Situação |", "|---|---|---|---|---|",
                   f"| {ind['nome']} | {formatar(ind['valor'])} | {base} | {formatar(ind['meta'])} | "
                   f"{'atinge' if ind['atinge_meta'] else 'abaixo da meta'} |", ""]
        if ind.get("meta_descricao"):
            linhas += [f"Valor e meta referem-se a: {ind['meta_descricao']}.", ""]
        linhas += [
                   "| Métrica de qualidade | Valor | Limite | Situação |", "|---|---|---|---|"]
        for q in mc["qualidade"]:
            situacao = {True: "ok", False: "fora do limite", None: "informativo"}[q["ok"]]
            linhas.append(f"| {q['nome']} | {formatar(q['valor'], q['chave'])} | "
                          f"{formatar_limite(q['limite'], q['chave'])} | {situacao} |")
        linhas += ["", "Detalhe: " + "; ".join(f"{k}: {v}" for k, v in mc["detalhe"].items()) + ".", ""]
        if mc["alertas"]:
            linhas += ["Alertas disparados:", ""]
            for a in mc["alertas"]:
                gatilho = formatar_limite(f"{a['operador']} {a['valor']}", a["metrica"])
                linhas.append(f"- **{a['nivel']}** ({a['metrica']} {gatilho}): {a['acao'].strip()}")
            linhas.append("")
        else:
            linhas += ["Nenhum alerta disparado.", ""]
    return "\n".join(linhas)


def main():
    try:
        dados_versoes = comum.versoes()
        resultado = calcular(dados_versoes)
    except (FileNotFoundError, RuntimeError, KeyError) as erro:
        print(f"Não foi possível calcular os contratos: {erro}")
        return 1
    comum.gravar("metricas", relatorio(resultado, dados_versoes), resultado)
    for mc in resultado:
        criticos = [a for a in mc["alertas"] if a["nivel"] == "critico"]
        print(f"{mc['id']}: {formatar(mc['indicador']['valor'])} "
              f"({len(mc['alertas'])} alerta(s), {len(criticos)} crítico(s))")
    print("Relatório: evidencias/metricas.md")
    return 0


if __name__ == "__main__":
    sys.exit(main())
