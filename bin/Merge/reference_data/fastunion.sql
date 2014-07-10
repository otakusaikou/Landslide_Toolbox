/*Create sequence geo_id if not exists*/
DROP SEQUENCE IF EXISTS GEO_ID;
CREATE SEQUENCE GEO_ID START 1; 

/*create union of two tables*/
DROP TABLE IF EXISTS t1t2combo;
CREATE TEMP TABLE t1t2combo AS
SELECT project, dmcdate, ST_Union(ST_Buffer(geom, 0)) AS geom
FROM table1
GROUP BY project, dmcdate
UNION ALL
SELECT project, dmcdate, ST_Union(ST_Buffer(geom, 0)) AS geom
FROM table2
GROUP BY project, dmcdate;

/*create union of t1t2combo table*/
DROP TABLE IF EXISTS new_polys;
CREATE TEMP TABLE new_polys (id serial PRIMARY KEY, project text, dmcdate date, geom geometry);
INSERT INTO new_polys (project, dmcdate, geom)
SELECT T.project, T.dmcdate, (ST_Dump(ST_Union(geom))).geom AS geom
FROM t1t2combo, (SELECT project, dmcdate
                     FROM table1 
                     LIMIT 1) AS T
GROUP BY T.project, T.dmcdate;

DROP TABLE IF EXISTS TALL;
CREATE TEMP TABLE TALL (gid serial PRIMARY KEY, project text, dmcdate date, geom geometry);
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
