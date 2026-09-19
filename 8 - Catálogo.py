# Databricks notebook source
# DBTITLE 1,Dicionário de Dados - Principais Colunas
# MAGIC %md
# MAGIC ## Dicionário de Dados
# MAGIC
# MAGIC Abaixo estão as **principais colunas** do dataset de gastos públicos federais, com seus tipos e descrições:
# MAGIC
# MAGIC | Coluna | Type | Comment |
# MAGIC |--------|------|--------|
# MAGIC | ID_ANO | INTEGER | Ano de referência da despesa (2024 ou 2025) |
# MAGIC | ID_MES | INTEGER | Mês de referência (1 a 12) |
# MAGIC | data_referencia | DATE | Data criada no formato YYYY-MM-01 para análises temporais |
# MAGIC | ORGAO_CODIGO | INTEGER | Código numérico do órgão federal |
# MAGIC | ORGAO_DESCRICAO | STRING | Nome completo do órgão (ex: MINISTERIO DA FAZENDA) |
# MAGIC | ORGAO_CNPJ | STRING | CNPJ do órgão federal |
# MAGIC | Poder_Orgao | STRING | Poder ao qual o órgão pertence (EXE, LEG, JUD) |
# MAGIC | UNIDADE_GESTORA_CODIGO | INTEGER | Código da unidade gestora responsável |
# MAGIC | UNIDADE_GESTORA_DESCRICAO | STRING | Nome da unidade gestora |
# MAGIC | FUNCAO | STRING | Função de governo (ex: SAUDE, EDUCACAO, PREVIDENCIA SOCIAL) |
# MAGIC | SUBFUNCAO | STRING | Subfunção detalhada da despesa |
# MAGIC | PROGRAMA_PT | STRING | Código do programa de trabalho |
# MAGIC | NO_PROGRAMA_PT | STRING | Nome do programa (ex: BOLSA FAMILIA, OPERACOES ESPECIAIS) |
# MAGIC | ACAO_PT | STRING | Código da ação programática |
# MAGIC | NO_ACAO_PT | STRING | Nome da ação orçamentária |
# MAGIC | DOTACAO_INICIAL | DECIMAL(18,2) | Valor inicial previsto no orçamento (em Reais) |
# MAGIC | DOTACAO_ATUALIZADA | DECIMAL(18,2) | Valor atualizado após remanejamentos (em Reais) |
# MAGIC | DESPESAS_EMPENHADAS | DECIMAL(18,2) | Total de despesas empenhadas no período (em Reais) |
# MAGIC | DESPESAS_LIQUIDADAS | DECIMAL(18,2) | Total de despesas liquidadas no período (em Reais) |
# MAGIC | DESPESAS_PAGAS | DECIMAL(18,2) | Total de despesas pagas no período (em Reais) |
# MAGIC | PAGAMENTOS_TOTAIS | DECIMAL(18,2) | **Coluna principal:** soma de todos os pagamentos executados (em Reais) |
# MAGIC
# MAGIC **Total de colunas:** 39 (incluindo metadados adicionais de classificação orçamentária)
# MAGIC
# MAGIC **Notas:**
# MAGIC - Valores financeiros estão em Reais (BRL)
# MAGIC - Valores negativos são legítimos (representam anulações ou devoluções)
# MAGIC - Coluna `PAGAMENTOS_TOTAIS` é a métrica principal para análises de execução

# COMMAND ----------

