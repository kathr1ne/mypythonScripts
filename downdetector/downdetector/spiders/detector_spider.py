#!/usr/bin/env python
# -*- coding: utf-8 -*-
# karub1n@163.com

import scrapy

class DetectorSpider(scrapy.Spider):

    name = 'detector'
    start_urls = ['https://downdetector.com/']

    def parse(self, response):
        """get all urls"""
        with open('serviceName.conf', 'r') as f:
            service = f.readlines()
        for name in service:
            url = '{}status/{}'.format(self.start_urls[0], name.strip())
            request = scrapy.Request(url, callback=self.parse_img)
            yield request

    def parse_img(self, response):
        """get data, date & value"""
        res = response.xpath('//script/text()').re(r".*date: '(.*)', value: (\d) .*")
        yield {
            'url': response.url,
            'date': res[::2],
            'value': res[1::2]
        }