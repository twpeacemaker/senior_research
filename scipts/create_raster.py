import constants
import arcpy

path = r'C:\Users\Thomas Peacemaker\Desktop\Senior_Research\data\land_cover\nlcd_2011_landcover_2011_edition_2014_10_10\nlcd_2011_clip.img'
raster = arcpy.Raster(path)
raster_array = arcpy.RasterToNumPyArray(raster)
lowerLeft = arcpy.Point(raster.extent.XMin,raster.extent.YMin)
cellSize = raster.meanCellWidth

(height, width) = raster_array.shape
row_bounds = (constants.BUFFER, width - constants.BUFFER)
col_bounds = (constants.BUFFER, height - constants.BUFFER)
(row_start, row_end) = row_bounds
(col_start, col_end) = col_bounds
row_end = 907


new_dict = {}
for key, value in constants.LAND_USE_CLASSES.iteritems():
    new = value.replace(" ","").replace("/","").replace(",","")
    new_dict[new] = key


path = r"C:\Users\Thomas Peacemaker\Desktop\Senior_Research\weka\predicted_set"
stream = open(path, 'r') # opens the file stream, clears the file

counter = 0
str = "=== Predictions on user test set ==="
str_len = len(str)
line = stream.readline()
while line[0:str_len] != str:
    line = stream.readline()

line = stream.readline()
line = stream.readline()
line = stream.readline()

stop = 0
for row in range(row_start, row_end):
    for col in range(col_start, col_end, 1):
        #if(not(stop)):
        land_use_class = line.split(":")[2].split(" ")[0]
        int_val = new_dict[land_use_class]
        if(int_val > 20 and int_val < 25):
            raster_array[row, col] = int_val
        line = stream.readline()
        if(line == "\n"):
            stop = 1

newRaster = arcpy.NumPyArrayToRaster(raster_array, lowerLeft, cellSize, value_to_nodata=0)
file_name = r"C:\Users\Thomas Peacemaker\Desktop\Senior_Research\data\land_cover\predicted\2016_predicted_2.tif"
color_map = r"C:\Users\Thomas Peacemaker\Desktop\Senior_Research\data\land_cover\nlcd_2011_landcover_2011_edition_2014_10_10\color_map.clr"
newRaster.save(file_name)
arcpy.AddColormap_management(file_name, "#", color_map)
