# Databricks notebook source
# MAGIC %sql
# MAGIC -- Define o catalog e schema
# MAGIC use catalog MVP_gastos_publicos;
# MAGIC use schema bronze;

# COMMAND ----------

# lendo o arquivo csv de 2024 com a indicaçao do separador ;
df_2024 = spark.read.format("csv").options(
    header=True,
    sep=";"
).load("/Volumes/MVP_gastos_publicos/staging/dados_gastos_publicos/gastos2024.csv")

# E lendo o arquivo CSV de 2025 tambem com a indicaçao do separador ;
df_2025 = spark.read.format("csv").options(
    header=True,
    sep=";"
).load("/Volumes/MVP_gastos_publicos/staging/dados_gastos_publicos/gastos2025.csv")

# Unindo os dois dataframes
df_bronze = df_2024.union(df_2025)

# Corrigindo o erro de algumas colunas que continham espaços a mais
# Para isso precisei remover os espaços usando .strip() no nome de cada coluna e renomear elas
new_columns = []
for col in df_bronze.columns:
    new_columns.append(col.strip()) 
df_bronze = df_bronze.toDF(*new_columns)

# Visualizar
display(df_bronze)

# COMMAND ----------

# salvando dataframe como tabela no Unity Catalog
df_bronze.write.format("delta").mode("overwrite").saveAsTable("MVP_gastos_publicos.bronze.gastos_publicos")


# COMMAND ----------

# MAGIC %sql
# MAGIC -- Adicionar descricao na tabela
# MAGIC COMMENT ON TABLE MVP_gastos_publicos.bronze.gastos_publicos IS 'Dados brutos de gastos publicos federais (2024-2025)';
# MAGIC
# MAGIC -- Adicionar descricoes nas colunas principais
# MAGIC COMMENT ON COLUMN MVP_gastos_publicos.bronze.gastos_publicos.ID_ANO IS 'Ano da despesa';
# MAGIC COMMENT ON COLUMN MVP_gastos_publicos.bronze.gastos_publicos.ID_MES IS 'Mes da despesa';
# MAGIC COMMENT ON COLUMN MVP_gastos_publicos.bronze.gastos_publicos.ORGAO_DESCRICAO IS 'Nome do orgao';
# MAGIC COMMENT ON COLUMN MVP_gastos_publicos.bronze.gastos_publicos.PAGAMENTOS_TOTAIS IS 'Valor total pago';

# COMMAND ----------

# MAGIC %sql
# MAGIC DESCRIBE MVP_gastos_publicos.bronze.gastos_publicos;

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT * FROM MVP_gastos_publicos.bronze.gastos_publicos LIMIT 10;