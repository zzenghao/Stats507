# -*- coding: utf-8 -*-
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

# + [markdown] slideshow={"slide_type": "slide"}
# # Filling missing values

# + [markdown] slideshow={"slide_type": "fragment"}
# > Creat a dataframe with nan value

# + slideshow={"slide_type": "fragment"}
import pandas as pd
import numpy as np

df = pd.DataFrame(
    np.random.randn(5, 3),
    index=["a", "c", "d", "e", "f"],
    columns=["one", "two", "three"],
)

df=df.reindex(["a", "b", "c", "d", "e", "f"])
df

# + [markdown] slideshow={"slide_type": "slide"}
# ## filna() method
# * fillna() can “fill in” NA values with non-NA data in a couple of ways
#     * Replace NA with a scalar value
#     
#     
# **fill the nan value with -1**

# + slideshow={"slide_type": "fragment"}
df.fillna(-1)

# + [markdown] slideshow={"slide_type": "subslide"}
# **fill nan with string**

# + slideshow={"slide_type": "fragment"}
df.fillna("missing")

# + [markdown] slideshow={"slide_type": "slide"}
# ## filna() method
# * fillna() can “fill in” NA values with non-NA data in a couple of ways
#     * Fill gaps forward(method="Pad") or backward(method="bfill")

# + slideshow={"slide_type": "fragment"}
print("fill the data based on the forward data")
print(df.fillna(method="pad"))
print("fill the data based on the backward data")
print(df.fillna(method="bfill"))
# -

# ## Question 1

# +

import pandas as pd
import numpy as np
import os
from scipy import stats


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


if os.path.exists("./"+"Q1_part_a"):
    demogradf=pd.read_pickle("Q1_part_a")
else:
        
    demogra_str=["SEQN","RIDSTATR", "RIAGENDR", "RIDAGEYR",  
                "DMDEDUC2","WTINT2YR"]
    demogra_col_str=["id number", "exam_status", "gender", "age", 
                     "education level", "time"]
    demogra_col_type=[int, int, int, int, int, int, int,
                    int, int, float, float, str]
    demogradf_col_type=dict(zip(demogra_col_str,demogra_col_type))
    
    demogradf=pd.DataFrame()
    time_name=["201"+str(i)+"_201"+str(i+1) for i in range(1,8,2)]
    df_name=["df"+time_name[i] for i in range(4)]
    
    url_path="https://wwwn.cdc.gov/Nchs/Nhanes/"
    url_file_path=["2011-2012/DEMO_G.XPT","2013-2014/DEMO_H.XPT",
                   "2015-2016/DEMO_I.XPT","2017-2018/DEMO_J.XPT"]
    i=0
    for i in range(4):
        if os.path.exists("./"+df_name[i]):
            locals()[df_name[i]]=pd.read_pickle("./"+df_name[i])
            #read the file from local folder
        else:
            locals()[df_name[i]]=pd.read_sas(url_path+url_file_path[i])
            locals()[df_name[i]].to_pickle(df_name[i])
            # download and write local copies of the datasets
        
        demogradf=appendDf(demogradf,locals()[df_name[i]],
                           demogra_str,time_name[i])
    
    demogradf.to_pickle("Q1_part_a")
#######
# end of question 1 part a
#######
if os.path.exists("./"+"Q1_oral"):
    oraldf=pd.read_pickle("Q1_oral")
else:
    oral_heal_col_str=["id number", "oral states"]
    oral_heal_str=["SEQN", "OHDDESTS"]
    oralHeal_col_type=[int,int]
    oralHealdf_col_type=dict(zip(oral_heal_col_str,oralHeal_col_type))
    time_name=["201"+str(i)+"_201"+str(i+1) for i in range(1,8,2)]
    url_path="https://wwwn.cdc.gov/Nchs/Nhanes/"
    
    oraldf=pd.DataFrame()
    url_file_o_path=["2011-2012/OHXDEN_G.XPT","2013-2014/OHXDEN_H.XPT",
                   "2015-2016/OHXDEN_I.XPT","2017-2018/OHXDEN_J.XPT"]
    df_o_name=["df_o_"+time_name[i] for i in range(4)]
    
    i=0
    for i in range(4):
        if os.path.exists("./"+df_o_name[i]):
            locals()[df_o_name[i]]=pd.read_pickle("./"+df_o_name[i])
            #read the file from local folder
        else:
            locals()[df_o_name[i]]=pd.read_sas(url_path+url_file_o_path[i])
            locals()[df_o_name[i]].to_pickle(df_o_name[i])
            # download and write local copies of the datasets
        
        oraldf=appendDf(oraldf,locals()[df_o_name[i]],
                        oral_heal_str,time_name[i])
    oraldf.to_pickle("Q1_oral")

