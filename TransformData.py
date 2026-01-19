#%%
import pandas as pd
import json
import dateparser
from sqlalchemy import create_engine,text

engine = create_engine("sqlite:///Data/database.db")
df = pd.read_sql_table("temporaryData",engine)
dfCopy = df.copy()

#deletar colunas que nao serão usadas
dfCopy = dfCopy.drop(columns=["packages","package_groups","ratings"],axis=1,inplace=False)

#atualizar a coluna release_date
x = dfCopy['release_date'].fillna('{}').apply(json.loads)
df = pd.DataFrame(x.tolist())

mask = ~df["coming_soon"]

dfCopy["coming_soon"] = df["coming_soon"]
dfCopy["release_date"] = df.loc[mask,'date'].apply(lambda x: dateparser.parse(str(x)))

#atualizar colunas que são mais de um valor em formato de lista
x = dfCopy['genres'].fillna('{}').apply(json.loads)
dfCopy['genres'] = x.apply(lambda y: [d['description'] for d in y] if isinstance(y, list) else [])
dfCopy['genres'] = dfCopy['genres'].str.join(",")

x = dfCopy['categories'].fillna('{}').apply(json.loads)
dfCopy['categories'] = x.apply(lambda y: [d['description'] for d in y] if isinstance(y, list) else [])
dfCopy['categories'] = dfCopy['categories'].str.join(",")

#plataformas
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

#salvar no banco de dados
cols = ", ".join(dfCopy.columns)
placeholders = ", ".join([f":{c}" for c in dfCopy.columns])

query = text(f"""
        INSERT OR IGNORE INTO gamesData ({cols})
        VALUES ({placeholders})
        """)

data = dfCopy.to_dict(orient="records")

with engine.begin() as conn:
    conn.execute(query, data)

#%%
#print(dfCopy.info())
print(dfCopy.columns)
#print(dfCopy.head())
dfCopy.to_csv("Data/transformData.csv",index=False)

#%%
dfCopy