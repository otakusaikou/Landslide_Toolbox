DROP SEQUENCE IF EXISTS GEOM_ID;
CREATE SEQUENCE GEOM_ID;
ALTER TABLE merged ADD COLUMN GEOM_ID bigint;
UPDATE merged SET GEOM_ID = nextval('GEOM_ID');

/*create centorid point of merged table*/
DROP TABLE IF EXISTS merged_pt;
CREATE TEMP TABLE merged_pt AS
SELECT GEOM_ID, ST_PointOnSurface(geom) AS geom
FROM merged;

/*Working Circle*/
DROP TABLE IF EXISTS MP_WC;
CREATE TEMP TABLE MP_WC AS
SELECT MP.*, WC.Working_id, WC.Working_ci
FROM merged_pt MP LEFT JOIN Working_circle WC ON ST_Intersects(MP.geom, WC.geom);

UPDATE MP_WC SET Working_id = '_', Working_ci = '_' WHERE Working_ci IS NULL;

/*Forest_district*/
DROP TABLE IF EXISTS MP_WC_F;
CREATE TEMP TABLE MP_WC_F AS
SELECT MP_WC.*, F.Forest_id, F.Forest_dis
FROM MP_WC LEFT JOIN Forest_district F ON ST_Intersects(MP_WC.geom, F.geom);

UPDATE MP_WC_F SET Forest_id = '_', Forest_dis = '_' WHERE Forest_dis IS NULL;

/*County*/
DROP TABLE IF EXISTS MP_WC_F_C;
CREATE TEMP TABLE MP_WC_F_C AS
SELECT MP_WC_F.*, C.County_id, C.County
FROM MP_WC_F LEFT JOIN County C ON ST_Intersects(MP_WC_F.geom, C.geom);

UPDATE MP_WC_F_C SET County_id = '_', County = '_' WHERE County IS NULL;

/*Township*/
DROP TABLE IF EXISTS MP_WC_F_C_T;
CREATE TEMP TABLE MP_WC_F_C_T AS
SELECT MP_WC_F_C.*, T.Town_id, T.Township
FROM MP_WC_F_C LEFT JOIN Township T ON ST_Intersects(MP_WC_F_C.geom, T.geom);

UPDATE MP_WC_F_C_T SET Town_id = '_', Township = '_' WHERE Township IS NULL;

/*Reservoir*/
DROP TABLE IF EXISTS MP_WC_F_C_T_R;
CREATE TEMP TABLE MP_WC_F_C_T_R AS
SELECT MP_WC_F_C_T.*, R.Reserv_id, R.Reservoir
FROM MP_WC_F_C_T LEFT JOIN Reservoir R ON ST_Intersects(MP_WC_F_C_T.geom, R.geom);

UPDATE MP_WC_F_C_T_R SET Reserv_id = '_', Reservoir = '_' WHERE Reservoir IS NULL;

/*Watershed*/
DROP TABLE IF EXISTS MP_WC_F_C_T_R_W;
CREATE TEMP TABLE MP_WC_F_C_T_R_W AS
SELECT MP_WC_F_C_T_R.*, W.Watersh_id, W.Watershed
FROM MP_WC_F_C_T_R LEFT JOIN Watershed W ON ST_Intersects(MP_WC_F_C_T_R.geom, W.geom);

UPDATE MP_WC_F_C_T_R_W SET Watersh_id = '_', Watershed = '_' WHERE Watershed IS NULL;

/*Basin*/
DROP TABLE IF EXISTS MP_WC_F_C_T_R_W_B;
CREATE TEMP TABLE MP_WC_F_C_T_R_W_B AS
SELECT MP_WC_F_C_T_R_W.*, B.Basin_id, B.Basin
FROM MP_WC_F_C_T_R_W LEFT JOIN Basin B ON ST_Intersects(MP_WC_F_C_T_R_W.geom, B.geom);

UPDATE MP_WC_F_C_T_R_W_B SET Basin_id = '_', Basin = '_' WHERE Basin IS NULL;

/*Join merged and County*/
DROP TABLE IF EXISTS merged2;
CREATE TABLE merged2 AS
SELECT M.geom, M.GEOM_ID, M.dmcdate, Working_id, Working_ci, Forest_id, Forest_dis, County_id, County, Town_id, Township, Reserv_id, Reservoir, Watersh_id, Watershed, Basin_id, Basin, ST_Area(M.geom) AS Area, ST_X(ST_Centroid(M.geom)) AS Centroid_X, ST_Y(ST_Centroid(M.geom)) AS Centroid_Y
FROM MP_WC_F_C_T_R_W_B, merged M
WHERE M.GEOM_ID = MP_WC_F_C_T_R_W_B.GEOM_ID
ORDER BY M.GEOM_ID;
