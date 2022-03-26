import requests
import json
import random
import get_image
from io import BytesIO
from PIL import Image

class ParseAPI():
    def __init__(self):
        pass

    def __get_api(self, url):
        req = requests.get(url).content
        return json.loads(req)

    def __get_image_bytes(self, image_url):
        req = requests.get(image_url)
        return BytesIO(req.content).read()

    def random_movie(self, url="https://swapi-deno.azurewebsites.net/api/films"):
        r = self.__get_api(url)
        chosen = random.choice(r)
        return {"title": chosen["title"], "desc": chosen["opening_crawl"]}

    def random_person(self, url="https://swapi-deno.azurewebsites.net/api/people"):
        r = self.__get_api(url)
        chosen = random.choice(r)
        return {"name": chosen["name"], "image_bytes": self.__get_image_bytes(get_image.GI(chosen['name']))}

    def random_vehicle(self, url="https://swapi-deno.azurewebsites.net/api/vehicles"):
        r = self.__get_api(url)
        chosen = random.choice(r)
        return {"name": chosen["name"], "image_bytes": self.__get_image_bytes(get_image.GI(chosen['name']))}

    def random_ship(self, url="https://swapi-deno.azurewebsites.net/api/starships"):
        r = self.__get_api(url)
        chosen = random.choice(r)
        return {"name": chosen["name"], "image_bytes": self.__get_image_bytes(get_image.GI(chosen['name']))}

if __name__ == '__main__':
    x = ParseAPI().get_image_bytes("https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSAW3PLsAxsd-IYE0zhg_nM2meANHQQkETYUtedI_TMWk54ZDg4QNEj1dcUZw&s")
    print(x)
