import requests
import os
import csv
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

def get_data(text):
    res = ""
    location = text[:3]
    print(location)
    print('Getting data...')
    with open('maskdata.csv',newline='',encoding="utf-8") as f:
        rows = csv.reader(f)
        for row in rows:
            location_store = row[2]
            if location == location_store[:3]:
                res += '{}\n'.format(location_store)
            #print(row[6]) #data update time
    print(res[:200])
    print('Get data OK.')
    f.close()
    return res[:200]

def reply(text):
    link = get_dl_link()
    get_file(link)
    return get_data(text)

'''
file_name = 'maskdata.csv'
if __name__ ==  "__main__":
    link = get_dl_link()
    get_file(link)
    get_data(file_name)
'''

'''
if __name__ ==  "__main__":
    reply('臺中市口罩')
'''