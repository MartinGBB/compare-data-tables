import pandas as pd

FILE_CSV_PROD = 'AT_PREPARE_STEP_PROD'; 
FILE_CSV_ACP = 'AT_PREPARE_STEP_ACP'; 
MAIN_COLUMN = 'ID';
GENERATE_FILE = False;


df_prod = pd.read_csv(rf'.\data_csv\{FILE_CSV_PROD}.csv')
df_acp = pd.read_csv(rf'.\data_csv\{FILE_CSV_ACP}.csv')

df_left = pd.merge(df_prod, df_acp, on=MAIN_COLUMN, how='left', suffixes=('_PROD', '_ACP'), indicator=True)
df_right = pd.merge(df_prod, df_acp, on=MAIN_COLUMN, how='right', suffixes=('_PROD', '_ACP'), indicator=True)

# Pega dados das novas listas e copiando em memoria
df_exclusivo_prod = df_left[df_left['_merge'] == 'left_only'].copy()
df_exclusivo_prod['Status_Comparacao'] = 'Exclusivo em Prod (Faltando em ACP)'

df_exclusivo_acp = df_right[df_right['_merge'] == 'right_only'].copy()
df_exclusivo_acp['Status_Comparacao'] = 'Exclusivo em ACP (Faltando em PROD)'

# Lipeza de colunas do Prod que ficam na aba de ACP
colunas_para_manter = ['ID', 'Status_Comparacao'] + [col for col in df_exclusivo_acp.columns if col.endswith('_ACP')]
df_exclusivo_acp_limpo = df_exclusivo_acp[colunas_para_manter].copy()


# Cria excel em abas separadas no mesmo arqvo. 
if GENERATE_FILE:
    with pd.ExcelWriter('Comparacao_Ambientes.xlsx') as writer:
        df_exclusivo_prod.to_excel(writer, sheet_name=f'Falta em ACP (Exclusivo Prod)-{len(df_exclusivo_prod)}', index=False)
        df_exclusivo_acp_limpo.to_excel(writer, sheet_name=f'Falta em Prod (Exclusivo ACP)-{len(df_exclusivo_acp)}', index=False)

print("Análise de diferenças")
print(f"- Qty exclusivo em Prod: {len(df_exclusivo_prod)}")
print(f"- Qty exclusivo em Test: {len(df_exclusivo_acp)}")