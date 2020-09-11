# -*- coding: utf-8 -*-
"""
Created on Thu Mar  5 10:30:11 2020

@author: 10799478
"""

# analysis of unique soils on continents, geoparks and the world 
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


#%% set style
# sns.axes_style() gives current style properties 
sns.set_style('whitegrid', {'axes.facecolor': '0.99','grid.color': '.93', 'axes.edgecolor': '.85', 'axes.labelcolor': '.25', 'xtick.color': '.35',\
                'ytick.color': '.35', 'xtick.bottom': True, 'ytick.left': True, 'patch.edgecolor': 'k', 'patch.force_edgecolor': False,})


# plt.style.use('ggplot') #for ggplot look and feel
sns.set_context('paper')       
#%% #############################VISUALISATION #############################

#BARPLOT percentage in geopark WORLD
fig = plt.figure(figsize= (12, 10), dpi=300)

plt.subplot(1,2,1)

#sort soils_world_compare from high to low percentage
soils_world_compare = soils_world_compare.sort_values('percentage_in_geopark', ascending = False)

# list for names etc
list_soil_names = soils_world_compare.soil_name.unique().tolist()


bar1 = sns.barplot(x = 'percentage_in_geopark', y = 'soil_name', data = soils_world_compare, orient = 'h', color = 'steelblue')
plt.axis(xmin = 0, xmax = 1.2) #set axis limits
plt.xlabel('')
plt.ylabel('') 
bar1.set_yticklabels(labels = list_soil_names, size = 12, rotation = 0) 

# add label 
bar1.text(1.1, -0.5, 'A', fontsize = 14)

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
for i in range(1,30, 2):
    plt.axhspan(i-0.5, i+0.5, facecolor='0.8', alpha=0.3)

#%%BARPLOT percentage in geopark Continents 
plt.subplot(1,2,2)

all_continents = 0

#sort soils_continents_compare in the same order as soils world
soil_order = soils_world_compare.soil_name.reset_index().reset_index()
soils_continents_compare1 = soils_continents_compare.join(other = soil_order.set_index('soil_name'), on='soil_name', how='left')
soils_continents_compare1 = soils_continents_compare1.sort_values(['continent', 'level_0'], ascending = True)

# list for names etc
list_soil_names = soils_continents_compare1.soil_name.unique().tolist()
plot_data_continent = soils_continents_compare1.loc[(soils_continents_compare['continent']!='australia') & (soils_continents_compare['continent']!= 'oceania')]

if all_continents == 1:
    continent_color = ['darkorange', 'indianred', 'darkseagreen', 'gold', 'royalblue']

else:
    continent_color = ['indianred', 'darkseagreen']
    plot_data_continent = plot_data_continent.loc[(plot_data_continent['continent']=='asia') | (plot_data_continent['continent']== 'europe')]
    
bar2 = sns.barplot(x = 'percentage_in_geopark', y = 'soil_name', hue = 'continent', data = plot_data_continent, orient = 'h', palette = continent_color)
plt.axis(xmin = 0, xmax = 40) #set axis limits
plt.xlabel('')
plt.ylabel('') 
bar2.set_yticklabels(labels = '', size = 12, rotation = 0) 

#change legend location
leg = plt.legend(['World','Asia', 'Europe'],loc= [0.75, 0.8], fontsize = 12, framealpha = 0.8)

for l in leg.legendHandles:            
    l.set_linewidth(7)
    
leg.legendHandles[0].set_color('steelblue')
leg.legendHandles[1].set_color('indianred')
leg.legendHandles[2].set_color('darkseagreen')
    

#add label
bar2.text(37, -0.5, 'B', fontsize = 14)

#add shading
for i in range(1,30, 2):
    plt.axhspan(i-0.5, i+0.5, facecolor='0.8', alpha=0.3)
    
#add common axes 
fig.add_subplot(1,1,1, frameon=False)
# hide tick and tick label of the big axes
plt.tick_params(labelcolor='none', top=False, bottom=False, left=False, right=False)
plt.grid(False)
plt.xlabel(r'A%$_{geoparks}$', size = 'x-large')

fig.tight_layout()
