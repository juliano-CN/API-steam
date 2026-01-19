--deleta linhas duplicadas mantendo uma
DELETE FROM temporaryData
WHERE rowid NOT IN (
    SELECT MAX(rowid)
    FROM temporaryData
    GROUP BY steam_appid
    ORDER BY name
);

--move a nova tabela para outra
--INSERT OR IGNORE INTO gamesData 
--SELECT *
--FROM temporaryData;

--deleta todos os elementos da tabela mas mantem a tabela
--DELETE FROM temporaryData;