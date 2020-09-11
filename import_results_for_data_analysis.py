# -*- coding: utf-8 -*-
"""
Created on Fri Feb 14 13:28:31 2020

@author: 10799478; Emma Polman
"""

# import needed modules
import os
from dbfread import DBF
import pandas as pd
import glob
import numpy as np

# set file paths 
disk = r'G:/'
folder = 'THESIS/results/results_january_2020/'
folder_world ='GD_HI_world/'
folder_europe = 'GD_HI_Europe/'
folder_asia = 'GD_HI_Asia/'
folder_geoparks = 'geoparks_world/'
folder_geoparks_EA = 'geoparks_asia_europe/'


#%% data World
#change directory
path = disk+folder+folder_world
os.chdir(path)

fileList = glob.glob("*.dbf")

#create empty dataframe 
data_world = pd.DataFrame()

for file in glob.glob("*.dbf"):
    # for index, file in enumerate(fileList):
    data = pd.DataFrame(iter(DBF((path+file), load=True)))
    data['name'] = file.replace(".dbf","")
    data_world = pd.concat([data_world, data], axis=0, sort=True)
    data_world.replace(99999, np.nan, inplace = True) #replace 0 by nan

data_worldM = pd.melt(data_world, id_vars = ["name"] )

#%% data Europe
path = disk+folder+folder_europe
os.chdir(path)

fileList = glob.glob("*.dbf")

#create empty dataframe 
data_europe = pd.DataFrame()

for file in glob.glob("*.dbf"):
    # for index, file in enumerate(fileList):
    data = pd.DataFrame(iter(DBF((path+file), load=True)))
    data['name'] = file.replace(".dbf","")
    data_europe = pd.concat([data_europe, data], axis=0, sort=True)
    data_europe.replace(99999, np.nan, inplace = True) #replace 0 by nan

data_europeM = pd.melt(data_europe, id_vars = ["name"] )
#%% data Asia
path = disk+folder+folder_asia
os.chdir(path)

fileList = glob.glob("*.dbf")

#create empty dataframe 
data_asia = pd.DataFrame()

for file in glob.glob("*.dbf"):
    # for index, file in enumerate(fileList):
    data = pd.DataFrame(iter(DBF((path+file), load=True)))
    data['name'] = file.replace(".dbf","")
    data_asia = pd.concat([data_asia, data], axis=0, sort=True)
    data_asia.replace(99999, np.nan, inplace = True) #replace 0 by nan
    
data_asiaM = pd.melt(data_asia, id_vars = ["name"] )

#%% data Geoparks World 
path = disk+folder+folder_geoparks
os.chdir(path)

fileList = glob.glob("*.dbf")

#create empty dataframe 
data_geoparks = pd.DataFrame()

for file in glob.glob("*.dbf"):
    # for index, file in enumerate(fileList):
    data = pd.DataFrame(iter(DBF((path+file), load=True)))
    data['name'] = file.replace(".dbf","")
    data_geoparks = pd.concat([data_geoparks, data], axis=0, sort=True)
    data_geoparks.replace(99999, np.nan, inplace = True) #replace 0 by nan
    
# data_geoparksM = pd.melt(data_geoparks, id_vars = ["name"] )

#%% data Geoparks Europe Asia 
path = disk+folder+folder_geoparks_EA
os.chdir(path)

fileList = glob.glob("*.dbf")

#create empty dataframe 
data_geoparksEA = pd.DataFrame()

for file in glob.glob("*.dbf"):
    # for index, file in enumerate(fileList):
    data = pd.DataFrame(iter(DBF((path+file), load=True)))
    data['name'] = file.replace(".dbf","")
    data_geoparksEA = pd.concat([data_geoparksEA, data], axis=0, sort=True)
    data_geoparksEA.replace(99999, np.nan, inplace = True) #replace 0 by nan
    
# data_geoparksEAM = pd.melt(data_geoparksEA, id_vars = ["name"] )