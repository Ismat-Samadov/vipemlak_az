import scrapy


class ContentSpider(scrapy.Spider):
    name = "content"
    allowed_domains = ["vipemlak.az"]
    start_urls = ["https://vipemlak.az/yaver-eliyev-kucesi-2595-ugur-2-yasayis-kompleksi-603888.html"]

    def parse(self, response):
        yield {
            'owner': response.css('div.infocontact::text').getall()[3],
            'phone_number': response.css('span#teldivid div#telshow::text').getall(),
        }
