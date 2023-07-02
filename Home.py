import streamlit as st
from pytrends.request import TrendReq
import pandas as pd
from textblob import TextBlob
import os

from llama_index import (
    GPTVectorStoreIndex, Document, SimpleDirectoryReader,
    QuestionAnswerPrompt, LLMPredictor, ServiceContext
)
import json
from langchain import OpenAI
from llama_index.retrievers import VectorIndexRetriever
from llama_index.query_engine import RetrieverQueryEngine



st.set_page_config(page_title=None, page_icon=None, layout="wide", initial_sidebar_state="auto", menu_items=None)

#image
st.image("https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQNmbbuVqoA2mtNcl9VEKVXXoS4ZxXuI4y4CQ&usqp=CAU", width=100, height=100)

# Initialize pytrends

st.markdown('<p style="font-size:30px; color:black; text-align:center;">Chatbot for helping Hotel marketers for promoting their businesses in Galle District</p>', unsafe_allow_html=True)

# Initialize pytrends
pytrends = TrendReq(hl='en-US', tz=360)

# List of initial keywords
initial_keywords = ['Galle Tourism', 'Galle', 'Hotels Galle', 'Resorts Galle ','Koggala Beach Hotels', 'Unawatuna Beach Hotels ', 'Galle Restaurants', 'Bentota Hotels']

# Initialize session state


if 'data2' not in st.session_state:
    st.session_state['data2'] = pd.DataFrame()

if 'data3' not in st.session_state:
    st.session_state['data3'] = pd.DataFrame()

tab1, tab2, tab3, tab4 = st.tabs(["Search Query Data Analytics and Forecasting", "Sentimental Analysis", "Price Optimization", "Chatbot"])

with st.expander("data"):
    col1, col2, col3 =  st.columns(3)



#####################   tab1 #@######################################################

# with tab1:
    # Create a for keyword selection
selected_keywords = tab1.multiselect('Select existing keywords', initial_keywords)


# When keywords are selected, fetch data from Google Trends and display it
if tab1.button('Fetch Google Trends data for selected keywords'):
    # Define the payload
    kw_list = selected_keywords

    # Get Google Trends data
    pytrends.build_payload(kw_list, timeframe='all')

    # Get interest over time
    data = pytrends.interest_over_time()
    if not data.empty:
        data = data.drop(labels=['isPartial'],axis='columns')

        # Save the data to the session state
        if 'data' not in st.session_state:

# st.session_state['data'] = pd.DataFrame()
            st.session_state['data'] = data
if 'data' in st.session_state:
    col1.write("## Trends Data")

    col1.write(st.session_state['data'])







#####################   tab2 #@######################################################

# with tab2:
    # Upload file

uploaded_file = tab2.file_uploader("Upload scraped data for reviews")
if uploaded_file is not None:
    st.session_state['data2'] = pd.read_csv(uploaded_file)
    col2.write("## Sentimental Data")
    col2.write(st.session_state['data2'])
    



#####################   tab1 #@######################################################

# with tab3:
    # Upload file

uploaded_file2 = tab3.file_uploader("Upload scraped data for prices")
if uploaded_file2 is not None:
    st.session_state['data3'] = pd.read_csv(uploaded_file2)
    
    col3.write("## Pricing Data")
    
    col3.write(st.session_state['data3'])
    
  


# with tab4:

if tab4.button('Save data and create index'):
    # Check if the 'data' directory exists
    if not os.path.exists('data'):
        os.makedirs('data')

    # Save the data from session state to CSV files
    if 'data' in st.session_state:
        st.session_state['data'].to_csv('data/data.csv')
        st.success('Data saved successfully in data/data.csv')

    if not st.session_state['data2'].empty:
        st.session_state['data2'].to_csv('data/data2.csv')
        st.success('Data2 saved successfully in data/data2.csv')

    if not st.session_state['data3'].empty:
        st.session_state['data3'].to_csv('data/data3.csv')
        st.success('Data3 saved successfully in data/data3.csv')

    documents = SimpleDirectoryReader('data').load_data()
    index = GPTVectorStoreIndex.from_documents(documents)
    query_engine = index.as_query_engine()
    if "query_engine" not in st.session_state:
        st.session_state.query_engine = query_engine

tab4.write("Chat Bot")
ques = tab4.text_input("Ask question")
ask = tab4.button("submit question")

if ask:
    response = st.session_state.query_engine.query(ques)
    if response is None:
        st.write("Please provide more details about the question.")
    else:
        st.write(response.response)


