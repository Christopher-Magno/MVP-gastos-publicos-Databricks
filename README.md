# Análise de Gastos Públicos Federais

Trabalho do MVP da Pós-Graduação em Engenharia de Dados da PUC-RJ.

## O que é esse projeto

Esse projeto analisa os gastos do governo federal brasileiro nos anos de 2024 e 2025. Os dados foram baixados do Portal da Transparência e processados no Databricks.

## Arquitetura

O projeto usa a arquitetura Medallion que aprendi no curso:

- **Bronze**: dados brutos dos CSVs
- **Silver**: dados limpos e organizados
- **Gold**: dados agregados para análise

## Notebooks do projeto

1. **Objetivo do projeto** - explica o que o trabalho vai fazer
2. **Preparação ambiente** - cria o catálogo e os schemas
3. **Coleta de dados** - upload dos arquivos CSV
4. **Tabela Bronze** - carrega os dados brutos
5. **Tabela Silver** - limpa e valida os dados
6. **Tabela Gold** - cria as tabelas agregadas
7. **Análise** - responde as 5 perguntas de negócio
8. **Catálogo** - documentação dos dados
9. **Autoavaliação** - reflexão sobre o trabalho

## Perguntas respondidas

1. Quais órgãos tiveram os maiores gastos?
2. Como os gastos evoluíram ao longo do tempo?
3. Quais funções de governo recebem mais recursos?
4. Qual a diferença entre o orçamento previsto e o executado?
5. Quais os programas que mais receberam recursos?

## Principais resultados

- O Ministério da Fazenda concentra mais da metade dos gastos
- Janeiro tem picos de gastos (13º salário)
- Previdência Social é a função com mais recursos
- Em média 65% do orçamento previsto foi executado
- Refinanciamento da dívida é o programa com mais gastos

## Tecnologias usadas

- Databricks
- PySpark
- SQL
- Delta Lake
- Unity Catalog
- Python (matplotlib para gráficos)

## Dados

Os dados vieram do Portal da Transparência do Governo Federal e contém informações sobre despesas públicas federais de 2024 e 2025.

Total de registros processados: 297.498

## Autor

Christopher Silva  
Pós-Graduação em Engenharia de Dados - PUC-RJ  
Setembro 2026
