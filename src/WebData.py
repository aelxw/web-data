
# coding: utf-8

# In[3]:


from bs4 import BeautifulSoup
import bs4
import pandas as pd
import requests
import datetime
from datetime import datetime as dt
import re
import numpy as np
import io
import json
import traceback
import sys


# In[4]:


cwd = "C:/Users/pchong/web-data/src/"


# In[5]:


# Get NYMEX data

def nymex(yyyymmdd):
      
    def nymex_ng(yyyymmdd):
        d = requests.get("https://www.cmegroup.com").cookies.get_dict()
        cookie = "; ".join([k + "=" + d[k] for k in d])
        res = requests.get(
            url="https://www.cmegroup.com/CmeWS/mvc/Settlements/Futures/Settlements/444/FUT",
            params={
                "strategy":"DEFAULT",
                "tradeDate":dt.strptime(str(yyyymmdd), "%Y%m%d").strftime("%m/%d/%Y"),
                "pageSize":"50"
            },
            headers={"cookie":cookie}
        )
        df = pd.DataFrame(res.json()["settlements"])            .assign(tradeDate=dt.strptime(yyyymmdd, "%Y%m%d").strftime("%d-%b-%Y"))            .assign(currency="USD")            .assign(uom="MMBTU")            .assign(market="HH-NG")

        df = df.loc[df.settle != '']
        df.month = df.month.map(lambda x: dt.strptime(x.lower().replace("jly", "jul"), "%b %y").strftime("%b-%Y"))

        rename = {
            "settle":"price"
        }

        df = df.rename(columns=rename)
        
        df = df.loc[:, ["tradeDate", "market", "price", "currency", "uom", "month"]]
        df.loc[:, ["price"]] = df.loc[:, ["price"]].applymap(lambda x: float(x))
        return df



    def nymex_cl(yyyymmdd):
        d = requests.get("https://www.cmegroup.com").cookies.get_dict()
        cookie = "; ".join([k + "=" + d[k] for k in d])
        res = requests.get(
            url="https://www.cmegroup.com/CmeWS/mvc/Settlements/Futures/Settlements/425/FUT",
            params={
                "strategy":"DEFAULT",
                "tradeDate":dt.strptime(str(yyyymmdd), "%Y%m%d").strftime("%m/%d/%Y"),
                "pageSize":"50"
            },
            headers={"cookie":cookie}
        )
        df = pd.DataFrame(res.json()["settlements"])            .assign(tradeDate=dt.strptime(yyyymmdd, "%Y%m%d").strftime("%d-%b-%Y"))            .assign(currency="USD")            .assign(uom="BBL")            .assign(market="HH-CL")

        df = df.loc[df.settle != '']
        df.month = df.month.map(lambda x: dt.strptime(x.lower().replace("jly", "jul"), "%b %y").strftime("%b-%Y"))

        rename = {
            "settle":"price"
        }

        df = df.rename(columns=rename)
        
        df = df.loc[:, ["tradeDate", "market", "price", "currency", "uom", "month"]]
        df.loc[:, ["price"]] = df.loc[:, ["price"]].applymap(lambda x: float(x))
        return df



    def nymex_ho(yyyymmdd):
        d = requests.get("https://www.cmegroup.com").cookies.get_dict()
        cookie = "; ".join([k + "=" + d[k] for k in d])
        res = requests.get(
            url="https://www.cmegroup.com/CmeWS/mvc/Settlements/Futures/Settlements/426/FUT",
            params={
                "strategy":"DEFAULT",
                "tradeDate":dt.strptime(str(yyyymmdd), "%Y%m%d").strftime("%m/%d/%Y"),
                "pageSize":"50"
            },
            headers={"cookie":cookie}
        )
        df = pd.DataFrame(res.json()["settlements"])            .assign(tradeDate=dt.strptime(yyyymmdd, "%Y%m%d").strftime("%d-%b-%Y"))            .assign(currency="USD")            .assign(uom="GAL")            .assign(market="HH-HO")

        df = df.loc[df.settle != '']
        df.month = df.month.map(lambda x: dt.strptime(x.lower().replace("jly", "jul"), "%b %y").strftime("%b-%Y"))

        rename = {
            "settle":"price"
        }

        df = df.rename(columns=rename)
        
        df = df.loc[:, ["tradeDate", "market", "price", "currency", "uom", "month"]]
        df.loc[:, ["price"]] = df.loc[:, ["price"]].applymap(lambda x: float(x))
        return df
    
    dfs = [nymex_ng(yyyymmdd), nymex_cl(yyyymmdd), nymex_ho(yyyymmdd)]
    return pd.concat(dfs, ignore_index=True)


