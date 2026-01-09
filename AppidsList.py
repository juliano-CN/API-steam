import requests
import pandas as pd
import os
from dotenv import load_dotenv
import time

#criando o arquivo .csv dos nomes e dos ids
def getAppids():
    load_dotenv()
    api_key = os.getenv("API_KEY")
    allData = []
    have_more_results = True
    last_appid = 10

    if not api_key:
        raise ValueError("API_KEY não encontrada")

    while have_more_results:

        params = {
        "key": api_key,
        "max_results": 50000,
        "last_appid": last_appid
        }
        
        url = "https://api.steampowered.com/IStoreService/GetAppList/v1/"
        
        try:
            resp = requests.get(url,params=params)
            print(resp)
            if resp.status_code == 200:
                data = resp.json()

            allData.extend(data["response"]["apps"])

            if "have_more_results" in data["response"]:
                print("tem mais jogos: ",data["response"]["have_more_results"])
                have_more_results = data["response"]["have_more_results"]
            else:
                have_more_results = False
            
            if "last_appid" in data["response"]:
                print("ultima appid: ",data["response"]["last_appid"])
                last_appid = data["response"]["last_appid"]

            time.sleep(1)

        except Exception as e:
            print("Erro ao obter a lista. Erro: ", e)
            have_more_results = False

    if not os.path.exists("Data"):
        os.makedirs("Data")

    df = pd.DataFrame(allData)
    df.to_csv("Data/appidsList.csv",index=False)

if __name__ == "__main__":
    getAppids()