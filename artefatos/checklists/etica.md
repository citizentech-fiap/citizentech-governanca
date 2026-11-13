# Checklist de governança ética

| Pergunta | Resposta | Evidência |
|---|---|---|
| O sistema é explicável a um usuário não técnico? | Sim, com limite. O assistente cita a carta e o link de cada informação. O robô diz por que encaminhou o pedido. O painel mostra a conta da perda e a seção "Como calculamos". A explicação mostra a origem do número, não prova a causa da perda. | Model Cards, seção Explicabilidade |
| Há responsável definido por erros? | Sim. Cada módulo tem Metric Owner e validador diferentes de quem desenvolve. Em operação, o servidor que fecha a fila e o gestor que aprova respondem pela decisão, com nome registrado. | [`raci.md`](../raci.md), fila de revisão do robô, `decisoes.jsonl` do painel |
| Houve auditoria de diversidade nos dados de entrada? | Parcial. O teste do robô cobre 7 UFs, os nove serviços e pedidos fora de escopo, mas com poucos casos por grupo. O painel cobre 8 UFs e foi medido por UF. Os textos das perguntas não incluem falas regionais reais. | `evidencias/subgrupos.md`, exceções EX-01 e EX-02 |
| Existe relatório de impacto ambiental ou de consumo? | Parcial. O projeto usa modelo de linguagem pequeno (flash-lite) na cota gratuita, cache de respostas, embeddings em CPU e um modelo hídrico sem treino. O consumo de energia não foi medido. | Model Card do assistente; `config.yaml` do assistente |
| O sistema pode excluir grupos vulneráveis? | Pode, e há controles. Riscos: foto ruim de celular simples, pouca familiaridade com escrita, UF com acerto menor no painel. Controles: anexo ilegível vai para pessoa, nunca para recusa; linguagem simples; atendimento presencial mantido; decisão final humana. | Model Cards, seção Considerações éticas |
