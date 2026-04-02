--calcula a variância da variável total_reviews
SELECT 
    count(total_reviews) as n,
    avg(total_reviews) as media,
    sum((total_reviews - (SELECT avg(total_reviews) FROM gamesReview)) 
    * (total_reviews - (SELECT avg(total_reviews) FROM gamesReview)))
    / (SELECT count(total_reviews) - 1 FROM gamesReview) as variancia
FROM gamesReview