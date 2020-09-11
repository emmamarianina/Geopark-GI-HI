# -*- coding: utf-8 -*-
"""
Created on Thu May 28 16:59:01 2020

@author: Emma
"""

import pandas as pd
# import geopandas
# import os
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

#%% set style
# sns.axes_style() gives current style properties 
sns.set_style('whitegrid', {'axes.facecolor': '0.99','grid.color': '.93', 'axes.edgecolor': '.85', 'axes.labelcolor': '.25', 'xtick.color': '.35',\
                'ytick.color': '.35', 'xtick.bottom': True, 'patch.edgecolor': 'k', 'patch.force_edgecolor': False,})


# plt.style.use('ggplot') #for ggplot look and feel
sns.set_context('paper')



#%% ############ VISUALISE ################# WOLRD 
fig = plt.figure(figsize= (12, 8), dpi=300)

    
# list for names etc
# list_lit1 = ['ev', 'mt', 'pa', 'pb', 'pi', 'py', 'sc', 'sm', 'ss', 'su', 'va', 'vb', 'vi', 'wb', 'ig', 'nd']

# list_litho_name2 = ['Evaporites', 'Metamorphic rocks', 'Acid plutonic rocks', 'Basic plutonic rocks',\
#                        'Intermediate plutonic rocks', 'Pyroclastics', 'Carbonate sedimentary rocks',\
#                            'Mixed sedimentary rocks', 'Siliciclastic sedimentary rocks', 'Unconsolidated sediments',\
#                                'Acid volcanic rocks', 'Basic volcanic rocks', 'Intermediate volcanic rocks',\
#                                    'Water Bodies', 'Ice and glaciers', 'No data'] # used for the legend 

#legend key is in the file where the data is loaded 
#add long names to data
lit1_compare = lit1_compare.join(legend_key.set_index('lithology_name'), on = 'lithology', rsuffix = '_x')

list_color = ['rebeccapurple', 'thistle', 'lightcoral', 'indianred', 'firebrick', 'lightsteelblue', 'goldenrod', 'gold', 'khaki', 'tan',\
              'seagreen', 'mediumseagreen', 'darkseagreen', 'dodgerblue', 'azure', 'black']  
    
plt.subplot(1,2,1)

lit1_compare = lit1_compare.sort_values(by = 'percentage_in_geopark', ascending=False,)
    
bar1 = sns.barplot(x = 'percentage_in_geopark', y = 'lithology_name', data = lit1_compare, orient = 'h', color = 'steelblue')
plt.axis(xmin = 0, xmax = 1) #set axis limits
plt.xlabel('')
plt.ylabel('') 
bar1.set_yticklabels(labels = lit1_compare.lithology_name, size = 14, rotation = 0)
fig.tight_layout()

# add label 
bar1.text(0.93, 0.1, 'A', fontsize = 14)

#change legend location
# plt.legend(['World'],loc=4, borderaxespad=0.8)

# Change barwidth
newwidth = 0.4

# Loop over the bars, and adjust the width and center bars around the x tick
for bar in bar1.patches:
    x = bar.get_y()
    width = bar.get_height()
    centre = x+width/2.
    bar.set_y(centre-newwidth/2.)
    bar.set_height(newwidth)

#add shading
for i in range(1,16, 2):
    plt.axhspan(i-0.5, i+0.5, facecolor='0.8', alpha=0.3)
    

 
##################################################################################
    
#%% ############ VISUALISE ################# CONTINENTS
# fig = plt.figure(figsize= (8, 8), dpi=300)

#only plot europe and asia
plot_data_C = lit1_compare_C[['continent', 'lithology', 'percentage_in_geopark', 'lithology_name']].loc[(lit1_compare_C['continent']=='asia') | (lit1_compare_C['continent']== 'europe')]

#add long names to the data
plot_data_C = plot_data_C.join(legend_key.set_index('lithology_name'), on = 'lithology', rsuffix = '_x')

#sort soils_continents_compare in the same order as soils world
lit_order = lit1_compare.lithology_name.reset_index().reset_index()
plot_data_C1 = plot_data_C.join(other = lit_order.set_index('lithology_name'), on='lithology_name', how='left')
plot_data_C1 = plot_data_C1.sort_values(['continent', 'level_0'], ascending = True)

#list of colors for the continents 
# continent_color = ['darkorange', 'indianred', 'darkseagreen', 'gold', 'royalblue']
continent_color = [ 'indianred', 'darkseagreen']

#plot all 
plt.subplot(1,2,2)
bar2 = sns.barplot(x = 'percentage_in_geopark', y = 'lithology_name', hue = 'continent', data = plot_data_C1, orient = 'h', palette = continent_color)
plt.axis(xmin = 0, xmax = 20) #set axis limits
plt.xlabel('')
plt.ylabel('') 
bar2.set_yticklabels(labels = [''], size = 14, rotation = 0)
fig.tight_layout()

#change legend location
leg = plt.legend(['World','Asia', 'Europe'],loc= [0.7, 0.8], fontsize = 12, framealpha = 0.8)

for l in leg.legendHandles:            
    l.set_linewidth(7)
    
leg.legendHandles[0].set_color('steelblue')
leg.legendHandles[1].set_color('indianred')
leg.legendHandles[2].set_color('darkseagreen')
    

#add label
bar2.text(18, 0.1, 'B', fontsize = 14)

#add shading
for i in range(1,16, 2):
    plt.axhspan(i-0.5, i+0.5, facecolor='0.8', alpha=0.3)
    
#add common axes 
fig.add_subplot(1,1,1, frameon=False)
# hide tick and tick label of the big axes
plt.tick_params(labelcolor='none', top=False, bottom=False, left=False, right=False)
plt.grid(False)
plt.xlabel(r'A%$_{geoparks}$', size = 'x-large')
