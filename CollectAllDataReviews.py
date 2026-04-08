import requests
import time

#variaveis globais
session = requests.Session()

#reviews positivo/negativo
def MakeRequestReview(steam_appid,retries = 3,waitTime = 10, timeout=10):  
    urlReview = "https://store.steampowered.com/appreviews/{id}?json=1&language=english"

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
def getData(appid,waitTime = 1.5):
    try:
        data_review = MakeRequestReview(appid)
        time.sleep(waitTime)
        if data_review:
            return data_review

    except Exception as e:
        print("erro: ", e)
    
    return None

if __name__ == "__main__":
    example = getData(281990)
    print(example)