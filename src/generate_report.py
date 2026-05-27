import pandas as pd 

class GenerateReport:
  def __init__(self, exclusives_prod: list[dict], exclusives_acp: list[dict], prefixFileName: str):
    self.exclusives_prod = exclusives_prod
    self.exclusives_acp = exclusives_acp
    self.prefixFileName = prefixFileName
    self.file_name = 'exclusives_' + prefixFileName + '.xlsx'

  def generate_excel(self):
    with pd.ExcelWriter(self.file_name) as writer:
      self.exclusives_prod.to_excel(writer, sheet_name=f'Falta em ACP (Exclusivo Prod)', index=False)
      self.exclusives_acp.to_excel(writer, sheet_name=f'Falta em Prod (Exclusivo ACP)', index=False)
