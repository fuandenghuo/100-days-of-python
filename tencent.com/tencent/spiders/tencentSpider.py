# -*- coding: utf-8 -*-
import scrapy
from tencent.items import TencentItem
import re

class TencentspiderSpider(scrapy.Spider):
    name = 'tencent'
    allowed_domains = ["hr.tencent.com"]
    start_urls = ["http://hr.tencent.com/position.php?&start=0#a"]

    def parse(self, response):

        for each in response.xpath("//tr[@class='even']|//tr[@class='odd']"):

            item = TencentItem()
            name = each.xpath('./td[1]/a/text()').extract()[0]
            detailLink = each.xpath('./td[1]/a/@href').extract()[0]
            positionInfo = each.xpath('./td[2]/text()').extract()[0]
            peopleNumber = each.xpath('./td[3]/text()').extract()[0]
            workLocation = each.xpath('./td[4]/text()').extract()[0]
            publishTime = each.xpath('./td[5]/text()').extract()[0]

            print(name,detailLink,positionInfo,peopleNumber,workLocation,publishTime)

            item['name'] = name
            item['detailLink'] = "http://hr.tencent.com/" + detailLink
            item['positionInfo'] = positionInfo
            item['peopleNumber'] = peopleNumber
            item['workLocation'] = workLocation
            item['publishTime'] = publishTime

            curpage = re.search('(\d+)',response.url).group(1)
            page = int(curpage) + 10
            url = re.sub('\d+',str(page),response.url)

            yield  scrapy.Request(url,callback=self.parse)

            yield item