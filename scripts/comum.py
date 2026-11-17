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
    """Hash do conteúdo com quebras de linha normalizadas (CRLF -> LF).

    Os repositórios guardam texto em LF (.gitattributes), mas uma cópia de trabalho no Windows pode estar em CRLF.
    Sem normalizar, o mesmo conteúdo teria hashes diferentes na máquina de quem registrou e num clone novo.
    """
    with open(caminho, "rb") as entrada:
        conteudo = entrada.read()
    return hashlib.sha256(conteudo.replace(b"\r\n", b"\n")).hexdigest()


def git(pasta_repo, *args):
    saida = subprocess.run(["git", "-C", str(pasta_repo), *args], capture_output=True, text=True,
                           encoding="utf-8")
    if saida.returncode != 0:
        raise RuntimeError(saida.stderr.strip() or f"git {' '.join(args)} falhou")
    return saida.stdout.strip()


def verificar_versoes(dados=None):
    """Interrompe se algum módulo não estiver no commit registrado ou se um conjunto de referência mudou."""
    dados = dados or versoes()
    registrados = json.loads((RAIZ / "golden" / "hashes.json").read_text(encoding="utf-8"))["hashes"]
    problemas = []
    for modulo, d in dados.items():
        base = pasta(modulo, dados)
        atual = git(base, "rev-parse", "HEAD")
        if atual != d["commit"]:
            problemas.append(f"{modulo} em {atual[:7]}, registrado {d['commit'][:7]}")
        if git(base, "status", "--porcelain", "--untracked-files=no"):
            problemas.append(f"{modulo} com alteração local sem commit")
        for rel in d["conjuntos_referencia"]:
            if not (base / rel).exists() or sha256(base / rel) != registrados.get(modulo, {}).get(rel):
                problemas.append(f"{modulo}: {rel} diferente do registrado")
    if problemas:
        raise RuntimeError("versões não conferem: " + "; ".join(problemas))


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
        por_uf={uf: dict(acuracia=float(acerto[g.index].mean()), n=int(len(g)), com_perda=int(real[g.index].sum()),
                         sensibilidade=float(estimado[g.index][real[g.index]].mean()) if real[g.index].any() else None)
                for uf, g in pares.groupby("uf")},
        por_ano={int(a): dict(acuracia=float(acerto[g.index].mean()), n=int(len(g)),
                              real_ge=float(real[g.index].mean()), estimado_ge=float(estimado[g.index].mean()))
                 for a, g in pares.groupby("ano")})
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
    linhas = [f"# {titulo}", "", f"Gerado em {date.today():%d/%m/%Y} sobre as versões de `versoes.yaml`, depois de "
                                 "conferir os commits e o hash dos conjuntos de referência:", ""]
    linhas += [f"- {m}: `{d['commit'][:7]}`" for m, d in dados_versoes.items()]
    return linhas + [""]
