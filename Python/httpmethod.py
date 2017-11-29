import urllib2
import urllib

query_args = {
    "data": {    
        "form": {
            "vtsData": {
                "0": {
                    "imei": "345678907643213",
                    "gpsDate": "121017",
                    "gpsTime": "100532",                    
                    "speed": "35",
                    "location": {
                        "lat": "11.78979",
                        "lng": "89.34567"
                    },
                    "others": {
                        "panic": "1",
                        "engine": "0",
                        "ac":"1",
                        "battVolt":"4",
                        "temp":"-30"
                    },
                     "sensors": {
                        "co2": "996",
                        "humidity": "56",
                        "temp":"35"                        
                    }
                }
                 
            }
        }
    }
}


#url = 'http://api.learn2crack.com/rpi/rpi_post.php'
url = 'http://128.199.209.142/iot/request.php'

data = urllib.urlencode(query_args)

request = urllib2.Request(url, data)

response = urllib2.urlopen(request).read()

print response
