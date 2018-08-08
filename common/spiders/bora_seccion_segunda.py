# -*- coding: utf-8 -*-

#  bora_seccion_segunda.py
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

class BoraSecSegundaSpider(scrapy.Spider):
    name = "bora_seccion_segunda"
    allowed_domains = ["boletinoficial.gob.ar"]
    start_urls = ()

    # Formato de fechahora tipo YYYY-MM-DD HH:MM:SS
    def formateafecha(self, fecha):
        return fecha[:4] + '-' + fecha[4:6] + '-' + fecha[6:8] + strftime(" %H:%M:%S")

    # Quita las etiquetas
    def limpiaetiquetas(self, item_texto):
        tag_re = re.compile(r'<[^>]+>')
        return tag_re.sub("", item_texto)

    # Solicita la segunda sección
    def start_requests(self):
        url = 'https://www.boletinoficial.gob.ar/secciones/secciones.json'
        payload = {'nombreSeccion': 'segunda', 'subCat': 'all',
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
        url = 'https://www.boletinoficial.gob.ar/norma/detalleSegunda'
        for edict in data['dataList'][0]:
            payload = {'id': edict['id']}
            yield scrapy.Request(url, callback = self.parse_items_segunda,
                 method = "POST",
                 headers = {'X-Requested-With': 'XMLHttpRequest',
                          'Referer':'https://www.boletinoficial.gob.ar/',
                          'Accept': 'application/json, text/javascript, */*; q=0.01',
                          'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'},
                 body = urllib.urlencode(payload))

    # Extrae la información de cada entrada y la almacena
    def parse_items_segunda(self, response):
        data = json.loads(response.body)['dataList']
        hxs = Selector(text = data['textoCompleto'])

        item = CommonItem()
        enlace = 'https://www.boletinoficial.gob.ar/#!DetalleSegunda/'
        item['url'] = enlace + data['idTramite'] + '/' + data['fechaPublicacion']
        item['fechahora'] = self.formateafecha(data['fechaPublicacion'])
        item['texto'] = self.limpiaetiquetas(data['textoCompleto'])
        return item
