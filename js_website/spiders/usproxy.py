# -*- coding: utf-8 -*-
import scrapy
from scrapy_splash import SplashRequest
from scrapy.selector import Selector

class UsproxySpider(scrapy.Spider):
    name = 'usproxy'

    script = """
function main(splash, args)
  assert(splash:go(args.url))
  assert(splash:wait(0.5))
  treat = require('treat')
  result = {}
  for i=1,9,1
  do
  assert(splash:runjs('document.querySelector("#proxylisttable_next a")'))
  result[i] = splash:html()
  end
  return treat.as_array(result)
  
end

    """

    def start_request(self):
    	url = 'https://us-proxy.org/'
    	yield SplashRequest(url=url, callback=self.parse, endpoint='render.html', args={'wait': 1})
    	yield SplashRequest(url=url, callback=self.parse_other_pages, endpoint='execute', args={'wait': 1, 'lua_source': self.script},
    		dont_filter=True)
    
    def parse(self, response):
        # //tbody/tr[@role='row']/td[2]/text()
        for tr in response.xpath("//tbody/tr[@role='row']"):
        	yield {
        		'ip': tr.xpath(".//td[1]/text()").extract_first(),
        		'port': tr.xpath(".//td[2]/text()").extract_first()
        	}

    def  parse_other_pages(self, response):
    	for page in response.data:
    		sel = Selector(text=page)
    		for tr in sel.xpath("//tbody/tr[@role='row']"):
        		yield {
        			'ip': tr.xpath(".//td[1]/text()").extract_first(),
        			'port': tr.xpath(".//td[2]/text()").extract_first()
        		}