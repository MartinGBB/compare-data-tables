from main import Main

FILE_CSV_PROD = 'AT_PREPARE_STEP_PROD' 
FILE_CSV_ACP = 'AT_PREPARE_STEP_ACP'

main = Main(FILE_CSV_PROD, FILE_CSV_ACP)
data_prod, data_acp = main.load_data()
exclusives_prod_len, exclusives_acp_len = main.compare_data_len()
exclusives_prod, exclusives_acp = main.compare_data()

main.generate_excel(exclusives_prod, exclusives_acp)

print(f"Exclusives in PROD: {exclusives_prod}")
print(f"Exclusives in ACP: {exclusives_acp}")