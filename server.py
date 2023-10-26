#Bibliotecas
import streamlit as st 
import numpy as np 
import pandas as pd 
import time 
import plotly.express as pxfrom 
from socket import *
import time as time
import pickle as pk
import threading
import sys

#Pré processamento dos dados
dfp = pd.DataFrame(open('pv_10kw.csv', 'r'))                 #Dados das Unidades produtoras
dfp = dfp.iloc[2:]
dfp = dfp[0].str.split(',', expand=True)
dfp = dfp.replace('\n','', regex=True)
dfp = dfp.set_index(0)
dfp.index = pd.to_datetime(dfp.index)
dfp = pd.DataFrame(dfp)
dfp = dfp.set_axis(['prod'], axis=1)
dfp['prod'] = dfp['prod'].astype(float)
dft = dfp['prod'].resample('15T').sum()
dft = pd.DataFrame(dft)
df = pd.DataFrame(open('profiles.csv.data', 'r'))            #Dados dasUnidades consumidoras
df = df[0].str.split(',', expand=True)
df1 = pd.DataFrame(df[0])
df2 = pd.DataFrame(df.iloc[0:,1:].sample(n=20,axis='columns'))
df3 = pd.merge(df1,df2,left_index=True, right_index=True)
df3 = df3.set_index(0)
df3.index = pd.to_datetime(df3.index)
df3 = df3.astype(float)
dftotal = df3.join(dft)
dftotal['index'] = dftotal.index                             #Unir informações em um unico dataframe


#Contador Global
lock = threading.Lock()        #Threads para permitir múltiplos acessos
def count(y):
    global x
    x = x+y
    return x

#Definição do host
host = gethostname()   #Computador local
port = 55553

x = 0



#Gerencia acessos do cliente

def gerencia(csocket, adress):
    print(f'Conexão estabelcida com: {adress} ')
    while True:
        time.sleep(0.5)
        csocket.sendall(pk.dumps(dftotal.iloc[[count(1)]]))          #Envia os dados


def main():


    #Inicia Servidor
    print('Servidor iniciado')
    serv = socket(AF_INET, SOCK_STREAM)
    serv.bind((host, port))
    serv.listen(10)                             #Limite de 10
    print(f'Servidor está em {host}:{port}')

    while True:
        csocket, adress = serv.accept()           #Aceita a conexão
        thread = threading.Thread(target=gerencia, args = (csocket, adress))       #Aciona a thread
        thread.start()
        

        #Imprime a quantidade de conexões
        print(f'Conexões ativas: {threading.activeCount() - 1}')
            
        
#Executa main
main()
