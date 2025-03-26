import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from Scripts.Views.settings import CONTROLLER
from Scripts.Connector import getSession
from Scripts.Queries import findLavoriAdmin
from datetime import datetime
import locale


def d_commesse():
    risorsa = CONTROLLER.get('risorsa')

    locale.setlocale(locale.LC_TIME, 'it_IT.UTF-8')

    with getSession() as session:
        lavori = findLavoriAdmin(session)

    if lavori is None or len(lavori) == 0:
        st.warning("Nessun dato di lavoro trovato per questa risorsa")
    
    else:
        df=pd.DataFrame(lavori)
        df['data']=pd.to_datetime(df['data'])
        df['mese']=df['data'].dt.strftime('%B')
        df['mese_numero']=df['data'].dt.month
        df['anno']=df['data'].dt.year
        df.sort_values(by='mese_numero',inplace=True)

        commesse=df['Commessa'].unique()
        commesse_attive=df[df['Stato_commessa']=='aperta']['Commessa'].unique()
        anno=df['anno'].unique()
        anno_recente=max(anno)
        
        st.title('Dashboard lavori')

        with st.container(border=True):
            st.write('Filtri')
            col1,col2=st.columns((1,3))
            with col1:
                tutte_commesse=st.checkbox('Ricerca tutte le commesse',value=False,help='Ricerca tutte le commesse, anche quelle chiuse')
                if tutte_commesse:
                    commessa_selezionata=st.selectbox('Commessa',commesse)
                else:
                    commessa_selezionata=st.selectbox('Commessa',commesse_attive)
            with col2:
                filtro_anno=st.checkbox('Filtra per anno',value=False)
                if filtro_anno:
                    anno_selezionato=st.selectbox('Anno',anno,index=anno.tolist().index(anno_recente))
                else:
                    anno_selezionato=None
            
        if commessa_selezionata:
            df_filtrato=df[df['Commessa']==commessa_selezionata]
            if filtro_anno:
                df_filtrato=df_filtrato[df_filtrato['anno']==anno_selezionato]
            
            ore_risorsa=df_filtrato.groupby('Risorsa').agg({'ore':'sum'}).reset_index()
            
            ore_risorsa_col_settings={
                'Risorsa': st.column_config.TextColumn('🪪 Risorsa'),
                'ore': st.column_config.NumberColumn('⌛ Ore totali',format='%f',width='small')
            }

            st.subheader(f'Commessa: {commessa_selezionata}')
            col3,col4=st.columns((1,2))
            with col3:
                with st.container(border=True):
                    st.dataframe(ore_risorsa,column_config=ore_risorsa_col_settings,hide_index=True,use_container_width=True,height=300)
                    st.write(f'Ore totali fatte: {df_filtrato['ore'].sum()}')
            with col4:
                ore_mese_anno_risorsa=df_filtrato.groupby(['mese','anno','Risorsa']).agg({'ore':'sum','mese_numero':'first'}).reset_index().sort_values(by=['anno','mese_numero'],ascending=[False,False])
                ore_mese_anno_risorsa['mese_anno']=ore_mese_anno_risorsa['mese']+' '+ore_mese_anno_risorsa['anno'].astype(str)
                
                ore_mese_anno_risorsa_col_settings={
                    'mese_anno': st.column_config.TextColumn('📅 Mese',width='small'),
                    'Risorsa': st.column_config.TextColumn('🪪 Risorsa',width='small'),
                    'ore': st.column_config.NumberColumn('⌛ Ore mensili',format='%f',width='small'),
                    'mese_numero': None,
                    'mese':None,
                    'anno':None
                }

                st.dataframe(ore_mese_anno_risorsa,column_config=ore_mese_anno_risorsa_col_settings,column_order=('mese_anno','Risorsa','ore'),hide_index=True,use_container_width=True,height=382)

            with st.expander('Tabella dati giornaliera'):
                df_filtrato.sort_values(by='data',inplace=True,ascending=False)

                df_filtrato_col_settings={
                    'Id': None,
                    'Commessa': None,
                    'Stato_commessa': None,
                    'ore':st.column_config.NumberColumn('⌛ Ore',format='%f',width='small'),
                    'data':st.column_config.DateColumn('📅 Data',format='DD-MM-YYYY',width='small'),
                    'note':st.column_config.TextColumn('💬 Descrizione',max_chars=255,width='large'),
                    'luogo':st.column_config.TextColumn('🏢 Luogo',width='small'),
                    'Risorsa':st.column_config.TextColumn('🪪 Risorsa',width='small'),
                    'mese':None,
                    'mese_numero':None,
                    'anno':None,
                }

                st.dataframe(df_filtrato,column_config=df_filtrato_col_settings,column_order=('data','Risorsa','ore','luogo','note'),hide_index=True,use_container_width=True,height=600)

            col5,col6=st.columns((1,2))
            
            with col5:
                with st.container(border=True):
                        fig_ore_risorse = px.bar(ore_risorsa, x='Risorsa', y='ore',
                                        labels={'Risorsa': 'Risorsa', 'ore': 'Ore totali lavorate'},
                                        title='Ore totali lavorate da risorsa')
                        st.plotly_chart(fig_ore_risorse)

            mesi=ore_mese_anno_risorsa['mese_anno'].unique()
            fig=go.Figure()
            for risorsa in ore_mese_anno_risorsa['Risorsa'].unique():
                df_filtrato_risorsa=ore_mese_anno_risorsa[ore_mese_anno_risorsa['Risorsa']==risorsa]
                mese_comessa = mesi
                ore_commessa = []
                for mese in mese_comessa:
                    if mese in df_filtrato_risorsa['mese_anno'].values:
                        ore_commessa.append(df_filtrato_risorsa[df_filtrato_risorsa['mese_anno']==mese]['ore'].values[0])
                    else:
                        ore_commessa.append(0)
                    
                fig.add_trace(go.Bar(
                    x=mese_comessa,
                    y=ore_commessa,
                    name=risorsa
                ))

            fig.update_layout(
                title='Ore mensili lavorate da risorsa',
                xaxis_title='Mese',
                yaxis_title='Ore',
                barmode='group',
                bargap=0.20,
                bargroupgap=0.1
            )
            with col6:
                with st.container(border=True):
                    st.plotly_chart(fig)
            
            

        
