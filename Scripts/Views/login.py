import streamlit as st
from Scripts.Connector import getSession
from Scripts.DTO import RisorsaDTOInsert
from Scripts.Queries import loginRisorsa,insertRisorsa,updatePasswordRisorsa
from streamlit_cookies_controller import CookieController
from Scripts.Views.settings import CONTROLLER

@st.dialog('Registrazione')
def registrazione_utente():
    nome_utente=st.text_input("Nome")
    cognome_utente=st.text_input("Cognome")
    email_utente=st.text_input("Email")
    password_utente=st.text_input("Password",type="password")
    password_utente_ver=st.text_input("Ripeti password",type="password")
    registrazione=st.button('Salva',type='primary',icon=':material/save:')

    if registrazione:
        if password_utente==password_utente_ver:
            with getSession() as session:
                risorsa=insertRisorsa(RisorsaDTOInsert(nome_utente=nome_utente,cognome_utente=cognome_utente,email_utente=email_utente,password_utente=password_utente),session)
            if risorsa:
                st.success("Iscrizione completata puoi effettuare il login", icon="✅")
            else:
                st.error("Utente già iscritto",icon="⚠️")
        else:
            st.error("La password non corrisponde",icon="⚠️")

@st.dialog('Recupero password')
def recupera_password():
    nome_utente=st.text_input("Nome")
    cognome_utente=st.text_input("Cognome")
    email_utente=st.text_input("Email")
    nuova_password=st.text_input("Nuova password",type="password")
    recupera=st.button('Recupera',type='primary',icon=':material/save:')
    
    if recupera:
        with getSession() as session:
            risorsa=updatePasswordRisorsa(RisorsaDTOInsert(email_utente=email_utente,nome_utente=nome_utente,cognome_utente=cognome_utente,password_utente=nuova_password),session)
        if risorsa:
            st.success("Password modificata con successo",icon="✅")
        else:
            st.error("Utente non trovato",icon="⚠️")


def login():
    col1,col2,col3=st.columns(spec=(0.3,0.4,0.3),gap='small')

    with col2:
        coll1,coll2,coll3=st.columns(spec=(.4,.6,.2),gap='small')
        with coll2:
            st.title("Anafyo")
        with st.form("login",enter_to_submit=False):
            email=st.text_input('📧 Email utente')
            password=st.text_input("🔑 Password",type='password')
            colll1,colll2,colll3=st.columns(spec=(3),gap='small')
            with colll1:
                accesso=st.form_submit_button("Accedi",use_container_width=True,type='primary')
            st.write('Non ancora iscritto?')
            registrazione=st.form_submit_button("Registrati",use_container_width=True)
            st.write('Hai dimenticato la password?')
            password_dimenticata=st.form_submit_button("Password dimenticata",use_container_width=True)
            
        if accesso:
            if(email=="" or password==""):
                st.warning("Per effettuare l'accesso inserisci email e password",icon="⚠️")
            else:
                with getSession() as session:
                    risorsa = loginRisorsa(email,password,session)
                if not risorsa:
                    st.error("⛔ Email o Password sbagliate")
                else:
                    if(risorsa.stato_utente==0):
                        st.error("⛔ L'utente non è attivo rivolgersi agli amministratori")
                    else:
                        CONTROLLER.set('risorsa',{'id':risorsa.id,'ruolo':risorsa.tipo_utente},max_age=9*60*60)
                        st.rerun()
        
        if registrazione:
            registrazione_utente()

        if password_dimenticata:
            recupera_password()
