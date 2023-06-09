# -*- coding: utf-8 -*-
"""Data Visualization Coursework.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1wVfPIZ9WdG3BtDK5j43rUlbthfManEy6

# **Data Visualisation Coursework**

**Import Libraries**
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
from plotly.subplots import make_subplots
from sklearn.preprocessing import MinMaxScaler 
import plotly.graph_objects as go
from datetime import datetime

"""**Reading Files**"""

covid_cases=pd.read_csv("covid_cases1.csv")
vaccine_data=pd.read_csv("vacc_data1.csv")
covid_meta=pd.read_csv("covid_meta.csv")

"""**Statistical calculation**"""

covid_cases.describe()

"""### **Covid Cases per Million by Country**"""

fig = px.choropleth(covid_cases, locations='Name', locationmode='country names',
                    color='Cases - cumulative total per 100000 population',
                    hover_name='Name', projection='natural earth',
                    color_continuous_scale='Greens')
fig.update_layout(title="COVID-19 Cases by Country", font_color='#D60CFE')

fig.show()

"""### **Top 10 Active Cases in Countries**

"""

covid_cases['Active_Cases']=covid_cases['Cases - cumulative total']-covid_cases['Deaths - cumulative total']

top_10_active_cases=covid_cases.groupby(by='Name').max()[['Active_Cases']].sort_values(by=['Active_Cases'], ascending=False).reset_index()
fig=plt.figure(figsize=(16,9))
plt.title("Top 10 Countries with most Active Cases", color='#D60CFE')
ax=sns.barplot(data=top_10_active_cases.iloc[1:10], y="Active_Cases", x="Name", linewidth=2,edgecolor="gold", width=0.5, alpha=0.75)
plt.xlabel("Countries")
plt.ylabel("Total Active Cases")

"""### **Total Cases over Time**"""

covid_meta['Date_reported'] = pd.to_datetime(covid_meta['Date_reported'])
grouped = covid_meta.groupby('Date_reported')['Cumulative_cases'].sum()
plt.plot(grouped.index, grouped.values, color='gold')
plt.xlabel('Date_reported')
plt.xticks(rotation=45)
plt.ylabel('Cumulative_cases')
plt.title('Cumulative Cases over Time', color='#D60CFE')
plt.show()

"""### **COVID-19 cases and deaths per Million**"""

sns.set(style="whitegrid")
fig, ax = plt.subplots(figsize=(10, 6))
sns.scatterplot(data=covid_cases, x="Cases - cumulative total per 100000 population", y="Deaths - cumulative total per 100000 population", size="Cases - cumulative total", hue="WHO Region", sizes=(20, 500), alpha=0.8, ax=ax)
ax.set_xlabel("Cases per 100000 people")
ax.set_ylabel("Deaths per 100000 people")
plt.title("COVID-19 Cases and Deaths", color='#D60CFE')
plt.show()

"""### **Death Rate Region wise**"""

country_wise=pd.pivot_table(covid_cases, values=["Cases - cumulative total", "Deaths - cumulative total"], 
                            index="WHO Region", aggfunc=max)
country_wise["Death_Rate"]=country_wise["Deaths - cumulative total"]*100/country_wise["Cases - cumulative total"]
country_wise=country_wise.sort_values(by="Cases - cumulative total", ascending=False)
country_wise.style.background_gradient(cmap="cubehelix")

"""### **Top Countries with Highest Deaths**"""

top_10_death_cases=covid_cases.groupby(by='Name').max()[['Deaths - cumulative total']].sort_values(by=['Deaths - cumulative total'], ascending=False).reset_index()
fig=plt.figure(figsize=(16,9))
plt.title("Top 10 Countries with most Death Cases", color='#D60CFE')
ax=sns.barplot(data=top_10_death_cases.iloc[1:12], y="Deaths - cumulative total", x="Name", linewidth=2,edgecolor="black", width=0.5, alpha=0.75)
plt.xlabel("Countries")
plt.ylabel("Total Death Cases")

"""### **Total Deaths by Each Country**"""

covid_meta['Date']=pd.to_datetime(covid_meta['Date_reported'])
dfs=list(covid_meta.groupby("Country"))
first_title = dfs[0][0]+'1 here represents :2399'
traces = []
buttons = []
for i,d in enumerate(dfs):
    visible=[False]*len(dfs)
    visible[i]=True
    name=d[0]
    scale=MinMaxScaler()
    yp=scale.fit_transform(d[1][['Cumulative_deaths']])
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=d[1]['Date'],y=[i[0] for i in yp]))
    mm=max(d[1]['Cumulative_deaths'])
    traces.append(
    fig.update_traces(visible=True if i==0 else False).data[0])
    buttons.append(dict(label=name,
                        method="update",
                        args=[{"visible":visible},
                              {"title":str(name)+' '*30+'1 here represents :'+str(mm)}]))

updatemenus = [{'active':0, "buttons":buttons}]
shapes=[({'type': 'line',
               'xref': 'x',
               'yref': 'y',
               'x0': '2020-12-20' ,
               'y0': 0,
               'x1': '2020-12-20',
               'y1': 1})]
fig = go.Figure(data=traces,
                 layout=dict(updatemenus=updatemenus,shapes=shapes,template='plotly_dark'))
fig.update_layout(title=first_title, title_x=0.5)
fig.show()

"""### **Types of Vaccines Used**"""

s=covid_meta.drop_duplicates(subset=['WHO_region'])['vaccines'].apply(lambda x: x.split(','))
dic={}
for i in s:
    for j in i :
        if j[0]==' ':
            k= j[1:]
        elif j[-1]==' ':
            k=j[:-1]
        else:
            k=j
        if k not in dic :
            dic[k]=1
        else:
            dic[k]+=1
px.bar(x=list(dic.keys()),y=list(dic.values()),title='Types Of Vaccines', color=list(dic.keys()),template='plotly_dark',labels={'x':'Vaccine Name','y':'Total Count'})

"""### **Total Vaccinations Region wise**"""

colors = ['#1b5c57', '#15876a', '#44b26c', '#89db5f', '#ddff46']

vacc_data = vaccine_data[['WHO_REGION', 'TOTAL_VACCINATIONS']]
vacc_data = vacc_data.sort_values(by='TOTAL_VACCINATIONS', ascending=False)
top_countries = vacc_data.head(5)

plt.pie(top_countries['TOTAL_VACCINATIONS'], labels=top_countries['WHO_REGION'], colors=colors,autopct='%1.1f%%', startangle=90,
        textprops={'color':'#DB0AFC', 'fontsize': 8, 'weight':'bold'})

plt.title('Total Vaccinations Region wise', color='#D60CFE')

plt.show()

"""### **Total Vaccinations Per Million**"""

data=pd.read_csv("covid_meta.csv")
fig=px.choropleth(data_frame=data,
                          locations=data['Country'],
                          locationmode='country names',
                          color=data['daily_vaccinations_per_million'],
                          animation_frame=data['Date_reported'],
                          animation_group=data['vaccines'])
fig.update_layout(dict1={'title':'Daily Vaccinations Per Million'}, font_color='#D60CFE')

fig.show()