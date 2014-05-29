import os, gdal, sys

def getElev(data, metadatainf, x, y):
    rows = metadatainf[0] 
    cols = metadatainf[1] 
    xOrigin = metadatainf[2] 
    yOrigin = metadatainf[3] 
    pixelWidth = metadatainf[4] 
    pixelHeight = metadatainf[5] 

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
