# -*- coding: utf-8 -*-
'''
Created on 2013/08/15
Updated on 2014/09/17
@author: Otakusaikou
'''
import os
import readimg
import shapefile
import glob
import getEO
import gdal
import sys
import numpy as np
from math import sin, cos, pi, atan2, sqrt, degrees
from gdalconst import GA_ReadOnly 


#---------img2map---------
def imgToWorld(imgX, imgY, z, m11, m12, m13, m21, m22, m23, m31, m32, m33, xL, yL, zL, focalLength):

    d = m13 * imgX + m23 * imgY + m33 * (-focalLength)
    a = m11 * imgX + m21 * imgY + m31 * (-focalLength)
    b = m12 * imgX + m22 * imgY + m32 * (-focalLength)
    x = xL + (z - zL) * a / d
    y = yL + (z - zL) * b / d
    return (x, y)

def readPoly(fileName, m11, m12, m13, m21, m22, m23, m31, m32, m33, xL, yL, zL, inputdir, outputdir, date, demlayer):
    #initial variable
    focalLength = 120.0
    dmcCols = 7680 / 8
    dmcRows = 13824 / 8
    #pixelSize = 12
    threshold = 0.2

    #minElev = 32.837001800537
    #maxElev = 2795.0
    meanElev = 525.0

    ioA0 = dmcCols / 2      # 3840 pixels
    ioA1 = 83.33333333333 / 8   # (7680/ 92.1600)  
    ioB0 = dmcRows / 2     # 6912 pixels        
    ioB2 = -83.33308216061 / 8  # (13824/165.8885)
    
    
    sf = shapefile.Reader(inputdir + "/" +fileName)
    shapes = sf.shapes()
    numShp = len(shapes)
    
    fields = sf.fields
    records = sf.records()
    fields.insert(2, ['DMCDate', 'D'])

    shpOut = shapefile.Writer(shapefile.POLYGON)
    
    for i in range(len(fields)):
        shpOut.field(*fields[i])
    
    #print "number of hsapes: ", numShp
    nShape = 0
    iter = 0
    #setup process bar
    sys.stdout.write("[%s]    0%%" % (" " * 65))
    sys.stdout.flush()
    sys.stdout.write("\b" * (72)) #return to start of line, after '['

    #read dem files
    gdal.AllRegister()

    ds = gdal.Open(demlayer, GA_ReadOnly)

    if ds is None:
        print 'Could not open image: %s' % img_name
        return False

    transform = ds.GetGeoTransform()
    metadatainf = [ds.RasterYSize, ds.RasterXSize, transform[0], transform[3], transform[1], transform[5]]

    band = ds.GetRasterBand(1)
    data = band.ReadAsArray(0, 0, ds.RasterXSize, ds.RasterYSize)

    
    for shp in shapes:
        parts = shp.parts
        numParts = len(parts)
        numPoints = len(shp.points)
        
        if int(65.0 * nShape / len(shapes)) > iter:
            iter = int(65.0 * nShape / len(shapes))
            sys.stdout.write("=" * iter + " " * (65 - iter) + "]  %3d%%" % int(iter * 100 / 65))
            sys.stdout.flush()
            sys.stdout.write("\b" * 72)
            

        partsOut = []
        
        for i in range(numParts):
            indexStart = parts[i]
            if i == numParts - 1:
                indexEnd = numPoints
            else:
                indexEnd = parts[i+1]
            
            polyOut = []
            for j in range(indexStart, indexEnd):
                count = 0
                z0 = meanElev
                imgX = (shp.points[j][0] - ioA0) / ioA1
                imgY = (dmcRows - shp.points[j][1] - ioB0) / ioB2
                
                while True:
                    x, y = imgToWorld(imgX, imgY, z0, m11, m12, m13, m21, m22, m23, m31, m32, m33, xL, yL, zL, focalLength)
                    z = readimg.getElev(data, metadatainf, x, y)
                    if abs(z - z0) <= threshold:
                        break
                    elif count == 20:
                        break
                    else:
                        z0 = z
                        count += 1
                 
                polyOut.append([x,y])
            
            partsOut.append(polyOut)

        shpOut.poly(partsOut)
        records[nShape].insert(1, date)
        rec = records[nShape]
        
        shpOut.record(*rec)
        nShape += 1
    #polygons whose attribute 'class_name' is 'landslide' will be saved to directory 'Landslide_97', this attribute is generated by ecognition
    shpOut.save(os.path.join(outputdir, "Landslide_97", fileName))
    sys.stdout.write("\b")
    sys.stdout.write("[" + "=" * 65 + "]  100%\n")
    
    
