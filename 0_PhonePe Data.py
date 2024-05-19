#UI Dashboard Libraries
import streamlit as st


#Streamlit page setup
st.set_page_config(
    page_title="Phonepe Pulse Data",
    page_icon="📊",
    layout="wide")


#Setting up background colour
page_bg_img = f"""
<style>
[data-testid="stAppViewContainer"] > .main {{
background: linear-gradient(#c1ade0,#f7f7f7);
ckground-attachment: local;
}}
[data-testid="stHeader"] {{
background: rgba(0,0,0,0);
}}
</style>
"""

st.markdown(page_bg_img, unsafe_allow_html=True)

#Title
st.title(':violet[Phonepe Pulse Data Visualization]')
st.markdown('**Note**: Data available is from **2018** to **2024 Quater 1** for **INDIA**')

st.markdown('**Click on any of the tabs from the side menu!**')