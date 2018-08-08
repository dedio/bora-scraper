# -*- coding: utf-8 -*-

#  bora_seccion_primera.py
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
import re
import urllib
import scrapy
from scrapy.selector import Selector
from common.items import CommonItem
from time import strftime

class BoraSecPrimeraSpider(scrapy.Spider):
    name = "bora_seccion_primera"
    allowed_domains = ["boletinoficial.gob.ar"]
    start_urls = ()

    # Formato de fechahora tipo YYYY-MM-DD HH:MM:SS
    def formateafecha(self, fecha):
        return fecha[:4] + '-' + fecha[4:6] + '-' + fecha[6:8] + strftime(" %H:%M:%S")

    def limpiaetiquetas(self, item_texto):
        tag_re = re.compile(r'<[^>]+>')
        return tag_re.sub("", item_texto)

    # Solicita la primera sección
    def start_requests(self):
        url = 'https://www.boletinoficial.gob.ar/secciones/secciones.json'
        payload = {'nombreSeccion': 'primera', 'subCat': 'all',
                   'offset': 1, 'itemsPerPage': 500,
                   'fecha': strftime("%Y%m%d")}
        yield scrapy.Request(url, callback = self.parse_primera,
             method = "POST",
             headers = {'X-Requested-With': 'XMLHttpRequest',
                      'Referer':'https://www.boletinoficial.gob.ar/',
                      'Accept': 'application/json, text/javascript, */*; q=0.01',
                      'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'},
             body = urllib.urlencode(payload))

    # Consulta cada una de las entradas
    def parse_primera(self, response):
        data = json.loads(response.body)
        url = 'https://www.boletinoficial.gob.ar/norma/detallePrimera'
        for edict in data['dataList'][0]:
            payload = {'numeroTramite': edict['idTamite']}
            yield scrapy.Request(url, callback = self.parse_items_primera,
                 method = "POST",
                 headers = {'X-Requested-With': 'XMLHttpRequest',
                          'Referer':'https://www.boletinoficial.gob.ar/',
                          'Accept': 'application/json, text/javascript, */*; q=0.01',
                          'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'},
                 body = urllib.urlencode(payload))

    # Extrae la información de cada entrada y la almacena
    def parse_items_primera(self, response):
        data = json.loads(response.body)['dataList']
        hxs = Selector(text = data['detalleNorma'])

        item = CommonItem()
        enlace = 'https://www.boletinoficial.gob.ar/#!DetalleNorma/'
        item['url'] = enlace + data['idTramite'] + '/' + data['fechaPublicacion']
        item['fechahora'] = self.formateafecha(data['fechaPublicacion'])
        item['texto'] = self.limpiaetiquetas(data['detalleNorma'])
        return item
