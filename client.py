#Bibliotecas
from socket import *
import pickle as pk
import streamlit as st
import numpy as np 
import pandas as pd 
import time 
import plotly.express as px 
import sys


#Definição do host
host = gethostname()
port = 55553


#Conecta ao servidor
client = socket(AF_INET,SOCK_STREAM)
client.connect((host, port))
df = pd.DataFrame(columns=['casa1','casa2','casa3','casa4','casa5','casa6','casa7','casa8','casa9','casa10','casa11','casa12','casa13','casa14','casa15','casa16','casa17','casa18','casa19','casa20','prod','index'])


#Configurações da pagina Web
st.set_page_config(
    page_title = 'Dados de consumo e geração de energia',
    layout = 'wide'
)
st.title('Dados de _consumo_ e _geração_ de :red[energia] elétrica :bulb:')
st.markdown(f'Connected to {host}...')
placeholder = st.empty()


while 1: 
    data = pk.loads(client.recv(9200))        #Recebe os dados

    #Processa os dados
    data = pd.DataFrame(data)
    df = pd.DataFrame(df.values)
    df.columns = range(df.shape[1])
    data.columns = range(data.shape[1])    df= pd.concat([df, data], axis=0)
    df[22] = df.iloc[0:,:20].sum(axis = 1)
    df[23] = df[22] + df[20]
   
    with placeholder.container():

        #Colunas com informações únicas
        prod= np.sum(df[20]) 
        gast= np.sum(df[22]) 
        rest = np.sum(df[22]) + np.sum(df[20]) 

        if1, if2, if3 = st.columns(3)
        if1.metric(label="Gasto", value= f"{int(gast)}KW ")
        if2.metric(label="Produção", value= f"{int(prod)}KW ")
        if3.metric(label="Resultado", value= f"{int(rest)}KW ")

        #Colunas com os Gráficos
        fig_col1, fig_col2 = st.columns(2)
        with fig_col1:
            st.markdown('Consumo de cada residência:')
            fig1 = px.line(data_frame= df,x = 21, y = [0,1,2,3,4,5,6,7,8,9,10,12,13,14,15,16,17,18,19] )
            st.write(fig1)

        with fig_col2:
            st.markdown('Consumo de todas as residências:')
            fig2 = px.line(data_frame= df,x = 21, y = 22)
            st.write(fig2)

        fig_col3, fig_col4 = st.columns(2)
           
        with fig_col3:   
            st.markdown('Produção das unidades geradoras:')
            fig3 = px.line(data_frame= df,x = 21, y = 20)
            st.write(fig3)

        with fig_col4:
            st.markdown('Produção x Consumo')
            fig3 = px.line(data_frame= df,x = 21, y = [20,22,23])
            st.write(fig3)

        #Imprime o Dataframe
        st.markdown('Visão de dados:  ')
        st.dataframe(df)
        time.sleep(0.2)
