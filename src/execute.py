import sys
import json

from environment_data import EnvironmentData
from compare_tables import CompareTables
from generate_report import GenerateReport
from sqlScriptGenerator import SqlScriptGenerator

# GENERATE_REPORT = True

# FILE_CSV_PROD = 'AT_PREPARE_STEP_PROD' 
# FILE_CSV_ACP = 'AT_PREPARE_STEP_ACP'
# CSV_PATH = r'..\data_csv'

# SELECTED_COLUMNS_TO_COMPARE_DIFFERENCES = ['Name', 'ValidFrom', 'ValidTo']
# SELECTED_COLUMNS_INSERT = ['Facility', 'StepCode', 'Name', 'CreatedBy',]

# IGNORE_COLUMNS_INSERT = [
#   'Facility',	'StepCode',	'Name',
# ]

# PATTERN_VALUES_INSERT = {
#   'CreatedBy': 'System',
# } 

print("Carregando configurações...")
try:
  with open('config.json', 'r', encoding='utf-8') as file:
    config = json.load(file)
except FileNotFoundError:
  print("\n❌ ERRO: Arquivo 'config.json' não encontrado na pasta!")
  sys.exit(1)

# variaveis do json
GENERATE_REPORT = config.get("GENERATE_REPORT", True)
FILE_CSV_PROD = config.get("FILE_CSV_PROD")
FILE_CSV_ACP = config.get("FILE_CSV_ACP")
CSV_PATH = config.get("CSV_PATH")

SELECTED_COLUMNS_TO_COMPARE_DIFFERENCES = config.get("SELECTED_COLUMNS_TO_COMPARE_DIFFERENCES", [])
SELECTED_COLUMNS_INSERT = config.get("SELECTED_COLUMNS_INSERT", [])
IGNORE_COLUMNS_INSERT = config.get("IGNORE_COLUMNS_INSERT", [])
PATTERN_VALUES_INSERT = config.get("PATTERN_VALUES_INSERT", {})

# (Para o SQL Generator, presumimos que a tabela leva o nome do arquivo sem o último bloco)
NOME_TABELA_BANCO = '_'.join(FILE_CSV_PROD.split('_')[:-1])

print("Carregando arquivos...")
try:
  data_prod = EnvironmentData('PROD', CSV_PATH, FILE_CSV_PROD).load_data()
  data_acp = EnvironmentData('ACP', CSV_PATH, FILE_CSV_ACP).load_data()
except FileNotFoundError as erro:
  print("\nErro: Arquivo CSV não encontrado!")
  sys.exit(1)

print("Cruzando dados...")
auditor = CompareTables(data_prod, data_acp, key_column='ID')
exclusive_prod = auditor.get_exclusives_prod()
exclusive_acp = auditor.get_exclusives_acp()
divergences = auditor.get_both_differences(selected_columns=SELECTED_COLUMNS_TO_COMPARE_DIFFERENCES)

print(f"- Qty exclusivo em Prod: {len(exclusive_prod)}")
print(f"- Qty exclusivo em ACP: {len(exclusive_acp)}")
print(f"- Qty com divergências: {len(divergences)}")

# Instancia o gerador de SQL
sql_generator = SqlScriptGenerator(
  table_name='_'.join(FILE_CSV_PROD.split('_')[:-1]),
  selected_columns_update=SELECTED_COLUMNS_TO_COMPARE_DIFFERENCES,
  ignore_columns_insert=IGNORE_COLUMNS_INSERT,
  pattern_values_insert=PATTERN_VALUES_INSERT,
  selected_columns_insert=SELECTED_COLUMNS_INSERT
)

#  Modifica as tabelas adicionando os scripts
divergences = sql_generator.generate_update_scripts(divergences)
exclusive_prod = sql_generator.generate_insert_scripts(exclusive_prod, '_PROD')
exclusive_acp = sql_generator.generate_insert_scripts(exclusive_acp, '_ACP')


# Passa as tabelas já prontas para o Relatório
if GENERATE_REPORT:
  print("Gerando Relatorio...")
  prefix_file_name = '_'.join(FILE_CSV_PROD.split('_')[:-1])
  # relatorio = GenerateReport(exclusive_prod, exclusive_acp, divergences, prefix_file_name, selected_columns=SELECTED_COLUMNS_TO_COMPARE_DIFFERENCES)
relatorio = GenerateReport(
  exclusives_prod=exclusive_prod, 
  exclusives_acp=exclusive_acp, 
  divergences=divergences, 
  file_prefix=prefix_file_name, 
  selected_columns_update=SELECTED_COLUMNS_TO_COMPARE_DIFFERENCES
)
relatorio.generate_excel()

print("Análise concluída com sucesso!")