# PhonePe_Pulse_Data_Visulaization
User can clone PhonePe Pulse from Github repository, extract required data, convert them to useable formats, store the data in SQL and visualize using Streamlit

**Introduction**

PhonePe is an Indian UPI App and a lot of transactions happen every day via it. There are huge number of users who are using the app.
Thus, the app collects relevant and necessary data and stores them as json files in PhonePe Pulse Github repository.

The repository is public and we can use the data to analyse and visualize.

**User Guide**
1. **All India Page**
     This page has two tabs Transaction and User. In the transaction tab, multiple dropdowns are give for year, qauter, state and transaction type. By selecting the required options, users can get various values, tables and charts displayed for the data selected.

    The User tab has similar dropdowns which are year, quater and state. Selecting different options, users can get various values, tables and charts displayed for the data selected.
   
2. **Top 10 Page**
    This page has two tabs Transaction and User. In the transaction tab, multiple dropdowns are give for year, qauter and state. By selecting the required options, top 10 states, districts and pincodes with their respective transaction counts are displayed as tables.

   In the user tab, multiple dropdowns are give for year, qauter and state. By selecting the required options, top 10 states, districts and pincodes with their respective registered users count are displayed as tables.

3. **User Analysis Page**
    This page has a dropdown box with 10 questions given. User can select a question and the relevant data is displayed as charts.


**Developer Guide**

1. **Tools required**
         
      •	 Python
   
      •	 Visual Studio Code
    
      •	 MySQL workbench
   
      •	 Github repository link


2. **Python libraries to install**
     
      •	pandas
   
      •	mysql-connector-python
   
      •	SQLAlchemy
   
      •	streamlit

      •	plotly-express

      •	numpy


3. **Modules to import**
   
      a. Github cloning Libraries
   
          •	import requests

          •	import subprocess

      b. File handling Libraries
   
          •	import os

          •	import json

      c. Pandas Library
   
          •	import pandas as pd

      d. MySQL and SQLAlchemy Libraries
   
          •	from mysql.connector import connect
   
          •	from urllib.parse import quote
   
          •	from sqlalchemy import create_engine
   
          •	import sqlalchemy

      e. UI Dashboard Libraries
   
          •	import streamlit as st

          • import plotly.graph_objects as go
   
          •	import plotly.express as px

       f. Numpy Library

           • import numpy as np

4. **Process**

        • Github clone PhonePe Pulse data and store it in your system

        • Extract the required data from the json files available

        • Create different dataframes for the extracted data

        • Migrate the data to MySQL and store them permanently

        • Create a streamlit dashboard and dynamically update the data by querting using SQLAlchemy

        • Use data visualization tools to display data on Streamlit

**NOTE:**

	      I have created a multipage Streamlit app. Except the 1_🏴All India.py, other files should be in a folder named 
 	"pages" under the directory where 1_🏴All India.py is saved.
