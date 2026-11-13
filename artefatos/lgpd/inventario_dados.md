# Inventário de dados pessoais

No protótipo, todos os dados pessoais são fictícios: CPF com dígito verificador inválido de propósito, nomes
inventados, e-mails em domínio de exemplo e anexos marcados como documento fictício. O inventário descreve
o tratamento que existiria em operação real e os controles que o código já aplica.

Controlador em operação real: o órgão público responsável pelo atendimento (por exemplo, a secretaria
municipal de agricultura que opera o robô e o painel). Encarregado no projeto: Jonas Alaf.

| Dado | Módulo | Finalidade | Base legal | Onde fica | Retenção proposta | Controle já aplicado |
|---|---|---|---|---|---|---|
| Nome, e-mail, CPF do pedido | RPA | identificar o pedido e responder ao cidadão | art. 7º, III, e art. 23 (política pública) | JSON do pedido em `processed/` | 1 ano após o fechamento do pedido | fora do git; máscara antes do classificador e do assistente |
| Texto livre do pedido | RPA, GenAI | entender o serviço pedido | art. 7º, III | JSON do pedido | 1 ano | máscara de CPF, e-mail, telefone e RG antes de qualquer modelo |
| Anexos (documentos com foto) | RPA | conferir documentos exigidos | art. 7º, III | `processed/` | 1 ano | OCR local, imagem não sai da máquina |
| Decisão, serviço, município do pedido | RPA, Dashboard | controle da fila e priorização | art. 7º, III | planilha de controle | 5 anos (prestação de contas) | planilha sem nome e sem CPF; painel lê só as colunas do contrato |
| Nome e e-mail na resposta | RPA | enviar a orientação | art. 7º, III | `.eml` em `outbox/` | até o envio, depois 90 dias | envio desligado por padrão; credenciais só no ambiente |
| Responsável pelo fechamento da fila | RPA | responsabilização | art. 7º, II e III | aba `revisao_humana` | 5 anos | campo obrigatório no fechamento |
| Identificação funcional do gestor | Dashboard | responsabilização da decisão | art. 7º, II e III | `output/decisoes.jsonl` | 5 anos | registro só de acréscimo; fora do git |
| NIS e nome do favorecido (Portal da Transparência) | Dashboard | contar famílias pagas por município | dado público (art. 7º, § 3º) | só em memória | nenhuma | nome nunca carregado; NIS só para contar; nada gravado |
| Pergunta ao assistente | GenAI | responder à dúvida | art. 7º, III | memória e cache de respostas | cache: 30 dias | máscara antes da busca e do modelo; log sem o texto da pergunta |
| Conversa usada para avaliar o assistente | GenAI | melhorar a qualidade das respostas | art. 7º, I (consentimento) | conjunto de avaliação | 1 ano, depois anonimizar | só com o [termo de consentimento](termo_consentimento_chat.docx) |
| Pergunta mascarada enviada ao modelo de linguagem | GenAI | gerar a resposta | art. 7º, III, com transferência internacional (art. 33) | serviço Gemini do Google, fora do Brasil | não armazenada pelo projeto; política do fornecedor | máscara antes do envio; em operação real, contrato com cláusulas de proteção ou modelo hospedado no país |

## Lacunas conhecidas

- A retenção proposta acima ainda não está implementada: pastas de pedidos processados, saídas e cache
  mantêm os arquivos até remoção manual.
- A máscara usa expressões regulares e não cobre nomes próprios.
- O protótipo usa a cota gratuita do Gemini, cujos termos permitem ao fornecedor usar o conteúdo enviado. Em
  operação real, isso exige troca para plano pago com cláusulas contratuais (art. 33, II) ou modelo local.
- Não há controle de acesso à planilha nem autenticação do gestor no painel.
