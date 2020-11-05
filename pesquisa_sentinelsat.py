import os 
path="C:/Users/Bia" 
os.chdir(path) 
os.getcwd() 
import json
from datetime import datetime
now = datetime.now()
now.strftime('%Y%m%d')
import pandas as pd 
import _thread
import threading
#import pandas as pd
#import numpy as np
# Nos conectamos a la API de sentinelsat:
#from sentinelsat import SentinelAPI, read_geojson, geojson_to_wkt

from sentinelsat import SentinelAPI, read_geojson, geojson_to_wkt
from datetime import date
import csv
 


# Iniciamos la solicitud de busqueda de la imagen:
class Mythread(threading.Thread):
    def __init__(self,data_end,data_start):
        super(Mythread, self).__init__()
        self.data_end=data_end
        self.data_start=data_start
        print("Running  "  +  str(self.data_end)+  str(self.data_start))
    def run(self):
        print("Running  "  +  str(self.data_end)+  str(self.data_start))
        api = SentinelAPI('biancasantana', '988245535', 'https://scihub.copernicus.eu/dhus',show_progressbars=True)
        footprint = geojson_to_wkt(read_geojson('Ufrj.geojson'))
        p='Sentinel-2'
        products = api.query(footprint,
                             date = (str(self.data_start),str(data_end)),
                             platformname = p,       
                             cloudcoverpercentage = '[0 TO 100]')
        print(type(products))

    
        products_df = api.to_dataframe(products)
 
        ids=products_df.index
        #correct abaixo
        ru=str(ids)
        io=(ru.replace("Index([",""))
        reti_col=(io.replace("],", ""))
        ids_pasta=reti_col.replace("dtype='object')","")

        b = "''"
        for i in range(0,len(b)):
            pro =ids_pasta.replace(b[i],"")


        b=","
        for i in range(0,len(b)):
            pio =pro.replace(b[i],"")
        prin=pio.split()

        with open('sentinel_ids_download.csv', mode='w', encoding='utf-8', newline='') as csv_file:
            
            fieldnames = ["id"]
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            writer.writeheader()
            for idi in prin:
                writer.writerow({"id": idi})
        
        #correct acima
        products_df = api.to_dataframe(products)
        title=(products_df.set_index('title'))
        ids_txt=(title.index)
        ru=str(ids_txt)
        int=(ru.replace("Index([",""))
        ret_para=(int.replace("dtype='object', name='title'",""))
        reti_col=(ret_para.replace("],", ""))
        ids_pasta=reti_col.replace(")","")
        b = "''"
        for i in range(0,len(b)):
            pro =ids_pasta.replace(b[i],"")
        print(pro)


        b=","
        for i in range(0,len(b)):
            pio =pro.replace(b[i],"")
        prin=pio.split()
        with open('sentinel_certo.csv', mode='w', encoding='utf-8', newline='') as csv_file:
            fieldnames = ["id"]
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            writer.writeheader()
            for idi in prin:
                writer.writerow({"id": idi})
        #correct acim
      
                             
        return products    
i=0
while i<100:        
    date_start="20151025"
    #input("Qual a data de inicio?")

    data_end="20151230"
    #input("Data de fim")
    threads=[]


    th= Mythread(data_end,date_start)

            
    threads.append(th)
    th.start()
  

    d_start="20120101"
    #input("Qual a data de inicio?")

    d_end="20120530"
    #input("Data de fim")


    the= Mythread(d_end,d_start)



            
    threads.append(the)
    the.start()

               
    start="20110611"
    #input("Qual a data de inicio?")

    end="20110825"
    #input("Data de fim")
    threads=[]


    thi= Mythread(end,start)

            
    threads.append(thi)
    thi.start()
    for th in threads:
        th.join()
    i+=1
    print(i)
                     
    
                     
