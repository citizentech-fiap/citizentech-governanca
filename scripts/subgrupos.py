"""Desempenho por subgrupo (equidade) nos módulos que influenciam o acesso a benefício.

Painel: igualdade de oportunidade entre UFs, medida pela sensibilidade (perdas reais de 40% ou mais
que o painel sinaliza). O dano principal do painel é deixar de sinalizar uma perda real.
Robô: decisão correta, erro grave e envio para revisão humana, por UF e por serviço.
A diferença máxima entre subgrupos com pelo menos 20 casos é comparada com o limite de 5 pontos
percentuais. Subgrupos menores aparecem nas tabelas, mas não entram na diferença.

    python scripts/subgrupos.py
"""
import sys

import pandas as pd

import comum
import metricas

LIMITE_PP = 5.0
AMOSTRA_MINIMA = 20


def _diferenca(tabela, coluna, tamanho="n"):
    validos = tabela[(tabela[tamanho] >= AMOSTRA_MINIMA) & tabela[coluna].notna()]
    if len(validos) < 2:
        return None, validos
    return (validos[coluna].max() - validos[coluna].min()) * 100, validos


def painel(placar):
    saida = {}
    for cultura, dados in placar.items():
        tabela = pd.DataFrame([{"uf": uf, **v} for uf, v in sorted(dados["por_uf"].items())])
        dif, validos = _diferenca(tabela, "sensibilidade")
        dif_acerto, _ = _diferenca(tabela, "acuracia")
        saida[cultura] = dict(tabela=tabela.to_dict("records"), diferenca_pp=dif, diferenca_acerto_pp=dif_acerto,
                              ufs_comparadas=list(validos.uf), sensibilidade_geral=dados["sensibilidade"],
                              geral=dados["acuracia"])
    return saida


def robo(pasta_rpa):
    base = metricas.pedidos_rpa(pasta_rpa)
    saida = {}
    for grupo in ("uf", "servico_real"):
        tabela = (base.groupby(grupo).agg(n=("request_id", "size"), decisao_correta=("acerto", "mean"),
                                          revisao_humana=("revisao", "mean"), erro_grave=("grave", "sum"))
                  .reset_index().rename(columns={grupo: "grupo"}))
        dif, validos = _diferenca(tabela, "decisao_correta")
        saida[grupo] = dict(tabela=tabela.to_dict("records"), diferenca_pp=dif, grupos_comparados=list(validos.grupo),
                            erro_grave_total=int(tabela.erro_grave.sum()))
    return saida


def _situacao(dif):
    if dif is None:
        return "não comparável: menos de dois grupos com 20 casos ou mais"
    return f"{comum.num(dif, 1)} p.p., " + ("acima do limite" if dif > LIMITE_PP else "dentro do limite")


def relatorio(res_painel, res_robo, dados_versoes=None):
    linhas = comum.cabecalho("Desempenho por subgrupo", dados_versoes)
    linhas += [f"Limite de diferença entre subgrupos: {comum.num(LIMITE_PP, 0)} pontos percentuais, calculado só "
               f"entre grupos com {AMOSTRA_MINIMA} casos ou mais.", ""]
    for cultura, r in res_painel.items():
        linhas += [f"## Painel: igualdade de oportunidade por UF ({cultura})", "",
                   "| UF | Pares município-safra | Pares com perda real ≥ 40% | Sensibilidade | Acerto |",
                   "|---|---|---|---|---|"]
        for t in r["tabela"]:
            sens = comum.pct(t["sensibilidade"]) if t["sensibilidade"] is not None else "n/d"
            linhas.append(f"| {t['uf']} | {t['n']} | {t['com_perda']} | {sens} | {comum.pct(t['acuracia'])} |")
        linhas += ["", f"Geral: sensibilidade {comum.pct(r['sensibilidade_geral'])}, acerto {comum.pct(r['geral'])}.",
                   f"Diferença máxima de sensibilidade: {_situacao(r['diferenca_pp'])}. "
                   f"Diferença máxima de acerto: {_situacao(r['diferenca_acerto_pp'])}.", ""]
    nomes = {"uf": ("UF", "UF"), "servico_real": ("serviço", "Serviço")}
    for grupo, r in res_robo.items():
        linhas += [f"## Robô: decisão por {nomes[grupo][0]}", "",
                   f"| {nomes[grupo][1]} | Pedidos | Decisão correta | Revisão humana | Erro grave |",
                   "|---|---|---|---|---|"]
        linhas += [f"| {t['grupo']} | {t['n']} | {comum.pct(t['decisao_correta'])} | {comum.pct(t['revisao_humana'])} | "
                   f"{int(t['erro_grave'])} |" for t in r["tabela"]]
        linhas += ["", f"Erro grave em todos os grupos somados: {r['erro_grave_total']}. Diferença de decisão correta: "
                       f"{_situacao(r['diferenca_pp'])}.", ""]
    return "\n".join(linhas)


def main():
    try:
        dados_versoes = comum.versoes()
        comum.verificar_versoes(dados_versoes)
        res_painel = painel(comum.placar_dashboard(dados_versoes))
        res_robo = robo(comum.pasta("rpa", dados_versoes))
    except (FileNotFoundError, RuntimeError, KeyError) as erro:
        print(f"Não foi possível calcular os subgrupos: {erro}")
        return 1
    comum.gravar("subgrupos", relatorio(res_painel, res_robo, dados_versoes),
                 {"painel": res_painel, "robo": res_robo})
    for cultura, r in res_painel.items():
        print(f"Painel {cultura}: sensibilidade entre UFs {_situacao(r['diferenca_pp'])}")
    for grupo, r in res_robo.items():
        print(f"Robô por {grupo}: {_situacao(r['diferenca_pp'])}; erro grave {r['erro_grave_total']}")
    print("Relatório: evidencias/subgrupos.md")
    return 0


if __name__ == "__main__":
    sys.exit(main())
