# Disciplinas da Global Solution não integradas

A Global Solution 2026.2 tem nove disciplinas. Quatro estão integradas ao CitizenTech: AI for RPA, Generative AI,
Front-end e Governança em IA e Business Analytics. As outras cinco não foram integradas, pelos motivos abaixo.

## PLN, Chatbots & Virtual Agents

A GS desta disciplina pede uma fábrica de corpus para ajustar um modelo pequeno, com corpus de treino, conjunto de
teste e anonimização com reconhecimento de nomes. Essa entrega não foi integrada. O CitizenTech já coleta as
cartas com metadados e mascara CPF, e-mail, telefone e RG, mas não gera corpus de treino. Como o próprio
enunciado separa o que se treina (tom e recusa) do que se consulta (valores e prazos), os fatos do Garantia-Safra
ficaram na busca com citação.

## Visão Computacional

A GS desta disciplina pede um módulo que identifique fissuras em concreto ou danos na pavimentação, com
modelo pré-treinado, métricas de classificação ou detecção e medida de latência. O tema é manutenção urbana,
fora do público do CitizenTech, e a entrega não foi integrada. A visão computacional do projeto se limita ao
OCR pronto do robô, que reconheceu 123 de 123 anexos sintéticos legíveis e recusou 5 de 5 degradados. No tema
da seca, o uso natural seria classificar fotos da lavoura enviadas pelo agricultor para apoiar a vistoria.

## Physical Computing, Embedded AI, Robotics & Cognitive IoT

A GS desta disciplina já define o projeto: o OuviAí, que reconhece sons domésticos para apoiar pessoas com
deficiência auditiva. O público e o problema são outros, e ligar o OuviAí ao agricultor do semiárido seria uma
conexão artificial. No CitizenTech, o ponto natural para IA embarcada seriam sensores de umidade do solo.

## Computação Quântica & IA

A GS desta disciplina pede um gargalo do protótipo e uma capacidade quântica para resolvê-lo. Na escala atual
não há gargalo: o classificador treina em segundos e o modelo do painel é uma fórmula fechada. No futuro, fariam
sentido a otimização da ordem de vistorias e a criptografia pós-quântica para CPF e NIS guardados por anos.

## Cluster Computing, Computação Neuromórfica e Supercomputadores

A GS desta disciplina pede a simulação, no iSPD, de uma carga do CitizenTech em clusters de 2 e de 4 workers. A
simulação não foi feita. A carga candidata é o OCR dos anexos, que leva cerca de 1,3 segundo por imagem e seria
dividida entre workers numa safra de seca com milhares de pedidos.
