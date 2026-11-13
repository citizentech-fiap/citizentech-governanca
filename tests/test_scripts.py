import json
import sys
import tempfile
import unittest
from datetime import date
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

import drift  # noqa: E402
import gate  # noqa: E402
import golden  # noqa: E402
import metricas  # noqa: E402


class TestPSI(unittest.TestCase):
    def test_mesma_distribuicao_fica_estavel(self):
        rng = np.random.default_rng(1)
        ref, atual = rng.gamma(2, 1, 5000), rng.gamma(2, 1, 5000)
        self.assertLess(drift.psi(ref, atual), 0.10)

    def test_distribuicao_deslocada_e_mudanca_relevante(self):
        rng = np.random.default_rng(2)
        ref, atual = rng.gamma(2, 1, 5000), rng.gamma(2, 1, 5000) * 0.3
        self.assertGreater(drift.psi(ref, atual), 0.20)

    def test_faixas(self):
        self.assertEqual(drift.classificar(0.05), "estável")
        self.assertEqual(drift.classificar(0.15), "investigar")
        self.assertEqual(drift.classificar(0.25), "mudança relevante")


class TestLimites(unittest.TestCase):
    def test_avaliar_limite(self):
        self.assertTrue(metricas.avaliar_limite(0.9, ">= 0.80"))
        self.assertFalse(metricas.avaliar_limite(1, "== 0"))
        self.assertIsNone(metricas.avaliar_limite(9, "informativo"))

    def test_formatacao_em_portugues(self):
        self.assertEqual(metricas.formatar(0.833), "83,3%")
        self.assertEqual(metricas.formatar(0.466, "spearman_milho"), "0,47")
        self.assertEqual(metricas.formatar_limite(">= 0.80", "x"), "≥ 80,0%")
        self.assertEqual(metricas.formatar_limite("<= 2", "x"), "≤ 2")


class TestGolden(unittest.TestCase):
    def test_detecta_arquivo_alterado(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp)
            (tmp / "mod").mkdir()
            dado = tmp / "mod" / "labels.csv"
            dado.write_text("a,b\n1,2\n", encoding="utf-8")
            versoes = {"m": {"pasta": str(tmp / "mod"), "conjuntos_referencia": ["labels.csv"]}}
            registro = tmp / "hashes.json"
            registro.write_text(json.dumps({"hashes": golden.calcular(versoes)}), encoding="utf-8")
            original, golden.ARQUIVO = golden.ARQUIVO, registro
            try:
                self.assertEqual(golden.conferir(versoes), [("m", "labels.csv", "igual")])
                dado.write_text("a,b\n1,3\n", encoding="utf-8")
                self.assertEqual(golden.conferir(versoes), [("m", "labels.csv", "alterado")])
            finally:
                golden.ARQUIVO = original


class TestGate(unittest.TestCase):
    def test_model_card_sem_secao_reprova(self):
        with tempfile.TemporaryDirectory() as tmp:
            card = Path(tmp) / "card.md"
            card.write_text("# Card\n\n## Detalhes do modelo\n\n## Uso pretendido\n", encoding="utf-8")
            ok, detalhe = gate.documento(card, gate.SECOES_CARD)
            self.assertFalse(ok)
            self.assertIn("Explicabilidade", detalhe)

    def test_excecao_vencida_nao_vale(self):
        with tempfile.TemporaryDirectory() as tmp:
            arquivo = Path(tmp) / "excecoes.yaml"
            arquivo.write_text("excecoes:\n  - {id: EX-9, modulo: rpa, criterio: equidade, prazo: 2026-01-01,"
                               " responsavel: x}\n", encoding="utf-8")
            self.assertIn(("rpa", "equidade"), gate.excecoes_validas(arquivo, hoje=date(2025, 12, 31)))
            self.assertEqual(gate.excecoes_validas(arquivo, hoje=date(2026, 1, 2)), {})


if __name__ == "__main__":
    unittest.main()
