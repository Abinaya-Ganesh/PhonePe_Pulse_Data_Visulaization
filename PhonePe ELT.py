#=================================== /   IMPORTING LIBRARIES /   ==================================#
#Git cloning Library
import git

#File handling Libraries
import os
import json

#Pandas Library
import pandas as pd

#Numpy Library
import numpy as np

#MySQL and SQLAlchemy Libraries
from mysql.connector import connect
from urllib.parse import quote
from sqlalchemy import create_engine
import sqlalchemy



#========================================= /   GIT CLONING   / =====================================#

repo_url="https://github.com/PhonePe/pulse.git"
destination_directory="C:/Phonepe Pulse data"
git.Repo.clone_from(repo_url,destination_directory)



#================================ /   COLLECTING DATA AND CREATING DATAFRAMES   / ================================#

#1
#Aggregated_Transaction_data

data_agg_transaction = { 'State':[], 'Year':[], 'Quater':[], 'Transaction_type':[], 'Transaction_count':[], 'Transaction_amount':[]}


path_1=r"C:\Phonepe Pulse data\data\aggregated\transaction\country\india\state"

Agg_state_list = os.listdir(path_1)

for i in Agg_state_list:
    p_i = path_1+"\\"+i
    Agg_year_list = os.listdir(p_i)
    for j in Agg_year_list:
        p_j = p_i+"\\"+j
        Agg_quater_list = os.listdir(p_j)
        for k in Agg_quater_list:
            p_k = p_j+"\\"+k
            data = open(p_k,'r')
            D = json.load(data)
            for z in D['data']['transactionData']:
                name=z['name']
                count=z['paymentInstruments'][0]['count']
                amount=z['paymentInstruments'][0]['amount']
                data_agg_transaction['State'].append(i)
                data_agg_transaction['Year'].append(j)
                data_agg_transaction['Quater'].append(int(k.strip('.json')))
                data_agg_transaction['Transaction_type'].append(name)
                data_agg_transaction['Transaction_count'].append(count)
                data_agg_transaction['Transaction_amount'].append(amount)

df_agg_transaction = pd.DataFrame(data_agg_transaction)


#2
#Aggregated_User_data

data_agg_user = { 'State':[], 'Year':[], 'Quater':[], 'Mobile_brand':[], 'User_count':[], 'User_Percentage':[]}

path_2=r"C:\Phonepe Pulse data\data\aggregated\user\country\india\state"

Agg_state_list = os.listdir(path_2)

for i in Agg_state_list:
    p_i = path_2+"\\"+i
    Agg_year_list = os.listdir(p_i)
    for j in Agg_year_list:
        p_j = p_i+"\\"+j
        Agg_quater_list = os.listdir(p_j)
        for k in Agg_quater_list:
            p_k = p_j+"\\"+k
            data = open(p_k,'r')
            D = json.load(data)
            try:
                for z in D['data']['usersByDevice']:
                    brand=z['brand']
                    count=z['count']
                    percentage=z['percentage']
                    data_agg_user['State'].append(i)
                    data_agg_user['Year'].append(j)
                    data_agg_user['Quater'].append(int(k.strip('.json')))
                    data_agg_user['Mobile_brand'].append(brand)
                    data_agg_user['User_count'].append(count)
                    data_agg_user['User_Percentage'].append(percentage)
            except:
                brand=None
                count=np.nan
                percentage=np.nan
                data_agg_user['State'].append(i)
                data_agg_user['Year'].append(j)
                data_agg_user['Quater'].append(int(k.strip('.json')))
                data_agg_user['Mobile_brand'].append(brand)
                data_agg_user['User_count'].append(count)
                data_agg_user['User_Percentage'].append(percentage)

df_agg_user = pd.DataFrame(data_agg_user)

#Data cleaning
df_agg_user.dropna(ignore_index=True, inplace=True)


#3
#Map_Transaction_District_data

data_map_transaction_dt = { 'State':[], 'Year':[], 'Quater':[], 'District_name':[], 'Transaction_count':[], 'Transaction_amount':[]}

path_3=r"C:\Phonepe Pulse data\data\map\transaction\hover\country\india\state"

Map_state_list = os.listdir(path_3)

for i in Map_state_list:
    p_i = path_3+"\\"+i
    Map_year_list = os.listdir(p_i)
    for j in Map_year_list:
        p_j = p_i+"\\"+j
        Map_quater_list = os.listdir(p_j)
        for k in Map_quater_list:
            p_k = p_j+"\\"+k
            data = open(p_k,'r')
            D = json.load(data)
            for z in D['data']['hoverDataList']:
                name=z['name']
                count=z['metric'][0]['count']
                amount=z['metric'][0]['amount']
                data_map_transaction_dt['State'].append(i)
                data_map_transaction_dt['Year'].append(j)
                data_map_transaction_dt['Quater'].append(int(k.strip('.json')))
                data_map_transaction_dt['District_name'].append(name)
                data_map_transaction_dt['Transaction_count'].append(count)
                data_map_transaction_dt['Transaction_amount'].append(amount)