# In[6]:


# Get NGX data

def ngx(yyyymmdd):
    s = requests.session()
    login_url = "https://secure.ngx.com/sso/login?service=https%3A%2F%2Fsecure.ngx.com%3A443%2Fngxcs%2Fj_spring_cas_security_check"
    res = s.get(login_url)
    login_form_url = "https://secure.ngx.com/sso/login;jsessionid={}?service=https%3A%2F%2Fsecure.ngx.com%3A443%2Fngxcs%2Fj_spring_cas_security_check".format(res.cookies.get("JSESSIONID"))
    soup = BeautifulSoup(res.text, 'html.parser')
    form = soup.find("form", {"id":"fm1"})
    lt = form.find("input", {"name":"lt"}).get("value")
    execution = form.find("input", {"name":"execution"}).get("value")
    eventId = "submit"
    data = {
        "username":"pchong@aegent.ca",
        "password":"NGXnew2012",
        "lt":lt,
        "execution":execution,
        "_eventId":eventId
    }

    s.post(login_form_url, data)

    excel_url = "https://secure.ngx.com/ngxcs/marketSettlementPrice.xls"
    params = {
        "market":"1,3,351,13,11",
        "stripType":"Monthly",
        "startdt":dt.strptime(str(yyyymmdd), "%Y%m%d").strftime("%d-%B-%Y"),
        "enddt":dt.strptime(str(yyyymmdd), "%Y%m%d").strftime("%d-%B-%Y"),
        "pageSize":"-1"
    }
    res = s.get(excel_url, params=params)
    s.close()
    
    buf = io.BytesIO(res.content)
    df = pd.read_excel(buf)
    
    def mkt_cur_uom(x):
        arr = x.split(", ")
        market = arr[2]
        groups = re.match(".*\(([A-Z]+)/([A-Z]+)\)", arr[1]).groups()
        currency = groups[0]
        uom = groups[1]
        curr_map = {"CA":"CAD", "US":"USD"}
        if(currency in curr_map):
            currency = curr_map[currency]
        row = pd.Series(dict(zip(["market", "currency", "uom"], [market, currency, uom])))
        return row.loc[["market", "currency", "uom"]]
    df = df.join(df.Market.apply(mkt_cur_uom))
    
    drop_cols = ["# Trades", "Total Volume", "Weighted Avg", "Open", "High", "Low", "Market"]
    rename_cols = {
        "Market Date":"tradeDate",
        "Begin Date":"beginDate",
        "End Date":"endDate",
        "Settlement":"price"
    }
    df = df.drop(drop_cols, axis=1).rename(columns=rename_cols)
    df = df.assign(month=df.endDate.apply(lambda x: x.strftime("%b-%Y")))
    df.loc[:, ["tradeDate"]] = df.loc[:, ["tradeDate"]].applymap(lambda x: x.strftime("%d-%b-%Y"))
    
    df = df.loc[:, ["tradeDate", "market", "price", "currency", "uom", "month"]]
    df.loc[:, ["price"]] = df.loc[:, ["price"]].applymap(lambda x: float(x))
    return df
    


# In[7]:


# Combined NYMEX and NGX data into settlement data

def settlement(yyyymmdd):
    return pd.concat([nymex(yyyymmdd), ngx(yyyymmdd)], ignore_index=True)


# In[8]:


# Get HOEP data

def hoep(yyyymmdd):
    url = "http://reports.ieso.ca/public/DispUnconsHOEP/PUB_DispUnconsHOEP_{date}.xml".format(date=yyyymmdd)
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'html.parser')
    l = []
    for el in soup.findAll("hoep"):
        d = {}
        for e in el:
            if(type(e) == bs4.element.Tag):
                d[e.name] = e.text
        l.append(d)
    
    df = pd.DataFrame(l).assign(date=dt.strptime(yyyymmdd, "%Y%m%d").strftime("%d-%b-%Y"))
    
    df = df.loc[:, ["date", "hour", "price"]]
    df.loc[:, ["hour", "price"]] = df.loc[:, ["hour", "price"]].applymap(lambda x: float(x))
    return df


# In[9]:


# Get Generator Output and Capability data

