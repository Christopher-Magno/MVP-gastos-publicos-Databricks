# Databricks notebook source
spark.sql("USE CATALOG MVP_gastos_publicos")
spark.sql("USE SCHEMA gold")

# COMMAND ----------

# MAGIC %sql
# MAGIC -- Criar tabela Gold com dados tratados e colunas relevantes para analise de negocio
# MAGIC
# MAGIC CREATE OR REPLACE TABLE gastos_publicos AS
# MAGIC SELECT
# MAGIC     ID_ANO,
# MAGIC     ID_MES,
# MAGIC     data_referencia,
# MAGIC     ORGAO_DESCRICAO,
# MAGIC     NO_FUNCAO_PT,
# MAGIC     NO_SUBFUNCAO_PT,
# MAGIC     NO_PROGRAMA_PT,
# MAGIC     NO_ACAO,
# MAGIC     DOTACAO_INICIAL,
# MAGIC     DOTACAO_ATUALIZADA,
# MAGIC     DESPESAS_EMPENHADAS,
# MAGIC     DESPESAS_LIQUIDADAS,
# MAGIC     DESPESAS_PAGAS,
# MAGIC     RESTOS_A_PAGAR_PAGOS,
# MAGIC     PAGAMENTOS_TOTAIS,
# MAGIC     Poder_Orgao,
# MAGIC     Primaria_Financeira
# MAGIC FROM MVP_gastos_publicos.silver.gastos_publicos
# MAGIC WHERE PAGAMENTOS_TOTAIS IS NOT NULL  

# COMMAND ----------

# MAGIC %sql
# MAGIC -- Verificar criacao da tabela Gold
# MAGIC SELECT *
# MAGIC FROM MVP_gastos_publicos.gold.gastos_publicos
# MAGIC LIMIT 10;

# COMMAND ----------

# MAGIC %sql
# MAGIC -- Criar tabela agregada para responder os orgaos que mais gastaram e a evolução dos gastos
# MAGIC --- Agregação: SUM dos valores financeiros agrupados por ORGAO + ANO 
# MAGIC CREATE OR REPLACE TABLE gastos_por_orgao_ano AS
# MAGIC SELECT
# MAGIC     ID_ANO,
# MAGIC     ORGAO_DESCRICAO,
# MAGIC     Poder_Orgao,
# MAGIC     COUNT(*) as total_registros,
# MAGIC     SUM(DOTACAO_INICIAL) as dotacao_inicial_total,
# MAGIC     SUM(DOTACAO_ATUALIZADA) as dotacao_atualizada_total,
# MAGIC     SUM(DESPESAS_EMPENHADAS) as despesas_empenhadas_total,
# MAGIC     SUM(DESPESAS_LIQUIDADAS) as despesas_liquidadas_total,
# MAGIC     SUM(DESPESAS_PAGAS) as despesas_pagas_total,
# MAGIC     SUM(PAGAMENTOS_TOTAIS) as pagamentos_totais
# MAGIC FROM MVP_gastos_publicos.silver.gastos_publicos
# MAGIC WHERE PAGAMENTOS_TOTAIS IS NOT NULL
# MAGIC GROUP BY ID_ANO, ORGAO_DESCRICAO, Poder_Orgao
# MAGIC ORDER BY ID_ANO DESC, pagamentos_totais DESC;

# COMMAND ----------



# COMMAND ----------

# MAGIC %sql
# MAGIC -- Criar tabela agregada para responder "Quais areas recebem mais recursos?"
# MAGIC
# MAGIC CREATE OR REPLACE TABLE gastos_por_funcao AS
# MAGIC SELECT
# MAGIC     ID_ANO,
# MAGIC     NO_FUNCAO_PT as funcao,
# MAGIC     COUNT(*) as total_registros,
# MAGIC     SUM(DOTACAO_INICIAL) as dotacao_inicial_total,
# MAGIC     SUM(DOTACAO_ATUALIZADA) as dotacao_atualizada_total,
# MAGIC     SUM(DESPESAS_EMPENHADAS) as despesas_empenhadas_total,
# MAGIC     SUM(DESPESAS_LIQUIDADAS) as despesas_liquidadas_total,
# MAGIC     SUM(DESPESAS_PAGAS) as despesas_pagas_total,
# MAGIC     SUM(PAGAMENTOS_TOTAIS) as pagamentos_totais
# MAGIC FROM MVP_gastos_publicos.silver.gastos_publicos
# MAGIC WHERE PAGAMENTOS_TOTAIS IS NOT NULL
# MAGIC GROUP BY ID_ANO, NO_FUNCAO_PT
# MAGIC ORDER BY ID_ANO DESC, pagamentos_totais DESC;

# COMMAND ----------

# MAGIC %sql
# MAGIC -- Criar uma tabela para serie temporal dos gastos
# MAGIC CREATE OR REPLACE TABLE evolucao_mensal AS
# MAGIC SELECT
# MAGIC     ID_ANO,
# MAGIC     ID_MES,
# MAGIC     data_referencia,
# MAGIC     COUNT(*) as total_registros,
# MAGIC     SUM(DOTACAO_INICIAL) as dotacao_inicial_total,
# MAGIC     SUM(DOTACAO_ATUALIZADA) as dotacao_atualizada_total,
# MAGIC     SUM(DESPESAS_EMPENHADAS) as despesas_empenhadas_total,
# MAGIC     SUM(DESPESAS_LIQUIDADAS) as despesas_liquidadas_total,
# MAGIC     SUM(DESPESAS_PAGAS) as despesas_pagas_total,
# MAGIC     SUM(PAGAMENTOS_TOTAIS) as pagamentos_totais
# MAGIC FROM MVP_gastos_publicos.silver.gastos_publicos
# MAGIC WHERE PAGAMENTOS_TOTAIS IS NOT NULL
# MAGIC GROUP BY ID_ANO, ID_MES, data_referencia
# MAGIC ORDER BY data_referencia;

# COMMAND ----------

# MAGIC %sql
# MAGIC -- Verificar tabelas Gold foram criadas
# MAGIC SHOW TABLES IN MVP_gastos_publicos.gold;