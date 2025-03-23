import streamlit as st
from Scripts.Views.settings import CONTROLLER
from streamlit_calendar import calendar
from Scripts.Connector import ENGINE
from Scripts.Connector import getSession
from Scripts.Queries import findAssenzeByRisorsa,deleteAssenzaById,insertAssenza,updateAssenza
from Scripts.DTO import AssenzaDTOInsert
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
            calendar_events.append({'title':data['tipo'],'start':data['data'].replace('/','-'),'end':data['data'].replace('/','-'),'resourceId':data['Id']})
        return calendar_events
    else:
        return []

def updateDataEditor(data,df,risorsa,session):
    for row_id,changes in data['edited_rows'].items():
        #print(f"ID Riga: {row_id}, Modifiche: {changes}")
        row_id_convertito=int(row_id)
        id_update=df[row_id_convertito]['Id']
        risorsa_convertita=int(risorsa['id'])
        tipo_assenza_convertita=changes.get('tipo',df[row_id_convertito]['tipo'])
        ore_convertite=int(changes.get('durata',df[row_id_convertito]['durata']))
        data_convertita=changes.get('data',df[row_id_convertito]['data'].strftime('%Y-%m-%d')).replace('-','/')
        descrizione_convertita=changes.get('note',df[row_id_convertito]['note'])
        assenza_aggiornata=AssenzaDTOInsert(id_utente=risorsa_convertita,tipo_assenza=tipo_assenza_convertita,durata_assenza=ore_convertite,data_assenza=data_convertita,note_assenza=descrizione_convertita)
        with getSession() as session:
            updateAssenza(id_update,assenza_aggiornata,session)        

    for new_row in data["added_rows"]:
        #print(f"Nuova Riga: {new_row}")
        tipo_assenza_convertita_n=new_row.get('tipo')
        risorsa_convertita=int(risorsa['id'])
        ore_convertite_n=int(new_row.get('durata'))
        data_convertita_n=new_row.get('data').replace('-','/')
        nuovo_assenza=AssenzaDTOInsert(id_utente=risorsa_convertita,tipo_assenza=tipo_assenza_convertita_n,durata_assenza=ore_convertite_n,data_assenza=data_convertita_n,note_assenza=new_row.get('note',''))
        with getSession() as session:
            insertAssenza(nuovo_assenza,session)

    for deleted_row_id in data["deleted_rows"]:
        id_delete=df[deleted_row_id]['Id']
        with getSession() as session:
            deleteAssenzaById(id_delete,session)

def assenze():
    risorsa = CONTROLLER.get('risorsa')

    if 'key' not in st.session_state:
        st.session_state['key']=0

    with getSession() as session:
            df=findAssenzeByRisorsa(risorsa['id'],session)

    if df is None:
        st.session_state[f'assenze_modificate_{st.session_state["key"]}']={}

    calendar_ev=addEventsFromDataFrame(df)

    convertDate(df)

    column_settings={
        'Id': None,
        'tipo':st.column_config.SelectboxColumn('🏖️ Tipo assenza',options=['Ferie','Malattia'],required=True,help="Elenco dei tipi di assenza",width='small'),
        'durata':st.column_config.NumberColumn('⌛ Ore',min_value=1,max_value=8,step=1,required=True,help="Numero ore di assenza",width='small'),
        'data':st.column_config.DateColumn('📅 Data',format='DD-MM-YYYY',required=True,help="Data dell'assenza",width='small'),
        'note':st.column_config.TextColumn('💬 Descrizione',max_chars=255,help="Motivo dell'assenza",width='large')
    }

    st.title("Assenze")
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
            "height":508,
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
            assenza = st.selectbox('🏖️ Tipo di assenza',options=['Ferie','Malattia'])
            ore = st.number_input('⌛ Ore',min_value=1,max_value=8,step=1)
            if creazione_multipla:
                col_mul_1,col_mul_2=st.columns(2)
                with col_mul_1:
                    data_inizio=st.date_input('📅 Data inizio',format='DD/MM/YYYY')
                with col_mul_2:
                    data_fine=st.date_input('📅 Data fine',format='DD/MM/YYYY')
            else:
                data = st.date_input('📅 Data',format='DD/MM/YYYY').strftime('%Y/%m/%d')
            note = st.text_area('💬 Descrizione',height=140)
            salva_form=st.form_submit_button('Aggiungi',type='primary',icon=':material/save:')

    with st.container(border=True):
        if df:
            st.data_editor(df,use_container_width=True,height=500,key=f'assenze_modificate_{st.session_state["key"]}',num_rows='dynamic',column_config=column_settings)
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
                assenza_dto=AssenzaDTOInsert(id_utente=risorsa['id'],tipo_assenza=assenza,durata_assenza=ore,data_assenza=data_corrente_conv,note_assenza=note)
                with getSession() as session:
                    try:
                        insertAssenza(assenza_dto,session)
                        data_corrente += timedelta(days=1)
                    except:
                        st.toast('Assenza già presente nel database',icon='⚠️')
                        time.sleep(2)
                        data_corrente += timedelta(days=1)
                        continue
            st.toast(f'Assenze aggiunte',icon='✅')
        else:
            assenza_dto=AssenzaDTOInsert(id_utente=risorsa['id'],tipo_assenza=assenza,durata_assenza=ore,data_assenza=data,note_assenza=note)
            with getSession() as session:
                try:
                    insertAssenza(assenza_dto,session)
                except:
                    st.toast('Assenza già presente nel database',icon='⚠️')
                    time.sleep(2)
                    st.rerun()
            st.toast('Assenza aggiunta',icon='✅')
        time.sleep(1)
        reset()
        st.rerun()
    
    if salva_tabella:
        with getSession() as session:
            updateDataEditor(st.session_state[f'assenze_modificate_{st.session_state["key"]}'],df,risorsa,session)
        st.toast('Modifiche salvate',icon='💾')
        time.sleep(1)
        reset()
        st.rerun()
    
    if annulla:
        st.toast('Modifiche annullate',icon='❌')
        time.sleep(1)
        reset()
        st.rerun()