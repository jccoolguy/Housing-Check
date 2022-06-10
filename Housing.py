# -*- coding: utf-8 -*-
"""
Created on Wed Jun  8 15:42:56 2022

@author: Jack Cunningham
"""
import streamlit as st
import nasdaqdatalink
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

#Setting NasdaqDataLink Up
nasdaqdatalink.ApiConfig.api_key='Y9AmWQk8hv27pFoxJq5c'

#Pulling Zillow Region Data
zillow_regions=pd.DataFrame(nasdaqdatalink.get_table('ZILLOW/REGIONS',region_type=['city','neigh'],paginate=True))


#Extracting important information
zillow_regions['region'].str.split('; ')
zillow_regions[['Searchable location','State','Metro Area','County','Extra']]=zillow_regions['region'].str.split('; ',expand=True)

#Getting location from user

zillow_regions['town+state']=zillow_regions['Searchable location']+', '+zillow_regions['State']
with st.sidebar:
    st.header("Housing Check")
    searched_location=st.selectbox("Type your town followed by state",options=zillow_regions['town+state'])

#Finding Housing Data

searched_region_id=zillow_regions.loc[zillow_regions['town+state']==searched_location]['region_id']
housing_data=pd.DataFrame(nasdaqdatalink.get_table('ZILLOW/DATA',region_id=searched_region_id))
housing_data_ZSFH=housing_data.loc[housing_data['indicator_id']=="ZSFH"]
#Adjusting DataSet
housing_data_ZSFH.set_index('date',inplace=True)
housing_data_ZSFH=housing_data_ZSFH.sort_index(ascending=True)

#Adding a YOY percentage change column
housing_data_ZSFH['pct_yoy']=housing_data_ZSFH['value'].pct_change(12)*100


#Grabbing most recent data for metrics
most_recent=housing_data_ZSFH.tail(1)
current_value=most_recent['value']
current_yoy=most_recent['pct_yoy']


#Displaying metrics
col1,col2=st.columns(2)
col1.metric("Average Single Family Home Value",round(current_value,0))
col2.metric("One Year Percentage Change",round(current_yoy,2))
#Displaying charts
st.line_chart(data=housing_data_ZSFH['value'])
st.line_chart(data=housing_data_ZSFH['pct_yoy'])


