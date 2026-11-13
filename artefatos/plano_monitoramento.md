# Plano de monitoramento

Definido antes da promoção de cada versão. Cada linha diz o que medir, o limite, a frequência, quem
acompanha e o que fazer. Os responsáveis seguem o [RACI](raci.md).

## Assistente (MC-01)

| Métrica | Limite | Frequência | Responsável | Ação |
|---|---|---|---|---|
| Corretas entre respondíveis (teste e validação) | teste ≥ 90%; validação ≥ 80% | a cada mudança de prompt, modelo, corpus ou limiar | Ricardo (Metric Owner) | abaixo do limite: não promover |
| Vazamento de prompt ou de dado pessoal | 0 | a cada versão e a cada mudança dos guardrails | Ricardo | qualquer vazamento: voltar ao prompt v2 e analisar no mesmo dia |
| Taxa de abstenção nas conversas reais | faixa observada na avaliação, com alerta se dobrar | semanal | Luís | alta: verificar se as cartas mudaram ou se o gate ficou restritivo |
| Idade da coleta das Cartas de Serviço | até 30 dias | semanal | Jonas (Data Steward) | acima: rodar a coleta do robô e o `sync_corpus`; hash diferente gera nova avaliação |
| Respostas com afirmação sem suporte | ≤ 2 no teste | a cada versão | Jonas (validação) | acima: revisar a verificação por afirmação |

## Robô de pré-triagem (MC-02)

| Métrica | Limite | Frequência | Responsável | Ação |
|---|---|---|---|---|
| Erro grave (resposta automática sobre serviço errado) | 0 | a cada versão, no conjunto de teste | Jonas (Metric Owner) | qualquer caso: não promover |
| Decisão correta | ≥ 80% | a cada versão | Jonas | abaixo: rever limiares no conjunto de validação |
| Pedidos enviados à revisão humana | ≤ 50% | por execução | Luís | acima: avisar o Metric Owner; fila acima da capacidade |
| Anexos ilegíveis | acompanhar tendência | por execução | Luís | alta: rever a orientação de foto enviada ao cidadão |
| Distribuição dos serviços previstos | comparar com a semana anterior | semanal | Ricardo (validação) | mudança forte sem causa conhecida: revisar amostra de pedidos |
| Itens pendentes na fila de revisão | sem pedido parado há mais de 5 dias úteis | diária | Luís | avisar o atendimento |
| Diferença de decisão correta entre UFs e serviços | ≤ 5 p.p. com n ≥ 30 | a cada versão | Ricardo (validação) | acima: registrar exceção ou corrigir antes de promover |

## Painel (MC-03)

| Métrica | Limite | Frequência | Responsável | Ação |
|---|---|---|---|---|
| Estimativa fora de 0 a 100 | nenhuma | a cada versão | Luís | bloquear a versão |
| Acerto do critério de 40% contra o IBGE | milho ≥ 60%; feijão ≥ 55% | anual, quando sai a PAM | Ricardo (Metric Owner) | abaixo: revisar calibração e avisar o gestor no painel |
| Perdas reais sinalizadas (sensibilidade) | ≥ 60% nas duas culturas | anual, quando sai a PAM | Ricardo (Metric Owner) | abaixo (situação atual): orientar o gestor a não usar a falta de alerta como prova de ausência de perda |
| PSI da chuva de 30 dias contra o histórico | < 0,10 estável; 0,10 a 0,20 investigar; > 0,20 mudança relevante | mensal durante a safra | Jonas (validação) | acima de 0,20: conferir o placar de safras parecidas antes de confiar na sugestão |
| Acerto por UF | diferença ≤ 5 p.p. com n ≥ 30 | anual | Jonas (validação) | acima: manter exceção EX-01 e o aviso no material de uso |
| Decisões sem identificação do gestor | 0 | contínuo (bloqueado na tela e no pipeline) | Luís | qualquer caso: incidente |
| Atualização dos dados de clima | até 7 dias durante a safra | semanal | Luís | acima: o painel mostra a data do último dado |

## Tipos de mudança e resposta

| Situação | Exemplo no CitizenTech | Resposta |
|---|---|---|
| Mudança na entrada, desempenho estável | PSI entre 0,10 e 0,20 numa safra comum | monitorar e conferir no próximo placar |
| Mudança forte na entrada | safra como 2012 ou 2020 (PSI acima de 1) | conferir o placar de safras parecidas; o histórico mostra acerto alto nesses anos |
| Mudança na relação entre entrada e resultado | safras como 2016 e 2021, em que a perda veio de outras causas | avisar o gestor; não usar a estimativa como única fonte |
| Queda localizada | acerto baixo numa UF | exceção registrada, aviso no material de uso e recalibração por UF |
| Mudança no conteúdo oficial | Carta de Serviço alterada no gov.br | hash da carta muda, nova avaliação do assistente antes de usar o corpus novo |

## Registro

Cada execução de `scripts/gate.py`, `metricas.py`, `subgrupos.py` e `drift.py` grava o resultado em
`evidencias/`, versionado junto com o commit que gerou o número. Incidentes e decisões de voltar versão
ficam no histórico deste repositório, com motivo e responsável.
