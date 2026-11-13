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
| Pares município-safra | 322 | 322 |

Por UF, o acerto no milho vai de 46,4% (RN) a 75,0% (PI); entre as UFs com pelo menos 30 pares, de 55,4%
(BA) a 69,6% (CE). A diferença passa do limite de 5 p.p. e está registrada como exceção EX-01.

Por safra, o acerto é alto nos anos extremos (2012: 95,7%; 2020: 91,3%) e baixo em anos de chuva
intermediária (2016: 13,0%; 2021: 17,4%). Ver [`evidencias/drift.md`](../../evidencias/drift.md).

## Considerações éticas

- Feedback loop: municípios priorizados recebem mais vistorias, geram mais registros e tendem a continuar
  priorizados. Por isso o painel mostra o placar contra o IBGE, que é independente das decisões do gestor.
- UF e município podem funcionar como proxy de renda e de acesso a serviços. O acerto desigual entre UFs
  significa que agricultores de algumas UFs recebem uma sugestão menos confiável.
- A decisão é sempre humana, registrada com identificação do gestor e motivo de recusa.

## Limitações

- Só chuva e demanda hídrica: praga, preço, área não plantada e distribuição da chuva dentro da safra ficam
  de fora. É provável que isso explique os anos 2016 a 2019 e 2021, em que o modelo não vê a perda.
- A calibração e a avaliação usam as mesmas safras (2012 a 2025). Não há conjunto de validação separado.
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
