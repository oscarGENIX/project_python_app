

import streamlit as st 
import pandas as pd
import numpy as np
import os
import re

code = """<!-- Global site tag (gtag.js) - Google Analytics -->
<script async src="https://www.googletagmanager.com/gtag/js?id=UA-197647129-1"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'UA-197647129-1');
</script>"""

a=os.path.dirname(st.__file__) + '/static/index.html'
with open(a, 'r') as f:
    data=f.read()
    if len(re.findall('UA-', data)) == 0:
        with open(a, 'w') as f:
            newdata=re.sub('<head>','<head>' + code, data)
            f.write(newdata)
st.title('Need to know how many Uber are currently in NYC?')
Date_Column= "date/time"
Data_Url= ('https://s3-us-west-2.amazonaws.com/''streamlit-demo-data/uber-raw-data-sep14.csv.gz')

@st.cache
def load_data(nrows):
    data2= pd.read_csv(Data_Url, nrows=nrows)
    lowercase = lambda x: str(x).lower()
    data2.rename(lowercase, axis='columns', inplace=True)
    data2[Date_Column] = pd.to_datetime(data2[Date_Column])
    return data2

data_load_state = st.text('Loading data...')
data2 = load_data(10000)
data_load_state.text('Done! ')

if st.checkbox('Show raw data'): 
    st.subheader('Raw data')
    st.write(data2)

st.subheader('Number of pickups by hour')
hist_values = np.histogram(data2[Date_Column].dt.hour, bins=24, range=(0,24))[0]
st.bar_chart(hist_values)

hour_to_filter = st.slider('hour', 0, 23, 17)
filtered_data = data2[data2[Date_Column].dt.hour == hour_to_filter]
st.subheader(f'Map of all pickups at{hour_to_filter}:00')
st.map(filtered_data)


if st.checkbox('Wanna see all the pickups made today? '): 
    st.subheader('Map of all pickups')
    st.map(data2)