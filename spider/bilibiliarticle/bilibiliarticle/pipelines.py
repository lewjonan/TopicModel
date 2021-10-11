# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import os
import os.path as osp

# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class BilibiliarticlePipeline:
    def __init__(self):
        self.output_dir = "../../data/bilibiliarticle/"
        if not osp.exists(self.output_dir):
            os.makedirs(self.output_dir)

    def process_item(self, item, spider):
        fp = osp.join(self.output_dir, "%d.txt" % item["id"])
        with open(fp, "w", encoding="utf-8") as f:
            f.write(item["text"])
            
        return item