def img2map(shpList, inputdir, outputdir, demlayer, flag):
    result = ""
    
    get_landslide(inputdir, outputdir, flag)
    inputdir = os.path.join(outputdir, "Landslide")
        
    for shp in shpList:
        if shp[-3:] != "shp":
            continue
            
        baseName = shp[:-4]
        
        imageFile = baseName + ".tif"
        strEO = getEO.getEO(imageFile)
        s = strEO.split(",")

        xL = float(s[0])
        yL = float(s[1])
        zL = float(s[2])
        omega = float(s[3])
        phi = float(s[4])
        kappa = float(s[5])
        date = "".join([str(e) for e in s[6:9]])

        omega = omega * pi / 180.0
        phi = phi * pi / 180.0
        kappa = kappa * pi / 180.0        

        m11 = cos(phi) * cos(kappa)                 
        m12 = sin(omega) * sin(phi) * cos(kappa) + sin(kappa) * cos(omega)               
        m13 = -cos(omega) * sin(phi) * cos(kappa) + sin(kappa) * sin(omega)               
        m21 = -cos(phi) * sin(kappa)                
        m22 = -sin(omega) * sin(phi) * sin(kappa) + cos(kappa) * cos(omega)               
        m23 = cos(omega) * sin(phi) * sin(kappa) + cos(kappa) * sin(omega)              
        m31 = sin(phi)                              
        m32 = -sin(omega) * cos(phi)                
        m33 = cos(omega) * cos(phi)                 
        
        print "Processing coordinate transformation of shapefile '%s'..." % shp
        result += "Processing coordinate transformation of shapefile '%s'...\n" % shp
        readPoly(baseName, m11, m12, m13, m21, m22, m23, m31, m32, m33, xL, yL, zL, inputdir, outputdir, date, demlayer)
        
    return result
#---------img2map---------

#---------landslide_analysis---------

def getExtent(filename):
    data = gdal.Open(filename, gdal.gdalconst.GA_ReadOnly)
    geoTransform = data.GetGeoTransform()
    left = geoTransform[0]
    top = geoTransform[3]
    right = left + geoTransform[1] * data.RasterXSize
    bottom = top + geoTransform[5] * data.RasterYSize
    return left, bottom, right, top

#global variable
root = os.getcwd()
reference_data = os.path.join(root, "reference_data")
skipped_list = []

#check if shapefile extent contained in raster layer content
def shpInRaster(shp_name, rasterlayer):
    raster_left, raster_bottom, raster_right, raster_top = getExtent(rasterlayer)
    sf = shapefile.Reader(shp_name)
    left,bottom,right,top = sf.bbox
    del sf
    if left >= raster_left and bottom >= raster_bottom and right <= raster_right and top <= raster_top:
        return True
    return False


