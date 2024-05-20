#================================ /   IMPORTING LIBRARIES /   =================================#   
#Pandas Library
import pandas as pd

#MySQL and SQLAlchemy Libraries
from urllib.parse import quote
from sqlalchemy import create_engine

#Dashboard Libraries
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

#========================= /   RE-ESTABLISHING CONNECTION WITH SQLALCHEMY   / ===========================#

#Configuring
db_config = {
    'host':'localhost',
    'user':'root',
    'password':'1234',
    'database':'phonepe_db'
    }
encoded_password = quote(db_config['password'])

#Connection for SQLAlchemy
connection_url = f"mysql+mysqlconnector://{db_config['user']}:{encoded_password}@{db_config['host']}/{db_config['database']}"
engine=create_engine(connection_url)

#================================== /   DASHBOARD SETUP   / ================================#


st.set_page_config(
    page_title="Phonepe Pulse Data Visualization",
    page_icon="📊",
    layout="wide")

page_bg_img = f"""
<style>
[data-testid="stAppViewContainer"] > .main {{
background: linear-gradient(#c1ade0,#f7f7f7);
ckground-attachment: local;
}}
[data-testid="stHeader"] {{
background: rgba(0,0,0,0);
title: 
}}
</style>
"""

st.markdown(page_bg_img, unsafe_allow_html=True)

st.title(":blue[User Analysis 📊 of PhonePe Pulse Data]")

sql_query = st.selectbox('**Questions regarding the PhonePe Pulse Data**',
('1. What is the Total Transaction count of every state from 2018 to 2024 Q1?',
'2. What is the Total Transaction amount of all the states from 2018 to 2024 Q1?',
'3. What are the Transaction counts and Total Transaction amount of each state?',
'4. What is the average Transaction value of each state?',
'5. What is the Trasaction count for each Transaction type?',
'6. Which year has highest number of regiesterd  users?',
'7. Which year marks the highest transaction count and transaction amount?',
'8. Which 10 states have the least number of registered users?',
'9. Which 20 districts have the least number of transaction count',
'10. Which 20 districts have the least number of users?'), 
key = 'question', index=0)


#================================== /   QUERYING AND OUTPUT PLOTS   / ================================#

if sql_query == '1. What is the Total Transaction count of every state from 2018 to 2024 Q1?':
    query_1="SELECT State, Year, SUM(Transaction_count) AS Transaction_count \
          FROM aggregated_transaction GROUP BY State,year;"
    df_1 = pd.read_sql(query_1, engine)
    fig_1 = px.bar(df_1, x='State', y='Transaction_count',  color ='Year', 
         title='Transaction Count of States from 2018 to 2024 Quater 1')
    st.plotly_chart(fig_1,use_container_width=True)

elif sql_query == '2. What is the Total Transaction amount of all the states from 2018 to 2024 Q1?':
    query_2 = "SELECT State, Year, ROUND(SUM(Transaction_amount)) AS Total_Transaction_Amount \
        FROM aggregated_transaction GROUP BY State, year;"
    df_2 = pd.read_sql(query_2,engine)
    fig_2 = px.bar(df_2, x='State', y='Total_Transaction_Amount', color='Year', 
        title='Transaction Amounts of States from 2018 to 2024 Quater 1')
    st.plotly_chart(fig_2,use_container_width=True)

elif sql_query == '3. What are the Transaction counts and Total Transaction amount of each state?':
    query_3 = "SELECT State, SUM(Transaction_count) AS Transaction_count, \
        ROUND(MAX(Transaction_amount)) AS Total_Transaction_Amount \
        FROM aggregated_transaction GROUP BY State;"
    df_3 = pd.read_sql(query_3,engine)
    fig_3 = px.scatter(df_3, x="Transaction_count", y="Total_Transaction_Amount", color="State",
                size='Total_Transaction_Amount', hover_data=['State'],
                title='Transaction Count Vs Total transaction Amount of all the states')
    st.plotly_chart(fig_3,use_container_width=True)

