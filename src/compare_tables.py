import pandas as pd

class CompareTables:
  def __init__(self, data_prod, data_acp, key_column):
    self.data_prod = data_prod
    self.data_acp = data_acp
    self.key_column = key_column

    self.df_left = pd.merge(self.data_prod, self.data_acp, on=self.key_column, how='left', suffixes=('_PROD', '_ACP'), indicator=True)
    self.df_right = pd.merge(self.data_prod, self.data_acp, on=self.key_column, how='right', suffixes=('_PROD', '_ACP'), indicator=True)
    self.df_both = pd.merge(self.data_prod, self.data_acp, on=self.key_column, how='both', suffixes=('_PROD', '_ACP'), indicator=True)

  def get_both_differences(self):
    df_both = self.df_left[self.df_left['_merge'] == 'both'].copy()
    
    base_columns = [col.replace('_PROD', '') for col in df_both.columns if col.endswith('_PROD')]
    has_changes = False
    for col in base_columns:
      # Compara se a coluna PROD é diferente da coluna ACP correspondente
      diverge = df_both[f'{col}_PROD'] != df_both[f'{col}_ACP']
      has_changes = has_changes | diverge
    
    df_divergencias = df_both[has_changes].copy() # copia apenas as linhas que tem divergências
    df_divergencias.drop(columns=['_merge'], inplace=True)
    
    return df_divergencias

  def get_exclusives_prod(self):
    # Filtro apenas os exclusivos
    df = self.df_left[self.df_left['_merge'] == 'left_only'].copy()
    df['Status_Comparacao'] = 'Exclusivo em Prod (Faltando em ACP)'
    df.drop(columns=['_merge'], inplace=True)
    return df

  def get_exclusives_acp(self):
    # Filtro apenas os exclusivos
    df = self.df_right[self.df_right['_merge'] == 'right_only'].copy()
    df['Status_Comparacao'] = 'Exclusivo em ACP (Faltando em Prod)'
    df.drop(columns=['_merge'], inplace=True)

    # Limpeza de colunas do Prod que ficam na aba de ACP
    requiered_columns = [self.key_column, 'Status_Comparacao'] + [col for col in df.columns if col.endswith('_ACP')]
    return df[requiered_columns].copy()
