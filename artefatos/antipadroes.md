# Antipadrões: o que evitamos e o que ainda temos

| Antipadrão | Situação | Como evitamos ou onde ainda aparece |
|---|---|---|
| Gate de carimbo (aprovação sem critério) | evitado | o gate tem oito critérios verificados por script e grava o detalhe de cada um em `evidencias/gate.md` |
| Gate informal (sem registro) | parcial | o resultado do gate fica versionado com o commit avaliado, mas a aprovação do Metric Owner ainda não tem registro formal com data e decisão |
| Contrato depois do painel | presente | os Metric Contracts foram escritos depois que os módulos já existiam; foram feitos a partir das métricas que os módulos já mediam e passam a valer para as próximas versões |
| Mudança silenciosa | evitado | conjuntos de referência com hash; `versoes.yaml`; RFC para mudança de significado |
| Multiplicidade de contas | evitado | uma definição por métrica nos Metric Contracts, calculada pelo código do próprio módulo |
| Planilha paralela | evitado | a planilha do robô é o registro oficial e o painel a lê pelas colunas do contrato, sem cópia editada à mão |
| Front-end que recalcula | evitado | no painel, a interface não importa pipelines nem providers; um teste de arquitetura impede |
| Goal seeking (ajustar o filtro para bater a meta) | evitado em dois módulos, presente em um | robô e assistente escolheram limiares na validação antes do teste. O modelo hídrico foi calibrado e avaliado nas mesmas safras |
| Modelo órfão | evitado | cada modelo tem Model Card com responsável e Metric Owner |
| Governança reativa | parcial | o plano de monitoramento e as exceções existem antes do uso real; o monitoramento contínuo em produção ainda não existe |
| Governança só no papel | parcial | os critérios do gate são executáveis; a aprovação do Metric Owner ainda não é imposta pelo repositório |
| Quem desenvolve promove sozinho | presente | as mudanças entraram direto na branch principal, sem pull request revisado por outro integrante. A separação está definida no RACI e é o primeiro item do roadmap |
| Múltiplas fontes verdadeiras | presente em um ponto | o catálogo de serviços vive no robô e o painel o lê de lá, mas o assistente tem o próprio corpus sincronizado por script |
| Trilha sem autenticação | presente | o nome do gestor e do atendente é digitado, sem login |
