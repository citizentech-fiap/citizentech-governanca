# Checklist de auditoria de equidade

| Item | Situação | Detalhe |
|---|---|---|
| Atributos sensíveis e proxies identificados | feito | Os módulos não usam gênero, raça, idade ou renda individual. O atributo de grupo disponível é território (município e UF), que pode funcionar como proxy de renda e de acesso a serviços. No robô, o serviço pedido também separa públicos (aposentadoria, salário-maternidade, BPC). |
| Pelo menos duas métricas de equidade testadas | feito | Painel: igualdade de oportunidade (sensibilidade por UF) e acerto por UF. Robô: erro grave, decisão correta e envio para revisão humana por UF e por serviço. Paridade demográfica não se aplica ao painel, porque a sugestão é por município, não por pessoa. |
| Trade-off entre acerto e equidade documentado | feito | Nivelar a sensibilidade entre UFs exigiria calibrar Ky por UF com 28 a 70 pares por estado, com risco de sobreajuste. Escolhemos manter um único modelo, mostrar o resultado por UF e registrar exceção com prazo (EX-01). |
| Monitoramento da equidade em produção | planejado | `subgrupos.py` roda a cada versão e a sensibilidade por UF é refeita a cada PAM publicada (plano de monitoramento). |
| Revisão das causas do viés | feito | O modelo usa só chuva. Nas UFs com sensibilidade menor (RN e BA) pesa mais a perda vinda de outras causas, como praga, preço e área não plantada. O loop de feedback da priorização está descrito no Model Card do painel. |

## Métrica priorizada e por quê

No painel, a métrica priorizada é a **sensibilidade por UF** (igualdade de oportunidade). O dano que mais pesa
é deixar de sinalizar uma perda real, porque o município deixa de ser priorizado e o agricultor espera mais
pela vistoria e pela convocação. A sensibilidade vai de 33,3% no RN a 62,5% no PI (milho), acima do limite, e
está coberta pela exceção EX-01.

No robô, a métrica priorizada é o **erro grave por grupo**, que é zero em todas as UFs e em todos os serviços:
nenhum agricultor recebe resposta automática sobre o serviço errado. As outras diferenças não podem ser
medidas, porque só Pernambuco tem mais de 20 pedidos (EX-02).
