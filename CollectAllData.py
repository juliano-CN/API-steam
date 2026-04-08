import requests
import time

#variaveis globais
session = requests.Session()

missing_values = []

#informacoes gerais 
#steam_appid,numero de tentativas, tempo de espera,tempo de espera da resposta do servidor
def MakeRequestGenre(steam_appid,retries = 3,waitTime = 10, timeout=10):
    #url da API
    urlGenre = "https://store.steampowered.com/api/appdetails?appids={id}&language=english"

    #tenta fazer a requisição no máximo 3 vezes, se falhar todas as vezes, retorna None 
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

            return rg
        else:
            time.sleep(waitTime)
    return None

#extração dos dados
#tenta chamar a função MakeRequestGenre, se der erro, printa o erro e retorna None
def getData(appid,wait_time = 1.5):
    try:
        data_genre = MakeRequestGenre(appid)
        time.sleep(wait_time)
        if data_genre:
            return data_genre

    except Exception as e:
        print("erro: ", e)

    return None

if __name__ == "__main__":
    import pandas as pd
    example = getData(281990)
    example = pd.DataFrame([example])
    example.to_csv("Data/example.csv",index=False)
    print(example)