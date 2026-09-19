# Databricks notebook source
# DBTITLE 1,Introducao
# MAGIC %md
# MAGIC # Análise
# MAGIC
# MAGIC Esta etapa está dividida em **qualidade de dados** e **solução do problema**.

# COMMAND ----------

spark.sql("USE CATALOG MVP_gastos_publicos")
spark.sql("USE SCHEMA gold")

# COMMAND ----------

from pyspark.sql.functions import col, count, when, isnan

# Verificar se existem dados nulos (NULL) para cada coluna

df = spark.table("gastos_publicos")

null_counts = df.select([
    count(when(col(c).isNull(), c)).alias(c)
    for c in df.columns
])


display(null_counts)

# COMMAND ----------

# Verificar se existem valores negativos nas colunas financeiras

df = spark.table("gastos_publicos")

colunas_financeiras = ['DOTACAO_INICIAL', 'DOTACAO_ATUALIZADA', 'DESPESAS_EMPENHADAS', 
                       'DESPESAS_LIQUIDADAS', 'DESPESAS_PAGAS', 'PAGAMENTOS_TOTAIS']

for coluna in colunas_financeiras:
    negativos = df.filter(col(coluna) < 0).count()
    print(f"{coluna}: {negativos} valores negativos")

# COMMAND ----------

# Verificar valores máximo e mínimo das colunas financeiras

df = spark.table("gastos_publicos")

from pyspark.sql.functions import max as spark_max, min as spark_min

extremos = df.agg(
    spark_max("PAGAMENTOS_TOTAIS").alias("max_pagamento"),
    spark_min("PAGAMENTOS_TOTAIS").alias("min_pagamento"),
    spark_max("DESPESAS_EMPENHADAS").alias("max_empenhado"),
    spark_min("DESPESAS_EMPENHADAS").alias("min_empenhado")
)

print("Valores extremos (máximo e mínimo):")
display(extremos)

# COMMAND ----------

# Verificar se existem registros duplicados

df = spark.table("gastos_publicos")

total_registros = df.count()
registros_unicos = df.distinct().count()
duplicados = total_registros - registros_unicos

print(f"Total de registros: {total_registros}")
print(f"Registros únicos: {registros_unicos}")
print(f"Registros duplicados: {duplicados}")

# COMMAND ----------

# MAGIC %sql
# MAGIC -- Verificar se todos os meses de 2024 e 2025 estão presentes
# MAGIC
# MAGIC SELECT 
# MAGIC     ID_ANO,
# MAGIC     ID_MES,
# MAGIC     COUNT(*) as total_registros
# MAGIC FROM evolucao_mensal
# MAGIC GROUP BY ID_ANO, ID_MES
# MAGIC ORDER BY ID_ANO, ID_MES;

# COMMAND ----------

# DBTITLE 1,Resumo da qualidade dos dados
# MAGIC %md
# MAGIC ### Pronto! 
# MAGIC ## feito todas as verificações!
# MAGIC
# MAGIC
# MAGIC #Os dados estão prontos para análise!

# COMMAND ----------

# DBTITLE 1,Solucao do problema
# MAGIC %md
# MAGIC ---
# MAGIC # Solução do Problema
# MAGIC
# MAGIC Próximo passo: responder as 5 perguntas de negócio com análises e visualizações.

# COMMAND ----------

# DBTITLE 1,Pergunta 1: Maiores gastos por orgao
# MAGIC %sql --name top_orgaos
# MAGIC -- Pergunta 1: Quais órgãos tiveram os maiores gastos em 2024-2025?
# MAGIC SELECT 
# MAGIC     ORGAO_DESCRICAO,
# MAGIC     Poder_Orgao,
# MAGIC     ROUND(pagamentos_totais / 1000000000, 2) as pagamentos_bilhoes
# MAGIC FROM MVP_gastos_publicos.gold.gastos_por_orgao_ano
# MAGIC ORDER BY pagamentos_totais DESC
# MAGIC LIMIT 10;

# COMMAND ----------

# DBTITLE 1,Grafico: Top 10 orgaos
import matplotlib.pyplot as plt
import pandas as pd

# Converter resultado SQL para pandas
df_top_orgaos = top_orgaos.toPandas()

