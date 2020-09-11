# -*- coding: utf-8 -*-
"""
Created on Tue Mar  3 11:32:14 2020

@author: 10799478
"""

#assess unique lithology in geoparks; continents and world

# import arcpy  
# from arcpy import env  
import pandas as pd
# import geopandas
from dbfread import DBF
import os
import glob
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

# set directory
disk = r'G:/'
folder = 'THESIS/results/unqiue_lithology_V2/'
path = disk+folder
os.chdir(path)

# %%#########################Load data##########################################

fileList = glob.glob('*.dbf') #INSERT add wildcard, do not select geopark data 

#create empty dataframe 
lit_world = pd.DataFrame()
lit_geoparks = pd.DataFrame()

for file in glob.glob('*.dbf'):
    # for index, file in enumerate(fileList):
    data = pd.DataFrame(iter(DBF((path+file), load=True)))
    
    if 'geopark' in file:#if file is geoparks , change to geoparks
        # data['continent'] = file.replace('soils_', '').replace('_polygon_join_dissolve.dbf', '')
        lit_geoparks = data
        
    else: #else, use continent name 
        data['continent'] = file.replace('lithology_','').replace('.dbf','') #change name to continent 
        lit_world = pd.concat([lit_world, data], axis=0, sort=True)

#take out unneccessary columns from geopark data
lit_geoparks = lit_geoparks.drop(['Shape_Leng', 'Join_Count', 'TARGET_FID', 'JOIN_FID', 'IDENTITY_', 'Shape_Area', 'Shape_Le_1'], 1)
lit_world = lit_world.drop(['Shape_Leng'], 1)

# replace South America with s_america and north america with n_america and main captials to kleine letters
# correct the typo in Asia that you keep on making  
lit_geoparks = lit_geoparks.replace(to_replace = ['South America', 'North America', 'Europe', 'Asia', 'Africa', 'Aisa'],\
                                                value=['s_america', 'n_america', 'europe', 'asia', 'africa', 'asia'])  

#make legend key
legend_key = pd.DataFrame([['No data', 'nd'],['Unconsolidated sediments', 'su'],['Siliciclastic sedimentary rocks','ss'],\
                           ['Mixed sedimentary rocks', 'sm'], ['Carbonate sedimentary rocks','sc'], ['Pyroclastics','py'],\
                           ['Evaporites','ev'], ['Metamorphic rocks','mt'], ['Acid plutonic rocks','pa'],\
                           ['Intermediate plutonic rocks','pi'],['Basic plutonic rocks','pb'], ['Acid volcanic rocks','va'],\
                           ['Intermediate volcanic rocks', 'vi'], ['Basic volcanic rocks','vb'], ['Ice and glaciers','ig'],\
                            ['Water Bodies','wb']], columns = ['lithology_name', 'lithology'])


#fix mistake, mexico is in n_america, not in s_america
lit_geoparks['continent']    
#%% PERCENTAGE PER CONTINENT 
    #calculate areas per lithology class for each CONTINENT 

#create lists with unique values
list_continent = lit_world.continent.unique().tolist()
list_lit1 = lit_world.xx.unique().tolist()
list_lit3 = lit_world.Litho.unique().tolist()

######################FIRST ORDER LITHOLOGY##############################
#for each continent, calculate the total area in km^2 (Column: POLY_AREA) for the first order lithology class (Column: xx) 

columns_list = ['continent', 'lithology', 'area_km2', 'area_%']
lit1_C = pd.DataFrame(columns = columns_list)

for continent in list_continent:
    for lit1 in list_lit1:
        lit_select = lit_world['POLY_AREA'].loc[(lit_world['continent']==continent) & (lit_world['xx']==lit1)]
        area_lit_sum = lit_select.sum()
        
        area_total = lit_world['POLY_AREA'].loc[(lit_world['continent']==continent)].sum()
        area_percentage = (area_lit_sum/area_total)*100
        
        #store in dataframe
        lit1_C = lit1_C.append({'continent': continent, 'lithology': lit1, 'area_km2': area_lit_sum, 'area_%': area_percentage}, ignore_index=True)

