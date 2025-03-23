import streamlit as st
from Scripts.Views.settings import CONTROLLER
from Scripts.Connector import ENGINE
from Scripts.Connector import getSession
from Scripts.DTO import RisorsaDTOInsert
from Scripts.Queries import findAllRisorseAdmin,insertRisorsa,updateRisorsaAdmin,deleteRisorsaById
from datetime import datetime,timedelta
import time


def reset():
     st.session_state['key']+=1

def updateDataEditor(data,df,risorsa,session):
    stato={
        'attiva':1,
        'disattiva':0
    }

    for row_id,changes in data['edited_rows'].items():
        #print(f"ID Riga: {row_id}, Modifiche: {changes}")
        row_id_convertito=int(row_id)
        id_update=df[row_id_convertito]['Id']
        nome_convertito=changes.get('Nome',df[row_id_convertito]['Nome'])
        cognome_convertito=changes.get('Cognome',df[row_id_convertito]['Cognome'])
        email_convertito=changes.get('Email',df[row_id_convertito]['Email'])
        tipo_convertito=changes.get('Tipo',df[row_id_convertito]['Tipo'])
        stato_convertito=stato[changes.get('Stato',df[row_id_convertito]['Stato'])]
        
        with getSession() as session:
            updateRisorsaAdmin(id_update,nome_convertito,cognome_convertito,email_convertito,tipo_convertito,stato_convertito,session)        

    for new_row in data["added_rows"]:
        #print(f"Nuova Riga: {new_row}")
        nome_convertito=new_row.get('Nome')
        cognome_convertito=new_row.get('Cognome')
        email_convertito=new_row.get('Email')
        tipo_convertito=new_row.get('Tipo')
        stato_convertito=stato[new_row.get('Stato')]
        nuova_risorsa=RisorsaDTOInsert(nome_utente=nome_convertito,cognome_utente=cognome_convertito,email_utente=email_convertito,tipo_utente=tipo_convertito,stato_utente=stato_convertito,password_utente='1234')
        with getSession() as session:
            insertRisorsa(nuova_risorsa,session)

    for deleted_row_id in data["deleted_rows"]:
        id_delete=df[deleted_row_id]['Id']
        if id_delete==risorsa['id']:
            st.toast('Non è possibile eliminare la risorsa corrente',icon='⚠️')
            time.sleep(2)
            reset()
            st.rerun()

        with getSession() as session:
            try:
                deleteRisorsaById(id_delete,session)
            except:
                st.toast('Non è possibile eliminare la risorsa',icon='⚠️')
                time.sleep(2)
                reset()
                st.rerun()


def risorse():
    risorsa = CONTROLLER.get('risorsa')
    
    if 'key' not in st.session_state:
        st.session_state['key']=0

    with getSession() as session:
        df_commesse=findAllRisorseAdmin(session)
    
    
    if df_commesse is None:
        st.session_state[f'risorse_modificate_{st.session_state["key"]}']={}

    column_settings={
        'Id': None,
        'Nome':st.column_config.TextColumn('🪪 Nome',required=True,help="Nome utente",width='medium'),
        'Cognome':st.column_config.TextColumn('🪪 Cognome',required=True,help="Cognome utente",width='medium'),
        'Email':st.column_config.TextColumn('📧 Email',required=True,help="Email utente",width='medium'),
        'Tipo':st.column_config.SelectboxColumn('👤 Ruolo',options=['admin','risorsa'],required=True,help="Ruolo utente",width='small'),
        'Stato':st.column_config.SelectboxColumn('📖 Stato',options=['attiva','disattiva'],required=True,help="Stato utente",width='small')
    }
    
    st.title("Gestione risorse")
    with st.form('aggiungi_da_form',enter_to_submit=False,clear_on_submit=True):
            nome = st.text_input('🪪 Nome')
            cognome=st.text_input('🪪 Cognome')
            email = st.text_input('📧 Email')
            tipo = st.selectbox('👤 Ruolo',['admin','risorsa'])
            salva_form=st.form_submit_button('Aggiungi',type='primary',icon=':material/save:')
    
    with st.container(border=True):
        if df_commesse:
            st.data_editor(df_commesse,use_container_width=True,height=500,key=f'risorse_modificate_{st.session_state["key"]}',num_rows='dynamic',column_config=column_settings)
            col1,col2,col3=st.columns((1,1,6),gap='small')
            with col1:
                salva_tabella=st.button('Salva',type='primary',icon=':material/save:')
            with col2:
                annulla=st.button('Annulla',icon=':material/cancel:')
        else:
            col1,col2,col3=st.columns((1,1,6),gap='small')
            with col1:
                salva_tabella=st.button('Salva',type='primary',icon=':material/save:',disabled=True)
            with col2:
                annulla=st.button('Annulla',icon=':material/cancel:',disabled=True)

    if salva_form:
        risorsa_dto=RisorsaDTOInsert(email_utente=email,nome_utente=nome,cognome_utente=cognome,tipo_utente=tipo,stato_utente=1,password_utente='1234')
        with getSession() as session:
            try:
                insertRisorsa(risorsa_dto,session)
            except:
                st.toast('Risorsa già presente nel database',icon='⚠️')
                time.sleep(2)
                st.rerun()
        st.toast('Risorsa aggiunta',icon='✅')
        time.sleep(1)
        reset()
        st.rerun()
    
    if salva_tabella:
        with getSession() as session:
            updateDataEditor(st.session_state[f'risorse_modificate_{st.session_state["key"]}'],df_commesse,risorsa,session)
        st.toast('Modifiche salvate',icon='💾')
        time.sleep(1)
        reset()
        st.rerun()
    
    if annulla:
        st.toast('Modifiche annullate',icon='❌')
        time.sleep(1)
        reset()
        st.rerun()