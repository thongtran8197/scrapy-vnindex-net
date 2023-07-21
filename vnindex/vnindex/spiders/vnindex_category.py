import scrapy

from .. import settings
from ..items import VnIndexCategoryItem


class VnIndexCategorySpider(scrapy.Spider):
    name = "vnindex_category"
    start_urls = ["https://vnindex.net/gia-hang-ngay"]

    custom_settings = {
        "FEEDS": {
            settings.VNINDEX_CATEGORY_FILE_NAME: {"format": "csv", "overwrite": True}
        },
        "FEED_EXPORT_FIELDS": ["name", "link", "dataid"],
    }

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url, self.parse)

    def parse(self, response):
        categories = response.xpath(
            '//*[@id="main-page-content"]/div/div/div/div/table/tbody/tr/td/a'
        )
        collected_links = []
        for category in categories:
            name = category.xpath("b/text()").get()
            link = category.attrib.get("href")
            if link not in collected_links:
                category_item = VnIndexCategoryItem(name=name, link=link)
                collected_links.append(link)
                yield category_item
