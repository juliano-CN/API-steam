import requests
import time
import pandas as pd
import sqlalchemy
from sqlalchemy import text
import json

#variaveis globais
session = requests.Session()

columns = ['type', 'name', 'steam_appid', 'required_age', 'is_free',
       'supported_languages',
       'website',
       'developers', 'publishers',
       'demos', 'price_overview', 'packages', 'package_groups', 'platforms',
       'categories', 'genres',
       'release_date',
       'ratings', 'dlc', 'controller_support',
       'recommendations']

missing_values = []

#informacoes gerais
def MakeRequestGenre(steam_appid,retries = 3,waitTime = 10, timeout=10):
    urlGenre = "https://store.steampowered.com/api/appdetails?appids={id}"

    for i in range(retries):
        respGenre = session.get(urlGenre.format(id=steam_appid),timeout=timeout)
        print("Tentativa ", i+1, " / 3 para o steam_appid ", steam_appid)
        print("Status: ", respGenre.status_code)

        if respGenre.status_code == 200:
            dataJson = respGenre.json()[str(steam_appid)]
            if not dataJson or not dataJson.get("success") or not dataJson.get("data"):
                missing_values.append(steam_appid)
                return None

            rg = dataJson["data"]
            rg = {key: rg.get(key, None) for key in columns}
            return rg
        else:
            time.sleep(waitTime)
    return None

#extração dos dados
def getData(appids,wait_time = 1.5):
    #conexao com o db
    engine = sqlalchemy.create_engine("sqlite:///Data/database.db")

    #carregar os dados caso existam, senao cria uma lista vazia
    try:
        data = pd.read_sql_table("temporaryData",engine)
        data = data.to_dict(orient="records")
    except Exception as e:
        print("Erro ao carregar dados existentes: ", e)
        data = []
    
    #importar a tabela de nomes
    #games_list = pd.read_csv("Data/appidsList.csv",sep = ",")
    #appid = appids#games_list["appid"][0:15]
    #existing_ids = {row["steam_appid"] for row in data}

    #importar a tabela de nomes
    existing_ids = {int(row["steam_appid"]) for row in data if row["steam_appid"] is not None}
    appid = [int(x) for x in appids]

    for i,item in enumerate(appid):
        print("Jogo nùmero ", i + 1 ," / ", len(appid),". steam_appid: ", item)
        if item not in existing_ids:
            try:
                data_genre = MakeRequestGenre(item)
                if data_genre:
                    new_row = data_genre

                    #converte as variaveis para string caso sejam list ou dict
                    for key in new_row:
                        if isinstance(new_row[key], (list, dict)):
                            new_row[key] = json.dumps(new_row[key], ensure_ascii=False)

                    existing_ids.add(item)

                    df = pd.DataFrame([new_row])
                    df.to_sql("temporaryData",engine,if_exists="append",index=False)
            except Exception as e:
                print("erro: ", e)
                

            time.sleep(wait_time)
    
    #with engine.begin() as conn:
    #    conn.execute(text("""INSERT OR IGNORE INTO gamesData 
    #                    SELECT *
    #                    FROM temporaryData;
    #                    """))

    print("Processo concluído.")
    print("Valores faltantes: ", missing_values)

if __name__ == "__main__":
    getData()