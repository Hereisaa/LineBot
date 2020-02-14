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

    # print('Total_info')
    # for addr, info in total_info.items():
    #     geocode_result = gmaps.geocode(addr)
    #     # print(geocode_result)
    #     lat = geocode_result[0]["geometry"]["location"]["lat"]
    #     lon = geocode_result[0]["geometry"]["location"]["lng"]
    #     info.append(str(lat))
    #     info.append(str(lon))
    #     total_info[addr] = info
    # print('Total_info Done')

    for addr in phar_addr:
        rad = gmaps.distance_matrix(ue_location,addr)['rows'][0]['elements'][0]

        if rad['status'] == 'ZERO_RESULTS': continue

        # print(ue_location)
        # print(addr)
        # print(rad)
        # print(json.dumps(rad, sort_keys=False, indent=4, separators=(', ', ': ')))
        stri = rad['distance']['text']
        d = float(''.join([x for x in stri if ( x.isdigit() or x == '.' )]))

        dist.update({addr:d})
        duration.update({addr:rad['duration']['text']})

    print('Total_info')
    geomatry = []
    for addr in dist.keys():
        geocode_result = gmaps.geocode(addr)
        # print(geocode_result)
        lat = geocode_result[0]["geometry"]["location"]["lat"]
        lon = geocode_result[0]["geometry"]["location"]["lng"]
        geomatry.append([str(lat),str(lon)])
    # print(geomatry)
    print('Total_info Done')

    sorted_dist = sorted(dist.items(),key=lambda item:item[1])
    # print(sorted_dist)

    return  sorted_dist, duration, geomatry





# if __name__ == "__main__":
#     dist, duration = calculating(ue_location, phar_addr, total_info)
# #     print(dist)
# #     print(duration)



# rad['distance']['text'] -> 距離(km)
# rad['duration']['text'] -> 時間(hours mins)