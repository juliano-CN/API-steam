import pandas as pd
from sqlalchemy import create_engine,text
import CollectAllData
import CollectAllDataReviews
import AppidsList

def load_data():
    games_list = pd.read_csv("Data/appidsList.csv",sep = ",")
    appid = games_list["appid"][0:10]

    engine = create_engine("sqlite:///Data/database.db")

    dataGames = []
    dataReviews = []

    for i,item in enumerate(appid):
        print("Jogo nùmero ", i + 1 ," / ", len(appid),". steam_appid: ", item)
        
        game_data = CollectAllData.getData(item,engine)
        if game_data:
            dataGames.append(game_data)
        
        review_data = CollectAllDataReviews.getData(item,engine,waitTime=1)
        if review_data:
            dataReviews.append(review_data)

    dfGames = pd.DataFrame(dataGames)
    dfReviews = pd.DataFrame(dataReviews)

    dfGames.to_csv("Data/gamesData.csv",index=False)
    dfReviews.to_csv("Data/gamesReviews.csv",index=False)

    # salvar no banco de dados
    import json

    dfGames = dfGames.apply(
    lambda col: col.map(
        lambda v: json.dumps(v, ensure_ascii=False)
        if isinstance(v, (list, dict))
        else v
        )
    )
    save_to_db(dfGames,engine,"gamesData")
    save_to_db(dfReviews,engine,"gamesReview")
    

def save_to_db(df,engine,table_name):
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