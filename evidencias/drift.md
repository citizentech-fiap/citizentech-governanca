# Mudança de distribuição da chuva por safra (PSI)

Gerado em 17/11/2026 sobre as versões de `versoes.yaml`, depois de conferir os commits e o hash dos conjuntos de referência:

- genai: `108dbfa`
- rpa: `bad8682`
- dashboard: `2b7340a`

Variável: chuva de 30 dias dividida pela normal 1991-2020, por município e dia, de janeiro a junho. Referência de cada safra: as demais safras do histórico.

| Safra | PSI | Faixa | Chuva / normal (mediana) | Pares com perda real ≥ 40% | Pares sinalizados pelo painel | Acerto, milho |
|---|---|---|---|---|---|---|
| 2012 | 2,25 | mudança relevante | 0,25 | 95,7% | 100,0% | 95,7% |
| 2013 | 0,36 | mudança relevante | 0,43 | 91,3% | 100,0% | 91,3% |
| 2014 | 0,16 | investigar | 0,62 | 65,2% | 56,5% | 65,2% |
| 2015 | 0,20 | mudança relevante | 0,53 | 65,2% | 65,2% | 82,6% |
| 2016 | 0,18 | investigar | 0,52 | 91,3% | 4,3% | 13,0% |
| 2017 | 0,05 | estável | 0,57 | 65,2% | 47,8% | 47,8% |
| 2018 | 0,12 | investigar | 0,69 | 47,8% | 13,0% | 65,2% |
| 2019 | 0,23 | mudança relevante | 0,83 | 47,8% | 0,0% | 52,2% |
| 2020 | 1,93 | mudança relevante | 1,35 | 8,7% | 0,0% | 91,3% |
| 2021 | 0,23 | mudança relevante | 0,43 | 17,4% | 91,3% | 17,4% |
| 2022 | 0,63 | mudança relevante | 0,93 | 17,4% | 8,7% | 82,6% |
| 2023 | 0,20 | investigar | 0,72 | 47,8% | 13,0% | 47,8% |
| 2024 | 0,36 | mudança relevante | 1,04 | 17,4% | 0,0% | 82,6% |
| 2025 | 0,11 | investigar | 0,60 | 60,9% | 34,8% | 47,8% |
| 2026 | 0,03 | estável | 0,64 | sem dado do IBGE | - | - |

Correlação de postos entre PSI e acerto do painel (safras com placar): 0,69.
Safras com PSI acima de 0,20: 8 de 15. A chuva do semiárido muda muito de um ano para outro, então o PSI da chuva serve de contexto; o alarme do painel é o placar anual contra o IBGE.

Safras com acerto abaixo de 50%:
- 2016: perda real não sinalizada (perda real em 91,3% dos pares; painel sinalizou 4,3%).
- 2017: perda real não sinalizada (perda real em 65,2% dos pares; painel sinalizou 47,8%).
- 2021: falso alarme (perda real em 17,4% dos pares; painel sinalizou 91,3%).
- 2023: perda real não sinalizada (perda real em 47,8% dos pares; painel sinalizou 13,0%).
- 2025: perda real não sinalizada (perda real em 60,9% dos pares; painel sinalizou 34,8%).

Nas safras em que quase todos ou quase nenhum dos pares teve perda real, o acerto alto vem da própria prevalência, não de discriminação entre municípios.
