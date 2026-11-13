"""Desempenho por subgrupo (equidade) nos módulos que influenciam o acesso a benefício.

Painel: acerto do critério de 40% contra a perda real do IBGE, por UF.
Robô: decisão correta e envio para revisão humana, por UF e por serviço.
A diferença máxima entre subgrupos é comparada com o limite de 5 pontos percentuais.
Subgrupos com menos de 30 casos são marcados como amostra pequena.

    python scripts/subgrupos.py
"""
import sys

import pandas as pd

import comum

LIMITE_PP = 5.0
AMOSTRA_MINIMA = 30


def _diferenca(tabela, coluna):
    validos = tabela[tabela.n >= AMOSTRA_MINIMA]
    base = validos if len(validos) >= 2 else tabela
    return (base[coluna].max() - base[coluna].min()) * 100, len(validos) >= 2


def painel(placar):
    saida = {}
    for cultura, dados in placar.items():
        tabela = pd.DataFrame([{"uf": uf, "acuracia": v["acuracia"], "n": v["n"]}
                               for uf, v in sorted(dados["por_uf"].items())])
        dif, robusta = _diferenca(tabela, "acuracia")
        saida[cultura] = dict(tabela=tabela.to_dict("records"), diferenca_pp=dif, so_amostras_grandes=robusta,
                              geral=dados["acuracia"])
    return saida


def robo(pasta_rpa):
    res = pd.read_csv(pasta_rpa / "eval/resultados_robo.csv")
    labels = pd.read_csv(pasta_rpa / "data/synthetic/labels.csv")[["request_id", "uf"]]
    base = res.merge(labels, on="request_id", how="left", validate="one_to_one")
    base["acerto"] = base.decisao_ok.astype(str).str.lower().eq("true")
    base["revisao"] = base.decisao.eq("revisao_humana")
    saida = {}
    for grupo in ("uf", "servico_real"):
        tabela = (base.groupby(grupo).agg(n=("request_id", "size"), decisao_correta=("acerto", "mean"),
                                          revisao_humana=("revisao", "mean")).reset_index()
                  .rename(columns={grupo: "grupo"}))
        dif, robusta = _diferenca(tabela, "decisao_correta")
        saida[grupo] = dict(tabela=tabela.to_dict("records"), diferenca_pp=dif, so_amostras_grandes=robusta)
    return saida


def _situacao(dif, robusta):
    texto = "acima do limite" if dif > LIMITE_PP else "dentro do limite"
    return texto if robusta else f"{texto} (amostras pequenas, sinal fraco)"


def relatorio(res_painel, res_robo, dados_versoes=None):
    linhas = comum.cabecalho("Desempenho por subgrupo", dados_versoes)
    linhas += [f"Limite de diferença entre subgrupos: {comum.num(LIMITE_PP, 0)} pontos percentuais. "
               f"Subgrupo com menos de {AMOSTRA_MINIMA} casos: amostra pequena.", ""]
    for cultura, r in res_painel.items():
        linhas += [f"## Painel: acerto do critério de 40% por UF ({cultura})", "",
                   "| UF | Pares município-safra | Acerto |", "|---|---|---|"]
        linhas += [f"| {t['uf']} | {t['n']} | {comum.pct(t['acuracia'])} |" for t in r["tabela"]]
        linhas += ["", f"Geral: {comum.pct(r['geral'])}. Diferença máxima: {comum.num(r['diferenca_pp'], 1)} p.p., "
                       f"{_situacao(r['diferenca_pp'], r['so_amostras_grandes'])}.", ""]
    nomes = {"uf": ("UF", "UF"), "servico_real": ("serviço", "Serviço")}
    for grupo, r in res_robo.items():
        linhas += [f"## Robô: decisão correta por {nomes[grupo][0]}", "",
                   f"| {nomes[grupo][1]} | Pedidos | Decisão correta | Revisão humana |", "|---|---|---|---|"]
        linhas += [f"| {t['grupo']} | {t['n']} | {comum.pct(t['decisao_correta'])} | {comum.pct(t['revisao_humana'])} |"
                   for t in r["tabela"]]
        linhas += ["", f"Diferença máxima de decisão correta: {comum.num(r['diferenca_pp'], 1)} p.p., "
                       f"{_situacao(r['diferenca_pp'], r['so_amostras_grandes'])}.", ""]
    return "\n".join(linhas)


def main():
    try:
        dados_versoes = comum.versoes()
        res_painel = painel(comum.placar_dashboard(dados_versoes))
        res_robo = robo(comum.pasta("rpa", dados_versoes))
    except (FileNotFoundError, RuntimeError, KeyError) as erro:
        print(f"Não foi possível calcular os subgrupos: {erro}")
        return 1
    comum.gravar("subgrupos", relatorio(res_painel, res_robo, dados_versoes),
                 {"painel": res_painel, "robo": res_robo})
    for cultura, r in res_painel.items():
        print(f"Painel {cultura}: diferença entre UFs {comum.num(r['diferenca_pp'], 1)} p.p.")
    for grupo, r in res_robo.items():
        print(f"Robô por {grupo}: diferença {comum.num(r['diferenca_pp'], 1)} p.p.")
    print("Relatório: evidencias/subgrupos.md")
    return 0


if __name__ == "__main__":
    sys.exit(main())
