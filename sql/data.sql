--SELECT t1.steam_appid,
--        t1.name,
--        t2.review_score_desc,
--        t2.total_reviews
--FROM gamesData AS t1
--LEFT JOIN gamesReview AS t2
--ON t1.steam_appid = t2.steam_appid
--ORDER BY t1.steam_appid ASC;

--SELECT t1.steam_appid,
--        T1.name
--FROM gamesData AS t1

SELECT count(t1.steam_appid) AS total_games,
        t1.steam_appid
FROM gamesReview AS t1
GROUP BY t1.steam_appid
ORDER BY total_games DESC
LIMIT 10;

SELECT count(*)
FROM temporaryData;

SELECT count(*)
FROM gamesData;

SELECT count(*)
FROM gamesReview;

--SELECT *
--FROM gamesReview
--ORDER BY steam_appid DESC;