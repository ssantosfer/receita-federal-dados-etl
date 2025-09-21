import os
import requests
import zipfile
import logging
import pandas as pd
from sqlalchemy import create_engine

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

def download_and_extract(url: str, output_path: str):
    local_zip = "temp.zip"
    
    os.makedirs(output_path, exist_ok=True)

    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(local_zip, "wb") as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)

    with zipfile.ZipFile(local_zip, "r") as zip_ref:
        zip_ref.extractall(output_path)

    os.remove(local_zip)
    logging.info(f"Download e extração concluídos em: {output_path}")

def load_to_postgres(df: pd.DataFrame, table_name: str, conn_str: str, dtype: dict = None, chunksize: int = None):
    """
    Salva um DataFrame no Postgres.

    Args:
        df (pd.DataFrame): DataFrame a ser salvo.
        table_name (str): Nome da tabela no Postgres.
        conn_str (str): Connection string no formato:
            postgresql+psycopg2://user:password@host:port/database
        dtype (dict, opcional): Dicionário de tipos de dados para a tabela.
        chunksize (int, opcional): Número de linhas para inserir por vez (útil para DataFrames grandes).
    """
    engine = create_engine(conn_str)

    df.to_sql(
        table_name,
        conn_str,
        if_exists="replace",
        index=False,
        dtype=dtype,
        chunksize=chunksize
    )

    logging.info(f"Dados salvos: {table_name}")