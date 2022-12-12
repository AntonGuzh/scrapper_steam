# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class Game(scrapy.Item):
    name = scrapy.Field()
    category = scrapy.Field()
    review_count = scrapy.Field()
    review_grade = scrapy.Field()
    created_at = scrapy.Field()
    developer = scrapy.Field()
    distributor = scrapy.Field()
    tags = scrapy.Field()
    cost = scrapy.Field()
    cost_with_discount = scrapy.Field()
    platforms = scrapy.Field()
