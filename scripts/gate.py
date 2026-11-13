"""Gate de promoção dos módulos do CitizenTech.

Confere oito critérios por módulo sobre a versão registrada em versoes.yaml e grava o resultado em
evidencias/gate.md. Um critério bloqueante que falha reprova o módulo, a menos que exista exceção
válida em artefatos/excecoes.yaml (com motivo, mitigação, responsável e prazo).

    python scripts/gate.py               # completo, roda as suítes de teste dos três módulos
    python scripts/gate.py --sem-testes  # pula as suítes (resultado fica incompleto)
"""
import argparse
import os
import re
import subprocess
import sys
from datetime import date

import yaml

import comum
import golden
import metricas
import subgrupos

MODEL_CARDS = {"genai": "assistente_rag.md", "rpa": "classificador_triagem.md", "dashboard": "modelo_hidrico.md"}
SECOES_CARD = ["Detalhes", "Uso pretendido", "Dados", "Métricas", "Considerações éticas", "Limitações",
               "Monitoramento", "Explicabilidade"]
MC = {"genai": "MC-01", "rpa": "MC-02", "dashboard": "MC-03"}
ROTULO = {"genai": "| GenAI", "rpa": "| RPA", "dashboard": "| Dashboard"}

CRITERIOS = [
    ("rastreabilidade", "Rastreabilidade: código no commit registrado, sem alteração local", "Engenharia"),
    ("reprodutibilidade", "Reprodutibilidade: suíte de testes do módulo passa", "Engenharia"),
    ("referencia", "Conjuntos de referência sem alteração (hash SHA-256)", "Data Steward"),
    ("desempenho", "Desempenho: Metric Contract sem alerta crítico", "Metric Owner"),
    ("equidade", "Equidade: diferença entre subgrupos dentro de 5 p.p.", "Model Validator"),
    ("documentacao", "Model Card com as oito seções, incluindo explicabilidade", "Model Validator"),
    ("monitoramento", "Plano de monitoramento com seção do contrato do módulo", "Metric Owner"),
    ("lgpd", "Revisão LGPD: dados do módulo no inventário e RIPD", "Encarregado de dados"),
]


def rastreabilidade(modulo, dados):
    pasta = comum.pasta(modulo, dados)
    atual = comum.git(pasta, "rev-parse", "HEAD")
    sujo = comum.git(pasta, "status", "--porcelain", "--untracked-files=no")
    esperado = dados[modulo]["commit"]
    if atual != esperado:
        return False, f"HEAD em {atual[:7]}, registrado {esperado[:7]}"
    if sujo:
        return False, f"{len(sujo.splitlines())} arquivo(s) alterado(s) sem commit"
    return True, f"commit {atual[:7]}, árvore limpa"


def reprodutibilidade(modulo, dados):
    cfg = dados[modulo]["testes"]
    comando = [sys.executable if p == "python" else p for p in cfg["comando"]]
    env = {**os.environ, "PYTHONIOENCODING": "utf-8", **{k: str(v) for k, v in (cfg.get("ambiente") or {}).items()}}
    saida = subprocess.run(comando, cwd=comum.pasta(modulo, dados), capture_output=True, text=True,
                           encoding="utf-8", errors="replace", env=env, timeout=1800)
    texto = saida.stdout + saida.stderr
    ran = re.findall(r"Ran (\d+) tests?", texto)
    total = ran[-1] if ran else "?"
    if saida.returncode == 0:
        return True, f"{total} testes OK"
    falhas = re.findall(r"FAILED \((.*?)\)", texto)
    return False, f"{total} testes, falhou ({falhas[-1] if falhas else 'ver saída'})"


def referencia(modulo, conferencia):
    itens = [(rel, s) for m, rel, s in conferencia if m == modulo]
    diferentes = [f"{rel} ({s})" for rel, s in itens if s != "igual"]
    return (not diferentes, f"{len(itens)} arquivos iguais" if not diferentes else "; ".join(diferentes))


def desempenho(modulo, contratos):
    mc = next((c for c in contratos if c["modulo"] == modulo), None)
    if mc is None:
        return False, "sem Metric Contract"
    criticos = [a for a in mc["alertas"] if a["nivel"] == "critico"]
    outros = [a for a in mc["alertas"] if a["nivel"] != "critico"]
    texto = f"{mc['id']}: {metricas.formatar(mc['indicador']['valor'])}"
    if outros:
        texto += f"; {len(outros)} alerta(s) não crítico(s): " + ", ".join(a["metrica"] for a in outros)
    return (not criticos, texto if not criticos else f"{texto}; crítico: " + ", ".join(a["metrica"] for a in criticos))


def equidade(modulo, res_subgrupos):
    if modulo == "genai":
        return None, "não aplicável: as perguntas não têm atributo de grupo; risco tratado por abstenção"
    if modulo == "dashboard":
        difs = {f"sensibilidade {c}": r["diferenca_pp"] for c, r in res_subgrupos["painel"].items()}
        extra = ""
    else:
        difs = {f"decisão por {g}": r["diferenca_pp"] for g, r in res_subgrupos["robo"].items()}
        graves = res_subgrupos["robo"]["uf"]["erro_grave_total"]
        extra = f"; erro grave em todos os grupos: {graves}"
    texto = "; ".join(f"{k}: " + (f"{comum.num(v, 1)} p.p." if v is not None else "amostra insuficiente")
                      for k, v in difs.items()) + extra
    ok = all(v is not None and v <= subgrupos.LIMITE_PP for v in difs.values())
    return ok, texto


