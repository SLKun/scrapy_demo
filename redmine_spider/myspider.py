import scrapy

class BlogSpider(scrapy.Spider):
    name = 'blogspider'
    start_urls = ['http://www.sinoss.net/guanli/tzgg/qitatz/1.html']

    def start_requests():
    	

    def parse(self, response):
        for title in response.xpath('//div[@class="listCont"]/ul/li'):
            print(title.xpath('./p/a/text()').extract_first())
            yield {'title': title.xpath('./p/a/text()').extract_first()}

        for next_page in response.xpath('//div[@class="contLeft"]/a[3]/@href'):
            yield response.follow(next_page, self.parse)