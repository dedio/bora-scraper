# -*- coding: utf-8 -*-

#  bora_seccion_cuarta.py
#  
#  Copyright 2018 Juan Manuel Dedionigis jmdedio@gmail.com
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#  

import json
import urllib
import scrapy
from common.items import CommonItem
from time import strftime

class BoraSecCuartaSpider(scrapy.Spider):
    name = "bora_seccion_cuarta"
    allowed_domains = ["boletinoficial.gob.ar"]
    start_urls = ()

    # Extrae el código para armar la url
    def formateaenlace(self, pdf):
        return pdf[:4] + pdf[4:6] + pdf[6:8]

    # Formato de fechahora tipo YYYY-MM-DD HH:MM:SS
    def formateafecha(self, fecha):
        return fecha[:4] + '-' + fecha[4:6] + '-' + fecha[6:8] + strftime(" %H:%M:%S")

    # Consulta cada una de las entradas
    def start_requests(self):
        url = 'https://www.boletinoficial.gob.ar/secciones/secciones.json'
        payload = {'nombreSeccion': 'cuarta', 'subCat': 'all',
                   'offset': 1, 'itemsPerPage': 500,
                   'fecha': strftime("%Y%m%d")}
        yield scrapy.Request(url, callback = self.parse_items_cuarta,
             method = "POST",
             headers = {'X-Requested-With': 'XMLHttpRequest',
                      'Referer':'https://www.boletinoficial.gob.ar/',
                      'Accept': 'application/json, text/javascript, */*; q=0.01',
                      'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'},
             body = urllib.urlencode(payload))

    # Extrae la información de cada entrada y la almacena
    def parse_items_cuarta(self, response):
        datos = json.loads(response.body)

        item = CommonItem()
        for data in datos['dataList'][0]:
            enlace = 'https://www.boletinoficial.gob.ar/#!Portada/cuarta/all/'
            item['url'] = enlace + self.formateaenlace(data['archivoPDF'])
            item['fechahora'] = self.formateafecha(data['archivoPDF'])
            item['texto'] = ('Dominio: ' + data['dominio'] + ', Autorizado: ' + data['autorizado'] + ', Num: ' + str(data['nroTramite']))
            yield item
