#===================================== /   IMPORTING LIBRARIES /   ======================================#   

#Pandas Library
import pandas as pd

#MySQL and SQLAlchemy Libraries
from urllib.parse import quote
from sqlalchemy import create_engine

#Dashboard Libraries
import plotly.express as px
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

st.title(":blue[Top 🔟 States, Districts and Pincode]")


#Creating tabs
tab1, tab2 = st.tabs(['**Transaction**','**User**'])


# ===================================================       /      TRANSACTION TAB    /     ===================================================== #
with tab1:
    st.markdown('This tab has Top 10 Transaction data of every state, district and pincode.')

    #============== / SELECT BOXES / ==============#
    col1, col2 = st.columns(2)

    with col1:
        tr_yr = st.selectbox('**Select Year**', ('2018','2019','2020','2021','2022','2023','2024'),key='tr_yr', index=0)
        tr_qtr = st.selectbox('**Select Quarter**', ('1','2','3','4'),key='tr_qtr', index=0)
    with col2:
        tr_state = st.selectbox('**Select State**',('andaman-&-nicobar-islands', 'andhra-pradesh', 'arunachal-pradesh','assam', 'bihar', 
            'chandigarh', 'chhattisgarh','dadra-&-nagar-haveli-&-daman-&-diu', 'delhi', 'goa', 'gujarat', 'haryana', 'himachal-pradesh', 
            'jammu-&-kashmir', 'jharkhand', 'karnataka', 'kerala', 'ladakh', 'lakshadweep', 'madhya-pradesh','maharashtra', 'manipur', 
            'meghalaya', 'mizoram', 'nagaland','odisha', 'puducherry', 'punjab', 'rajasthan', 'sikkim', 'tamil-nadu', 'telangana', 
            'tripura', 'uttar-pradesh', 'uttarakhand', 'west-bengal','All'),key='tr_state', index=36)
        

    #============== / OUTPUT / ==============#

    col3,col4,col5=st.columns(3)

    # -------------------------       /     All India Transaction        /        ------------------ #
    if tr_state == 'All':
        with col3:

        #Tables and toggle switches with bar plots
            st.markdown(":violet[**Top 10 States**]")
            query_tp1=f"SELECT State, SUM(Transaction_count) AS Transaction_count \
                FROM aggregated_transaction WHERE year='{tr_yr}' AND quater = '{tr_qtr}' \
                GROUP BY state ORDER BY Transaction_count DESC LIMIT 10;"
            df_tp1=pd.read_sql(query_tp1,engine)
            df_tp1.index += 1
            st.dataframe(df_tp1)

            on_1 = st.toggle("Show plot",key='on_1')

        if on_1:
            fig1 = px.bar(df_tp1 , x = 'State', y ='Transaction_count', color ='Transaction_count', 
                color_continuous_scale = 'thermal', title = 'Top 10 states based on Transaction Count', 
                height = 600)
            st.plotly_chart(fig1)

        with col4:
            st.markdown(":violet[**Top 10 Districts**]")
            query_tp2=f"SELECT District_name, Transaction_count FROM top_transaction_dt \
            WHERE year='{tr_yr}' AND quater = '{tr_qtr}' ORDER BY Transaction_count DESC LIMIT 10;"
            df_tp2=pd.read_sql(query_tp2,engine)
            df_tp2.index += 1
            st.dataframe(df_tp2)

            on_2 = st.toggle("Show plot",key='on_2')

        if on_2:
            fig2 = px.bar(df_tp2 , x = 'District_name', y ='Transaction_count', color ='Transaction_count', 
                color_continuous_scale = 'thermal', title = 'Top 10 districts based on Transaction Count', 
                height = 600,)
            st.plotly_chart(fig2)

        with col5:
            st.markdown(":violet[**Top 10 Pincode**]")
            query_tp3=f"SELECT District_pincode, Transaction_count FROM top_transaction_pincode \
                WHERE year='{tr_yr}' AND quater = '{tr_qtr}' ORDER BY Transaction_count DESC LIMIT 10;"
            df_tp3=pd.read_sql(query_tp3,engine)
            df_tp3.index += 1
            st.dataframe(df_tp3)

            on_3 = st.toggle("Show plot",key='on_3')

        if on_3:
            fig3 = px.bar(df_tp3 , x = 'District_pincode', y ='Transaction_count', color ='Transaction_count', 
                color_continuous_scale = 'thermal', title = 'Top 10 pincodes based on Transaction Count', 
                height = 600,)
            fig3.update_layout(xaxis_type='category')
            st.plotly_chart(fig3)


    # -------------------------       /     State wise Transaction        /        ------------------ #
    else: 

        with col3:

            #Tables and toggle switches with bar plots
            st.markdown(":violet[**Top 10 Districts**]")
            query_tp2=f"SELECT District_name, Transaction_count FROM top_transaction_dt \
            WHERE year='{tr_yr}' AND quater = '{tr_qtr}' AND State = '{tr_state}' \
            ORDER BY Transaction_count DESC LIMIT 10;"
            df_tp2=pd.read_sql(query_tp2,engine)
            df_tp2.index += 1
            st.dataframe(df_tp2)

            on_2 = st.toggle("Show plot",key='on_2')

        if on_2:
            fig2 = px.bar(df_tp2 , x = 'District_name', y ='Transaction_count', color ='Transaction_count', 
                color_continuous_scale = 'thermal', title = 'Top 10 districts based on Transaction Count', 
                height = 600,)
            st.plotly_chart(fig2)

        with col4:
            st.markdown(":violet[**Top 10 Pincode**]")
            query_tp3=f"SELECT District_pincode, Transaction_count FROM top_transaction_pincode \
                WHERE year='{tr_yr}' AND quater = '{tr_qtr}' AND State = '{tr_state}' \
                ORDER BY Transaction_count DESC LIMIT 10;"
            df_tp3=pd.read_sql(query_tp3,engine)
            df_tp3.index += 1
            st.dataframe(df_tp3)

            on_3 = st.toggle("Show plot",key='on_3')

        if on_3:
            fig3 = px.bar(df_tp3 , x = 'District_pincode', y ='Transaction_count', color ='Transaction_count', 
                color_continuous_scale = 'thermal', title = 'Top 10 pincodes based on Transaction Count', 
                height = 600,)
            fig3.update_layout(xaxis_type='category')
            st.plotly_chart(fig3)


