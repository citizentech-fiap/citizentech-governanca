# Papéis e responsabilidades (RACI)

R = executa, A = aprova e responde pelo resultado, C = é consultado, I = é informado.

Regra central: quem desenvolve não promove sozinho. A promoção de uma versão depende do gate automático
(`scripts/gate.py`) e da aprovação do Metric Owner do módulo, e a validação do modelo fica com um
integrante diferente de quem o construiu.

## Papéis

| Papel | Integrante | Responsabilidade | Fora do escopo |
|---|---|---|---|
| Engenharia de ML e dados (Data Custodian) | Luís Fernando de Oliveira Salgado | código, pipelines, testes, versionamento, infraestrutura e scripts de verificação | aprovar a própria versão; definir sozinho o critério de equidade |
| Metric Owner do MC-01 (assistente) e do MC-03 (painel) | Ricardo de Paiva Melo | definição das métricas, metas e limiares; aprovação da promoção desses módulos | escrever o pipeline |
| Model Validator do robô | Ricardo de Paiva Melo | validação independente do classificador, dos limiares e da equidade | operação diária |
| Metric Owner do MC-02 (robô) | Jonas Alaf | definição das métricas, metas e limiares do robô; aprovação da promoção | escrever o pipeline |
| Model Validator do assistente e do painel | Jonas Alaf | validação independente das avaliações e do placar | operação diária |
| Encarregado de dados (DPO) e Data Steward | Jonas Alaf | inventário de dados, RIPD, termo de consentimento, catálogo e conjuntos de referência | decidir o uso do dado sem base legal |

Na operação real, o Data Owner é o órgão público responsável por cada serviço (MDA para Garantia-Safra,
CAF e Pronaf; INSS para os benefícios previdenciários; MDS para Cadastro Único e Bolsa Família) e quem
decide sobre o cidadão é sempre um servidor: o atendente da fila de revisão do robô e o gestor no painel.

## Matriz por atividade

| Atividade | Luís | Ricardo | Jonas |
|---|---|---|---|
| Alterar código, prompt, modelo ou limiar | R | C | C |
| Escrever RFC de mudança | R | A (MC-01, MC-03) | A (MC-02) |
| Rodar o gate de promoção | R | I | I |
| Aprovar promoção do assistente | C | A | R (validação) |
| Aprovar promoção do robô | C | R (validação) | A |
| Aprovar promoção do painel | C | A | R (validação) |
| Registrar exceção ao gate | R | A (EX-01) | A (EX-02) |
| Manter inventário de dados e RIPD | C | I | A/R |
| Atualizar conjuntos de referência (golden) | R | I | A |
| Responder a incidente de dado pessoal | R | I | A |
| Monitorar métricas e alertas | R | A (MC-01, MC-03) | A (MC-02) |

## Monitoramento

A responsabilidade pelo monitoramento é definida antes do deploy, não depois do primeiro incidente. A
tabela acima cobre quem acompanha cada alerta. O detalhe de métrica, limiar, frequência e ação está em
[`plano_monitoramento.md`](plano_monitoramento.md).
