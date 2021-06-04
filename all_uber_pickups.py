import streamlit as st 
import pandas as pd
import numpy as np
import os
import re
import logging
import requests
import matplotlib.pyplot as plt
from pytrends.request import TrendReq
from collections import Counter 







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

name = st.text_input("entrez ici votre nom", value ="", max_chars=None, key=None, type="default", )
if name == "oscar": 
    logging.warning(' this name is already on the DB ')
st.button('enter')

st.write ("your name is: ", name )


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
req = requests.get("https://www.google.com/")
st.markdown(req.cookies._cookies)
req2 = requests.get("https://analytics.google.com/analytics/web/#/report-home/a197647129w273277126p243459380")
st.text(req2.status_code)
st.markdown(req2.text)


pytrends = TrendReq(hl='en-US', tz=360)
searchTrend = ['Wine', 'Beer']
pytrends.build_payload(searchTrend, timeframe = '2020-01-01 2021-01-01', geo='US')
data = pytrends.interest_over_time()
st.line_chart(data)


exec_times_counter = []
exec_times_dico = []

def timer(fn):
    from time import perf_counter
    def inner(*args, **kwargs):
        start_time = perf_counter()
        to_execute = fn(*args, **kwargs)
        end_time = perf_counter()
        execution_time = end_time - start_time
        if(fn.__name__ == "counting_words_counter"):
            exec_times_counter.append(execution_time)
        if(fn.__name__ == "counting_words_dictionnary"):
            exec_times_dico.append(execution_time)
        print("{0} took {1:.8f}s to execute".format(fn.__name__, execution_time))
        return to_execute
    
    return inner
    
@timer
def counting_words_dictionnary(filename):
    file = open(filename)
    str = file.read().replace("\n", " ")
    counts = dict()
    words = str.split()
    for word in words:
        if word in counts:
            counts[word] += 1
        else:
            counts[word] = 1

    return counts

def readFile(filename):
    with open(filename, "r") as data:
        text = data.read()
    return re.findall('[a-z]+', text)

@timer
def counting_words_counter(filename):
    res = readFile(filename)
    return Counter(res)
        

st.markdown("Number of appearance for each words in shakespeare artwork file (using dictionnary):")
st.text(counting_words_dictionnary("shakespeare.txt"))
st.markdown("Number of appearance for each words in shakespeare artwork file (using counter):")
st.text(counting_words_counter("shakespeare.txt"))

for i in range(100):
    counting_words_dictionnary("shakespeare.txt")
    counting_words_counter("shakespeare.txt")

st.markdown("**Chart showing execution times for 100 occurences of the function counting words with dictionnary**")
st.line_chart(exec_times_dico)
st.markdown("**Chart showing execution times for 100 occurences of the function counting words with counter**")
st.line_chart(exec_times_counter)