def gen(yyyymmdd):
    url = "http://reports.ieso.ca/public/GenOutputCapability/PUB_GenOutputCapability_{date}.xml".format(date=yyyymmdd)
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'html.parser')

    generators = soup.findAll("generator")

    dfs = []

    for g in generators:
        name = g.find("generatorname").text
        fuel = g.find("fueltype").text
        
        for performance in ["capability", "output"]:
            index = pd.MultiIndex(labels=[[0],[0],[0]], levels=[[name], [fuel], [performance]], names=["generatorname","fueltype","performance"])
            data = {}
            for x in g.findAll(performance):
                if(x.find("energymw")):
                    data[x.find("hour").text] = x.find("energymw").text
                else:
                    data[x.find("hour").text] = 0
            df = pd.DataFrame([data], index=index)
            dfs.append(df)
        
    df_c = pd.concat(dfs)
    num_cols = df_c.columns
    df_c = df_c.reset_index()
    df_c.loc[:, num_cols] = df_c.loc[:, num_cols].astype(int)
    df_c = df_c.drop("generatorname", axis=1)        .groupby(["fueltype", "performance"]).sum()        .unstack(level=0).T.reset_index()        .rename(columns={"level_0":"hour", "fueltype":"source"})        .assign(date=dt.strptime(yyyymmdd, "%Y%m%d").strftime("%d-%b-%Y"))
    
    df_c = df_c.loc[:, ["date", "source", "hour", "capability", "output"]]
    df_c.loc[:, ["hour", "capability", "output"]] = df_c.loc[:, ["hour", "capability", "output"]].applymap(lambda x: float(x))
    df_c = df_c.sort_values(["date", "hour", "source"]).reset_index(drop=True)
    del df_c.columns.name
    
    return df_c


# In[10]:


# Get weather data

def weather(yyyymmdd):
    
    year = dt.strptime(str(yyyymmdd), "%Y%m%d").year
    month = dt.strptime(str(yyyymmdd), "%Y%m%d").month
    
    url = "http://climate.weather.gc.ca/climate_data/daily_data_e.html"
    
    with open(cwd + "stations.json") as f:
        stations = json.load(f)
    

    def weather_df(station):
        
        params = {
            "timeframe":2,
            "StationID":station["stationid"],
            "Month":month,
            "Year":year
        }

        res = requests.get(url, params=params)

        soup = BeautifulSoup(res.text, 'html.parser')

        table = soup.find("div", {"id":"dynamicDataTable"}).find("table")
        thead = table.find("thead")
        tbody = table.find("tbody")
        
        def toNumber(arr):
            ret = []
            try:
                date = dt(year=year, month=month, day=int(arr[0])).strftime("%d-%b-%Y")
                ret.append(date)
                for x in arr[1:]:
                    try:
                        ret.append(float(x))
                    except:
                        ret.append(np.nan)
                return ret
            except:
                return None

        header = []
        body = []

        for tr in thead:
            for td in tr:
                if(type(td) == bs4.element.Tag):
                    if(td.find("abbr")):
                        header.append(td.find("abbr").text.lower())

        for tr in tbody:
            temp = []
            for td in tr:
                if(type(td) == bs4.element.Tag):
                    temp.append(td.text)

            temp = toNumber(temp)
            if(temp is not None):
                body.append(temp)

        rename = {
            "max temp":"maxTemp",
            "min temp":"minTemp",
            "mean temp":"meanTemp",
            "heat deg days":"hdd",
            "cool deg days":"cdd"
        }

        date = dt.strptime(yyyymmdd, "%Y%m%d")
        
        df = pd.DataFrame(body, columns=["day"]+header).rename(columns=rename)            .assign(place=station["place"])            .assign(name=station["name"])            .assign(month=date.strftime("%b-%Y"))
            
        df = df.loc[df["day"] == date.strftime("%d-%b-%Y")]
        df = df.loc[:, ["day", "month", "place", "name", "hdd", "cdd", "minTemp", "meanTemp", "maxTemp"]]
        df = df.loc[~df.isnull().any(axis=1)]
        df.loc[:, ["hdd", "cdd", "minTemp", "meanTemp", "maxTemp"]] = df.loc[:, ["hdd", "cdd", "minTemp", "meanTemp", "maxTemp"]].applymap(lambda x: float(x))
        
        return df
    
    dfs = [];
    for station in stations:
        df = weather_df(station)
        dfs.append(df)
        
    return pd.concat(dfs).reset_index(drop=True)
        
    

