import ARFFCreator

LAND_USE_CLASSES = [ 'Open Water', 'Perennial Ice/Snow', 'Developed, Open Space', 'Developed, Low Intensity',
                     'Developed, Medium Intensity', 'Developed, High Intensity', 'Barren Land (Rock/Sand/Clay)',
                     'Deciduous Forest', 'Mixed Forest', 'Dwarf Scrub', 'Shrub/Scrub',
                     'Grassland/Herbaceous', 'Sedge/Herbaceous', 'Lichens', 'Moss', 'Pasture/Hay', 'Cultivated Crops',
                     'Woody Wetlands', 'Emergent Herbaceous Wetlands']

# ATTRS = [ "d_categoryI", "d_categoryII", "d_city", "d_highway", "d_lake_pond", "d_main_roads", "d_rail", "d_ramps",
#           "d_stream_river", "elevation","prev_LU_class", "mf_LU_class", "smf_LU_class","VAC","AVG_VAC","VAC_3","VAC_3TO6","VAC_6TO12",
#           "VAC_12TO24","VAC_24TO36", "VAC_36", "LU_class" ]

ATTRS = [ "d_categoryI", "d_categoryII", "d_city", "d_highway", "d_lake_pond", "d_main_roads", "d_rail", "d_ramps",
          "d_stream_river", "elevation","prev_LU_class", "mf_LU_class", "smf_LU_class","VAC","AVG_VAC","VAC_3","VAC_3TO6", "LU_class" ]

NOMINAL_CLASS_INDEXS = [10,11,12,len(ATTRS) - 1]


arff = ARFFCreator.ARFFCreator("D:\Senior_Research\weka\weka-LU-Prject.arff", 'Land-Use-Proj-Future')

for i in range(0, len(LAND_USE_CLASSES)):
    LAND_USE_CLASSES[i] = LAND_USE_CLASSES[i].replace(",", "").replace("/", "").replace(" ", "")


for i in range(0, len(ATTRS)):
    if(i in NOMINAL_CLASS_INDEXS):
        arff.add_nominal_attr(ATTRS[i], LAND_USE_CLASSES)
    else:
        arff.add_numeric_attr(ATTRS[i])
arff.add_header()

# print (arff.attr_order)
count = 0
# for row in range(0, 25):
#     print("file start: " + str(row))
#     path = r"E:\Senior_Research\instances\computer"
#     stream = open(path + str(row), 'r') # opens the file stream, clears the file
#
#     line = stream.readline()
#
path = r"D:\Senior_Research\instances\test"
stream = open(path, 'r') # opens the file stream, clears the file
line = stream.readline()
while line:
    instances = line[0:-1].split("|")
    add_dict = {}
    for i in range(0, len(instances)):
        if len(ATTRS) != len(ATTRS):
           print line
           break
        if(isinstance(instances[i], str)):
            attr = instances[i].replace(",", "").replace(",", "").replace("/", "").replace(" ", "")
        else:
            attr = instances[i]
        if i == len(ATTRS)-1:
            for j in range(0, len(LAND_USE_CLASSES)):
                if(attr == LAND_USE_CLASSES[j][0:-1]):
                    attr = LAND_USE_CLASSES[j].replace(",", "").replace("/", "").replace(" ", "")

        add_dict[ATTRS[i]] = attr  # builds the dict
    line = stream.readline()
    count += 1
    arff.add_data(add_dict)


arff.end()

print ("total instances: " + str(count))
