/*find intersection of polygon from t1*/
DROP TABLE IF EXISTS table1;
CREATE TABLE table1 AS
SELECT DISTINCT t1.*
FROM t1, t2
WHERE ST_Intersects(t1.geom, t2.geom);


/*find intersection of polygon from t2*/
DROP TABLE IF EXISTS table2;
CREATE TABLE table2 AS
SELECT DISTINCT t2.*
FROM t1, t2
WHERE ST_Intersects(t1.geom, t2.geom);

/*delete intersection of polygon from t1*/
DELETE FROM t1 USING table1
WHERE t1.gid = table1.gid;

/*delete intersection of polygon from t2*/
DELETE FROM t2 USING table2
WHERE t2.gid = table2.gid;

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
 SELECT gid AS T1_gid, project AS T1_project, dmcdate AS T1_date, (ST_Dump(geom)).geom
 FROM table1;

DROP TABLE IF EXISTS T2_exp; 
CREATE TEMP TABLE T2_exp AS 
 SELECT gid AS T2_gid, project AS T2_project, dmcdate AS T2_date, (ST_Dump(geom)).geom
 FROM table2;
 
DROP TABLE IF EXISTS T1_exp2;
CREATE TEMP TABLE T1_exp2 AS
 --SELECT gid AS T1_gid, project AS T1_project, dmcdate AS T1_date, (ST_Dump(geom)).geom
 SELECT gid AS T1_gid, project AS T1_project, dmcdate AS T1_date, ST_MakePolygon(St_ExteriorRing((ST_Dump(geom)).geom)) geom
 FROM table1;

DROP TABLE IF EXISTS T2_exp2; 
CREATE TEMP TABLE T2_exp2 AS 
 SELECT gid AS T2_gid, project AS T2_project, dmcdate AS T2_date, ST_MakePolygon(St_ExteriorRing((ST_Dump(geom)).geom)) geom
 FROM table2;

 
/*combine geometries into a single table*/

/*creates a single table of non-overalapping polygons*/
/*warning takes a long time to execute..*/
DROP TABLE IF EXISTS all_lines;
CREATE TEMP TABLE all_lines AS
SELECT St_ExteriorRing(geom) AS geom
FROM T1_exp
UNION ALL
SELECT St_ExteriorRing(geom) AS geom
FROM T2_exp;

DROP TABLE IF EXISTS noded_lines;
CREATE TEMP TABLE noded_lines AS
SELECT St_Union(geom) AS geom
FROM all_lines;

DROP TABLE IF EXISTS new_polys;
CREATE TEMP TABLE new_polys (id serial PRIMARY KEY, geom geometry);
INSERT INTO new_polys (geom)
SELECT geom AS geom
FROM St_Dump((
 SELECT St_Polygonize(geom) AS geom
 FROM noded_lines
 WHERE ST_IsValid(geom)
));

DROP TABLE IF EXISTS new_polys_pip;
CREATE TEMP TABLE new_polys_pip AS
SELECT id, ST_PointOnSurface(geom) AS geom
FROM new_polys;

DROP TABLE IF EXISTS T1_T2_combo;
CREATE TEMP TABLE T1_T2_combo AS
SELECT T1_gid, T1_project, T1_date, null AS T2_gid, null AS T2_project, null AS T2_date, geom as geom FROM T1_exp2
UNION ALL
SELECT null AS T1_gid, null AS T1_project, null AS T1_date, T2_gid, T2_project, T2_date, geom as geom FROM T2_exp2;
 
/*group by geom and aggregate original ids by point overlap*/
/* Replicates an ArcGIS-style Union*/
DROP TABLE IF EXISTS T1_T2_union;
 
CREATE TEMP TABLE T1_T2_union AS (
 SELECT NEW.geom AS geom, MAX(orig.T1_gid) AS T1_gid, MIN(orig.T2_gid) AS T2_gid
 FROM T1_T2_combo AS orig, new_polys_pip AS pt, new_polys AS NEW
 WHERE orig.geom && pt.geom AND NEW.geom && pt.geom AND ST_Intersects(orig.geom, pt.geom) AND ST_Intersects (NEW .geom, pt.geom)
 GROUP BY NEW.geom
);
 
/*Join with the original tables to pull in attributes*/
/*This is still single part geometry*/
DROP TABLE IF EXISTS T1_T2_unionjoin;
CREATE TEMP TABLE T1_T2_unionjoin AS 
 SELECT 
	UGeom.geom AS geom, 
	T1.gid AS T1_gid, 
	T2.gid AS T2_gid, 
	array_distinct(ARRAY[T1.gid] || T2.gid) AS Agid, 
	array_distinct(ARRAY[T1.project::text] || T2.project::text) AS Aproject, 
	array_distinct(ARRAY[T1.dmcdate] || T2.dmcdate) AS Adate
 FROM T1_T2_union AS UGeom LEFT JOIN table1 AS T1 ON T1.gid = UGeom.T1_gid LEFT JOIN table2 AS T2 ON T2.gid = UGeom.T2_gid;
 
DROP TABLE IF EXISTS table1;
CREATE TABLE table1 AS 
 SELECT CAST(nextval('GEO_ID') AS integer) AS gid, MAX(UJoin.Aproject[1]) AS project, MAX(UJoin.Adate[1]) AS dmcdate, ST_Multi(ST_Union(UJoin.geom)) AS GEOM
 FROM T1_T2_unionjoin AS UJoin
 GROUP BY T1_gid, T2_gid;
 
DROP TABLE IF EXISTS TALL;
CREATE TABLE TALL (gid serial PRIMARY KEY, project text, dmcdate date, geom geometry);
INSERT INTO TALL (project, dmcdate, geom)
 SELECT project, dmcdate, geom
 FROM table1
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
