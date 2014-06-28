/*merge all small polygons (without attribute)*/

/*split all multi-polygons to single polygon*/
DROP TABLE IF EXISTS input_table_exp;
CREATE TEMP TABLE input_table_exp AS
 SELECT (ST_Dump(geom)).geom
 FROM input_table;

/*create buffer*/
DROP TABLE IF EXISTS U1_BUF ;
CREATE TEMP TABLE U1_BUF AS
SELECT ST_Buffer(geom, 0) AS geom
FROM input_table_exp;

/*merge near polygons*/
DROP TABLE IF EXISTS U1_U ;
CREATE TEMP TABLE U1_U AS
SELECT ST_Buffer(ST_Union(geom), 0) AS geom
FROM U1_BUF;


DROP TABLE IF EXISTS unishp;
CREATE TABLE unishp (gid serial PRIMARY KEY, geom geometry);
INSERT INTO unishp (geom)
SELECT (ST_Dump(geom)).geom
FROM U1_U;
