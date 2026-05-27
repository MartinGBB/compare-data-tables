import pandas as pd
from typing import Literal

class Environment:
  def __init__(self, environment_type: Literal['PROD', 'ACP'], path: str, file_csv: str):
    
    if environment_type not in ('PROD', 'ACP'):
      raise ValueError("environment must be 'PROD' or 'ACP'")
    
    self.environment_type = environment_type
    self.path = path
    self.file_csv = file_csv

  def load_data(self):
    data = pd.read_csv(rf'{self.path}\{self.file_csv}.csv') 
    return data