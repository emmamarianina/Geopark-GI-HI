# -*- coding: utf-8 -*-
"""
Created on Thu Mar  5 10:30:11 2020

@author: 10799478
"""

# analysis of unique soils on continents, geoparks and the world 
import os
from dbfread import DBF
import pandas as pd
import glob
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# set directory
disk = r'G:/'
folder = 'THESIS/results/unique_soils_polygon_tables/'
path = disk+folder
os.chdir(path)

#import legend
soil_legend = pd.read_csv(disk+'THESIS/data_GEODIVERSITY/TAXNWRB_250m_ll.csv')

#import geopark id key
geoparks_key = pd.read_excel(disk+folder+'geopark_name_key.xlsx')
soil_key_col = 'WRB_group'

# %%#########################Load data##########################################

fileList = glob.glob('*.dbf') #INSERT add wildcard, do not select geopark data 

#create empty dataframe 
data_soils_world = pd.DataFrame()
data_soils_geoparks = pd.DataFrame()

for file in glob.glob('*.dbf'):
    # for index, file in enumerate(fileList):
    data = pd.DataFrame(iter(DBF((path+file), load=True)))
    
    if 'geopark' in file:#if file is geoparks , change to geoparks
        # data['continent'] = file.replace('soils_', '').replace('_polygon_join_dissolve.dbf', '')
        data_soils_geoparks = data
        
    else: #else, use continent name 
        data['continent'] = file.replace('soils_','').replace('.dbf','') #change name to continent 
        data_soils_world = pd.concat([data_soils_world, data], axis=0, sort=True)

#take out unneccessary columns from geopark data
data_soils_geoparks = data_soils_geoparks.drop(['Shape_Leng'], 1)
data_soils_world = data_soils_world.drop(['Shape_Leng', 'Id'], 1)

#join geopark names to table
data_soils_geoparks = data_soils_geoparks.rename(columns = {'JOIN_FID':'geopark_id'})
geoparks_key = geoparks_key.rename(columns = {'object_id':'geopark_id'})#.drop(['country', 'continent'], axis = 1)
# data_soils_geoparks = data_soils_geoparks.join(other = geoparks_key.set_index('geopark_id'), on = 'geopark_id', how = 'left')

# replace South America with s_america and north america with n_america and main captials to kleine letters 
data_soils_geoparks = data_soils_geoparks.replace(to_replace = ['South America', 'North America', 'Europe', 'Asia', 'Africa', 'Aisa'],\
                                                value=['s_america', 'n_america', 'europe', 'asia', 'africa', 'asia']) 

#%% calculate area, add WRB soil group name to the data

#prepare soil key for join
soil_key = soil_legend[['Number', soil_key_col]]
soil_key = soil_key.rename(columns = {'Number': 'Value'})

########### DATA WORLD ############
#CALCULATE AREA in km2 by dividing by 1E6. 
data_soils_world['area_km2'] = data_soils_world.Shape_Area/1E6

#join legend name (soil legend, soil group) to the column with codes (Values)
data_soils_world = data_soils_world.join(other = soil_key.set_index('Value'), on='gridcode', how='left')
data_soils_world = data_soils_world.rename(columns = {'WRB_group':'Group', 'gridcode': 'Value'})

########## DATA GEOPARKS #########
#calculate surface area in km2 by multiplying amount of cells (FREQUENCY) with (250*250/10E6)
data_soils_geoparks['area_km2'] = data_soils_geoparks.Shape_Area/1E6

#join legend name (soil legend, soil group) to the column with codes (Values)
data_soils_geoparks = data_soils_geoparks.join(other = soil_key.set_index('Value'), on='gridcode', how='left')
data_soils_geoparks = data_soils_geoparks.rename(columns = {'WRB_group':'Group', 'gridcode': 'Value'})



#%% ####################### SOILS WORLD ######################################


#make lists to loop through different soil types
list_continent = data_soils_world.continent.unique().tolist()
list_soils = data_soils_world.Group.unique().tolist()
list_soils_nr = data_soils_world.Value.unique().tolist()

########################### WORLD ############################################
#make list of column names & dataframe to store data in
columns_list = ['soil_name' , 'area_km2', 'area_%']
soils_world = pd.DataFrame(columns = columns_list)

# calculate percentage cover of each soil type by summing the area per continent and dividing each class by the total 
#WORLD
for soil, soil_nr in zip(list_soils, list_soils_nr): 
    
    #select all rows on a continent with a specific soil type and sum area of one specific soil group at a continent
    area_select = data_soils_world['area_km2'].loc[data_soils_world['Group']==soil] 
    area_select = area_select.sum()
    
    #calculate total area (for all soil types) on a continent to calculate percentages
    area_total = data_soils_world['area_km2'].sum()
    area_percentage = (area_select/area_total)*100
    
    #store in dataframe
    soils_world = soils_world.append({'soil_name': soil , 'area_km2': area_select, 'area_%': area_percentage}, ignore_index=True)

############################# END WORLD ######################################

########################### CONTINENTS #######################################
#make list of column names & dataframe to store data in
columns_list = ['continent',  'soil_name', 'area_km2', 'area_%']
soils_continents = pd.DataFrame(columns = columns_list)

# calculate percentage cover of each soil type by summing the area per continent and dividing each class by the total 
#WORLD
for continent in list_continent:
    for soil, soil_nr in zip(list_soils, list_soils_nr): 
        
        #select all rows on a continent with a specific soil type and sum area of one specific soil group at a continent
        area_select = data_soils_world['area_km2'].loc[(data_soils_world['continent']==continent) & (data_soils_world['Group']==soil)] 
        area_select = area_select.sum()
        
        #calculate total area (for all soil types) on a continent to calculate percentages
        area_total = data_soils_world['area_km2'].loc[(data_soils_world['continent']==continent)].sum()
        area_percentage = (area_select/area_total)*100
        
        #store in dataframe
        soils_continents = soils_continents.append({'continent': continent, 'soil_name': soil , 'area_km2': area_select, 'area_%': area_percentage}, ignore_index=True)

