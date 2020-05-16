#!/usr/bin/env python
# coding: utf-8
import json
import chart_studio.plotly as py
import numpy as np
import pandas as pd
import plotly.graph_objs as go
import scrap
import requests
API="https://d85517ae.ngrok.io"

def save_news():
	news_list=requests.get(API+"/api/news").json()
	with open("news.save","w") as newsfile:
		json.dump(news_list,newsfile)
def save_stats():
	total_stats={"world":dict(),"india":dict()}
	india_stats=requests.get(API+"/api/total").json()
	total_stats['india']={"Total":india_stats['cases'],"Active":india_stats['hospitalized'],"Cured":india_stats['cured'],"Deaths":india_stats['death']}
	world_stats=scrap.scrap_data()['data'][0]
	total_stats['world']={"Total":world_stats['cases'],"Active":world_stats['cases']-(world_stats['death']+world_stats['recovered']),"Cured":world_stats['recovered'],"Deaths":world_stats['death']}
	with open("stats.save","w") as statfile:
		json.dump(total_stats,statfile)
def save_india():
	india_map=requests.get(API+"/india").text
	with open("india.html","w",encoding="utf8") as map:
		map.write(india_map)
def save_world():
	df=pd.read_csv('2014_world_gdp_with_codes.csv')
	df3=pd.DataFrame.from_dict(pd.read_json('data.json'))
	df3=df3['data']
	country=[]
	active=[]
	death=[]
	recover=[]
	for i in df3:
		country.append(i['country'])
		death.append(i['death'])
		recover.append(i['recovered'])
		active.append(i['cases'])
	df2=pd.DataFrame({'COUNTRY':country,'active':active,'recover':recover,'death':death})
	df=pd.merge(df,df2,how='inner',on='COUNTRY')
	fig = go.Figure()
	data=dict(type='choropleth',locations=df['CODE'],z=df['active'],
			 text=df['active'],colorbar={'title':'Country wise case distribution'})
	layout=dict(title='COVID-19 outbreak',geo=dict(showframe=False, projection={'type':'natural earth'}))
	chormap=go.Figure([data],layout)
	chormap.write_html('world.html')
def save_data():
	save_news()
	save_stats()
	save_india()
	save_world()