# do we want an outer merge or an inner merge?
df=pd.merge(demogradf, oraldf, on="SEQN", how='outer', suffixes=('', '_y')).\
    filter(regex='^(?!.*_y)')

# age20 with 1 age less than 20 and 2 age greater than 20
df["age20"]=df["RIDAGEYR"].apply(lambda x: 1 if x<20 else 2)  

# college with 1 some college, and 2 no college
df["college"]=df["DMDEDUC2"].apply(lambda x: 2 if x == 4 or x == 5 else 1)
df_order=["SEQN","RIAGENDR","RIDAGEYR","age20",
          "college","RIDSTATR","OHDDESTS"]
df_col_str=["id","gender","age","age20",
          "college","exam_status","ohx_status"]
df=df[df_order]

df["OHDDESTS"] = pd.Categorical(df['OHDDESTS'].replace\
                ({1: "complete", 2: "complete", 3:"missing", None:"missing"}))
df["OHDDESTS"]=df['OHDDESTS'].fillna("missing")
    
df.columns=df_col_str
df.to_pickle("Q1_part_b")
print("valid data number is")
print(df.shape[0])

#######
# end of part b
#######
df_exam = df[df['exam_status'] == 2]
print("number removed " + str(df.shape[0]-df_exam.shape[0]))
print("number remained " + str(df_exam.shape[0]))
#######
# end of part c
#######
d_data_mean=df_exam.groupby("ohx_status").mean()
d_data_std=df_exam.groupby("ohx_status").std()
d_data_sum=df_exam.groupby("ohx_status").sum()

d_data=pd.DataFrame()
d_data_tab=pd.DataFrame()

for i in ["gender","age20","college"]:
    for j in [1,2]:
        temp_d_data=df_exam.groupby([i,"ohx_status"]).count().loc[j,"id"]
        d_data_tab=d_data_tab.append(temp_d_data.apply(lambda x: 
                    str(x)+"("+str(round(100*x/temp_d_data.sum(),1))+"%)").T)
        d_data=d_data.append(temp_d_data.T)
        


        

d_data_tab=d_data_tab.append(d_data_mean["age"].apply(lambda x: round(x,2)).T)
d_data_tab=d_data_tab.append(d_data_std["age"].apply(lambda x: round(x,2)).T)
d_data=d_data.append(d_data_mean["age"].apply(lambda x: round(x,2)).T)
d_data=d_data.append(d_data_std["age"].apply(lambda x: round(x,2)).T)

arrays = [
    ["gender", "gender", "age20", "age20", "college", "college","age","age"],
    ["male", "female", "under 20", "20 or older",
     "True", "False","age mean","age std"],
]
tuples = list(zip(*arrays))
index = pd.MultiIndex.from_tuples(tuples)
d_data_tab=d_data_tab.set_index(index)
d_data=d_data.set_index(index)



print(d_data_tab)
# -

# **oral health test status table**
#
# |         |            | complete     | missing     |
# |---------|------------|--------------|-------------|
# | gender  | male       | 17038(92.4%) | 1393(7.6%)  |
# |         | female     | 17358(91.5%) | 1610(8.5%)  |
# | age20   | under 20   | 14004(88.9%) | 1749(11.1%) |
# |         | 20 or older| 20392(94.2%) | 1254(5.8%)  |
# | college | True       | 22998(90.5%) | 2403(9.5%)  |
# |         | False      | 11398(95.0%) | 600(5.0%)   |
# | age     | age mean   | 33.17        | 21.9        |
# |         | age std    | 24.36        | 26.63       |

