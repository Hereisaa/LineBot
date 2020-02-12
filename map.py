import googlemaps

apiKey = 'AIzaSyCnfl_3Kn51wVMmu8JfiKCs91YlI70HQig'

gmaps = googlemaps.Client(key = apiKey)
res = gmaps.geocode('高雄市')
print(res)
loc = res[0]['geometry']['location']
print(loc)
rad = gmaps.places_nearby(type = 'food', location = loc, radius = 1000)

for k, v in rad.items():
    print(k,v)