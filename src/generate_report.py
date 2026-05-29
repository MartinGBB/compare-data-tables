import pandas as pd 

class GenerateReport:
  def __init__(self, exclusives_prod: pd.DataFrame, exclusives_acp: pd.DataFrame, divergences: pd.DataFrame, file_prefix: str, selected_columns_update=None):
    self.exclusives_prod = exclusives_prod
    self.exclusives_acp = exclusives_acp
    self.divergences = divergences
    self.selected_columns_update = selected_columns_update
    self.file_name = f'exclusives_{file_prefix}.xlsx'

  def _highlight_differences(self, row):
    styles = pd.Series('', index=row.index)
      
    for name_column in row.index:
      if str(name_column).endswith('_ACP'):
        base_name = str(name_column).replace('_ACP', '')
        prod_column = str(name_column).replace('_ACP', '_PROD')
        
        if self.selected_columns_update and (base_name not in self.selected_columns_update):
          continue
        
        val_acp = row.get(name_column)
        val_prod = row.get(prod_column)
        
        if pd.isna(val_acp) and pd.isna(val_prod):
          continue
            
        if val_acp != val_prod:
          styles[name_column] = 'background-color: #FFFF00'
            
    return styles

  def generate_excel(self):
    with pd.ExcelWriter(self.file_name, engine='openpyxl') as writer:
      self.exclusives_prod.to_excel(writer, sheet_name='Falta em ACP', index=False)
      self.exclusives_acp.to_excel(writer, sheet_name='Falta em Prod', index=False)
      
      if not self.divergences.empty:
        df_colorful = self.divergences.style.apply(self._highlight_differences, axis=1)
        df_colorful.to_excel(writer, sheet_name='Divergências', index=False)
