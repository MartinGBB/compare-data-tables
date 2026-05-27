from Environment import Environment

CSV_PATH = r'..\data_csv'

class Main:
  def __init__(self, csv_prod: str, csv_acp: str):
    self.environment_prod = Environment('PROD', CSV_PATH, csv_prod)
    self.environment_acp = Environment('ACP', CSV_PATH, csv_acp)

  def load_data(self):
    data_prod = self.environment_prod.load_data()
    data_acp = self.environment_acp.load_data()
    return data_prod, data_acp


  def compare_data(self):
    return "Comparação concluída"