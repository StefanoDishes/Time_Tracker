import streamlit as st
from Scripts.Views.settings import CONTROLLER
from streamlit_calendar import calendar
from Scripts.Connector import ENGINE
from Scripts.Connector import getSession
from Scripts.Queries import findLavoriByRisorsa,insertLavoro,findAllCommesse,deleteLavoroById,insertLavoro,updateLavoro,findAllActiveCommesse
from Scripts.DTO import LavoroDTOInsert
from datetime import datetime,timedelta
import time

def reset():
     st.session_state['key']+=1

def convertDate(df):
    if df:
        for data in df:
            data['data']=datetime.strptime(data['data'],'%Y/%m/%d')

def addEventsFromDataFrame(df):
    if df:
        calendar_events=[]
        for data in df:
            calendar_events.append({'title':data['Commessa'],'start':data['data'].replace('/','-'),'end':data['data'].replace('/','-'),'resourceId':data['Id']})
        return calendar_events
    else:
        return []

def updateDataEditor(data,df,risorsa,commesse,session):
    for row_id,changes in data['edited_rows'].items():
        #print(f"ID Riga: {row_id}, Modifiche: {changes}")
        row_id_convertito=int(row_id)
        id_update=df[row_id_convertito]['Id']
        commessa_convertita=int(commesse[changes.get('Commessa',df[row_id_convertito]['Commessa'])])
        risorsa_convertita=int(risorsa['id'])
        ore_convertite=float(changes.get('ore',df[row_id_convertito]['ore']))
        data_convertita=changes.get('data',df[row_id_convertito]['data'].strftime('%Y-%m-%d')).replace('-','/')
        luogo_convertito=changes.get('luogo',df[row_id_convertito]['luogo'])
        descrizione_convertita=changes.get('note',df[row_id_convertito]['note'])
        lavoro_aggiornato=LavoroDTOInsert(id_risorsa=risorsa_convertita,id_commessa=commessa_convertita,ore_lavoro=ore_convertite,data_lavoro=data_convertita,luogo_di_lavoro=luogo_convertito,descrizione_lavoro=descrizione_convertita)
        with getSession() as session:
            updateLavoro(id_update,lavoro_aggiornato,session)        

    for new_row in data["added_rows"]:
        #print(f"Nuova Riga: {new_row}")
        commessa_convertita=int(commesse[new_row.get('Commessa')])
        risorsa_convertita=int(risorsa['id'])
        ore_convertite=float(new_row.get('ore'))
        nuovo_lavoro=LavoroDTOInsert(id_risorsa=risorsa_convertita,id_commessa=commessa_convertita,ore_lavoro=ore_convertite,data_lavoro=new_row.get('data').replace('-','/'),luogo_di_lavoro=new_row.get('luogo'),descrizione_lavoro=new_row.get('note',''))
        with getSession() as session:
            insertLavoro(nuovo_lavoro,session)

    for deleted_row_id in data["deleted_rows"]:
        id_delete=df[deleted_row_id]['Id']
        with getSession() as session:
            deleteLavoroById(id_delete,session)

