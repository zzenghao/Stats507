# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:light
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.12.0
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# ### Q0
# a:
# The snippet deletes the tuples with same 1st element,
# while keeping only one of them with the largest 3rd element.
#
# b:
# 1. do not need to append a tuple in li, instead just overwrite the value 
#     after necessary comparison
# 2. the loop index m and n are nor necessary here.
#     instead of index, m and n can be the tuple object
#     and many of the assignment opeartion can be waived.
#     Also m[0] is more easily to read compared to sample_list[m][0].
# 3. Those 0 and 3(should be 2) numbers could be parameterized
#     so that any furthur modifications are easier to do.
#    

# ### Q1+Q2

# +
import numpy as np
import pandas as pd
from timeit import default_timer as timer


def genRan(n, k, low, high):
    """
    generate n k-tuples with random integer

    Parameters
    ----------
    n : int
        number of tuple in return list
    k : int
        number of element in a tuple
    low : int
        low boundary of the random number
    high: int
        high boundary of the random number

     Returns
     -------
     list_in

    """

    list_in=[tuple(np.random.randint(low, high, k)) for x in range(n)]

    return(list_in)

def takeSort1(list_in, a, b):
    """
    from the given code snippet
    keep only one tuple with the same number "a" element, 
    while with the largest number at "b"th element

    Parameters
    ----------
    list_in : list
        list with n k-tuples
    a : int
        main index that keep only one out of other same ones
    b : int
        keep the list with largest bth index

     Returns
     -------
     dict

    """
    sample_list=list_in
    op=[]
    for m in range(len(sample_list)):
        li=[sample_list[m]]
        for n in range(len(sample_list)):
            if (sample_list[m][a] == sample_list[n][a] and
                        sample_list[m][b] != sample_list[n][b]):
                li.append(sample_list[n])
        op.append(sorted(li, key=lambda dd: dd[b], reverse=True)[0])
    res = list(set(op))

    return(res)

def takeSort2(list_in, a, b):
    """
    from the given code snippet
    keep only one tuple with the same number "a" element, 
    while with the largest number at "b"th element

    Parameters
    ----------
    list_in : list
        list with n k-tuples
    a : int
        main index that keep only one out of other same ones
    b : int
        keep the list with largest bth index

     Returns
     -------
     dict

    """
    

    list_out=[]
    for x in list_in:
        maxEle=x
        for y in list_in:
            if x[a] == y[a] and y[b] >= maxEle[b]: 
                maxEle=y
        list_out.append(maxEle)
    list_out=list(set(list_out))

    
    return(list_out)

def takeSort3(list_in, a, b):
    """
    from the given code snippet
    keep only one tuple with the same number "a" element, 
    while with the largest number at "b"th element
    
    using dictionary function

    Parameters
    ----------
    list_in : list
        list with n k-tuples
    a : int
        main index that keep only one out of other same ones
    b : int
        keep the list with largest bth index

     Returns
     -------
     dict

    """    
    
    list_out={}
    for x in list_in:
        try:
            if list_out[x[a]][b]<=list_in[x][b]:
                list_out[x[a]]=x
        except:
            list_out[x[a]]=x
    list_out=list(list_out.values())
    return(list_out)

# initiallization
n, k=5, 3
low, high=5, 10

Res=np.zeros((2,3))

############################################
# test n range from 5 to 300)

nrepUp=300
nrepLo=5
nrepT=300
m=np.zeros(nrepT)

i=0
for n in genRan(nrepT,1,nrepLo,nrepUp):
    n=n[0]
    s=timer()
    list_in=genRan(n,k,low,high)
    list_sorted=takeSort1(list_in, a=0, b=2)
    e=timer()
    m[i]=e-s
    i+=1
    
Res[0,0]=np.mean(m)
i=0
for n in genRan(nrepT,1,nrepLo,nrepUp):
    n=n[0]
    s=timer()
    list_in=genRan(n,k,low,high)
    list_sorted=takeSort2(list_in, a=0, b=2)
    e=timer()
    m[i]=e-s
    i+=1
    
Res[0,1]=np.mean(m)
i=0
for n in genRan(nrepT,1,nrepLo,nrepUp):
    n=n[0]
    s=timer()
    list_in=genRan(n,k,low,high)
    list_sorted=takeSort3(list_in, a=0, b=2)
    e=timer()
    m[i]=e-s
    i+=1
    
