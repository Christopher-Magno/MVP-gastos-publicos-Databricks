# Databricks notebook source
# Conectar ao catalogo e schema Silver
spark.sql("USE CATALOG MVP_gastos_publicos")
spark.sql("USE SCHEMA silver")

# COMMAND ----------

from pyspark.sql.functions import col, regexp_replace, trim, when, lit, to_date, concat_ws, lpad
from pyspark.sql.types import DecimalType, IntegerType

# Ler a tabela Bronze
df = spark.table("MVP_gastos_publicos.bronze.gastos_publicos")

#Fazendo as devidas limpezas e conversoes nos dados 
# Como o os valores financeiros do arquivo estão como STRING temos que converter para decimal para que depois consiga fazer os devidos cálculos

df_silver = (
    df
    .withColumn("SALDO_PLOA",
                when(trim(col("SALDO_PLOA")).isin(["", "-"]), lit(None))
                .otherwise(regexp_replace(regexp_replace(trim(col("SALDO_PLOA")), "\\.", ""), ",", ".").cast(DecimalType(18, 2))))
    .withColumn("DOTACAO_INICIAL",
                when(trim(col("DOTACAO_INICIAL")).isin(["", "-"]), lit(None))
                .otherwise(regexp_replace(regexp_replace(trim(col("DOTACAO_INICIAL")), "\\.", ""), ",", ".").cast(DecimalType(18, 2))))
    .withColumn("DOTACAO_ATUALIZADA",
                when(trim(col("DOTACAO_ATUALIZADA")).isin(["", "-"]), lit(None))
                .otherwise(regexp_replace(regexp_replace(trim(col("DOTACAO_ATUALIZADA")), "\\.", ""), ",", ".").cast(DecimalType(18, 2))))
    .withColumn("DESPESAS_EMPENHADAS",
                when(trim(col("DESPESAS_EMPENHADAS")).isin(["", "-"]), lit(None))
                .otherwise(regexp_replace(regexp_replace(trim(col("DESPESAS_EMPENHADAS")), "\\.", ""), ",", ".").cast(DecimalType(18, 2))))
    .withColumn("DESPESAS_LIQUIDADAS",
                when(trim(col("DESPESAS_LIQUIDADAS")).isin(["", "-"]), lit(None))
                .otherwise(regexp_replace(regexp_replace(trim(col("DESPESAS_LIQUIDADAS")), "\\.", ""), ",", ".").cast(DecimalType(18, 2))))
    .withColumn("DESPESAS_PAGAS",
                when(trim(col("DESPESAS_PAGAS")).isin(["", "-"]), lit(None))
                .otherwise(regexp_replace(regexp_replace(trim(col("DESPESAS_PAGAS")), "\\.", ""), ",", ".").cast(DecimalType(18, 2))))
    .withColumn("RESTOS_A_PAGAR_PAGOS",
                when(trim(col("RESTOS_A_PAGAR_PAGOS")).isin(["", "-"]), lit(None))
                .otherwise(regexp_replace(regexp_replace(trim(col("RESTOS_A_PAGAR_PAGOS")), "\\.", ""), ",", ".").cast(DecimalType(18, 2))))
    .withColumn("PAGAMENTOS_TOTAIS",
                when(trim(col("PAGAMENTOS_TOTAIS")).isin(["", "-"]), lit(None))
                .otherwise(regexp_replace(regexp_replace(trim(col("PAGAMENTOS_TOTAIS")), "\\.", ""), ",", ".").cast(DecimalType(18, 2))))
    
    # Convertendo colunas de codigo para INTEGER
    .withColumn("ID_ANO", col("ID_ANO").cast(IntegerType()))
    .withColumn("ID_MES", col("ID_MES").cast(IntegerType()))

    # Padronizando o formato das datas
    .withColumn("data_referencia",
                to_date(concat_ws("-", col("ID_ANO"), lpad(col("ID_MES"), 2, "0"), lit("01")), "yyyy-MM-dd"))
)


display(df_silver.limit(5))

# COMMAND ----------

# Salvar a tabela no schema silver 
df_silver.write.format("delta").mode("overwrite").saveAsTable("MVP_gastos_publicos.silver.gastos_publicos")

# COMMAND ----------

# MAGIC %sql
# MAGIC -- Visualizando os dados limpos
# MAGIC SELECT 
# MAGIC     ID_ANO,
# MAGIC     ID_MES,
# MAGIC     data_referencia,
# MAGIC     ORGAO_DESCRICAO,
# MAGIC     PAGAMENTOS_TOTAIS,
# MAGIC     DESPESAS_EMPENHADAS
# MAGIC FROM MVP_gastos_publicos.silver.gastos_publicos
# MAGIC LIMIT 10;