# add lithology names to abbrivations in dataframe 
lit1_C = lit1_C.join(other = legend_key.set_index('lithology'), on = 'lithology', how = 'left')   
     
###################THRIRD ORDER LITHOLOGY###########################
#for each continent, calculate the total area in km^2 (Column: POLY_AREA) for the thrid order lithology class (Column: Litho) 

#create empty dataframe 
columns_list = ['continent', 'lithology', 'area_km2', 'area_%']
lit3_C= pd.DataFrame(columns = columns_list)

for continent in list_continent:
    for lit3 in list_lit3:
        lit_select = lit_world['POLY_AREA'].loc[(lit_world['continent']==continent) & (lit_world['Litho']==lit3)]
        area_lit_sum = lit_select.sum()
        
        area_total = lit_world['POLY_AREA'].loc[(lit_world['continent']==continent)].sum()
        area_percentage = (area_lit_sum/area_total)*100
        
        #store in dataframe
        lit3_C = lit3_C.append({'continent': continent, 'lithology': lit3, 'area_km2': area_lit_sum, 'area_%': area_percentage}, ignore_index=True)

#%%  PERCENTAGE PER CONTINENT GEOPARKS 
#calculate percentages per class geoparks per coninent 

###########FIRST ORDER LITHOLOGY ######################### 
    
#create lists with unique values; use world lists, so more values 
list_continent = lit_geoparks.continent.unique().tolist()
list_lit1 = lit_world.xx.unique().tolist()
list_lit3 = lit_world.Litho.unique().tolist()

#create empty dataframe 
columns_list = ['continent', 'lithology', 'area_km2', 'area_%']
lit1_geoparks_C = pd.DataFrame(columns = columns_list)

for continent in list_continent:
    for lit1 in list_lit1:
        lit_select = lit_geoparks['POLY_AREA'].loc[(lit_geoparks['continent']==continent) & (lit_geoparks['xx']==lit1)]
        area_lit_sum = lit_select.sum()
        
        area_total = lit_geoparks['POLY_AREA'].loc[(lit_geoparks['continent']==continent)].sum()
        area_percentage = (area_lit_sum/area_total)*100
        
        #store in dataframe
        lit1_geoparks_C = lit1_geoparks_C.append({'continent': continent, 'lithology': lit1, 'area_km2': area_lit_sum, 'area_%': area_percentage}, ignore_index=True)

# add lithology names to abbrivations in dataframe 
lit1_geoparks_C = lit1_geoparks_C.join(other = legend_key.set_index('lithology'), on = 'lithology', how = 'left')  

      
###########THRID ORDER LITHOLOGY ######################### 
columns_list = ['continent', 'lithology', 'area_km2', 'area_%']
lit3_geoparks_C = pd.DataFrame(columns = columns_list)

for continent in list_continent:
    for lit3 in list_lit3:
        lit_select = lit_geoparks['POLY_AREA'].loc[(lit_geoparks['continent']==continent) & (lit_geoparks['Litho']==lit3)]
        area_lit_sum = lit_select.sum()
        
        area_total = lit_geoparks['POLY_AREA'].loc[(lit_geoparks['continent']==continent)].sum()
        area_percentage = (area_lit_sum/area_total)*100
        
        #store in dataframe
        lit3_geoparks_C = lit3_geoparks_C.append({'continent': continent, 'lithology': lit3, 'area_km2': area_lit_sum, 'area_%': area_percentage}, ignore_index=True)

#%% PERCENTAGE FOR WORLD
#Calculate area and percentage for the entire WORLD (lit1 and lit3 level)    

######################FIRST ORDER LITHOLOGY##############################
        
#create empty dataframes
lit1_W = pd.DataFrame()
lit3_W = pd.DataFrame()

for lit1W in list_lit1:
    
    #select all lithology from 
    lit_select = lit1_C['area_km2'].loc[(lit1_C['lithology']==lit1W)]
    area_lit_sum = lit_select.sum()
    
    area_total = lit1_C['area_km2'].sum()
    area_percentage = (area_lit_sum/area_total)*100
    
    #store in dataframe 
    lit1_W = lit1_W.append({'lithology': lit1W, 'area_km2': area_lit_sum, 'area_%': area_percentage}, ignore_index=True)

    
