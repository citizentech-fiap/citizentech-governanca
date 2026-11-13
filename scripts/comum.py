"""Funções compartilhadas pelos scripts de governança. Tudo roda offline, sem LLM."""
import hashlib
import json
import os
import subprocess
import sys
from datetime import date
from pathlib import Path

import yaml

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

RAIZ = Path(__file__).resolve().parents[1]
EVIDENCIAS = RAIZ / "evidencias"
ARTEFATOS = RAIZ / "artefatos"


def versoes(arquivo=None):
    with open(arquivo or RAIZ / "versoes.yaml", encoding="utf-8") as entrada:
        return yaml.safe_load(entrada)["modulos"]


def pasta(modulo, dados=None):
    dados = dados or versoes()
    return (RAIZ / dados[modulo]["pasta"]).resolve()


def sha256(caminho):
    h = hashlib.sha256()
    with open(caminho, "rb") as entrada:
        for bloco in iter(lambda: entrada.read(1 << 20), b""):
            h.update(bloco)
    return h.hexdigest()


def git(pasta_repo, *args):
    saida = subprocess.run(["git", "-C", str(pasta_repo), *args], capture_output=True, text=True,
                           encoding="utf-8")
    if saida.returncode != 0:
        raise RuntimeError(saida.stderr.strip() or f"git {' '.join(args)} falhou")
    return saida.stdout.strip()


def python_no_modulo(pasta_repo, codigo, ambiente=None, timeout=600):
    """Executa código Python dentro da pasta de um módulo e devolve o JSON impresso por ele."""
    env = {**os.environ, "PYTHONIOENCODING": "utf-8", "PYTHONUTF8": "1", **(ambiente or {})}
    saida = subprocess.run([sys.executable, "-c", codigo], cwd=pasta_repo, capture_output=True, text=True,
                           encoding="utf-8", env=env, timeout=timeout)
    if saida.returncode != 0:
        raise RuntimeError(saida.stderr.strip().splitlines()[-1] if saida.stderr.strip() else "falha sem mensagem")
    return json.loads(saida.stdout.strip().splitlines()[-1])


_PLACAR = """
import json
from pipelines.realidade import validacao
from providers.config import carregar
cfg = carregar()
limiar = cfg["risco"]["criterio_garantia_safra"]
saida = {}
for cultura in cfg["modelo_hidrico"]["culturas"]:
    p = validacao(cultura)
    d = p["dados"]
    pares = d.dropna(subset=["perda_estimada_pct", "perda_producao_pct"])
    estimado, real = pares.perda_estimada_pct.ge(limiar), pares.perda_producao_pct.ge(limiar)
    acerto = estimado.eq(real)
    est = d.perda_estimada_pct.dropna()
    saida[cultura] = dict(
        acuracia=p["acuracia"], spearman=p["spearman"], pares=p["pares_validos"],
        sensibilidade=float(estimado[real].mean()), especificidade=float((~estimado)[~real].mean()),
        excluidos=p["pares_excluidos"], perda_min=float(est.min()), perda_max=float(est.max()),
        n_estimativas=int(len(est)), criterio=limiar,
        por_uf={uf: dict(acuracia=float(g.mean()), n=int(len(g))) for uf, g in acerto.groupby(pares.uf)},
        por_ano={int(a): dict(acuracia=float(g.mean()), n=int(len(g))) for a, g in acerto.groupby(pares.ano)})
print(json.dumps(saida))
"""


def placar_dashboard(dados_versoes=None):
    """Placar estimado x real calculado pelo código do próprio painel (nada é recalculado aqui)."""
    return python_no_modulo(pasta("dashboard", dados_versoes), _PLACAR)


def pct(valor, casas=1):
    if valor is None or valor != valor:
        return "n/d"
    return f"{valor * 100:.{casas}f}%".replace(".", ",")


def num(valor, casas=2):
    if valor is None or valor != valor:
        return "n/d"
    return f"{valor:.{casas}f}".replace(".", ",")


def gravar(nome, texto, dados=None):
    EVIDENCIAS.mkdir(exist_ok=True)
    (EVIDENCIAS / f"{nome}.md").write_text(texto, encoding="utf-8", newline="\n")
    if dados is not None:
        (EVIDENCIAS / f"{nome}.json").write_text(json.dumps(dados, ensure_ascii=False, indent=2, default=str),
                                                 encoding="utf-8", newline="\n")


def cabecalho(titulo, dados_versoes=None):
    dados_versoes = dados_versoes or versoes()
    linhas = [f"# {titulo}", "", f"Gerado em {date.today():%d/%m/%Y} sobre as versões de `versoes.yaml`:", ""]
    linhas += [f"- {m}: `{d['commit'][:7]}`" for m, d in dados_versoes.items()]
    return linhas + [""]
