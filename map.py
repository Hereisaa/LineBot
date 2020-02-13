import googlemaps
import json

'''
input:  {ue_loc} user location  # 使用者定位
        {phar_info} pharmacy info # 藥局地址
'''
apiKey = 'AIzaSyCnfl_3Kn51wVMmu8JfiKCs91YlI70HQig'
gmaps = googlemaps.Client(key = apiKey)

ue_loc = '台中市北屯區九龍街31號'
phar_info =['新北市石碇區潭邊里碇坪路１段８２號','新北市平溪區公園街１７號１樓',
'新北市貢寮區朝陽街７０巷１０號','新北市烏來區新烏路５段１０９號']

# 計算使用者到各藥局的距離
dist = {}
duration = {}
def geocoding(ue_loc,phar_info):
    for addr in phar_info:
        rad = gmaps.distance_matrix(ue_loc,addr)['rows'][0]['elements'][0]
        print(json.dumps(rad, sort_keys=False, indent=4, separators=(', ', ': ')))
        dist.update({addr:rad['distance']['text']})
        duration.update({addr:rad['duration']['text']})

geocoding(ue_loc,phar_info)
print(dist)
print(duration)


# res = gmaps.geocode('花蓮縣豐濱鄉豐濱村光豐路４１號')
# print(res)
# loc = res[0]['geometry']['location']
# print(loc)
# rad = gmaps.places_nearby(type = 'food', location = loc, radius = 1000)

# for k, v in rad.items():
#     print(k,v)

# rad = gmaps.distance_matrix(ue_loc,addr)['rows'][0]['elements'][0]
# res = json.dumps(rad, sort_keys=False, indent=4, separators=(', ', ': '))
# print(res)


# rad['distance']['text'] -> 距離(km)
# rad['duration']['text'] -> 時間(hours mins)