# Criar um gráfico de barras para melhor visualizar

plt.figure(figsize=(12, 6))
plt.barh(df_top_orgaos['ORGAO_DESCRICAO'], df_top_orgaos['pagamentos_bilhoes'], color='steelblue')
plt.xlabel('Pagamentos Totais (Bilhões R$)', fontsize=12)
plt.ylabel('Órgão', fontsize=12)
plt.title('Top 10 Órgãos com Maiores Gastos (2024-2025)', fontsize=14, fontweight='bold')
plt.gca().invert_yaxis() 
plt.tight_layout()
plt.show()

print("\n Gráfico: Os órgãos com maiores gastos são os relacionados à Previdência Social, Saúde e Educação.")

# COMMAND ----------

# DBTITLE 1,Pergunta 2: Evolucao mensal dos gastos
# MAGIC %sql --name evolucao
# MAGIC -- Pergunta 2: Como os gastos evoluíram mensalmente ao longo do tempo?
# MAGIC SELECT 
# MAGIC     data_referencia,
# MAGIC     ROUND(pagamentos_totais / 1000000000, 2) as pagamentos_bilhoes
# MAGIC FROM evolucao_mensal
# MAGIC ORDER BY data_referencia;

# COMMAND ----------

# DBTITLE 1,Grafico: Evolucao temporal
import matplotlib.pyplot as plt
import pandas as pd

# Converter resultado SQL para pandas
df_evolucao = evolucao.toPandas()
df_evolucao['data_referencia'] = pd.to_datetime(df_evolucao['data_referencia'])

# Agora criar gráfico de linha para visualizar melhor 
plt.figure(figsize=(14, 6))
plt.plot(df_evolucao['data_referencia'], df_evolucao['pagamentos_bilhoes'], 
         marker='o', linewidth=2, markersize=6, color='darkgreen')
plt.xlabel('Mês', fontsize=12)
plt.ylabel('Pagamentos Totais (Bilhões R$)', fontsize=12)
plt.title('Evolução Mensal dos Gastos Públicos Federais (2024-2025)', fontsize=14, fontweight='bold')
plt.grid(True, alpha=0.3)
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

print("\n gráfico: Os gastos apresentam sazonalidade, com picos em determinados meses do ano.")

# COMMAND ----------

# DBTITLE 1,Pergunta 3: Gastos por funcao de governo
# MAGIC %sql 
# MAGIC -- Pergunta 3: Quais funções de governo (saúde, educação, defesa) recebem mais recursos?
# MAGIC SELECT 
# MAGIC     funcao,
# MAGIC     ROUND(SUM(pagamentos_totais) / 1000000000, 2) as pagamentos_bilhoes
# MAGIC FROM gastos_por_funcao
# MAGIC GROUP BY funcao
# MAGIC ORDER BY pagamentos_bilhoes DESC
# MAGIC LIMIT 10;

# COMMAND ----------

# DBTITLE 1,Grafico: Top funcoes
import matplotlib.pyplot as plt
import pandas as pd

# convertendo 
df_funcoes = top_funcoes.toPandas()

# Criar gráfico de pizza
plt.figure(figsize=(10, 8))
colors = plt.cm.Set3(range(len(df_funcoes)))
plt.pie(df_funcoes['pagamentos_bilhoes'], labels=df_funcoes['funcao'], autopct='%1.1f%%',
        startangle=90, colors=colors, textprops={'fontsize': 10})
plt.title('Distribuição de Gastos por Função de Governo (Top 10)', fontsize=14, fontweight='bold')
plt.axis('equal')
plt.tight_layout()
plt.show()

print("\n Gráfico: Previdência Social, Saúde e Educação concentram a maior parte do orçamento federal.")

# COMMAND ----------

