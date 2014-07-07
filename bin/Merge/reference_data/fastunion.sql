/*function to remove null and duplicate value from array*/
CREATE OR REPLACE FUNCTION array_distinct(anyarray)
RETURNS anyarray AS $$
  SELECT ARRAY(SELECT DISTINCT unnest($1) EXCEPT SELECT NULL)
$$ LANGUAGE sql;

/*Create sequence geo_id if not exists*/
DROP SEQUENCE IF EXISTS GEO_ID;
CREATE SEQUENCE GEO_ID START 1; 

/*explode multipolygons to single parts*/
DROP TABLE IF EXISTS T1_exp;
CREATE TEMP TABLE T1_exp AS
 SELECT project, dmcdate, (ST_Dump(ST_Buffer(geom, 0))).geom AS geom
 FROM table1;

DROP TABLE IF EXISTS T2_exp; 
CREATE TEMP TABLE T2_exp AS 
 SELECT project, dmcdate, (ST_Dump(ST_Buffer(geom, 0))).geom AS geom
 FROM table2;

 
/*combine geometries into a single table*/

/*creates a single table of non-overalapping polygons*/
/*warning takes a long time to execute..*/

--Get interior parts of geometry in table1
DROP TABLE IF EXISTS t1i;
CREATE TEMP TABLE t1i AS 
SELECT ST_Makepolygon(ST_InteriorRingN(
    geom,
    generate_series(1, ST_NumInteriorRings(geom)))) AS geom
FROM T1_exp;

--Get interior parts of geometry in table2
DROP TABLE IF EXISTS t2i;
CREATE TEMP TABLE t2i AS 
SELECT ST_Makepolygon(ST_InteriorRingN(
    geom,
    generate_series(1, ST_NumInteriorRings(geom)))) AS geom
FROM T2_exp;

--Get interior rings of two tables
DROP TABLE IF EXISTS all_in_lines;
CREATE TEMP TABLE all_in_lines AS
SELECT ST_ExteriorRing((ST_Dump(geom)).geom) AS geom
FROM  (SELECT COALESCE(ST_Difference(t1i.geom, T2_exp.geom), t1i.geom) AS geom 
      FROM t1i LEFT JOIN T2_exp ON ST_Intersects(t1i.geom, T2_exp.geom)
      UNION ALL
      SELECT COALESCE(ST_Difference(t2i.geom, T1_exp.geom), t2i.geom) AS geom 
      FROM t2i LEFT JOIN T1_exp ON ST_Intersects(t2i.geom, T1_exp.geom)) AS T;

--Union interior rings from two tables
DROP TABLE IF EXISTS noded_in_lines;
CREATE TEMP TABLE noded_in_lines AS
SELECT ST_Union(geom) AS geom
FROM all_in_lines;

--Get exterior rings of two tables
DROP TABLE IF EXISTS all_ex_lines;
CREATE TEMP TABLE all_ex_lines AS
SELECT ST_ExteriorRing(geom) AS geom
FROM T1_exp
UNION ALL
SELECT ST_ExteriorRing(geom) AS geom
FROM T2_exp;

--Union exterior rings from two tables
DROP TABLE IF EXISTS noded_ex_lines;
CREATE TEMP TABLE noded_ex_lines AS
SELECT ST_Union(geom) AS geom
FROM all_ex_lines;

--Polygonize exterior rings
DROP TABLE IF EXISTS new_ex_polys;
CREATE TEMP TABLE new_ex_polys (geom geometry);
INSERT INTO new_ex_polys (geom)
SELECT geom AS geom
FROM St_Dump((
 SELECT St_Polygonize(geom) AS geom
 FROM noded_ex_lines
 WHERE ST_IsValid(geom)
));

--Polygonize interior rings
DROP TABLE IF EXISTS new_in_polys;
CREATE TEMP TABLE new_in_polys (geom geometry);
INSERT INTO new_in_polys (geom)
SELECT geom AS geom
FROM St_Dump((
 SELECT St_Polygonize(geom) AS geom
 FROM noded_in_lines
 WHERE ST_IsValid(geom)
));

--Dissolve two layers
DROP TABLE IF EXISTS new_ex_polys_exp;
CREATE TEMP TABLE new_ex_polys_exp AS
 SELECT (ST_Dump(geom)).geom
 FROM new_ex_polys;

/*create buffer*/
DROP TABLE IF EXISTS bufshp ;
CREATE TEMP TABLE bufshp AS
SELECT ST_Buffer(geom, 0) AS geom
FROM new_ex_polys_exp;

/*merge near polygons*/
DROP TABLE IF EXISTS new_ex_polys ;
CREATE TEMP TABLE new_ex_polys AS
SELECT ST_Buffer(ST_Union(geom), 0) AS geom
FROM bufshp;

DROP TABLE IF EXISTS new_in_polys_exp;
CREATE TEMP TABLE new_in_polys_exp AS
 SELECT (ST_Dump(geom)).geom
 FROM new_in_polys;

/*create buffer*/
DROP TABLE IF EXISTS bufshp ;
CREATE TEMP TABLE bufshp AS
SELECT ST_Buffer(geom, 0) AS geom
FROM new_in_polys_exp;

/*merge near polygons*/
DROP TABLE IF EXISTS new_in_polys ;
CREATE TEMP TABLE new_in_polys AS
SELECT ST_Buffer(ST_Union(geom), 0) AS geom
FROM bufshp;

--Generate new polygons
DROP TABLE IF EXISTS new_polys_uni;
CREATE TEMP TABLE new_polys_uni AS
SELECT COALESCE(ST_Difference(E.geom, I.geom), E.geom) AS geom 
FROM new_ex_polys AS E JOIN new_in_polys AS I ON ST_Intersects(E.geom, I.geom);

DROP TABLE IF EXISTS new_polys;
CREATE TEMP TABLE new_polys (id serial PRIMARY KEY, project text, dmcdate date, geom geometry);
INSERT INTO new_polys (project, dmcdate, geom)
SELECT T.project, T.dmcdate, (ST_Dump(geom)).geom
FROM new_polys_uni, (SELECT project, dmcdate
                     FROM T1_exp
                     LIMIT 1) AS T;

DROP TABLE IF EXISTS TALL;
CREATE TABLE TALL (gid serial PRIMARY KEY, project text, dmcdate date, geom geometry);
INSERT INTO TALL (project, dmcdate, geom)
 SELECT project, dmcdate, geom
 FROM new_polys 
 UNION (
  SELECT project::text, dmcdate, geom
  FROM t1 
  )
 UNION (
  SELECT project::text, dmcdate, geom
  FROM t2
 );

DROP TABLE IF EXISTS T1;
DROP TABLE IF EXISTS T2;
DROP TABLE IF EXISTS table1;
ALTER TABLE TALL RENAME TO T1;