def landslide_analysis(conn, inputdir, outputdir, slopelayer, overwriteSlope, aspectlayer, overwriteAspect, host, port, database, user, password): #The variable inputdir here equals to outputdir in function img2map
    result = ""
    #get shapefile list
    os.chdir(inputdir)
    shp_list = glob.glob("*.shp")
    
    #check raster data 
    try:
        cur = conn.cursor()
        #import slope layer
        slopedir, slopefile = os.path.split(slopelayer)
        #check if slope raster table exists
        cur.execute("SELECT EXISTS(SELECT relname FROM pg_class WHERE relname='slopelayer')")
        exists = cur.fetchone()[0]
        if not exists or overwriteSlope:
                if overwriteSlope:
                    cur.execute("DROP TABLE IF EXISTS slopelayer;")
                    conn.commit()
                    
                os.chdir(slopedir)
                cmdstr = "raster2pgsql -s 3826 -I -C -M %s -F -t 300x300 slopelayer | psql -h %s -p %s -d %s -U %s" % (slopefile, host, port, database, user)
                print "Import raster data '%s' to database '%s' as table 'slopelayer'..." % (slopefile, database)
                result += "Import raster data '%s' to database '%s' as table 'slopelayer'...\n" % (slopefile, database)
                os.popen(cmdstr)
                os.chdir(inputdir)  #change directory to Toolbox\output\tmpdir

        #import aspect layer
        aspectdir, aspectfile = os.path.split(aspectlayer)
        #check if aspect raster table exists
        cur.execute("SELECT EXISTS(SELECT relname FROM pg_class WHERE relname='aspectlayer')")
        exists = cur.fetchone()[0]
        if not exists or overwriteAspect:
            if overwriteAspect:
                cur.execute("DROP TABLE IF EXISTS aspectlayer;")
                conn.commit()
            os.chdir(aspectdir)
            cmdstr = "raster2pgsql -s 3826 -I -C -M %s -F -t 300x300 aspectlayer | psql -h %s -p %s -d %s -U %s" % (aspectfile, host, port, database, user)
            print "Import raster data '%s' to database '%s' as table 'aspectlayer'..." % (aspectfile, database)
            result += "Import raster data '%s' to database '%s' as table 'aspectlayer'...\n" % (aspectfile, database)
            os.popen(cmdstr)
            os.chdir(inputdir)  #change directory to Toolbox\output\tmpdir
    except:
        conn.close()
        result += "Import raster data error.\n"
        return "Import raster data error.", result, True, True
        
    c = 0
    for shp_data in shp_list:
        c += 1
        
        #check if shapefile extent is contained in raster layer content
        if not shpInRaster(shp_data, slopelayer):
            print "Warning: shapefile '%s' has no overlapping area with  slope raster layer '%s'. Skip analysis of this shapefile." % (shp_data, slopefile)
            result += "Warning: shapefile '%s' has no overlapping area with slope raster layer '%s'. Skip analysis of this shapefile.\n" % (shp_data, slopefile)
            skipped_list.append(shp_data)
            continue
            
        if not shpInRaster(shp_data, aspectlayer):
            print "Warning: shapefile '%s' has no overlapping area with  aspect raster layer '%s'. Skip analysis of this shapefile." % (shp_data, aspectfile)
            result += "Warning: shapefile '%s' has no overlapping area with aspect raster layer '%s'. Skip analysis of this shapefile.\n" % (shp_data, aspectfile)
            skipped_list.append(shp_data)
            continue
        
        #clean old data
        cur.execute("DROP TABLE IF EXISTS tmp2;DROP TABLE IF EXISTS tmp;DROP TABLE IF EXISTS inputdata;DROP TABLE IF EXISTS riverside;DROP TABLE IF EXISTS vectordata;")
        conn.commit()
        
        #import new data
        try:
            cmdstr = "shp2pgsql -s 3826 -c -D -I -W big5 %s inputdata | psql -h %s -p %s -d %s -U %s" % (shp_data, host, port, database, user)
            print "Import shapefile '%s' to database '%s'..." % (shp_data, database)
            result += "Import shapefile '%s' to database '%s'...\n" % (shp_data, database)
            result += os.popen(cmdstr).read()
            
        except:
            conn.close()
            return "Import shapefile data error.", result, True, True
            
        #recalculate main direction
        try:
            print "Recalculate main direction and length width ratio of shapefile '%s'..." % shp_data
            result += "Recalculate main direction and length width ratio  of shapefile '%s'...\n" % shp_data
            #polygon to points
            sql = """
                    DROP TABLE IF EXISTS TP; 
                    CREATE TABLE TP AS
                    SELECT rid, (ST_PixelAsPoints(rast)).*
                    FROM (SELECT ST_AsRaster(geom, 5.0, 5.0, '8BUI') rast, gid rid
                    FROM inputdata) AS T1_R;"""
            cur.execute(sql) 
            conn.commit()
            
            #check number of point in every polygons, if less than 2 points, change the resolution to 1 meter
            sql = """
                    SELECT rid, COUNT(*)
                    FROM TP
                    GROUP BY rid
                    ORDER BY rid;"""
            cur.execute(sql) 
            ans = cur.fetchall()
            for i in range(len(ans)):
                row = ans[i]
                if row[1] <= 2:
                    sql = """
                            DELETE FROM TP
                            WHERE rid = %d;

                            INSERT INTO TP
                            SELECT rid, (ST_PixelAsPoints(rast)).*
                            FROM (SELECT ST_AsRaster(geom, 1.0, 1.0, '8BUI') rast, gid rid
                                  FROM inputdata
                                  WHERE gid = %d) AS T1_R;""" % (row[0], row[0])
                    cur.execute(sql)  
                    conn.commit()

            sql = """
                    SELECT rid, var_pop(ST_X(geom)), var_pop(-ST_Y(geom)), covar_pop(-ST_Y(geom), ST_X(geom))
                    FROM TP
                    GROUP BY rid
                    ORDER BY rid;"""
            cur.execute(sql) 
            ans = cur.fetchall()
            
            #calculate length/width ratio with eigenvalues
            length_width_ev = []
            main_direc = []
            sql = ""
            for i in range(len(ans)):
                var_cov = ans[i]
                varx = var_cov[1]
                vary = var_cov[2]
                varxy = var_cov[3]
                lambda1 = max(np.linalg.eig(np.array([[var_cov[1], var_cov[3]], [var_cov[3], var_cov[2]]]))[0])
                lambda2 = min(np.linalg.eig(np.array([[var_cov[1], var_cov[3]], [var_cov[3], var_cov[2]]]))[0])
                theta = atan2(varxy, lambda1 - vary) + 0.5 * pi
                main_direc.append(degrees(theta))
                #rotate polygons
                sql += "UPDATE TP SET geom = ST_Rotate(geom, %f) WHERE rid = %d;\n" % (theta, var_cov[0])

                #let lambda2 be 1 if it's value is too close to zero
                if not round(lambda2, 6):
                    lambda2 = 1.0

                length_width_ev.append(sqrt(lambda1/lambda2))
                

            cur.execute(sql)
            conn.commit()
            sql = """
                    SELECT MAX(ST_X(geom)), MIN(ST_X(geom)), MAX(ST_Y(geom)), MIN(ST_Y(geom))
                    FROM TP
                    GROUP BY rid
                    ORDER BY rid;"""
                    
            cur.execute(sql) 
            ans2 = cur.fetchall()
            length_width_bb = []
            sql = ""
            for i in range(len(ans)):
                #calculate length/width ratio with bounding box
                xmax = ans2[i][0]
                xmin = ans2[i][1]
                ymax = ans2[i][2]
                ymin = ans2[i][3]
                length_width = [(ymax - ymin), (xmax - xmin)]
                length_width_bb.append(max(length_width) / min(length_width))
                
                length_width = min(length_width_bb[i], length_width_ev[i])
                sql += ("UPDATE inputdata SET (Main_direc, LengthWidt) = (%f, %f) WHERE gid = %s;\n" % (main_direc[i], length_width, ans[i][0]))
            cur.execute(sql + "DROP TABLE IF EXISTS TP;\n")
            conn.commit()
        except:
            #delete template tables
            conn.rollback()
            
            cur.execute("DROP TABLE IF EXISTS tmp2;DROP TABLE IF EXISTS tmp;DROP TABLE IF EXISTS inputdata;DROP TABLE IF EXISTS riverside;DROP TABLE IF EXISTS vectordata;")
            conn.commit()
            conn.close()
            return "Error in recalculation of main direction and length width ratio. Shapefile name is '%s'." % shp_data, result, True, True
            
        #Execute zonal statistic analysis
        try:
            print "Execute zonal statistic analysis..."
            result += "Execute zonal statistic analysis...\n"
            cur.execute(open(os.path.join(reference_data, "zonalAnalysis.sql"), "r").read())
            conn.commit()
        except:
            conn.rollback()
            cur.execute("DROP TABLE IF EXISTS tmp2;DROP TABLE IF EXISTS tmp;DROP TABLE IF EXISTS inputdata;DROP TABLE IF EXISTS riverside;DROP TABLE IF EXISTS vectordata;")
            conn.commit()
            conn.close()
            result += "Zonal Statistic analysis error.\n"
            return "Zonal Statistic analysis error.", result, True, True
        
        
        cur.execute("SELECT DISTINCT COUNT(shp_id) FROM riverside")
        nrow_riverside = int(cur.fetchall()[0][0])
        cur.execute("SELECT DISTINCT COUNT(shp_id) FROM vectordata")
        nrow_landslide = int(cur.fetchall()[0][0])
        
        #export data
        try:
            #for riverside
            if nrow_riverside != 0:
                os.chdir(os.path.join(outputdir, "RiverSide"))  #change directory to Toolbox\output\RiverSide
                cmdstr = 'pgsql2shp -f %s -h %s -u %s -p %s %s "SELECT * FROM riverside"' % (shp_data.replace("~", "_"), host, user, port, database)
                print "Export riverside of shapefile '%s'..." % shp_data.replace("~", "_")
                result += "Export riverside of shapefile '%s'...\n" % shp_data.replace("~", "_")
                result += os.popen(cmdstr).read()
                os.chdir(inputdir)  #change directory to Toolbox\output\tmpdir
            else:
                 print "Shapefile '%s' has no riverside." % shp_data
                 result += "Shapefile '%s' has no riverside.\n" % shp_data
            
            #for landslide
            if nrow_landslide != 0:
                os.chdir(os.path.join(outputdir, "Landslide"))  #change directory to Toolbox\output\Landslide
                cmdstr = 'pgsql2shp -f %s -h %s -u %s -p %s %s "SELECT * FROM vectordata"' % (shp_data.replace("~", "_"), host, user, port, database)
                print "Export landslide of shapefile '%s'..." % shp_data.replace("~", "_")
                result += "Export landslide of shapefile '%s'...\n" % shp_data.replace("~", "_")
                result += os.popen(cmdstr).read()
                os.chdir(inputdir)  #change directory to Toolbox\output\tmpdir
            else:
                print "Shapefile '%s' has no landslide." % shp_data
                result += "Shapefile '%s' has no landslide.\n" % shp_data
                if shp_data not in skipped_list:
                    skipped_list.append(shp_data)
            
        except:
            conn.close()
            result += "Export data error.\n"
            return "Export data error.", result, True, True
            
        #clean old data
        cur.execute("DROP TABLE IF EXISTS tmp2;DROP TABLE IF EXISTS tmp;DROP TABLE IF EXISTS inputdata;DROP TABLE IF EXISTS riverside;DROP TABLE IF EXISTS vectordata;")
        conn.commit()

        print "Filtering of shapefile '%s' succeed!....(%d / %d)" % (shp_data, c, len(shp_list))
        result += "Filtering of shapefile '%s' succeed!....(%d / %d)\n" % (shp_data, c, len(shp_list))
    
    
    conn.close()
    result += "Landslide analysis succeed.\n"
    return "Landslide analysis succeed.\n", result, True, False

    
