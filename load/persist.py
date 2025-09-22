import os
import pandas as pd
from sqlalchemy import create_engine, text
from utils.utils import load_to_postgres
from schema.empresas_schema import empresas_schema
from schema.socios_schema import socios_schema
import logging

def build_gold_sql(conn_str: str, gold_path="data/gold/final.parquet"):
    engine = create_engine(conn_str)
    logging.info("Conectando ao Postgres...")

    df_empresas = pd.read_parquet("data/silver/empresas/empresas.parquet")
    df_socios = pd.read_parquet("data/silver/socios/socios.parquet")
    logging.info(f"Tabelas lidas: empresas({len(df_empresas):,} linhas), sócios({len(df_socios):,} linhas)")

    load_to_postgres(df_empresas, "stg_empresas", conn_str, chunksize=100000, dtype=empresas_schema)
    load_to_postgres(df_socios, "stg_socios", conn_str, chunksize=100000, dtype=socios_schema)
    logging.info("Tabelas inseridas no Postgres...")

    sql = """
        WITH agg_socios AS (
            SELECT 
                cnpj,
                COUNT(*) AS qtde_socios,
                BOOL_OR(documento_socio ~ '^9+$') AS flag_socio_estrangeiro
            FROM stg_socios
            GROUP BY cnpj
        )
        SELECT 
            e.cnpj,
            COALESCE(s.qtde_socios, 0) AS qtde_socios,
            COALESCE(s.flag_socio_estrangeiro, false) AS flag_socio_estrangeiro,
            (e.cod_porte = '03' AND COALESCE(s.qtde_socios, 0) > 1) AS doc_alvo
        FROM stg_empresas e
        LEFT JOIN agg_socios s ON e.cnpj = s.cnpj;
    """

    with engine.connect() as conn:
        df_gold = pd.read_sql(text(sql), conn)

    os.makedirs(os.path.dirname(gold_path), exist_ok=True)
    df_gold.to_parquet(gold_path, index=False)
    load_to_postgres(df_gold, "agg_empresas", conn_str)
    
    logging.info("Processo finalizado: camada Gold gerada e persistida com sucesso")