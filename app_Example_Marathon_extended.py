# -*- coding: utf-8 -*-
"""
Created on Thu Jan 16 09:33:27 2020
Adapted example based on Book: Van der Plas, see EBook PDF Chapter 4
@author: Andreas Traut
"""

import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

st.title("Example Marathon")

#%% 1 Read the data. The function "convert" will split the Data after ":"
def convert(s):
    h, m, s = map(int, s.split(':'))
    return pd.Timedelta(hours=h, minutes=m, seconds=s)  #EBook PDF page 350: return pd.datetools.timedelta(...) does not work

data=pd.read_csv('marathon-data_extended.csv', converters={'split':convert, 'final':convert})
# print(data.dtypes)

#%% 2 Apply the converter "convert" to transform the hh:mm:ss. 
data['split_sec'] = data['split'] / np.timedelta64(1, 's') #EBook PDF page 351: data['split_sec'] = data['split'].astype(int) / 1E9  does not work

data['final_sec'] = data['final'] / np.timedelta64(1, 's')

#%% 3 Add more colums. 
data['size_to_weight'] = data['size'] / data['weight']
# print(data.head())
st.write(data)

#%% 4 Doppel-Abbildung (Punktewolke mit Histogramm) mit x=size und y=weight
with sns.axes_style('white'):
    g = sns.jointplot("size", "weight", data, kind='hex')
    g.ax_joint.plot(np.linspace(min(data['size']), max(data['size'])), 
                    np.linspace(min(data['weight']), max(data['weight'])), ':k')
st.pyplot(g)

#%% 5 Histogram for 'size' and 'weight' (distplot=Distribution Plot) 
g = sns.displot(data['size'], kde=False);
st.pyplot(g)
# plt.show()
g = sns.displot(data['weight'], kde=False)
st.pyplot(g)

#%% 6 PairGrids with variables 'nationality', 'size', 'final_sec', 'weight'
#   colors for gender (hue) is GreenBlue (GnBu)
g = sns.PairGrid(data, vars=['nationality', 'size', 'final_sec', 'weight'],
                  hue='gender', palette='GnBu_r')
g.map(plt.scatter, alpha=0.8)
g.add_legend();
st.pyplot(g)

#%% 7 KernelDensity (kde) for column "size_to_weight" 
sns.kdeplot(data.size_to_weight[data.nationality=='DE'], label='Deutschland', shade=True)
sns.kdeplot(data.size_to_weight[data.nationality=='AU'], label='Österreich', shade=True)
plt.xlabel('size_to_weight');
# plt.show()
st.pyplot(plt)

#%% 8 KernelDensity (kde) for column "weight" 
sns.kdeplot(data.weight[data.nationality=='DE'], label='Deutschland', shade=True)
sns.kdeplot(data.weight[data.nationality=='AU'], label='Österreich', shade=True)
plt.xlabel('size');
st.pyplot(plt)

#%% 9 Regression Plot for "weight" and "size"
h = sns.lmplot('weight', 'size', hue='nationality', data=data[data.gender=="M"], markers=".")              
h = sns.lmplot('weight', 'size', hue='nationality', data=data[data.gender=="W"], markers=".")              
st.pyplot(h)

#%% 10 Violinplot using "size" and "nationality"
men = (data.gender == 'M')
women = (data.gender == 'W')
fig, ax = plt.subplots() 
with sns.axes_style(style=None):
    ax=sns.violinplot("size", "nationality", hue="gender", data=data,
                    split=True, inner="quartile",
                    palette=["lightblue", "lightpink"]);
# plt.show()
st.pyplot(fig)

#%% 11 Violinplot using "weight" and "nationality"

fig, ax = plt.subplots() 
with sns.axes_style(style=None):
    ax=sns.violinplot("weight", "nationality", hue="gender", data=data,
                    split=True, inner="quartile",
                    palette=["lightblue", "lightpink"]);
st.pyplot(fig)

