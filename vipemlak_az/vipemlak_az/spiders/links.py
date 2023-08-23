import scrapy
from urllib.parse import urljoin

class LinksSpider(scrapy.Spider):
    name = "links"
    allowed_domains = ["vipemlak.az"]
    start_urls = ["https://vipemlak.az/yeni-tikili"]

    def parse(self, response):
        # Extract links from the current page
        links = response.css('div.pranto.prodbig a::attr(href)').getall()

        # Yield the links on the current page
        yield {'href': links}

        # Extract and follow pagination links
        pagination_links = response.css('div.pagination a::attr(href)').getall()
        for link in pagination_links:
            full_link = urljoin(response.url, link)
            yield scrapy.Request(url=full_link, callback=self.parse)
