"""
Developer: Rajat Shinde
Api Sources-
1. [nsetools](https://nsetools.readthedocs.io/en/latest/index.html)
2. [nsepy](https://nsepy.readthedocs.io/en/latest/)
3. [NSE India](http://www.nseindia.com/)
"""

import nsetools as nse
import streamlit as st
import nsepy
from nsepy import get_history
from datetime import date
import datetime
from nsetools import Nse
import pandas as pd
import numpy as np

st.write("""# ANSESAI: App for NSE Stocks And Indices""")
st.write("""### Developed by- [Rajat Shinde](http://home.iitb.ac.in/~rajatshinde)""")
st.write("##### *Note: Press Generate Charts button mutiple times if data is not fetched.*")
st.write(" ")

# #Importing Nse class instance
nse = Nse()

#Get advances decline information
if st.sidebar.button('Get Advances-Declines'):
	st.table(nse.get_advances_declines())


#Select among Traded Stock Codes and Index Codes
codeList = ['Traded Stock Codes', 'Index Codes']
codeSelect = st.sidebar.selectbox(
	'Which code do you want to analyze?',
	codeList)
# st.write('Selected Option:', codeSelect)

all_stock_codes = nse.get_stock_codes()
all_stock_codes_values = list(nse.get_stock_codes().values())

if(codeSelect == 'Traded Stock Codes'):
	option = st.sidebar.selectbox(
    'Which Stock do you want to analyze?',
     all_stock_codes_values[1:])
	# st.write('You have selected:', option)
	if st.sidebar.button('Get Stock Quote'):
		# st.write(all_stock_codes)
		reqKey = [key  for (key, value) in all_stock_codes.items() if value == option]
		st.write(nse.get_quote(reqKey[0]))
	
else:
	option = st.sidebar.selectbox(
    'Which Index do you want to analyze?',
     list(nse.get_index_list()), index=1)
	#st.write('You have selected:', option)
	if st.sidebar.button('Get Index Quote'):
		# st.write(all_stock_codes[option])
		st.write(nse.get_index_quote(option))

#Button to get Open Price, Closed Price, High and Low
#TODO: Replace data selection by slider
startDate = st.sidebar.date_input("Select start date",datetime.date(2020, 3, 6))
endDate = st.sidebar.date_input("Select end date",datetime.date(2020, 7, 6))

if st.sidebar.button('Generate Charts'):
	st.write("Fetching data for the %s %s!"%(option, codeSelect[:-1]))
	if(codeSelect == 'Traded Stock Codes'):
		data = get_history(symbol=option, start=startDate, end=endDate)
	else:
		data = get_history(symbol=option, start=startDate, end=endDate, index=True)

	st.write("""### Closing Price Chart""")
	st.line_chart(data.Close)
	st.write("""### Opening Price Chart""")
	st.line_chart(data.Open)
	st.write("""### High Price Chart""")
	st.bar_chart(data.High)
	st.write("""### Low Price Chart""")
	st.bar_chart(data.Low)
	st.write("""### Opening/Closing Price Chart""")
	arr1 = np.vstack([data.Open, data.Close])
	st.line_chart(pd.DataFrame(arr1.T, columns=["Opening", "Closing"]))
	st.write("""### High/Low Price Chart""")
	arr2 = np.vstack([data.High, data.Low])
	st.line_chart(pd.DataFrame(arr2.T, columns=["High", "Low"]))
	st.write("""### Combined Price Chart""")
	arr = np.vstack([data.Open, data.Close, data.High, data.Low])
	st.line_chart(pd.DataFrame(arr.T, columns=["Opening", "Closing", "High", "Low"]))
	st.write("""### Volume""")
	st.line_chart(data.Volume)
	


