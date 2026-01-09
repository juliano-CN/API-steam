import pandas as pd
import CollectAllData
import CollectAllDataReviews

def load_data():
    games_list = pd.read_csv("Data/appidsList.csv",sep = ",")#carrega a lista de appids(5 de janeiro de 2026)
    appid = games_list["appid"][76000:80000]

    CollectAllData.getData(appid)
    #CollectAllDataReviews.getData(appid)

if __name__ == "__main__":
    load_data()