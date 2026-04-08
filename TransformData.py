#%%
import pandas as pd
import json
import dateparser #converte datas de diferentes formatos
import sqlite3

#conecta ao banco de dados
conn = sqlite3.connect("Data/database.db")
cursor = conn.cursor()

#le o arquivo sql da querry
with open("sql/data.sql", "r") as file:
    query = file.read()

#cria um dataFrame da querry
dfCopy = pd.read_sql_query(query, conn)

#atualizar a coluna release_date
x = dfCopy['release_date'].fillna('{}').apply(json.loads)
df = pd.DataFrame(x.tolist())

mask = ~df["coming_soon"]#se coming_soon e verdadeiro

dfCopy.insert(loc=11, column="coming_soon", value=df["coming_soon"])
dfCopy["release_date"] = df['date'].apply(lambda x: dateparser.parse(str(x)))

#atualizar colunas que são mais de um valor em formato de lista
#genres (generos)
x = dfCopy['genres'].fillna('{}').apply(json.loads)
dfCopy['genres'] = x.apply(lambda y: [d['description'] for d in y] if isinstance(y, list) else [])
dfCopy['genres'] = dfCopy['genres'].str.join(",")

#categories (categorias)
x = dfCopy['categories'].fillna('{}').apply(json.loads)
dfCopy['categories'] = x.apply(lambda y: [d['description'] for d in y] if isinstance(y, list) else [])
dfCopy['categories'] = dfCopy['categories'].str.join(",")

#platforms (plataformas)
x = dfCopy["platforms"].apply(json.loads)
df = pd.DataFrame(x.tolist())
dfCopy["windows"] = df["windows"]
dfCopy["mac"] = df["mac"]
dfCopy["linux"] = df["linux"]
dfCopy = dfCopy.drop(columns=["platforms"],axis=1,inplace=False)

#transformar a coluna 'recommendations' para int
x = dfCopy["recommendations"].fillna('{}').apply(json.loads)
dfCopy["recommendations"] = pd.DataFrame(x.tolist())["total"]

#preços
df = dfCopy["price_overview"].fillna('{}').apply(json.loads)
df = pd.DataFrame(df.tolist())

dfCopy["currency"] = df["currency"]
dfCopy["inicial_price"] = df["initial"]/100
dfCopy = dfCopy.drop(columns=["price_overview"],axis=1,inplace=False)

#metacritc
df = dfCopy["metacritic"].fillna('{}').apply(json.loads)
df = pd.DataFrame(df.tolist())

dfCopy["metacritic"] = df["score"]


#criar o .csv
dfCopy.to_csv("Data/steam_games.csv", index=False)