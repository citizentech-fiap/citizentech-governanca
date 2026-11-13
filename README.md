# CitizenTech: governança de IA e Business Analytics

Global Solution 2026.2 · FIAP · Governança em IA e Business Analytics · Turma 2TIAPF

Este repositório reúne a governança dos três módulos do CitizenTech, a solução que ajuda o agricultor
familiar do semiárido atingido pela seca a acessar serviços públicos (Garantia-Safra, CAF, Pronaf,
benefícios rurais). Aqui ficam os documentos de governança e os scripts que verificam, sobre o código
entregue, se cada módulo cumpre o que esses documentos prometem.

## Integrantes

| Nome completo | RM |
|---|---|
| Luís Fernando de Oliveira Salgado | RM561401 |
| Ricardo de Paiva Melo | RM565522 |
| Jonas Alaf | RM566479 |

## Módulos governados

| Repositório | Disciplina | Papel na solução |
|---|---|---|
| [`citizentech-rpa`](https://github.com/citizentech-fiap/citizentech-rpa) | AI for RPA | coleta as Cartas de Serviço do gov.br e faz a pré-triagem dos pedidos |
| [`citizentech-genai`](https://github.com/citizentech-fiap/citizentech-genai) | Generative AI | assistente que responde com citação das fontes oficiais |
| [`citizentech-dashboard`](https://github.com/citizentech-fiap/citizentech-dashboard) | Front-end | painel de decisão do gestor público |

A versão de cada módulo coberta por esta governança está em [`versoes.yaml`](versoes.yaml).

## Resultado atual

| Módulo | Risco | Metric Contract | Gate de promoção |
|---|---|---|---|
| RPA | alto | [MC-02](artefatos/metric_contracts/MC-02.yaml): decisão correta 83,3%, erro grave 0 | aprovado com exceção [EX-02](artefatos/excecoes.yaml) |
| GenAI | limitado | [MC-01](artefatos/metric_contracts/MC-01.yaml): 22 de 22 corretas no teste, 6 de 6 na validação | aprovado |
| Dashboard | alto | [MC-03](artefatos/metric_contracts/MC-03.yaml): acerto de 63,0% contra o IBGE, sensibilidade de 51,2% (alerta) | aprovado com exceção [EX-01](artefatos/excecoes.yaml) |

Detalhe em [`evidencias/gate.md`](evidencias/gate.md) e [`evidencias/metricas.md`](evidencias/metricas.md).

## Como reproduzir

Os quatro repositórios ficam lado a lado na mesma pasta:

```bash
git clone https://github.com/citizentech-fiap/citizentech-rpa.git RPA
git clone https://github.com/citizentech-fiap/citizentech-genai.git genAI
git clone https://github.com/citizentech-fiap/citizentech-dashboard.git dashboard
git clone https://github.com/citizentech-fiap/citizentech-governanca.git governanca
```

Ambiente único para os quatro (Python 3.11 ou mais novo):

```bash
python -m venv .venv
.venv/Scripts/python -m pip install -e genAI -r RPA/requirements.txt -r dashboard/requirements.txt -r governanca/requirements.txt
```

Dentro de `governanca/`, nenhum script usa rede ou chave de API:

| Comando | O que faz | Saída |
|---|---|---|
| `python scripts/golden.py` | confere o hash dos conjuntos de referência | terminal |
| `python scripts/metricas.py` | recalcula os três Metric Contracts e dispara alertas | `evidencias/metricas.md` |
| `python scripts/subgrupos.py` | acerto por UF no painel; decisão por UF e serviço no robô | `evidencias/subgrupos.md` |
| `python scripts/drift.py` | PSI da chuva por safra ao lado do acerto do painel | `evidencias/drift.md` |
| `python scripts/ponte_series.py` | perda estimada antes e depois do RFC-03 | `evidencias/rfc03_ponte_series.md` |
| `python scripts/gate.py` | oito critérios por módulo, incluindo as suítes de teste dos três | `evidencias/gate.md` |
| `python -m unittest discover -s tests -q` | testes dos próprios scripts | terminal |

O gate só gera evidência se cada módulo estiver no commit de `versoes.yaml` e sem alteração local.

## Mapa dos artefatos

| Conteúdo da disciplina | Arquivo |
|---|---|
| Classificação de risco (EU AI Act, PL 2.338/2023) | [`artefatos/classificacao_risco.md`](artefatos/classificacao_risco.md) |
| Papéis e RACI | [`artefatos/raci.md`](artefatos/raci.md) |
| NIST AI RMF aplicado | [`artefatos/nist_ai_rmf.md`](artefatos/nist_ai_rmf.md) |
| Linhagem dos dados e integração | [`artefatos/linhagem.md`](artefatos/linhagem.md) |
| Model Cards | [`artefatos/model_cards/`](artefatos/model_cards/) |
| Metric Contracts (modelo da disciplina e YAML executável) | [`artefatos/metric_contracts/`](artefatos/metric_contracts/) |
| RFCs com ponte entre séries | [`artefatos/rfc/`](artefatos/rfc/) |
| Gate de promoção e exceções | [`artefatos/checklists/gate_promocao.md`](artefatos/checklists/gate_promocao.md), [`artefatos/excecoes.yaml`](artefatos/excecoes.yaml) |
| Plano de monitoramento | [`artefatos/plano_monitoramento.md`](artefatos/plano_monitoramento.md) |
| Checklists de ética, equidade e LGPD | [`artefatos/checklists/`](artefatos/checklists/) |
| LGPD: inventário, RIPD e termo de consentimento | [`artefatos/lgpd/`](artefatos/lgpd/) |
| Maturidade (DAMA-DMBOK2, MLOps) e roadmap | [`artefatos/maturidade_roadmap.md`](artefatos/maturidade_roadmap.md) |
| Antipadrões evitados e presentes | [`artefatos/antipadroes.md`](artefatos/antipadroes.md) |
| Disciplinas da GS não integradas e motivo | [`artefatos/disciplinas_nao_integradas.md`](artefatos/disciplinas_nao_integradas.md) |

## Relatório

[`relatorio/CitizenTech_Governanca.docx`](relatorio/CitizenTech_Governanca.docx), no formato ABNT. Ao abrir no
Word, aceite a atualização dos campos para montar o sumário e as listas de figuras e quadros.

## Links

- Vídeo:
- RPA: https://github.com/citizentech-fiap/citizentech-rpa
- GenAI: https://github.com/citizentech-fiap/citizentech-genai
- Dashboard: https://github.com/citizentech-fiap/citizentech-dashboard

## Licença

MIT. Ver [`LICENSE`](LICENSE).
