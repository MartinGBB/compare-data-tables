import sys

from environment_data import EnvironmentData
from compare_tables import CompareTables
from generate_report import GenerateReport

GENERATE_REPORT = True

FILE_CSV_PROD = 'AT_PREPARE_STEP_PROD' 
FILE_CSV_ACP = 'AT_PREPARE_STEP_ACP'
CSV_PATH = r'..\data_csv'

SELECTED_COLUMNS_TO_COMPARE_DIFFERENCES = ['Name', 'ValidFrom', 'ValidTo']

NOME_TABELA_BANCO = 'AT_PREPARE_STEP' 
# Escolha a direção: 'PROD_PARA_ACP' (Pega o valor de Prod e joga no ACP) ou 'ACP_PARA_PROD'
DIRECAO_CORRECAO = 'PROD_PARA_ACP'

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

if GENERATE_REPORT:
  print("Gerando Relatorio...")
  table_name = '_'.join(FILE_CSV_PROD.split('_')[:-1])
  # relatorio = GenerateReport(exclusive_prod, exclusive_acp, divergences, prefix_file_name, selected_columns=SELECTED_COLUMNS_TO_COMPARE_DIFFERENCES)
  relatorio = GenerateReport(
    exclusive_prod, exclusive_acp, divergences, table_name, 
    SELECTED_COLUMNS_TO_COMPARE_DIFFERENCES,
    DIRECAO_CORRECAO
)
  relatorio.generate_excel()

print("Análise concluída com sucesso!")