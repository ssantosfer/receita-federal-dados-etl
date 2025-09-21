import os
from dotenv import load_dotenv
from ingestion.ingest import ingest_empresas, ingest_socios
from transformation.transform import process_empresas, process_socios
from load.persist import build_gold_sql

def main():
    #load_dotenv()
    conn_str = "postgresql+psycopg2://postgres:1020@localhost:5432/receita"
    
    ingest_empresas()
    ingest_socios()
    process_empresas()
    process_socios()
    build_gold_sql(conn_str)

if __name__ == "__main__":
    main()