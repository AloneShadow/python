import gmplot
import redis
import geoip2.database, pygeoip
import time

countries = {}
ips = {}
dmin = 5
dmax = 50
xmin = 100000
xmax = 0
ll_countries = {}

for country in open("countries.txt","r+"):
    country_c, lat, lng = country.strip().split()
    ll_countries[country_c] = (lat,lng)

reader = geoip2.database.Reader("/home/user/geo-ip/GeoLite2-City.mmdb")

#connect to Redis database
r = redis.StrictRedis(host='10.20.30.1', port=6379, db=0)


def country_map ():
 global xmin, xmax
 #make Gmap object
 gmap = gmplot.GoogleMapPlotter(49.0, 31.0, 3)
 #print r.hgetall('ip_score')
 for key in r.hscan_iter('ip_score',match="c*"):
    country = key[0].split(":")[1]
    reputation = float(key[1].split('|')[0])
    if reputation < 0: color = "green"
    elif reputation > 9.0: color = "red"
    else: color = "black"
    message_amount = int(key[1].split('|')[1])
    if message_amount > xmax: xmax = message_amount
    if message_amount < xmin: xmin = message_amount
    if country in ll_countries: 
        lat, lng = ll_countries[country]
    else:
        lat,lng = gmap.from_geocode(country).center
        fd = open("countries.txt","a")
        fd.write(country+"  "+str(lat)+" "+str(lng)+"\n")
        fd.close()
    #print country, reputation, message_amount #debug
    countries[country] = [(lat, lng), color, message_amount]
    #print country, time.sleep(5)

 for country in countries:
    radius = ((countries[country][2] - xmin)*(dmax-dmin)/(xmax - xmin)) + dmin
    #print country, countries[country][0][0], countries[country][0][1], countries[country][1], radius #debug
    gmap.circle(float(countries[country][0][0]), float(countries[country][0][1]), radius=0, color = countries[country][1], edge_width = radius, title = 'AA')

 gmap.draw("country.html")

def ip_map ():
 fd = open("ip_csv","w")
 global xmax, xmin
 lat_lng = {}
 cities = {}
 #make Gmap object
 gmap = gmplot.GoogleMapPlotter(49.0, 31.0, 3)
 #print r.hgetall('ip_score')
 for key in r.hscan_iter('ip_score',match="[0-9]*.*[0-9].*"):
    ip = key[0]
    reputation = float(key[1].split('|')[0])
    if reputation < 0: color = "green"
    elif reputation > 9.0: color = "red"
    else: color = "blue"
    message_amount = int(key[1].split('|')[1])
    if message_amount > xmax: xmax = message_amount
    if message_amount < xmin: xmin = message_amount
    try:
        response = reader.city(ip)
    except:
        print ip
    city = response.city.name
    lat = response.location.latitude
    lng = response.location.longitude
    if type(lat)==float and type(lng)==float: pass
    else: print ip, lat, lng; continue
    key = str(lat)+"_"+str(lng)
    if key in lat_lng:
        lat_lng[key] += message_amount
    else:
        lat_lng[key] = message_amount
    if city in cities:
        cities[city] += message_amount
    else:
        cities[city] = message_amount

 fw = open("cities_sorted", mode="w")
 for city in sorted(cities, key=cities.get, reverse=True):
    c = city
    print city, c, type(city), type(c), cities[city]
    #print key, cities[key] #debug
    if len(city) <= 7: city = city+"\t\t\t"
    elif len(city) <=15: city = city+"\t\t"
    else: city = city+"\t"
    fw.write(city+str(cities[city])+"\n")
 fw.close()
 """for ip in ips:
    radius = ((ips[ip][2] - xmin)*(dmax-dmin)/(xmax - xmin)) + dmin
    #print country, ips[][0][0], countries[country][0][1], countries[country][1], radius #debug
    try:
        gmap.circle(float(ips[ip][0][0]), float(ips[ip][0][1]), radius=0, color = ips[ip][1], edge_width = radius, title = 'AA')
    except: 
        print ip, ips[ip]
 """
 # gmap.heatmap(lats, lngs)

 #gmap.draw("ip.html")

def city_map ():
 global xmax, xmin
 lat_lng = {}
 cities = {}
 cnt=1
 #make Gmap object
 gmap = gmplot.GoogleMapPlotter(49.0, 31.0, 3)
 for key in r.hscan_iter('ip_score',match="[0-9]*.*[0-9].*"):
    ip = key[0]

    reputation = float(key[1].split('|')[0])
    if reputation < 0: color = "green"
    elif reputation > 9.0: color = "red"
    else: color = "blue"

    message_amount = int(key[1].split('|')[1])
    if message_amount > xmax: xmax = message_amount
    if message_amount < xmin: xmin = message_amount

    try:
        response = reader.city(ip)
    except:
        print ip
    city = response.city.name
    lat = response.location.latitude
    lng = response.location.longitude
    if type(lat)==float and type(lng)==float: 
        pass
    else:
        print ip, lat, lng
        continue

    key = str(round(lat, 2))+"_"+str(round(lng,2))
    if key in lat_lng:
        lat_lng[key] += message_amount
    else:
        lat_lng[key] = message_amount
    if city in cities:
        cities[city] += message_amount
    else:
        cities[city] = message_amount
    #if cnt> 20:break
    cnt+=1

 fw = open("city.txt", mode="w")
 for city in cities:
    try:
        if len(city) <= 7: city_ch = city+"\t\t\t"
        elif len(city) <=15: city_ch = city+"\t\t"
        else: city_ch = city+"\t"
    except:
        print city, type(city), cities[city]
        city_ch = "Unknown \t\t"
    fw.write(city_ch.encode('utf-8')+str(cities[city])+"\n")
 fw.close()

 for key in lat_lng:
    lat = key.split("_")[0]
    lng = key.split("_")[1]
    #print lat, lng, key
    radius = ((lat_lng[key] - xmin)*(dmax-dmin)/(xmax - xmin)) + dmin
    gmap.circle(float(lat), float(lng), radius=0, face_color="white", edge_width = radius, edge_color="black")
    #print key, lat_lng[key]
 gmap.draw("city.html")

country_map()
city_map()
#ip_map()

