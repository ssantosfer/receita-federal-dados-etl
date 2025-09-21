from utils.utils import download_and_extract

def ingest_empresas(bronze_path="data/bronze/empresas"):
    url = "https://arquivos.receitafederal.gov.br/dados/cnpj/dados_abertos_cnpj/2025-09/Empresas2.zip"
    download_and_extract(url, bronze_path)

def ingest_socios(bronze_path="data/bronze/socios"):
    url = "https://arquivos.receitafederal.gov.br/dados/cnpj/dados_abertos_cnpj/2025-09/Socios2.zip"
    download_and_extract(url, bronze_path)