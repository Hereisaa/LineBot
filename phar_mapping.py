import googlemaps
import json

'''
input:  {ue_location} user location  # 使用者定位
        {phar_addr} pharmacy info # 藥局地址
'''
apiKey = 'AIzaSyCnfl_3Kn51wVMmu8JfiKCs91YlI70HQig'
gmaps = googlemaps.Client(key = apiKey)

# ue_location
# phar_info
# MAX_NUM = 5 # 回傳給使用者的數量
# ue_location = '台東縣台東市更生路11號'
# phar_addr =['新北市石碇區潭邊里碇坪路１段８２號','新北市平溪區公園街１７號１樓',
# '新北市貢寮區朝陽街７０巷１０號','新北市烏來區新烏路５段１０９號']

# 計算使用者到各藥局的 距離(dist) 與 時間(duration)
def calculating(ue_location, phar_addr, total_info):
    dist = {}
    duration = {}
    for addr, info in total_info.items():
        geocode_result = gmaps.geocode(addr)
        lat = geocode_result[0]["geometry"]["location"]["lat"]
        lon = geocode_result[0]["geometry"]["location"]["lng"]
        total_info[addr] = info.append(lat, lon)

    for addr in phar_addr:
        rad = gmaps.distance_matrix(ue_location,addr)['rows'][0]['elements'][0]
        
        # print(addr)
        # print(json.dumps(rad, sort_keys=False, indent=4, separators=(', ', ': ')))
        str = rad['distance']['text']
        d = float(''.join([x for x in str if ( x.isdigit() or x == '.' )]))

        dist.update({addr:d})
        duration.update({addr:rad['duration']['text']})

    sorted_dist = sorted(dist.items(),key=lambda item:item[1])
    print(sorted_dist)
    print('\n')

    return  sorted_dist, duration, total_info





# if __name__ == "__main__":
#     dist, duration = calculating(ue_location, phar_addr, total_info)
# #     print(dist)
# #     print(duration)



# rad['distance']['text'] -> 距離(km)
# rad['duration']['text'] -> 時間(hours mins)