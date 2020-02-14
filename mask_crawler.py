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
        ue_location = content[:3]

        with open('maskdata.csv',newline='',encoding="utf-8") as f:
            rows = csv.reader(f)
            for row in rows:
                name_store = row[1]
                location_store = row[2]

                if ue_location == location_store[:3]:
                    phar_info.update({name_store: location_store})
                    phar_addr.append(location_store)
                    res += '{}\n'.format(location_store)
                #print(row[6]) #data update time
            sorted_dist, duration = phar_mapping.calculating(ue_location, phar_addr)

        f.close()

        candi = get_key(phar_info, sorted_dist[:5])
        new_phar_info = dict(zip(candi, sorted_dist))

        return new_phar_info

def get_key(dict, value):
    return [k for k, v in dict.items() if v == value]

def reply(content, msg_type):
    link = get_dl_link()
    get_file(link)
    return get_data(content, msg_type)


# if __name__ ==  "__main__":
#     reply('臺中市口罩')
