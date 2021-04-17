import pathlib

import pandas as pd
from decouple import config
from pandas import DataFrame
from sqlalchemy import create_engine

from translations import DEPARTMENT_TRANSLATIONS, MARKET_TRANSLATIONS
from viacep import get_address_data

TAXA_REAL = 6.74
TAXA_DOLAR = 1.1986
VALOR_DOLAR = TAXA_REAL / TAXA_DOLAR

DATA_PATH = pathlib.Path.cwd() / "data"
DADOS_COMPLEMENTARES_PATH = DATA_PATH / "dados-complementares.csv"
DADOS_PESSOAIS_PATH = DATA_PATH / "dados-pessoais.xlsx"

dados_pessoais: DataFrame = pd.read_excel(DADOS_PESSOAIS_PATH, engine="openpyxl")
dados_complementares: DataFrame = pd.read_csv(DADOS_COMPLEMENTARES_PATH)
data = dados_pessoais.join(dados_complementares)

data[["nome", "sobrenome"]] = data["Nome completo"].str.split(" ", n=1, expand=True)
data.drop(columns=["Nome completo"], inplace=True)
data.rename(
    columns={
        "Data de aniversário": "data_aniversario",
        "id": "id_usuario",
        "Dinheiro": "dinheiro_real",
        "wage": "salario_dolar",
        "department": "profissao",
        "market": "mercado",
    },
    inplace=True,
)


data[["uf", "bairro", "localidade", "logradouro", "complemento"]] = data.apply(
    get_address_data, axis=1, result_type="expand"
)
data["dinheiro_dolar"] = data["dinheiro_real"].apply(
    lambda x: round(x / VALOR_DOLAR, 2)
)
data["salario_dolar"] = data["salario_dolar"].apply(
    lambda x: float(x[1:]) if type(x) == str else None
)
data["salario_real"] = data["salario_dolar"].apply(
    lambda x: round(x * VALOR_DOLAR, 2) if type(x) == float else None
)
data["mercado"] = data["mercado"].apply(lambda x: MARKET_TRANSLATIONS.get(x))
data["profissao"] = data["profissao"].apply(lambda x: DEPARTMENT_TRANSLATIONS.get(x))

data = data[
    [
        "id_usuario",
        "nome",
        "sobrenome",
        "RG",
        "CPF",
        "data_aniversario",
        "logradouro",
        "complemento",
        "bairro",
        "localidade",
        "uf",
        "CEP",
        "dinheiro_real",
        "dinheiro_dolar",
        "profissao",
        "mercado",
        "salario_real",
        "salario_dolar",
    ]
]

engine = create_engine(f'mysql+pymysql://{config("DR_URL")}')
data.to_sql(name="dados", con=engine, if_exists="replace")
