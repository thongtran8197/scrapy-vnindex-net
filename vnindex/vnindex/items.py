# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field


class VnIndexCategoryItem(Item):
    name = Field()
    link = Field()


class VnIndexDataItem(Item):
    date = Field()
    price = Field()
    unit = Field()
    file_name = Field()
