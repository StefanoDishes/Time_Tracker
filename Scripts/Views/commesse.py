import streamlit as st
from Scripts.Views.settings import CONTROLLER
from Scripts.Connector import ENGINE
from Scripts.Connector import getSession
from Scripts.DTO import CommessaDTOInsert
from Scripts.Queries import insertCommessa,findAllCommesseAdmin,updateCommessa,deleteCommessaById
from datetime import datetime,timedelta
import time

def reset():
     st.session_state['key']+=1

def updateDataEditor(data,df,session):
    for row_id,changes in data['edited_rows'].items():
        #print(f"ID Riga: {row_id}, Modifiche: {changes}")
        row_id_convertito=int(row_id)
        id_update=df[row_id_convertito]['Id']
        commessa_convertita=changes.get('Nome',df[row_id_convertito]['Nome'])
        stato_convertito=changes.get('Stato',df[row_id_convertito]['Stato'])
        inizio_convertito=changes.get('Inizio',df[row_id_convertito]['Inizio'])
        fine_convertito=changes.get('Fine',df[row_id_convertito]['Fine'])
        descrizione_convertita=changes.get('Note',df[row_id_convertito]['Note'])
        commessa_aggiornata=CommessaDTOInsert(nome_commessa=commessa_convertita,stato_commessa=stato_convertito,inizio_commessa=inizio_convertito,fine_commessa=fine_convertito,note_commessa=descrizione_convertita)
        with getSession() as session:
            updateCommessa(id_update,commessa_aggiornata,session)        

    for new_row in data["added_rows"]:
        #print(f"Nuova Riga: {new_row}")
        commessa_convertita=new_row.get('Nome')
        stato_convertito=new_row.get('Stato')
        inizio_convertito=int(new_row.get('Inizio'))
        descrizione_convertita=new_row.get('Note','')
        nuova_commessa=CommessaDTOInsert(nome_commessa=commessa_convertita,stato_commessa=stato_convertito,inizio_commessa=inizio_convertito,note_commessa=descrizione_convertita)
        with getSession() as session:
            insertCommessa(nuova_commessa,session)

    for deleted_row_id in data["deleted_rows"]:
        id_delete=df[deleted_row_id]['Id']
        with getSession() as session:
            try:
                deleteCommessaById(id_delete,session)
            except:
                st.toast('Non è possibile eliminare la commessa',icon='⚠️')
                time.sleep(2)
                reset()
                st.rerun()

def commesse():
    risorsa = CONTROLLER.get('risorsa')
    
    if 'key' not in st.session_state:
        st.session_state['key']=0

    with getSession() as session:
        df_commesse=findAllCommesseAdmin(session)
    
    
    if df_commesse is None:
        st.session_state[f'commesse_modificate_{st.session_state["key"]}']={}
    
    column_settings={
        'Id': None,
        'Nome':st.column_config.TextColumn('🏗️ Nome',required=True,help="Nome commessa",width='medium'),
        'Stato':st.column_config.SelectboxColumn('📖 Stato',options=['aperta','chiusa'],required=True,help="Stato della commessa",width='small'),
        'Inizio':st.column_config.NumberColumn('📅 Inizio',step=1,format='%i',required=True,help="Anno di inizio",width='small'),
        'Fine':st.column_config.NumberColumn('📅 Fine',step=1,format='%i',help="Anno di fine",width='small'),
        'Note':st.column_config.TextColumn('💬 Descrizione',max_chars=255,help="Descrizione della commessa",width='large')
    }
    
    st.title("Gestione commesse")
    with st.form('aggiungi_da_form',enter_to_submit=False,clear_on_submit=True):
            commessa = st.text_input('🏗️ Commessa')
            note = st.text_area('💬 Descrizione',height=140)
            salva_form=st.form_submit_button('Aggiungi',type='primary',icon=':material/save:')
    
    with st.container(border=True):
        if df_commesse:
            st.data_editor(df_commesse,use_container_width=True,height=500,key=f'commesse_modificate_{st.session_state["key"]}',num_rows='dynamic',column_config=column_settings)
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
        commessa_dto=CommessaDTOInsert(nome_commessa=commessa,note_commessa=note)
        with getSession() as session:
            try:
                insertCommessa(commessa_dto,session)
            except:
                st.toast('Commessa già presente nel database',icon='⚠️')
                time.sleep(2)
                st.rerun()
        st.toast('Commessa aggiunta',icon='✅')
        time.sleep(1)
        reset()
        st.rerun()
    
    if salva_tabella:
        with getSession() as session:
            updateDataEditor(st.session_state[f'commesse_modificate_{st.session_state["key"]}'],df_commesse,session)
        st.toast('Modifiche salvate',icon='💾')
        time.sleep(1)
        reset()
        st.rerun()
    
    if annulla:
        st.toast('Modifiche annullate',icon='❌')
        time.sleep(1)
        reset()
        st.rerun()