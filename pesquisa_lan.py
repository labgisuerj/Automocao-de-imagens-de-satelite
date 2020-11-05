import urllib.request    
import urllib.parse
import json
import requests
import _thread
import threading
import time
import csv
from datetime import datetime, date, time, timezone
import os.path


a=os.path.exists("C:\\Users\\Bia\\logi.txt")

if not a:
    login=input("Entre com seu login")
    senha=input("Entre com sua senha")
    autenticacao=[login,senha]
    f = open("C:/Users/Bia/logi.txt", "w")
    f.write(str(autenticacao)) 
else:
    f = open("C:/Users/Bia/logi.txt", "r")
    login=f.read().split(',')
    refinar=(''.join(s.replace("'", "") for s in login))
    garimpar=refinar[1:-1]
    autenticacao=garimpar.split()
    
    
date_start=input("Qual a data de inicio?")
data_end=input("Data de fim")
dt_start = datetime.strptime(date_start, '%d/%m/%Y')
dt_limit= datetime.strptime(data_end, '%d/%m/%Y')
ano=dt_start.year
print(ano)
global dat_start
global dat_end
dat_start= dt_start.isoformat()[:10]
dat_end= dt_limit.isoformat()[:10]

class minhaThread(threading.Thread):
    def __init__(self,):
        threading.Thread.__init__(self)       
    def chave_id():
        r = requests.post("https://m2m.cr.usgs.gov/api/api/json/stable/login", json={"username":"britogeo", "password":"988245535Mn2"}) 
    #1  
        retorno=r.text
        chave=json.loads(retorno)
        chavei=chave.get("data")
        erro_code=chave.get("errorCode") 
        error=chave.get("error")
   
        print(chavei)
            
        if error=="AUTH_NO_SSL":
            print("SSL é necessário para a solicitação executada")
        if error=="AUTH_INVALID":
            print("Credenciais de login inválidas")
        if error=="AUTH_UNAUTHORIZED":
            print("Uma chave de API inválida ou expirada foi usada")
        if error=="AUTH_RATE_LIMIT":
            print("Seu nome de usuário e IP tiveram repetidos logins inválidos e foram temporariamente bloqueados")
        if error=="AUTH_ERROR":
            print("Ocorreu um erro durante a autorização")
                    
        return chavei


    def key_id():
        url = requests.post("https://m2m.cr.usgs.gov/api/api/json/stable/login", json={"username":""+autenticacao[0]+"", "password":""+autenticacao[1]+""}) 
    #1  
        retorno2=url.text
        answer=json.loads(retorno2)
        chavei_id=answer.get("data")
        errocode=answer.get("errorCode") 
        error=answer.get("error")
   
        print(chavei_id)
           
        if errocode=="AUTH_NO_SSL":
            print("SSL é necessário para a solicitação executada")
        if errocode=="AUTH_INVALID":
            print("Credenciais de login inválidas")
        if errocode=="AUTH_UNAUTHORIZED":
            print("Uma chave de API inválida ou expirada foi usada")
        if errocode=="AUTH_RATE_LIMIT":
           print("Seu nome de usuário e IP tiveram repetidos logins inválidos e foram temporariamente bloqueados")
        if errocode=="AUTH_ERROR"	:
            print("Ocorreu um erro durante a autorização")
        return chavei_id

           
    def total_cenas():
        chavei=minhaThread.chave_id()
        headers = {'User-Agent': 'ceilometerclient.openstack.common.apiclient','X-Auth-Token': ''+str(chavei)+''}
        r2 = requests.get("https://m2m.cr.usgs.gov/api/api/json/stable/scene-search",headers=headers, json={"maxResults": 400,"datasetName":"LANDSAT_8_C1","sceneFilter": {"ingestFilter": "start":, "end":,"spatialFilter": {"filterType": "mbr", "lowerLeft": {"longitude": -43.4080, "latitude": -23.0775}, "upperRight": {"longitude": -43.1323, "latitude": -22.8499}},"cloudCoverFilter": {"max": 100,"min": 0,"includeUnknown": True}}, "metadataType": "summary","sortDirection": "ASC","startingNumber": 1})
        
        dicionario=r2.text
        dic=json.loads(dicionario)
        dado=dic.get("data")  
        hit=dado.get("totalHits")
        print(hit)
        
        return hit
    
