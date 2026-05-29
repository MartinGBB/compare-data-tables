import pandas as pd 

class GenerateReport:
  def __init__(self, exclusives_prod: pd.DataFrame, exclusives_acp: pd.DataFrame, divergences: pd.DataFrame, table_name: str, selected_column=None, direcao='PROD_TO_ACP'):
    self.exclusives_prod = exclusives_prod
    self.exclusives_acp = exclusives_acp
    self.divergences = divergences
    self.table_name = table_name
    self.selected_column = selected_column
    self.direcao = direcao
    self.file_name = f'exclusives_{table_name}.xlsx'

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

  def _gerar_coluna_sql(self):
    if self.divergences.empty:
      return

    update_script_list = []
    
    if self.selected_column:
      rows = self.selected_column
    else:
      rows = [str(c).replace('_PROD', '') for c in self.divergences.columns if str(c).endswith('_PROD')]

    for index, row_divergence in self.divergences.iterrows():
      sets_sql = []
      
      for row in rows:
        val_prod = row_divergence.get(f'{row}_PROD')
        val_acp = row_divergence.get(f'{row}_ACP')

        if val_prod != val_acp and not (pd.isna(val_prod) and pd.isna(val_acp)):
          # Fonte da verdade baseado na direção selecionada
          new_value = val_prod if self.direcao == 'PROD_TO_ACP' else val_acp

          if pd.isna(new_value):
            value_sql = "NULL"
          else:
            # Evita números inteiros fiquem com '.0' no final quando convertidos para string
            if isinstance(new_value, float) and new_value.is_integer():
              new_value = int(new_value)

            formatted_value = str(new_value).replace("'", "''")
            value_sql = f"'{formatted_value}'"

          sets_sql.append(f"{row} = {value_sql}")

        # build query final
        if sets_sql:
          id_row = row_divergence['ID']
          query = f"UPDATE {self.table_name} SET {', '.join(sets_sql)} WHERE ID = '{id_row}';"
          update_script_list.append(query)
        else:
          update_script_list.append("")

    # Adiciona a lista final como uma nova linha na tabela
    self.divergences['Script_Update'] = update_script_list

  def generate_excel(self):
    self._gerar_coluna_sql() # Gera a coluna de SQL para divergências
    
    with pd.ExcelWriter(self.file_name, engine='openpyxl') as writer:
      self.exclusives_prod.to_excel(writer, sheet_name='Falta em ACP', index=False)
      self.exclusives_acp.to_excel(writer, sheet_name='Falta em Prod', index=False)
      
      if not self.divergences.empty:
        df_colorfull = self.divergences.style.apply(self._highlight_differences, axis=1)
        df_colorfull.to_excel(writer, sheet_name='Divergências', index=False)
