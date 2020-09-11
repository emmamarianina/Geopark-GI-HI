# -*- coding: utf-8 -*-
"""
Created on Wed Feb 19 11:08:27 2020

@author: 10799478
"""

#import needed modules

import pandas as pd
import statistics
from scipy.stats import mannwhitneyu
from statsmodels.stats.multitest import multipletests
from statsmodels.stats.diagnostic import lilliefors

#select type of correction method used
method_c = 'holm-sidak'
alpha_c = 0.05

#%% #Mann whitney U test in a LOOP -->  WORLD 
    
#use mann whitney u test to test if geodiversity data is GREATER in geoparks than in random world samples. One-tailed test, where geopark data=X and Global data = Y. 
#H alternative = 'greater'
#this is tested a 100 times, so the alpha was corrected for the family-wise error rate by aplha/number of tests. 

#make list of variables to conduct test between geoparks and world on. 
#147 for lakes, lithology, soils, slope std and slope range
#139 for rivers, geodiversity sum
variable_world_list = ['geodiversity139_mean', 'lakes_mean', 'lithology_mean', 'slope_range_mean',\
                       'slope_std_mean', 'soils_mean', 'Rivers139_mean', 'HF_1993_mean', 'HF_2009_mean', 'HF_change_mean', 'gHM_mean']
variable_geopark_list = ['GDsum_stats_139', 'Lakes_stats_147', 'Lithology_stats_147', 'SlopeRange_stats_147',\
                         'SlopeSTD_stats_147', 'Soils_stats_147', 'Rivers_stats_139', 'HF1993_stats_147', 'HF2009_stats_147', 'HFchange_stats_147', 'gHM_stats_147'] 
print_pval = 0 #disable printing p values

#create empty dataframe to store p-values 
p_vals_world = pd.DataFrame(columns = ['var_world', 'var_geopark', 'stat', 'p_val', 'layer'])

for variable_world, variable_geopark in zip(variable_world_list, variable_geopark_list): 
                    
    #create df with run MEAN results only                          
    df_mean = data_world.loc[data_world['name']== variable_world]
    df_mean = df_mean.drop('name', axis=1)
    
    #do mann whitney u test
    for (columnName, columnData) in df_mean.iteritems(): #loop through column names and column data
        stat, p = mannwhitneyu(data_geoparks['MEAN'].loc[data_geoparks['name']== variable_geopark], columnData, alternative = 'greater')
        
        if print_pval ==1:
            print ('Statistic = %.5f, p=%.20f' % (stat, p)) 
            # p_total = p_total+p
            alpha = alpha_c #/100 #apply bonferroni correction for 100 tests 
            if p > alpha:
                print('Samples are not significantly different (fail to reject H0)')
            else:
                print('Samples are significantly different  (reject H0)')
                
    
    #check if individual distributions are normally distributed with lilliefors
        stat_lillie, p_lillie = lilliefors(columnData, pvalmethod = 'table')
        # print('Statistics=%.3f, p=%.3f' % (stat, p))
        # interpret
        
        if p_lillie > 0.05:
        	distribution = 'normal'#print('world ' + layer + ' looks Gaussian (fail to reject H0)')
        else:
        	distribution = 'not normal'#print('world ' + layer + ' does not look Gaussian (reject H0)')
        
        #calculate medians of each random sample set
        medians = statistics.median(columnData)
    
      #store p values and statistic in a dataframe, with names of the compared layers 
        if '139' in variable_geopark:
            layer = variable_geopark.replace('_stats_139', '')
        else: 
            layer = variable_geopark.replace('_stats_147', '')
        p_vals_world = p_vals_world.append({'var_world': variable_world, 'var_geopark': variable_geopark, 'stat': stat,\
                                            'p_val': p, 'layer': layer, 'index_p':columnName, 'distribution': distribution,\
                                                'median': medians}, ignore_index=True)

#apply correction on p values
list_layers = p_vals_world.layer.unique().tolist() #list to loop through
p_vals_world_corrected = pd.DataFrame(columns = ['p_val', 'p_val_uncorrected', 'Ha','layer', 'index_p']) # make empty dataframe 

for layer in list_layers:
    p_vector = p_vals_world['p_val'].loc[p_vals_world['layer']==layer] # select p_values per layer
    
    #calculate corrected p vals 
    p_corrected = multipletests(p_vector, alpha = alpha_c, method = method_c, is_sorted = False, returnsorted = False)
    
    #get medians 
    median_array = p_vals_world['median'].loc[p_vals_world['layer']==layer]
    
    #convert corrected p vals from numpy array to pandas series 
    index_vector = p_vals_world['index_p'].loc[p_vals_world['layer']==layer] # used for pivot in the visualisation
    p_corrected_df = pd.DataFrame({'p_val': p_corrected[1], 'p_val_uncorrected': p_vector ,'Ha': p_corrected[0] , 'layer': layer, 'index_p': index_vector, 'median': median_array})
    
    #contenate all dataframes to get all layers
    p_vals_world_corrected = pd.concat([p_vals_world_corrected, p_corrected_df] ,ignore_index = True)