#---------landslide_analysis---------
#---------extract_origin---------
def get_landslide(inputdir, outputdir, flag):
    #this function split landslide and unclassified polygon into two shapefiles
    root = os.getcwd()
    os.chdir(os.path.join(inputdir))
    shp_list = glob.glob("*.shp")
    os.chdir(root)
    for imageFile in shp_list:
        if imageFile in skipped_list:
            continue

        result = ""

        sf = shapefile.Reader(os.path.join(inputdir, imageFile))
        shapes = sf.shapes()

        fields = sf.fields
        records = sf.records()
        #flag means that program will do both coordinate transformation and zonal statistic analysis
        if flag:
            print "Adding field 'Shp_id' to shapefiles '%s'..." % imageFile
            result += "Adding field 'Shp_id' to shapefiles '%s'...\n" % imageFile
            fields.insert(2, ['Shp_id', 'N', 8, 0])
            fields.insert(3, ['Main_direc', 'N', 32, 10])
            fields.insert(3, ['LengthWidt', 'N', 32, 10])

        allShp = shapefile.Writer(shapefile.POLYGON)
        landslideShp = shapefile.Writer(shapefile.POLYGON)
        
        for field in fields:
            allShp.field(*field)
            landslideShp.field(*field)
    
        nShape = 0
        for shp in shapes:
            parts = shp.parts
            numParts = len(parts)
            numPoints = len(shp.points)
            partsOut = []
    
            for i in range(numParts):
                indexStart = parts[i]
                if i == numParts - 1:
                    indexEnd = numPoints
                else:
                    indexEnd = parts[i+1]
            
                polyOut = []
                for j in range(indexStart, indexEnd):
                    x = shp.points[j][0]
                    y = shp.points[j][1]
                    polyOut.append([x,y])

                partsOut.append(polyOut)
        
            allShp.poly(partsOut)
            #flag means that program will do both coordinate transformation and zonal statistic analysis
            if flag:
                records[nShape].insert(1, nShape + 1)
                records[nShape].insert(2, 0)
                records[nShape].insert(2, 0)
                
            allShp.record(*records[nShape])
            if records[nShape][0] == "landslide":
                landslideShp.poly(partsOut)
                landslideShp.record(*records[nShape])
            nShape += 1

        #save two shapefile, one has all polygon, and the other has only polygon whose attribute 'class_name' is 'landslide', this attribute is modified by user manually
        #both two shapefile are in image coordinate system
        allShp.save(os.path.join(outputdir, "AllPolygon", imageFile))
        landslideShp.save(os.path.join(outputdir, "Landslide", imageFile))

