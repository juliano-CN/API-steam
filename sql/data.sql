/*SELECT t1.steam_appid,
        t1.name,
        t1.required_age,
        t2.review_score_desc,
        t2.total_reviews
FROM gamesData AS t1
LEFT JOIN gamesReview AS t2
ON t1.steam_appid = t2.steam_appid
ORDER BY t1.required_age DESC*/

--SELECT t1.steam_appid,
--        T1.name
--FROM gamesData AS t1

SELECT count(t1.steam_appid) AS total_games,
        t1.steam_appid
FROM gamesData AS t1
GROUP BY t1.steam_appid
ORDER BY total_games DESC;

SELECT *
FROM gamesData AS t1
WHERE t1.steam_appid = 39160;

SELECT count(*)
FROM gamesData;



