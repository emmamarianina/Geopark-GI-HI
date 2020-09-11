# -*- coding: utf-8 -*-
"""
Created on Wed Apr 15 10:33:08 2020

@author: Emma
"""
from statsmodels.stats.diagnostic import lilliefors
from scipy.stats import t
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


# GOAL: perform the analysis on the correlations betwee GDsum and geodiversity sublayers (calculated in "correlations_calculate_all.py")
# WORLD, ASIA and EUROPE
# input datasets random samples: corr_world, corr_asia, corr_europe
# input datasets geopark samples: corr_geoparks_world, corr_geopark_asia, corr_geopark_europe

#%% check if random sample distributions are NORMALLY DISTRIBUTED 
# in order to to give extra reasoning to calculate confidence intervals assuming normal distribution
# Lilliefors test to see if data is normally distributed
    
layer_list = corr_world.layer.unique().tolist()

perform_lilliefors = 0

if perform_lilliefors == 1:

    for layer in layer_list:
        
        stat, p = lilliefors(corr_world['correlation'].loc[corr_world['layer']==layer], pvalmethod = 'table')
        print('Statistics=%.3f, p=%.3f' % (stat, p))
        # interpret
        alpha = 0.05
        if p > alpha:
        	print('world ' + layer + ' looks Gaussian (fail to reject H0)')
        else:
        	print('world ' + layer + ' does not look Gaussian (reject H0)')
            
        stat, p = lilliefors(corr_asia['correlation'].loc[corr_asia['layer']==layer], pvalmethod = 'table')
        print('Statistics=%.3f, p=%.3f' % (stat, p))
        # interpret
        alpha = 0.05
        if p > alpha:
        	print('Asia ' + layer + ' looks Gaussian (fail to reject H0)')
        else:
        	print('Asia ' + layer + ' does not look Gaussian (reject H0)')
        
        stat, p = lilliefors(corr_europe['correlation'].loc[corr_europe['layer']==layer], pvalmethod = 'table')
        print('Statistics=%.3f, p=%.3f' % (stat, p))
        # interpret
        alpha = 0.05
        if p > alpha:
        	print('Europe ' + layer + ' looks Gaussian (fail to reject H0)')
        else:
        	print('Europe ' + layer + ' does not look Gaussian (reject H0)')

#%% Check if the geopark correlation falls within the 95% confidence interval of the random samples distributions
# Calculate the sample mean (X) and sample std (s) from the distribution data. 
# 95% confidence interval is mean+-1.96*std

#use confidence intervals
confidence = 0.95 #set confidence level on 95%

#list to loop through, dataframe to store in
data_list = [corr_world, corr_asia, corr_europe]
data_name_list = ['corr_world', 'corr_asia', 'corr_europe']
layer_list = corr_world.layer.unique().tolist()
corr_interval_world = pd.DataFrame(columns= ['layer', 'lower', 'upper', 'interval' , 'mean', 'std', 'n', 't'])
corr_interval_asia = pd.DataFrame(columns= ['layer', 'lower', 'upper', 'interval' , 'mean', 'std', 'n', 't'])
corr_interval_europe = pd.DataFrame(columns= ['layer', 'lower', 'upper', 'interval' , 'mean', 'std', 'n', 't'])
 
for data, data_name in zip(data_list, data_name_list):   
    for layer in layer_list:
        corr_vector = data['correlation'].loc[data['layer']==layer]
        n = len(corr_vector) #number of observations (correlations)
        corr_mean = corr_vector.mean() #calculate estimated mean 
        corr_std = corr_vector.std(ddof = 1) #calculate estimated std, by adding ddof = 1
        t_stat = t.ppf((1+confidence)/2, n-1) #calculate the t statistic you need for this confidence level and dofs
        
        #calculate upper and lower boundary and interval
        
        #this code calculates the 95% CI of the population mean, so probably not what I am looking for
        # corr_low = corr_mean - t_stat*(corr_std/math.sqrt(n)) #t_score * estimated std/sqrt(n), so t_Score*standard error
        # corr_up  = corr_mean + t_stat*(corr_std/math.sqrt(n))
        
        #This calculates the interval in which 95% of the data lies assuming a t-distribution with n-1 dofs; Confidence LEVEL?
        corr_low = corr_mean - t_stat*corr_std #t_score * estimated std
        corr_up  = corr_mean + t_stat*corr_std
        corr_interval = corr_up-corr_low
        
        if data_name == 'corr_world':
            corr_interval_world = corr_interval_world.append({'layer': layer, 'lower': corr_low, 'upper': corr_up,'interval': corr_interval,\
                                                              'mean':corr_mean, 'std': corr_std, 'n': n, 't': t_stat}, ignore_index = True)
        if data_name == 'corr_asia':
            corr_interval_asia = corr_interval_asia.append({'layer': layer, 'lower': corr_low, 'upper': corr_up,'interval': corr_interval,\
                                                              'mean':corr_mean, 'std': corr_std, 'n': n, 't': t_stat}, ignore_index = True)
        if data_name == 'corr_europe':
            corr_interval_europe = corr_interval_europe.append({'layer': layer, 'lower': corr_low, 'upper': corr_up,'interval': corr_interval,\
                                                              'mean':corr_mean, 'std': corr_std, 'n': n, 't': t_stat}, ignore_index = True)