# add lithology names to abbrivations in dataframe 
lit1_W = lit1_W.join(other = legend_key.set_index('lithology'), on = 'lithology', how = 'left')   


###################THIRD ORDER LITHOLOGY########################### 
for lit3W in list_lit3:
    
    #select all lithology from 
    lit_select = lit3_C['area_km2'].loc[(lit3_C['lithology']==lit3W)]
    area_lit_sum = lit_select.sum()
    
    area_total = lit3_C['area_km2'].sum()
    area_percentage = (area_lit_sum/area_total)*100
    
    #store in dataframe 
    lit3_W = lit3_W.append({'lithology': lit3W, 'area_km2': area_lit_sum, 'area_%': area_percentage}, ignore_index=True)      
        

#%% PERCENTAGE FOR WOLRD GEOPARKS 
#Calculate area and percentage for GEOPARKS in the entire world (lit1 and lit3 level)    

lit1_geoparks_W = pd.DataFrame()
lit3_geoparks_W = pd.DataFrame()

############################## FIRST ORDER LITHOLOGY ###################
for lit1W in list_lit1:
    
    #select all lithology from lithology geoparks 
    lit_select = lit1_geoparks_C['area_km2'].loc[(lit1_geoparks_C['lithology']==lit1W)]
    area_lit_sum = lit_select.sum()
    
    area_total = lit1_geoparks_C['area_km2'].sum()
    area_percentage = (area_lit_sum/area_total)*100
    
    #store in dataframe 
    lit1_geoparks_W = lit1_geoparks_W.append({'lithology': lit1W, 'area_km2': area_lit_sum, 'area_%': area_percentage}, ignore_index=True)

    
# add lithology names to abbrivations in dataframe 
lit1_geoparks_W = lit1_geoparks_W.join(other = legend_key.set_index('lithology'), on = 'lithology', how = 'left') 

############################## THIRD ORDER LITHOLOGY ###################
for lit3W in list_lit3:
    
    #select all lithology from 
    lit_select = lit3_geoparks_C['area_km2'].loc[(lit3_geoparks_C['lithology']==lit3W)]
    area_lit_sum = lit_select.sum()
    
    area_total = lit3_geoparks_C['area_km2'].sum()
    area_percentage = (area_lit_sum/area_total)*100
    
    #store in dataframe 
    lit3_geoparks_W = lit3_geoparks_W.append({'lithology': lit3W, 'area_km2': area_lit_sum, 'area_%': area_percentage}, ignore_index=True)
    

     
#%% COMPARISON

#merge world and geoparks dataframes, but first get australia and oceania out 
lit1_C_no_aus = lit1_C[['continent', 'lithology', 'lithology_name', 'area_km2', 'area_%']].loc[(lit1_C['continent']!='australia') & (lit1_C['continent']!= 'oceania')]
lit1_Comp_geoparks = lit1_C_no_aus.merge(right = lit1_geoparks_C, how= 'left', on = ['continent', 'lithology', 'lithology_name'], suffixes = ['_world','_geoparks']) 

#add column with difference GEOPARK - WORLD --> positve means overrepresented by geopark, negative means underrepresented by surface area
lit1_Comp_geoparks['difference'] = lit1_Comp_geoparks['area_%_geoparks'] - lit1_Comp_geoparks['area_%_world']

#%% set style
# sns.axes_style() gives current style properties 
sns.set_style('whitegrid', {'axes.facecolor': '0.99','grid.color': '.93', 'axes.edgecolor': '.85', 'axes.labelcolor': '.25', 'xtick.color': '.35',\
                'ytick.color': '.35', 'xtick.bottom': True, 'patch.edgecolor': 'k', 'patch.force_edgecolor': False,})


# plt.style.use('ggplot') #for ggplot look and feel
sns.set_context('paper')
        
#%% VISUALISATION CONTINENTS: visualise the bars side by side 
sns.set_palette('deep')


#geoparks 
lit1_geoparks_C = lit1_geoparks_C.sort_values(by = ['continent', 'lithology'])

list_lit1 = ['ev', 'mt', 'pa', 'pb', 'pi', 'py', 'sc', 'sm', 'ss', 'su', 'va', 'vb', 'vi', 'wb', 'ig', 'nd']

