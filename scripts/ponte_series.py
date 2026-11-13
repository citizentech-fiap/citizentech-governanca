"""Ponte entre séries do RFC-03: perda estimada antes e depois da calibração pela normal 1991-2020.

v1 (até o commit 9371172): perda = 100 x Ky x (1 - ISNA_ano), limitada a 0 e 100.
v2 (atual):                perda = 100 x Ky x (1 - ISNA_ano / ISNA_normal), limitada a 0 e 100.

As duas versões são calculadas sobre os mesmos dados e comparadas com a perda real do IBGE, usando o
código do próprio painel. Saída: evidencias/rfc03_ponte_series.md.

    python scripts/ponte_series.py
"""
import sys

import comum

CODIGO = """
import json
import pandas as pd
from pipelines import risco
from pipelines.realidade import perda_real
from providers.config import carregar
cfg = carregar()
lim = cfg["risco"]["criterio_garantia_safra"]
anos = [a for a in cfg["safra"]["anos_disponiveis"] if a <= cfg["fontes"]["pam_fim"]]
saida = {}
for cultura, par in cfg["modelo_hidrico"]["culturas"].items():
    est = pd.concat([risco.indicadores(a, cultura).assign(ano=a) for a in anos], ignore_index=True)
    est["perda_v1"] = (100 * par["ky"] * (1 - est.isna_ano)).clip(0, 100)
    base = est.merge(perda_real(cultura)[["cod_ibge", "ano", "perda_producao_pct"]], on=["cod_ibge", "ano"])
    base = base.dropna(subset=["perda_estimada_pct", "perda_producao_pct"])
    real = base.perda_producao_pct.ge(lim)
    def medir(col):
        e = base[col].ge(lim)
        sens, espec = float(e[real].mean()), float((~e)[~real].mean())
        return dict(acuracia=float(e.eq(real).mean()),
                    spearman=float(base[col].rank().corr(base.perda_producao_pct.rank())),
                    sinalizados=float(e.mean()), sensibilidade=sens, especificidade=espec,
                    acuracia_balanceada=(sens + espec) / 2)
    saida[cultura] = dict(v1=medir("perda_v1"), v2=medir("perda_estimada_pct"), pares=len(base),
                          real_ge_40=float(real.mean()),
                          por_ano={int(a): dict(v1=float(g.perda_v1.median()), v2=float(g.perda_estimada_pct.median()))
                                   for a, g in base.groupby("ano")})
print(json.dumps(saida))
"""


def relatorio(dados, dados_versoes=None):
    linhas = comum.cabecalho("RFC-03: ponte entre séries da perda estimada", dados_versoes)
    linhas += ["v1: perda = 100 x Ky x (1 - ISNA_ano). v2: perda = 100 x Ky x (1 - ISNA_ano / ISNA_normal).",
               "Mesmos dados de chuva e ET0; referência: perda real do IBGE no critério de 40%.", ""]
    for cultura, r in dados.items():
        linhas += [f"## {cultura.capitalize()} ({r['pares']} pares município-safra)", "",
                   "| Medida | v1 | v2 |", "|---|---|---|",
                   f"| Acerto do critério de 40% | {comum.pct(r['v1']['acuracia'])} | {comum.pct(r['v2']['acuracia'])} |",
                   f"| Correlação de postos com a perda real | {comum.num(r['v1']['spearman'])} | "
                   f"{comum.num(r['v2']['spearman'])} |",
                   f"| Perdas reais sinalizadas (sensibilidade) | {comum.pct(r['v1']['sensibilidade'])} | "
                   f"{comum.pct(r['v2']['sensibilidade'])} |",
                   f"| Safras sem perda reconhecidas (especificidade) | {comum.pct(r['v1']['especificidade'])} | "
                   f"{comum.pct(r['v2']['especificidade'])} |",
                   f"| Acerto balanceado | {comum.pct(r['v1']['acuracia_balanceada'])} | "
                   f"{comum.pct(r['v2']['acuracia_balanceada'])} |",
                   f"| Pares sinalizados com perda ≥ 40% | {comum.pct(r['v1']['sinalizados'])} | "
                   f"{comum.pct(r['v2']['sinalizados'])} |",
                   f"| Pares com perda real ≥ 40% (IBGE) | {comum.pct(r['real_ge_40'])} | {comum.pct(r['real_ge_40'])} |",
                   "", "| Safra | Perda mediana v1 | Perda mediana v2 |", "|---|---|---|"]
        linhas += [f"| {ano} | {comum.num(v['v1'], 1)}% | {comum.num(v['v2'], 1)}% |" for ano, v in r["por_ano"].items()]
        linhas.append("")
    return "\n".join(linhas)


def main():
    try:
        dados_versoes = comum.versoes()
        comum.verificar_versoes(dados_versoes)
        dados = comum.python_no_modulo(comum.pasta("dashboard", dados_versoes), CODIGO)
    except (FileNotFoundError, RuntimeError, KeyError) as erro:
        print(f"Não foi possível calcular a ponte entre séries: {erro}")
        return 1
    comum.gravar("rfc03_ponte_series", relatorio(dados, dados_versoes), dados)
    for cultura, r in dados.items():
        print(f"{cultura}: acerto v1 {comum.pct(r['v1']['acuracia'])} -> v2 {comum.pct(r['v2']['acuracia'])}")
    print("Relatório: evidencias/rfc03_ponte_series.md")
    return 0


if __name__ == "__main__":
    sys.exit(main())
