import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from Scripts.Views.settings import CONTROLLER
from Scripts.Connector import getSession
from Scripts.Queries import findLavoriByRisorsa, findAllCommesse
from datetime import datetime
import locale


def user_dashboard():
    risorsa = CONTROLLER.get('risorsa')

    locale.setlocale(locale.LC_TIME, 'it_IT.UTF-8')

    with getSession() as session:
        lavori = findLavoriByRisorsa(risorsa['id'], session)

    if lavori is None or len(lavori) == 0:
        st.warning("Nessun dato di lavoro trovato per questa risorsa")
    
    else:
        df=pd.DataFrame(lavori)
        df['data']=pd.to_datetime(df['data'])
        df['mese']=df['data'].dt.strftime('%B')
        df['mese_numero']=df['data'].dt.month
        df['anno']=df['data'].dt.year
        df.sort_values(by='mese_numero',inplace=True)
        mesi=df['mese'].unique()
        anno=df['anno'].unique()
        anno_recente=max(anno)
        st.title("Dashboard")
        with st.container(border=True):
            st.write('Filtri')
            col1,col2=st.columns((1,3))
            with col1:
                anno_selezionato=st.selectbox('Anno',anno,index=anno.tolist().index(anno_recente))
            with col2:
                mesi_selezionati=st.multiselect('Mese',mesi,default=mesi)
        
        df_filtrato = df
        if anno_selezionato:
            df_filtrato = df_filtrato[df_filtrato['anno'] == int(anno_selezionato)]
        if mesi_selezionati:
            df_filtrato = df_filtrato[df_filtrato['mese'].isin(mesi_selezionati)]

        ore_per_mese = df_filtrato.groupby('mese').agg({'ore':'sum', 'mese_numero':'first'}).reset_index().sort_values(by='mese_numero')

        fig_ore_mese = px.bar(ore_per_mese, x='mese', y='ore',
                                labels={'mese': 'Mese', 'ore': 'Ore Lavorate'},
                                title='Ore lavorate per mese')
        st.plotly_chart(fig_ore_mese)

        ore_commessa_mese=df_filtrato.groupby(['mese','Commessa']).agg({'ore':'sum','mese_numero':'first'}).reset_index().sort_values(by='Commessa')
        
        #st.write(ore_commessa_mese)

        fig=go.Figure()
        
        for commessa in ore_commessa_mese['Commessa'].unique():
            df_filtrato_commessa=ore_commessa_mese[ore_commessa_mese['Commessa']==commessa]
            mese_comessa = mesi_selezionati
            ore_commessa = []
            for mese in mesi_selezionati:
                if mese in df_filtrato_commessa['mese'].values:
                    ore_commessa.append(df_filtrato_commessa[df_filtrato_commessa['mese']==mese]['ore'].values[0])
                else:
                    ore_commessa.append(0)
            fig.add_trace(go.Bar(
                x=mese_comessa,
                y=ore_commessa,
                name=commessa
            ))

        fig.update_layout(
            title='Ore lavorate per commessa per mese',
            xaxis_title='Mese',
            yaxis_title='Ore',
            barmode='group',
            bargap=0.20,
            bargroupgap=0.1
        )

        st.plotly_chart(fig)






    


