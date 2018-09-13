# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class Client(scrapy.Item):
    id = scrapy.Field()
    first_name = scrapy.Field()
    last_name = scrapy.Field()
    email = scrapy.Field()
