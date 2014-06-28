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
