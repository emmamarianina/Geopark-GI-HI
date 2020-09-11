# -*- coding: utf-8 -*-
"""
Created on Thu Mar 26 16:13:07 2020

@author: Emma
"""

#GOAL: visualise mean geodiversity values in violin plots and p values of testing in boxplots  

#Version:No p vals V2

# - plots are without p vals (p vals code has been removed from this file)
# - random and geoparks are swtiched to match the scatterplots 
# - order has been changed to match the scatterplots 

# update july: intergrate all plots into one figure 


import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from textwrap import wrap
import numpy as np

# which variables should be plotted
plot_all = 0
 
#%% Initialisation for data boxplot part 
        
#make lists of the variable names to loop through 

#WORLD
var_world_list =  ['geodiversity139_mean', 'soils_mean',  'lithology_mean', 'slope_range_mean', 'slope_std_mean', 'Rivers139_mean', 'lakes_mean'] 
var_geopark_list = ['GDsum_stats_139', 'Soils_stats_147', 'Lithology_stats_147', 'SlopeRange_stats_147', 'SlopeSTD_stats_147', 'Rivers_stats_139', 'Lakes_stats_147' ] 
t_world_list = ['GDsum', 'SoilDiv', 'LithoDiv', 'SlopeRange', 'SlopeSTD', 'RiverLength', 'LakeArea']

#ASIA
var_asia_list =  ['Asia_60NBgeodiversity_mean', 'Asia_soils_mean', 'Asia_lithology_mean', 'Asia_slope_range_mean', 'Asia_slope_std_mean', 'Asia_60NBrivers_mean', 'Asia_lakes_mean']
var_geoparkA_list = ['GDsum_stats_61', 'Soils_stats_61', 'Lithology_stats_61', 'SlopeRange_stats_61', 'SlopeSTD_stats_61', 'Rivers_stats_61', 'Lakes_stats_61' ]

#EUROPE
var_europe_list =  ['Europe_60NBgeodiversity_mean', 'europesoils_mean', 'europelithology_mean', 'europeslope_range_mean', 'europe_slope_std_mean', 'Europe_60NBrivers_mean','europelakes_mean']
var_geoparkE_list = ['GDsum_stats_66', 'Soils_stats_74', 'Lithology_stats_74', 'SlopeRange_stats_74', 'SlopeSTD_stats_74', 'Rivers_stats_66', 'Lakes_stats_74'] 

#locations in subplots
if plot_all == 0:
    loc_list =     [0, 1, 2, 0, 1, 2, 0]
    loc_list_col = [0, 0, 0, 0, 2, 2, 0]
    letter_labels = ['A', 'B', 'D', '0', 'C', 'E', '0']

else:
    loc_list = [0, 0, 1, 2, 3, 4, 5]

#list for setting y axis limits
y_max_list = [20, 23, 8, 80, 20, 70, 1.2*10**2 ]

#list for y axis labels
y_label_list = ['GD sum', '# types', '# types', 'degrees' , 'degrees' , 'km', 'km$^2$']

#%% Make Figure 
nr_columns = 2

#Fig 1
fig = plt.figure(figsize= (10, 12), dpi=300)
fig.tight_layout() 

#fliersymbol
dot = dict(markerfacecolor='black', marker='+')

#box width
box_w1 = 0.2


#create boxplots, per row a layer, per column a continent 