list_litho_name = ['Evaporites (ev)', 'Metamorphic rocks (mt)', 'Acid plutonic rocks (pa)', 'Basic plutonic rocks (pb)',\
                       'Intermediate plutonic rocks (pi)', 'Pyroclastics (py)', 'Carbonate sedimentary rocks (sc)',\
                           'Mixed sedimentary rocks (sm)', 'Siliciclastic sedimentary rocks (ss)', 'Unconsolidated sediments (su)',\
                               'Acid volcanic rocks (va)', 'Basic volcanic rocks (vb)', 'Intermediate volcanic rocks (vi)',\
                                   'Water Bodies (wb)', 'Ice and glaciers (ig)', 'No data (nd)'] # used for the legend 

list_color = ['rebeccapurple', 'thistle', 'lightcoral', 'indianred', 'firebrick', 'lightsteelblue', 'goldenrod', 'gold', 'khaki', 'tan',\
              'seagreen', 'mediumseagreen', 'darkseagreen', 'dodgerblue', 'azure', 'black']                     

list_continent_g = ['continent\n\n               Africa', 'geoparks',\
                    'continent\n\n               Asia', 'geoparks',\
                    'continent\n\n               Europe','geoparks',\
                    'continent\n\n               North America', 'geoparks',\
                    'continent\n\n               South America', 'geoparks']
N = 10 #make bars for 7 continents
ind = np.arange(N)#used for the locations of the bars at the x-axis
ind = [0, 0.75, 2, 2.75, 4, 4.75, 6, 6.75, 8, 8.75]
width = 0.35

fig2 = plt.figure(figsize=(11.69, 4.27), dpi=300)

for lit1, color_ in zip(list_lit1, list_color):
    
    plot_vector1 = lit1_Comp_geoparks[['area_%_world', 'continent']].loc[lit1_Comp_geoparks['lithology']==lit1]
    plot_vector2 = lit1_Comp_geoparks[['area_%_geoparks', 'continent']].loc[lit1_Comp_geoparks['lithology']==lit1]
    
    plot_vector1 = plot_vector1.rename(columns = {'area_%_world':'area_%'})
    plot_vector2 = plot_vector2.rename(columns = {'area_%_geoparks':'area_%'})
    
    plot_vector1['scale'] = 'random'
    plot_vector2['scale'] = 'geoparks'
    
    plot_vector = pd.concat([plot_vector1, plot_vector2], axis = 0)
    plot_vector = plot_vector.sort_values(by = 'continent')
    plot_vector = plot_vector['area_%']
    
    if list_lit1[0] == lit1:
        p2 = plt.bar(ind, plot_vector, width, color = color_)
        bottom_vector = plot_vector

    else:
        p1 = plt.bar(ind, plot_vector, width, bottom = bottom_vector, color = color_)
        bottom_vector = bottom_vector + plot_vector.values
    
    plt.legend(list_litho_name, loc = 'best', bbox_to_anchor=(1,1))
      
#lay out
plt.ylabel('% area')
plt.title('% area of each rock types on the continent and the geoparks on the continent')
plt.xticks(ind, (list_continent_g))
plt.ylim(0, 105)

#change legend order

##################################################################################
#%% compare World to geoparks World 

#Calculate what percentage area of each lithology type is actually captured within geopark borders GLOBALLY


#################### FIRST ORDER ##################################

#List to loop through 
list_lit1 = lit_world.xx.unique().tolist()

#Store in this dataframe 
lit1_compare = pd.DataFrame()

for lit1 in list_lit1:  
    
    area_world = lit1_W['area_km2'].loc[lit1_W['lithology'] == lit1].sum()
    area_geopark = lit1_geoparks_W['area_km2'].loc[lit1_geoparks_W['lithology'] == lit1].sum()
    
    #calculate the percentage of each rock type that is located in the geopark
    percentage_in_geopark = (area_geopark/area_world)*100
    
    #store in dataframe 
    lit1_compare = lit1_compare.append({'lithology': lit1, 'percentage_in_geopark': percentage_in_geopark}, ignore_index=True)
    
