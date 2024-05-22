#==================================== /   IMPORTING LIBRARIES /   =======================================#   

#File handling Libraries
import json
import requests

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


#========================================== /   DEFINING A FUNCTION   / ================================#

#Formats an integer with commas as thousand separators
def format_int_with_commas(x):
    return f"{x:,}"


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

st.title(":blue[Transaction and User Data of India🧾]")

#Creating tabs
tab1, tab2 = st.tabs(['**Transaction**','**User**'])

# ===================================================       /      TRANSACTION TAB    /     ===================================================== #

with tab1:

    #Select boxes
    st.markdown('This tab has Transaction data of whole of India and every state.')
    col1, col2, col3 = st.columns(3)
    with col1:
        tr_yr = st.selectbox('**Select Year**', ('2018','2019','2020','2021','2022','2023','2024'),key='tr_yr', index=0)
        tr_qtr = st.selectbox('**Select Quarter**', ('1','2','3','4'),key='tr_qtr', index=0)
    with col2:
        tr_state = st.selectbox('**Select State**',('andaman-&-nicobar-islands', 'andhra-pradesh', 'arunachal-pradesh','assam', 'bihar', 
            'chandigarh', 'chhattisgarh','dadra-&-nagar-haveli-&-daman-&-diu', 'delhi', 'goa', 'gujarat', 'haryana', 'himachal-pradesh', 
            'jammu-&-kashmir', 'jharkhand', 'karnataka', 'kerala', 'ladakh', 'lakshadweep', 'madhya-pradesh','maharashtra', 'manipur', 
            'meghalaya', 'mizoram', 'nagaland','odisha', 'puducherry', 'punjab', 'rajasthan', 'sikkim', 'tamil-nadu', 'telangana', 
            'tripura', 'uttar-pradesh', 'uttarakhand', 'west-bengal','All'),key='tr_state', index=36)
        
    with col3:
        tr_type = st.selectbox('**Select Transaction Type**',('Recharge & bill payments','Peer-to-peer payments',
            'Merchant payments','Financial Services','Others','All'),key='tr_type',index=5)


    #============== / OUTPUT / ==============#
    try:
        col4,col5 = st.columns(2)

        # -------------------------       /     All India Transaction        /        ------------------ #
        if tr_state == 'All':
            
            with col4:
                #Query part
                query_t1_a=(f"SELECT SUM(transaction_count) AS All_PhonePe_Transactions, \
                        ROUND(SUM(transaction_amount)) AS Total_Transaction_Amount, \
                        round(avg((transaction_amount)/(transaction_count)),2) AS Avg_Transaction_Value \
                        FROM aggregated_transaction WHERE year='{tr_yr}' AND quater = '{tr_qtr}';")
                df_t1_a = pd.read_sql(query_t1_a, engine)
                df_t1_a = df_t1_a.map(int)
                df_t1_a = df_t1_a.map(format_int_with_commas)


                #Values
                value_1 = str(df_t1_a['All_PhonePe_Transactions'][0])
                st.metric(label=":violet[**All PhonePe Transactions**]", value=value_1)
                value_2 = "Rs."+str(df_t1_a['Total_Transaction_Amount'][0])
                st.metric(label=":violet[**Total Transaction Amount**]", value=value_2)
                value_3 = "Rs."+str(df_t1_a['Avg_Transaction_Value'][0])
                st.metric(label=":violet[**Avg. Transaction Value**]", value=value_3)

                #Table
                st.markdown(':violet[**Transactions by Category**]')
                query_t2_a= f"SELECT Transaction_type AS Categories, SUM(Transaction_count) AS Transactions \
                    FROM aggregated_transaction WHERE year='{tr_yr}' AND quater = '{tr_qtr}' GROUP BY Transaction_type \
                          ORDER BY Transaction_type;"
                df_t2_a = pd.read_sql(query_t2_a, engine)
                df_t2_a.index += 1
                if tr_type == 'Recharge & bill payments':
                    st.dataframe(df_t2_a.loc[[5]], hide_index=True)
                elif tr_type == 'Peer-to-peer payments':
                    st.dataframe(df_t2_a.loc[[4]], hide_index=True)
                elif tr_type == 'Merchant payments':
                    st.dataframe(df_t2_a.loc[[2]], hide_index=True)
                elif tr_type == 'Financial Services':
                    st.dataframe(df_t2_a.loc[[1]], hide_index=True)
                elif tr_type == 'Others':
                    st.dataframe(df_t2_a.loc[[3]], hide_index=True)
                else:
                    st.dataframe(df_t2_a)     

            #Pie-chart for every type of transaction
            with col5:
                dict1 = df_t2_a.to_dict('list')
                list1 = list(dict1.values())
                if tr_type == 'Recharge & bill payments':
                    # pull is given as a fraction of the pie radius
                    fig = go.Figure(data=[go.Pie(labels=list1[0], values=list1[1], pull=[0, 0, 0, 0, 0.1], 
                        marker_colors=px.colors.sequential.RdBu)])
                    fig.update_traces(textposition='inside', textinfo='percent+label',
                        title_text='Transactions by Category',title_font={'size':20,'color':'black'})
                        # width=500, height=500)
                    st.plotly_chart(fig,use_container_width=True)

                elif tr_type == 'Peer-to-peer payments':
                    # pull is given as a fraction of the pie radius
                    fig = go.Figure(data=[go.Pie(labels=list1[0], values=list1[1], pull=[0, 0, 0, 0.1, 0], 
                        marker_colors=px.colors.sequential.RdBu)])
                    fig.update_traces(textposition='inside', textinfo='percent+label',
                        title_text='Transactions by Category',title_font={'size':20,'color':'black'})
                    st.plotly_chart(fig,use_container_width=True)

                elif tr_type == 'Merchant payments':
                    # pull is given as a fraction of the pie radius
                    fig = go.Figure(data=[go.Pie(labels=list1[0], values=list1[1], pull=[0, 0.1, 0, 0, 0], 
                        marker_colors=px.colors.sequential.RdBu)])
                    fig.update_traces(textposition='inside', textinfo='percent+label',
                        title_text='Transactions by Category',title_font={'size':20,'color':'black'})
                    st.plotly_chart(fig,use_container_width=True)

                elif tr_type == 'Financial Services':
                    # pull is given as a fraction of the pie radius
                    fig = go.Figure(data=[go.Pie(labels=list1[0], values=list1[1], pull=[0.2, 0, 0, 0, 0], 
                        marker_colors=px.colors.sequential.RdBu)])
                    fig.update_traces(textposition='inside', textinfo='percent+label',
                        title_text='Transactions by Category',title_font={'size':20,'color':'black'})
                    st.plotly_chart(fig,use_container_width=True)

                elif tr_type == 'Others':
                    # pull is given as a fraction of the pie radius
                    fig = go.Figure(data=[go.Pie(labels=list1[0], values=list1[1], pull=[0, 0, 0.2, 0, 0], 
                        marker_colors=px.colors.sequential.RdBu)])
                    fig.update_traces(textposition='inside', textinfo='percent+label',
                        title_text='Transactions by Category',title_font={'size':20,'color':'black'})
                    st.plotly_chart(fig,use_container_width=True)

                else:
                    fig = px.pie(df_t2_a, values='Transactions', names='Categories', title=f"Transactions by Category in {tr_yr} Quater {tr_qtr}", 
                                color_discrete_sequence=px.colors.sequential.RdBu, hover_data=['Transactions'], 
                                labels={'Categories':'Transaction Type'},width = 500, height = 500)
                    fig.update_traces(textposition='inside', textinfo='percent+label')
                    st.plotly_chart(fig)
            
            #bar chart with toggle button
            on_1 = st.toggle("Show plot",key='on_1')

            if on_1:
                query_t3_a=f"SELECT State, SUM(Transaction_count) AS Transaction_count FROM aggregated_transaction WHERE year='{tr_yr}' AND quater='{tr_qtr}' GROUP BY State ORDER BY State;"
                df_u4_a = pd.read_sql(query_t3_a, engine)
                fig = px.bar(df_u4_a , x = 'State', y ='Transaction_count', color ='Transaction_count', 
                        color_continuous_scale = 'thermal', title = 'Transaction count Analysis Chart for INDIA', width = 900, height = 600, text='Transaction_count')
                fig.update_traces(textposition='outside')
                st.plotly_chart(fig)
                    
        # -------------------------       /     State wise Transaction        /        ------------------ #
        else:
            
            with col4:
            #query part
                query_t1_b=(f"SELECT SUM(transaction_count) AS All_PhonePe_Transactions, \
                        ROUND(SUM(transaction_amount)) AS Total_Transaction_Amount, \
                        ROUND(AVG((transaction_amount)/(transaction_count)),2) AS Avg_Transaction_Value \
                        FROM aggregated_transaction WHERE year='{tr_yr}' AND quater = '{tr_qtr}' AND State='{tr_state}';")
                df_t1_b = pd.read_sql(query_t1_b, engine)
                df_t1_b = df_t1_b.map(int)
                df_t1_b = df_t1_b.map(format_int_with_commas)

                #values
                value_1 = str(df_t1_b['All_PhonePe_Transactions'][0])
                st.metric(label=":violet[**All PhonePe Transactions**]", value=value_1)
                value_2 = "Rs."+str(df_t1_b['Total_Transaction_Amount'][0])
                st.metric(label=":violet[**Total Transaction Amount**]", value=value_2)
                value_3 = "Rs."+str(df_t1_b['Avg_Transaction_Value'][0])
                st.metric(label=":violet[**Avg. Transaction Value**]", value=value_3)

                #table
                st.markdown(':violet[**Transactions by Category**]')
                query_t2_b= f"SELECT Transaction_type AS Categories, SUM(Transaction_count) AS Transactions \
                    FROM aggregated_transaction WHERE year='{tr_yr}' AND quater = '{tr_qtr}' AND State='{tr_state}' GROUP BY Transaction_type \
                        ORDER BY Transaction_type;"
                df_t2_b = pd.read_sql(query_t2_b, engine)
                df_t2_b.index += 1
                if tr_type == 'Recharge & bill payments':
                    st.dataframe(df_t2_b.loc[[5]],hide_index=True)
                elif tr_type == 'Peer-to-peer payments':
                    st.dataframe(df_t2_b.loc[[4]], hide_index=True)
                elif tr_type == 'Merchant payments':
                    st.dataframe(df_t2_b.loc[[2]], hide_index=True)
                elif tr_type == 'Financial Services':
                    st.dataframe(df_t2_b.loc[[1]], hide_index=True)
                elif tr_type == 'Others':
                    st.dataframe(df_t2_b.loc[[3]], hide_index=True)
                else:
                    st.dataframe(df_t2_b)

            
            #pie-chart
            with col5:
                dict2 = df_t2_b.to_dict('list')
                list1 = list(dict2.values())
                if tr_type == 'Recharge & bill payments':
                    # pull is given as a fraction of the pie radius
                    fig = go.Figure(data=[go.Pie(labels=list1[0], values=list1[1], pull=[0, 0, 0, 0, 0.1], 
                        marker_colors=px.colors.sequential.RdBu)])
                    fig.update_traces(textposition='inside', textinfo='percent+label',
                        title_text=f"Transactions by Category for {tr_state}",title_font={'size':20,'color':'black'})
                    st.plotly_chart(fig,use_container_width=True)

                elif tr_type == 'Peer-to-peer payments':
                    # pull is given as a fraction of the pie radius
                    fig = go.Figure(data=[go.Pie(labels=list1[0], values=list1[1], pull=[0, 0, 0, 0.1, 0], 
                        marker_colors=px.colors.sequential.RdBu)])
                    fig.update_traces(textposition='inside', textinfo='percent+label',
                        title_text=f"Transactions by Category for {tr_state}",title_font={'size':20,'color':'black'})
                    st.plotly_chart(fig,use_container_width=True)

                elif tr_type == 'Merchant payments':
                    # pull is given as a fraction of the pie radius
                    fig = go.Figure(data=[go.Pie(labels=list1[0], values=list1[1], pull=[0, 0.1, 0, 0, 0], 
                        marker_colors=px.colors.sequential.RdBu)])
                    fig.update_traces(textposition='inside', textinfo='percent+label',
                        title_text=f"Transactions by Category for {tr_state}",title_font={'size':20,'color':'black'})
                    st.plotly_chart(fig,use_container_width=True)

                elif tr_type == 'Financial Services':
                    # pull is given as a fraction of the pie radius
                    fig = go.Figure(data=[go.Pie(labels=list1[0], values=list1[1], pull=[0.2, 0, 0, 0, 0], 
                        marker_colors=px.colors.sequential.RdBu)])
                    fig.update_traces(textposition='inside', textinfo='percent+label',
                        title_text=f"Transactions by Category for {tr_state}",title_font={'size':20,'color':'black'})
                    st.plotly_chart(fig,use_container_width=True)

                elif tr_type == 'Others':
                    # pull is given as a fraction of the pie radius
                    fig = go.Figure(data=[go.Pie(labels=list1[0], values=list1[1], pull=[0, 0, 0.2, 0, 0], 
                        marker_colors=px.colors.sequential.RdBu)])
                    fig.update_traces(textposition='inside', textinfo='percent+label',
                        title_text=f"Transactions by Category for {tr_state}",title_font={'size':20,'color':'black'})
                    st.plotly_chart(fig,use_container_width=True)

                else:
                    fig = px.pie(df_t2_b, values='Transactions', names='Categories', title=f"Transactions by Category for {tr_state}", 
                                color_discrete_sequence=px.colors.sequential.RdBu, hover_data=['Transactions'], 
                                labels={'Categories':'Transaction Type'},width = 500, height = 500)
                    fig.update_traces(textposition='inside', textinfo='percent+label')
                    st.plotly_chart(fig)    
        
            #bar chart with toggle button
            on_2 = st.toggle("Show plot",key='on_2')

            if on_2:
                query_t3_b=f"SELECT District_name, SUM(Transaction_count) AS Transaction_count FROM map_transaction WHERE year='{tr_yr}' AND quater='{tr_qtr}' AND State = '{tr_state}' GROUP BY District_name ORDER BY District_name;"
                df_u4_a = pd.read_sql(query_t3_b, engine)
                fig = px.bar(df_u4_a , x = 'District_name', y ='Transaction_count', color ='Transaction_count', 
                        color_continuous_scale = 'thermal', title = f"Transaction count Analysis Chart for {tr_state}", height = 600, text='Transaction_count')
                fig.update_traces(textposition='outside')
                st.plotly_chart(fig,use_container_width=True)

        #=========================================== /   GEO VISUALISATION   / ===================================#

        query_m1=(f"SELECT SUM(transaction_amount) AS Total_payment_value, \
                    SUM(transaction_count) AS All_Transactions, \
                    ROUND(AVG(transaction_amount/transaction_count),2) AS Avg_transaction_value \
                    FROM map_transaction WHERE year='{tr_yr}' AND quater = '{tr_qtr}' GROUP BY state;")
        
        df_m1 = pd.read_sql(query_m1,engine)
        
        # Clone the geo data
        url = "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
        response = requests.get(url)
        data = json.loads(response.content)

        # Extract state names and sort them in alphabetical order
        state_names = [i['properties']['ST_NM'] for i in data['features']]
        state_names.sort()

        # Create a DataFrame with the state names column
        df_states= pd.DataFrame({'State': state_names})
        df_m2 = pd.concat([df_states,df_m1],axis=1)
        
        # Geo plot
        fig_tra = px.choropleth(
            df_m2,
            geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
            featureidkey='properties.ST_NM',locations='State',color='Total_payment_value', hover_name='State', hover_data=['All_Transactions','Avg_transaction_value'], 
            color_continuous_scale='Viridis', title = f"State wise Transaction Analysis for {tr_yr} and Quater {tr_qtr}", projection='orthographic', labels={'Total_payment_value':'Transaction amount','All_Transactions':'Transaction count','Avg_transaction_value':'Avg Transaction value'})
        fig_tra.update_geos(fitbounds="locations", visible=False)
        fig_tra.update_layout(title_font={'size':30},title_font_color='#6739b7', height=700)
        st.plotly_chart(fig_tra,use_container_width=True)

    except:
        #if user select quater 2,3,4 of 2024
        st.error('**Select a different Quater**')


