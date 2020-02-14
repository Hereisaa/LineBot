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
        phar_addr = []
        sorted_dist = []
        duration ={}
        candi = []
        ue_location = '臺東縣台東市更生路11號'

        total_info = {}

        with open('maskdata.csv',newline='',encoding="utf-8") as f:
            rows = csv.reader(f)
            for row in rows:
                name_store      = row[1]
                location_store  = row[2]
                # {location: name, tel, adult, kid}     
                total_info.update({row[2]:[row[1], row[3], row[4], row[5]]})      

                if ue_location[:3] == location_store[:3]:
                    phar_info.update({name_store: location_store})
                    phar_addr.append(location_store)
                    res += '{}\n'.format(location_store)
                #print(row[6]) #data update time
            sorted_dist, duration, total_info = phar_mapping.calculating(ue_location, phar_addr, total_info)
        f.close()
        # print(sorted_dist[:5])



        res ={}
        for i in range(5):
            info = total_info.get(sorted_dist[i][0])
            info.append(sorted_dist[i][1])
            res.update({sorted_dist[i][0] : info})
        # {location: name, tel, adult, kid, lat, lon, distance}   

        # # 藥局名稱
        # for i in range(5):
        #     candi.append( list(phar_info.keys())[list(phar_info.values())
        #          .index(sorted_dist[i][0])] )

        # # 藥局地址
        # sorted_addr = []
        # for i in range(5):
        #     sorted_addr.append(sorted_dist[i][0])

        # # 名稱:地址
        # new_phar_info = dict(zip(candi, sorted_addr))

        print(res)
        return res


def reply(content, msg_type):
    link = get_dl_link()
    get_file(link)
    return get_data(content, msg_type)


if __name__ ==  "__main__":
    reply('臺東縣口罩', 'text')
