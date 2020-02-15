import googlemaps
import json
import time
import threading

'''
input:  {ue_location} user location  # 使用者定位
        {phar_addr} pharmacy info # 藥局地址
'''
apiKey = 'AIzaSyCnfl_3Kn51wVMmu8JfiKCs91YlI70HQig'
gmaps = googlemaps.Client(key = apiKey)


# Threads todo
def job_distance_matrix(ue_location, addr, dist):
    rad = gmaps.distance_matrix(ue_location,addr)['rows'][0]['elements'][0]
    if rad['status'] == 'ZERO_RESULTS': return
    # print(json.dumps(rad, sort_keys=False, indent=4, separators=(', ', ': ')))
    stri = rad['distance']['text']
    d = float(''.join([x for x in stri if ( x.isdigit() or x == '.' )]))
    dist.update({addr:d})
    # duration.update({addr:rad['duration']['text']})


def job_geocode(addr, geomatry, count):
    geocode_result = gmaps.geocode(addr)
    # print(geocode_result)
    lat = geocode_result[0]["geometry"]["location"]["lat"]
    lon = geocode_result[0]["geometry"]["location"]["lng"]
    # geomatry.append([str(lat),str(lon)])
    geomatry[count] = [str(lat),str(lon)]


# 計算使用者到各藥局的 距離(dist) 與 時間(duration)
def calculating(ue_location, phar_addr, total_info):
    dist = {}
    # geomatry = []
    geomatry = [None]*5
    
    # # # #
    tStart = time.time()
    print('Calculating Matrix...')
    t_distance = []
    count = 0
    for addr in phar_addr:
        t_distance.append(threading.Thread(target = job_distance_matrix, args = (ue_location, addr, dist)))
        t_distance[count].start()
        count += 1
 
    for t in t_distance:
        t.join()

    print('Matrix Done.')
    tEnd = time.time()
    print('It cost %f sec' % (tEnd - tStart))
    # print(dist)

    sorted_dist = sorted(dist.items(),key=lambda item:item[1])
    print(sorted_dist)

    # # # #
    tStart = time.time()
    print('Geomatry...')
    t_geocode = []
    count = 0
    for content in sorted_dist[:5]:
        t_geocode.append(threading.Thread(target = job_geocode, args = (content[0], geomatry, count)))
        t_geocode[count].start()
        count += 1

    for t in t_geocode:
        t.join()

    print('Geomatry Done.')
    tEnd = time.time()
    print('It cost %f sec' % (tEnd - tStart))
    # print(geomatry)




    

    return  sorted_dist, geomatry





# if __name__ == "__main__":
#     dist, duration = calculating(ue_location, phar_addr, total_info)
# #     print(dist)
# #     print(duration)

# # rad['distance']['text'] -> 距離(km)
# # rad['duration']['text'] -> 時間(hours mins)