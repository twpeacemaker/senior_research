import arcpy
import CustomRasterAnalysis
import functions
import time
import constants
import multiprocessing


path_2006 = constants.PATH + r'\Senior_Research\data\land_cover\nlcd_2011_landcover_2011_edition_2014_10_10\nlcd_2011_clip.img'
path_2011 = constants.PATH + r'\Senior_Research\data\land_cover\nlcd_2011_landcover_2011_edition_2014_10_10\nlcd_2011_clip.img'
path_elevation = constants.PATH + r"\Senior_Research\data\elevation\elevation_clip.tif"
# tract_2006 = constants.PATH + r'\Senior_Research\usps_data\usps_tracts.mdb\tract_2006'


def f(x):
    raster = CustomRasterAnalysis.CustomRasterAnalysis(path_2011, path_2006, path_elevation)
    (col_start, col_end) = raster.col_bounds
    rv = ""
    for col in range(col_start, col_end, 1):
    # for col in range(col_start, col_start + 4, 1):
        rv += raster.get_instance_attrs(x, col) + "*"
    print("Row: " + str(x) + " Done")
    return rv


if __name__ == '__main__':
    raster = CustomRasterAnalysis.CustomRasterAnalysis(path_2011, path_2006, path_elevation)
    # num_computers = input('How many computers? ')
    # comp_number = input('What order is this computer? ')
    # comp_number -= 1
    (row_start, row_end) = raster.row_bounds
    (col_start, col_end) = raster.col_bounds

    row_end = 907

    # num_rows = row_end - row_start
    # per_comp = num_rows / num_computers
    #
    # #for comp_number in range(num_computers):
    # start = comp_number * per_comp
    # end = start + per_comp
    # if(comp_number == (num_computers - 1)):
    #     # print "here"
    #     end = num_rows
    #
    # start = start + row_start
    # end = end + row_start
    # print "Computer: " + str(comp_number + 1) + " "+ str(start) + "->" + str(end) + " on " + str(multiprocessing.cpu_count()) + " processors (" + str(per_comp / multiprocessing.cpu_count()) + ") a processor"

    # pool = multiprocessing.Pool(processes=multiprocessing.cpu_count())
    start_time = time.time()
    rv = ""
    raster = CustomRasterAnalysis.CustomRasterAnalysis(path_2011, path_2006, path_elevation)
    for x in range(row_start, row_end):
        (col_start, col_end) = raster.col_bounds
        for col in range(col_start, col_end, 1):
            # for col in range(col_start, col_start + 4, 1):
            rv += raster.get_instance_attrs(x, col) + "\n"
        print("Row: " + str(x) + " Done")
    # arr = pool.map(f, range(int(start), int(start) + 4))
    end_time = time.time()

    file_stream = open( constants.PATH + r"\Senior_Research\instances\test", 'w')  # opens the file stream, clears the file
    file_stream.write(rv)
    print(end_time - start_time)






