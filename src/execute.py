from Main import Main

FILE_CSV_PROD = 'AT_PREPARE_STEP_PROD' 
FILE_CSV_ACP = 'AT_PREPARE_STEP_ACP'

main = Main(FILE_CSV_PROD, FILE_CSV_ACP)
data_prod, data_acp = main.load_data()
exclusives_prod, exclusives_acp = main.compare_data_len()

print(f"Exclusives in PROD: {exclusives_prod}")
print(f"Exclusives in ACP: {exclusives_acp}")