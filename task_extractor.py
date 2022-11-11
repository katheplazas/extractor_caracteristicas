import asyncio
import sys
import pandas as pd

async def get_steam_reader(pipe) -> asyncio.StreamReader:
    loop = asyncio.get_event_loop()
    reader = asyncio.StreamReader(loop=loop)
    protocol = asyncio.StreamReaderProtocol(reader)
    await loop.connect_read_pipe(lambda: protocol, pipe)
    return reader

async def main():
    reader = await get_steam_reader(sys.stdin)
    cont_data = 0
    ids = ["stime", "proto", "saddr", "sport", "daddr", "dport", "pkts", "bytes"
                , "state", "ltime", "dur", "spkts", "dpkts", "sbytes", "dbytes"]
    data = pd.DataFrame(columns=ids)
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

            data.loc[cont_data] = list_data    
            cont_data = cont_data + 1

            if cont_data == 100:
                    cont_data = 0
                    print(data)
        #data_argus = data_argus.rstrip('\n')
        #print(list_data[3])


if __name__ == "__main__":
    asyncio.run(main())