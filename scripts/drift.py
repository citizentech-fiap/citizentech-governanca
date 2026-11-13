"""Mudança de distribuição da chuva entre safras (PSI) e o acerto do painel em cada safra.

Variável monitorada: chuva acumulada em 30 dias dividida pela normal 1991-2020 do mesmo período,
para cada município e cada dia da safra (janeiro a junho). Para cada safra, a referência é o conjunto
das demais safras do histórico do painel. Faixas de PSI: abaixo de 0,10 estável; de 0,10 a 0,20
investigar; acima de 0,20 mudança relevante.

    python scripts/drift.py
"""
import sys

import numpy as np
import pandas as pd

import comum

JANELA_DIAS = 30
FAIXAS = 10


def razao_chuva(pasta_dashboard):
    clima = pd.read_csv(pasta_dashboard / "data/clima_diario.csv", parse_dates=["data"])
    normal = pd.read_csv(pasta_dashboard / "data/climatologia.csv")
    clima = clima.sort_values(["cod_ibge", "data"])
    clima["dia_ano"] = clima.data.dt.day_of_year.clip(upper=365)
    clima = clima.merge(normal[["cod_ibge", "dia_ano", "chuva_media_mm"]], on=["cod_ibge", "dia_ano"], how="left")
    agrupado = clima.groupby("cod_ibge")
    clima["obs_30d"] = agrupado.chuva_mm.transform(lambda s: s.rolling(JANELA_DIAS, min_periods=JANELA_DIAS).sum())
    clima["normal_30d"] = agrupado.chuva_media_mm.transform(
        lambda s: s.rolling(JANELA_DIAS, min_periods=JANELA_DIAS).sum())
    clima = clima[clima.data.dt.month.le(6) & clima.normal_30d.gt(0)].dropna(subset=["obs_30d"])
    clima["safra"] = clima.data.dt.year
    clima["razao"] = clima.obs_30d / clima.normal_30d
    return clima[["cod_ibge", "safra", "data", "razao"]]


def psi(referencia, atual, faixas=FAIXAS):
    cortes = np.unique(np.quantile(referencia, np.linspace(0, 1, faixas + 1)))
    cortes[0], cortes[-1] = -np.inf, np.inf
    ref = np.histogram(referencia, cortes)[0] / len(referencia)
    obs = np.histogram(atual, cortes)[0] / len(atual)
    ref, obs = np.clip(ref, 1e-4, None), np.clip(obs, 1e-4, None)
    return float(np.sum((obs - ref) * np.log(obs / ref)))


def classificar(valor):
    return "estável" if valor < 0.10 else ("investigar" if valor <= 0.20 else "mudança relevante")


def calcular(dados_versoes=None):
    dados_versoes = dados_versoes or comum.versoes()
    serie = razao_chuva(comum.pasta("dashboard", dados_versoes))
    placar = comum.placar_dashboard(dados_versoes)["milho"]["por_ano"]
    linhas = []
    for safra, grupo in serie.groupby("safra"):
        ref = serie.loc[serie.safra.ne(safra), "razao"].to_numpy()
        valor = psi(ref, grupo.razao.to_numpy())
        acerto = placar.get(str(safra)) or placar.get(safra)
        linhas.append(dict(safra=int(safra), psi=valor, faixa=classificar(valor),
                           mediana_razao=float(grupo.razao.median()),
                           acuracia_milho=acerto["acuracia"] if acerto else None,
                           pares=acerto["n"] if acerto else 0))
    tabela = pd.DataFrame(linhas)
    com_placar = tabela.dropna(subset=["acuracia_milho"])
    correlacao = (float(com_placar.psi.rank().corr(com_placar.acuracia_milho.rank()))
                  if len(com_placar) > 2 else float("nan"))
    return tabela, correlacao


def relatorio(tabela, correlacao, dados_versoes=None):
    linhas = comum.cabecalho("Mudança de distribuição da chuva por safra (PSI)", dados_versoes)
    linhas += [f"Variável: chuva de {JANELA_DIAS} dias dividida pela normal 1991-2020, por município e dia, "
               "de janeiro a junho. Referência de cada safra: as demais safras do histórico.", "",
               "| Safra | PSI | Faixa | Chuva / normal (mediana) | Acerto do painel, milho | Pares |",
               "|---|---|---|---|---|---|"]
    for t in tabela.itertuples():
        acerto = comum.pct(t.acuracia_milho) if t.acuracia_milho == t.acuracia_milho and t.acuracia_milho is not None \
            else "sem dado do IBGE"
        linhas.append(f"| {t.safra} | {comum.num(t.psi)} | {t.faixa} | {comum.num(t.mediana_razao)} | {acerto} | "
                      f"{t.pares} |")
    linhas += ["", f"Correlação de postos entre PSI e acerto do painel (safras com placar): {comum.num(correlacao)}."]
    com_placar = tabela.dropna(subset=["acuracia_milho"])
    if len(com_placar) > 2:
        extremas = ", ".join(str(s) for s in com_placar.nlargest(2, "psi").safra)
        piores = ", ".join(str(s) for s in com_placar.nsmallest(2, "acuracia_milho").safra)
        sentido = ("o acerto é maior nas safras em que a chuva mais se afastou do histórico"
                   if correlacao > 0 else "o acerto cai nas safras em que a chuva mais se afastou do histórico")
        linhas.append(f"Leitura: {sentido}. Maiores PSI: {extremas}. Menores acertos: {piores}.")
    return "\n".join(linhas + [""])


def main():
    try:
        dados_versoes = comum.versoes()
        tabela, correlacao = calcular(dados_versoes)
    except (FileNotFoundError, RuntimeError, KeyError) as erro:
        print(f"Não foi possível calcular o PSI: {erro}")
        return 1
    comum.gravar("drift", relatorio(tabela, correlacao, dados_versoes),
                 {"safras": tabela.to_dict("records"), "correlacao_psi_acerto": correlacao})
    for t in tabela.itertuples():
        print(f"{t.safra}: PSI {comum.num(t.psi)} ({t.faixa})")
    print("Relatório: evidencias/drift.md")
    return 0


if __name__ == "__main__":
    sys.exit(main())
