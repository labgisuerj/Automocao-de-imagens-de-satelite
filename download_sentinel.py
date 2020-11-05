import os 
path="C:/Users/Bia" 
os.chdir(path) 
os.getcwd() 
import json
from datetime import datetime
now = datetime.now()
now.strftime('%Y%m%d')
from sentinelsat import SentinelAPI, read_geojson, geojson_to_wkt
from datetime import date


f = open("ano.txt", "r")
pri=f.read()
b = "''"
for i in range(0,len(b)):
	pr =pri.replace(b[i],"")
f.close()

b = ","
for i in range(0,len(b)):
	p =pr.replace(b[i],"")
f.close()

ids_=p[1:]  
liste=ids_.split()[2:]#lista dos ids do download

f=open("c:/Users/Bia/ids_pasta_sentinel.txt")
s=f.read()

b = ","
for i in range(0,len(b)):
	pr =s.replace(b[i],"")

lista_verifica=pr.split()#lista dos ids que são nomeados assim que baixados
print(lista_verifica)
print(liste)

n=0
m=2
cont=0
list=[]
arq = open('sentinel.csv')
ids = arq.read().split('\n')
print(len(ids))
for i in ids_verificar:
    a=os.path.exists("C:/Users/Bia/" +i+ ".zip")
    if not a:
        while len(ids):
            while cont>=0:
                print(n,m)
                if cont==0:
                    api = SentinelAPI('biancasantana', '988245535', 'https://scihub.copernicus.eu/dhus',show_progressbars=True)
                elif cont==1:
                    api = SentinelAPI('_labgis', '988245535', 'https://scihub.copernicus.eu/dhus',show_progressbars=True)
                else:
                    api = SentinelAPI('labgis_', '988245535', 'https://scihub.copernicus.eu/dhus',show_progressbars=True)

                for e in range(n,m,1):
                    if (m!=(e)):
                        list.append(ids[e])
                break
            
            product_info = api.get_product_odata(list[0])
            product_info1 = api.get_product_odata(list[1])
            if product_info['Online']:
                print('Product {} is online. Starting download.'.format(list[0]))
                api.download(list[0])
            elif product_info1['Online']:
                print('Product {} is online. Starting download.'.format(list[1]))
                api.download(list[1])
            else:
                print('Product {} is not online.'.format(list[0]))
                print('Product {} is not online.'.format(list[1]))
        
            print(list)
            n+=2
            m+=2
            list=[]
            
            print(list)
            if cont==2:
                cont=0
    else:
        print("Produtos das cenas que serão baixados: \n ""Arquivo "+i+" já existem na maquina")
"""
n=0
m=2
cont=0
list=[]
for i in ids_verificar:
	a=os.path.exists("C:/Users/Bia/" +i+ ".zip")
	if not a:
		for item in p:			
			g=(item)[8:]
			#print(g)
			product_info = api.get_product_odata(g[1:-1])
			#p.remove('bb3c799a-3673-46d5-bd60-a75f0b5c7a36')
			
			if product_info['Online']:
			
				print('Product {} is online. Starting download.'.format(g[1:-1]))
				#api.download(g[1:-1])
			else:
				print('Product {} is not online.'.format(g[1:-1]))
	else:
		print("Produtos das cenas que serão baixados: \n ""Arquivo "+i+" já existem na maquina")
        
"""      
        