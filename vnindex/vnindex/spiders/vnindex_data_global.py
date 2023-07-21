import csv
import os

import scrapy

from .. import settings
import json
from ..items import VnIndexDataItem


class VnIndexDataGlobalSpider(scrapy.Spider):
    name = "vnindex_data_global"

    custom_settings = {
        "ITEM_PIPELINES": {"vnindex.pipelines.VnIndexDataGlobalSpiderPipeline": 1}
    }

    def start_requests(self):
        self.start_urls = self.get_start_urls()
        for start_url in self.start_urls:
            yield scrapy.Request(
                start_url.get("url"),
                callback=self.parse,
                errback=self.errback_httpbin,
                meta={"file_name": start_url.get("file_name")},
            )

    def parse(self, response):
        data = json.loads(response.text).get("series", [])
        if data:
            file_name = response.meta.get("file_name", "")
            unit = data[0].get("unit", "")
            price_by_date = data[0].get("data", {})
            for value in price_by_date:
                data_item = VnIndexDataItem(
                    date=value.get("date", ""),
                    price=value.get("y", ""),
                    unit=unit,
                    file_name=file_name,
                )
                yield data_item

    def get_start_urls(self) -> list:
        start_urls = []
        category_file_name = os.getcwd() + settings.VNINDEX_CATEGORY_FILE_NAME
        with open(category_file_name) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=",")
            next(csv_reader)
            for row_data in csv_reader:
                if "gia-hang-ngay" in row_data[1]:
                    file_name = (
                        row_data[1].split("/")[-2] + "_quoc-te_" + row_data[0] + ".csv"
                    )
                    start_urls.append(
                        dict(
                            url=f"https://vnindex.net/api/v1/chart?s={str(int(float(row_data[2])))}&span=max&ohlc=0",
                            file_name=file_name,
                        )
                    )
        return start_urls

    def errback_httpbin(self, failure):
        a = 1
