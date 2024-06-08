from googlemaps import Client
from googlemaps.places import places_nearby, place
import random

class FoodMapApi:
    def __init__(self, key: str):
        self.api_key = key
        self.gmaps = Client(key = self.api_key)

    def getFoodInfo(self, lat: float, lng: float, target: str = "restaurant") -> list:
        
        radar_results = places_nearby(self.gmaps, location = (lat, lng), radius = 500, type = target, open_now = True)
        info = []
        for result in radar_results['results']:
            if result.get('business_status') == "OPERATIONAL" and \
                result.get('rating') is not None and \
                result.get('rating')  > 4 :
                id, name, rating = "", "", 0.0
                if result.get('place_id') is not None:
                    id = result.get('place_id')
                if result.get('name') is not None:
                    name = result.get('name')
                if result.get('rating') is not None:
                    rating = result.get('rating')
                info.append((id, name, rating))
        result = []
        if len(info) > 3:
            indexs = random.sample(range(1, len(info)-1), 3)
            result = [info[i] for i in indexs]
        else:
            result = info
        return result
    def getLocationUrl(self, id: str) -> str:
        resp = place(self.gmaps, place_id = id)
        if resp.get('result') is None:
            return ""
        return resp.get('result').get('url')
    def getRecommend(self, lat: float, lng: float, target: str = "restaurant"):
        urls, count = [], 0
        while len(urls) < 1 and count < 5:
            infos = self.getFoodInfo(lat, lng, target)
            for info in infos:
                if len(info) > 0: 
                    url = self.getLocationUrl(info[0])
                    if url != "":
                        urls.append(url)
            count += 1
        if len(urls) < 1:
            resp = "I can't find any restaurant nearby now"
        else:
            resp = "I recommend the below restaurant for you\n {}".format("\n".join(urls))
        return resp