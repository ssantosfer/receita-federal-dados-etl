import os
import pandas as pd
import logging

def process_empresas(bronze_path="data/bronze/empresas", silver_path="data/silver/empresas"):
    os.makedirs(silver_path, exist_ok=True)
    file = [f for f in os.listdir(bronze_path) if f.endswith(".EMPRECSV")][0]

    logging.info(f"Processando arquivo: {file}")

    colunas = [
        "cnpj", "razao_social", "natureza_juridica",
        "qualificacao_responsavel", "capital_social", "cod_porte"
    ]

    df = pd.read_csv(
        os.path.join(bronze_path, file),
        sep=";",
        encoding="latin1",
        header=None,
        usecols=[0, 1, 2, 3, 4, 5],
        names=colunas,
        dtype=str
    )

    df["natureza_juridica"] = pd.to_numeric(df["natureza_juridica"]).astype("Int64")
    df["qualificacao_responsavel"] = pd.to_numeric(df["qualificacao_responsavel"]).astype("Int64")
    df["capital_social"] = pd.to_numeric(df["capital_social"].str.replace(",", "."))

    df.to_csv(os.path.join(silver_path, "empresas.csv"), index=False)
    logging.info(f"Arquivo processado ({len(df):,} linhas) | Arquivo salvo em {silver_path}")


def process_socios(bronze_path="data/bronze/socios", silver_path="data/silver/socios"):
    os.makedirs(silver_path, exist_ok=True)

    file = [f for f in os.listdir(bronze_path) if f.endswith(".SOCIOCSV")][0]

    logging.info(f"Processando arquivo: {file}")

    colunas = [
        "cnpj", "tipo_socio", "nome_socio",
        "documento_socio", "codigo_qualificacao_socio"
    ]

    df = pd.read_csv(
        os.path.join(bronze_path, file),
        sep=";",
        encoding="latin1",
        header=None,
        usecols=[0, 1, 2, 3, 4],
        names=colunas,
        dtype=str
    )

    df["tipo_socio"] = pd.to_numeric(df["tipo_socio"]).astype("Int64")

    df.to_csv(os.path.join(silver_path, "socios.csv"), index=False)
    logging.info(f"Arquivo processado ({len(df):,} linhas) | Arquivo salvo em {silver_path}")