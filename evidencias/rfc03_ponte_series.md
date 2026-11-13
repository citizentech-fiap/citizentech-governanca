# RFC-03: ponte entre séries da perda estimada

Gerado em 13/11/2026 sobre as versões de `versoes.yaml`, depois de conferir os commits e o hash dos conjuntos de referência:

- genai: `e3f65dd`
- rpa: `c8dbe72`
- dashboard: `1514bb2`

v1: perda = 100 x Ky x (1 - ISNA_ano). v2: perda = 100 x Ky x (1 - ISNA_ano / ISNA_normal).
Mesmos dados de chuva e ET0; referência: perda real do IBGE no critério de 40%.

## Milho (322 pares município-safra)

| Medida | v1 | v2 |
|---|---|---|
| Acerto do critério de 40% | 58,1% | 63,0% |
| Correlação de postos com a perda real | 0,46 | 0,47 |
| Perdas reais sinalizadas (sensibilidade) | 96,5% | 51,2% |
| Safras sem perda reconhecidas (especificidade) | 15,1% | 76,3% |
| Acerto balanceado | 55,8% | 63,7% |
| Pares sinalizados com perda ≥ 40% | 91,0% | 38,2% |
| Pares com perda real ≥ 40% (IBGE) | 52,8% | 52,8% |

| Safra | Perda mediana v1 | Perda mediana v2 |
|---|---|---|
| 2012 | 100,0% | 97,1% |
| 2013 | 100,0% | 63,5% |
| 2014 | 93,0% | 45,8% |
| 2015 | 95,1% | 47,9% |
| 2016 | 77,5% | 23,3% |
| 2017 | 91,1% | 34,4% |
| 2018 | 78,6% | 17,5% |
| 2019 | 71,2% | 0,0% |
| 2020 | 31,0% | 0,0% |
| 2021 | 97,0% | 53,2% |
| 2022 | 62,4% | 0,0% |
| 2023 | 82,3% | 17,1% |
| 2024 | 70,2% | 0,0% |
| 2025 | 87,6% | 26,5% |

## Feijao (322 pares município-safra)

| Medida | v1 | v2 |
|---|---|---|
| Acerto do critério de 40% | 66,8% | 57,8% |
| Correlação de postos com a perda real | 0,49 | 0,44 |
| Perdas reais sinalizadas (sensibilidade) | 94,9% | 43,7% |
| Safras sem perda reconhecidas (especificidade) | 22,4% | 80,0% |
| Acerto balanceado | 58,7% | 61,8% |
| Pares sinalizados com perda ≥ 40% | 88,2% | 34,5% |
| Pares com perda real ≥ 40% (IBGE) | 61,2% | 61,2% |

| Safra | Perda mediana v1 | Perda mediana v2 |
|---|---|---|
| 2012 | 100,0% | 89,3% |
| 2013 | 94,1% | 58,4% |
| 2014 | 83,8% | 42,1% |
| 2015 | 85,8% | 44,0% |
| 2016 | 68,5% | 21,5% |
| 2017 | 81,8% | 31,6% |
| 2018 | 69,7% | 16,1% |
| 2019 | 62,4% | 0,0% |
| 2020 | 23,1% | 0,0% |
| 2021 | 87,7% | 48,9% |
| 2022 | 53,8% | 0,0% |
| 2023 | 73,3% | 15,7% |
| 2024 | 61,4% | 0,0% |
| 2025 | 78,4% | 24,4% |