# ===================================================       /      USER TAB    /     ===================================================== #

with tab2:

    #Select boxes
    st.markdown('This tab has User data of whole of India and every state.')
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
    
    col3,col4 = st.columns(2)

    # -------------------------       /     All India Users        /        ------------------ #
    if u_state == 'All':
        with col3:

            #query and values
            query_u1_a=f"SELECT SUM(Registered_users) AS Registered_users FROM map_user WHERE year='{u_yr}' AND quater ='{u_qtr}';"
            df_u1_a = pd.read_sql(query_u1_a, engine)
            df_u1_a = df_u1_a.map(int)
            df_u1_a = df_u1_a.map(format_int_with_commas)
            value_4 = df_u1_a['Registered_users'][0]
            label=f":violet[**Registered PhonePe users in {u_yr} Quater {u_qtr}**]"
            st.metric(label=label, value=value_4)

            query_u2_a=f"SELECT SUM(App_opens_count) AS PhonePe_App_opens FROM map_user WHERE year='{u_yr}' AND quater ='{u_qtr}';"
            df_u2_a = pd.read_sql(query_u2_a, engine)
            df_u2_a = df_u2_a.map(int)
            df_u2_a = df_u2_a.map(format_int_with_commas)
            value_5 = df_u2_a['PhonePe_App_opens'][0]
            label=f":violet[**PhonePe App opens in {u_yr} Quater {u_qtr}**]"
            st.metric(label=label, value=value_5)
        
        
            #table
            st.markdown(':violet[**Mobile Brand vs Registered Users**]')
            query_u3_a=f"SELECT Mobile_brand, sum(User_count) AS Registered_users FROM aggregated_user WHERE year='{u_yr}' AND quater ='{u_qtr}' GROUP BY Mobile_brand;"
            df_u2_a = pd.read_sql(query_u3_a, engine)
            df_u2_a.index += 1
            st.dataframe(df_u2_a)


        with col4:

            #bar chart
            query_u4_a=f"SELECT State, SUM(Registered_Users) AS Registered_Users FROM map_user WHERE year='{u_yr}' AND quater='{u_qtr}' GROUP BY State ORDER BY State;"
            df_u4_a = pd.read_sql(query_u4_a, engine)
            fig = px.bar(df_u4_a , x = 'State', y ='Registered_Users', color ='Registered_Users', 
                    color_continuous_scale = 'thermal', title = 'Top User Analysis Chart', height = 600, text='Registered_Users')
            fig.update_traces(textposition='outside')
            st.plotly_chart(fig)


    # -------------------------       /     State wise Users        /        ------------------ #
    else:

        with col3:

            #query and values
            query_u1_b=f"SELECT SUM(Registered_users) AS Registered_users FROM map_user \
                WHERE year='{u_yr}' AND quater ='{u_qtr}' AND state = '{u_state}';"
            df_u1_b = pd.read_sql(query_u1_b, engine)
            df_u1_b = df_u1_b.map(int)
            df_u1_b = df_u1_b.map(format_int_with_commas)
            value_4 = df_u1_b['Registered_users'][0]
            label=f":violet[**Registered PhonePe users in {u_yr} Quater {u_qtr}**]"
            st.metric(label=label, value=value_4)

            query_u2_b=f"SELECT SUM(App_opens_count) AS PhonePe_App_opens FROM map_user \
                WHERE year='{u_yr}' AND quater ='{u_qtr}' AND state = '{u_state}';"
            df_u2_b = pd.read_sql(query_u2_b, engine)
            df_u2_b = df_u2_b.map(format_int_with_commas)
            value_5 = df_u2_b['PhonePe_App_opens'][0]
            label=f":violet[**PhonePe App opens in {u_yr} Quater {u_qtr}**]"
            st.metric(label=label, value=value_5)
        
        
            #table
            st.markdown(':violet[**Mobile Brand vs Registered Users**]')
            query_u3_b=f"SELECT Mobile_brand, sum(User_count) AS Registered_users FROM aggregated_user \
                WHERE year='{u_yr}' AND quater ='{u_qtr}' AND state='{u_state}' GROUP BY Mobile_brand;"
            df_u3_b = pd.read_sql(query_u3_b, engine)
            df_u3_b.index += 1
            st.dataframe(df_u3_b)

        with col4:

            #bar chart
            query_u4_b=f"SELECT District_name, sum(Registered_users) AS Registered_users FROM map_user \
                WHERE year='{u_yr}' AND quater ='{u_qtr}' AND state = '{u_state}' GROUP BY District_name ORDER BY District_name;"
            df_u4_b = pd.read_sql(query_u4_b, engine)
            fig = px.bar(df_u4_b, x = 'District_name', y ='Registered_users', color ='Registered_users', 
                    color_continuous_scale = 'thermal', title = 'Top User Analysis Chart', text='Registered_users')
            fig.update_traces(textposition='outside')
            st.plotly_chart(fig)


    #=========================================== /   GEO VISUALISATION   / ===================================#

    query_m2=(f"SELECT SUM(Registered_users) AS Registered_users, \
            SUM(App_opens_count) AS PhonePe_App_opens FROM map_user \
            WHERE year='{u_yr}' AND quater ='{u_qtr}' GROUP BY state;")
    
    df_m3 = pd.read_sql(query_m2,engine)

    # Clone the geo data
    url = "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
    response = requests.get(url)
    data = json.loads(response.content)

    # Extract state names and sort them in alphabetical order
    state_names = [i['properties']['ST_NM'] for i in data['features']]
    state_names.sort()

    # Create a DataFrame with the state names column
    df_states= pd.DataFrame({'State': state_names})
    df_m4 = pd.concat([df_states,df_m3],axis=1)
    
    # Geo plot
    fig_tra = px.choropleth(
        df_m4,
        geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
        featureidkey='properties.ST_NM',locations='State',color='Registered_users', hover_name='State', hover_data='PhonePe_App_opens', 
        color_continuous_scale='Viridis', title = f"State wise Registerd Users Analysis for {u_yr} and Quater {u_qtr}", projection='orthographic', labels={'Registered_users':'Registered users', 'PhonePe_App_opens':'PhonePe App Opens'})
    fig_tra.update_geos(fitbounds="locations", visible=False)
    fig_tra.update_layout(title_font={'size':30}, title_font_color='#6739b7', height=700)
    st.plotly_chart(fig_tra,use_container_width=True)
    
    
