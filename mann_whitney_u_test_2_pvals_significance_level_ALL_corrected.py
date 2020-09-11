# -*- coding: utf-8 -*-
"""
Created on Tue Apr 14 15:22:57 2020

@author: Emma
"""
import pandas as pd

#make a table with for every layer with the % of significant p-values 

#list with layers 
list_gd = ['GDsum', 'Lakes', 'Lithology', 'SlopeRange', 'SlopeSTD', 'Soils', 'Rivers']
list_hf = ['HF1993', 'HF2009', 'HFchange', 'gHM']

#significance level
sig_lvl1 = 0.05

#make empty dataframe
column_names = ['global', 'Asia', 'Europe']
# column2 = [('global', '0.05'),('global', '0.0005'), ('Asia', '0.05'), ('Asia', '0.0005'), ('Europe', '0.05'), ('Europe', '0.0005')]
geodiversity_table = pd.DataFrame(columns = column_names)
# geodiversity_table.columns = pd.MultiIndex.from_tuples(column2)

human_influence_table = pd.DataFrame(columns = column_names)
# human_influence_table.columns = pd.MultiIndex.from_tuples(column2)

#%% table geodiversity

for layer_gd in list_gd:
    p_world = p_vals_world_corrected['p_val'].loc[p_vals_world['layer']==layer_gd]
    p_asia = p_vals_asia_corrected['p_val'].loc[p_vals_asia['layer']==layer_gd]
    p_europe = p_vals_europe_corrected['p_val'].loc[p_vals_europe['layer']==layer_gd]

    #get the total amount of p values
    world_all = len(p_world)
    asia_all = len(p_asia)
    europe_all = len(p_europe)
    
    #get the number of tests that is smaller than the significance level
    world_smaller1 = len(p_world[p_world < sig_lvl1]) 
    asia_smaller1 = len(p_asia[p_asia < sig_lvl1]) 
    europe_smaller1 = len(p_europe[p_europe < sig_lvl1]) 
    
    # world_smaller2 = len(p_world[p_world < sig_lvl2]) 
    # asia_smaller2 = len(p_asia[p_asia < sig_lvl2]) 
    # europe_smaller2 = len(p_europe[p_europe < sig_lvl2]) 
    
    #calculate percentages
    world_perc1 = world_smaller1/world_all*100
    asia_perc1 = asia_smaller1/asia_all*100
    europe_perc1 = europe_smaller1/europe_all*100
    
    # world_perc2 = world_smaller2/world_all*100
    # asia_perc2 = asia_smaller2/asia_all*100
    # europe_perc2 = europe_smaller2/europe_all*100
    
    #write everything to the dataframe 
    geodiversity_table.loc[layer_gd] = [world_perc1, asia_perc1, europe_perc1]

#%% table human influence
    
for layer_hf in list_hf:
    p_world = p_vals_world_corrected['p_val'].loc[p_vals_world['layer']==layer_hf]
    p_asia = p_vals_asia_corrected['p_val'].loc[p_vals_asia['layer']==layer_hf]
    p_europe = p_vals_europe_corrected['p_val'].loc[p_vals_europe['layer']==layer_hf]

    #get the total amount of p values
    world_all = len(p_world)
    asia_all = len(p_asia)
    europe_all = len(p_europe)
    
    #get the number of tests that is smaller than the significance level
    world_smaller1 = len(p_world[p_world < sig_lvl1]) 
    asia_smaller1 = len(p_asia[p_asia < sig_lvl1]) 
    europe_smaller1 = len(p_europe[p_europe < sig_lvl1]) 
    
    # world_smaller2 = len(p_world[p_world < sig_lvl2]) 
    # asia_smaller2 = len(p_asia[p_asia < sig_lvl2]) 
    # europe_smaller2 = len(p_europe[p_europe < sig_lvl2]) 
    
    #calculate percentages
    world_perc1 = world_smaller1/world_all*100
    asia_perc1 = asia_smaller1/asia_all*100
    europe_perc1 = europe_smaller1/europe_all*100
    
    # world_perc2 = world_smaller2/world_all*100
    # asia_perc2 = asia_smaller2/asia_all*100
    # europe_perc2 = europe_smaller2/europe_all*100
    
    #write everything to the dataframe 
    human_influence_table.loc[layer_hf] = [world_perc1, asia_perc1, europe_perc1]

#%% visualise 
import matplotlib.pyplot as plt

# fig = plt.figure(figsize= (11.69, 4.27), dpi=300)
# ax = plt.subplot(111, frame_on=False)
# ax.xaxis.set_visible(False)  # hide the x axis
# ax.yaxis.set_visible(False)  # hide the y axis
# pd.plotting.table(ax, human_influence_table)

fig = plt.figure(figsize= (8.27, 8.27), dpi=300)
import seaborn as sns
sns.heatmap(geodiversity_table, cmap = 'BuGn_r', annot = True, cbar = False, square = False)