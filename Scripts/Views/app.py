import streamlit as st
from Scripts.Views.info import informazioni_utente
from Scripts.Views.lavori import lavori
from Scripts.Views.assenze import assenze
from Scripts.Views.dashboard import user_dashboard
from Scripts.Views.settings import CONTROLLER
from Scripts.Views.commesse import commesse
from Scripts.Views.risorse import risorse
from Scripts.Views.d_commesse import d_commesse
from Scripts.Views.d_risorse import d_risorse
from Scripts.Views.dati_risorse import dati_risorse

def app():    
    risorsa=CONTROLLER.get('risorsa')
    CONTROLLER.set('risorsa',risorsa,max_age=9*60*60)

    info=st.Page(informazioni_utente,title='Info',icon=':material/info:')

    if risorsa['ruolo']=='risorsa':
        inserisci_ore=st.Page(lavori,title='Lavori',icon=':material/work:')
        ferie=st.Page(assenze,title='Assenze',icon=':material/free_cancellation:')
        u_dash=st.Page(user_dashboard,title='Dashboard',icon=':material/dashboard:')

        with st.sidebar:
            logout=st.button('Logout',use_container_width=True)
            if logout:
                CONTROLLER.remove('risorsa')
                st.rerun()

        pg = st.navigation({"Inserisci":[inserisci_ore,ferie],"Informazioni":[u_dash,info]})
        pg.run()
    
    elif risorsa['ruolo']=='admin':
        gestione_commesse=st.Page(commesse,title='Commesse',icon=':material/work:')
        gestione_risorse=st.Page(risorse,title='Risorse',icon=':material/person:')

        dashboard_commesse=st.Page(d_commesse,title='Dashboard Commesse',icon=':material/monitoring:')
        dashboard_risorse=st.Page(d_risorse,title='Dashboard Risorse',icon=':material/monitoring:')
        estrazione_dati_risorse=st.Page(dati_risorse,title='Ricerca personalizzata',icon=':material/database:')

        with st.sidebar:
            logout=st.button('Logout',use_container_width=True)
            if logout:
                CONTROLLER.remove('risorsa')
                st.rerun()
        
        pg = st.navigation({"Gestione":[gestione_commesse,gestione_risorse],"Dashboard":[dashboard_commesse,dashboard_risorse,estrazione_dati_risorse],"Informazioni":[info]})
        pg.run()


    
    
    