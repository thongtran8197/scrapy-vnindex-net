# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


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
        prefix_folder = "output/vnbiz/vi_mo/"
        filename = prefix_folder + item["file_name"]
        with open(filename, "a") as f:
            writer = csv.writer(f)
            row = [item["date"], item["value"], item["unit"]]
            writer.writerow(row)
        return item
