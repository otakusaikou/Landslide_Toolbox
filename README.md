Landslide_Toolbox
==========

Description
----------
###Author: Otakusaikou  
###Created: 2014/05/28  
###This program provides the following functions:  
+ 1.  Upload: Upload shapefile to database as table.  
+ 2.  Export: Export geometry table as shapefile.  
+ 3.  Analysis: Transform coordinates from image coordinates to world     coordinates(TWD97), filtering error with DEM, Slope and Aspect.  
+ 4.  Merge: Merge and dissolve shapefiles.  
+ 5.  Zonal Split: Identity analysis with input layers.  

***
Update Log
----------
####2014-05-28 23:41
+ 1.  Zonal Split: Fix error in uploding identity layers to database.  
+ 2.  Config directory error fixed.  
+ 3.  Default config settings modified.  

*** 
####2014-05-29 18:19
+ 1.  Add three file dialog to specify dem, slope and aspect raster data.
+ 2.  Bug in making new I/O directories fixed.

***
####2014-05-29 20:40
+ 1.  Add function to check if shapefile extent is contained in raster layer, making program to skip shapefiles sitting outside of raster layers.

***
####2014-06-04 12:30
+ 1.  Analysis: Add two check button to check whether to overwrite existing raster table in database.   

***
####2014-06-05 17:04
+ 1.  Zonal Split: Modify sql file, making output result have identity layer id.  

***
####2014-06-07 17:30
+ 1.  Zonal Split: Modify sql file, replace all '<NONE>' and NULL values with '_' in output result.  

***
####2014-06-09 17:05
+ 1.  Analysis: Change rasterizing pixel size from 1mx1m to 5mx5m.  

***
####2014-06-13 16:48
+ 1.  Analysis: Delete meaningless statement.  
+ 2.  Export: Add support of database having new structure.Disable function of split query result with date/year column.  

***
####2014-06-13 17:08
+ 1.  Export: Bug in connecting to database fixed.  

***
####2014-06-21 01:05
+ 1.  Add GUI of config settings for all programs.  

***
####2014-06-27 10:36
+ 1.  Analysis:
  + Ignore unused attributes like brightness and ndvi.  
  + Add a new check button. Let user to choose whether to do all analysis process or just do coordinate transformation.  
  + Delete unused commands.  

***
####2014-06-28 03:20
+ 1.  Analysis: Add message for skipped shapefile names which have no landslide and riverside.  
+ 2.  Merge: Algorithm modified for new database structure. Remove handling for image name.  
+ 3.  Zonal: Algorithm modified for new database structure. Remove handling for image name.  
+ 4.  Export: Add support of database having new structure.  

***
####2014-06-28 17:55
+ 1.  Merge: Add fast merge method.  

***
####2014-06-28 18:08
+ 1.  Export: Bug in config setting panel fixed..  

***
####2014-06-29 01:35
+ 1.  Merge: Algorithm modified. The program will automatically check the number of intersection polygons. If union table has more than 100 intersection polygons with new shapefile, dissolve these intersection polygons, otherwise get the union of union table and new shapefile directly.  

***
####2014-06-30 10:15
+ 1.  All: Add support for remote processing.  
+ 2.  Analysis: Bug in connection of database fixed.  
+ 3.  Export: Bug in output table name fixed.  

***
####2014-06-30 19:45
+ 1.  Merged: Delete unused commands.  

***
####2014-07-03 12:12
+ 1.  Merged: Apply new merge algorithm.

***
####2014-07-04 04:35
+ 1.  Analysis:   
  + Output content of shapefile attribute 'project' modified.   
  + Bug in loading raster data to remote database fixed.  

***
####2014-07-04 14:45
+ 1.  All: Add about dialog.  

***
####2014-07-05 01:35
+ 1.  All: Add support for independent execution.

***
####2014-07-06 04:28
+ 1.  All: Add support for Linux.

***
####2014-07-06 21:58
+ 1.  Upload: Bug in file encoding fixed.

***
####2014-07-07 00:10
+ 1.  Upload: Change option "Existing Table" to "Use Big5 Encoding".

***
####2014-07-07 00:49
+ 1.  Export: Bug in clean button fixed.

***
####2014-07-07 21:25
+ 1.  Toolbox: Bug in loading button icon fixed.
+ 2.  Merge: Algorithm modified. 
+ 3.  All: Add compelete credit information.

***
####2014-07-08 21:25
+ 1.  All: Bug in resetting item values fixed.  

***
####2014-07-09 15:02
+ 1.  Export: Bug in export filename fixed. 

***
####2014-07-10 09:50 
+ 1.  Merge: Algorithm modified. Make the process simpler and more correct.

***
####2014-07-10 10:36 
+ 1.  Merge: Let the ouput polygon area greater than 1000 square meters.

***
####2014-07-22 22:26 
+ 1.  All: Add port entry in config setting panel.
+ 2.  Export: Enable capibility of splitting shapefile by date attribute. 

***
####2014-07-23 00:07 
+ 1.  Export: Bug in exporting data fixed.  

***
####2014-08-30 11:14 
+ 1.  Zonal Split: Add function for generating statistic report after analysis is done.   

***
####2014-09-14 11:28
+ 1. Export, Analysis, Merge, Zonal Split: Delete attribute 'project'.  
+ 2. Toolbox: Add message dialog to prompt users if they trying to terminate the toolbox while other subprocess still running.  
+ 3. All: Logo in help dialog has been changed.

***
####2014-09-15 22:12
+ 1. Toolbox: Bug in message dialog fixed.  
+ 2. All: Version Up.  
