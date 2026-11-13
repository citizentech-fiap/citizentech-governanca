# Classificação de risco dos módulos

Usamos os quatro níveis de risco do EU AI Act (inaceitável, alto, limitado, mínimo), que também orientam
o PL 2.338/2023. O CitizenTech não é um sistema europeu. A escala serve como régua para decidir quanto
controle cada módulo precisa.

## Critério

Pesamos três perguntas para cada módulo:

1. A saída influencia o acesso de uma pessoa a um benefício ou serviço público essencial?
2. Existe uma pessoa que decide antes de qualquer efeito sobre o cidadão?
3. O público atingido é vulnerável (renda baixa, pouca conectividade, pouca familiaridade com sistemas)?

O Anexo III do EU AI Act lista como alto risco os sistemas usados por autoridades públicas para avaliar a
elegibilidade a benefícios e serviços de assistência pública essenciais (item 5, alínea a). O PL 2.338/2023
segue a mesma linha ao tratar de serviços públicos essenciais. Esses dois textos são a fonte externa da
classificação abaixo. O material da disciplina cita crédito, saúde, emprego, segurança pública e educação
como exemplos de alto risco; o acesso a benefício público fica na mesma família de decisão.

## Resultado

| Módulo | O que faz com o cidadão | Nível | Justificativa |
|---|---|---|---|
| RPA: pré-triagem de pedidos | classifica o pedido, confere documentos e decide entre responder, mandar para revisão humana ou marcar como inválido | **Alto** | Influencia quando e como o agricultor chega ao Garantia-Safra, ao CAF e a outros benefícios. Público vulnerável. |
| Dashboard: priorização de municípios | estima perda de safra e sugere onde o gestor pede vistoria ou chama agricultores | **Alto** | Influencia a ordem em que comunidades recebem atenção do poder público. A decisão é do gestor, mas a sugestão pesa. |
| GenAI: assistente de orientação | responde dúvidas sobre serviços com base nas Cartas de Serviço, citando a fonte | **Limitado** | Informa, não decide. A obrigação principal é de transparência: o cidadão precisa saber que fala com um sistema automático e de onde vem a informação. Uma resposta errada ainda pode custar viagem ou prazo, por isso o assistente se abstém sem evidência. |

## O que muda por nível

| Obrigação | Alto (RPA, Dashboard) | Limitado (GenAI) |
|---|---|---|
| Supervisão humana | obrigatória antes de qualquer efeito sobre o cidadão | caminho de saída para atendimento humano |
| Registro de decisões | trilha com responsável, data e motivo | trace técnico por resposta |
| Gate de promoção | oito critérios, incluindo equidade | oito critérios; equidade não se aplica |
| Documentação | Model Card, Metric Contract, plano de monitoramento | os mesmos |
| Transparência ao cidadão | motivo do encaminhamento e canal humano | fonte citada em toda resposta e abstenção explícita |

## Limites desta classificação

- Os dados de pedidos são sintéticos. Em uso real, a classificação precisa ser refeita com o órgão
  responsável e o encarregado de dados.
- A classificação vale para o uso descrito. Se o robô passar a negar pedidos sem revisão humana, o risco
  sobe e o desenho atual deixa de ser suficiente.
