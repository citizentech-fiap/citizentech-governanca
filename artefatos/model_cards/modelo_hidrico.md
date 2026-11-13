# Model Card: modelo hídrico de perda de safra (painel do gestor)

## Detalhes do modelo

| Campo | Valor |
|---|---|
| Nome | modelo hídrico, `pipelines/risco.py` do painel |
| Versão | commit `1514bb2` (09/11/2026); calibração pela normal 1991-2020 desde o commit `9371172` |
| Tipo | regra física adaptada da resposta FAO-33, sem aprendizado de máquina |
| Fórmula | perda (%) = 100 x Ky x (1 - ISNA_ano / ISNA_normal), limitada a 0 e 100 |
| Entradas | chuva e ET0 diárias (Open-Meteo, reanálise ERA5), Kc e Ky por cultura, normal 1991-2020 do município |
| Responsáveis | engenharia: Luís Fernando de Oliveira Salgado; Metric Owner: Ricardo de Paiva Melo; validação: Jonas Alaf |
| Contrato de métrica | [MC-03](../metric_contracts/MC-03.yaml) |

## Uso pretendido

- **Adequado:** apontar ao gestor municipal onde a falta de chuva provavelmente derrubou a safra, para
  priorizar vistoria, mutirão de cadastro e convocação de agricultores para o Garantia-Safra.
- **Inadequado:** comprovar perda, conceder ou negar o Garantia-Safra, substituir a vistoria oficial ou o
  indicador do INMET. O painel diz isso na tela.

## Dados

- 23 municípios do semiárido em 8 UFs, safras de 2012 a 2026, milho e feijão.
- Clima: reanálise ERA5, escolhida porque cobre toda a série sem lacunas.
- Verdade de referência: produção municipal do IBGE (PAM, tabela 1612), com perda calculada contra a média
  dos 10 anos anteriores.
- Pagamentos do Garantia-Safra (Portal da Transparência) entram só como contexto, não como verdade.
- Pedidos de agricultores no painel são sintéticos e marcados com selo "simulado".

## Métricas

| Métrica | Milho | Feijão |
|---|---|---|
| Acerto do critério de 40% contra o IBGE | 63,0% | 57,8% |
| Correlação de postos (Spearman) | 0,47 | 0,44 |
| Perdas reais de 40% ou mais sinalizadas (sensibilidade) | 51,2% | 43,7% |
| Safras sem perda de 40% reconhecidas (especificidade) | 76,3% | 80,0% |
| Pares município-safra | 322 | 322 |

O acerto sozinho engana: antes da calibração pela normal, o modelo marcava perda de 40% em cerca de 90% dos
pares e acertava 66,8% no feijão só porque a maioria dos pares teve perda real. Depois da calibração, o
acerto balanceado subiu nas duas culturas (milho de 55,8% para 63,7%; feijão de 58,7% para 61,8%), mas o
painel passou a deixar de sinalizar cerca de metade das perdas reais. Ver
[`evidencias/rfc03_ponte_series.md`](../../evidencias/rfc03_ponte_series.md) e o RFC-03.

Por UF, a sensibilidade no milho vai de 33,3% (RN) a 62,5% (PI) entre as UFs com pelo menos 20 pares. A
diferença passa do limite de 5 p.p. de igualdade de oportunidade e está registrada como exceção EX-01. Ver
[`evidencias/subgrupos.md`](../../evidencias/subgrupos.md).

Por safra, há dois tipos de erro ([`evidencias/drift.md`](../../evidencias/drift.md)):

- **Perda real não sinalizada.** Em 2016, 91,3% dos pares tiveram perda real de 40% ou mais e o painel
  sinalizou 4,3%: a chuva de 30 dias ficou, em mediana, em 52% da normal, e a perda foi maior do que a
  chuva explica.
- **Falso alarme.** Em 2021, a chuva de 30 dias ficou, em mediana, em 43% da normal e o painel sinalizou
  91,3% dos pares, mas só
  17,4% tiveram perda real. A referência do IBGE é a média dos 10 anos anteriores, rebaixada pelas secas de
  2012 a 2017; contra essa média, a produção de 2021 não caiu tanto.

O acerto alto em 2012 (95,7%) e 2020 (91,3%) vem da prevalência: em 2012 quase todos tiveram perda e o
painel marcou todos; em 2020 quase nenhum teve perda e o painel não marcou nenhum.

## Considerações éticas

- Feedback loop: municípios priorizados recebem mais vistorias, geram mais registros e tendem a continuar
  priorizados. Por isso o painel mostra o placar contra o IBGE, que é independente das decisões do gestor.
- UF e município podem funcionar como proxy de renda e de acesso a serviços. O acerto desigual entre UFs
  significa que agricultores de algumas UFs recebem uma sugestão menos confiável.
- A decisão é sempre humana, registrada com identificação do gestor e motivo de recusa.

## Limitações

- Só chuva e demanda hídrica: praga, preço, área não plantada e distribuição da chuva dentro da safra ficam
  de fora. É provável que isso explique as perdas não sinalizadas de 2016 a 2019.
- A verdade de referência também tem limite: a média de 10 anos do IBGE muda depois de uma sequência de
  secas, o que gera falsos alarmes aparentes, como em 2021.
- A calibração e a avaliação usam as mesmas safras (2012 a 2025). Não há conjunto de validação separado.
- Sensibilidade abaixo da meta: a ausência de alerta não prova que não houve perda. O painel não deve ser
  usado para fechar a inscrição de nenhum município.
- A PAM sai com um ano de atraso; o placar da safra corrente só fecha no ano seguinte.
- Sem balanço de água no solo nem fenologia da cultura.

## Monitoramento

Ver [plano de monitoramento](../plano_monitoramento.md). PSI da chuva de 30 dias por safra (`drift.py`),
placar anual quando o IBGE publica a PAM, acerto por UF (`subgrupos.py`). Mudança na fórmula ou nos
coeficientes é mudança de significado da série e exige RFC MAJOR ([RFC-03](../rfc/)).

## Explicabilidade

| Campo | Valor |
|---|---|
| Método | fórmula aberta: cada número na tela pode ser refeito a partir da chuva, da ET0 e dos coeficientes |
| Tipo de explicação | global (seção "Como calculamos" no painel) e local (chuva, anomalia, déficit hídrico e perda por município) |
| Contrafactual | o déficit hídrico em mm mostra quanta água faltou para a cultura ficar na condição da normal |
| Atendimento ao cidadão | a recomendação vem com a justificativa por município, e o agricultor não é avaliado individualmente |
| Limitação conhecida | a fórmula explica o número, não prova que a perda real veio da seca |
