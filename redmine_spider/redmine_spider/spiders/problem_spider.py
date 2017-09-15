import scrapy
import helper.IterHelper


class ProblemSpider(scrapy.Spider):
    name = "problem"

    def start_requests(self):
        # prefer using cookie rather than login again
        if hasattr(self, "cookie"):
            # signed in
            url = 'https://redmine.csdc.info/redmine'
            yield scrapy.Request(url, self.check_login, cookies={'_redmine_session': self.cookie})
        elif hasattr(self, "username") and hasattr(self, "password"):
            # prepare signed in
            url = 'https://redmine.csdc.info/redmine/login'
            yield scrapy.Request(url, self.login)

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
        if 'login' in response.url: # dummy way to estimate
            print(response.status, response.url)
            if response.xpath('//div[@id="flash_error"]/text()').extract_first():
                print(response.xpath('//div[@id="flash_error"]/text()').extract_first())
            else:
                print("Invalid Cookie. Try to login with username and Password.")
                url = 'https://redmine.csdc.info/redmine/login'
                yield scrapy.Request(url, self.login)
        else:
            yield self.main_requests()

    def main_requests(self):
        urls = ['https://redmine.csdc.info/redmine/projects/smdb/issues']
        for url in urls:
            return scrapy.Request(url, self.parse)

    def parse(self, response):
        table = response.xpath('//table[thead][tbody]');
        table_content = []
        # parse table head
        table_head = []
        for head in table.xpath('./thead/tr[1]/th'):
            table_head.append(head.xpath('./a/text()').extract_first())
        table_content.append(table_head)
        # parse table body
        for line in table.xpath('./tbody/tr'):
            item_content = []
            for item in line.xpath('./td'):
                if item.xpath('./a'):
                    item_content.append(item.xpath('./a/text()').extract_first())
                elif item.xpath('./table'):
                    if item.xpath('./table/tr/td[@class="closed"]'):
                        progress = int(
                            item.xpath('./table/tr/td[@class="closed"]/@style').re(r'.*width: ([0-9]+)%.*')[0])
                        item_content.append(progress)
                    else:
                        progress = 100 - int(
                            item.xpath('./table/tr/td[@class="todo"]/@style').re(r'.*width: ([0-9]+)%.*')[0])
                        item_content.append(progress)
                else:
                    item_content.append(item.xpath('./text()').extract_first())
            yield self.issue_request(item_content[1], item_content)
            table_content.append(item_content)
        print(table_content)
        helper.IterHelper.print_beauty(table_content)
        return None

    def issue_request(self, issue_id, item_content):
        url = 'https://redmine.csdc.info/redmine/issues/' + issue_id
        request = scrapy.Request(url, self.issues_parse)
        request.meta["item_content"] = item_content
        return request

    def issues_parse(self, response):
        item_content = response.meta['item_content']
        description = response.xpath('//div[@class="wiki"][p]/p/text()').extract_first()
        for change in response.xpath('//div[@id="history"][div]/div[div[contains(@id, "journal")]]'):
            change_id = change.xpath('./@id').re(r'change-([0-9]+)')[0]
            change_person = change.xpath('./h4/a[3]/text()').extract_first()
            change_date = change.xpath('./h4/a[4]/@title').extract_first()
            change_content = change.xpath('./div[contains(@id, "journal")]/p/text()').extract_first()
            change = {}
            change['id'] = change_id
            change['person'] = change_person
            change['date'] = change_date
            change['content'] = change_content
            print(change)
        item_content.append(description)
        return None
