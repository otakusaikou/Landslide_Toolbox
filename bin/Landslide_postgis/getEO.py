import os
import glob

def readSEL(selFile):
    print "Read sel file '%s'" % os.path.basename(selFile)
    fin = open(selFile)

    # read the first two lines, which are the header part
    line = fin.readline()
    line = fin.readline()

    # build a dictionary for all the photos
    photoDict = dict()
    for line in fin:
        line.strip()
        
        name = line[0:10]
        photoId = line[11:15]
        #for date
        if line[85:87] != "20":
            date = [int(line[85:87]) + 1911, line[87:89], line[89:91]]
        else:
            date = [line[85:89], line[89:91], line[91:93]]
        imageName = name + '~' + photoId + '_hr4.tif'
        
        x = line[17:28]
        y = line[28:40]
        z = line[73:81]
        
        omega = line[136:147]
        phi = line[147:159]
        kappa = line[159:171]
        
        photoDict[imageName] =  x + "," + y + "," + z + "," + omega + "," + phi + "," + kappa + "," + str(date[0]) + "," + date[1] + "," + date[2]
        #print imageName, x, y, z, omega, phi, kappa
    
    fin.close()
    return photoDict
    
def getEO(imageName):
    year = imageName[0:2]
    
    selFileList = glob.glob("reference_data\\*.sel")
    try:
        photoDict = readSEL(os.path.join(os.getcwd(), "reference_data", "new20%sall.sel" % year))
        return photoDict[imageName]
    except:
        return ""
  

if __name__ == "__main__":
    tifList = glob.glob("*.tif")

    for t in tifList:
        strEO = getEO(t)
        print t, ",", strEO
         