# add lithology names to abbrivations in dataframe 
lit1_compare = lit1_compare.join(other = legend_key.set_index('lithology'), on = 'lithology', how = 'left') 

####################### THIRD ORDER ################################

#List to loop through 
list_lit3 = lit_world.Litho.unique().tolist()

#Store in this dataframe 
lit3_compare = pd.DataFrame()

for lit3 in list_lit3:  
    
    area_world = lit3_W['area_km2'].loc[lit3_W['lithology'] == lit3].sum()
    area_geopark = lit3_geoparks_W['area_km2'].loc[lit3_geoparks_W['lithology'] == lit3].sum()
    
    #calculate the percentage of each rock type that is located in the geopark
    percentage_in_geopark = (area_geopark/area_world)*100
    
    #store in dataframe 
    lit3_compare = lit3_compare.append({'lithology': lit3, 'percentage_in_geopark': percentage_in_geopark}, ignore_index=True)
        
#%% ############ VISUALISE #################
fig = plt.figure(figsize= (12, 8), dpi=300)

# list for names etc
list_lit1 = ['ev', 'mt', 'pa', 'pb', 'pi', 'py', 'sc', 'sm', 'ss', 'su', 'va', 'vb', 'vi', 'wb', 'ig', 'nd']

list_litho_name2 = ['Evaporites', 'Metamorphic rocks', 'Acid plutonic rocks', 'Basic plutonic rocks',\
                       'Intermediate plutonic rocks', 'Pyroclastics', 'Carbonate sedimentary rocks',\
                           'Mixed sedimentary rocks', 'Siliciclastic sedimentary rocks', 'Unconsolidated sediments',\
                               'Acid volcanic rocks', 'Basic volcanic rocks', 'Intermediate volcanic rocks',\
                                   'Water Bodies', 'Ice and glaciers', 'No data'] # used for the legend 

list_color = ['rebeccapurple', 'thistle', 'lightcoral', 'indianred', 'firebrick', 'lightsteelblue', 'goldenrod', 'gold', 'khaki', 'tan',\
              'seagreen', 'mediumseagreen', 'darkseagreen', 'dodgerblue', 'azure', 'black']     

bar = sns.barplot(x = 'percentage_in_geopark', y = 'lithology_name', data = lit1_compare, orient = 'h', order = list_litho_name2, color = 'black')
plt.axis(xmin = 0, xmax = 1) #set axis limits
plt.xlabel('% area in geoparks')
plt.ylabel('') 
bar.set_yticklabels(labels = list_litho_name2, size = 14, rotation = 0)


#third order
plot_third = 0

if plot_third == 1:
    
    
    fig2 = plt.figure(figsize= ( 8, 6), dpi=300)
    
    #only plot rows with values higher than 5%
    # plot_data = lit3_compare[lit3_compare != 0.].dropna(axis=0) #only takes zeros out
    plot_data = lit3_compare.loc[lit3_compare['percentage_in_geopark']>=1.] #also takes values <5 out
    
    #sort plot data from high to low
    plot_data = plot_data.sort_values(by = 'percentage_in_geopark', ascending = False)
    
    bar = sns.barplot(x = 'percentage_in_geopark', y = 'lithology', data = plot_data, orient = 'h', color = 'black')
    plt.axis(xmin = 0, xmax = 100) #set axis limits 
    bar.set_yticklabels(labels = plot_data['lithology'], size = 12, rotation = 0)
    plt.xlabel('% area in geoparks')
    plt.ylabel('') 

#%% Compare CONTINENTS to geoparks on these CONTINENTS 
    #what % aera of lithology types can be found within geoparks on the continent 

#################### FIRST ORDER ##################################

#takes out rows with zero values. Emma: Is this necessary? solution with if statement better
# lit1_C2 = lit1_C[lit1_C != 0.].dropna(axis=0)

#List to loop through 
list_lito = lit1_C.lithology.unique().tolist()
list_continents = lit1_C.continent.unique().tolist()

#Store in this dataframe 
lit1_compare_C = pd.DataFrame()

