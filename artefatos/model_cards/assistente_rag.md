# Model Card: assistente de serviços públicos (citizen_rag)

## Detalhes do modelo

| Campo | Valor |
|---|---|
| Nome | citizen_rag, assistente de orientação sobre serviços públicos |
| Versão | prompt v3 com verificação por afirmação, commit `e3f65dd` (09/11/2026) |
| Tipo | geração aumentada por recuperação (RAG) |
| Recuperação | BM25 e embeddings multilingual-e5-small, fundidos por RRF, 5 trechos |
| Geração | Gemini `gemini-3.5-flash-lite`, com `gemini-3.6-flash` como reserva, via API gratuita |
| Responsáveis | engenharia: Luís Fernando de Oliveira Salgado; Metric Owner: Ricardo de Paiva Melo; validação: Jonas Alaf |
| Contrato de métrica | [MC-01](../metric_contracts/MC-01.yaml) |

## Uso pretendido

- **Adequado:** orientar o agricultor familiar e o atendente sobre requisitos, documentos, etapas, canais e
  prazos de nove serviços (Garantia-Safra, CAF, Pronaf, aposentadoria rural, salário-maternidade rural,
  Cadastro Único, Bolsa Família, BPC e CPF), sempre citando a Carta de Serviço de origem.
- **Inadequado:** dizer se uma pessoa tem direito a um benefício, consultar a situação de um pedido
  individual, dar orientação jurídica ou médica, responder sobre serviços fora das cartas coletadas.
  Nesses casos o assistente se abstém e indica o canal oficial.

## Dados

- Corpus: 9 Cartas de Serviço do gov.br coletadas pelo robô em 05/11/2026, com data de coleta, origem e hash
  por carta (`genAI/data/corpus/FONTES.md`). Nenhum dado pessoal no corpus.
- Avaliação: 40 perguntas de teste (18 respondíveis, 4 em várias rodadas, 6 sem resposta, 4 ambíguas,
  4 fora de escopo, 4 ataques) e 16 de validação, escritas depois da primeira rodada e não usadas para
  desenhar o prompt v3. Os fatos esperados foram conferidos no texto do corpus.
- Limitação: as perguntas foram escritas pela equipe, não por agricultores.

## Métricas

| Métrica | Resultado | Fonte |
|---|---|---|
| Serviço certo entre os 5 trechos recuperados | 95,3% | relatório de avaliação do módulo |
| Corretas entre respondíveis, teste | 22 de 22 (rodada 1: 15 de 22) | `evidencias/metricas.md` |
| Corretas entre respondíveis, validação | 6 de 6 (rodada 1: 4 de 6) | `evidencias/metricas.md` |
| Abstenção correta sem resposta ou fora de escopo | 9 de 10 | `evidencias/metricas.md` |
| Respostas com afirmação sem suporte | 1 (Q23) | `evidencias/metricas.md` |
| Ataques de injeção bloqueados | 4 de 4 | revisão independente do módulo |
| Vazamentos com proteções ligadas | 0 em 12 cenários | `evidencias/metricas.md` |

As respostas foram julgadas por um revisor de outra família de modelo (GPT), com regras escritas, para não
deixar o Gemini corrigir o próprio Gemini. Métrica por subgrupo não se aplica: as perguntas não carregam
atributo de grupo.

## Considerações éticas

- O público tem pouca conectividade e pouca familiaridade com sistemas. O prompt pede linguagem simples e
  resposta direta no início.
- Uma resposta plausível e errada é pior que nenhuma: o assistente prefere se abster quando a evidência é
  fraca (gate de evidência antes de chamar o modelo).
- Dados pessoais da pergunta são mascarados antes da busca e do modelo. Pedidos de dados de terceiros
  ("CPF da vizinha") são bloqueados.
- O assistente não substitui o atendimento presencial, que continua sendo o canal de quem não tem internet.

## Limitações

- A verificação por afirmação é por palavras: remove canal ou link sem suporte, mas não pega função errada
  atribuída a um link verdadeiro (caso Q23).
- Pergunta vaga pode ser barrada pelo gate mesmo havendo trechos úteis (caso V13).
- O limiar do gate (0,85) tem margem de 0,024 entre respondíveis e fora de escopo, medido em poucas
  perguntas.
- Depende de cota gratuita do Gemini. Sem chave ou sem rede, devolve os trechos e se abstém.

## Monitoramento

Frequência, limiares e responsáveis estão no [plano de monitoramento](../plano_monitoramento.md). Em
resumo: o MC-01 é recalculado a cada mudança de prompt, modelo, corpus ou limiar; vazamento maior que zero
bloqueia a versão; a taxa de abstenção e a data de coleta das cartas são acompanhadas para detectar
mudança no corpus (as Cartas de Serviço mudam sem aviso). Versão de reserva: prompt v2 (commit `1f87cdb`).

## Explicabilidade

| Campo | Valor |
|---|---|
| Método | citação obrigatória e verificada: cada afirmação aponta para o trecho numerado de onde veio |
| Tipo de explicação | local, por resposta: trecho, título da carta, seção e link oficial |
| Registro técnico | `last_trace` com sinais de busca, decisão do gate, modelo, versão de prompt, trechos removidos pela verificação |
| Atendimento ao cidadão (LGPD art. 20) | o assistente não decide sobre direitos; quando há decisão, ela vem do robô ou do servidor, com revisão humana |
| Limitação conhecida | a citação mostra de onde veio a informação, não prova que o modelo a interpretou corretamente |
