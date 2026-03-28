import pandas as pd
import os
import json
from sqlalchemy import create_engine,text,inspect
import CollectAllData
import CollectAllDataReviews
import AppidsList

def load_data():
    #executa a função para obter os appids e cria o .csv caso o arquivo não exista
    if not os.path.exists("Data/appidsList.csv"):
        AppidsList.getAppids()

    #carrega a lista de appids
    games_list = pd.read_csv("Data/appidsList.csv",sep = ",")
    appid = games_list["appid"][0:1000]

    #carrga o banco de dados (.db)
    engine = create_engine("sqlite:///Data/database.db")

    dataGames = []
    dataReviews = []

    #para cada appid da steam, extrai os dados e salva em um vetor
    for i,item in enumerate(appid):
        print("Jogo nùmero ", i + 1 ," / ", len(appid),". steam_appid: ", item)
        
        game_data = CollectAllData.getData(item)
        if game_data:
            dataGames.append(game_data)
        
        review_data = CollectAllDataReviews.getData(item,waitTime=1)
        if review_data:
            dataReviews.append(review_data)

    #cria os dataframes e salva em .csv
    dfGames = pd.DataFrame(dataGames)
    dfReviews = pd.DataFrame(dataReviews)

    dfGames.to_csv("Data/gamesData.csv",index=False)
    dfReviews.to_csv("Data/gamesReviews.csv",index=False)

    #converte as listas e json para string para salvar no .db
    dfGames = dfGames.apply(
    lambda col: col.map(
        lambda v: json.dumps(v, ensure_ascii=False)
        if isinstance(v, (list, dict))
        else v
        )
    )
    save_to_db(dfGames,engine,"gamesData")
    save_to_db(dfReviews,engine,"gamesReview")
    
# salvar os dados no banco de dados
def save_to_db(df,engine,table_name):
    inspector = inspect(engine)
    
    # colunas que EXISTEM no banco
    cols_db = [col["name"] for col in inspector.get_columns(table_name)]
    
    # mantém só o que existe no banco
    df = df[[c for c in df.columns if c in cols_db]]

    cols = ", ".join(df.columns)
    placeholders = ", ".join([f":{c}" for c in df.columns])
    
    query = text(f"""
            INSERT OR IGNORE INTO {table_name} ({cols})
            VALUES ({placeholders})
            """)
    
    data = df.to_dict(orient="records")
    with engine.begin() as conn:
        conn.execute(query, data)

if __name__ == "__main__":
    load_data()