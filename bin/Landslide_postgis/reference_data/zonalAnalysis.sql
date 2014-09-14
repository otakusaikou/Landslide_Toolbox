UPDATE inputdata
SET geom = ST_Multi(ST_Buffer(geom, 0.0))
WHERE NOT ST_IsValid(geom);

DROP TABLE IF EXISTS tmp2;
DROP TABLE IF EXISTS tmp;

CREATE TEMP TABLE tmp AS 
 SELECT inputdata.*, AVG((ST_SummaryStats(ST_Clip(rast,1,geom, True))).mean) AS slope_mean
 FROM slopelayer, inputdata
 WHERE ST_Intersects(geom, rast) 
GROUP BY gid
HAVING AVG((ST_SummaryStats(ST_Clip(rast,1,geom, True))).mean) > 17;


CREATE TEMP TABLE tmp2 AS 
SELECT gid, 
	shp_id, 
	dmcdate,
	lengthwidt, 
	main_direc, 
	slope_mean,
	--CASE WHEN ABS(AVG((ST_SummaryStats(ST_Clip(rast,1,geom, True))).mean) - main_direc) > 180
		--THEN (360 - ABS(AVG((ST_SummaryStats(ST_Clip(rast,1,geom, True))).mean) - main_direc))
		--ELSE ABS(AVG((ST_SummaryStats(ST_Clip(rast,1,geom, True))).mean) - main_direc)
	--END AS collapse,
	ABS(main_direc - ABS(180 - AVG((ST_SummaryStats(ST_Clip(rast,1,geom, True))).mean))) collapse,
	AVG((ST_SummaryStats(ST_Clip(rast,1,geom, True))).mean) AS aspect_mean,
	geom
 FROM aspectlayer, tmp
 WHERE ST_Intersects(geom, rast)
GROUP BY gid, shp_id, dmcdate, lengthwidt, main_direc, slope_mean, geom;

CREATE TABLE RiverSide AS
 SELECT *
 FROM tmp2
 --WHERE lengthwidt >= 3 AND collapse <= 30;
 WHERE lengthwidt >= 3 AND (collapse >= 50 AND collapse <= 130);

CREATE TABLE VectorData AS
 SELECT *
 FROM tmp2 AS T
 WHERE T.gid NOT IN (SELECT gid
            FROM RiverSide);
