/*merge all small polygons (without attribute)*/

/*split all multi-polygons to single polygon*/
DROP TABLE IF EXISTS T1_exp;
CREATE TEMP TABLE T1_exp AS
 SELECT (ST_Dump(geom)).geom
 FROM T1;

/*create buffer*/
DROP TABLE IF EXISTS U1_BUF ;
CREATE TEMP TABLE U1_BUF AS
SELECT ST_Buffer(geom, 0) AS geom
FROM T1_exp;

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