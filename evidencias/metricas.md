# Metric Contracts recalculados

Gerado em 13/11/2026 sobre as versões de `versoes.yaml`:

- genai: `e3f65dd`
- rpa: `c8dbe72`
- dashboard: `1514bb2`

## MC-01 Respostas corretas do assistente de serviços públicos (v1.0.0)

| Indicador | Valor | Baseline | Meta | Situação |
|---|---|---|---|---|
| Respostas corretas entre as perguntas respondíveis (conjunto de teste) | 100,0% | 68,2% | 90,0% | atinge |

| Métrica de qualidade | Valor | Limite | Situação |
|---|---|---|---|
| Corretas entre respondíveis no conjunto de validação (perguntas não usadas no desenho) | 100,0% | ≥ 80,0% | ok |
| Abstenção correta em perguntas sem resposta ou fora de escopo | 90,0% | ≥ 95,0% | fora do limite |
| Respostas com afirmação sem suporte nos trechos (teste) | 1 | ≤ 2 | ok |
| Vazamentos de prompt ou de dado pessoal com as proteções ligadas | 0 | == 0 | ok |

Detalhe: teste: 22 de 22; validacao: 6 de 6; abstencao: 9 de 10; cenarios_protecao_ligada: 12.

Alertas disparados:

- **alerta** (abstencao_correta < 95,0%): Registrar os casos como falha conhecida e avisar no material de uso. Promover só se nenhum caso levar o agricultor a um canal ou endereço inexistente.

## MC-02 Decisão correta da pré-triagem de pedidos (v1.0.0)

| Indicador | Valor | Baseline | Meta | Situação |
|---|---|---|---|---|
| Decisão final correta (resolvido, revisão humana ou inválido) | 83,3% | 76,7% | 80,0% | atinge |

| Métrica de qualidade | Valor | Limite | Situação |
|---|---|---|---|
| Respostas automáticas sobre o serviço errado ou fora de escopo | 0 | == 0 | ok |
| Classificação correta do serviço (exceto inválidos e fora de escopo) | 93,8% | ≥ 90,0% | ok |
| Pedidos enviados para revisão humana | 41,7% | ≤ 50,0% | ok |
| Pedidos resolvíveis que foram para revisão humana | 9 | informativo | informativo |

Detalhe: pedidos: 60; respostas_automaticas: 29; classificados: 48.

Nenhum alerta disparado.

## MC-03 Perda estimada de safra por município (v1.0.0)

| Indicador | Valor | Baseline | Meta | Situação |
|---|---|---|---|---|
| Perda estimada de produção por município e safra (%) | 63,0% | não medido | 60,0% | atinge |

Valor e meta referem-se a: acerto do critério de 40% contra o IBGE no milho (cultura principal do painel).

| Métrica de qualidade | Valor | Limite | Situação |
|---|---|---|---|
| Acerto do critério de 40% contra a perda real do IBGE, milho | 63,0% | ≥ 60,0% | ok |
| Acerto do critério de 40% contra a perda real do IBGE, feijão | 57,8% | ≥ 55,0% | ok |
| Correlação de postos entre perda estimada e real, milho | 0,47 | ≥ 0,40 | ok |
| Perdas reais de 40% ou mais que o painel sinaliza, milho | 51,2% | ≥ 60,0% | fora do limite |
| Perdas reais de 40% ou mais que o painel sinaliza, feijão | 43,7% | ≥ 60,0% | fora do limite |
| Safras sem perda de 40% que o painel reconhece como tal, milho | 76,3% | ≥ 60,0% | ok |
| Toda estimativa entre 0 e 100 | 1 | == 1 | ok |

Detalhe: milho: 322 pares municipio-safra; perda entre 0,0 e 100,0; feijao: 322 pares municipio-safra; perda entre 0,0 e 97,7.

Alertas disparados:

- **alerta** (sensibilidade_milho < 60,0%): O painel deixa de sinalizar parte das perdas reais. Orientar o gestor a não tratar a ausência de alerta como prova de que não houve perda e manter a inscrição aberta a todos os municípios.
- **alerta** (sensibilidade_feijao < 60,0%): O painel deixa de sinalizar parte das perdas reais. Orientar o gestor a não tratar a ausência de alerta como prova de que não houve perda e manter a inscrição aberta a todos os municípios.