########################### END CONTINENTS ###################################
        
#%% ############################### GEOPARKS #################################

#make lists of unqiue values to loop through
# list_geoparks = data_soils_geoparks.geopark.unique().tolist()
list_soils_g = data_soils_geoparks.Group.unique().tolist()
list_soils_nr_g = data_soils_geoparks.Value.unique().tolist()
list_continent_g = data_soils_geoparks.continent.unique().tolist()

######################## WORLD ###############################################
#make list of column names & dataframe to store data in
columns_list = ['soil_name' , 'area_km2', 'area_%']
soils_world_geoparks = pd.DataFrame(columns = columns_list)


for soil, soil_nr in zip(list_soils_g, list_soils_nr_g): 
    
    #select all rows on a continent with a specific soil type and sum area of one specific soil group at a continent
    area_select = data_soils_geoparks['area_km2'].loc[data_soils_geoparks['Group']==soil]
    area_km = area_select.sum()
    
    #calculate total area (for all soil types) on a continent to calculate percentages
    area_total = data_soils_geoparks['area_km2'].sum()
    area_percentage = (area_km/area_total)*100
        
    #store in dataframe
    soils_world_geoparks = soils_world_geoparks.append({'soil_name': soil , 'area_km2': area_km, 'area_%': area_percentage}, ignore_index=True)
    
########################### END WOLRD ########################################
        
####################### CONTINENTS ###########################################
#make list of column names & dataframe to store data in
columns_list = ['continent','soil_name' , 'area_km2', 'area_%']
soils_continents_geoparks = pd.DataFrame(columns = columns_list)


for continent in list_continent_g:
    for soil, soil_nr in zip(list_soils_g, list_soils_nr_g): 
        
        #select all rows on a continent with a specific soil type and sum area of one specific soil group at a continent
        area_select = data_soils_geoparks['area_km2'].loc[(data_soils_geoparks['continent']==continent) & (data_soils_geoparks['Group']==soil)]
        area_km = area_select.sum()
        
        #calculate total area (for all soil types) on a continent to calculate percentages
        area_total = data_soils_geoparks['area_km2'].loc[(data_soils_geoparks['continent']==continent)].sum()
        area_percentage = (area_km/area_total)*100
            
        #store in dataframe
        soils_continents_geoparks = soils_continents_geoparks.append({'continent': continent, 'soil_name': soil , 'area_km2': area_km, 'area_%': area_percentage}, ignore_index=True)
        
########################### END CONTINENTS ###################################
        
# %% ############################COMPARISON ################################
        
#merge continent and geoparks dataframes, but first get australia and oceania out 
soils_continents_no_aus = soils_continents[['continent', 'soil_name', 'area_km2', 'area_%']].loc[(soils_continents['continent']!='australia') & (soils_continents['continent']!= 'oceania')]
soils_continents_difference = soils_continents_no_aus.merge(right = soils_continents_geoparks, how= 'left', on = ['continent', 'soil_name'], suffixes = ['_world','_geoparks']) 

#add column with difference GEOPARK - WORLD --> positve means overrepresented by geopark, negative means underrepresented by surface area
soils_continents_difference['difference'] = soils_continents_difference['area_%_geoparks'] - soils_continents_difference['area_%_world']

# merge world and world geoparks dataframes 
soils_world_difference = soils_world.merge(right = soils_world_geoparks, how= 'left', on = 'soil_name', suffixes = ['_world','_geoparks'])  

################## CALCULATE PERCENTAGE IN GEOPARK WORLD #####################

#List to loop through 
list_soils = soils_world.soil_name.unique().tolist()

#Store in this dataframe 
soils_world_compare = pd.DataFrame()

for soil in list_soils:  
    
    area_world = soils_world['area_km2'].loc[soils_world['soil_name'] == soil].sum()
    area_geopark = soils_world_geoparks['area_km2'].loc[soils_world_geoparks['soil_name'] == soil].sum()
    
    #calculate the percentage of each rock type that is located in the geopark
    percentage_in_geopark = (area_geopark/area_world)*100
    
    #store in dataframe 
    soils_world_compare = soils_world_compare.append({'soil_name': soil, 'percentage_in_geopark': percentage_in_geopark}, ignore_index=True)
 
############### CALCULATE PERCENTAGE IN GEOPARK CONTINENTS ###################

#List to loop through 
list_soils = soils_continents.soil_name.unique().tolist()
list_continents = soils_continents.continent.unique().tolist()

#Store in this dataframe 
soils_continents_compare = pd.DataFrame()

for continent in list_continents:
    for soil in list_soils:
    
        area_world = soils_continents['area_km2'].loc[(soils_continents['soil_name'] == soil) & (soils_continents['continent']== continent)].sum()
        area_geopark = soils_continents_geoparks['area_km2'].loc[(soils_continents_geoparks['soil_name'] == soil) & (soils_continents_geoparks['continent'] == continent)].sum()
        
        if area_geopark == 0 :
            percentage_in_geopark = 0
        else:
            #calculate the percentage of each soil type that is located in the geopark when area geopark > 0
            percentage_in_geopark = (area_geopark/area_world)*100
        
        #store in dataframe 
        soils_continents_compare = soils_continents_compare.append({'continent': continent, 'soil_name': soil, 'percentage_in_geopark': percentage_in_geopark}, ignore_index=True)

