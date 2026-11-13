# Relatório de impacto à proteção de dados (versão simplificada)

## Descrição do tratamento

O CitizenTech recebe pedidos de agricultores familiares sobre serviços públicos, confere documentos,
orienta com base nas Cartas de Serviço e ajuda o gestor municipal a priorizar comunidades afetadas pela
seca. Dados tratados e finalidades: ver o [inventário](inventario_dados.md).

## Necessidade e proporcionalidade

- A triagem precisa saber qual serviço foi pedido e quais documentos foram enviados. Não precisa de raça,
  religião, saúde ou renda declarada, e esses dados não são pedidos.
- A planilha de controle e o painel funcionam sem nome e sem CPF. O dado pessoal fica só no pedido
  original, que é o que o atendente precisa para responder.
- O painel prioriza municípios, não pessoas.

## Riscos e medidas

| Risco ao titular | Probabilidade | Impacto | Medida existente | Medida pendente |
|---|---|---|---|---|
| CPF ou telefone enviado a serviço externo de IA | baixa | alto | máscara antes do assistente; teste de segurança com 0 vazamentos com proteção ligada | máscara de nomes próprios |
| Pedido lido por pessoa não autorizada | média | alto | arquivos fora do git; planilha sem nome e CPF | controle de acesso e autenticação |
| Decisão automática prejudicial ao titular | baixa | alto | robô não nega benefício; dúvida vai para pessoa; erro grave 0 | auditoria periódica de amostra da fila |
| Dado mantido por mais tempo que o necessário | alta | médio | nenhuma automática | rotina de expurgo pelos prazos do inventário |
| Uso das conversas para outro fim | baixa | médio | finalidade única no termo | registro de consentimento por conversa |
| Reidentificação a partir do painel | baixa | médio | painel só mostra agregados por município | revisão quando houver município com poucas famílias |

## Plano de resposta a incidente (art. 48)

1. Quem detectar avisa a engenharia e o encarregado no mesmo dia.
2. A engenharia contém o incidente (revoga acesso, retira arquivo exposto, troca chave) e registra o que
   aconteceu no histórico do repositório.
3. O encarregado avalia se há risco ou dano relevante. Havendo, comunica a ANPD e os titulares em prazo
   razoável, com a natureza dos dados, os titulares afetados, as medidas tomadas e os riscos.
4. Postmortem sem busca de culpados, focado no processo, com ação e prazo.

## Conclusão do encarregado

O tratamento é compatível com a finalidade pública, desde que, antes de uso real, sejam implementados o
controle de acesso, a autenticação do gestor e a rotina de expurgo. Revisar este relatório quando entrar
uma nova fonte de dados ou um novo uso das conversas.
