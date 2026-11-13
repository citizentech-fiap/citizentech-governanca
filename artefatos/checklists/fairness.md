# Checklist de auditoria de equidade

| Item | Situação | Detalhe |
|---|---|---|
| Atributos sensíveis e proxies identificados | feito | Os módulos não usam gênero, raça, idade ou renda individual. O atributo de grupo disponível é território (município e UF), que pode funcionar como proxy de renda e de acesso a serviços. No robô, o serviço pedido também separa públicos (aposentadoria, salário-maternidade, BPC). |
| Pelo menos duas métricas de equidade testadas | parcial | Medimos a diferença de acerto entre grupos (painel por UF; robô por UF e por serviço) e a diferença na taxa de envio para revisão humana (robô). Paridade demográfica não se aplica ao painel: a sugestão é por município, não por pessoa. |
| Trade-off entre acerto e equidade documentado | feito | Nivelar o acerto entre UFs exigiria calibrar Ky por UF com poucos pares por estado, o que aumenta o risco de sobreajuste. Escolhemos manter um único modelo, mostrar o acerto por UF e registrar exceção com prazo. |
| Monitoramento da equidade em produção | planejado | `subgrupos.py` roda a cada versão e o acerto por UF é refeito a cada PAM publicada (plano de monitoramento). |
| Revisão das causas do viés | feito | O modelo usa só chuva. As UFs com acerto menor têm mais perda vinda de outras causas (praga, preço, área não plantada). O loop de feedback da priorização está descrito no Model Card do painel. |

## Métrica priorizada e por quê

No robô, a métrica de equidade priorizada é o **erro grave por grupo**, que hoje é zero em todos os grupos:
nenhum agricultor recebe resposta automática errada, em nenhuma UF. A diferença de decisão correta entre
grupos vem quase toda de pedidos que foram para revisão humana sem precisar, que é o erro seguro.

No painel, a métrica priorizada é o **acerto do critério de 40% por UF**, porque é ela que decide se o gestor
de uma UF recebe uma sugestão tão confiável quanto a de outra. Ela está acima do limite e coberta pela
exceção EX-01.