Res[0,2]=np.mean(m)

#############################################
# test k range from 3 to 20)

krepUp=3
krepLo=20
krepT=300
n=10

m=np.zeros(krepT)


i=0
for k in genRan(krepT,1,nrepLo,nrepUp):
    k=k[0]
    s=timer()
    list_in=genRan(n,k,low,high)
    list_sorted=takeSort1(list_in, a=0, b=2)
    e=timer()
    m[i]=e-s
    i+=1
    
Res[1,0]=np.mean(m)
i=0
for k in genRan(krepT,1,nrepLo,nrepUp):
    k=k[0]
    s=timer()
    list_in=genRan(n,k,low,high)
    list_sorted=takeSort2(list_in, a=0, b=2)
    e=timer()
    m[i]=e-s
    i+=1
    
Res[1,1]=np.mean(m)
i=0
for k in genRan(krepT,1,nrepLo,nrepUp):
    k=k[0]
    s=timer()
    list_in=genRan(n,k,low,high)
    list_sorted=takeSort3(list_in, a=0, b=2)
    e=timer()
    m[i]=e-s
    i+=1
    
Res[1,2]=np.mean(m)
Res=pd.DataFrame((Res*100000).astype(int))
Res.columns=["sort (a)","sort (b)","sort (c)"]
Res.index=["n","k"]
print("Time used for different sorting functions")
print(Res)

'''
Time used for different sorting functions
   sort (a)  sort (b)  sort (c)
n       576       357       131
k        19        17        15
'''
# -

# ### Q3

# +
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



demograStr=["SEQN", "RIDAGEYR", "RIDRETH3", "DMDEDUC2", "DMDMARTL", 
            "RIDSTATR", "SDMVPSU", "SDMVSTRA", "WTMEC2YR", "WTINT2YR"]
demo_str=["id number", "age", "race", "education level", "marital", 
                "interview status", "masked variance pseudo psu", 
                "masked variance pseudo stratum", "two year mec weight", 
                "two year interviewed weight", "time"]
demo_type=[int, int, int, int, int, int, int, int, float, float, str]
demo_ctype=dict(zip(demo_str,demo_type))

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
demograDf.columns=demo_str  # rename the colume
demograDf=demograDf.astype(demo_ctype)  # set the data tpye of column

demograDf.to_pickle("./demograDf.pkl")
print("cases in demographic data")
print(len(demograDf.index))





tooth_count=["OHX"+str(x+1).zfill(2)+"TC" for x in range(32)]
corCavi=["OHX"+str(x+2).zfill(2)+"CTC" for x in range(30)
          if x!=14 and x!=15]

oh_cstr=["SEQN", "OHDDESTS"]+tooth_count+corCavi

tooth_cStr=["Tooth Count: #"+str(x+1) for x in range(32)]
corCaviStr=["Coronal Caries: Tooth Count #"+str(x+2) for x in range(30)
            if x!=14 and x!=15]


oh_str=["id number", "status code"]+tooth_cStr+corCaviStr+["time"]


oh_type=[int for x in range(2+32)]+[str for x in range(29-1)]
oralHealDfColType=dict(zip(oh_str,oh_type))

oralHealDf=pd.DataFrame()

df2011_2012=pd.read_sas(
    "https://wwwn.cdc.gov/Nchs/Nhanes/2011-2012/OHXDEN_G.XPT")
oralHealDf=appendDf(oralHealDf,df2011_2012,oh_cstr,"2011-2012")

df2013_2014=pd.read_sas(
    "https://wwwn.cdc.gov/Nchs/Nhanes/2013-2014/OHXDEN_H.XPT")
oralHealDf=appendDf(oralHealDf,df2013_2014,oh_cstr,"2013-2014")

df2015_2016=pd.read_sas(
    "https://wwwn.cdc.gov/Nchs/Nhanes/2015-2016/OHXDEN_I.XPT")
oralHealDf=appendDf(oralHealDf,df2015_2016,oh_cstr,"2015-2016")


df2017_2018=pd.read_sas(
    "https://wwwn.cdc.gov/Nchs/Nhanes/2017-2018/OHXDEN_J.XPT")
oralHealDf=appendDf(oralHealDf,df2017_2018,oh_cstr,"2017-2018")



oralHealDf.fillna(-1,inplace= True) # replace all the nan to -1
oralHealDf.columns=oh_str  # rename the colume


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
# -


