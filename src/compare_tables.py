import pandas as pd

class CompareTables:
  def __init__(self, data_prod, data_acp, key_column):
    self.data_prod = data_prod
    self.data_acp = data_acp
    self.key_column = key_column

    self.df_left = pd.merge(self.data_prod, self.data_acp, on=self.key_column, how='left', suffixes=('_PROD', '_ACP'), indicator=True)
    self.df_right = pd.merge(self.data_prod, self.data_acp, on=self.key_column, how='right', suffixes=('_PROD', '_ACP'), indicator=True)

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
    return df