#%% #Mann whitney U test in a LOOP --> ASIA
    
#use mann whitney u test to test if geodiversity data is GREATER in geoparks than in random asia samples. One-tailed test, where geopark data=X and Global data = Y. 
#H alternative = 'greater'
#this is tested a 100 times, so the alpha was corrected for the family-wise error rate by aplha/number of tests. 

#make list of variables to conduct test between geoparks and asia on. 
#147 for lakes, lithology, soils, slope std and slope range
#139 for rivers, geodiversity sum
variable_asia_list = ['Asia_60NBgeodiversity_mean', 'Asia_lakes_mean', 'Asia_lithology_mean', 'Asia_slope_range_mean',\
                      'Asia_slope_std_mean', 'Asia_soils_mean', 'Asia_60NBrivers_mean', 'HF1993_Asia_mean', 'HF2009_Asia_mean', 'HFchange_Asia_mean', 'gHM_Asia_mean']
variable_geopark_list = ['GDsum_stats_61', 'Lakes_stats_61', 'Lithology_stats_61', 'SlopeRange_stats_61',\
                         'SlopeSTD_stats_61', 'Soils_stats_61', 'Rivers_stats_61', 'HF1993_stats_61', 'HF2009_stats_61', 'HFchange_stats_61', 'gHM_stats_61' ] 
print_pval = 0 #disable printing p values

#create empty dataframe to store p-values 
p_vals_asia = pd.DataFrame(columns = ['var_asia', 'var_geopark', 'stat', 'p_val', 'layer'])

for variable_asia, variable_geopark in zip(variable_asia_list, variable_geopark_list): 
                    
    #create df with run MEAN results only                          
    df_mean = data_asia.loc[data_asia['name']== variable_asia]
    df_mean = df_mean.drop('name', axis=1)
    
    #do mann whitney u test
    for (columnName, columnData) in df_mean.iteritems(): #loop through column names and column data
        stat, p = mannwhitneyu(data_geoparksEA['MEAN'].loc[data_geoparksEA['name']== variable_geopark], columnData, alternative = 'greater')
        
        if print_pval ==1:
            print ('Statistic = %.5f, p=%.20f' % (stat, p)) 
            # p_total = p_total+p
            alpha = alpha_c #/100 #apply bonferroni correction for 100 tests 
            if p > alpha:
                print('Samples are not significantly different (fail to reject H0)')
            else:
                print('Samples are significantly different  (reject H0)')
                
                
        #check if individual distributions are normally distributed with lilliefors
        stat_lillie, p_lillie = lilliefors(columnData, pvalmethod = 'table')
        # print('Statistics=%.3f, p=%.3f' % (stat, p))
        # interpret
        
        if p_lillie > 0.05:
        	distribution = 'normal'#print('world ' + layer + ' looks Gaussian (fail to reject H0)')
        else:
        	distribution = 'not normal'#print('world ' + layer + ' does not look Gaussian (reject H0)')
            
      #calculate medians of each random sample set
        medians = statistics.median(columnData)
        
      #store p values and statistic in a dataframe, with names of the compared layers 
        if '61' in variable_geopark:
            layer = variable_geopark.replace('_stats_61', '')
        else: 
            layer = variable_geopark.replace('_stats_61', '')
        p_vals_asia = p_vals_asia.append({'var_asia': variable_asia, 'var_geopark': variable_geopark, 'stat': stat,\
                                          'p_val': p, 'layer': layer, 'index_p':columnName, 'distribution': distribution,\
                                              'median': medians}, ignore_index=True)

#apply correction on p values
list_layers = p_vals_asia.layer.unique().tolist() #list to loop through
p_vals_asia_corrected = pd.DataFrame(columns = ['p_val', 'p_val_uncorrected', 'Ha','layer', 'index_p']) # make empty dataframe 

for layer in list_layers:
    p_vector = p_vals_asia['p_val'].loc[p_vals_asia['layer']==layer] # select p_values per layer
    
    #calculate corrected p vals 
    p_corrected = multipletests(p_vector, alpha = alpha_c, method = method_c, is_sorted = False, returnsorted = False)
    
    #get medians 
    median_array = p_vals_asia['median'].loc[p_vals_asia['layer']==layer]
    
    #convert corrected p vals from numpy array to pandas series 
    index_vector = p_vals_asia['index_p'].loc[p_vals_asia['layer']==layer] # used for pivot in the visualisation
    p_corrected_df = pd.DataFrame({'p_val': p_corrected[1],'p_val_uncorrected': p_vector ,'Ha': p_corrected[0] ,'layer': layer, 'index_p': index_vector, 'median': median_array})
    
    #contenate all dataframes to get all layers
    p_vals_asia_corrected = pd.concat([p_vals_asia_corrected, p_corrected_df] ,ignore_index = True)