# DBTITLE 1,Pergunta 4: Orcamento vs Executado
# MAGIC %sql --name orcado_vs_executado
# MAGIC -- Pergunta 4: Qual a diferença entre o orçamento previsto (dotação) e o executado (pago)?
# MAGIC SELECT 
# MAGIC     ID_ANO,
# MAGIC     ROUND(SUM(DOTACAO_ATUALIZADA) / 1000000000, 2) as orcado_bilhoes,
# MAGIC     ROUND(SUM(PAGAMENTOS_TOTAIS) / 1000000000, 2) as executado_bilhoes,
# MAGIC     ROUND((SUM(PAGAMENTOS_TOTAIS) / SUM(DOTACAO_ATUALIZADA)) * 100, 2) as percentual_executado
# MAGIC FROM gastos_publicos
# MAGIC WHERE DOTACAO_ATUALIZADA IS NOT NULL AND PAGAMENTOS_TOTAIS IS NOT NULL
# MAGIC GROUP BY ID_ANO
# MAGIC ORDER BY ID_ANO;

# COMMAND ----------

# DBTITLE 1,Grafico: Orcado vs Executado
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# convertendo 
df_orcamento = orcado_vs_executado.toPandas()

# Criar gráfico de barras agrupadas
x = np.arange(len(df_orcamento))
width = 0.35

fig, ax = plt.subplots(figsize=(10, 6))
rects1 = ax.bar(x - width/2, df_orcamento['orcado_bilhoes'], width, label='Orçado', color='lightblue')
rects2 = ax.bar(x + width/2, df_orcamento['executado_bilhoes'], width, label='Executado', color='darkblue')

ax.set_xlabel('Ano', fontsize=12)
ax.set_ylabel('Valores (Bilhões R$)', fontsize=12)
ax.set_title('Orçamento Previsto vs Executado por Ano', fontsize=14, fontweight='bold')
ax.set_xticks(x)
ax.set_xticklabels(df_orcamento['ID_ANO'])
ax.legend()
ax.grid(True, alpha=0.3, axis='y')

plt.tight_layout()
plt.show()

print(f"\n Gráfico: Em média, {df_orcamento['percentual_executado'].mean():.1f}% do orçamento previsto foi executado.")

# COMMAND ----------

# DBTITLE 1,Pergunta 5: Top programas
# MAGIC %sql --name top_programas
# MAGIC -- Pergunta 5: Quais os top 10 programas que mais receberam recursos?
# MAGIC SELECT 
# MAGIC     NO_PROGRAMA_PT as programa,
# MAGIC     ROUND(SUM(PAGAMENTOS_TOTAIS) / 1000000, 2) as pagamentos_milhoes
# MAGIC FROM gastos_publicos
# MAGIC WHERE NO_PROGRAMA_PT IS NOT NULL AND PAGAMENTOS_TOTAIS IS NOT NULL
# MAGIC GROUP BY NO_PROGRAMA_PT
# MAGIC ORDER BY pagamentos_milhoes DESC
# MAGIC LIMIT 10;

# COMMAND ----------

# DBTITLE 1,Grafico: Top programas
import matplotlib.pyplot as plt
import pandas as pd

# Convertendo 
df_programas = top_programas.toPandas()

# Criar gráfico de barras horizontais
plt.figure(figsize=(12, 8))
plt.barh(df_programas['programa'], df_programas['pagamentos_milhoes'], color='coral')
plt.xlabel('Pagamentos Totais (Milhões R$)', fontsize=12)
plt.ylabel('Programa', fontsize=12)
plt.title('Top 10 Programas com Maiores Gastos (2024-2025)', fontsize=14, fontweight='bold')
plt.gca().invert_yaxis() 
plt.tight_layout()
plt.show()

print("\n Gráfico: Programas de Previdência, Saúde e Transferência de Renda concentram os maiores volumes de recursos.")

# COMMAND ----------

# DBTITLE 1,Conclusoes finais
# MAGIC %md
# MAGIC ---
# MAGIC ## Conclusões Finais
# MAGIC
# MAGIC Após as análises realizadas, podemos concluir:
# MAGIC
# MAGIC  **Concentração de gastos**: Poucos órgãos concentram a maior parte do orçamento federal (Previdência, Saúde, Educação).  
# MAGIC  **Sazonalidade**: Os gastos apresentam variações mensais, com picos em determinados períodos.   
# MAGIC  **Execução orçamentária**: Nem todo o orçamento previsto é executado, indicando oportunidades de otimização.  
# MAGIC  **Áreas prioritárias**: Previdência Social, Saúde e Educação são as funções que mais recebem recursos.
# MAGIC
# MAGIC