# DBTITLE 1,Linhagem de Dados (Data Lineage)
# MAGIC %md
# MAGIC ## Linhagem de Dados
# MAGIC
# MAGIC Este projeto segue a **arquitetura Medallion**, organizando os dados em camadas progressivas de qualidade e agregação.
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ### 1. Fontes (Staging)
# MAGIC
# MAGIC **Nome dos arquivos:** 
# MAGIC - `gastos2024.csv` (150.423 registros)
# MAGIC - `gastos2025.csv` (147.075 registros)
# MAGIC
# MAGIC **Origem:** Portal da Transparência - Governo Federal  
# MAGIC **URL:** https://portaldatransparencia.gov.br/download-de-dados/despesas-execucao
# MAGIC
# MAGIC **Formato técnico:**
# MAGIC - Separador: `;` (ponto e vírgula)
# MAGIC - Encoding: ISO-8859-1 (Latin-1)
# MAGIC - Header: Sim (primeira linha)
# MAGIC - Valores financeiros: formato brasileiro com vírgula decimal
# MAGIC
# MAGIC **Volume criado:** `MVP_gastos_publicos.staging.dados_gastos_publicos` (Unity Catalog Volume)
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ### 2. Schema Bronze
# MAGIC
# MAGIC **Tabela:** `MVP_gastos_publicos.bronze.gastos_publicos`
# MAGIC
# MAGIC **Transformações aplicadas:**
# MAGIC - Leitura dos 2 arquivos CSV com encoding ISO-8859-1
# MAGIC - União (UNION) dos datasets 2024 + 2025
# MAGIC - Todas as colunas mantidas como **STRING** (dados brutos)
# MAGIC - Preservação de valores originais (sem limpeza)
# MAGIC
# MAGIC **Registros:** 297.498
# MAGIC
# MAGIC **Objetivo:** Camada de dados brutos, imutável, para auditoria e reprocessamento
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ### 3. Schema Silver
# MAGIC
# MAGIC **Tabela:** `MVP_gastos_publicos.silver.gastos_publicos`
# MAGIC
# MAGIC **Transformações aplicadas:**
# MAGIC - **Conversão de tipos:** 
# MAGIC   - 8 colunas financeiras: STRING → DECIMAL(18,2)
# MAGIC   - 10 colunas de códigos: STRING → INTEGER
# MAGIC   - Criação de `data_referencia`: DATE (formato YYYY-MM-01)
# MAGIC - **Limpeza de dados:** 
# MAGIC   - Remoção de valores malformados ('N/A', '00QD', strings inválidas)
# MAGIC   - Conversão de formato brasileiro (vírgula → ponto decimal)
# MAGIC   - Substituição de valores inválidos por NULL
# MAGIC - **Remoção de duplicados:** Eliminados 27.000 registros duplicados
# MAGIC
# MAGIC **Registros:** 270.498 (após limpeza)
# MAGIC
# MAGIC **Objetivo:** Camada de dados limpos e validados, pronta para análise
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ### 4. Armazenamento Gold
# MAGIC
# MAGIC **Tabelas criadas:**
# MAGIC
# MAGIC #### 4.1 `gastos_publicos` (tabela base)
# MAGIC - Dados da camada Silver filtrados e otimizados
# MAGIC - Registros: 270.498
# MAGIC
# MAGIC #### 4.2 `gastos_por_orgao_ano` (agregação por órgão)
# MAGIC ```sql
# MAGIC GROUP BY ORGAO_DESCRICAO, Poder_Orgao, ID_ANO
# MAGIC SUM(PAGAMENTOS_TOTAIS)
# MAGIC ```
# MAGIC - Registros: ~1.200 (órgãos × anos)
# MAGIC
# MAGIC #### 4.3 `gastos_por_funcao` (agregação por função de governo)
# MAGIC ```sql
# MAGIC GROUP BY FUNCAO, ID_ANO
# MAGIC SUM(PAGAMENTOS_TOTAIS)
# MAGIC ```
# MAGIC - Registros: ~60 (funções × anos)
# MAGIC
# MAGIC #### 4.4 `evolucao_mensal` (série temporal)
# MAGIC ```sql
# MAGIC GROUP BY ID_ANO, ID_MES, data_referencia
# MAGIC SUM(PAGAMENTOS_TOTAIS)
# MAGIC ```
# MAGIC - Registros: 24 (12 meses × 2 anos)
# MAGIC
# MAGIC **Objetivo:** Tabelas agregadas otimizadas para responder as 5 perguntas de negócio com performance

# COMMAND ----------

# DBTITLE 1,Visualizar schemas criados
# MAGIC %sql
# MAGIC -- Listar todos os schemas do catálogo
# MAGIC SHOW SCHEMAS IN MVP_gastos_publicos;

# COMMAND ----------

# DBTITLE 1,Visualizar tabelas da camada Bronze
# MAGIC %sql
# MAGIC -- Tabelas na camada Bronze
# MAGIC USE CATALOG MVP_gastos_publicos;
# MAGIC SHOW TABLES IN bronze;

# COMMAND ----------

# DBTITLE 1,Visualizar tabelas da camada Silver
# MAGIC %sql
# MAGIC -- Tabelas na camada Silver
# MAGIC SHOW TABLES IN silver;

# COMMAND ----------

