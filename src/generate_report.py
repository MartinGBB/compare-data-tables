import pandas as pd 

class GenerateReport:
  def __init__(self, exclusives_prod: pd.DataFrame, exclusives_acp: pd.DataFrame, prefixFileName: str):
    self.exclusives_prod = exclusives_prod
    self.exclusives_acp = exclusives_acp
    self.prefixFileName = prefixFileName
    self.file_name = f'exclusives_{prefixFileName}.xlsx'

  def generate_excel(self):
    with pd.ExcelWriter(self.file_name) as writer:
      self.exclusives_prod.to_excel(writer, sheet_name=f'Falta em ACP', index=False)
      self.exclusives_acp.to_excel(writer, sheet_name=f'Falta em Prod', index=False)
