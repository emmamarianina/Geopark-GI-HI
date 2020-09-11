# -*- coding: utf-8 -*-
"""
Created on Tue Apr 14 17:07:24 2020

@author: Emma
"""
#Calculate all the correlations between GDsum and other layers. Global, Asia, Europe

#%% import modules
import pandas as pd
import scipy
import scipy.stats


#%% World 

################################# GEOPARKS ##################################
#takes column out of the different layers 
soils = data_geoparks[['MEAN', 'Geopark_NA']].loc[data_geoparks['name']== 'Soils_stats_139']
slope_std = data_geoparks[['MEAN', 'Geopark_NA']].loc[data_geoparks['name']== 'SlopeSTD_stats_139']
slope_range = data_geoparks[['MEAN', 'Geopark_NA']].loc[data_geoparks['name']== 'SlopeRange_stats_139']
rivers = data_geoparks[['MEAN', 'Geopark_NA']].loc[data_geoparks['name']== 'Rivers_stats_139'] 
lakes = data_geoparks[['MEAN', 'Geopark_NA']].loc[data_geoparks['name']== 'Lakes_stats_139']
lithology = data_geoparks[['MEAN', 'Geopark_NA']].loc[data_geoparks['name']== 'Lithology_stats_139']
geodiversity = data_geoparks[['MEAN', 'Geopark_NA']].loc[data_geoparks['name']== 'GDsum_stats_139']

#make list of dataframes and column titles
column_title_list = ['geopark','geodiversity', 'soils', 'slope_std', 'slope_range', 'rivers', 'lakes','lithology']
column_list = [geodiversity, soils, slope_std, slope_range, rivers, lakes, lithology]

#contenate the dataframes for all layers on geopark name; this dataframe will be used to calculate correlations
geoparks_matrix = pd.concat([df.set_index('Geopark_NA') for df in column_list], axis=1, join='inner', sort=True).reset_index()
geoparks_matrix.columns = column_title_list #change column names from MEAN to the layer name

# Calculate correlaton geodiversity and layers; use spearman r because data is not normally distributed

#option: correlation Matrix: 
# corrMatrix_geoparks = geoparks_matrix.corr(method = 'spearman')
# print(corrMatrix)

#dataframe for storing calculated correlations
corr_geopark_world = pd.DataFrame(columns = ['layer', 'correlation', 'p_val'])

#calculate correlations between geodiversity and diversity layers 
for column in column_title_list[2:8]:
    geodiversity_geoparks = geoparks_matrix.geodiversity
    
    #calculate the correlation between geodiversity and other layers. NaN values (in this case only lithology on 
    #jeju island are omitted)
    corr, p_geopark = scipy.stats.spearmanr(geoparks_matrix[column], geodiversity_geoparks, nan_policy = 'omit')
    corr_geopark_world = corr_geopark_world.append({'layer': column, 'correlation': corr, 'p_val': p_geopark }, ignore_index=True)

################################# END GEOPARKS ###############################
# WORLD: correlation in loop, exclude columns with nan values from correlation

# """ when there is no data in the raster, zonal stats leaves out the entire row of the overlying polygon. This means that 
# the order of the random areas has changed, and you do not known where the row was taken out. So columns with NaNs  were taken out 
# of the correlation analyis. This is one or a few columns for most layers, and 22 columns for lithology """

#make list of column names, remove column 'name', to only get run1 till run100
col_list = list(data_world)
col_list.remove('name')

# Select MEAN values from data_world layers and store them in DataFrames 
soilsWorld = data_world[col_list].loc[data_world['name']== 'soils139_mean']
slopestdWorld = data_world[col_list].loc[data_world['name']== 'slope_std139_mean']
sloperangeWorld = data_world[col_list].loc[data_world['name']== 'slope_range139_mean']
riversWorld = data_world[col_list].loc[data_world['name']== 'Rivers139_mean']
lakesWorld = data_world[col_list].loc[data_world['name']== 'lakes139_mean']
lithologyWorld = data_world[col_list].loc[data_world['name']== 'lithology139_mean']
geodiversityWorld = data_world[col_list].loc[data_world['name']== 'geodiversity139_mean']

