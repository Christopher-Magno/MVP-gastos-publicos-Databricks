# Databricks notebook source
# MAGIC %sql
# MAGIC -- selecionar o catalogo e schema 
# MAGIC use catalog MVP_gastos_publicos;
# MAGIC use schema staging;

# COMMAND ----------

# MAGIC %sql
# MAGIC --criar o volume para os dados 
# MAGIC create volume if not exists dados_gastos_publicos

# COMMAND ----------

# MAGIC %sql
# MAGIC show volumes in MVP_gastos_publicos.staging;

# COMMAND ----------

# MAGIC %md
# MAGIC # Dados
# MAGIC
# MAGIC **Fonte:** Portal da Transparência do Governo Federal
# MAGIC
# MAGIC **URL:** https://portaldatransparencia.gov.br/download-de-dados/despesas
# MAGIC
# MAGIC **Período:** 2024 e 2025
# MAGIC
# MAGIC **Formato:** CSV (separador ;)
# MAGIC
# MAGIC **Tamanho total:** 220 MB (3 arquivos + metadados)

# COMMAND ----------

# MAGIC %md
# MAGIC