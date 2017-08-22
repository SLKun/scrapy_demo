import scrapy


class ProblemSpider(scrapy.Spider):
    name = "problem"

    def start_requests(self):
        urls = ['https://redmine.csdc.info/redmine/login']
        for url in urls:
            yield scrapy.Request(url, self.login)

    def main_requests(self):
        urls = ['https://redmine.csdc.info/redmine/projects/smdb/issues']
        for url in urls:
            return scrapy.Request(url, self.parse)

    def login(self, response):
        return scrapy.FormRequest.from_response(
            response,
            formdata=self.param,
            callback=self.check_login
        )

    def check_login(self, response):
        # fail to login
        if('login' in response.url):
            print(response.status, response.url)
            print(response.xpath('//div[@id="flash_error"]/text()').extract_first())
        else:
            yield self.main_requests()

    def parse(self, response):
        table = response.xpath('//table[thead][tbody]');
        # parse table title
        for title in table.xpath('./thead/tr[1]/th'):
            print(title.xpath('./a/text()').extract_first())
        return None