#make list of the layers that will be used to loop through the layers when calculating correlations
layer_list = [soilsWorld, slopestdWorld, sloperangeWorld, riversWorld, lakesWorld, lithologyWorld, geodiversityWorld] # names of the layers to loop through
layer_list_name = ['soils', 'slope_std', 'slope_range','rivers','lakes','lithology']
corr_world = pd.DataFrame(columns = ['layer', 'correlation', 'p_val']) # make empty dataframe to store corr world in (long format)

#Calculate & store correlations 
# Loop through the layers and calculate correlation between layer and geodiversity for each RUN. values are stored in column format
for layer, layer_name in zip(layer_list, layer_list_name):
    layer2 = layer[layer.columns[layer.notnull().all()]] #only take columns WITHOUT any NaN values
    layer_geodiv = geodiversityWorld[layer2.columns]
    
    for run in layer2.columns:
        corr, p_world = scipy.stats.spearmanr(layer2[run], layer_geodiv[run])
        corr_world = corr_world.append({'layer': layer_name, 'correlation': corr, 'p_val': p_world }, ignore_index=True)

#Calculate and store mean correlations      
corr_world_mean = pd.DataFrame(columns = ['layer', 'correlation_mean']) #create empty dataframe to store mean correlations
for layer_name1 in layer_list_name:
    vector = corr_world['correlation'].loc[corr_world['layer']==layer_name1]
    mean = vector.mean()
    std = vector.std()
    corr_world_mean = corr_world_mean.append({'layer': layer_name1, 'correlation_mean': mean}, ignore_index=True)

#%% ASIA
    
#takes column out of the different layers 
soils = data_geoparksEA[['MEAN', 'Geopark_NA']].loc[data_geoparksEA['name']== 'Soils_stats_61']
slope_std = data_geoparksEA[['MEAN', 'Geopark_NA']].loc[data_geoparksEA['name']== 'SlopeSTD_stats_61']
slope_range = data_geoparksEA[['MEAN', 'Geopark_NA']].loc[data_geoparksEA['name']== 'SlopeRange_stats_61']
rivers = data_geoparksEA[['MEAN', 'Geopark_NA']].loc[data_geoparksEA['name']== 'Rivers_stats_61'] 
lakes = data_geoparksEA[['MEAN', 'Geopark_NA']].loc[data_geoparksEA['name']== 'Lakes_stats_61']
lithology = data_geoparksEA[['MEAN', 'Geopark_NA']].loc[data_geoparksEA['name']== 'Lithology_stats_61']
geodiversity = data_geoparksEA[['MEAN', 'Geopark_NA']].loc[data_geoparksEA['name']== 'GDsum_stats_61']

#make list of dataframes and column titles
column_title_list = ['geopark','geodiversity', 'soils', 'slope_std', 'slope_range', 'rivers', 'lakes','lithology']
column_list = [geodiversity, soils, slope_std, slope_range, rivers, lakes, lithology]

#contenate the dataframes for all layers on geopark name; this dataframe will be used to calculate correlations
geoparks_matrix = pd.concat([df.set_index('Geopark_NA') for df in column_list], axis=1, join='inner', sort=True).reset_index()
geoparks_matrix.columns = column_title_list #change column names from MEAN to the layer name

# Calculate correlaton geodiversity and layers; use spearman r because data is not normally distributed

#option: correlation Matrix: 
# corrMatrix_geoparks = geoparks_matrix.corr(method = 'spearman')
# print(corrMatrix)

#dataframe for storing calculated correlations
corr_geopark_asia = pd.DataFrame(columns = ['layer', 'correlation', 'p_val'])

#calculate correlations between geodiversity and diversity layers 
for column in column_title_list[2:8]:
    geodiversity_geoparks = geoparks_matrix.geodiversity
    
    #calculate the correlation between geodiversity and other layers. NaN values (in this case only lithology on 
    #jeju island are omitted)
    corr, p_geopark = scipy.stats.spearmanr(geoparks_matrix[column], geodiversity_geoparks, nan_policy = 'omit')
    corr_geopark_asia = corr_geopark_asia.append({'layer': column, 'correlation': corr, 'p_val': p_geopark }, ignore_index=True)

#ASIA correlation in loop, exclude columns with nan values from correlation

