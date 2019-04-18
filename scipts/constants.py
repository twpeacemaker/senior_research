import arcpy


PATH = r"D:"
# dataset = PATH + r'\Senior_Research\land_cover\nlcd_2001_landcover_2011_edition_2014_10_10\nlcd_2001_clip.img'
# SPATIAL_REFERENCE = arcpy.Describe(dataset).spatialReference




LAND_USE_CLASSES = {
    11 : 'Open Water',
    12 : 'Perennial Ice/Snow',
    21 : 'Developed, Open Space',
    22 : 'Developed, Low Intensity',
    23 : 'Developed, Medium Intensity',
    24 : 'Developed, High Intensity',
    31 : 'Barren Land (Rock/Sand/Clay)',
    41 : 'Deciduous Forest',
    42 : 'Deciduous Forest',
    43 : 'Mixed Forest',
    51 : 'Dwarf Scrub',
    52 : 'Shrub/Scrub',
    71 : 'Grassland/Herbaceous',
    72 : 'Sedge/Herbaceous',
    73 : 'Lichens',
    74 : 'Moss',
    81 : 'Pasture/Hay',
    82 : 'Cultivated Crops',
    90 : 'Woody Wetlands',
    95 : 'Emergent Herbaceous Wetlands',
}

LAND_USE_MAX = 95
LAND_USE_MIN = 11

GREEN_ARRAY = [41, 42, 43, 51, 52, 71, 72, 81, 82]
VAC_ATTR_ARRAY = ["VAC", "AVG_VAC", "VAC_3", "VAC_3TO6", "VAC_6TO12", "VAC_12TO24", "VAC_24TO36", "VAC_36"]

MOORE_SIZE = 7
BUFFER = 108 + MOORE_SIZE

SEPARATOR = "|"

VAC_PATH = r"D:\Senior_Research\data\usps_data\2011_USPS_raster_data.gdb"
DIST_PATH = r"D:\Senior_Research\data\transportation\DistanceRasters.mdb"




