import requests
import json
from .models import *

def get_url():
    adress = "Красная площадь"
    req_url = requests.get('https://geocode-maps.yandex.ru/1.x/?format=json&apikey=5ee7f7a0-4e38-4217-a958-5215b17c4fe1&geocode={}'.format('adress'))
    data = req_url.json()

    #
    data7 = data['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']['metaDataProperty']['GeocoderMetaData']['text']

    def get_address():
        adresses = data['response']['GeoObjectCollection']['featureMember']
        for adress_data in data:
            address = adress_data['GeoObject']['metaDataProperty']['GeocoderMetaData']['text']
            print(address)

    # дождаться результата
    from subprocess import Popen
    result = Popen.comunicate










#5ee7f7a0-4e38-4217-a958-5215b17c4fe1
