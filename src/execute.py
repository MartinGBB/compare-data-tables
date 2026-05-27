import sys

from environment_data import EnvironmentData
from compare_tables import CompareTables
from generate_report import GenerateReport

GENERATE_REPORT = False

FILE_CSV_PROD = 'AT_PREPARE_STEP_PROD' 
FILE_CSV_ACP = 'AT_PREPARE_STEP_ACP'
CSV_PATH = r'..\data_csv'

print("Carregando arquivos...")
try:
  data_prod = EnvironmentData('PROD', CSV_PATH, FILE_CSV_PROD).load_data()
  data_acp = EnvironmentData('ACP', CSV_PATH, FILE_CSV_ACP).load_data()
except FileNotFoundError as erro:
  print("\nErro: Arquivo CSV não encontrado!")
  sys.exit(1)

print("Cruzando dados...")
auditor = CompareTables(data_prod, data_acp, key_column='ID')
exclusivos_prod = auditor.get_exclusives_prod()
exclusivos_acp = auditor.get_exclusives_acp()

print(f"- Qty exclusivo em Prod: {len(exclusivos_prod)}")
print(f"- Qty exclusivo em ACP: {len(exclusivos_acp)}")

if GENERATE_REPORT:
  print("Gerando Relatorio...")
  prefix_file_name = '_'.join(FILE_CSV_PROD.split('_')[:-1])
  relatorio = GenerateReport(exclusivos_prod, exclusivos_acp, prefix_file_name)
  relatorio.generate_excel()

print("Análise concluída com sucesso!")