import json
import requests
import threading
import csv
from datetime import datetime
import os.path
import os
import sqlite3
import blowfish
import acesso_py
import ast

#requirement.conda

global name_arquivo
global chaves
global url
global datasetName
global spatialFilter
global temporalFilter
global cloudCoverFilter
global resultadofinal

authentication=acesso_py.inicializar_autenticacao()
print(authentication[0])

cob_nuvem_max = input("Insira a porcetagem máxima de nuvem: ")
cob_nuvem_min = input("Insira a porcetagem miníma de nuvem: ")

name_arquivo= input("Nomeie o arquivo que será gerado: ")
date_start_str = input("Qual a data de início(dia/mes/ano): ")#mudar str
data_end_str = input("Data de fim (dia/mes/ano): ")
dt_start = datetime.strptime(date_start_str, '%d/%m/%Y')
dt_limit = datetime.strptime(data_end_str, '%d/%m/%Y')
year = dt_start.year

dat_start = dt_start.isoformat()[:10]#altera o formato da data para pesquisa
dat_end = dt_limit.isoformat()[:10]

diretorio = (os.path.dirname(os.path.realpath(__file__)))

#passar as credenciais aqui, do acesso
chaves=[authentication[0],authentication[2],authentication[4]]

url = "https://m2m.cr.usgs.gov/api/api/json/stable/"

datasetName = "LANDSAT_8_C1"  
    
spatialFilter =  {"filterType": "mbr",
                          "lowerLeft": {"longitude": -43.4080, "latitude": -23.0775},
                          "upperRight": {"longitude": -43.1323, "latitude": -22.8499}}                 
temporalFilter =  {"end": str(dat_end), "start": str(dat_start)}
        
cloudCoverFilter = {"max": cob_nuvem_max ,"min": cob_nuvem_min,"includeUnknown": "true"}


#Obtendo a primeira chave de acesso
def key_api(login, senha):
    try:
        #revisar
        login1 = {"username": login, "password": senha}
        dictionary = requests.post(url+"login", json.dumps(login1))
        
        print(url+"login")
        
        print(dictionary.text)
        
        
        response_dic = json.loads(dictionary.text)       
        erro_code = response_dic.get("errorCode") 
        if erro_code == "AUTH_INVALID":
            print("Credenciais de login inválidas, a verificação da credencial do usuário falhou")
        if erro_code == "AUTH_UNAUTHORIZED":
            print("A conta do usuário não tem acesso ao endpoint solicitado")
        elif erro_code == "AUTH_KEY_INVALID":
            print("Chave de API inválida")

    
        httpStatusCode = dictionary.status_code 
        if dictionary == None:
            print("No output from service")
               
        if response_dic['errorCode'] != None:
            print(response_dic['errorCode'], "- ", response_dic['errorMessage'])
                
        if  httpStatusCode == 404:
            print("404 Not Found")
                
        elif httpStatusCode == 401: 
            print("401 Unauthorized")
                
        elif httpStatusCode == 400:
            print("Error Code", httpStatusCode)
        else:
            key_api = response_dic.get("data")
        
    except Exception as e: 
        dictionary.close()
        print(e)
            
    dictionary.close()
        
    return key_api
   
    #Adquirindo o total de cena para ser utilizado no parametro da pesquisa

write_list=[]

#Classe em que realiza o pedido das cenas
class ThreadSearch(threading.Thread):
    def __init__(self, numero, number,cont):
        super(ThreadSearch, self).__init__()
        #mude renomear variaveis
        self.result= []
        self.number = number#numero inicial 
        self.numero = numero#numero maximo de cada pesquisa, nesse caso é 10
        self.cont = cont#contador para alternar os logins
    def run(self):
        print("Running  "  +  str(self.numero) + " "+  str(self.number)+"  "+ str(self.cont)  )

        if (self.cont% 2 == 0):#alternancia de logins
            keys = key_api(authentication[0],authentication[1])
        else:
            keys = key_api(authentication[2],authentication[3])
            
        header = {'User-Agent': 'ceilometerclient.openstack.common.apiclient','X-Auth-Token': str(keys)}
          
        sceneSearchParameters = {'datasetName' : datasetName, 
                                 'maxResults' : str(self.numero),
                                 
                                 'sceneFilter' : {
                                                  'spatialFilter' : spatialFilter,
                                                  'cloudCoverFilter': cloudCoverFilter,
                                                  'ingestFilter': temporalFilter,
                                                  },
                                                  'startingNumber' : str(self.number), 
                                                  "metadataType": "summary",
                                                  "sortDirection": 'ASC'};
        
        print((sceneSearchParameters))
        scenes = requests.post(url+"scene-search", json.dumps(sceneSearchParameters), headers=header)
     
        txt_decode = json.loads(scenes.text)
        erro = txt_decode.get("errorCode")
        #print(txt_decode)
        if erro == "SEARCH_ERROR":
            print("Ocorreu um erro ao procurar dados")
        if erro == "SEARCH_INVALID_PARAM":
            print("Um parâmetro de pesquisa inválido foi fornecido")
        
        print(txt_decode)
        numberReturn = txt_decode.get("data")
        dic_return = numberReturn.get("results") 
        record = numberReturn.get('recordsReturned')
        
        totalHits= numberReturn.get('totalHits')
       
        print(record)
        
        if record > 0:
            for content in dic_return:
                self.result.append(content['entityId'])#adiciona os ids na lista result
       
    def pegaresultado(self):
        return self.result
        
  
        
#Inicio da thread    
max_scene = 10 #máximo de ids na pesquisa
start_num = 1 #posição inicial
sum_value= 1 

thread_list = []
resultadofinal = []




while True:
    thread1 = []
    while len(thread1) <= len(chaves):
     
        entire_thread = ThreadSearch(max_scene,start_num,sum_value)
        thread1.append(entire_thread)
        entire_thread.start()
        start_num += 10
        sum_value += 1
        
    for entire_thread in thread1:
        entire_thread.join()
        resultadofinal.extend(entire_thread.pegaresultado())
    if len(thread1[-1].pegaresultado()) == 0:
        break

print(resultadofinal)  
        
check_paste = os.path.exists(diretorio+'\\usgs_'+name_arquivo+'.csv')
if  check_paste == False: 
    with open('usgs_'+name_arquivo+'.csv', mode='w', encoding='utf-8', newline='') as csv_file:
        fieldnames = [year]
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        for ids in resultadofinal:
            writer.writerow({year: ids})
        
else:
    print("olabianca")
    unlock = open(diretorio+'\\usgs_'+name_arquivo+'.csv', 'r')
    read = unlock.read().split()
    print(reading)
    del(read[0])#exclui o ano
    if set(read).intersection(resultadofinal):#verifica se há os mesmos itens 
        #if reading in write_list:
        print("Lista Atualizada")
    else:
        for item in resultadofinal:# se nao existir o id no arquivo, adicionará o novo item
            reading.append(item)
        print(reading,"bia")
        with open(r'usgs_'+ano+'.csv', mode = 'a', encoding = 'utf-8', newline = '') as csv_file:
            fieldnames = [ano]
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            writer.writeheader()
            for idi in reading:
                writer.writerow({ano: idi})
            #f.writelines(item) 
            mode=ab