# +
# p-value
result=stats.ttest_ind(df_exam.groupby("ohx_status").get_group("complete")\
        ["age"],df_exam.groupby("ohx_status").get_group("missing")["age"])
print("p-value testing for a mean difference in age")
print('%.2e'%result.pvalue)

print("p-value of Chi-square test for gender from oral test complete\
missing")
print('%.2e'%stats.chi2_contingency(d_data.loc["gender"])[1])
print("p-value of Chi-square test for age under 20 from oral test complete\
missing")
print('%.2e'%stats.chi2_contingency(d_data.loc["age20"])[1])
print("p-value of Chi-square test for college from oral test complete\
missing")
print('%.2e'%stats.chi2_contingency(d_data.loc["college"])[1])
# -

# ## Question 2
#
# Credit: the confidence interval calculation is revised from Dr. Henderson's solution

# +

import numpy as np
from confidence_interval import ci_prop
import pandas as pd
import os
import matplotlib.pyplot as plt
from scipy.stats import norm

lvl=0.9
z = norm.ppf(1 - (1 - lvl) / 2)
m=z*z*lvl*(1-lvl)/(0.005**2)
# m is the replicae number for Monte Carlo method to have
# confidence level be no larger than 0.005
md_r=int(m)
x=np.linspace(100,1000,20)
y=np.linspace(0.5,0.999,20)
X, Y = np.meshgrid(x, y)
method=['Mean', 'Normal', 'AC', 'CP', 'Jeffrey']
width_method=[str(method[i])+"_wid" for i in range(5)]


for met in range(5):
    #
    m=method[met]
    locals()[m]=pd.DataFrame()
    locals()[width_method[met]]=pd.DataFrame()
    
    if os.path.exists("./"+m) and os.path.exists("./"+width_method[met]):
        locals()[m]=pd.read_pickle(m)
        locals()[width_method[met]]=pd.read_pickle(width_method[met])
    else:
            
        for n in x:
            n=int(n)
            for p in y:
                count=0
                wid=0
                for i in range(md_r):
                    arr=np.random.binomial(1,p,n)
                    data=ci_prop(arr,lvl,None,m)
                    if data["lwr"] < p < data["upr"]:
                        count+=1 #success
                        wid=data["upr"]-data["lwr"] #confidence interval width
                        
                
                locals()[m].loc[n,p]=count/md_r
                locals()[width_method[met]].loc[n,p]=wid/count
        print(m)
        print("complete")
        locals()[m].to_pickle(m)
        locals()[width_method[met]].to_pickle(width_method[met])
        
        
fig, ax = plt.subplots(3,2,sharex=True)            
for i in range(5):
        
    CS=ax[int(i/3)+i%3-1,int(i/3)].contour(X, Y, locals()[method[i]])
    ax[int(i/3)+i%3-1,int(i/3)].clabel(CS, inline=True, fontsize=5)
    ax[int(i/3)+i%3-1,int(i/3)].set_title(method[i])
fig.delaxes(ax[2,1])
fig.suptitle('confidence interval contour plot')


fig1, ax = plt.subplots(3,2,sharex=True)            
for i in range(5):
        
    CS=ax[int(i/3)+i%3-1,int(i/3)].contour(X, Y, locals()[width_method[i]])
    ax[int(i/3)+i%3-1,int(i/3)].clabel(CS, inline=True, fontsize=5)
    ax[int(i/3)+i%3-1,int(i/3)].set_title(width_method[i])
fig1.delaxes(ax[2,1])
fig1.suptitle('confidence interval width contour plot')

fig2, ax = plt.subplots(3,2,sharex=True)            
for i in range(5):
        
    CS=ax[int(i/3)+i%3-1,int(i/3)].contour(X, Y, 
                            locals()[width_method[i]] / AC_wid)
    ax[int(i/3)+i%3-1,int(i/3)].clabel(CS, inline=True, fontsize=5)
    ax[int(i/3)+i%3-1,int(i/3)].set_title(width_method[i])
fig2.delaxes(ax[2,1])
fig2.suptitle('relative CI width contour plot')

        
# -


