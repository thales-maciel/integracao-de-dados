# Integração de dados

## CONTEXTO
Temos dados de pessoas, que estão fragmentados em pontos diversos.
Precisamos buscar estes dados e oferecer ao usuário uma visualização destes dados unificados e tratados, pois parte deles necessitam de tradução ou conversão.

## ENTRADA
Na planilha (`data/dados-pessoais.xlsx`) temos as informações básicas.
No arquivo (`data/dados-complementares.csv`) temos dados complementares.
- execute a leitura dos arquivos

## BUSCA DE DADOS
- busque os dados do endereço (rua, bairro, cidade, estado) via CEP:
https://viacep.com.br

## TRATAMENTO DE DADOS
- faça as conversões monetárias necessárias, com base em https://www.ecb.europa.eu/stats/eurofxref/eurofxref-daily.xml
Exemplo de cálculo para conversão:
Taxa do real (BRL): 3.2091
Taxa do dólar americano (USD): 1.3776
Valor de um dólar americano em reais: 3.2091 / 1.3776 = 2.33
- para os dados profissionais, crie uma função que traduza os termos dos campos "department" e "market" para português (para esta ação, não é necessário o uso de API)

## CRIAÇÃO DO BANCO DE DADOS
- crie uma tabela no banco de dados para armazenar os dados. Campos:
id_usuario | nome | sobrenome | RG | CPF | data_aniversario
logradouro | complemento | bairro | localidade | uf | CEP
dinheiro_real | dinheiro_dolar
profissao | mercado | salario_real | salario_dolar
obs.: trata-se de apenas uma tabela. A quebra de linha foi utilizada para agrupar campos relacionados.

## INSERÇÃO DE DADOS
- armazene os dados unificados/tratados na tabela.
