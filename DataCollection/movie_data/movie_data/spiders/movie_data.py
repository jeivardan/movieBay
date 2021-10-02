from scrapy import linkextractors
from scrapy.spiders import CrawlSpider, Rule


class MovieDataSpider(CrawlSpider):
    name = "movies"
    allowed_domains = ["www.imdb.com"]
    start_urls = [
        "https://www.imdb.com/search/title/?title_type=feature&release_date=1990-01-01,2021-08-01&countries=in&count=250&view=simple"
    ]

    rules = (
        Rule(
            linkextractors.LinkExtractor(restrict_xpaths=("//div[@class='desc']//a")),
            follow=True,
            callback="parse_search_results_page",
        ),
    )

    def parse_search_results_page(self, response):
        movie_links = response.xpath(
            '//span[@class="lister-item-header"]//a//@href'
        ).extract()
        for link in movie_links:
            yield response.follow(link, callback=self.parse_movie_details_page)

    def parse_movie_details_page(self, response):
        data = {}
        data["title"] = response.css("h1::text").extract_first().strip()
        data["rating"] = (
            response.xpath(
                '//span[@class="AggregateRatingButton__RatingScore-sc-1ll29m0-1 iTLWoV"]//text()'
            ).extract_first()
            # .strip()
        )

        data["year"] = (
            response.xpath(
                '//div[@class="TitleBlock__TitleMetaDataContainer-sc-1nlhx7j-2 hWHMKr"]//ul//li[1]//span//text()'
            ).extract_first()
            # .strip()
        )
        data["certificate"] = (
            response.xpath(
                '//div[@class="TitleBlock__TitleMetaDataContainer-sc-1nlhx7j-2 hWHMKr"]//ul//li[2]//span//text()'
            ).extract_first()
            # .strip()
        )
        data["runtime"] = (
            response.xpath(
                '//li[contains(@data-testid,"title-techspec_runtime")]//div//ul//li//span//text()'
            ).extract_first()
            # .strip()
        )
        data["languages"] = response.xpath(
            '//li[contains(@data-testid,"title-details-languages")]//div/ul//li//a//text()'
        ).extract()
        data["img_url"] = response.xpath(
            '//div[contains(@class, "ipc-media--poster")]/img/@src'
        ).extract_first()
        actors = response.xpath(
            '//a[@class="StyledComponents__ActorName-y9ygcu-1 eyqFnv"]//text()'
        ).extract()
        data["actors"] = [actor.strip() for actor in actors]
        data["genres"] = response.xpath(
            '//li[contains(@data-testid,"storyline-genres")]//div//ul//li//a//text()'
        ).extract()
        data["plot"] = (
            response.xpath(
                '//p[contains(@data-testid, "plot")]//span[1]//text()'
            ).extract_first()
            # .strip()
        )
        data["directors"] = (
            response.xpath(
                '//div[contains(@class, "ExpandablePrincipalCreditsPanel__PrincipalCredits-krzxv6-1")]//ul//li[1]//div//ul//li//a//text()'
            ).extract()
            or None
        )
        data["imdb_url"] = response.url.replace("?ref_=adv_li_tt", "")
        # data["Storyline"] = (
        #     response.xpath(
        #         '//div[contains(@data-testid,"storyline-plot-summary")]//div//div//text()'
        #     )
        #     .extract_first()
        #     .strip()
        # )
        yield data
