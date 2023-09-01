# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import os

# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import csv


class VnindexPipeline:
    def process_item(self, item, spider):
        return item


class VnIndexDataGlobalSpiderPipeline:
    def process_item(self, item, spider):
        prefix_folder = "output/gia_hang_ngay/quoc_te/"
        filename = prefix_folder + item["file_name"]
        with open(filename, "a") as f:
            writer = csv.writer(f)
            row = [item["date"], item["price"], item["unit"]]
            writer.writerow(row)
        return item


class VnIndexDataChinaSpiderPipeline:
    def process_item(self, item, spider):
        prefix_folder = "output/gia_hang_ngay/trung_quoc/"
        filename = prefix_folder + item["file_name"]
        with open(filename, "a") as f:
            writer = csv.writer(f)
            row = [item["date"], item["price"]]
            writer.writerow(row)
        return item

class VnBizDataSpiderPipeline:
    def process_item(self, item, spider):
        headerList = ['date', 'price', 'unit', 'title']
        prefix_folder = "output/vnbiz/vi_mo_1/"
        filename = prefix_folder + item["file_name"] + ".csv"
        exists = os.path.exists(filename)
        with open(filename, "a") as f:
            writer = csv.writer(f)
            if not exists:
                dw = csv.DictWriter(f, delimiter=',', fieldnames=headerList)
                dw.writeheader()
            row = [item["date"], item["value"], item["unit"], item["title"]]
            writer.writerow(row)
        return item


class FinnTradeSpiderPipeline:
    def process_item(self, item, spider):
        header_list = ['date', 'ticker', 'value']
        prefix_folder = "output/finntrade/pe/"
        filename = prefix_folder + item["file_name"] + ".csv"
        exists = os.path.exists(filename)
        with open(filename, "a") as f:
            writer = csv.writer(f)
            if not exists:
                dw = csv.DictWriter(f, delimiter=',', fieldnames=header_list)
                dw.writeheader()
            row = [item["date"], item["ticker"], item["value"]]
            writer.writerow(row)
        return item

class StockPriceSpiderPipeline:
    def process_item(self, item, spider):
        header_list = ['date', 'ticker', 'open', 'close', 'high', 'low', "total_match_volume"]
        prefix_folder = "output/finntrade/price/"
        filename = prefix_folder + item["file_name"] + ".csv"
        exists = os.path.exists(filename)
        with open(filename, "a") as f:
            writer = csv.writer(f)
            if not exists:
                dw = csv.DictWriter(f, delimiter=',', fieldnames=header_list)
                dw.writeheader()
            row = [item["date"], item["ticker"], item["open"], item["close"], item["high"], item["low"], item['total_match_volume']]
            writer.writerow(row)
        return item