# DBTITLE 1,Visualizar tabelas da camada Gold
# MAGIC %sql
# MAGIC -- Tabelas na camada Gold
# MAGIC SHOW TABLES IN gold;

# COMMAND ----------

# DBTITLE 1,Estrutura detalhada da tabela Silver
# MAGIC %sql
# MAGIC -- Descrever estrutura completa da tabela principal (Silver)
# MAGIC DESCRIBE TABLE EXTENDED silver.gastos_publicos;

# COMMAND ----------

# DBTITLE 1,Exemplo de dados - Silver
# MAGIC %sql
# MAGIC -- Visualizar amostra de dados da camada Silver
# MAGIC SELECT 
# MAGIC     ID_ANO,
# MAGIC     ID_MES,
# MAGIC     data_referencia,
# MAGIC     ORGAO_DESCRICAO,
# MAGIC     Poder_Orgao,
# MAGIC     FUNCAO,
# MAGIC     NO_PROGRAMA_PT,
# MAGIC     ROUND(PAGAMENTOS_TOTAIS, 2) as PAGAMENTOS_TOTAIS
# MAGIC FROM silver.gastos_publicos
# MAGIC WHERE PAGAMENTOS_TOTAIS IS NOT NULL
# MAGIC ORDER BY PAGAMENTOS_TOTAIS DESC
# MAGIC LIMIT 10;

# COMMAND ----------

# DBTITLE 1,Resumo Final
# MAGIC %md
# MAGIC ## Resumo da Arquitetura
# MAGIC
# MAGIC ### Pipeline Medallion Implementado
# MAGIC
# MAGIC ```
# MAGIC 📁 STAGING (Unity Catalog Volume)
# MAGIC    ↓
# MAGIC 🥉 BRONZE (Dados Brutos)
# MAGIC    ├─ gastos_publicos (297k registros, 39 colunas STRING)
# MAGIC    ↓
# MAGIC 🥈 SILVER (Dados Limpos)
# MAGIC    ├─ gastos_publicos (270k registros, tipos validados)
# MAGIC    ↓
# MAGIC 🥇 GOLD (Dados Agregados)
# MAGIC    ├─ gastos_publicos (base filtrada)
# MAGIC    ├─ gastos_por_orgao_ano (por órgão + ano)
# MAGIC    ├─ gastos_por_funcao (por função)
# MAGIC    └─ evolucao_mensal (série temporal)
# MAGIC ```
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ### Métricas do Projeto
# MAGIC
# MAGIC | Métrica | Valor |
# MAGIC |---------|-------|
# MAGIC | **Registros brutos** | 297.498 |
# MAGIC | **Registros após limpeza** | 270.498 |
# MAGIC | **Colunas totais** | 39 |
# MAGIC | **Período coberto** | 24 meses (2024-2025) |
# MAGIC | **Órgãos analisados** | ~600 órgãos federais |
# MAGIC | **Funções de governo** | 28 funções principais |
# MAGIC | **Volume total de gastos** | R$ 9,88 trilhões |
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ### Qualidade dos Dados
# MAGIC
# MAGIC ✅ **Validações aplicadas:**
# MAGIC - Verificação de valores nulos em colunas críticas
# MAGIC - Detecção e tratamento de valores negativos legítimos
# MAGIC - Identificação de duplicados (4.402 registros = 1,6%)
# MAGIC - Completude temporal confirmada (24 meses sem gaps)
# MAGIC - Valores extremos documentados e validados
# MAGIC
# MAGIC ✅ **Governança:**
# MAGIC - Catálogo Unity Catalog com controle de acesso
# MAGIC - Schemas separados por camada de qualidade
# MAGIC - Tabelas Delta Lake com histórico de versões
# MAGIC - Documentação completa em notebooks
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ### Próximos Passos
# MAGIC
# MAGIC Este catálogo serve como base para:
# MAGIC 1. ✅ Análise das 5 perguntas de negócio (notebook **7 - Analise**)
# MAGIC 2. 🔄 Atualizações incrementais com novos períodos
# MAGIC 3. 📊 Dashboards executivos de acompanhamento
# MAGIC 4. 🤖 Modelos preditivos de execução orçamentária
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC   
# MAGIC **Responsável:** Christopher Silva  
# MAGIC **Projeto:** MVP PUC-RJ - Análise de Gastos Públicos Federais