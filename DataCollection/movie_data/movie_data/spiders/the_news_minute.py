import re
from datetime import datetime
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class TheNewsMinuteSpider(CrawlSpider):
    name = "the_news_minute"
    allowed_domains = ["thenewsminute.com"]
    start_urls = ["https://www.thenewsminute.com/section/Flix?page=1"]

    rules = (
        Rule(
            LinkExtractor(restrict_xpaths=('//li[contains(@class, "pager-next")]//a')),
            callback="parse_results_page",
            follow=True,
        ),
    )

    def parse_results_page(self, response):
        article_links = response.xpath(
            '//div[contains(@class, "view-display-id-block_4")]//h3[@class="article-title"]//a//@href'
        ).extract()
        for link in article_links:
            yield response.follow(link, callback=self.parse_article)

    def parse_article(self, response):
        article = {}
        article["title"] = (
            response.xpath('//h1[contains(@class,"article-title")]//text()')
            .extract_first()
            .strip()
        )
        article["subtitle"] = (
            response.xpath('//p[contains(@class,"article-body")]//text()')
            .extract_first()
            .strip()
        )
        time_stamp = int(
            response.xpath('//span[contains(@class, "time")]//@data-create')
            .extract_first()
            .strip()
        )
        article["date"] = datetime.utcfromtimestamp(time_stamp).strftime(
            "%d-%m-%y %H:%M:%S"
        )
        article["link"] = response.url
        content = response.xpath(
            '..//div[contains(@class,"article-content article-body")]//text()'
        ).extract()
        content = re.sub(" +", " ", "".join(content).strip())
        content = re.sub("\t", " ", "".join(content).strip())
        article["content"] = content

        yield article
