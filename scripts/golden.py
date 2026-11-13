"""Hash SHA-256 dos conjuntos de referência de cada módulo (golden datasets).

Os conjuntos de teste, validação, rótulos e snapshots de dados não podem mudar sem registro: uma
mudança silenciosa invalida a comparação entre versões. Este script registra os hashes atuais ou
confere se continuam iguais aos registrados.

    python scripts/golden.py              # confere
    python scripts/golden.py --registrar  # registra (só junto com uma mudança de versoes.yaml)
"""
import argparse
import json
import sys

import comum

ARQUIVO = comum.RAIZ / "golden" / "hashes.json"


def calcular(dados_versoes=None):
    dados_versoes = dados_versoes or comum.versoes()
    hashes = {}
    for modulo, dados in dados_versoes.items():
        base = comum.pasta(modulo, dados_versoes)
        hashes[modulo] = {rel: comum.sha256(base / rel) for rel in dados["conjuntos_referencia"]}
    return hashes


def conferir(dados_versoes=None):
    """Lista de (módulo, arquivo, situação); situação é 'igual', 'alterado', 'novo' ou 'ausente'."""
    registrados = json.loads(ARQUIVO.read_text(encoding="utf-8"))["hashes"]
    resultado = []
    for modulo, arquivos in (dados_versoes or comum.versoes()).items():
        base = comum.pasta(modulo, dados_versoes)
        for rel in arquivos["conjuntos_referencia"]:
            esperado = registrados.get(modulo, {}).get(rel)
            if not (base / rel).exists():
                situacao = "ausente"
            elif esperado is None:
                situacao = "novo"
            else:
                situacao = "igual" if comum.sha256(base / rel) == esperado else "alterado"
            resultado.append((modulo, rel, situacao))
    return resultado


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--registrar", action="store_true")
    args = parser.parse_args()
    if args.registrar:
        ARQUIVO.parent.mkdir(exist_ok=True)
        dados_versoes = comum.versoes()
        conteudo = {"commits": {m: d["commit"] for m, d in dados_versoes.items()}, "hashes": calcular(dados_versoes)}
        ARQUIVO.write_text(json.dumps(conteudo, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(f"Hashes registrados em {ARQUIVO.relative_to(comum.RAIZ)}")
        return 0
    resultado = conferir()
    for modulo, rel, situacao in resultado:
        print(f"{situacao:9} {modulo}: {rel}")
    return 0 if all(s == "igual" for _, _, s in resultado) else 1


if __name__ == "__main__":
    sys.exit(main())