# ===================================================       /      USER TAB    /     ===================================================== #

with tab2:
    st.markdown('This tab has Top 10 User data of every state, district and pincode.')


    #============== / SELECT BOXES / ==============#
    col1, col2 = st.columns(2)

    with col1:
        u_yr = st.selectbox('**Select Year**', ('2018','2019','2020','2021','2022','2023','2024'),key='u_yr', index=0)
        u_qtr = st.selectbox('**Select Quarter**', ('1','2','3','4'),key='u_qtr', index=0)
    with col2:
        u_state = st.selectbox('**Select State**',('andaman-&-nicobar-islands', 'andhra-pradesh', 'arunachal-pradesh','assam', 'bihar', 
            'chandigarh', 'chhattisgarh','dadra-&-nagar-haveli-&-daman-&-diu', 'delhi', 'goa', 'gujarat', 'haryana', 'himachal-pradesh', 
            'jammu-&-kashmir', 'jharkhand', 'karnataka', 'kerala', 'ladakh', 'lakshadweep', 'madhya-pradesh','maharashtra', 'manipur', 
            'meghalaya', 'mizoram', 'nagaland','odisha', 'puducherry', 'punjab', 'rajasthan', 'sikkim', 'tamil-nadu', 'telangana', 
            'tripura', 'uttar-pradesh', 'uttarakhand', 'west-bengal','All'),key='u_state', index=36)

    
    #============== / OUTPUT / ==============#
    col3, col4, col5=st.columns(3)

    # -------------------------       /     All India Users        /        ------------------ #
    if u_state == 'All':

        #Tables and toggle switches with bar plots
        with col3:
            st.markdown(":violet[**Top 10 States**]")
            query_tp4=f"SELECT State, SUM(Registered_users) AS Registered_users \
                FROM map_user WHERE year='{u_yr}' AND quater = '{u_qtr}' GROUP BY state \
                    ORDER BY Registered_users DESC LIMIT 10;"
            df_tp4=pd.read_sql(query_tp4,engine)
            df_tp4.index += 1
            st.dataframe(df_tp4)

            on_4 = st.toggle("Show plot",key='on_4')

        if on_4:
            fig4 = px.bar(df_tp4 , x = 'State', y ='Registered_users', color ='Registered_users', 
                color_continuous_scale = 'thermal', title = 'Top 10 states based on Registered Users', 
                height = 600,)
            st.plotly_chart(fig4)

        with col4:
            st.markdown(":violet[**Top 10 Districts**]")
            query_tp5=f"SELECT District_name, Registered_users FROM top_user_dt \
                WHERE year='{u_yr}' AND quater = '{u_qtr}' ORDER BY Registered_users DESC LIMIT 10;"
            df_tp5=pd.read_sql(query_tp5,engine)
            df_tp5.index += 1
            st.dataframe(df_tp5)

            on_5 = st.toggle("Show plot",key='on_5')

        if on_5:
            fig5 = px.bar(df_tp5 , x = 'District_name', y ='Registered_users', color ='Registered_users', 
                color_continuous_scale = 'thermal', title = 'Top 10 districts based on Registered Users', 
                height = 600,)
            st.plotly_chart(fig5)

        with col5:
            st.markdown(":violet[**Top 10 Pincode**]")
            query_tp6=f"SELECT District_pincode, Registered_users FROM top_user_pincode \
                WHERE year='{u_yr}' AND quater = '{u_qtr}' ORDER BY Registered_users DESC LIMIT 10;"
            df_tp6=pd.read_sql(query_tp6,engine)
            df_tp6.index += 1
            st.dataframe(df_tp6)

            on_6 = st.toggle("Show plot",key='on_6')

        if on_6:
            fig6 = px.bar(df_tp6 , x = 'District_pincode', y ='Registered_users', color ='Registered_users', 
                color_continuous_scale = 'thermal', title = 'Top 10 pincodes based on Registered Users', 
                height = 600,)
            fig6.update_layout(xaxis_type='category')
            st.plotly_chart(fig6)

    # -------------------------       /     State wise Users        /        ------------------ #
    else:
        
        #Tables and toggle switches with bar plots
        with col3:
            st.markdown(":violet[**Top 10 Districts**]")
            query_tp5=f"SELECT District_name, Registered_users FROM top_user_dt \
                WHERE year='{u_yr}' AND quater = '{u_qtr}' AND State = '{u_state}' \
                ORDER BY Registered_users DESC LIMIT 10;"
            df_tp5=pd.read_sql(query_tp5,engine)
            df_tp5.index += 1
            st.dataframe(df_tp5)

            on_5 = st.toggle("Show plot",key='on_5')

        if on_5:
            fig5 = px.bar(df_tp5 , x = 'District_name', y ='Registered_users', color ='Registered_users', 
                color_continuous_scale = 'thermal', title = 'Top 10 districts based on Registered Users', 
                height = 600,)
            st.plotly_chart(fig5)

        with col4:
            st.markdown(":violet[**Top 10 Pincode**]")
            query_tp6=f"SELECT District_pincode, Registered_users FROM top_user_pincode \
                WHERE year='{u_yr}' AND quater = '{u_qtr}' AND State = '{u_state}' \
                ORDER BY Registered_users DESC LIMIT 10;"
            df_tp6=pd.read_sql(query_tp6,engine)
            df_tp6.index += 1
            st.dataframe(df_tp6)

            on_6 = st.toggle("Show plot",key='on_6')

        if on_6:
            fig6 = px.bar(df_tp6 , x = 'District_pincode', y ='Registered_users', color ='Registered_users', 
                color_continuous_scale = 'thermal', title = 'Top 10 pincodes based on Registered Users', 
                height = 600,)
            fig6.update_layout(xaxis_type='category')
            st.plotly_chart(fig6)