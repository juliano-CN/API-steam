SELECT *
FROM gamesData AS t1
LEFT JOIN gamesReview AS t2
ON t1.steam_appid = t2.steam_appid
LIMIT 10;