from environment_data import EnvironmentData
from compare_tables import CompareTables

CSV_PATH = r'..\data_csv'

class Main:
  def __init__(self, csv_prod: str, csv_acp: str):
    self.environment_prod = EnvironmentData('PROD', CSV_PATH, csv_prod)
    self.environment_acp = EnvironmentData('ACP', CSV_PATH, csv_acp)

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