import sys
import pandas as pd
import requests
import time
import json

url = "http://sistemic.udea.edu.co:4000/seguridad/preprocesamiento/data/standardization/faster/10/g"
url2 = "http://sistemic.udea.edu.co:4000/seguridad/prediccion/save/time/argus/"
payload={}

headers = {'Cookie': 'color=rojo','Content-Type': 'application/json'}


cont = 0
ids = ["stime", "proto", "saddr", "sport", "daddr", "dport", "pkts", "bytes"
                , "state", "ltime", "dur", "spkts", "dpkts", "sbytes", "dbytes"]
data = pd.DataFrame(columns=ids)
#print(data)
cont2 = 0
while True:
    time_ini = time.time()
    lineaArgus = sys.stdin.readline()
    if lineaArgus:
        #data = data.split(",")
        lineaArgus = lineaArgus.rstrip('\n')
        list_data = lineaArgus.split(",")
        print(list_data)
        if list_data[1] != "man":
            if len(list_data) == 14:
                list_data.insert(7,0)
            if len(list_data) == 15:
                if type(list_data[3]) != int:
                    try:
                        if list_data[3].startswith('0x'):
                          list_data[3] = int(list_data[3],16)
                        else:
                          list_data[3] = int(list_data[3])
                    except:
                        list_data[3] = -1
                        #print("sport: "+str(list_data[3]))
                if type(list_data[5]) != int:
                    try:
                        if list_data[5].startswith('0x'):
                          list_data[5] = int(list_data[5],16)
                        else:
                          list_data[5] = int(list_data[5])
                    except:
                        list_data[5] = -1
                #print("dport: "+str(list_data[5]))
                dur = float(list_data[10])
                #print(dur)
                if dur == 0.0:
                    list_data[10] = "0.000001"
                    #print(f'Cambio: {list_data[10]}')
                #print(list_data)
                data.loc[cont] = list_data
                cont = cont + 1
                if cont == 100:
                    cont2 += 1
                    print(data)
                    cont = 0
                    response = requests.request("GET", url, headers=headers, data=json.dumps(data.to_dict()))
                    time_end = time.time() - time_ini
                    response2 = requests.request("POST", url2+str(time_end), headers=headers, data=payload)
                    print(response.text)