def extract_origin(inputdir, outputdir):
    #this function find landslide in TWD97 CRS, and link it to image CRS, finally extract it out
    count = 1
    origin = os.getcwd()
    os.chdir(inputdir)
    shp_list = glob.glob("*.shp")
    os.chdir(origin)
    
    result = ""
    
    for shpfile in shp_list:
        if shpfile in skipped_list:
            continue
        print "Transform projected polygon of shapefile '%s' to original image CRS...(%d / %d)" % (shpfile.replace("~", "_"), count, len(shp_list))
        result += "Transform projected polygon of shapefile '%s' to original image CRS...(%d / %d)\n" % (shpfile.replace("~", "_"), count, len(shp_list))
        # Read corrected landslides
        sfread = shapefile.Reader(os.path.join(outputdir, "Landslide", shpfile.replace("~", "_")))
        shapes = sfread.shapes()

        records = sfread.records()
        
        nShape = 0
        output_list = []
        for shp in shapes:
            output_list.append(records[nShape][0])
            nShape += 1
        
        # Read  original shapefile have field 'Shp_id'
        shpIn = shapefile.Reader(os.path.join(outputdir, "tmpdir", "AllPolygon", shpfile))
        
        shapes2 = shpIn.shapes()
        records2 = shpIn.records()
        nShape = 0
        allShp = shapefile.Writer(shapefile.POLYGON)
        landslideShp = shapefile.Writer(shapefile.POLYGON)
        
        for field in shpIn.fields:
            allShp.field(*field)
            landslideShp.field(*field)
        
        for shp in shapes2:
            parts = shp.parts
            numParts = len(parts)
            numPoints = len(shp.points)    
            partsOut = []
    
            for i in range(numParts):
                indexStart = parts[i]
                if i == numParts - 1:
                    indexEnd = numPoints
                else:
                        indexEnd = parts[i+1]
                polyOut = []
                for j in range(indexStart, indexEnd):
                    x = shp.points[j][0]
                    y = shp.points[j][1]
                    polyOut.append([x,y])

                partsOut.append(polyOut)
                
            # Filter original shapefile with field 'Shp_id'
            if records2[nShape][1] in output_list:
                landslideShp.poly(partsOut)
                records2[nShape][0] = "landslide"
                landslideShp.record(*records2[nShape])
            else:
                records2[nShape][0] = "unclassified"
            
            allShp.poly(partsOut)
            allShp.record(*records2[nShape])
                
            nShape += 1
        
        #save two shapefile, one has all polygon, and the other has only polygon whose 'class_name' is 'landslide'
        #both two shapefile are in image coordinate system
        allShp.save(os.path.join(os.path.join(outputdir, "Origin", "AllPolygon", shpfile)))
        landslideShp.save(os.path.join(os.path.join(outputdir, "Origin", "Landslide", shpfile)))
        print "Transformation of shapefile '%s' succeed!....(%d / %d)" % (shpfile, count, len(shp_list))
        result += "Transformation of shapefile '%s' succeed!....(%d / %d)\n" % (shpfile, count, len(shp_list))
        count += 1
    if len(skipped_list) != 0:
        result += "Because having no landslide or riverside, the following %s shapefile(s) have no output result: %s\n" % (len(skipped_list), ", ".join(skipped_list))
        print "Because having no landslide or riverside, the following %s shapefile(s) have no output result: %s" % (len(skipped_list), ", ".join(skipped_list))
    result += "The filtering of all original shapefiles has finished!\n"
    print "The filtering of all original shapefiles has finished!"
    global skipped_list 
    skipped_list = []

    return "The filtering of all original shapefiles has finished!", result, True, False
    
def main():
    return 0
    
if __name__ == "__main__":
    main()