#%% #Mann whitney U test in a LOOP --> EUROPE
    
#use mann whitney u test to test if geodiversity data is GREATER in geoparks than in random europe samples. One-tailed test, where geopark data=X and Global data = Y. 
#H alternative = 'greater'
#this is tested a 100 times, so the alpha was corrected for the family-wise error rate by aplha/number of tests. 

#make list of variables to conduct test between geoparks and europe on. 
variable_europe_list = ['Europe_60NBgeodiversity_mean', 'europelakes_mean', 'europelithology_mean', 'europeslope_range_mean',\
                        'europe_slope_std_mean', 'europesoils_mean', 'Europe_60NBrivers_mean', 'HF1993_Europe_mean', 'HF2009_Europe_mean', 'HFchange_Europe_mean', 'gHM_Europe_mean']
variable_geopark_list = ['GDsum_stats_66', 'Lakes_stats_74', 'Lithology_stats_74', 'SlopeRange_stats_74',\
                         'SlopeSTD_stats_74', 'Soils_stats_74', 'Rivers_stats_66','HF1993_stats_74', 'HF2009_stats_74', 'HFchange_stats_74', 'gHM_stats_74' ] 
print_pval = 0 #disable printing p values

#create empty dataframe to store p-values 
p_vals_europe = pd.DataFrame(columns = ['var_europe', 'var_geopark', 'stat', 'p_val', 'layer'])

for variable_europe, variable_geopark in zip(variable_europe_list, variable_geopark_list): 
                    
    #create df with run MEAN results only                          
    df_mean = data_europe.loc[data_europe['name']== variable_europe]
    df_mean = df_mean.drop('name', axis=1)
    
    #do mann whitney u test
    for (columnName, columnData) in df_mean.iteritems(): #loop through column names and column data
        stat, p = mannwhitneyu(data_geoparksEA['MEAN'].loc[data_geoparksEA['name']== variable_geopark], columnData, alternative = 'greater')
        
        if print_pval ==1:
            print ('Statistic = %.5f, p=%.20f' % (stat, p)) 
            # p_total = p_total+p
            alpha = alpha_c #/100 #apply bonferroni correction for 100 tests 
            if p > alpha:
                print('Samples are not significantly different (fail to reject H0)')
            else:
                print('Samples are significantly different  (reject H0)')
                
                
        #check if individual distributions are normally distributed with lilliefors
        stat_lillie, p_lillie = lilliefors(columnData, pvalmethod = 'table')
        # print('Statistics=%.3f, p=%.3f' % (stat, p))
        # interpret
        
        if p_lillie > 0.05:
        	distribution = 'normal'#print('world ' + layer + ' looks Gaussian (fail to reject H0)')
        else:
        	distribution = 'not normal'#print('world ' + layer + ' does not look Gaussian (reject H0)')
            
        #calculate medians of each random sample set
        medians = statistics.median(columnData)
        
        #store p values and statistic in a dataframe, with names of the compared layers 
        if '74' in variable_geopark:
            layer = variable_geopark.replace('_stats_74', '')
        else: 
            layer = variable_geopark.replace('_stats_66', '')
        p_vals_europe = p_vals_europe.append({'var_europe': variable_europe, 'var_geopark': variable_geopark, 'stat': stat,\
                                              'p_val': p, 'layer': layer, 'index_p':columnName, 'distribution': distribution,\
                                                  'median': medians}, ignore_index=True)
                            
#apply correction on p values 
list_layers = p_vals_europe.layer.unique().tolist() #list to loop through
p_vals_europe_corrected = pd.DataFrame(columns = ['p_val', 'p_val_uncorrected', 'Ha','layer', 'index_p']) # make empty dataframe 

for layer in list_layers:
    p_vector = p_vals_europe['p_val'].loc[p_vals_europe['layer']==layer] # select p_values per layer
    
    #calculate corrected p vals 
    p_corrected = multipletests(p_vector, alpha = alpha_c, method = method_c, is_sorted = False, returnsorted = False)
    
    #get medians 
    median_array = p_vals_europe['median'].loc[p_vals_europe['layer']==layer]
    
    #convert corrected p vals from numpy array to pandas series 
    index_vector = p_vals_europe['index_p'].loc[p_vals_europe['layer']==layer] # used for pivot in the visualisation
    p_corrected_df = pd.DataFrame({'p_val': p_corrected[1], 'p_val_uncorrected': p_vector , 'Ha': p_corrected[0],'layer': layer, 'index_p': index_vector, 'median': median_array})
    
    #contenate all dataframes to get all layers
    p_vals_europe_corrected = pd.concat([p_vals_europe_corrected, p_corrected_df] ,ignore_index = True)