def cobre_modulo(caminho, termos):
    if not caminho.exists():
        return False, f"{_nome(caminho)} ausente"
    texto = caminho.read_text(encoding="utf-8")
    faltando = [t for t in termos if t not in texto]
    return (not faltando, _nome(caminho) if not faltando else f"{_nome(caminho)} não cobre: " + ", ".join(faltando))


def _nome(caminho):
    try:
        return caminho.relative_to(comum.RAIZ).as_posix()
    except ValueError:
        return caminho.name


def documento(caminho, secoes=None):
    if not caminho.exists():
        return False, f"{_nome(caminho)} ausente"
    if secoes:
        titulos = re.findall(r"^##\s+(.+)$", caminho.read_text(encoding="utf-8"), flags=re.M)
        faltando = [s for s in secoes if not any(t.strip().startswith(s) for t in titulos)]
        if faltando:
            return False, "faltam seções: " + ", ".join(faltando)
    return True, _nome(caminho)


def excecoes_validas(arquivo=None, hoje=None):
    arquivo = arquivo or comum.ARTEFATOS / "excecoes.yaml"
    if not arquivo.exists():
        return {}
    dados = yaml.safe_load(arquivo.read_text(encoding="utf-8"))["excecoes"]
    hoje = hoje or date.today()
    return {(e["modulo"], e["criterio"]): e for e in dados if date.fromisoformat(str(e["prazo"])) >= hoje}


def avaliar(rodar_testes=True):
    dados = comum.versoes()
    conferencia = golden.conferir(dados)
    contratos = metricas.calcular(dados)
    res_sub = {"painel": subgrupos.painel(comum.placar_dashboard(dados)),
               "robo": subgrupos.robo(comum.pasta("rpa", dados))}
    excecoes = excecoes_validas()
    resultado = {}
    for modulo in dados:
        checagens = {
            "rastreabilidade": rastreabilidade(modulo, dados),
            "reprodutibilidade": reprodutibilidade(modulo, dados) if rodar_testes else (None, "não executado"),
            "referencia": referencia(modulo, conferencia),
            "desempenho": desempenho(modulo, contratos),
            "equidade": equidade(modulo, res_sub),
            "documentacao": documento(comum.ARTEFATOS / "model_cards" / MODEL_CARDS[modulo], SECOES_CARD),
            "monitoramento": cobre_modulo(comum.ARTEFATOS / "plano_monitoramento.md", [f"({MC[modulo]})"]),
            "lgpd": (lambda r: (all(x[0] for x in r), "; ".join(x[1] for x in r)))(
                [cobre_modulo(comum.ARTEFATOS / "lgpd/inventario_dados.md", [ROTULO[modulo]]),
                 documento(comum.ARTEFATOS / "lgpd/ripd_simplificado.md")]),
        }
        linhas, situacao = [], "aprovado"
        for chave, nome, papel in CRITERIOS:
            ok, detalhe = checagens[chave]
            if ok is False and (modulo, chave) in excecoes:
                ex = excecoes[(modulo, chave)]
                estado = f"exceção {ex['id']}"
                detalhe += f" (exceção até {ex['prazo']}, responsável: {ex['responsavel']})"
                situacao = "aprovado com exceção" if situacao == "aprovado" else situacao
            elif ok is False:
                estado, situacao = "reprovado", "reprovado"
            elif ok is None and chave == "reprodutibilidade":
                estado = "não executado"
                situacao = "incompleto" if situacao != "reprovado" else situacao
            else:
                estado = "ok" if ok else "não se aplica"
            linhas.append(dict(criterio=nome, papel=papel, estado=estado, detalhe=detalhe))
        resultado[modulo] = dict(situacao=situacao, criterios=linhas, commit=dados[modulo]["commit"])
    return resultado, dados


def relatorio(resultado, dados):
    linhas = comum.cabecalho("Gate de promoção", dados)
    linhas += ["| Módulo | Commit | Resultado |", "|---|---|---|"]
    linhas += [f"| {m} | `{r['commit'][:7]}` | **{r['situacao']}** |" for m, r in resultado.items()]
    linhas.append("")
    for modulo, r in resultado.items():
        linhas += [f"## {modulo} ({dados[modulo]['disciplina']})", "",
                   "| # | Critério | Papel | Situação | Detalhe |", "|---|---|---|---|---|"]
        linhas += [f"| {i} | {c['criterio']} | {c['papel']} | {c['estado']} | {c['detalhe']} |"
                   for i, c in enumerate(r["criterios"], 1)]
        linhas.append("")
    linhas += ["Este registro é gerado por script e não substitui a aprovação do Metric Owner de cada módulo, "
               "definida em artefatos/raci.md.", ""]
    return "\n".join(linhas)


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--sem-testes", action="store_true")
    args = parser.parse_args()
    try:
        resultado, dados = avaliar(rodar_testes=not args.sem_testes)
    except (FileNotFoundError, RuntimeError, KeyError, subprocess.TimeoutExpired) as erro:
        print(f"Gate não concluído: {erro}")
        return 2
    comum.gravar("gate", relatorio(resultado, dados), resultado)
    for modulo, r in resultado.items():
        print(f"{modulo}: {r['situacao']}")
    print("Relatório: evidencias/gate.md")
    return 1 if any(r["situacao"] == "reprovado" for r in resultado.values()) else 0


if __name__ == "__main__":
    sys.exit(main())
