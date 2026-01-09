#%%
import pandas as pd
import json

df = pd.read_sql_table("gamesData","sqlite:///Data/database.db")
dfCopy = df.copy()
dfCopy.columns

#%%
x = dfCopy['release_date'].fillna('{}').apply(json.loads)
df = pd.DataFrame(x.tolist())
df["date"] = pd.to_datetime(df["date"],format="mixed")
df

#%%
x = dfCopy['price_overview'].fillna('{}').apply(json.loads)
df = pd.DataFrame(x.tolist())
df

#%%
x = dfCopy['genres'].fillna('{}').apply(json.loads)
x.apply(lambda y: [d['description'] for d in y] if isinstance(y, list) else [])

#%%
x = dfCopy['categories'].fillna('{}').apply(json.loads)
x.apply(lambda y: [d['description'] for d in y] if isinstance(y, list) else [])

#%%
x = dfCopy["platforms"].apply(json.loads)
df = pd.DataFrame(x.tolist())
df

#%%
dfCopy['demos'].isna().value_counts()