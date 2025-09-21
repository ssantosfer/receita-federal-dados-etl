from sqlalchemy import String, Integer, Float

empresas_schema = {
    "cnpj": String,
    "razao_social": String,
    "natureza_juridica": Integer,
    "qualificacao_responsavel": Integer,
    "capital_social": Float,
    "cod_porte": String
}