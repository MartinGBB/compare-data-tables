import pandas as pd 

class SqlScriptGenerator:
	def __init__(self, table_name: str, selected_columns_update=None, ignore_columns_insert=None, pattern_values_insert=None, selected_columns_insert=None):
		self.table_name = table_name
		self.selected_columns_update = selected_columns_update

		self.ignore_columns_insert = ignore_columns_insert if ignore_columns_insert is not None else []
		self.pattern_values_insert = pattern_values_insert if pattern_values_insert is not None else {}
		self.selected_columns_insert = selected_columns_insert if selected_columns_insert is not None else []

	def generate_update_scripts(self, divergences_df: pd.DataFrame) -> pd.DataFrame:
		if divergences_df.empty:
			return divergences_df

		script_update_prod = []
		script_update_acp = []
		
		if self.selected_columns_update:
			columns = self.selected_columns_update
		else:
			columns = [str(c).replace('_PROD', '') for c in divergences_df.columns if str(c).endswith('_PROD')]

		for index, row in divergences_df.iterrows():
			sets_sql_prod = [] 
			sets_sql_acp = []  
			
			for col in columns:
				val_prod = row.get(f'{col}_PROD')
				val_acp = row.get(f'{col}_ACP')

				if val_prod != val_acp and not (pd.isna(val_prod) and pd.isna(val_acp)):
					
					# Formata ACP para atualizar PROD
					if pd.isna(val_acp):
						val_acp_sql = "NULL"
					else:
						if isinstance(val_acp, float) and val_acp.is_integer():
							val_acp = int(val_acp)
						val_acp_sql = f"'{str(val_acp).replace(chr(39), chr(39)+chr(39))}'"

					# Formata PROD para atualizar ACP
					if pd.isna(val_prod):
						val_prod_sql = "NULL"
					else:
						if isinstance(val_prod, float) and val_prod.is_integer():
							val_prod = int(val_prod)
						val_prod_sql = f"'{str(val_prod).replace(chr(39), chr(39)+chr(39))}'"

					sets_sql_prod.append(f"{col} = {val_acp_sql}")
					sets_sql_acp.append(f"{col} = {val_prod_sql}")

			id_row = row['ID']
			
			if sets_sql_prod:
				script_update_prod.append(f"UPDATE {self.table_name} SET {', '.join(sets_sql_prod)} WHERE ID = '{id_row}';")
			else:
				script_update_prod.append("")

			if sets_sql_acp:
				script_update_acp.append(f"UPDATE {self.table_name} SET {', '.join(sets_sql_acp)} WHERE ID = '{id_row}';")
			else:
				script_update_acp.append("")

		divergences_df['Script_Update_em_PROD'] = script_update_prod
		divergences_df['Script_Update_em_ACP'] = script_update_acp
		
		return divergences_df


	def generate_insert_scripts(self, df: pd.DataFrame, source_suffix: str) -> pd.DataFrame:
		if df.empty:
			return df

		insert_script_list = []
		valid_columns = []
		real_columns = []
		
		for c in df.columns:
			if str(c).endswith(source_suffix) or c == 'ID':
				real_name = str(c).replace(source_suffix, '')
				
				# Whitelist vs Blacklist
				if self.selected_columns_insert:
					if real_name in self.selected_columns_insert:
						valid_columns.append(c)
						real_columns.append(real_name)
				else:
					if real_name not in self.ignore_columns_insert:
						valid_columns.append(c)
						real_columns.append(real_name)

		columns_sql_str = ", ".join(real_columns)

		for index, row in df.iterrows():
			sql_values = []
			
			for i, col in enumerate(valid_columns):
				real_name = real_columns[i]
				
				if real_name in self.pattern_values_insert:
					val = self.pattern_values_insert[real_name]
				else:
					val = row.get(col)

				if pd.isna(val) or val is None:
					sql_values.append("NULL")
				else:
					if isinstance(val, float) and val.is_integer():
						val = int(val)
					formatted_value = str(val).replace("'", "''")
					sql_values.append(f"'{formatted_value}'")

			values_sql_str = ", ".join(sql_values)
			insert_script_list.append(f"INSERT INTO {self.table_name} ({columns_sql_str}) VALUES ({values_sql_str});")

		df['Script_Insert'] = insert_script_list
		return df
