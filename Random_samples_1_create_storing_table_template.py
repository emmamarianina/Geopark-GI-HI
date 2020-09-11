# -*- coding: utf-8 -*-
"""
Created on Mon Jan 13 11:07:06 2020

@author: 10799478

create empty basis template table of x*100

x = number of random sample areas per iteration; dependends on extent of the analysis
"""
import arcpy
arcpy.env.overwriteOutput = True
arcpy.env.workspace = r"G:\THESIS\GIS_files\scratch1.gdb"

#create template table for storing stats
location = r"G:\THESIS\GIS_files\scratch1.gdb"
template_table = arcpy.CreateTable_management(location, "stat_store_template66")

check = arcpy.Exists("stat_store_template66")
print (check)  

#%% #insert x empty rows 
template_location = r"G:\THESIS\GIS_files\scratch1.gdb\stat_store_template66" 

#add first field
arcpy.AddField_management(template_table, "run1", "FLOAT", 9, 9, "", "", "NULLABLE", "NON_REQUIRED")

#amount of rows is equal to amount of geoparks included in the analysis
row_count = 66    #example, this is for 66 random samples per iteration
insertC = arcpy.da.InsertCursor(template_location, ["OBJECTID", "run1"])
for row in range(0, row_count):
    insertC.insertRow((row, None))    
    
#%% Add fields 
for x in range(2,101):
    x_name = str(x)
    arcpy.AddField_management(template_table, "run"+x_name, "FLOAT", 9, 9, "", "", "NULLABLE", "NON_REQUIRED")
    