# """ when there is no data in the raster, zonal stats leaves out the entire row of the overlying polygon. This means that 
# the order of the random areas has changed, and you do not known where the row was taken out. So columns with NaNs  were taken out 
# of the correlation analyis. This is one or a few columns for most layers, and 22 columns for lithology """

#make list of column names, remove column 'name', to only get run1 till run100
col_list = list(data_asia)
col_list.remove('name')

# Select MEAN values from data_asia layers and store them in DataFrames 
soilsAsia = data_asia[col_list].loc[data_asia['name']== 'Asia_60NBsoils_mean']
slopestdAsia = data_asia[col_list].loc[data_asia['name']== 'Asia_60NB_slope_std_mean']
sloperangeAsia = data_asia[col_list].loc[data_asia['name']== 'Asia_60NBslope_range_mean']
riversAsia = data_asia[col_list].loc[data_asia['name']== 'Asia_60NBrivers_mean']
lakesAsia = data_asia[col_list].loc[data_asia['name']== 'Asia_60NBlakes_mean']
lithologyAsia = data_asia[col_list].loc[data_asia['name']== 'Asia_60NBlithology_mean']
geodiversityAsia = data_asia[col_list].loc[data_asia['name']== 'Asia_60NBgeodiversity_mean']

#make list of the layers that will be used to loop through the layers when calculating correlations
layer_list = [soilsAsia, slopestdAsia, sloperangeAsia, riversAsia, lakesAsia, lithologyAsia, geodiversityAsia] # names of the layers to loop through
layer_list_name = ['soils', 'slope_std', 'slope_range','rivers','lakes','lithology']
corr_asia = pd.DataFrame(columns = ['layer', 'correlation', 'p_val']) # make empty dataframe to store corr asia in (long format)

#Calculate & store correlations 
# Loop through the layers and calculate correlation between layer and geodiversity for each RUN. values are stored in column format
for layer, layer_name in zip(layer_list, layer_list_name):
    layer2 = layer[layer.columns[layer.notnull().all()]] #only take columns WITHOUT any NaN values
    layer_geodiv = geodiversityAsia[layer2.columns]
    
    for run in layer2.columns:
        corr, p_asia = scipy.stats.spearmanr(layer2[run], layer_geodiv[run])
        corr_asia = corr_asia.append({'layer': layer_name, 'correlation': corr, 'p_val': p_asia }, ignore_index=True)

#Calculate and store mean correlations      
corr_asia_mean = pd.DataFrame(columns = ['layer', 'correlation_mean']) #create empty dataframe to store mean correlations
for layer_name1 in layer_list_name:
    vector = corr_asia['correlation'].loc[corr_asia['layer']==layer_name1]
    mean = vector.mean()
    std = vector.std()
    corr_asia_mean = corr_asia_mean.append({'layer': layer_name1, 'correlation_mean': mean}, ignore_index=True)    
    
#%% EUROPE
#takes column out of the different layers 
soils = data_geoparksEA[['MEAN', 'Geopark_NA']].loc[data_geoparksEA['name']== 'Soils_stats_66']
slope_std = data_geoparksEA[['MEAN', 'Geopark_NA']].loc[data_geoparksEA['name']== 'SlopeSTD_stats_66']
slope_range = data_geoparksEA[['MEAN', 'Geopark_NA']].loc[data_geoparksEA['name']== 'SlopeRange_stats_66']
rivers = data_geoparksEA[['MEAN', 'Geopark_NA']].loc[data_geoparksEA['name']== 'Rivers_stats_66'] 
lakes = data_geoparksEA[['MEAN', 'Geopark_NA']].loc[data_geoparksEA['name']== 'Lakes_stats_66']
lithology = data_geoparksEA[['MEAN', 'Geopark_NA']].loc[data_geoparksEA['name']== 'Lithology_stats_66']
geodiversity = data_geoparksEA[['MEAN', 'Geopark_NA']].loc[data_geoparksEA['name']== 'GDsum_stats_66']

#make list of dataframes and column titles
column_title_list = ['geopark','geodiversity', 'soils', 'slope_std', 'slope_range', 'rivers', 'lakes','lithology']
column_list = [geodiversity, soils, slope_std, slope_range, rivers, lakes, lithology]

