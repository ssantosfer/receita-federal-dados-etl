from utils.utils import download_and_extract

def ingest(table: str, bronze_path_base="data/bronze"):
    url = f"https://arquivos.receitafederal.gov.br/dados/cnpj/dados_abertos_cnpj/2025-09/{table}.zip"
    
    table_map = {
        "Empresas2": "empresas",
        "Socios2": "socios"
    }
    folder_name = table_map.get(table, table.lower())
    bronze_path = f"{bronze_path_base}/{folder_name}"
    download_and_extract(url, bronze_path)