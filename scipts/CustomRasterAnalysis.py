import arcpy
import constants
import functions


class CustomRasterAnalysis:
    """Handles custom analysis of raster maps """
    # ==== Attributes =====
    raster = '';
    raster_array = []
    cellSize = 0

    def __init__(self, current_raster_path, prevous_raster_path, elevation_path):
        self.raster = arcpy.Raster(current_raster_path)
        self.raster_array = arcpy.RasterToNumPyArray(self.raster)

        self.prev_raster = arcpy.Raster(prevous_raster_path)
        self.prev_raster_array = arcpy.RasterToNumPyArray(self.prev_raster)

        self.elevation = arcpy.Raster(elevation_path)
        self.elevation = arcpy.RasterToNumPyArray(self.elevation)

        #vacancy data
        self.VAC = arcpy.Raster(constants.VAC_PATH + "\VAC")
        self.VAC = arcpy.RasterToNumPyArray(self.VAC)

        self.AVG_VAC = arcpy.Raster(constants.VAC_PATH + "\AVG_VAC")
        self.AVG_VAC = arcpy.RasterToNumPyArray(self.AVG_VAC)

        self.VAC_3 = arcpy.Raster(constants.VAC_PATH + "\VAC_3")
        self.VAC_3 = arcpy.RasterToNumPyArray(self.VAC_3)

        self.VAC_3TO6 = arcpy.Raster(constants.VAC_PATH + "\VAC_3TO6")
        self.VAC_3TO6 = arcpy.RasterToNumPyArray(self.VAC_3TO6)

        #distance data
        self.Category_1 = arcpy.Raster(constants.DIST_PATH + "\Category_1")
        self.Category_1 = arcpy.RasterToNumPyArray(self.Category_1)

        # distance data
        self.Category_2 = arcpy.Raster(constants.DIST_PATH + "\Category_2")
        self.Category_2 = arcpy.RasterToNumPyArray(self.Category_2)

        self.Cites = arcpy.Raster(constants.DIST_PATH + "\Cites")
        self.Cites = arcpy.RasterToNumPyArray(self.Cites)

        self.Highway = arcpy.Raster(constants.DIST_PATH + "\Highway")
        self.Highway = arcpy.RasterToNumPyArray(self.Highway)

        self.Lake_Pond = arcpy.Raster(constants.DIST_PATH + "\Lake_Pond")
        self.Lake_Pond = arcpy.RasterToNumPyArray(self.Lake_Pond)

        self.Main_Road = arcpy.Raster(constants.DIST_PATH + "\Main_Roads")
        self.Main_Road = arcpy.RasterToNumPyArray(self.Main_Road)

        self.Rail = arcpy.Raster(constants.DIST_PATH + "\Rail")
        self.Rail = arcpy.RasterToNumPyArray(self.Rail)

        self.Ramp = arcpy.Raster(constants.DIST_PATH + "\Rail")
        self.Ramp = arcpy.RasterToNumPyArray(self.Ramp)

        self.Stream_River = arcpy.Raster(constants.DIST_PATH + "\Stream_River")
        self.Stream_River = arcpy.RasterToNumPyArray(self.Stream_River)


        # self.tract_path = tract_path

        self.cellSize = self.raster.meanCellWidth

        (height, width) = self.raster_array.shape
        self.row_bounds = (constants.BUFFER, width - constants.BUFFER)
        self.col_bounds = (constants.BUFFER, height - constants.BUFFER)

        self.prev_tract_found = None
        self.loop_avioded = 0
        self.prev_tract_str_found = ''

        self.feature_class_dict = {}

    #  PRE: Takes the int row, and int col of the point requested
    # POST: returns the arcpy.Point of the matrix
    def get_geo_point_from_raster(self, row, col):
        # gets the position of the lower left corner and
        x_min = self.raster.extent.XMin
        y_min = self.raster.extent.YMin
        # calculations the desired position relative to XMin and YMin
        x = x_min + (row * self.cellSize)
        y = y_min + (col * self.cellSize)
        point = arcpy.PointGeometry(arcpy.Point(x, y), constants.SPATIAL_REFERENCE)
        return point

    #  PRE: takes the number representation of the land use class
    # POST: returns the string representation of the class
    def get_land_use_class(self, number):
        if number >= constants.LAND_USE_MIN and number <= constants.LAND_USE_MAX:
            return constants.LAND_USE_CLASSES[number]
        else:
            return 0

    # PRE:  takes the row and col of the current_raster
    # POST: returns the value of the previous raster
    def get_curr_raster_cell(self, row, col):
        return self.get_land_use_class(self.raster_array.item(row, col))

    # PRE:  takes the row and col of the current_raster
    # POST: returns the value of the previous raster
    def get_prev_raster_cell(self, row, col):
        return self.get_land_use_class(self.prev_raster_array.item(row, col))


    #  PRE: take the (row, col) of the pixel and the layer as a string
    # POST: returns the closest distance to a feature within the layer, rounds the value to 2 decimal places
    def find_nearest_distance(self, row, col, layer):
        point = self.get_geo_point_from_raster(row, col)
        if layer not in self.feature_class_dict:
            # so the whole layer does not have to be loaded at a time
            self.feature_class_dict[layer] = arcpy.CopyFeatures_management(layer, arcpy.Geometry())
        geometries = self.feature_class_dict[layer]
        closeted = None
        for geometry in geometries:
            possible_closest = geometry.distanceTo(point)
            if closeted is None:
                closeted = possible_closest
            elif possible_closest < closeted:
                closeted = possible_closest
        return closeted

        #  PRE: int row and col you want to get the vacancy data for
        #       str the path to the vacancy layer you want to get
        # POST: returns an array of values that hold the vac data in order of VAC_ATTR_ARRAY

    # def get_vac_data(self, row, col):
    #     point = self.get_geo_point_from_raster(row, col)  # gets the linear point of the raster cell
    #     found = 0;  # keeps weather the geometry was found
    #     tract = None  # holds the tract that was last found
    #     return_str = ""
    #
    #     if self.prev_tract_found is not None:
    #         if point.within(self.prev_tract_found.SHAPE):
    #             found = 1
    #             tract = self.prev_tract_found
    #             return_str = self.prev_tract_str_found
    #     if not found:
    #         rows = arcpy.SearchCursor(self.tract_path, ["SHAPE@"] + constants.VAC_ATTR_ARRAY)
    #         # start searching
    #         row = rows.next()
    #         while row and not found:
    #             if point.within(row.SHAPE):
    #                 # found, loop ends
    #                 found = 1
    #                 # number_in += 1 #testing
    #                 self.prev_tract_found = row
    #                 tract = row
    #             else:
    #                 # ASSERT: did not find go to next row
    #                 row = rows.next()
    #         for attr in constants.VAC_ATTR_ARRAY:
    #             return_str += str(tract.getValue(attr)) + constants.SEPARATOR
    #         self.prev_tract_str_found = return_str
    #     return return_str

    #  PRE:  the row, col values must not be out of bounds
    # POST:  return the number of occurrences
    def count_neighbours(self, row, col):
        buffer = constants.MOORE_SIZE / 2
        dict = {}
        for x in range(row - buffer, constants.MOORE_SIZE + (row - buffer) + 1, 1):
            for y in range(col - buffer, constants.MOORE_SIZE + (col - buffer) + 1, 1):
                if x != buffer + 1 and y != buffer + 1:
                    land_use_class = self.get_land_use_class(self.raster_array.item(x, y))
                    # print(str(x) + ',' + str(y) + ', ' + land_use_class)
                    if land_use_class in dict:
                        dict[land_use_class] += 1
                    else:
                        dict[land_use_class] = 1
        return functions.find_two_most_freq_in_dect(dict)

    def create_green_areas(self, size, path):
        (height, width) = self.raster_array.shape
        num_add = 0
        for row in range(constants.BUFFER, width - constants.BUFFER, 1):
            for col in range(constants.BUFFER, height - constants.BUFFER, 1):
                land_use_number = self.raster_array.item(row, col)
                # ASSERT: if the land use class is green
                green = land_use_number in constants.GREEN_ARRAY
                if green == 1 and row + (size - 1) < width and col + (size - 1):
                    if self.check_square(row, col, size):
                        # Create a polygon geometry
                        array = arcpy.Array([self.get_geo_point_from_raster(row, col),
                                             self.get_geo_point_from_raster(row, col + size - 1),
                                             self.get_geo_point_from_raster(row + size - 1, col + size - 1),
                                             self.get_geo_point_from_raster(row + size - 1, col),
                                             self.get_geo_point_from_raster(row, col)
                                             ])
                        num_add += 1
                        if num_add % 100 == 0:
                            print "number added:" + str(num_add) + " row: " + str(row) + "/" + str(width - constants.BUFFER) + " " + "col: " + str(col) + "/" + str(height - constants.BUFFER);
                        functions.create_polygon(array, path)

    #  PRE: takes a int row, col, and size of square you want to check
    # POST: if valid square of size n was discovered, returns true else false
    def check_square(self, row, col, size):
        row_end = row + size - 1;
        col_end = col + size - 1;
        stop = 0
        while row < row_end and stop == 0:
            while col < col_end and stop == 0:
                land_use_number = self.raster_array.item(row, col)
                # ASSERT: if the land use class is green
                green = land_use_number in constants.GREEN_ARRAY
                if green == 0:
                    stop = 1
                col += 1
            row += 1
        # ASSERT: if the stop bool is set to 1, the square was invalid, if set to 0 was valid rv = not stop
        return not stop;

    #  PRE: object CustomRasterAnalysis r, the custom object that is needed
    # POST: returns a string separated by constants.SEPARATOR in the order called in the function
    def get_instance_attrs(self, row, col):
        # ASSERT: this string will hold all of the attr of this instance separated by a |
        instance_string = ''
        # ASSERT: gets all the distance attrs and adds them to the string
        instance_string += str(self.Category_1.item(row, col)) + constants.SEPARATOR
        instance_string += str(self.Category_2.item(row, col)) + constants.SEPARATOR
        instance_string += str(self.Cites.item(row, col)) + constants.SEPARATOR
        instance_string += str(self.Highway.item(row, col)) + constants.SEPARATOR
        instance_string += str(self.Lake_Pond.item(row, col)) + constants.SEPARATOR
        instance_string += str(self.Main_Road.item(row, col)) + constants.SEPARATOR
        instance_string += str(self.Rail.item(row, col)) + constants.SEPARATOR
        instance_string += str(self.Ramp.item(row, col)) + constants.SEPARATOR
        instance_string += str(self.Stream_River.item(row, col)) + constants.SEPARATOR

        # ASSERT: get elevation of instance and adds it to the string
        instance_string += str(self.elevation.item(row, col)) + constants.SEPARATOR

        # ASSERT: adds the prev raster cell
        instance_string += self.get_prev_raster_cell(row, col) + constants.SEPARATOR
        # ASSERT: gets the moore neighbours of the instance and adds them
        (mf_LU_class, smf_LU_class) = self.count_neighbours(row, col)
        instance_string += mf_LU_class + constants.SEPARATOR + smf_LU_class + constants.SEPARATOR

        # ASSERT: gets the vacancy data
        instance_string += str(self.VAC.item(row, col)) + constants.SEPARATOR
        instance_string += str(self.AVG_VAC.item(row, col)) + constants.SEPARATOR
        instance_string += str(self.VAC_3.item(row, col)) + constants.SEPARATOR
        instance_string += str(self.VAC_3TO6.item(row, col)) + constants.SEPARATOR
        # ASSERT: adds land use class last
        instance_string += "?" # self.get_curr_raster_cell(row, col)

        return instance_string  # remove the last constants.SEPARATOR and return


