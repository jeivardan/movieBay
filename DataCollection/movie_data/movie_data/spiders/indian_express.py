import re
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class IndianExpressSpider(CrawlSpider):
    name = "indian_express"
    allowed_domains = ["indianexpress.com"]
    start_urls = ["https://indianexpress.com/section/entertainment/page/2/"]

    rules = (
        Rule(
            LinkExtractor(
                restrict_xpaths=('//a[contains(@class,"next page-numbers")]')
            ),
            callback="parse_results_page",
            follow=True,
        ),
    )

    def parse_results_page(self, response):
        article_links = response.xpath(
            '//div[contains(@class, "title")]//a//@href'
        ).extract()
        for link in article_links:
            yield response.follow(link, callback=self.parse_article)

    def parse_article(self, response):
        article = {}
        article["title"] = (
            response.xpath('//h1[contains(@class, "native_story_title")]//text()')
            .extract_first()
            .strip()
        )
        article["subtitle"] = (
            response.xpath('//h2[contains(@class, "synopsis")]//text()')
            .extract_first()
            .strip()
        )
        article["date"] = (
            response.xpath('//div[contains(@class, "editor")]//span//text()')
            .extract_first()
            .strip()
        )
        article["link"] = response.url
        content = response.xpath('//div[@id="pcl-full-content"]//p//text()').extract()
        content = re.sub(" +", " ", "".join(content).strip())
        content = re.sub("\t", " ", "".join(content).strip())
        article["content"] = content

        yield article
