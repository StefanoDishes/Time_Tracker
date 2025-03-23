import streamlit as st

st.set_page_config(page_title="Anafyo Time Tracker",layout='wide')

from Scripts.Views.settings import CONTROLLER
from Scripts.Views.app import app
from Scripts.Views.login import login

risorsa=CONTROLLER.get('risorsa')

if CONTROLLER.get('risorsa'):
    app()
else:
    login()