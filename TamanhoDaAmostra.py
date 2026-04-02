#%%
#Calcular o tamanho da amostra
#Amostragem: amostra aleatória simples sem reposição

#Objetivo da pesquisa: Descobrir quais fatores influenciam
#na quantidade de reviews positivas e negativas que um jogo tem.

import pandas as pd

#Tamanho da população
games_list = pd.read_csv("Data/appidsList.csv",sep = ",")
appid = games_list["appid"]
N = len(appid)
print("Tamanho da população:", N)

import sqlite3

#Variância da amostra
conn = sqlite3.connect("Data/database.db")
cursor = conn.cursor()

query = "SELECT total_reviews FROM gamesReview"

gamesReviewTotal = pd.read_sql_query(query, conn)
S2 = gamesReviewTotal.var().values[0]

print("Variância da amostra:", S2)

#distribuição normal
import scipy.stats as stats

alfa = 0.05# probabilidade de erro
Pnorm = stats.norm.ppf(1-alfa)

#calculo do tamanho da amostra

B = [i*10 for i in range(1,101)]
D = (B/Pnorm)**2
n = 1/(D/S2+1/N)

dfSampleSize = pd.DataFrame({"erro":B,
              "tamanho da amostra":n})

dfSampleSize.to_csv("Data/sampleSize.csv",index=False)

#grau de confiança escolhido: 0.95
#erro escolhido: 190
#tamanho da amostra escolhido: 4927.91 (arrendodar p/ 5000)

