/*so rode este script uma vez para criar a tabela,
caso a tabela ja exista vai apagar os dados antigos*/

--deleta tabela se existir
DROP TABLE IF EXISTS "gamesData";

--cria a tabela
CREATE TABLE IF NOT EXISTS "gamesData"(
	type TEXT,
	name TEXT,
	steam_appid INTEGER NOT NULL PRIMARY KEY ,
	required_age INTEGER ,
	is_free BOOLEAN ,
	detailed_description TEXT ,
	about_the_game TEXT ,
	short_description TEXT ,
	supported_languages TEXT ,
	header_image TEXT ,
	capsule_image TEXT ,
	capsule_imagev5 TEXT ,
	website TEXT ,
	pc_requirements TEXT ,
	mac_requirements TEXT ,
	linux_requirements TEXT ,
	developers TEXT ,
	publishers TEXT ,
	price_overview TEXT ,
	packages TEXT ,
	package_groups TEXT ,
	platforms TEXT ,
	categories TEXT ,
	genres TEXT ,
	screenshots TEXT ,
	recommendations TEXT ,
	release_date TEXT ,
	support_info TEXT ,
	background TEXT ,
	background_raw TEXT ,
	content_descriptors TEXT ,
	ratings TEXT ,
	metacritic TEXT ,
	controller_support TEXT ,
	dlc TEXT ,
	demos TEXT ,
	movies TEXT ,
	achievements TEXT ,
	reviews TEXT,
	legal_notice TEXT,
	drm_notice TEXT
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