for var_world, var_asia, var_europe, var_geopark, var_geoparkA, var_geoparkE, loc,\
    t_world, y_max, y_label, loc_col, letter in\
    zip(var_world_list, var_asia_list, var_europe_list, var_geopark_list, var_geoparkA_list, var_geoparkE_list, loc_list,\
        t_world_list, y_max_list, y_label_list, loc_list_col, letter_labels):
      
        #filter out NaN values before plotting
        vector_world = data_worldM['value'].loc[data_worldM['name']==var_world]
        vector_world = vector_world[~np.isnan(vector_world)]
        
        vector_geopark = data_geoparks['MEAN'].loc[data_geoparks['name']==var_geopark]
        vector_geopark = vector_geopark[~np.isnan(vector_geopark)]
        
        vector_asia = data_asiaM['value'].loc[data_asiaM['name']==var_asia]
        vector_asia = vector_asia[~np.isnan(vector_asia)]
        
        vector_geoparkA = data_geoparksEA['MEAN'].loc[data_geoparksEA['name']==var_geoparkA]
        vector_geoparkA = vector_geoparkA[~np.isnan(vector_geoparkA)]
        
        vector_europe = data_europeM['value'].loc[data_europeM['name']==var_europe]
        vector_europe = vector_europe[~np.isnan(vector_europe)]
        
        vector_geoparkE = data_geoparksEA['MEAN'].loc[data_geoparksEA['name']==var_geoparkE]
        vector_geoparkE = vector_geoparkE[~np.isnan(vector_geoparkE)]
        
        #convert river and lake data to km
        if var_world == 'Rivers139_mean':
            vector_world = vector_world/1000
            vector_geopark = vector_geopark/1000
            vector_asia = vector_asia/1000
            vector_geoparkA = vector_geoparkA/1000
            vector_europe = vector_europe/1000
            vector_geoparkE = vector_geoparkE/1000
        
        if var_world == 'lakes_mean':
            vector_world = vector_world/1E6
            vector_geopark = vector_geopark/1E6
            vector_asia = vector_asia/1E6
            vector_geoparkA = vector_geoparkA/1E6
            vector_europe = vector_europe/1E6
            vector_geoparkE = vector_geoparkE/1E6
    
        ########################## end DATA FORMATTING #######################################
        
        #make two figures. 
        #FIG1 has geodiversity sum
        #FIG2 soil diversity and lithology diversity, river length, slope std, range and lakes 
        
        ###################### SET STYLES ###################################################
        # sns.axes_style() gives current style properties 
        sns.set_style('whitegrid', {'axes.facecolor': '0.99','grid.color': '.93', 'axes.edgecolor': '.85', 'axes.labelcolor': '.25', 'xtick.color': '.35',\
                        'ytick.color': '.35', 'xtick.bottom': True})
        
        
        # plt.style.use('ggplot') #for ggplot look and feel
        sns.set_context('paper')
        
        fsize = 'large'
        
        
        ###################### END SET STYLES ##########################################
        
        #LABELS 
        xlabels = ['Global-Geoparks', 'Global-Random', 'AS-Geoparks', 'AS-Random', 'EU-Geoparks', 'EU-Random']
        xlabels2 = ['Global\nGeoparks', 'Global\nRandom', 'AS\nGeoparks', 'AS\nRandom', 'EU\nGeoparks', 'EU\nRandom']
      
        
        ################################### FIGURE 1 #########################
        
        if var_world == 'geodiversity139_mean':
            
            ################## Make Violinplot 1 #############################
            sns.set_palette(['powderblue', 'steelblue', 'lightcoral', 'indianred', 'lightgreen', 'darkseagreen'])
            plt.subplot2grid(shape = (3,4),loc = (loc, loc_col), colspan = 4)
            box = sns.boxplot(data = [vector_geopark, vector_world, vector_geoparkA, vector_asia, vector_geoparkE, vector_europe], width = box_w1, flierprops = dot) 
            box.text(-0.35, 0.9*y_max, letter, fontsize = 14)
            locs, labels = plt.xticks()
            plt.xticks(locs, xlabels)
            plt.axis(ymin = -1, ymax = y_max) #set axis limits 
            fig.tight_layout()
            plt.title(t_world + ' means', size = 13)
            plt.ylabel(y_label, size = fsize)
            ################## End Violinplot 1 ##############################
        
            #shift plots down to make room for a title 
            # fig.subplots_adjust(top=0.925)            
        
            # ### pass on to second figure ###
            # if var_world == 'geodiversity139_mean':
            #     #Fig 2
            #     fig2 = plt.figure(figsize= (11.69, 14), dpi=300)
            #     fig2.tight_layout()
             ##################### END FIGURE 1 ##############################   
                
        ########################## Make second figure  #######################   
        elif var_world == 'soils_mean' or var_world == 'lithology_mean' or var_world == 'slope_std_mean' or var_world == 'Rivers139_mean' and plot_all == 0:
            
            ###################### Begin Violinplot 2 ########################
            sns.set_palette(['powderblue', 'steelblue', 'lightcoral', 'indianred', 'lightgreen', 'darkseagreen'])
            plt.subplot2grid(shape = (3,4),loc = (loc, loc_col), colspan = 2)
            box = sns.boxplot(data = [vector_geopark, vector_world, vector_geoparkA, vector_asia, vector_geoparkE, vector_europe], width = box_w1, flierprops = dot)
            box.text(-0.25, 0.9*y_max, letter, fontsize = 14)
            plt.axis(ymin = -1, ymax = y_max) #set axis limits 
            fig.tight_layout()
            plt.title(t_world + ' means', size = 13)
            plt.ylabel(y_label, size = fsize)
            locs, labels = plt.xticks() 
            plt.xticks(locs,xlabels2)
            
            # locs, labels = plt.xticks() #only x labels in the bottom graph
            # plt.xticks(locs, xlabels)
            ##################### End Violinplot 2 ###########################
                
            
           
#shift plots down to make room for a title 
fig.subplots_adjust(top=0.925) 
        

        
    
    