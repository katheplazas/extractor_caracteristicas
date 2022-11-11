import asyncio
import aiohttp

import json
import sys
import pandas as pd
import time

#pd.options.display.max_columns = None
#pd.options.display.max_rows = None

async def get_steam_reader(pipe) -> asyncio.StreamReader:
    loop = asyncio.get_event_loop()
    reader = asyncio.StreamReader(loop=loop)
    protocol = asyncio.StreamReaderProtocol(reader)
    await loop.connect_read_pipe(lambda: protocol, pipe)
    return reader

async def send_api_request(payload_queue):
    api_predition = "http://sistemic.udea.edu.co:4000/seguridad/preprocesamiento/data/standardization/faster/10/g" #get
    headers = {'Cookie': 'color=rojo','Content-Type': 'application/json'}

    api_time_100_connection = "http://sistemic.udea.edu.co:4000/seguridad/prediccion/save/time/argus/" #post


    #api_predition = "http://194.163.44.55:1880/seguridad/preprocesamiento/data/standardization/faster/10/g"
    #headers = {"Accept": "application/json", "Content-Type": "application/json"}

    #api_time_100_connection = "http://194.163.44.55:1880/seguridad/prediccion/save/time/argus/"
    
    async with aiohttp.ClientSession() as session:
        while True:
            time_ini = time.time()
            data = await payload_queue.get()
            payload = json.dumps(data)
            try:
                async with session.get(api_predition, headers=headers, data=payload) as response:
                    status = await response.text()
                    time_end = time.time() - time_ini
                    print(status)
                    #print(time_end)
                    payload2 = {"time": time_end}
                async with session.post(api_time_100_connection, headers=headers, data = json.dumps(payload2)) as response:
                    status = await response.text()
                    #print("analizado")
            except Exception as e:
                print(e)

async def main():
    reader = await get_steam_reader(sys.stdin)
    count_data = 0
    count = 0
    ids = ["stime", "proto", "saddr", "sport", "daddr", "dport", "pkts", "bytes"
                , "state", "ltime", "dur", "spkts", "dpkts", "sbytes", "dbytes"]
    data = pd.DataFrame(columns=ids)

    payload_queue = asyncio.Queue()
    asyncio.create_task(send_api_request(payload_queue))

    while True:
        data_argus = await reader.readline()
        data_argus = data_argus.decode().rstrip('\n')
        list_data = data_argus.split(",")
        if len(list_data) == 15:
            if type(list_data[3]) != int:
                try:
                    if list_data[3].startswith('0x'):
                        list_data[3] = int(list_data[3],16)
                    else:
                        list_data[3] = int(list_data[3])
                except:
                    list_data[3] = -1
            if type(list_data[5]) != int:
                try:
                    if list_data[5].startswith('0x'):
                        list_data[5] = int(list_data[5],16)
                    else:
                        list_data[5] = int(list_data[5])
                except:
                    list_data[5] = -1
            
            if float(list_data[10]) == 0.0:
                list_data[10] = "0.000001"

            data.loc[count_data] = list_data
            count_data = count_data + 1
            if count_data == 100:
                count_data = 0
                count += 1
                await payload_queue.put(data.to_dict())
                print(count)

if __name__ == "__main__":
    asyncio.run(main())