thread_list=[]


class Mythread(threading.Thread):
    def __init__(self, numbero, numero,monte):
        super(Mythread, self).__init__()
        self.numbero=numbero
        self.numero=numero
        self.monte=monte
    def run(self):
        print("Running  "  +  str(self.numero)+  str(self.numbero)+ str(self.monte))

        url4="https://earthexplorer.usgs.gov/inventory/json/v/1.4.0/search"
        url_conf="https://www.labgis.uerj.br/apps/postecho.php"
        if (self.monte%2==0):
            keys=minhaThread.chave_id()
        else:
            keys=minhaThread.key_id()
            
        header = {'User-Agent': 'ceilometerclient.openstack.common.apiclient','X-Auth-Token': ''+str(keys)+''}
        r = requests.get("https://m2m.cr.usgs.gov/api/api/json/stable/scene-search",headers=header, json={"maxResults": 1,"datasetName":"LANDSAT_8_C1","sceneFilter": {"spatialFilter": {"filterType": "mbr", "lowerLeft": {"longitude": -43.4080, "latitude": -23.0775}, "upperRight": {"longitude": -43.1323, "latitude": -22.8499}},"temporalFilter": {"startDate": "2020-01-01", "endDate": "2020-09-30"},"cloudCoverFilter": {"max": 100,"min": 0,"includeUnknown": True}}, "metadataType": "summary","sortDirection": "ASC","startingNumber": 1})
     
        texto_decode=r.text
        txt_decode=json.loads(texto_decode)
        erro=txt_decode.get("error")
      
            
   
        if erro=="SEARCH_ERROR":
            print("Ocorreu um erro ao procurar dados")
        if erro=="SEARCH_INVALID_PARAM":
            print("Um parâmetro de pesquisa inválido foi fornecido")
        

        
        
        numbeReturn= txt_decode.get("data")
        resu=numbeReturn.get("results")
        lista_sumaries= []  
        lista_dicts= [resu]

        gravar = []
        for infos in resu:
            gravar.append(infos['entityId'])
            
        for item in  gravar:
            g=(item)
        ani=str(ano)
        a=os.path.exists('C:/Users/Bia/usgs_'+ani+'.csv')
        if  a==True:
            f = open('C:/Users/Bia/usgs_'+ani+'.csv', 'r')
            ler=f.read().split()
            del(ler[0])
            for item in  gravar:
                ler.append(item)
        else:
            ler=gravar
        
        with open('usgs_'+ani+'.csv', mode='w', encoding='utf-8', newline='') as csv_file:
            fieldnames = [ani]
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            writer.writeheader()
            for idi in ler:
                writer.writerow({ani: idi})
                
                
        with open('meu_arquivo.csv', 'w') as csvfile:
            writer = csv.writer(csvfile,delimiter=",")
            for idi in gravar:
                writer.writerow(idi)

        f = open("C:/Users/Bia/usgs_id.txt", "w")
        f.write(str(gravar)) 

contador=10
start_num=0
mont=0

d=minhaThread.total_cenas()
data1=d
threads=[]
thread_list=[]
while start_num<=data1:
    if(start_num!=0 and  start_num<=data1):        
        while len(threads) < contador and start_num<=data1:
            contador=10
            start_num+=10
            mont+=1
            if start_num<=data1:
                th= Mythread(start_num,contador,mont)
            
                threads.append(th)
                th.start()

            for th in threads:
                th.join()
        threads=[]
        break
    else:
        start_num+=1
        contador=10

        mont+=1

        thread2=Mythread(start_num,contador,mont)
        threads.append(thread2)
        thread2.start()
        for th in threads:
            th.join()
