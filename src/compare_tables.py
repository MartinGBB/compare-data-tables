import pandas as pd

class CompareTables:
  def __init__(self, data_prod, data_acp, key_column):
    self.data_prod = data_prod
    self.data_acp = data_acp
    self.key_column = key_column

  def _execute_merge(self, join_direction):
    merge = pd.merge(self.data_prod, self.data_acp, on=self.key_column, how=join_direction, suffixes=('_PROD', '_ACP'), indicator=True)
    return merge

  def exclusives_prod(self):
    return self._execute_merge(join_direction='left')
  
  def exclusives_acp(self):
    return self._execute_merge(join_direction='right')
  
  def exclusives_prod_len(self):
    return len(self.exclusives_prod()[self.exclusives_prod()['_merge'] == 'left_only'])
  
  def exclusives_acp_len(self):
    return len(self.exclusives_acp()[self.exclusives_acp()['_merge'] == 'right_only'])
