# -*- coding: utf-8 -*-

#  bora.py
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

from scrapy.crawler import CrawlerProcess
from scrapy.conf import settings
from scrapy.utils.project import get_project_settings
from common.spiders.bora_seccion_primera import BoraSecPrimeraSpider
from common.spiders.bora_seccion_segunda import BoraSecSegundaSpider
from common.spiders.bora_seccion_tercera import BoraSecTerceraSpider
from common.spiders.bora_seccion_cuarta import BoraSecCuartaSpider

# Lanza cada uno de los spiders
process = CrawlerProcess(get_project_settings())

process.crawl(BoraSecPrimeraSpider)
process.crawl(BoraSecSegundaSpider)
process.crawl(BoraSecTerceraSpider)
process.crawl(BoraSecCuartaSpider)
process.start()
