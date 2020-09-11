# -*- coding: utf-8 -*-
"""
Created on Thu Mar 26 16:13:07 2020

@author: Emma
"""

#GOAL: visualise mean geodiversity values in violin plots and p values of testing in boxplots  

#Version:No p vals V2

# - plots are without p vals (p vals code has been removed from this file)
# - random and geoparks are swtiched to match the scatterplots 

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from textwrap import wrap
import numpy as np

 
#%% Initialisation for data boxplot part 
        
#make lists of the variable names to loop through 

#WORLD
var_world_list =  ['HF_1993_mean', 'HF_2009_mean', 'HF_change_mean', 'gHM_mean'] 
var_geopark_list = ['HF1993_stats_147', 'HF2009_stats_147', 'HFchange_stats_147', 'gHM_stats_147'] 
t_world_list = ['HF 1993', 'HF 2009', 'HF change', 'gHM 2016']

#ASIA
var_asia_list =  ['HF1993_Asia_mean', 'HF2009_Asia_mean', 'HFchange_Asia_mean', 'gHM_Asia_mean']
var_geoparkA_list = ['HF1993_stats_61', 'HF2009_stats_61', 'HFchange_stats_61', 'gHM_stats_61']

#EUROPE
var_europe_list =  ['HF1993_Europe_mean', 'HF2009_Europe_mean', 'HFchange_Europe_mean', 'gHM_Europe_mean']
var_geoparkE_list = ['HF1993_stats_74', 'HF2009_stats_74', 'HFchange_stats_74', 'gHM_stats_74'] 

#locations in subplots
loc_list = [0, 0, 1, 1]

#letter labels
letter_label = ['A', 'A', 'B', 'B']

#list for setting y axis limits
y_min_list = [-1, -1, -11, -0.1]
y_max_list = [50, 50, 20, 1]

#list for y axis labels
y_label_list = ['HF', 'HF', 'HF 2009-1993', 'gHM']


#%% Make Figure for report 
nr_columns = 2

#Fig 1
fig = plt.figure(figsize= (11.69, 11.69), dpi=300)
fig.tight_layout() 

#fliersymbol
dot = dict(markerfacecolor='black', marker='+')

#box width
box_w1 = 0.2

#create boxplots, per row a layer, per column a continent 

for var_world, var_asia, var_europe, var_geopark, var_geoparkA, var_geoparkE, loc,\
    t_world, y_min, y_max, y_label, letter in\
    zip(var_world_list, var_asia_list, var_europe_list, var_geopark_list, var_geoparkA_list, var_geoparkE_list, loc_list,\
        t_world_list, y_min_list, y_max_list, y_label_list, letter_label):
      
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
        
        ########################## end DATA FORMATTING #######################################
        
        #make three figures. 
        #FIG1 has geodiversity sum
        #FIG2 soil diversity and lithology diversity, river length
        #FIG3 has slope std, range and lakes 
        
        
        
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
        ################################### FIGURE 1 #########################
        if var_world == 'HF_2009_mean' or var_world == 'HF_change_mean':  
            ################## Make Violinplot 1 #############################
            sns.set_palette(['powderblue', 'steelblue', 'lightcoral', 'indianred', 'lightgreen', 'darkseagreen'])
            plt.subplot2grid(shape = (4,4),loc = (loc, 0), colspan = 3)
            box = sns.boxplot(data = [vector_geopark, vector_world, vector_geoparkA, vector_asia, vector_geoparkE, vector_europe], width = box_w1, flierprops = dot) 
            box.text(-0.35, y_max-(0.1*(y_max-y_min)), letter, fontsize = 14)
            locs, labels = plt.xticks()
            plt.xticks(locs, xlabels)
            plt.axis(ymin = y_min, ymax = y_max) #set axis limits 
            fig.tight_layout()
            plt.title(t_world + ' means', size = 13)
            plt.ylabel(y_label, size = fsize)
            ################## End Violinplot 1 ##############################
fig.tight_layout()          

#%% Make Figure for appendix 
nr_columns = 2

#Fig 1
fig = plt.figure(figsize= (11.69, 11.69), dpi=300)
fig.tight_layout() 

#fliersymbol
dot = dict(markerfacecolor='black', marker='+')

#box width
box_w1 = 0.2

#create boxplots, per row a layer, per column a continent 

for var_world, var_asia, var_europe, var_geopark, var_geoparkA, var_geoparkE, loc,\
    t_world, y_min, y_max, y_label, letter in\
    zip(var_world_list, var_asia_list, var_europe_list, var_geopark_list, var_geoparkA_list, var_geoparkE_list, loc_list,\
        t_world_list, y_min_list, y_max_list, y_label_list, letter_label):
      
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
        
        ########################## end DATA FORMATTING #######################################
        
        #make three figures. 
        #FIG1 has geodiversity sum
        #FIG2 soil diversity and lithology diversity, river length
        #FIG3 has slope std, range and lakes 
        
        
        
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
        ################################### FIGURE 1 #########################
        if var_world == 'HF_1993_mean' or var_world == 'gHM_mean':  
            ################## Make Violinplot 1 #############################
            sns.set_palette(['powderblue', 'steelblue', 'lightcoral', 'indianred', 'lightgreen', 'darkseagreen'])
            plt.subplot2grid(shape = (4,4),loc = (loc, 0), colspan = 3)
            box = sns.boxplot(data = [vector_geopark, vector_world, vector_geoparkA, vector_asia, vector_geoparkE, vector_europe], width = box_w1, flierprops = dot) 
            box.text(-0.35, y_max-(0.1*(y_max-y_min)), letter, fontsize = 14)
            locs, labels = plt.xticks()
            plt.xticks(locs, xlabels)
            plt.axis(ymin = y_min, ymax = y_max) #set axis limits 
            fig.tight_layout()
            plt.title(t_world + ' means', size = 13)
            plt.ylabel(y_label, size = fsize)
            ################## End Violinplot 1 ##############################
fig.tight_layout()          
       
            
        
        
    
         
            
        
        
    
    