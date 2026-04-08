SELECT t1.steam_appid,t1.name, t1.required_age, 
    t1.is_free,t1.supported_languages,t1.website,
    t1.price_overview,t1.platforms,t1.categories,
    t1.genres,t1.recommendations,t1.release_date,t1.metacritic,
    t1.demos,t1.dlc,
    t2.review_score_desc,
    t2.total_positive,t2.total_negative,t2.total_reviews
FROM gamesData AS t1
LEFT JOIN gamesReview AS t2
ON t1.steam_appid = t2.steam_appid;