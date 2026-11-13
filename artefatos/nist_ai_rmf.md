# NIST AI RMF aplicado ao CitizenTech

O NIST AI Risk Management Framework organiza a gestão de risco em quatro funções: Govern (cultura,
papéis e políticas), Map (contexto e riscos), Measure (métricas) e Manage (resposta). Usamos o framework
como mapa da integração: cada função junta controles que estão espalhados pelos três módulos.

## Govern

| Ação | Onde está |
|---|---|
| Papéis definidos, com a regra de que quem desenvolve não promove sozinho | [`raci.md`](raci.md) |
| Classificação de risco por módulo e obrigações por nível | [`classificacao_risco.md`](classificacao_risco.md) |
| Definição única das métricas, com dono, meta e limiares | [`metric_contracts/`](metric_contracts/) |
| Mudança que altera métrica ou série passa por RFC | [`rfc/`](rfc/) |
| Versão governada de cada módulo registrada | [`../versoes.yaml`](../versoes.yaml) |
| Dados pessoais só sintéticos no projeto; chaves fora do código e do git | `.gitignore` e geradores de dados dos módulos |

## Map

| Risco | Módulo | Quem é afetado | Onde está mapeado |
|---|---|---|---|
| Resposta errada levar o agricultor a um canal inexistente ou à perda de prazo | GenAI | agricultor | Model Card do assistente, MC-01 |
| Resposta automática sobre o serviço errado | RPA | agricultor | Model Card do classificador, MC-02 |
| Exclusão de quem tem celular simples e foto ruim | RPA | agricultor com pouca conectividade | Model Card do classificador |
| Sugestão de prioridade menos confiável em algumas UFs | Dashboard | comunidades dessas UFs | Model Card do modelo hídrico, EX-01 |
| Feedback loop na priorização | Dashboard | municípios fora do foco | Model Card do modelo hídrico |
| Injeção de instrução no pedido ou no documento | GenAI | todos | guardrails do assistente |
| Exposição de CPF, NIS ou nome | todos | agricultor | [`lgpd/inventario_dados.md`](lgpd/inventario_dados.md) |

## Measure

| Medida | Resultado atual | Evidência |
|---|---|---|
| Corretas entre respondíveis, teste e validação | 22 de 22 e 6 de 6 | `evidencias/metricas.md` |
| Vazamentos com proteções ligadas | 0 em 12 cenários | `evidencias/metricas.md` |
| Decisão correta e erro grave do robô | 83,3% e 0 | `evidencias/metricas.md` |
| Acerto do painel contra o IBGE | milho 63,0%, feijão 57,8% | `evidencias/metricas.md` |
| Perdas reais sinalizadas pelo painel | milho 51,2%, feijão 43,7% (meta 60%, alerta) | `evidencias/metricas.md` |
| Efeito da calibração pela normal (antes e depois) | acerto balanceado sobe, sensibilidade cai pela metade | `evidencias/rfc03_ponte_series.md` |
| Diferença entre subgrupos | painel: 14,3 p.p. (milho) e 22,0 p.p. (feijão) entre UFs; robô: amostras pequenas | `evidencias/subgrupos.md` |
| Mudança de distribuição da chuva | PSI por safra; correlação com o acerto 0,69 | `evidencias/drift.md` |
| Conjuntos de referência intactos | hash SHA-256 de 12 arquivos | `golden/hashes.json` |

## Manage

| Resposta | Onde está |
|---|---|
| Gate de promoção com oito critérios por módulo | `scripts/gate.py`, `evidencias/gate.md` |
| Exceções com motivo, mitigação, responsável e prazo | [`excecoes.yaml`](excecoes.yaml) |
| Supervisão humana antes de qualquer efeito sobre o cidadão | fila de revisão do robô; aprovação do gestor no painel |
| Volta automática para caminho sem IA | template no robô e no painel quando o modelo falha, atrasa ou se abstém |
| Plano de monitoramento com ação por tipo de mudança | [`plano_monitoramento.md`](plano_monitoramento.md) |
| Volta de versão | versões de reserva nos Model Cards e plano de rollback nos RFCs |
