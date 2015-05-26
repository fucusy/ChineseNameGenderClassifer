
SELECT `name`,`is_male` FROM person WHERE `is_male` IS NOT NULL ORDER BY `name`
INTO OUTFILE '/tmp/name_gender.cvs'
FIELDS TERMINATED BY ','
  ENCLOSED BY '"'
LINES TERMINATED BY '\n';