#%% Make TABLE
# Make a table which summarises all correlation results

#dataframe to store; use multi-index  
column_names = [('global', 'geoparks'),('global', 'random samples lower'), ('global', 'random samples upper'),\
               ('Asia', 'geoparks'), ('Asia', 'random samples lower'), ('Asia', 'random samples upper'),\
               ('Europe', 'geoparks'), ('Europe', 'random samples lower'), ('Europe', 'random samples upper')]
corr_summary = pd.DataFrame(columns = column_names)
corr_summary.columns = pd.MultiIndex.from_tuples(column_names)

#list to loop through
layer_list = corr_geopark_world.layer.unique().tolist()
title_list = ['soil diversity', 'slope std', 'slope range', 'river length', 'lake area', 'lithology diversity']

for layer, title in zip(layer_list, title_list):
    
    #geopark correlations
    geopark_w = corr_geopark_world['correlation'].loc[corr_geopark_world['layer']==layer].values[0]
    geopark_a = corr_geopark_asia['correlation'].loc[corr_geopark_asia['layer']==layer].values[0]
    geopark_e = corr_geopark_europe['correlation'].loc[corr_geopark_europe['layer']==layer].values[0]
    
    #random sample intervals
    lower_w = corr_interval_world['lower'].loc[corr_interval_world['layer']==layer].values[0]
    upper_w = corr_interval_world['upper'].loc[corr_interval_world['layer']==layer].values[0]
    lower_a = corr_interval_asia['lower'].loc[corr_interval_asia['layer']==layer].values[0]
    upper_a = corr_interval_asia['upper'].loc[corr_interval_asia['layer']==layer].values[0]
    lower_e = corr_interval_europe['lower'].loc[corr_interval_europe['layer']==layer].values[0]
    upper_e = corr_interval_europe['upper'].loc[corr_interval_europe['layer']==layer].values[0]

    
    #write everything to the dataframe 
    corr_summary.loc[title] = [geopark_w, lower_w, upper_w, geopark_a, lower_a, upper_a, geopark_e, lower_e, upper_e]
#%% VISUALISATION

#FIRST code is for plotting correlations for one dataset (world, Asia or Europe) in one plot
#SECOND code is for plotting all correlations in the same figure

#plot parameters
labsize = 20
nr_bins = 'rice'

#Lay out parameters  
sns.set_palette('muted')

sns.axes_style() #gives current style properties 
sns.set_style('whitegrid', {'axes.facecolor': '0.99','grid.color': '.93', 'axes.edgecolor': '.85', 'axes.labelcolor': '.25', 'xtick.color': '.35',\
                'ytick.color': '.35', 'xtick.bottom': True})

# plt.style.use('ggplot') #for ggplot look and feel
# sns.set_context('paper')

#%% PLOT CORRELATIONS IN HISTOGRAM with confidence intervals. Worls, AS and EU separate 

plot_1 = 0

if plot_1 == 1:
    #data to be plotted
    data_plot = corr_world
    data_plot_g = corr_geopark_world
    data_name =  'World'
    data_corr = corr_interval_world
        
    #lists to loop through 
    layer_list = data_plot.layer.unique().tolist()
    plot_loc = [1,2,3,4,5,6]
    
    #figure initialisation
    fig = plt.figure(figsize= (8.27, 8.27), dpi=300)
    fig.suptitle(data_name+': Distributions of random sample geodiversity-sub layer correlations compared to geopark correlations')
    
    
    for layer, loc in zip(layer_list, plot_loc):
        plot_vector = data_plot['correlation'].loc[data_plot['layer']==layer] #select correlations to plot
        plt.subplot(3,2,loc) #location of subpot
        plt.hist(plot_vector, bins = nr_bins) #make histogram with set nr of bins
        
        #lay out and title things
        plt.title(layer)
        plt.xlim(-0.5,1)
        plt.ylim(0, 20)
        fig.tight_layout(pad=3.0) #this makes sure the figures do not overlap. if only () it minimises the distance between the subplots
        
        #plot vertical lines for interval and geopark correlation
        plt.vlines(data_plot_g['correlation'].loc[data_plot_g['layer']==layer], 0, 10, colors='r', linestyles = 'solid', label = r'$r_s$ geoparks')
        # plt.vlines(data_corr['lower'].loc[data_corr['layer']==layer], 0, 10, colors='g', linestyles = 'dashed', label = '95% confidence interval')
        # plt.vlines(data_corr['upper'].loc[data_corr['layer']==layer], 0, 10, colors='g', linestyles = 'dashed')
        lower = data_corr['lower'].loc[data_corr['layer']==layer].values[0]
        upper = data_corr['upper'].loc[data_corr['layer']==layer].values[0]
        plt.axvspan(xmin = lower, xmax = upper, ymin = 0, ymax = 1, facecolor='green', alpha=0.3, label = '95% CI')
        #display the nr of correlations used for the histogram in each plot (because columns with nans were omitted when calculating correlations)
        plt.text(0.98, 19, 'N = '+ str(len(plot_vector)), verticalalignment = 'top', horizontalalignment = 'right')
        
        #plot legend 
        if loc ==1:
            plt.legend(loc = 'upper left')

