# Data Collection for Search Engine

## Tool and Technologies used

- Python 3.x
- Scrapy

## Web Scraping

For this Engine two types of data are required:

- Movies
- Articles

### Movies

- Movies data are scraped from **imdb** website
- Scrapy's **CrawlSpider** is used to scrape this website with scrape rules to follow next pages.
- IMDB has static results page so using the pagination links we navigate to the next page and so on till the end to scrape the data
- Data collected ranges from **1990 - 2021** with over _26,000_ titles
- Movie data has the following JSON structure

```json
{
  "title": "Aruvi",
  "rating": "8.5",
  "year": "2016",
  "certificate": "UA",
  "runtime": "2h 10min",
  "languages": ["Tamil"],
  "img_url": "https://m.media-amazon.com/images/aruvi.jpg",
  "actors": ["Aditi Balan", "Padmashri Mohammad Ali", "Pradeep Anthony", "..."],
  "genres": ["Drama"],
  "plot": "A gentle girl born and brought up amidst the ever growing eco-social-consumeristic environment ...",
  "directors": ["Arun Prabhu Purushothaman"],
  "imdb_url": "https://www.imdb.com/title/tt5867800/"
}
```

### Articles

- Articles are scraped from **indianexpress** and **thenewsminiute**

- Scrapy's **CrawlSpider** is used to scrape this website with scrape rules to follow next pages.

- Articles scraped from both the websited have the following JSON structure

```json
{
  "title": "Vicky Kaushal on shooting for Sardar Udham ...",
  "subtitle": "Vicky Kaushal speaks about playing ...",
  "date": "Updated: October 1, 2021  8:37:14 am",
  "link": "https://indianexpress.com/article/entertainment/bollywood/vicky-kaushal-sardar-udham-singh-injury-13-stiches-on-face-7544426/",
  "content": "Vicky Kaushal plays the revolutionary Sardar Udham Singh ... October 16 on Amazon Prime Video."
},
```

## To run this Datacollection module follow the steps below in a Shell

```bash
$ cd DataCollection/movie_data/movie_data/spiders
$ scrapy crawl movie_data -o movie_data.json
$ scrapy crawl the_news_minute -o newsminute_articles.json
$ scrapy crawl indian_express -o indian_express_articles.json
```
