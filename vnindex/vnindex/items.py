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


class VnBizItem(Item):
    date = Field()
    unit = Field()
    value = Field()
    file_name = Field()
    title = Field()


class FinnTradeItem(Item):
    date = Field()
    ticker = Field()
    value = Field()
    file_name = Field()


class StockPriceItem(Item):
    date = Field()
    ticker = Field()
    open = Field()
    close = Field()
    high = Field()
    low = Field()
    total_match_volume = Field()
    file_name = Field()
