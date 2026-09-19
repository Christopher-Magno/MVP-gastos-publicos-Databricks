# Databricks notebook source
# MAGIC %sql
# MAGIC -- Criando o catalogo 
# MAGIC -- if not exists usamos para evitar erros criando apenas se nao existir o catalogo
# MAGIC create catalog if not exists MVP_gastos_publicos
# MAGIC
# MAGIC

# COMMAND ----------

# MAGIC %sql
# MAGIC -- usando o catálogo criado 
# MAGIC use catalog MVP_gastos_publicos

# COMMAND ----------

# MAGIC %sql
# MAGIC -- criando o schema staging 
# MAGIC create schema if not exists staging
# MAGIC

# COMMAND ----------

# MAGIC %sql
# MAGIC -- deleta se existir algum schema bronze 
# MAGIC drop schema if exists bronze cascade 

# COMMAND ----------

# MAGIC %sql
# MAGIC -- agora crio o schema bronze 
# MAGIC create schema if not exists bronze 

# COMMAND ----------

# MAGIC %sql
# MAGIC -- deleta schema silver se existir 
# MAGIC drop schema if exists silver cascade

# COMMAND ----------

# MAGIC %sql
# MAGIC -- criando o schema silver 
# MAGIC create schema if not exists silver

# COMMAND ----------

# MAGIC %sql
# MAGIC -- deleta schema gold se existir
# MAGIC drop schema if exists gold cascade 

# COMMAND ----------

# MAGIC %sql
# MAGIC --criando o schema gold 
# MAGIC create schema if not exists gold

# COMMAND ----------

# MAGIC %sql
# MAGIC -- visualizar os schemas criados 
# MAGIC show schemas in MVP_gastos_publicos