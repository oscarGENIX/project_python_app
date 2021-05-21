import streamlit as st 
import pandas as pd
import numpy as np

st.title('Need to find an Uber in NYC?')
Date_Column= "date/time"
Data_Url= ('https://s3-us-west-2.amazonaws.com/''streamlit-demo-data/uber-raw-data-sep14.csv.gz')

@st.cache
def load_data(nrows):
    data= pd.read_csv(Data_Url, nrows=nrows)
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis='columns', inplace=True)
    data[Date_Column] = pd.to_datetime(data[Date_Column])
    return data 

data_load_state = st.text('Loading data...')
data = load_data(10000)
data_load_state.text('Done! ')

if st.checkbox('Show raw data'): 
    st.subheader('Raw data')
    st.write(data)

st.subheader('Number of pickups by hour')
hist_values = np.histogram(data[Date_Column].dt.hour, bins=24, range=(0,24))[0]
st.bar_chart(hist_values)

hour_to_filter = st.slider('hour', 0, 23, 17)
filtered_data = data[data[Date_Column].dt.hour == hour_to_filter]
st.subheader(f'Map of all pickups at{hour_to_filter}:00')
st.map(filtered_data)


if st.checkbox('Wanna see all the pickups during today? '): 
    st.subheader('Map of all pickups')
    st.map(data)