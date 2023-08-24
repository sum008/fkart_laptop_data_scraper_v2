import scrapy
from scrapy.exceptions import CloseSpider


class FkartScraper(scrapy.Spider):
    url = 'https://www.flipkart.com/search?q=laptops&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on' \
          '&as=off&page=1 '
    name = 'fkart_data_scraper'
    start_urls = [url]
    page_no = 1

    custom_settings = {
        'FEEDS': {'specs.jsonl': {'format': 'jsonlines', }}
    }

    def parse(self, response):
        if response.status == 404:
            raise CloseSpider('Receive 404 response')

        for link in response.xpath('//div[@class="_2kHMtA"]/a/@href'):
            yield response.follow(link.get(), callback=self.extract_info)
            self.page_no += 1
            next_page = f'https://www.flipkart.com/search?q=laptops&otracker=search&otracker1=search&marketplace' \
                        f'=FLIPKART&as-show=on&as=off&page={self.page_no} '
            yield response.follow(next_page, callback=self.parse)

    def extract_info(self, response):
        # //span[@class="B_NuCI"]
        price, off_percent, rating = [], [], []
        specs = response.xpath("//tr[@class='_1s_Smc row']//text()").extract()
        price = response.xpath(
            '//div[@class="_30jeq3 _16Jk6d"]//text()').extract()
        off_percent = response.xpath(
            '//div[@class="_3Ay6Sb _31Dcoz"]//text()').extract()
        rating = response.xpath('//div[@class="_3_L3jD"]//text()').extract()
        if len(rating) >= 1:
            rating = rating[0]
        else:
            rating = None
        if len(price) > 0:
            price = price[0]
        else:
            price = None
        if len(off_percent) > 0:
            off_percent = off_percent[0]
        else:
            off_percent = None
        specs.append("price")
        specs.append(price)
        specs.append("off_percentage")
        specs.append(off_percent)
        specs.append("rating")
        specs.append(rating)
        yield {"specs ": specs}
