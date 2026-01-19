/*so rode este script uma vez para criar a tabela,
caso a tabela ja exista vai apagar os dados antigos*/

--deleta tabela se existir
DROP TABLE IF EXISTS "gamesData";

--cria a tabela
CREATE TABLE IF NOT EXISTS "gamesData"(
	type TEXT,  
	name TEXT,
	steam_appid INTEGER NOT NULL PRIMARY KEY , 
	required_age INTEGER  ,
	is_free BOOLEAN  ,
	supported_languages TEXT  ,
	website TEXT  ,
	developers TEXT  ,
	publishers TEXT  ,
	demos TEXT  ,
	price_overview TEXT  ,
	categories TEXT  ,
	genres TEXT  ,
	release_date TEXT  ,
	dlc TEXT  ,
	controller_support TEXT  ,
	recommendations TEXT ,
	coming_soon BOOLEAN  ,
	windows BOOLEAN ,
	mac BOOLEAN , 
	linux BOOLEAN
);

--tabela de reviews
DROP TABLE IF EXISTS "gamesReview";

CREATE TABLE IF NOT EXISTS "gamesReview" (
	steam_appid INTEGER NOT NULL PRIMARY KEY ,  
	num_reviews BIGINT  ,
	review_score BIGINT  ,
	review_score_desc TEXT ,  
	total_positive BIGINT  ,
	total_negative BIGINT  ,
	total_reviews BIGINT
);