def lavori():
    risorsa = CONTROLLER.get('risorsa')

    if 'key' not in st.session_state:
        st.session_state['key']=0

    with getSession() as session:
            df=findLavoriByRisorsa(risorsa['id'],session)
            commesse=findAllCommesse(session)
            commesse_attive=findAllActiveCommesse(session)
            
    if df is None:
        st.session_state[f'lavori_modificati_{st.session_state["key"]}']={}

    calendar_ev=addEventsFromDataFrame(df)

    convertDate(df)

    column_settings={
        'Id': None,
        'Commessa':st.column_config.SelectboxColumn('🏗️ Commessa',options=commesse.keys(),required=True,help="Elenco delle commesse attive",width='small'),
        'ore':st.column_config.NumberColumn('⌛ Ore',min_value=0.5,max_value=8.0,step=0.5,required=True,help="Numero ore lavorate",width='small'),
        'data':st.column_config.DateColumn('📅 Data',format='DD-MM-YYYY',required=True,help="Data dell'attività lavorativa",width='small'),
        'luogo':st.column_config.SelectboxColumn('🏢 Luogo',options=['Ufficio','Trasferta','Smart working'],required=True,help="Luogo di lavoro",width='small'),
        'note':st.column_config.TextColumn('💬 Descrizione',max_chars=255,help="Descrizione dell'attività lavorativa",width='large')
    }

    st.title("Lavori")
    creazione_multipla=st.checkbox('Creazione multipla',value=False)
    col1,col2=st.columns((1,2))
    with col2:
        calendar_options = {
            "editable": False,
            "selectable": False,
            "initialView": "dayGridMonth",
            "locale": "it",
            "buttonText": {
                "today": "Oggi",
                "month": "Mese",
                "week": "Settimana",
                "day": "Giorno"
            },
            "height":592,
            "headerToolbar": {
                "left": "title",
                "center": "",
                "right": "prev,next"
            },
            "views": {
                "rigth": "prev,next"
            }
        }

        c_css="""
            .fc-toolbar-title {
                font-size: 1.5rem;
            }
        """

        calendar(
            events=calendar_ev,
            options=calendar_options,
            custom_css=c_css,
            key=f'calendar{st.session_state["key"]}'
            )
    
    with col1:          
        with st.form('aggiungi_da_form',enter_to_submit=False,clear_on_submit=True):
            commessa = st.selectbox('🏗️ Commessa',options=commesse_attive.keys())
            ore = st.number_input('⌛ Ore',min_value=0.5,max_value=8.0,step=0.5)
            if creazione_multipla:
                col_mul_1,col_mul_2=st.columns(2)
                with col_mul_1:
                    data_inizio=st.date_input('📅 Data inizio',format='DD/MM/YYYY')
                with col_mul_2:
                    data_fine=st.date_input('📅 Data fine',format='DD/MM/YYYY')
            else:
                data = st.date_input('📅 Data',format='DD/MM/YYYY').strftime('%Y/%m/%d')
            luogo = st.selectbox('🏢 Luogo',options=['Ufficio','Trasferta','Smart working'])
            note = st.text_area('💬 Descrizione',height=140)
            salva_form=st.form_submit_button('Aggiungi',type='primary',icon=':material/save:')

    with st.container(border=True):
        if df:
            st.data_editor(df,use_container_width=True,height=500,key=f'lavori_modificati_{st.session_state["key"]}',num_rows='dynamic',column_config=column_settings)
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

    #st.write(st.session_state[f'lavori_modificati_{st.session_state["key"]}'])
    
    if salva_form:
        if creazione_multipla:
            if data_fine <= data_inizio:
                st.toast('La data di fine deve essere successiva alla data di inizio.',icon='⚠️')
                time.sleep(2)
                st.rerun()

            data_corrente = data_inizio
            while data_corrente <= data_fine:
                data_corrente_conv=data_corrente.strftime('%Y/%m/%d')
                lavoro_dto=LavoroDTOInsert(id_risorsa=risorsa['id'],id_commessa=commesse[commessa],ore_lavoro=ore,data_lavoro=data_corrente_conv,luogo_di_lavoro=luogo,descrizione_lavoro=note)
                with getSession() as session:
                    try:
                        insertLavoro(lavoro_dto,session)
                        data_corrente += timedelta(days=1)
                    except:
                        st.toast('Lavoro già presente nel database',icon='⚠️')
                        time.sleep(2)
                        data_corrente += timedelta(days=1)
                        continue
            st.toast(f'Lavori aggiunti',icon='✅')
        else:
            lavoro_dto=LavoroDTOInsert(id_risorsa=risorsa['id'],id_commessa=commesse[commessa],ore_lavoro=ore,data_lavoro=data,luogo_di_lavoro=luogo,descrizione_lavoro=note)
            with getSession() as session:
                try:
                    insertLavoro(lavoro_dto,session)
                except:
                    st.toast('Lavoro già presente nel database',icon='⚠️')
                    time.sleep(2)
                    st.rerun()
            st.toast('Lavoro aggiunto',icon='✅')
        time.sleep(1)
        reset()
        st.rerun()
    
    if salva_tabella:
        with getSession() as session:
            updateDataEditor(st.session_state[f'lavori_modificati_{st.session_state["key"]}'],df,risorsa,commesse,session)
        st.toast('Modifiche salvate',icon='💾')
        time.sleep(1)
        reset()
        st.rerun()
    
    if annulla:
        st.toast('Modifiche annullate',icon='❌')
        time.sleep(1)
        reset()
        st.rerun()
    
        