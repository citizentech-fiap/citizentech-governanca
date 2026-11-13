# Model Card: classificador da pré-triagem de pedidos (robô de RPA)

## Detalhes do modelo

| Campo | Valor |
|---|---|
| Nome | classificador de intenção dos pedidos, `robo/classifier.py` |
| Versão | commit `c8dbe72` (09/11/2026), limiar de ambiguidade calibrado em validação |
| Tipo | TF-IDF de palavras (1 e 2 palavras) e de caracteres (2 a 5) com regressão logística multinomial, `class_weight=balanced`, semente 42 |
| Saída | serviço (9 classes) ou `fora_escopo`, com confiança e segunda opção |
| Regra de decisão | confiança abaixo de 0,45 ou razão entre as duas maiores probabilidades abaixo de 3,5 vai para revisão humana |
| Responsáveis | engenharia: Luís Fernando de Oliveira Salgado; Metric Owner: Jonas Alaf; validação: Ricardo de Paiva Melo |
| Contrato de métrica | [MC-02](../metric_contracts/MC-02.yaml) |

## Uso pretendido

- **Adequado:** identificar o serviço pedido pelo agricultor, conferir os documentos anexados e decidir se o
  pedido pode receber resposta automática de orientação ou se vai para um atendente.
- **Inadequado:** negar benefício, julgar elegibilidade, decidir pagamento. O robô orienta e confere
  documentos; quem decide sobre o direito é o órgão responsável.

## Dados

- Treino: 400 textos sintéticos (`data/synthetic/treino_classificador.csv`) com erros de digitação e falta
  de acento, mascarados antes do treino.
- Validação para calibrar limiares: 39 pedidos (semente 20261109), separados do teste.
- Teste: 60 pedidos sintéticos de 23 municípios do semiárido, escritos com modelos de frase diferentes do
  treino (sobreposição de sequências de 4 palavras: 0%).
- Todos os dados pessoais são fictícios: CPF com dígito verificador inválido de propósito, nomes inventados,
  e-mails em domínio de exemplo, anexos marcados como documento fictício.

## Métricas

| Métrica | Resultado | n |
|---|---|---|
| Validação cruzada no treino (5 dobras) | 98,0% | 400 |
| Classificação correta do serviço no teste | 93,8% | 48 |
| Decisão final correta | 83,3% (antes da calibração: 76,7%) | 60 |
| Erro grave: resposta automática sobre o serviço errado | 0 de 29 respostas automáticas | 29 |
| Pedidos ambíguos enviados para revisão humana | 5 de 6 (antes: 0 de 6) | 6 |
| Revisões desnecessárias (erro seguro) | 9 | 60 |

Por subgrupo, a decisão correta vai de 50% a 100% entre UFs e de 33,3% a 100% entre serviços, todos com
menos de 30 pedidos ([`evidencias/subgrupos.md`](../../evidencias/subgrupos.md)). A diferença não pode ser
separada do ruído de amostra e está registrada como exceção EX-02.

## Considerações éticas

- Celular simples e sinal fraco geram foto ruim. Anexo ilegível vira revisão humana, nunca recusa.
- O texto do pedido é mascarado antes do classificador e antes do assistente.
- O robô erra para o lado seguro: na dúvida, manda para uma pessoa. O custo é fila maior (41,7% dos pedidos).
- O atendimento presencial continua disponível para quem não tem internet.

## Limitações

- Dados sintéticos: o desempenho com pedidos reais é desconhecido.
- O OCR não foi testado com fotos reais de celular.
- Um pedido ambíguo do teste (REQ-0011) ainda é resolvido automaticamente.
- A verificação dos documentos é por tipo e palavras-chave, não verifica autenticidade.

## Monitoramento

Ver [plano de monitoramento](../plano_monitoramento.md). Por execução do robô: taxa de revisão humana, taxa
de anexos ilegíveis, distribuição dos serviços previstos e confiança média. Mudança de limiar exige RFC
([RFC-02](../rfc/)). Versão de reserva: limiar anterior à calibração (commit `1fdeb87`).

## Explicabilidade

| Campo | Valor |
|---|---|
| Método | modelo linear: o peso de cada termo para cada serviço pode ser lido diretamente |
| Tipo de explicação | local: serviço previsto, confiança, segunda opção e motivo da decisão gravados por pedido na planilha |
| Motivo ao cidadão | a resposta informa quando o pedido foi encaminhado para um atendente e por quê (documento faltando, ilegível, dúvida sobre o serviço) |
| Revisão humana (LGPD art. 20) | fila `revisao_humana` com responsável obrigatório, desfecho e data de fechamento |
| Limitação conhecida | a confiança da regressão logística não é calibrada como probabilidade real |
