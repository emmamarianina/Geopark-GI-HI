# -*- coding: utf-8 -*-
"""
Created on Wed Jul 22 15:50:00 2020

@author: Emma
"""

#%% PLOT CORRELATIONS IN HISTOGRAM with confidence intervals. Worls, AS and EU together 

#data to be plotted
data_plot_list = [corr_world, corr_asia, corr_europe]
data_plot_g_list = [corr_geopark_world, corr_geopark_asia, corr_geopark_europe]
data_corr_list = [corr_interval_world, corr_interval_asia, corr_interval_europe]

#add letters
letter1 = ['A1', 'B1', 'C1', 'A1', 'D1', 'B1']
letter2 = ['A2', 'B2', 'C2', 'A2', 'D2', 'B2']
letter3 = ['A3', 'B3', 'C3', 'A3', 'D3', 'B3']
    
#lists to loop through 
layer_list = ['soils', 'lithology', 'rivers', 'slope_range', 'slope_std', 'lakes']  #this is to make it to match the order of other figures #corr_world.layer.unique().tolist()
plot_loc = [1,2,3,0,4,0]
subplot_loc_list = [0, 4, 8]
title_list = ['SoilDiv', 'LithoDiv', 'RiverLength', 'SlopeRange', 'SlopeSTD', 'LakeArea']
scale_list = ['World: ', 'Asia: ', 'Europe: ']
letter_list = [letter1, letter2, letter3]
letter_index = [0,1,2,3,4,5]

#figure initialisation
fig = plt.figure(figsize= (12, 8), dpi=300)
# fig.suptitle('Distributions of random sample geodiversity-sub layer correlations compared to geopark correlations')

for data_plot, data_plot_g, data_corr, subplot_loc, scale, letter in zip(data_plot_list, data_plot_g_list, data_corr_list, subplot_loc_list, scale_list, letter_list):
    for layer, loc, title, l_index in zip(layer_list, plot_loc, title_list, letter_index):
        
        if layer == 'soils' or layer == 'lithology' or layer == 'slope_std' or layer == 'rivers':
            plot_vector = data_plot['correlation'].loc[data_plot['layer']==layer] #select correlations to plot
            plt.subplot(3,4,loc + subplot_loc) #location of subpot
            plt.hist(plot_vector, bins=np.arange(min(plot_vector), max(plot_vector) + 0.04, 0.04), color = 'darkblue') #make histogram with set nr of bins
            
            #lay out and title things
            plt.xlim(-0.5,1)
            plt.ylim(0, 40)
            fig.tight_layout() #pad=3.0) #this makes sure the figures do not overlap. if only () it minimises the distance between the subplots
            
            #plot vertical lines for interval and geopark correlation
            plt.vlines(data_plot_g['correlation'].loc[data_plot_g['layer']==layer], 0, 40, colors='r', linestyles = 'dashed', label = r'$r_s$ geoparks')
            lower = data_corr['lower'].loc[data_corr['layer']==layer].values[0]
            upper = data_corr['upper'].loc[data_corr['layer']==layer].values[0]
            plt.axvspan(xmin = lower, xmax = upper, ymin = 0, ymax = 1, facecolor='gray', alpha=0.3, label = '95% CI')
            
            #display the nr of correlations used for the histogram in each plot (because columns with nans were omitted when calculating correlations)
            if subplot_loc + loc == 1:
                # plt.text(-0.4, 1, 'N = '+ str(len(plot_vector)), verticalalignment = 'bottom', horizontalalignment = 'left')
                t = plt.text(0.95, 39, 'N = '+ str(len(plot_vector)), verticalalignment = 'top', horizontalalignment = 'right')
            else:
                t = plt.text(0.95, 39, 'N = '+ str(len(plot_vector)), verticalalignment = 'top', horizontalalignment = 'right')
                t.set_bbox(dict(facecolor='white', alpha=0.3, edgecolor=None))
            
            #titles
            plt.title(letter[l_index]+'. '+scale+title, size = 14)
        
            # #remove xticks in upper rows
            # if loc != 16:
            plt.xticks(size ='medium' )
            
            #only yticks in first column
            if loc != 1:
                plt.yticks([], size = 'small')
                
            plt.grid(False)
    
            #plot legend 
            if loc + subplot_loc ==1:
                plt.legend(loc = 'upper left', frameon = True, fancybox =True)
            
            #add common axes 
            fig.add_subplot(1,1,1, frameon=False)
            # hide tick and tick label of the big axes
            plt.tick_params(labelcolor='none', top=False, bottom=False, left=False, right=False)
            plt.grid(False)
            plt.xlabel("Correlation", size = 'x-large')
            plt.ylabel("Count", size = 'x-large')
            
