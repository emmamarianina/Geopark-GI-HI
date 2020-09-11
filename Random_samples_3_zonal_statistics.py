# -*- coding: utf-8 -*-
"""
Created on Fri Jan 10 14:03:11 2020

Goal: calculate zonal statistics for random samples.

This script is an example showing the calculation of zonal statistics for SlopeSTD in Asia.
In order to sample other layers and extents, the extraction raster and extraction features need to be changed.
Relative paths are examples of where and how data should be accessed and saved. 

NB: zonal stats does not calculate MEDIAN for floating point rasters 
"""

import arcpy
from arcpy import env
from arcpy.sa import *

#set environment
arcpy.env.workspace = r"D:\Emma_Polman\thesis_geodiversity_analyse" 

# To allow overwriting the outputs change the overwrite option to true.
arcpy.env.overwriteOutput = True

#the amount of iterations made by the model
iterations = 1
geoparks_in_analysis = 61

#%% Slope STD asia ------------------------------------------------------------------------------------------------------------------------------
#%% ################ INITSALISATION ##############
#type of layer for which statistic is calculated; this name is used for saving the results
layer_type = "asia_slope_std"
layer_type_pathname = "\asia_slope_std"

#data raster layer from which the stats are calculated
extraction_raster = r"D:\Emma_Polman\Versteegh\Results\data_SlopeSTD.tif"

#Ouput of zonal stats tool goes to this table. Data is then stored in other tables. This table changed every iteration. 
table_out_zonal = r"D:\Emma_Polman\thesis_geodiversity_analyse\scratch_geodiversity.gdb"+layer_type_pathname+"_stats"

# location of table template used to make the storage tables for each statistic
table_template = arcpy.env.workspace = r"D:\Emma_Polman\thesis_geodiversity_analyse\scratch_geodiversity.gdb\stat_store_template61" #location where table template is stored

#location where stat tables will be stored 
table_loc = r"D:\Emma_Polman\thesis_geodiversity_analyse\results_geodiversity_asia.gdb" 

#this script saves mean, std, median, maximum and minimum. 
#table template is copied to create a storage table for each statistic 
mean_table = arcpy.Copy_management(table_template, table_loc+layer_type_pathname+"_mean" )
std_table = arcpy.Copy_management(table_template, table_loc+layer_type_pathname+"_std")
#median_table = arcpy.Copy_management(table_template, table_loc+layer_type_pathname+"_median" )
minimum_table = arcpy.Copy_management(table_template, table_loc+layer_type_pathname+"_minimum")
maximum_std_table = arcpy.Copy_management(table_template, table_loc+layer_type_pathname+"_maximum")

#model parameters
count_features_init = 1 #model starts at feature class 1
count_features = count_features_init 
count_features_max = iterations  #model calculates zonal stats for all feature classes


print ("calculating statistics for "+ layer_type + " diversity; 61 points" )
############### END INITIALISATION ###########


#% ############### DYNAMIC PART #################
while count_features <= count_features_max:
    count_features_name = str(count_features)
    extraction_features = r"D:\Emma_Polman\thesis_geodiversity_analyse\asia_random_shapefiles.gdb\randomAsia_sample_area"+count_features_name
    
    #Calculate zonal stats
    #zonal stats are saved in scratch gdb and overwritten every iteration (to avoid 600 zonal stats tables)
    #ZonalStatisticsAsTable (in_zone_data, zone_field, in_value_raster, out_table, {ignore_nodata}, {statistics_type})
    print("Performing zonal statistics: " + count_features_name)
    ZonalStatisticsAsTable (extraction_features, "ORIG_FID", extraction_raster, table_out_zonal, "DATA", "ALL")
    
    #1) read values from zonal stats table for required stats
    read_stats = ["MEAN", "STD", "MIN", "MAX"]
    zonal_stats_table = table_out_zonal
    
    #search for all stat values that need to be copied using a Search Cursor 
    SC = arcpy.da.SearchCursor(zonal_stats_table, read_stats)
    
    for row in SC:
        mean = [row[0] for row in arcpy.da.SearchCursor(zonal_stats_table, read_stats)]
        std = [row[1] for row in arcpy.da.SearchCursor(zonal_stats_table, read_stats)]
#        median = [row[2] for row in arcpy.da.SearchCursor(zonal_stats_table, read_stats)]
        minimum = [row[2] for row in arcpy.da.SearchCursor(zonal_stats_table, read_stats)]
        maximum = [row[3] for row in arcpy.da.SearchCursor(zonal_stats_table, read_stats)]
    del row
    
    # storing table with stat values found using an Update Cursor 
    if len(mean) <geoparks_in_analysis:
        add_rows = geoparks_in_analysis-len(mean)
        
        mean.extend([None]*add_rows)
        std.extend([None]*add_rows)
#        median.extend([None]*add_rows)
        minimum.extend([None]*add_rows)
        maximum.extend([None]*add_rows)
    
    #MEAN
    update_field = "run"+count_features_name
    with arcpy.da.UpdateCursor(r"D:\Emma_Polman\thesis_geodiversity_analyse\results_geodiversity_asia.gdb"+layer_type_pathname+"_mean", [update_field]) as UC:
        for value in mean:
            next(UC)
            UC.updateRow([value])
    del (UC)
    del (value)
    
    #STD
    update_field = "run"+count_features_name
    with arcpy.da.UpdateCursor(r"D:\Emma_Polman\thesis_geodiversity_analyse\results_geodiversity_asia.gdb"+layer_type_pathname+"_std", [update_field]) as UC:
        for value in std:
            next(UC)
            UC.updateRow([value])
    del (UC)
    del (value)
    
#    #MEDIAN
#    update_field = "run"+count_features_name
#    with arcpy.da.UpdateCursor(r"D:\Emma_Polman\thesis_geodiversity_analyse\results_geodiversity_asia.gdb"+layer_type_pathname+"_median", [update_field]) as UC:
#        for value in median:
#            next(UC)
#            UC.updateRow([value])
#    del (UC)
#    del (value)
    
    #MINIMUM
    update_field = "run"+count_features_name
    with arcpy.da.UpdateCursor(r"D:\Emma_Polman\thesis_geodiversity_analyse\results_geodiversity_asia.gdb"+layer_type_pathname+"_minimum", [update_field]) as UC:
        for value in minimum:
            next(UC)
            UC.updateRow([value])
    del (UC)
    del (value)
    
    #MAXIMUM
    update_field = "run"+count_features_name
    with arcpy.da.UpdateCursor(r"D:\Emma_Polman\thesis_geodiversity_analyse\results_geodiversity_asia.gdb"+layer_type_pathname+"_maximum", [update_field]) as UC:
        for value in maximum:
            next(UC)
            UC.updateRow([value])
    del (UC)
    del (value)
    
    #delete values that will be overwritten to avoid problems with null values 
    del (SC)
    del (mean)
    del (std)
#    del (median) 
    del (minimum) 
    del (maximum) 
        
    
    #update counter
    count_features = count_features+1
    
print ("analysis for "+layer_type+" is finished!")


