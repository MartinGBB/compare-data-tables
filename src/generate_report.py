import pandas as pd 

class GenerateReport:
  def __init__(self, exclusives_prod: pd.DataFrame, exclusives_acp: pd.DataFrame, divergencias: pd.DataFrame, prefixFileName: str, selected_column=None):
    self.exclusives_prod = exclusives_prod
    self.exclusives_acp = exclusives_acp
    self.divergencias = divergencias
    self.selected_column = selected_column
    self.file_name = f'exclusives_{prefixFileName}.xlsx'

  def _highlight_differences(self, row):
    styles = pd.Series('', index=row.index)
    
    for name_column in row.index:
      if str(name_column).endswith('_ACP'):
        base_name = str(name_column).replace('_ACP', '')
        coluna_prod = str(name_column).replace('_ACP', '_PROD')
        
        if self.selected_column and (base_name not in self.selected_column):
          continue
        
        # Busca os valores
        val_acp = row[name_column]
        val_prod = row[coluna_prod]
        
        # Ignora se ambos forem nulos/vazios
        if pd.isna(val_acp) and pd.isna(val_prod):
          continue
            
        # Se forem diferentes, coloreia a célula
        if val_acp != val_prod:
          styles[name_column] = 'background-color: #FFFF00'
                
    return styles

  def generate_excel(self):
    with pd.ExcelWriter(self.file_name, engine='openpyxl') as writer:
      self.exclusives_prod.to_excel(writer, sheet_name='Falta em ACP', index=False)
      self.exclusives_acp.to_excel(writer, sheet_name='Falta em Prod', index=False)
      
      if not self.divergencias.empty:
        df_colorfull = self.divergencias.style.apply(self._highlight_differences, axis=1)
        df_colorfull.to_excel(writer, sheet_name='Divergências', index=False)
