import streamlit as st
from streamlit_cookies_controller import CookieController
from Scripts.Views.settings import CONTROLLER
from Scripts.Connector import getSession
from Scripts.Queries import updateRisorsa,resetPassword,findRisorsaById
import time

@st.dialog('Modifica utente')
def modifica_utente(risorsa,nome,cognome):
    nome_utente=st.text_input("Nome",value=nome,key='modifica_nome')
    cognome_utente=st.text_input("Cognome",value=cognome,key='modifica_cognome')
    modifica_utente=st.button('Salva',type='primary',icon=':material/save:')

    if modifica_utente:
        with getSession() as session:
            risorsa=updateRisorsa(risorsa['id'],nome_utente,cognome_utente,session)
        if risorsa:
            st.success("Modifica completata", icon="✅")
            time.sleep(1)
            st.rerun()

@st.dialog('Reset password')
def recupera_password(risorsa_cookie):
    nuova_password=st.text_input("Nuova password",type="password")
    recupera=st.button('Salva',type='primary',icon=':material/save:')
    
    if recupera:
        with getSession() as session:
            risorsa=resetPassword(risorsa_cookie['id'],nuova_password,session)
        if risorsa:
            st.success("Password modificata con successo",icon="✅")

def informazioni_utente():
    risorsa_cookie = CONTROLLER.get('risorsa')
    
    st.title("Informazioni utente")

    with getSession() as session:
        risorsa_dto=findRisorsaById(risorsa_cookie['id'],session)
    with st.container(border=True):
        nome=st.text_input('Nome',value=risorsa_dto.nome_utente,disabled=True)
        cognome=st.text_input('Cognome',value=risorsa_dto.cognome_utente,disabled=True)
        email=st.text_input('Email',value=risorsa_dto.email_utente,disabled=True)
        ruolo=st.text_input('Ruolo',value=risorsa_dto.tipo_utente,disabled=True)

    col1,col2,col3=st.columns((1,1,5))
    with col1:
        modifica=st.button('Modifica')
    with col2:
        reset_password=st.button('Reset password')
    
    if modifica:
        modifica_utente(risorsa_cookie,risorsa_dto.nome_utente,risorsa_dto.cognome_utente)

    if reset_password:
        recupera_password(risorsa_cookie)

    


    

