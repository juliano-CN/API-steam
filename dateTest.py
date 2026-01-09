#%%
import requests
import json
import pandas as pd
appid = [3820, 3960, 7610, 7620, 8040, 8060, 11610, 12140, 12650, 12660, 19500, 22490, 26300, 32000, 33550, 33700, 33710, 33720, 35030, 39160, 60700, 63970, 106000, 201230, 201330, 202370, 202570, 211070, 212160, 212200, 215100, 217980, 230330, 230350, 231390, 235700, 247930, 280620, 288390, 288570, 326350, 326740, 331560, 354830, 433290, 436890, 499950, 530940, 537180, 558230, 630790, 648590, 650500, 653120, 657860, 681810, 681820, 681830, 681840, 698600, 698920, 710130, 714210, 721310, 723330]

url = "https://store.steampowered.com/api/appdetails?appids={id}"

data = []

for i in appid:
    resp = requests.get(url.format(id=i))
    print(resp.status_code)
    if resp.status_code == 200:
        data.append(resp.json())
        print(resp.json()[str(i)]["success"])

with open("Data/test.json","w") as f:
    json.dump(data,f)

#%%
import pandas as pd

#df = pd.read_csv("Data/steamData.csv")
df = pd.read_sql_table("gamesData","sqlite:///Data/database.db")
df["release_date"].to_dict()


#%%
import pandas as pd
games_list = pd.read_csv("Data/appidsList.csv",sep = ",")
appid = games_list["appid"]
len(appid)