import arcpy
import CustomRasterAnalysis
import constants

#  PRE: takes a dict
# POST: returns a tuple of the two most frequent values

#  PRE: takes a dictionary of values and ints
# POST: returns a tuple of the most frequent and the second most f
def find_two_most_freq_in_dect(dict):
    most_freq = ''
    second_most_freq = ''
    for key in dict:
        if most_freq == '' and second_most_freq == '':
            most_freq = key
            second_most_freq = key
        if dict[key] > dict[most_freq]:
            most_freq = key
        elif dict[key] > dict[second_most_freq]:
            second_most_freq = key
    return most_freq, second_most_freq


def create_polygon(array, path):
    polygon = arcpy.Polygon(array)
    # Open an InsertCursor and insert the new geometry
    cursor = arcpy.da.InsertCursor(path, ['SHAPE@'])
    cursor.insertRow([polygon])
    # Delete cursor object
    del cursor





def get_cols_at_range(raster, col_start, col_end):
    (row_start, row_end) = raster.row_bounds
    for col in range(col_start, col_end, 1):
        for row in range(row_start, row_end, 1):
            get_instance_attrs(raster, row, col)
            break
        break
