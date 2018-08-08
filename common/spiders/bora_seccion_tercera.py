# -*- coding: utf-8 -*-

#  bora_seccion_tercera.py
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

class BoraSecTerceraSpider(scrapy.Spider):
    name = "bora_seccion_tercera"
    allowed_domains = ["boletinoficial.gob.ar"]
    start_urls = ()

    # Extrae el código para armar la url
    def formateaenlace(self, pdf):
        return pdf[:4] + pdf[4:6] + pdf[6:8]

    # Formato de fechahora tipo YYYY-MM-DD HH:MM:SS
    def formateafecha(self, fecha):
        return fecha[:4] + '-' + fecha[4:6] + '-' + fecha[6:8] + strftime(" %H:%M:%S")

    # Quita las etiquetas
    def limpiaetiquetas(self, item_texto):
        tag_re = re.compile(r'<[^>]+>')
        return tag_re.sub("", item_texto)

    # Solicita la tercera sección
    def start_requests(self):
        url = 'https://www.boletinoficial.gob.ar/secciones/secciones.json'
        payload = {'nombreSeccion': 'tercera', 'subCat': 'all',
                   'offset': 1, 'itemsPerPage': 500,
                   'fecha': strftime("%Y%m%d")}
        yield scrapy.Request(url, callback = self.parse_segunda,
             method = "POST",
             headers = {'X-Requested-With': 'XMLHttpRequest',
                      'Referer':'https://www.boletinoficial.gob.ar/',
                      'Accept': 'application/json, text/javascript, */*; q=0.01',
                      'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'},
             body = urllib.urlencode(payload))

    # Consulta cada una de las entradas
    def parse_segunda(self, response):
        data = json.loads(response.body)
        url = 'https://www.boletinoficial.gob.ar/norma/detalleTercera'
        for edict in data['dataList'][0]:
            payload = {'idDetalle': edict['idTramite']}
            yield scrapy.Request(url, callback = self.parse_items_segunda,
                 method = "POST",
                 headers = {'X-Requested-With': 'XMLHttpRequest',
                          'Referer':'https://www.boletinoficial.gob.ar/',
                          'Accept': 'application/json, text/javascript, */*; q=0.01',
                          'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'},
                 body = urllib.urlencode(payload), meta = {'id': edict['idTramite']})

    # Extrae la información de cada entrada y la almacena
    def parse_items_segunda(self, response):
        data = json.loads(response.body)['dataList']
        hxs = Selector(text = data['textoXHTML'])

        item = CommonItem()
        enlace = 'https://www.boletinoficial.gob.ar/#!DetalleTercera/'
        item['url'] = enlace + str(response.meta['id']) + '/' + self.formateaenlace(data['archivoPDF'])
        item['fechahora'] = self.formateafecha(data['fechaPublicacion'])
        item['texto'] = self.limpiaetiquetas(data['textoXHTML'])
        return item
