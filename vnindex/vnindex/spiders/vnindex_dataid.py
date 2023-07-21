import os

import scrapy
import csv
import pandas as pd

from .. import settings


class VnIndexDetailSpider(scrapy.Spider):
    name = "vnindex_data_id"

    def start_requests(self):
        category_file_name = os.getcwd() + settings.VNINDEX_CATEGORY_FILE_NAME
        with open(category_file_name) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=",")
            next(csv_reader)
            for row_index, row_data in enumerate(csv_reader):
                yield scrapy.Request(
                    row_data[1],
                    callback=self.parse,
                    cb_kwargs=dict(row_index=row_index),
                )

    def parse(self, response, **kwargs):
        data_id = response.xpath('//*[@class="overflow-hidden daily_spot_price"]')[
            0
        ].attrib.get("data-id")
        category_file_name = os.getcwd() + settings.VNINDEX_CATEGORY_FILE_NAME
        df = pd.read_csv(category_file_name)
        df.at[int(kwargs.get("row_index")), "dataid"] = int(data_id)
        df.to_csv(category_file_name, index=False)
