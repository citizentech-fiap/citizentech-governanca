# Desempenho por subgrupo

Gerado em 13/11/2026 sobre as versões de `versoes.yaml`:

- genai: `e3f65dd`
- rpa: `c8dbe72`
- dashboard: `1514bb2`

Limite de diferença entre subgrupos: 5 pontos percentuais. Subgrupo com menos de 30 casos: amostra pequena.

## Painel: acerto do critério de 40% por UF (milho)

| UF | Pares município-safra | Acerto |
|---|---|---|
| AL | 28 | 64,3% |
| BA | 56 | 55,4% |
| CE | 56 | 69,6% |
| PB | 42 | 69,0% |
| PE | 70 | 60,0% |
| PI | 28 | 75,0% |
| RN | 28 | 46,4% |
| SE | 14 | 71,4% |

Geral: 63,0%. Diferença máxima: 14,3 p.p., acima do limite.

## Painel: acerto do critério de 40% por UF (feijao)

| UF | Pares município-safra | Acerto |
|---|---|---|
| AL | 28 | 53,6% |
| BA | 56 | 51,8% |
| CE | 56 | 60,7% |
| PB | 42 | 73,8% |
| PE | 70 | 57,1% |
| PI | 28 | 60,7% |
| RN | 28 | 50,0% |
| SE | 14 | 42,9% |

Geral: 57,8%. Diferença máxima: 22,0 p.p., acima do limite.

## Robô: decisão correta por UF

| UF | Pedidos | Decisão correta | Revisão humana |
|---|---|---|---|
| AL | 8 | 50,0% | 75,0% |
| BA | 4 | 100,0% | 50,0% |
| CE | 6 | 83,3% | 16,7% |
| PB | 6 | 100,0% | 50,0% |
| PE | 32 | 84,4% | 37,5% |
| PI | 3 | 100,0% | 33,3% |
| SE | 1 | 100,0% | 0,0% |

Diferença máxima de decisão correta: 50,0 p.p., acima do limite (amostras pequenas, sinal fraco).

## Robô: decisão correta por serviço

| Serviço | Pedidos | Decisão correta | Revisão humana |
|---|---|---|---|
| aposentadoria_rural | 7 | 85,7% | 42,9% |
| bolsa_familia | 5 | 100,0% | 20,0% |
| bpc | 3 | 100,0% | 0,0% |
| cadunico | 6 | 83,3% | 33,3% |
| caf | 8 | 87,5% | 37,5% |
| cpf | 3 | 33,3% | 66,7% |
| fora_escopo | 6 | 100,0% | 100,0% |
| garantia_safra | 8 | 87,5% | 37,5% |
| pronaf | 8 | 75,0% | 25,0% |
| salario_maternidade_rural | 6 | 66,7% | 50,0% |

Diferença máxima de decisão correta: 66,7 p.p., acima do limite (amostras pequenas, sinal fraco).
