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
        param = {
            'username': self.username,
            'password': self.password
        }
        return scrapy.FormRequest.from_response(
            response,
            formdata=param,
            callback=self.check_login
        )

    def check_login(self, response):
        # fail to login
        if 'login' in response.url:
            print(response.status, response.url)
            print(response.xpath('//div[@id="flash_error"]/text()').extract_first())
        else:
            yield self.main_requests()

    def parse(self, response):
        table = response.xpath('//table[thead][tbody]');
        # parse table head
        table_head = []
        for head in table.xpath('./thead/tr[1]/th'):
            table_head.append(head.xpath('./a/text()').extract_first())
        print(table_head)
        table_content = []
        for line in table.xpath('./tbody/tr'):
            item_content = []
            for item in line.xpath('./td'):
                if item.xpath('./a'):
                    item_content.append(item.xpath('./a/text()').extract_first())
                elif item.xpath('./table'):
                    if item.xpath('./table/tr/td[@class="closed"]'):
                        progress = int(item.xpath('./table/tr/td[@class="closed"]/@style').re(r'.*width: ([0-9]+)%.*')[0])
                        item_content.append(progress)
                    else:
                        progress = 100 - int(item.xpath('./table/tr/td[@class="todo"]/@style').re(r'.*width: ([0-9]+)%.*')[0])
                        item_content.append(progress)
                else:
                    item_content.append(item.xpath('./text()').extract_first())
            table_content.append(item_content)
            print(item_content)
        return None