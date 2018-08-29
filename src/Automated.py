
# coding: utf-8

# In[1]:


import WebData as wd
import sys
import pandas as pd


# In[77]:


folderpath = "C:/Users/Alexander/Jupyter/web-data/archive/"
yyyymmdd = sys.argv[1]
filename = sys.argv[2]


# In[78]:


if(filename == "weather"):
    filepath = folderpath + "/weather/weather_{}.csv".format(yyyymmdd)
    wd.weather(yyyymmdd).to_csv(filepath, index=False)
if(filename == "hoep"):
    filepath = folderpath + "/hoep/hoep_{}.csv".format(yyyymmdd)
    wd.hoep(yyyymmdd).to_csv(filepath, index=False)
if(filename == "settlement"):
    filepath = folderpath + "/settlement/settlement_{}.csv".format(yyyymmdd)
    wd.settlement(yyyymmdd).to_csv(filepath, index=False)
if(filename == "gen"):
    filepath = folderpath + "/gen/gen_{}.csv".format(yyyymmdd)
    wd.gen(yyyymmdd).to_csv(filepath, index=False)

