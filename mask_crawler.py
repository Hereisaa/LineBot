import requests
import os
import csv
import phar_mapping
from bs4 import BeautifulSoup

def get_dl_link():
    target_url = 'https://data.nhi.gov.tw/Datasets/DatasetResource.aspx?rId=A21030000I-D50001-001'
    rs = requests.session()
    res = rs.get(target_url, verify=False)
    res.encoding = 'utf-8'
    soup = BeautifulSoup(res.text, 'html.parser')   
    content = ""
    for data in soup.select('div .table_common td'):
        content = data.text
        if content[:4] == 'http':
            print(content)
            return content
    return "There have no link."

def get_file(link):
    url = link
    path = 'maskdata.csv'
    
    print('downloading...')

    r = requests.get(url)

    print('download OK.')

    with open(path,'wb') as f:
        f.write(r.content)
    f.close()
    return

def get_data(content, msg_type):
    res = ""
    # location = content[:3]
    # print(location)

    print('Getting data...')

    # content is text
    if msg_type == 'text':
        phar_info = {}
        # phar_addr = []
        phar_addr = set()
        sorted_dist = []

        ue_location = content
        total_info = {}

        with open('maskdata.csv',newline='',encoding="utf-8") as f:
            rows = csv.reader(f)
            count = 0
            for row in rows:
                if count == 0 : 
                    count+=1 
                    continue
                name_store      = row[1]
                location_store  = row[2]
                # {location: name, tel, adult, kid}     
                total_info.update({row[2]:[row[1], row[3], row[4], row[5]]})      

                if ue_location[:3] == location_store[:3]:
                    phar_info.update({name_store: location_store})
                    # phar_addr.append(location_store)
                    phar_addr.add(location_store)
                    res += '{}\n'.format(location_store)
                #print(row[6]) #data update time

            print('Calculating...')
            sorted_dist, geomatry = phar_mapping.calculating(ue_location, phar_addr, total_info)
            print('Done ...')
        f.close()
        print('File closed ...')
        # print(sorted_dist[:5])



        res ={}
        for i in range(5):
            info = total_info.get(sorted_dist[i][0])
            info.append(sorted_dist[i][1])
            info.append(geomatry[i][0])
            info.append(geomatry[i][1])
            res.update({sorted_dist[i][0] : info})
        # {location: name, tel, adult, kid, lat, lon, distance}   


        print(res)
        return res


def reply(content, msg_type):
    link = get_dl_link()
    get_file(link)
    return get_data(content, msg_type)


# if __name__ ==  "__main__":
#     msg = '406台灣台中市北屯區九龍街17號'
#     print(msg[5:])
#     reply(msg[5:], 'text')
