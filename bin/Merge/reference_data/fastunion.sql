/*Create sequence geo_id if not exists*/
DROP SEQUENCE IF EXISTS GEO_ID;
CREATE SEQUENCE GEO_ID START 1;

/*create union of two tables*/
DROP TABLE IF EXISTS t1t2combo;
CREATE TEMP TABLE t1t2combo AS
SELECT dmcdate, ST_Union(ST_Buffer(geom, 0)) AS geom
FROM table1
GROUP BY dmcdate
UNION ALL
SELECT dmcdate, ST_Union(ST_Buffer(geom, 0)) AS geom
FROM table2
GROUP BY dmcdate;

/*create union of t1t2combo table*/
DROP TABLE IF EXISTS new_polys;
CREATE TEMP TABLE new_polys (id serial PRIMARY KEY, dmcdate date, geom geometry);
INSERT INTO new_polys (dmcdate, geom)
SELECT T.dmcdate, (ST_Dump(ST_Union(geom))).geom AS geom
FROM t1t2combo, (SELECT dmcdate
                     FROM table1
                     LIMIT 1) AS T
GROUP BY T.dmcdate;

DROP TABLE IF EXISTS TALL;
CREATE TEMP TABLE TALL (gid serial PRIMARY KEY, dmcdate date, geom geometry);
INSERT INTO TALL (dmcdate, geom)
 SELECT dmcdate, ST_Buffer(geom, 0) AS geom
 FROM new_polys
 WHERE ST_Area(geom) > 1000
 UNION (
  SELECT dmcdate, ST_Buffer(geom, 0) AS geom
  FROM t1
  WHERE ST_Area(geom) > 1000
  )
 UNION (
  SELECT dmcdate, ST_Buffer(geom, 0) AS geom
  FROM t2
  WHERE ST_Area(geom) > 1000
 );

DROP TABLE IF EXISTS T1;
DROP TABLE IF EXISTS T2;
DROP TABLE IF EXISTS table1;
ALTER TABLE TALL RENAME TO T1;
