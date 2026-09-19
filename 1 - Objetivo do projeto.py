# Databricks notebook source
# MAGIC %md
# MAGIC # MVP: Engenharia de Dados
# MAGIC
# MAGIC O portal da transparência é uma ferramenta do governo para garantir o controle social e fiscalizar o uso do dinheiro público. É um canal de prestação de contas que permite que qualquer cidadão acompanhe como os recursos dos impostos estão sendo arrecadados e gastos.
# MAGIC
# MAGIC # Descrição do problema 
# MAGIC
# MAGIC Como a principal função do portal é fiscalizar os gastos públicos, acompanhar as receitas, monitorar os programas sociais e combater a corrupção, vamos em cima desses dados tentar responder algumas perguntas e verificar se conseguimos essas informações com os dados disponibilizados pelo portal. Faremos, então, uma análise da execução orçamentária do governo federal através destes dados. O objetivo é responder a 5 perguntas de negócio fundamentais sobre a alocação de recursos, eficiência na execução orçamentária e identificação de oportunidades.
# MAGIC
# MAGIC **Período analisado:** Janeiro/2024 a dezembro/2025
# MAGIC
# MAGIC **Fonte de dados:** (https://portaldatransparencia.gov.br)
# MAGIC
# MAGIC **Tecnologias:** Databricks(PySpark + SQL)
# MAGIC
# MAGIC
# MAGIC # Perguntas:
# MAGIC
# MAGIC 1. Quais órgãos tiveram os maiores gastos em 2024 - 2025?
# MAGIC 2. Como os gastos evoluíram mensalmente ao longo do tempo?
# MAGIC 3. Quais funções do governo (saúde, educação, defesa) receberam mais recursos?
# MAGIC 4. Qual a diferença entre o orçamento previsto (dotação) e o executado (pago)?
# MAGIC 5. Quais os top 10 programas que mais receberam recursos?
# MAGIC
# MAGIC