#contenate the dataframes for all layers on geopark name; this dataframe will be used to calculate correlations
geoparks_matrix = pd.concat([df.set_index('Geopark_NA') for df in column_list], axis=1, join='inner', sort=True).reset_index()
geoparks_matrix.columns = column_title_list #change column names from MEAN to the layer name

# Calculate correlaton geodiversity and layers; use spearman r because data is not normally distributed

#option: correlation Matrix: 
# corrMatrix_geoparks = geoparks_matrix.corr(method = 'spearman')
# print(corrMatrix)

#dataframe for storing calculated correlations
corr_geopark_europe = pd.DataFrame(columns = ['layer', 'correlation', 'p_val'])

#calculate correlations between geodiversity and diversity layers 
for column in column_title_list[2:8]:
    geodiversity_geoparks = geoparks_matrix.geodiversity
    
    #calculate the correlation between geodiversity and other layers. NaN values (in this case only lithology on 
    #jeju island are omitted)
    corr, p_geopark = scipy.stats.spearmanr(geoparks_matrix[column], geodiversity_geoparks, nan_policy = 'omit')
    corr_geopark_europe = corr_geopark_europe.append({'layer': column, 'correlation': corr, 'p_val': p_geopark }, ignore_index=True)

# correlation in loop, exclude columns with nan values from correlation

# """ when there is no data in the raster, zonal stats leaves out the entire row of the overlying polygon. This means that 
# the order of the random areas has changed, and you do not known where the row was taken out. So columns with NaNs  were taken out 
# of the correlation analyis. This is one or a few columns for most layers, and 22 columns for lithology """

#make list of column names, remove column 'name', to only get run1 till run100
col_list = list(data_europe)
col_list.remove('name')

# Select MEAN values from data_europe layers and store them in DataFrames 
soilseurope = data_europe[col_list].loc[data_europe['name']== 'Europe_60NBsoils_mean']
slopestdeurope = data_europe[col_list].loc[data_europe['name']== 'Europe_60NB_slope_std_mean']
sloperangeeurope = data_europe[col_list].loc[data_europe['name']== 'Europe_60NBslope_range_mean']
riverseurope = data_europe[col_list].loc[data_europe['name']== 'Europe_60NBrivers_mean']
lakeseurope = data_europe[col_list].loc[data_europe['name']== 'Europe_60NBlakes_mean']
lithologyeurope = data_europe[col_list].loc[data_europe['name']== 'Europe_60NBlithology_mean']
geodiversityeurope = data_europe[col_list].loc[data_europe['name']== 'Europe_60NBgeodiversity_mean']

#make list of the layers that will be used to loop through the layers when calculating correlations
layer_list = [soilseurope, slopestdeurope, sloperangeeurope, riverseurope, lakeseurope, lithologyeurope, geodiversityeurope] # names of the layers to loop through
layer_list_name = ['soils', 'slope_std', 'slope_range','rivers','lakes','lithology']
corr_europe = pd.DataFrame(columns = ['layer', 'correlation', 'p_val']) # make empty dataframe to store corr europe in (long format)

#Calculate & store correlations 
# Loop through the layers and calculate correlation between layer and geodiversity for each RUN. values are stored in column format
for layer, layer_name in zip(layer_list, layer_list_name):
    layer2 = layer[layer.columns[layer.notnull().all()]] #only take columns WITHOUT any NaN values
    layer_geodiv = geodiversityeurope[layer2.columns]
    
    for run in layer2.columns:
        corr, p_europe = scipy.stats.spearmanr(layer2[run], layer_geodiv[run])
        corr_europe = corr_europe.append({'layer': layer_name, 'correlation': corr, 'p_val': p_europe }, ignore_index=True)

#Calculate and store mean correlations      
corr_europe_mean = pd.DataFrame(columns = ['layer', 'correlation_mean']) #create empty dataframe to store mean correlations
for layer_name1 in layer_list_name:
    vector = corr_europe['correlation'].loc[corr_europe['layer']==layer_name1]
    mean = vector.mean()
    std = vector.std()
    corr_europe_mean = corr_europe_mean.append({'layer': layer_name1, 'correlation_mean': mean}, ignore_index=True)
        