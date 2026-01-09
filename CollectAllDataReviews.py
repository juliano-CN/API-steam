import requests
import time
import pandas as pd
import sqlalchemy

#variaveis globais
session = requests.Session()

#reviews positivo/negativo
def MakeRequestReview(steam_appid,retries = 3,waitTime = 10, timeout=10):  
    urlReview = "https://store.steampowered.com/appreviews/{id}?json=1&language=all"

    for i in range(retries):
        respReview = session.get(urlReview.format(id=steam_appid),timeout=timeout)
        json_data = respReview.json()

        print("Tentativa ", i+1, " / 3 para o steam_appid ", steam_appid)
        print("Status:", respReview.status_code)

        if "query_summary" not in json_data:
            return None

        if respReview.status_code == 200:
            rd = {"steam_appid":steam_appid,
            **json_data["query_summary"]}
            return rd
        else:
            time.sleep(waitTime)
    return None

#extração dos dados
def getData(appids,wait_time = 1.5):
    #conexao com o db
    engine = sqlalchemy.create_engine("sqlite:///Data/database.db")

    #carregar os dados caso existam, senao cria uma lista vazia
    try:
        data = pd.read_sql_table("gamesReview",engine)
        data = data.to_dict(orient="records")
    except Exception as e:
        print("Erro ao carregar dados existentes: ", e)
        data = []
    
    #importar a tabela de nomes
    #games_list = pd.read_csv("Data/appidsList.csv",sep = ",")
    appid = appids#games_list["appid"][0:10]

    existing_ids = {row["steam_appid"] for row in data}

    for i,item in enumerate(appid):
        print("Jogo nùmero ", i + 1 ," / ", len(appid),". steam_appid: ", item)
        if item not in existing_ids:
            try:
                data_review = MakeRequestReview(item)

                if data_review:
                    new_row = data_review

                    existing_ids.add(item)

                    df = pd.DataFrame([new_row])
                    df.to_sql("gamesReview",engine,if_exists="append",index=False)

            except Exception as e:
                print("erro: ", e)

            time.sleep(wait_time)

if __name__ == "__main__":
    getData()