elif sql_query == '4. What is the average Transaction value of each state?':
    query_4 = "SELECT State, ROUND(AVG(transaction_amount/transaction_count)) AS Avg_transaction_value \
        FROM aggregated_transaction GROUP BY state;"
    df_4 = pd.read_sql(query_4,engine)
    fig_4 = px.bar(df_4, x='State', y='Avg_transaction_value', color='Avg_transaction_value', 
        color_continuous_scale = 'thermal', title='Average Transaction Values of States from 2018 to 2024 Quater 1')
    st.plotly_chart(fig_4,use_container_width=True)

elif sql_query == '5. What is the Trasaction count for each Transaction type?':
    query_5 = "SELECT Transaction_type, SUM(Transaction_count) AS Transaction_count \
        FROM aggregated_transaction GROUP BY Transaction_type"
    df_5 = pd.read_sql(query_5,engine)
    fig_5 = px.bar(df_5, x='Transaction_type', y='Transaction_count', color='Transaction_count', 
        color_continuous_scale = 'thermal', title='Transaction Count for every Transaction type')
    st.plotly_chart(fig_5,use_container_width=True)
   
elif sql_query == '6. Which year has highest number of regiesterd  users?':
    query_6 = "SELECT year, SUM(Registered_users) AS Registered_users FROM map_user GROUP BY year;"
    df_6 = pd.read_sql(query_6,engine)
    fig_6 = px.bar(df_6, x='year', y='Registered_users', color='Registered_users', 
        color_continuous_scale = 'thermal', title='Total no. of Registered users every year')
    st.plotly_chart(fig_6,use_container_width=True)

elif sql_query == '7. Which year marks the highest transaction count and transaction amount?':
    query_7 = "SELECT year, SUM(Transaction_count) AS Transaction_count, ROUND(SUM(Transaction_amount)) AS Total_Transaction_Amount \
        FROM aggregated_transaction GROUP BY year;"
    df_7 = pd.read_sql(query_7,engine)
    fig_7a = px.bar(df_7,x='year',y='Total_Transaction_Amount', color='Total_Transaction_Amount', 
        color_continuous_scale = 'thermal', title='Transaction amount of all states each year')
    st.plotly_chart(fig_7a,use_container_width=True)
    fig_7b = px.bar(df_7,x='year',y='Transaction_count', color='Transaction_count', 
        color_continuous_scale = 'thermal', title='Transaction count of all states each year')
    st.plotly_chart(fig_7b,use_container_width=True)

elif sql_query=='8. Which 10 states have the least number of registered users?': 
    query_8="SELECT State, SUM(User_count) AS Registered_users \
        FROM aggregated_user GROUP BY State ORDER BY Registered_users LIMIT 10;"
    df_8 = pd.read_sql(query_8,engine)
    fig_8 = px.bar(df_8,x='State',y='Registered_users', color='Registered_users', 
        color_continuous_scale = 'thermal', title='10 States with least Registered users')
    st.plotly_chart(fig_8,use_container_width=True)

elif sql_query == '9. Which 20 districts have the least number of transaction count':
    query_9="SELECT District_name, SUM(Transaction_count) AS Transaction_count \
        FROM map_transaction GROUP BY District_name ORDER BY Transaction_count LIMIT 10;"
    df_9 = pd.read_sql(query_9,engine)
    fig_9 = px.bar(df_9,x='District_name',y='Transaction_count', color='Transaction_count', 
        color_continuous_scale = 'thermal', title='20 Districts with least Transaction count')
    st.plotly_chart(fig_9,use_container_width=True)

elif '10. Which 20 districts have the least number of users?':
    query_10="SELECT District_name, SUM(Registered_users) AS Registered_users \
        FROM map_user GROUP BY District_name ORDER BY Registered_users LIMIT 10;"
    df_10 = pd.read_sql(query_10,engine)
    fig_10 = px.bar(df_10,x='District_name',y='Registered_users', color='Registered_users', 
        color_continuous_scale = 'thermal', title='20 Districts with least Registered users')
    st.plotly_chart(fig_10,use_container_width=True)