for continent in list_continents:
    for lito in list_lito:
    
        area_world = lit1_C['area_km2'].loc[(lit1_C['lithology'] == lito) & (lit1_C['continent']== continent)].sum()
        area_geopark = lit1_geoparks_C['area_km2'].loc[(lit1_geoparks_C['lithology'] == lito) & (lit1_geoparks_C['continent'] == continent)].sum()
        
        if area_geopark == 0 :
            percentage_in_geopark = 0
        else:
            #calculate the percentage of each rock type that is located in the geopark when area geopark > 0
            percentage_in_geopark = (area_geopark/area_world)*100
        
        #store in dataframe 
        lit1_compare_C = lit1_compare_C.append({'continent': continent, 'lithology': lito, 'percentage_in_geopark': percentage_in_geopark}, ignore_index=True)
        
# add lithology names to abbrivations in dataframe 
lit1_compare_C = lit1_compare_C.join(other = legend_key.set_index('lithology'), on = 'lithology', how = 'left') 

#%%
####################### THIRD ORDER ################################

#List to loop through 
list_lit3 = lit_world.Litho.unique().tolist()
list_continent = lit_world.continent.unique().tolist()

#Store in this dataframe 
lit3_compare_C = pd.DataFrame()

for continent in list_continent:
    for lit3 in list_lit3:  
    
        area_world = lit3_C['area_km2'].loc[(lit3_C['lithology'] == lit3) & (lit3_C['continent'] == continent)].sum()
        area_geopark = lit3_geoparks_C['area_km2'].loc[(lit3_geoparks_C['lithology'] == lit3) & (lit3_geoparks_C['continent'] == continent)].sum()
        
        #make sure that if the surface area in geopark is zero, a zero is given. If the lithology is not present on the continent, the calculation does not work because of nan error
        
        if area_geopark == 0:
            percentage_in_geopark = 0 
        else:
            #calculate the percentage of each rock type that is located in the geopark
            percentage_in_geopark = (area_geopark/area_world)*100.
        
        #store in dataframe 
        lit3_compare_C = lit3_compare_C.append({'continent': continent,'lithology': lit3, 'percentage_in_geopark': percentage_in_geopark}, ignore_index=True)

#%% ############ VISUALISE #################
fig = plt.figure(figsize= (8, 8), dpi=300)

#take out australia and oceania because there are no geoparks on these continents 
# plot_data_C = lit1_compare_C.loc[(lit1_C['continent']!='australia') & (lit1_C['continent']!= 'oceania')]

#only plot europe and asia
plot_data_C = lit1_compare_C[['continent', 'lithology', 'percentage_in_geopark', 'lithology_name']].loc[(lit1_compare_C['continent']=='asia') | (lit1_compare_C['continent']== 'europe')]


#list of colors for the continents 
# continent_color = ['darkorange', 'indianred', 'darkseagreen', 'gold', 'royalblue']
continent_color = [ 'indianred', 'darkseagreen']

#plot all 
sns.barplot(x = 'percentage_in_geopark', y = 'lithology_name', hue = 'continent', data = plot_data_C, orient = 'h', order = list_litho_name2, palette = continent_color)
plt.axis(xmin = 0, xmax = 20) #set axis limits
plt.xlabel('% area in geoparks')
plt.ylabel('') 


#third order
plot_third = 1
if plot_third == 1:
    
    
    fig2 = plt.figure(figsize= ( 8, 6), dpi=300)
    
    #list of colors for the continents 
    continent_color = ['indianred', 'darkseagreen', 'royalblue']

    #only plot rows with values higher than 5%
    # plot_data = lit3_compare[lit3_compare != 0.].dropna(axis=0) #only takes zeros out
    plt_data_C = lit3_compare_C.loc[lit3_compare_C['percentage_in_geopark']>=5.] #also takes values <5 out
   
    #sort plot data from high to low
    plt_data_C = plt_data_C.sort_values(by = ['continent','lithology'], ascending = True)
    
    bar = sns.barplot(x = 'percentage_in_geopark', y = 'lithology', hue = 'continent', data = plt_data_C, orient = 'h', palette = continent_color)
    plt.axis(xmin = 0, xmax = 100) #set axis limits 
    bar.set_yticklabels(labels = plt_data_C['lithology'], size = 6, rotation = 0)
    plt.xlabel('% area in geoparks')
    plt.ylabel('') 