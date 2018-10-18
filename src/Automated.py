
# coding: utf-8

# In[1]:


import WebData as wd
import sys
import pandas as pd
import datetime
from datetime import datetime as dt


# In[ ]:


folderpath = "T:/Web Data/"
filename = sys.argv[1]

today = dt.today().strftime("%Y%m%d")
yesterday = (dt.today() - datetime.timedelta(days=1)).strftime("%Y%m%d")

if(filename == "weather"):
    filepath = folderpath + "weather/weather_{}.csv".format(yesterday)
    wd.weather(yesterday).to_csv(filepath, index=False)
if(filename == "hoep"):
    filepath = folderpath + "hoep/hoep_{}.csv".format(yesterday)
    wd.hoep(yesterday).to_csv(filepath, index=False)
if(filename == "settlement"):
    filepath = folderpath + "settlement/settlement_{}.csv".format(today)
    wd.settlement(today).to_csv(filepath, index=False)
if(filename == "gen"):
    filepath = folderpath + "gen/gen_{}.csv".format(yesterday)
    wd.gen(yesterday).to_csv(filepath, index=False)
if(filename == "ngxrate"):
    filepath = folderpath + "ngxrate/ngxrate_{}.csv".format(today)
    wd.ngx_rate_today().to_csv(filepath, index=False)