df_map_transaction = pd.DataFrame(data_map_transaction_dt)


#4
#Map_User_District_data

data_map_user_dt = { 'State':[], 'Year':[], 'Quater':[], 'District_name':[], 'Registered_users':[], 'App_opens_count':[]}

path_4=r"C:\Phonepe Pulse data\data\map\user\hover\country\india\state"

Map_state_list = os.listdir(path_4)

for i in Map_state_list:
    p_i = path_4+"\\"+i
    Map_year_list = os.listdir(p_i)
    for j in Map_year_list:
        p_j = p_i+"\\"+j
        Map_quater_list = os.listdir(p_j)
        for k in Map_quater_list:
            p_k = p_j+"\\"+k
            data = open(p_k,'r')
            D = json.load(data)
            for y,z in D['data']['hoverData'].items():
                name=y
                registerd_users=z['registeredUsers']
                app_opens=z['appOpens']
                data_map_user_dt['State'].append(i)
                data_map_user_dt['Year'].append(j)
                data_map_user_dt['Quater'].append(int(k.strip('.json')))
                data_map_user_dt['District_name'].append(name)
                data_map_user_dt['Registered_users'].append(registerd_users)
                data_map_user_dt['App_opens_count'].append(app_opens)

df_map_user = pd.DataFrame(data_map_user_dt)


#5
#Top_Transaction_District_and_Pincode_data

data_top_transaction_dt = { 'State':[], 'Year':[], 'Quater':[], 'District_name':[], 'Transaction_count':[], 'Transaction_amount':[]}
data_top_transaction_pincode = { 'State':[], 'Year':[], 'Quater':[], 'District_pincode':[], 'Transaction_count':[], 'Transaction_amount':[]}

path_5=r"C:\Phonepe Pulse data\data\top\transaction\country\india\state"

Top_state_list = os.listdir(path_5)

for i in Top_state_list:
    p_i = path_5+"\\"+i
    Top_year_list = os.listdir(p_i)
    for j in Top_year_list:
        p_j = p_i+"\\"+j
        Top_quater_list = os.listdir(p_j)
        for k in Top_quater_list:
            p_k = p_j+"\\"+k
            data = open(p_k,'r')
            D = json.load(data)
            #districts
            for y in D['data']['districts']:
                name=y['entityName']
                count=y['metric']['count']
                amount=y['metric']['amount']
                data_top_transaction_dt['State'].append(i)
                data_top_transaction_dt['Year'].append(j)
                data_top_transaction_dt['Quater'].append(int(k.strip('.json')))
                data_top_transaction_dt['District_name'].append(name)
                data_top_transaction_dt['Transaction_count'].append(count)
                data_top_transaction_dt['Transaction_amount'].append(amount)
            #pincode
            for z in D['data']['pincodes']:
                name=z['entityName']
                count=z['metric']['count']
                amount=z['metric']['amount']
                data_top_transaction_pincode['State'].append(i)
                data_top_transaction_pincode['Year'].append(j)
                data_top_transaction_pincode['Quater'].append(int(k.strip('.json')))
                data_top_transaction_pincode['District_pincode'].append(name)
                data_top_transaction_pincode['Transaction_count'].append(count)
                data_top_transaction_pincode['Transaction_amount'].append(amount)

df_top_transaction_dt = pd.DataFrame(data_top_transaction_dt)
df_top_transaction_pincode = pd.DataFrame(data_top_transaction_pincode)


#6
#Map_User_District_and_Pincode_data

data_top_user_dt = { 'State':[], 'Year':[], 'Quater':[], 'District_name':[], 'Registered_users':[]}
data_top_user_pincode = { 'State':[], 'Year':[], 'Quater':[], 'District_pincode':[], 'Registered_users':[]}

path_6=r"C:\Phonepe Pulse data\data\top\user\country\india\state"

Top_state_list = os.listdir(path_6)

for i in Top_state_list:
    p_i = path_6+"\\"+i
    Top_year_list = os.listdir(p_i)
    for j in Top_year_list:
        p_j = p_i+"\\"+j
        Top_quater_list = os.listdir(p_j)
        for k in Top_quater_list:
            p_k = p_j+"\\"+k
            data = open(p_k,'r')
            D = json.load(data)
            #districts
            for y in D['data']['districts']:
                name=y['name']
                registerd_users=y['registeredUsers']
                data_top_user_dt['State'].append(i)
                data_top_user_dt['Year'].append(j)
                data_top_user_dt['Quater'].append(int(k.strip('.json')))
                data_top_user_dt['District_name'].append(name)
                data_top_user_dt['Registered_users'].append(registerd_users)
            #pincode
            for z in D['data']['pincodes']:
                name=z['name']
                registerd_users=z['registeredUsers']
                data_top_user_pincode['State'].append(i)
                data_top_user_pincode['Year'].append(j)
                data_top_user_pincode['Quater'].append(int(k.strip('.json')))
                data_top_user_pincode['District_pincode'].append(name)
                data_top_user_pincode['Registered_users'].append(registerd_users)

