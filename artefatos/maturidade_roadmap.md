# Maturidade e roadmap

## DAMA-DMBOK2 por área

Escala: 1 inicial, 2 repetível, 3 definido, 4 gerenciado, 5 otimizado. Áreas diferentes podem estar em
níveis diferentes.

| Área | Nível | Por quê | O que falta para subir |
|---|---|---|---|
| Governança de dados | 2 | papéis e métricas definidos neste repositório, mas recentes e sem rotina de reunião | aprovações registradas por pull request; revisão periódica dos contratos |
| Qualidade de dados | 3 | validação na entrada dos três módulos (dados ausentes não viram zero), conjuntos de referência com hash, placar contra o IBGE | alertas automáticos em execução, não só a cada versão |
| Metadados | 2 | data de coleta e hash por Carta de Serviço, contratos de dados no robô e no painel | catálogo único com dono e atualização de cada conjunto |
| Segurança de dados | 2 | máscara de PII, dados fora do git, só dados sintéticos | controle de acesso, autenticação, expurgo automático |
| Arquitetura de dados | 3 | camadas separadas e testadas no painel, contratos entre módulos | versão de um módulo fixada dentro do outro, sem caminho relativo |
| Dados de referência | 3 | catálogo de serviços e documentos num único `config.yaml` do robô, lido pelo painel; lista oficial de municípios do IBGE | identificador estável para cada versão do catálogo |
| BI e analytics | 3 | métricas com contrato, placar estimado x real, painel que não recalcula fora do pipeline | changelog e versão do contrato visíveis no painel |
| Integração | 2 | robô importa o assistente; painel lê a planilha do robô pelas colunas do contrato | desfecho da fila de revisão voltando ao painel |

## MLOps

Estamos no **nível 1** (pipeline: treino e avaliação automatizados, registro básico, retreino manual) com
peças do nível 2: o gate é automatizado e os limiares do robô e do assistente foram escolhidos em validação
separada. Não temos registro de modelos com estados nem monitoramento contínuo em produção.

## Maturidade de dados para o setor público

| Dimensão | Situação |
|---|---|
| Estratégia de dados | o projeto usa dados abertos (gov.br, IBGE, Portal da Transparência) e diz na tela o que é simulado |
| Estruturas de governança | RACI, contratos de métrica, RFC e gate neste repositório |
| Infraestrutura técnica | ferramentas abertas e gratuitas: Python, Streamlit, reanálise ERA5, cota gratuita do Gemini |
| Capacidades humanas | o painel foi simplificado para uso sem treinamento; a fila de revisão pede só desfecho e responsável |
| Engajamento do cidadão | orientação com fonte oficial; atendimento presencial mantido; falta canal para o cidadão contestar a triagem |

## Roadmap

| Horizonte | Ação | Responsável |
|---|---|---|
| Curto (até a próxima safra) | pull request obrigatório com aprovação do Metric Owner; desfecho da fila no painel; expurgo pelos prazos do inventário | Luís (R), Metric Owners (A) |
| Curto | perguntas reais de agricultores no conjunto de validação do assistente; 30 pedidos por UF no teste do robô | Jonas |
| Médio (1 a 2 safras) | calibrar Ky por UF com validação separada por safra (fecha EX-01); autenticação do gestor e da fila | Ricardo (A), Luís (R) |
| Médio | verificação semântica das afirmações do assistente (caso Q23) | Luís (R), Jonas (validação) |
| Longo | registro de modelos com estados e volta automática; catálogo de dados único; auditoria externa de equidade | órgão operador |
