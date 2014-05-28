import os, gdal

from gdalconst import *

#dir_name = "f:/gdal"
#dir_name = "J:/eCoginition/shp/GDAL/gdal"
dir_name = os.getcwd()

#img_name = 'Chi-Shan_9m_R_0823.img'
img_name = 'Chi-Shan_9m_R_0823.img'
#img_name = 'tw20-97.lan'

gdal.AllRegister()

ds = gdal.Open(os.path.join(dir_name, "reference_data", img_name), GA_ReadOnly)

if ds is None:
    print 'Could not open image: %s' % img_name
    sys.exit(1)
    
rows = ds.RasterYSize
cols = ds.RasterXSize
bands = ds.RasterCount

transform = ds.GetGeoTransform()
xOrigin = transform[0]
yOrigin = transform[3]
pixelWidth = transform[1]
pixelHeight = transform[5]

print 'rows = ', rows
print 'cols = ', cols
print 'bands = ', bands
print 'xOrigin = ', xOrigin
print 'yOrigin = ', yOrigin
print 'pixelWidth = ', pixelWidth
print 'pixelHeight = ', pixelHeight

band = ds.GetRasterBand(1)
data = band.ReadAsArray(0, 0, cols, rows)

#224,525.148  2,581,643.814  Stretched value	149  Pixel value	1138.619995
'''
x = int((224525.148 - xOrigin) / pixelWidth)
y = int((2581643.814 - yOrigin) / pixelHeight)
data = band.ReadAsArray(x, y, 1, 1)
print '(%d, %d) = %f' % (x, y, data)

data = band.ReadAsArray(0, 0, cols, rows)

print 'len = ', len(data)

print '(%d, %d) = %f' % (y, x, data[y,x])
def getElev(x, y):
    xOffset = int((x - xOrigin) / pixelWidth)
    yOffset = int((y - yOrigin) / pixelHeight)
    return data[yOffset,xOffset]
'''
    

def getElev(x, y):
    xOffset = int((x - xOrigin) / pixelWidth)
    yOffset = int((y - yOrigin) / pixelHeight)
    
    x1 = xOrigin + xOffset * pixelWidth
    y1 = yOrigin + yOffset * pixelHeight
    z1 = data[yOffset, xOffset]
    p = [[x1, y1, z1]]
    
    if xOffset == cols - 1:
        if yOffset == rows - 1:
            return z1
        else:
            x2 = x1
            y2 = y1 + pixelHeight
            z2 = data[yOffset + 1, xOffset]
            p.append([x2, y2, z2])
    else:
        x2 = x1 + pixelWidth
        y2 = y1
        z2 = data[yOffset, xOffset + 1]
        p.append([x2, y2, z2])
        
        if yOffset != rows - 1:
            x3 = x1
            y3 = y1 + pixelHeight
            z3 = data[yOffset + 1, xOffset]
            p.append([x3, y3, z3])
            
            x4 = x2
            y4 = y3
            z4 = data[yOffset + 1, xOffset + 1]
            p.append([x4, y4, z4])
    
    weights = []
    res = 0
    for i in range(len(p)):
        w = 1 / ((p[i][0] - x) ** 2 + (p[i][1] - y) ** 2)
        res += w * p[i][2]
        weights.append(w)
        
    return res / sum(weights)
