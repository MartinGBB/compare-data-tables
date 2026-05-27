from environment_data import EnvironmentData
from compare_tables import CompareTables
from generate_report import GenerateReport

CSV_PATH = r'..\data_csv'

class Main:
  def __init__(self, csv_prod: str, csv_acp: str):
    self.environment_prod = EnvironmentData('PROD', CSV_PATH, csv_prod)
    self.environment_acp = EnvironmentData('ACP', CSV_PATH, csv_acp)
    self.csv_prod = csv_prod
    self.csv_acp = csv_acp

  def load_data(self):
    data_prod = self.environment_prod.load_data()
    data_acp = self.environment_acp.load_data()
    return data_prod, data_acp

  def compare_data(self):
    compare_tables = CompareTables(self.environment_prod.load_data(), self.environment_acp.load_data(), 'ID')
    exclusives_prod = compare_tables.exclusives_prod()
    exclusives_acp = compare_tables.exclusives_acp()
    return exclusives_prod, exclusives_acp

  def compare_data_len(self):
    compare_tables = CompareTables(self.environment_prod.load_data(), self.environment_acp.load_data(), 'ID')
    exclusives_prod = compare_tables.exclusives_prod_len()
    exclusives_acp = compare_tables.exclusives_acp_len()
    return exclusives_prod, exclusives_acp
  
  def generate_excel(self, exclusives_prod, exclusives_acp):
    prefixFileName = '_'.join(self.csv_prod.split('_')[:-1])
    print(f"Prefixo do nome do arquivo: {prefixFileName}")
    GenerateReport(exclusives_prod, exclusives_acp, prefixFileName).generate_excel()