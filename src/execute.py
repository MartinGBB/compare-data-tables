from Main import Main

FILE_CSV_PROD = 'AT_PREPARE_STEP_PROD' 
FILE_CSV_ACP = 'AT_PREPARE_STEP_ACP'

main = Main(FILE_CSV_PROD, FILE_CSV_ACP)
data_prod, data_acp = main.load_data()

print(data_prod.head())
print(data_acp.head())