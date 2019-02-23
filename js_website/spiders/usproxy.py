# -*- coding: utf-8 -*-
import scrapy
from scrapy_splash import SplashRequest

class UsproxySpider(scrapy.Spider):
    name = 'usproxy'

    def start_request(self):
    	url = 'https://us-proxy.org/'
    	yield SplashRequest(url=url, callback=self.parse, endpoint='render.html', args={'wait': 0.5})
    
    def parse(self, response):
        # //tbody/tr[@role='row']/td[2]/text()
        for tr in response.xpath("//tbody/tr[@role='row']"):
        	print(tr.xpath(".//td[1]/text()").extract_first())
        	yield {
        		'ip': tr.xpath(".//td[1]/text()").extract_first(),
        		'port': tr.xpath(".//td[2]/text()").extract_first()
        	}