df_top_user_dt = pd.DataFrame(data_top_user_dt)
df_top_user_pincode = pd.DataFrame(data_top_user_pincode)


#======================================================= /   CONNECTING TO SQL   / ============================================#

#Configuring
db_config = {
    'host':'localhost',
    'user':'root',
    'password':'1234',
    'database':'phonepe_db'
    }
encoded_password = quote(db_config['password'])


#Connecting to MySQL Workbench
connection = connect(user=db_config['user'], password=encoded_password, host=db_config['host'])
cursor = connection.cursor(buffered=True)


#Creating and Using "youtube_db" database
cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_config['database']}")
cursor.execute(f"USE {db_config['database']}")


#Closing the cursor and database connection
cursor.close()
connection.close()


#Connection for SQLAlchemy
connection_url = f"mysql+mysqlconnector://{db_config['user']}:{encoded_password}@{db_config['host']}/{db_config['database']}"
engine=create_engine(connection_url)



#====================================== /   MIGRATING DATA TO MYSQL TABLES   / ===================================#

#1
df_agg_transaction.to_sql(name='aggregated_transaction', con=engine, if_exists = 'replace', index=False,   
    dtype={'State': sqlalchemy.types.VARCHAR(length=50), 
            'Year': sqlalchemy.types.Integer, 
            'Quater': sqlalchemy.types.Integer, 
            'Transaction_type': sqlalchemy.types.VARCHAR(length=50), 
            'Transaction_count': sqlalchemy.types.Integer,
            'Transaction_amount': sqlalchemy.types.FLOAT(precision=5, asdecimal=True)})
#2
df_agg_user.to_sql(name='aggregated_user', con=engine, if_exists = 'replace', index=False,
    dtype={'State': sqlalchemy.types.VARCHAR(length=50), 
            'Year': sqlalchemy.types.Integer, 
            'Quater': sqlalchemy.types.Integer,
            'Mobile_brand': sqlalchemy.types.VARCHAR(length=50), 
            'User_Count': sqlalchemy.types.Integer, 
            'User_Percentage': sqlalchemy.types.FLOAT(precision=5, asdecimal=True)})
#3                       
df_map_transaction.to_sql(name='map_transaction', con=engine, if_exists = 'replace', index=False,
    dtype={'State': sqlalchemy.types.VARCHAR(length=50), 
            'Year': sqlalchemy.types.Integer, 
            'Quater': sqlalchemy.types.Integer, 
            'District_name': sqlalchemy.types.VARCHAR(length=50), 
            'Transaction_count': sqlalchemy.types.Integer, 
            'Transaction_amount': sqlalchemy.types.FLOAT(precision=5, asdecimal=True)})
#4
df_map_user.to_sql(name='map_user', con=engine, if_exists = 'replace', index=False,
    dtype={'State': sqlalchemy.types.VARCHAR(length=50), 
            'Year': sqlalchemy.types.Integer, 
            'Quater': sqlalchemy.types.Integer, 
            'District_name': sqlalchemy.types.VARCHAR(length=50), 
            'Registered_users': sqlalchemy.types.Integer, 
            'App_opens_count': sqlalchemy.types.Integer})
#5                  
df_top_transaction_dt.to_sql(name='top_transaction_dt', con=engine, if_exists = 'replace', index=False,
    dtype={'State': sqlalchemy.types.VARCHAR(length=50), 
        'Year': sqlalchemy.types.Integer, 
        'Quater': sqlalchemy.types.Integer,   
        'District_name': sqlalchemy.types.VARCHAR(length=50),
        'Transaction_count': sqlalchemy.types.Integer, 
        'Transaction_amount': sqlalchemy.types.FLOAT(precision=5, asdecimal=True)})

#6
df_top_transaction_pincode.to_sql(name='top_transaction_pincode', con=engine, if_exists='replace', index=False,
    dtype={'State': sqlalchemy.types.VARCHAR(length=50), 
            'Year': sqlalchemy.types.Integer, 
            'Quater': sqlalchemy.types.Integer,   
            'District_pincode': sqlalchemy.types.VARCHAR(length=50),
            'Transaction_count': sqlalchemy.types.Integer, 
            'Transaction_amount': sqlalchemy.types.FLOAT(precision=5, asdecimal=True)})
#7
df_top_user_dt.to_sql(name='top_user_dt', con=engine, if_exists = 'replace', index=False,
    dtype={'State': sqlalchemy.types.VARCHAR(length=50), 
            'Year': sqlalchemy.types.Integer, 
            'Quater': sqlalchemy.types.Integer,                           
            'District_name': sqlalchemy.types.VARCHAR(length=50), 
            'Registered_User': sqlalchemy.types.Integer})

#8
df_top_user_pincode.to_sql(name='top_user_pincode', con=engine, if_exists = 'replace', index=False,
    dtype={'State': sqlalchemy.types.VARCHAR(length=50), 
            'Year': sqlalchemy.types.Integer, 
            'Quater': sqlalchemy.types.Integer,                           
            'District_pincode': sqlalchemy.types.VARCHAR(length=50), 
            'Registered_User': sqlalchemy.types.Integer})
