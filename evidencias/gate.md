# Gate de promoção

Gerado em 13/11/2026 sobre as versões de `versoes.yaml`, depois de conferir os commits e o hash dos conjuntos de referência:

- genai: `e3f65dd`
- rpa: `c8dbe72`
- dashboard: `1514bb2`

| Módulo | Commit | Resultado |
|---|---|---|
| genai | `e3f65dd` | **aprovado** |
| rpa | `c8dbe72` | **aprovado com exceção** |
| dashboard | `1514bb2` | **aprovado com exceção** |

## genai (Generative AI & Advanced Nets)

| # | Critério | Papel | Situação | Detalhe |
|---|---|---|---|---|
| 1 | Rastreabilidade: código no commit registrado, sem alteração local | Engenharia | ok | commit e3f65dd, árvore limpa |
| 2 | Reprodutibilidade: suíte de testes do módulo passa | Engenharia | ok | 63 testes OK |
| 3 | Conjuntos de referência sem alteração (hash SHA-256) | Data Steward | ok | 3 arquivos iguais |
| 4 | Desempenho: Metric Contract sem alerta crítico | Metric Owner | ok | MC-01: 100,0%; 1 alerta(s) não crítico(s): abstencao_correta |
| 5 | Equidade: diferença entre subgrupos dentro de 5 p.p. | Model Validator | não se aplica | não aplicável: as perguntas não têm atributo de grupo; risco tratado por abstenção |
| 6 | Model Card com as oito seções, incluindo explicabilidade | Model Validator | ok | artefatos/model_cards/assistente_rag.md |
| 7 | Plano de monitoramento com seção do contrato do módulo | Metric Owner | ok | artefatos/plano_monitoramento.md |
| 8 | Revisão LGPD: dados do módulo no inventário e RIPD | Encarregado de dados | ok | artefatos/lgpd/inventario_dados.md; artefatos/lgpd/ripd_simplificado.md |

## rpa (AI for Robotic Process Automation)

| # | Critério | Papel | Situação | Detalhe |
|---|---|---|---|---|
| 1 | Rastreabilidade: código no commit registrado, sem alteração local | Engenharia | ok | commit c8dbe72, árvore limpa |
| 2 | Reprodutibilidade: suíte de testes do módulo passa | Engenharia | ok | 47 testes OK |
| 3 | Conjuntos de referência sem alteração (hash SHA-256) | Data Steward | ok | 3 arquivos iguais |
| 4 | Desempenho: Metric Contract sem alerta crítico | Metric Owner | ok | MC-02: 83,3% |
| 5 | Equidade: diferença entre subgrupos dentro de 5 p.p. | Model Validator | exceção EX-02 | decisão por uf: amostra insuficiente; decisão por servico_real: amostra insuficiente; erro grave em todos os grupos: 0 (exceção até 2027-03-01, responsável: Jonas Alaf (Metric Owner do MC-02)) |
| 6 | Model Card com as oito seções, incluindo explicabilidade | Model Validator | ok | artefatos/model_cards/classificador_triagem.md |
| 7 | Plano de monitoramento com seção do contrato do módulo | Metric Owner | ok | artefatos/plano_monitoramento.md |
| 8 | Revisão LGPD: dados do módulo no inventário e RIPD | Encarregado de dados | ok | artefatos/lgpd/inventario_dados.md; artefatos/lgpd/ripd_simplificado.md |

## dashboard (Front-end em Sistemas de IA)

| # | Critério | Papel | Situação | Detalhe |
|---|---|---|---|---|
| 1 | Rastreabilidade: código no commit registrado, sem alteração local | Engenharia | ok | commit 1514bb2, árvore limpa |
| 2 | Reprodutibilidade: suíte de testes do módulo passa | Engenharia | ok | 74 testes OK |
| 3 | Conjuntos de referência sem alteração (hash SHA-256) | Data Steward | ok | 6 arquivos iguais |
| 4 | Desempenho: Metric Contract sem alerta crítico | Metric Owner | ok | MC-03: 63,0%; 2 alerta(s) não crítico(s): sensibilidade_milho, sensibilidade_feijao |
| 5 | Equidade: diferença entre subgrupos dentro de 5 p.p. | Model Validator | exceção EX-01 | sensibilidade milho: 29,2 p.p.; sensibilidade feijao: 24,6 p.p. (exceção até 2027-03-01, responsável: Ricardo de Paiva Melo (Metric Owner do MC-03)) |
| 6 | Model Card com as oito seções, incluindo explicabilidade | Model Validator | ok | artefatos/model_cards/modelo_hidrico.md |
| 7 | Plano de monitoramento com seção do contrato do módulo | Metric Owner | ok | artefatos/plano_monitoramento.md |
| 8 | Revisão LGPD: dados do módulo no inventário e RIPD | Encarregado de dados | ok | artefatos/lgpd/inventario_dados.md; artefatos/lgpd/ripd_simplificado.md |

Este registro é gerado por script e não substitui a aprovação do Metric Owner de cada módulo, definida em artefatos/raci.md.
