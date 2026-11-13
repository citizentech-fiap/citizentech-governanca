# Checklist do gate de promoção

O gate é executado por `scripts/gate.py` sobre a versão registrada em `versoes.yaml`. O resultado da última
execução está em [`evidencias/gate.md`](../../evidencias/gate.md). Um critério bloqueante que falha reprova o
módulo, salvo exceção válida em [`excecoes.yaml`](../excecoes.yaml). O gate não substitui a aprovação do
Metric Owner: ele dá ao Metric Owner a evidência para aprovar.

| # | Critério | Padrão mínimo | Papel | Como é verificado |
|---|---|---|---|---|
| 1 | Rastreabilidade | código no commit registrado, sem alteração local | Engenharia | `git rev-parse HEAD` e `git status` em cada módulo |
| 2 | Reprodutibilidade | suíte de testes do módulo passa do zero | Engenharia | roda a suíte de cada módulo (o assistente com embeddings determinísticos, sem rede) |
| 3 | Conjuntos de referência | mesmo hash SHA-256 registrado | Data Steward | `scripts/golden.py` |
| 4 | Desempenho | Metric Contract sem alerta crítico | Metric Owner | `scripts/metricas.py` |
| 5 | Equidade | diferença entre subgrupos ≤ 5 p.p. | Model Validator | `scripts/subgrupos.py` |
| 6 | Documentação | Model Card com todas as seções, incluindo monitoramento e explicabilidade | Model Validator | leitura das seções do card |
| 7 | Monitoramento | plano com limiares, frequência e responsável | Metric Owner | presença do plano |
| 8 | LGPD | inventário de dados e RIPD | Encarregado de dados | presença dos documentos |

## Antes de aprovar, além do script

- [ ] O RFC da mudança está preenchido, com impacto na série, invariantes e plano de volta.
- [ ] O Model Validator é uma pessoa diferente de quem implementou a mudança.
- [ ] Alertas não críticos do Metric Contract foram lidos e têm resposta registrada.
- [ ] Exceções vencidas foram renovadas com nova justificativa ou o problema foi corrigido.
- [ ] O material de uso (README do módulo) reflete as limitações conhecidas.
