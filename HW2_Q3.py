# -*- coding: utf-8 -*-
"""
Created on Wed Sep 29 20:30:48 2021

@author: zhang
"""
import pandas as pd



def appendDf(df1, df2, Str_, time_):
    """
    after add a column as time at the end of df2
    append df2 to df1
    

    Parameters
    ----------
    df1 : datafram
        the total dataframe
    df2 : dataframe
        current dataframe
    Str_: list of string
        used to select column
    time_ : string
        time added to the last column

     Returns
     -------
     df1

    """    
    df2=df2[Str_] # keep the selected column
    df2["time"]=time_ 
    df1=df1.append(df2)
   
    return(df1) 



demograStr=["SEQN", "RIAGENDR", "RIDAGEYR", "RIDRETH3", "DMDEDUC2", "DMDMARTL", 
            "RIDSTATR", "SDMVPSU", "SDMVSTRA", "WTMEC2YR", "WTINT2YR"]
demograColStr=["id number","gender", "age", "race", "education level", "marital", 
                "interview status", "masked variance pseudo psu", 
                "masked variance pseudo stratum", "two year mec weight", 
                "two year interviewed weight", "time"]
demograColType=[int, int, int, int, int, int, int, int, int, float, float, str]
demograDfColType=dict(zip(demograColStr,demograColType))

demograDf=pd.DataFrame()

df2011_2012=pd.read_sas(
    "https://wwwn.cdc.gov/Nchs/Nhanes/2011-2012/DEMO_G.XPT")
demograDf=appendDf(demograDf,df2011_2012,demograStr,"2011-2012")

df2013_2014=pd.read_sas(
    "https://wwwn.cdc.gov/Nchs/Nhanes/2013-2014/DEMO_H.XPT")
demograDf=appendDf(demograDf,df2013_2014,demograStr,"2013-2014")

df2015_2016=pd.read_sas(
    "https://wwwn.cdc.gov/Nchs/Nhanes/2015-2016/DEMO_I.XPT")
demograDf=appendDf(demograDf,df2015_2016,demograStr,"2015-2016")


df2017_2018=pd.read_sas(
    "https://wwwn.cdc.gov/Nchs/Nhanes/2017-2018/DEMO_J.XPT")
demograDf=appendDf(demograDf,df2017_2018,demograStr,"2017-2018")


demograDf.fillna(-1,inplace= True) # replace all the nan to -1
demograDf.columns=demograColStr  # rename the colume
demograDf=demograDf.astype(demograDfColType)  # set the data tpye of column

demograDf.to_pickle("./demograDf.pkl")
print("cases in demographic data")
print(len(demograDf.index))





toothCount=["OHX"+str(x+1).zfill(2)+"TC" for x in range(32)]
corCavi=["OHX"+str(x+2).zfill(2)+"CTC" for x in range(30)
          if x!=14 and x!=15]

oralHealStr=["SEQN", "OHDDESTS"]+toothCount+corCavi

toothCountStr=["Tooth Count: #"+str(x+1) for x in range(32)]
corCaviStr=["Coronal Caries: Tooth Count #"+str(x+2) for x in range(30)
            if x!=14 and x!=15]


oralHealColStr=["id number", "status code"]+toothCountStr+corCaviStr+["time"]


oralHealColType=[int for x in range(2+32)]+[str for x in range(29-1)]
oralHealDfColType=dict(zip(oralHealColStr,oralHealColType))

oralHealDf=pd.DataFrame()

df2011_2012=pd.read_sas(
    "https://wwwn.cdc.gov/Nchs/Nhanes/2011-2012/OHXDEN_G.XPT")
oralHealDf=appendDf(oralHealDf,df2011_2012,oralHealStr,"2011-2012")

df2013_2014=pd.read_sas(
    "https://wwwn.cdc.gov/Nchs/Nhanes/2013-2014/OHXDEN_H.XPT")
oralHealDf=appendDf(oralHealDf,df2013_2014,oralHealStr,"2013-2014")

df2015_2016=pd.read_sas(
    "https://wwwn.cdc.gov/Nchs/Nhanes/2015-2016/OHXDEN_I.XPT")
oralHealDf=appendDf(oralHealDf,df2015_2016,oralHealStr,"2015-2016")


df2017_2018=pd.read_sas(
    "https://wwwn.cdc.gov/Nchs/Nhanes/2017-2018/OHXDEN_J.XPT")
oralHealDf=appendDf(oralHealDf,df2017_2018,oralHealStr,"2017-2018")



oralHealDf.fillna(-1,inplace= True) # replace all the nan to -1
oralHealDf.columns=oralHealColStr  # rename the colume


for i in corCaviStr:
     oralHealDf[i] = oralHealDf[i].str.decode("utf-8")

oralHealDf=oralHealDf.astype(oralHealDfColType)  # set the data tpye of column
oralHealDf.to_pickle("./oralHealDf.pkl")

print("cases in oral health")
print(len(oralHealDf.index))

'''
cases in demographic data
39156
cases in oral health
35909
'''