#%% PLOT CORRELATIONS IN HISTOGRAM with confidence intervals. Worls, AS and EU together 

if plot_1 == 1:
    #data to be plotted
    data_plot_list = [corr_world, corr_asia, corr_europe]
    data_plot_g_list = [corr_geopark_world, corr_geopark_asia, corr_geopark_europe]
    data_corr_list = [corr_interval_world, corr_interval_asia, corr_interval_europe]
        
    #lists to loop through 
    layer_list = ['soils', 'lithology', 'rivers', 'slope_range', 'slope_std', 'lakes']  #this is to make it to match the order of other figures #corr_world.layer.unique().tolist()
    plot_loc = [1,4,7,10,13,16]
    subplot_loc_list = [0, 1, 2]
    title_list = ['SoilDiv', 'LithoDiv', 'RiverLength', 'SlopeRange', 'SlopeSTD', 'LakeArea']
    scale_list = ['\ World', '\ Asia', '\ Europe']
    
    #figure initialisation
    fig = plt.figure(figsize= (8.27, 11.69), dpi=300)
    fig.suptitle('Distributions of random sample geodiversity-sub layer correlations compared to geopark correlations')
    
    for data_plot, data_plot_g, data_corr, subplot_loc, scale in zip(data_plot_list, data_plot_g_list, data_corr_list, subplot_loc_list, scale_list):
        for layer, loc, title in zip(layer_list, plot_loc, title_list):
            plot_vector = data_plot['correlation'].loc[data_plot['layer']==layer] #select correlations to plot
            plt.subplot(6,3,loc + subplot_loc) #location of subpot
            plt.hist(plot_vector, bins = nr_bins, color = 'darkblue',  rwidth = 2) #make histogram with set nr of bins
            
            #lay out and title things
            plt.xlim(-0.5,1)
            plt.ylim(0, 30)
            fig.tight_layout() #pad=3.0) #this makes sure the figures do not overlap. if only () it minimises the distance between the subplots
            
            #plot vertical lines for interval and geopark correlation
            plt.vlines(data_plot_g['correlation'].loc[data_plot_g['layer']==layer], 0, 30, colors='r', linestyles = 'dashed', label = r'$r_s$ geoparks')
            # plt.vlines(data_corr['lower'].loc[data_corr['layer']==layer], 0, 10, colors='g', linestyles = 'dashed', label = '95% confidence interval')
            # plt.vlines(data_corr['upper'].loc[data_corr['layer']==layer], 0, 10, colors='g', linestyles = 'dashed')
            lower = data_corr['lower'].loc[data_corr['layer']==layer].values[0]
            upper = data_corr['upper'].loc[data_corr['layer']==layer].values[0]
            plt.axvspan(xmin = lower, xmax = upper, ymin = 0, ymax = 1, facecolor='green', alpha=0.3, label = '95% CI')
            
            #display the nr of correlations used for the histogram in each plot (because columns with nans were omitted when calculating correlations)
            if subplot_loc + loc == 1:
                # plt.text(-0.4, 1, 'N = '+ str(len(plot_vector)), verticalalignment = 'bottom', horizontalalignment = 'left')
                t = plt.text(0.95, 29, 'N = '+ str(len(plot_vector)), verticalalignment = 'top', horizontalalignment = 'right')
            else:
                t = plt.text(0.95, 29, 'N = '+ str(len(plot_vector)), verticalalignment = 'top', horizontalalignment = 'right')
                t.set_bbox(dict(facecolor='white', alpha=0.3, edgecolor=None))
            
            #titles
            plt.title(title+r'$_{'+scale+'}$', size = 'large')
        
            # #remove xticks in upper rows
            # if loc != 16:
            plt.xticks(size ='medium' )
            
            if subplot_loc != 0:
                plt.yticks([], size = 'small')
                
            plt.grid(False)
    
            #plot legend 
            if loc + subplot_loc ==1:
                plt.legend(loc = 'upper left', frameon = True, fancybox =True)
            
            #add common axes 
            fig.add_subplot(111, frameon=False)
            # hide tick and tick label of the big axes
            plt.tick_params(labelcolor='none', top=False, bottom=False, left=False, right=False)
            plt.grid(False)
            plt.xlabel("Correlation", size = 'x-large')
            plt.ylabel("Count", size = 'x-large')
                        
    #shift plots down to make room for a title 
    fig.subplots_adjust(top=0.925) 
                
