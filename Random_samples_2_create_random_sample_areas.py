# -*- coding: utf-8 -*-
"""Generated by ArcGIS ModelBuilder on: 2020-01-09 17:32:40

Edited by Emma Polman on 10-1-2020

This script can be used a standalone script to create random sample areas

This is an example for making random samples in Asia, random samples for Europe and the world
are made with the same code, but different input layers. Relative paths are examples to clearify the datatypes
and data storing locations.


This script:
create 61 random samples and iterates 100 times. random samples are only taken in Asia

Random sampling is constrained to 56.607 Northern Lattitude 
"""


import arcpy

#set environment
arcpy.env.workspace = r"E:\THESIS"

# To allow overwriting the outputs change the overwrite option to true.
arcpy.env.overwriteOutput = True

#%% ################ INITSALISATION ##############
# Script parameters & variables

# create random points 
RP_outloc = r"E:\THESIS\GIS_files\scratch1.gdb"
RP_outname = "random_pointsAsia"
RP_constrain = r"E:\THESIS\data_LOCATIES\locations_FINAL.gdb\world_countries_Asia_merge"

#intersect file used to cut away sample area located on the sea surface
intersect_landsurface = r"E:\THESIS\data_LOCATIES\locations_FINAL.gdb\world_countries_Asia"

## end ##

#model variables 
count_init = 54
count = count_init
count_max = 100
geoparks_in_analysis = 61

## Add field "random_join_id" to geopark_radius_m ##
# Process: Add Field (2)
geopark_radius_m = r"E:\THESIS\data_LOCATIES\data_random_sample_locations.gdb\geopark_radius_asia"
arcpy.AddField_management(geopark_radius_m, "random_join_id", "SHORT", "", "", "", "random_join_id", "NULLABLE", "NON_REQUIRED", "")
############### END INITIALISATION ##################

#%% ################DYNAMIC PART ########################

while count <= count_max:
    # Process: Create Random Points
    arcpy.CreateRandomPoints_management(RP_outloc, RP_outname, RP_constrain, "", geoparks_in_analysis, "0 Kilometer", "POINT", 0)
    print ("creating random points: "+ str(count))
    
    # Process: Calculate Field; give random_join_id the values 1:139 in random order
    arcpy.CalculateField_management(in_table=geopark_radius_m, field="random_join_id", expression="update()", expression_type="PYTHON3", code_block=r"""def update():  
      import random 
      import arcpy
      
      mylist = []  
      x = 1  
      while x <= 61:  
        mylist.append(x)  
        x += 1  
      x = 1  
      rows = arcpy.UpdateCursor(r"E:\THESIS\data_LOCATIES\data_random_sample_locations.gdb\geopark_radius_asia")  
      for row in rows:  
        y = random.choice(mylist)  
        row.random_join_id = y
        rows.updateRow(row)
        val = row.random_join_id
        mylist.remove(y)  
      del row, rows  
      return val  """)
    
    # Process: Join Field; add geopark radius to random points based on the randomly generated "random_join_id"
    random_pointsAsia = r"E:\THESIS\GIS_files\scratch1.gdb\random_pointsAsia"    
    arcpy.JoinField_management(random_pointsAsia, "OID", geopark_radius_m, "random_join_id", ["radius_m","random_join_id"])
    
    # Process: Buffer; use added geopark radius to create circular area with distribution of geopark surfaces
    buffer_out_feat = r"E:\THESIS\GIS_files\scratch1.gdb\random_bufferAsia"
    arcpy.Buffer_analysis(random_pointsAsia, buffer_out_feat, "radius_m", "FULL", "ROUND", "NONE", "", "GEODESIC")
    
    # Process: Intersect; intersect buffers with land surface outlines to delete all sample areas that are located on water surface
    intersect_in = [buffer_out_feat, intersect_landsurface]
    intersect_out = r"E:\THESIS\GIS_files\scratch1.gdb\random_bufferAsia_intersect"
    
    arcpy.Intersect_analysis(intersect_in, intersect_out, "ALL", "", "INPUT")
    
    # Process: Dissolve; intersect creates multiple polygons, these are now dissolved to multipart polygons based on the ORIG_FID
    dissolve_in = intersect_out
    count_name = str(count)
    dissolve_out = r"E:\THESIS\results\Asia_random_shapefiles.gdb\randomAsia_sample_area"+count_name
    arcpy.Dissolve_management(dissolve_in, dissolve_out, "ORIG_FID","", "MULTI_PART","DISSOLVE_LINES")

    count = count + 1
print("finished! Created " + str(count-1) + " sets of "+str(arcpy.GetCount_management(geopark_radius_m))+" random points")
#%% ##### END DYNAMIC #####
