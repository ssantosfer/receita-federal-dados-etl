import os
from dotenv import load_dotenv
from ingestion.ingest import ingest
from transformation.transform import process_empresas, process_socios
from load.persist import build_gold_sql

def main():
    load_dotenv()
    conn_str = os.getenv("POSTGRES_CONN")

    tables = ["Empresas2", "Socios2"]

    for table in tables:
        ingest(table)

    process_empresas()
    process_socios()
    build_gold_sql(conn_str)

if __name__ == "__main__":
    main()