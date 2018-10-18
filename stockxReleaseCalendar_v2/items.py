# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class StockxreleasecalendarV2Item(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
	title = scrapy.Field()
	link = scrapy.Field()
	month = scrapy.Field()
	day = scrapy.Field()
	date = scrapy.Field()
	lowestAsk = scrapy.Field()
	highestBid = scrapy.Field()
	single_product = scrapy.Field()