fig.tight_layout()
                        
    #shift plots down to make room for a title 
    # fig.subplots_adjust(top=0.925) 
                
#%% PLOT CORRELATIONS IN HISTOGRAM FOR APPENDIX

#data to be plotted
data_plot_list = [corr_world, corr_asia, corr_europe]
data_plot_g_list = [corr_geopark_world, corr_geopark_asia, corr_geopark_europe]
data_corr_list = [corr_interval_world, corr_interval_asia, corr_interval_europe]
    
#lists to loop through 
layer_list = ['soils', 'lithology', 'rivers', 'slope_range', 'slope_std', 'lakes']  #this is to make it to match the order of other figures #corr_world.layer.unique().tolist()
plot_loc = [1,4,10,1,7,2]
subplot_loc_list = [0, 2, 4]
title_list = ['SoilDiv', 'LithoDiv', 'RiverLength', 'SlopeRange', 'SlopeSTD', 'LakeArea']
scale_list = ['World: ', 'Asia: ', 'Europe: ']

#figure initialisation
fig = plt.figure(figsize= (12, 8), dpi=300)
# fig.suptitle('Distributions of random sample geodiversity-sub layer correlations compared to geopark correlations')

for data_plot, data_plot_g, data_corr, subplot_loc, scale, letter in zip(data_plot_list, data_plot_g_list, data_corr_list, subplot_loc_list, scale_list, letter_list):
    for layer, loc, title, l_index in zip(layer_list, plot_loc, title_list, letter_index):
        
        if layer == 'slope_range' or layer == 'lakes':
            plot_vector = data_plot['correlation'].loc[data_plot['layer']==layer] #select correlations to plot
            plt.subplot(3,2,loc + subplot_loc) #location of subpot
            plt.hist(plot_vector, bins=np.arange(min(plot_vector), max(plot_vector) + 0.04, 0.04), color = 'darkblue') #make histogram with set nr of bins
            
            #lay out and title things
            plt.xlim(-0.5,1)
            plt.ylim(0, 45)
            fig.tight_layout() #pad=3.0) #this makes sure the figures do not overlap. if only () it minimises the distance between the subplots
            
            #plot vertical lines for interval and geopark correlation
            plt.vlines(data_plot_g['correlation'].loc[data_plot_g['layer']==layer], 0, 45, colors='r', linestyles = 'dashed', label = r'$r_s$ geoparks')
            lower = data_corr['lower'].loc[data_corr['layer']==layer].values[0]
            upper = data_corr['upper'].loc[data_corr['layer']==layer].values[0]
            plt.axvspan(xmin = lower, xmax = upper, ymin = 0, ymax = 1, facecolor='gray', alpha=0.3, label = '95% CI')
            
            #display the nr of correlations used for the histogram in each plot (because columns with nans were omitted when calculating correlations)
            if subplot_loc + loc == 1:
                # plt.text(-0.4, 1, 'N = '+ str(len(plot_vector)), verticalalignment = 'bottom', horizontalalignment = 'left')
                t = plt.text(0.95, 44, 'N = '+ str(len(plot_vector)), verticalalignment = 'top', horizontalalignment = 'right')
            else:
                t = plt.text(0.95, 44, 'N = '+ str(len(plot_vector)), verticalalignment = 'top', horizontalalignment = 'right')
                t.set_bbox(dict(facecolor='white', alpha=0.3, edgecolor=None))
            
            #titles
            plt.title(letter[l_index]+'. '+scale+title, size = 14)
        
            # #remove xticks in upper rows
            # if loc != 16:
            plt.xticks(size ='medium' )
            
            if loc != 1:
                plt.yticks([], size = 'small')
                
            plt.grid(False)
    
            #plot legend 
            if loc + subplot_loc ==1:
                plt.legend(loc = 'upper left', frameon = True, fancybox =True)
            
            #add common axes 
            fig.add_subplot(1,1,1, frameon=False)
            # hide tick and tick label of the big axes
            plt.tick_params(labelcolor='none', top=False, bottom=False, left=False, right=False)
            plt.grid(False)
            plt.xlabel("Correlation", size = 'x-large')
            plt.ylabel("Count", size = 'x-large')
            
fig.tight_layout()
                        
    #shift plots down to make room for a title 
    # fig.subplots_adjust(top=0.925) 
                