# Desempenho por subgrupo

Gerado em 13/11/2026 sobre as versões de `versoes.yaml`, depois de conferir os commits e o hash dos conjuntos de referência:

- genai: `e3f65dd`
- rpa: `c8dbe72`
- dashboard: `cae045f`

Limite de diferença entre subgrupos: 5 pontos percentuais, calculado só entre grupos com 20 casos ou mais.

## Painel: igualdade de oportunidade por UF (milho)

| UF | Pares município-safra | Pares com perda real ≥ 40% | Sensibilidade | Acerto |
|---|---|---|---|---|
| AL | 28 | 19 | 57,9% | 64,3% |
| BA | 56 | 23 | 43,5% | 55,4% |
| CE | 56 | 23 | 52,2% | 69,6% |
| PB | 42 | 17 | 58,8% | 69,0% |
| PE | 70 | 51 | 52,9% | 60,0% |
| PI | 28 | 16 | 62,5% | 75,0% |
| RN | 28 | 18 | 33,3% | 46,4% |
| SE | 14 | 3 | 33,3% | 71,4% |

Geral: sensibilidade 51,2%, acerto 63,0%.
Diferença máxima de sensibilidade: 29,2 p.p., acima do limite. Diferença máxima de acerto: 28,6 p.p., acima do limite.

## Painel: igualdade de oportunidade por UF (feijao)

| UF | Pares município-safra | Pares com perda real ≥ 40% | Sensibilidade | Acerto |
|---|---|---|---|---|
| AL | 28 | 19 | 47,4% | 53,6% |
| BA | 56 | 37 | 40,5% | 51,8% |
| CE | 56 | 28 | 35,7% | 60,7% |
| PB | 42 | 19 | 57,9% | 73,8% |
| PE | 70 | 51 | 49,0% | 57,1% |
| PI | 28 | 14 | 50,0% | 60,7% |
| RN | 28 | 18 | 33,3% | 50,0% |
| SE | 14 | 11 | 27,3% | 42,9% |

Geral: sensibilidade 43,7%, acerto 57,8%.
Diferença máxima de sensibilidade: 24,6 p.p., acima do limite. Diferença máxima de acerto: 23,8 p.p., acima do limite.

## Robô: decisão por UF

| UF | Pedidos | Decisão correta | Revisão humana | Erro grave |
|---|---|---|---|---|
| AL | 8 | 50,0% | 75,0% | 0 |
| BA | 4 | 100,0% | 50,0% | 0 |
| CE | 6 | 83,3% | 16,7% | 0 |
| PB | 6 | 100,0% | 50,0% | 0 |
| PE | 32 | 84,4% | 37,5% | 0 |
| PI | 3 | 100,0% | 33,3% | 0 |
| SE | 1 | 100,0% | 0,0% | 0 |

Erro grave em todos os grupos somados: 0. Diferença de decisão correta: não comparável: menos de dois grupos com 20 casos ou mais.

## Robô: decisão por serviço

| Serviço | Pedidos | Decisão correta | Revisão humana | Erro grave |
|---|---|---|---|---|
| aposentadoria_rural | 7 | 85,7% | 42,9% | 0 |
| bolsa_familia | 5 | 100,0% | 20,0% | 0 |
| bpc | 3 | 100,0% | 0,0% | 0 |
| cadunico | 6 | 83,3% | 33,3% | 0 |
| caf | 8 | 87,5% | 37,5% | 0 |
| cpf | 3 | 33,3% | 66,7% | 0 |
| fora_escopo | 6 | 100,0% | 100,0% | 0 |
| garantia_safra | 8 | 87,5% | 37,5% | 0 |
| pronaf | 8 | 75,0% | 25,0% | 0 |
| salario_maternidade_rural | 6 | 66,7% | 50,0% | 0 |

Erro grave em todos os grupos somados: 0. Diferença de decisão correta: não comparável: menos de dois grupos com 20 casos ou mais.
