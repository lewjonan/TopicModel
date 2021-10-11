import re
import scrapy
import json
from functools import partial

from bilibiliarticle.items import BilibiliarticleItem


class BilibiliarticleSpider(scrapy.Spider):
    name = "bilibiliarticle"
    allowed_domains = ["bilibili.com"]
    # you can change different up by set uid here
    uid = 92334349
    pn = 1
    base_url = "https://api.bilibili.com/x/space/article?mid=%d&pn=%d&sort=publish_time"
    start_urls = [
        base_url % (uid, pn),
    ]

    def set_uid(self, uid):
        self.uid = uid

    def parse(self, response):
        article_list = json.loads(response.body)

        if "articles" not in article_list["data"].keys():
            return
        
        for article_info in article_list["data"]["articles"]:
            item = BilibiliarticleItem()
            item["id"] = int(article_info["id"])
            item["title"] = article_info["title"]
            item["url"] = "https://www.bilibili.com/read/cv%d" % item["id"]

            callback = partial(self.parse_article, item=item)

            yield scrapy.Request(item["url"], callback=callback)

        self.pn += 1

        yield scrapy.Request(self.base_url % (self.uid, self.pn), callback = self.parse)

    def parse_article(self, response, item):
        data = response.xpath("//div[@class='article-content']/div//p").extract()

        pattern = re.compile(r"\s|\n|<.*?>")
        clean_data = re.sub(pattern, "", "".join(data))

        item["text"] = clean_data

        return item

