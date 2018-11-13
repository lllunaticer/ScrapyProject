# -*- coding: utf-8 -*-

import scrapy
from doubanmovie.items import DoubanmovieItem


class DoubanMovie(scrapy.Spider):
    name = 'doubanMovie'
    allowed_domain = ['movie.douban.com']
    start_urls = ['https://movie.douban.com/top250']

    def parse(self, response):
        selector = scrapy.Selector(response)
        # 解析电影信息所在目录
        movies = selector.xpath('//div[@class="item"]')
        # 存放电影信息
        item = DoubanmovieItem()

        for movie in movies:
            titles = movie.xpath('.//span[@class="title"]/text()').extract()
            name = ''
            for title in titles:
                name += title.strip()
            item['name'] = name

            infos = movie.xpath('.//div[@class="bd"]/p/text()').extract()
            fullInfo = ''
            for info in infos:
                fullInfo += info.strip()
            item['info'] = fullInfo

            item['rating'] = movie.xpath('.//span[@class="rating_num"]/text()').extract()[0].strip()
            item['num'] = movie.xpath('.//div[@class="star"]/span[last()]/text()').extract()[0].strip()[:-3]

            quote = movie.xpath('.//span[@class="inq"]/text()').extract()
            if quote:
                quote = quote[0].strip()
            else:
                quote = ' '
            item['quote'] = quote

            item['img_url'] = movie.xpath('.//img/@src').extract()[0]

            yield item

            next_page = selector.xpath('//span[@class="next"]/a/@href').extract_first()
            if next_page:
                url = 'https://movie.douban.com/top250' + next_page
                yield scrapy.Request(url, callback=self.parse)










