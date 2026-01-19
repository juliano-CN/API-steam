import pandas as pd
import CollectAllData
import CollectAllDataReviews

def load_data():
    games_list = pd.read_csv("Data/appidsList.csv",sep = ",")
    appid = games_list["appid"]

    CollectAllData.getData(appid)
    CollectAllDataReviews.getData(appid,wait_time=1)

if __name__ == "__main__":
    load_data()