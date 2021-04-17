import requests as requests


def call_api(url: str) -> dict:
    r = requests.get(url)
    return r.json()


def get_address_data(row):
    cep = row["CEP"]
    url = f"https://viacep.com.br/ws/{cep}/json/"
    response = call_api(url)

    uf = response.get("uf", None)
    bairro = response.get("bairro", None)
    localidade = response.get("localidade", None)
    logradouro = response.get("logradouro", None)
    complemento = response.get("complemento", None)
    return uf, bairro, localidade, logradouro, complemento
