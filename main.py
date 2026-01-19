import pandas as pd
import CollectAllData
import CollectAllDataReviews

def load_data():
    games_list = pd.read_csv("Data/appidsList.csv",sep = ",")#carrega a lista de appids(5 de janeiro de 2026)
    appid = games_list["appid"][145000:151975]#1150

    #CollectAllData.getData(appid)
    CollectAllDataReviews.getData(appid,wait_time=1)

if __name__ == "__main__":
    load_data()