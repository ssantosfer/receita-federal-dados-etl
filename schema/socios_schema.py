from sqlalchemy import String, Integer

socios_schema = {
    "cnpj": String,
    "tipo_socio": Integer,
    "nome_socio": String,
    "documento_socio": String,
    "codigo_qualificacao_socio": String
}