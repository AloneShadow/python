import geoip, pygeoip, geoip2.database, redis, gmplot, gmaps

ip="178.151.158.167"
#GEOIP = pygeoip.GeoIP("/home/user/geo-ip/GeoLite2-City.mmdb", pygeoip.MEMORY_CACHE)
#GEOIP.country_name_by_addr(ip)

#db = geoip.open_database("/home/user/geo-ip/GeoLite2-City.mmdb")
#result = geoip.geolite2.lookup(ip)
#print result

reader = geoip2.database.Reader("/home/user/geo-ip/GeoLite2-City.mmdb")
response = reader.city(ip)

print response.city.name
print response.location.latitude, response.location.longitude
lat = response.location.latitude
lng = response.location.longitude


#r = redis.StrictRedis(host='212.42.70.1', port=6379, db=0)
#print r.hgetall('ip_score')
#for key in r.hscan_iter('ip_score',match="c*"):
#    print key[1].split('|')[0]


#make base object
gmap = gmplot.GoogleMapPlotter(0, 0, 0)

#make needed object
#gmap = gmap.from_geocode("UA")
#print  dir(gmap.from_geocode("UA"))
#print gmap.from_geocode("UA").center

lats = [20,10]
lngs = [20,10]
gmap.heatmap(lats,lngs,radius=20)


#gmap.plot(7.428, -122.145, 'cornflowerblue', edge_width=10)
#gmap.scatter(more_lats, more_lngs, '#3B0B39', size=40, marker=False)
#gmap.scatter(marker_lats, marker_lngs, 'k', marker=True)
#gmap.heatmap(heat_lats, heat_lngs)

#gmap.draw("mymap.html")

