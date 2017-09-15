import re
import sys
import scrapy
import logging
from scrapy.crawler import CrawlerProcess

class UniversitySpider(scrapy.Spider):
    name = 'universityspider'
    start_urls = ['http://m.unjs.com/']

    def __init__(self):
        self.check = open('check.log', 'a')
        self.warning = open('warning.log', 'a')
        self.error = open('error.log', 'a')

    def parse(self, response):
        nav = response.xpath('//nav')[0]
        for province in nav.xpath('./a'):
            if 'daxue' in province.xpath('./@href').extract_first():
                yield response.follow(province.xpath('./@href').extract_first(), self.content_parse)

    def content_parse(self, response):
        for item in response.xpath('//div[contains(@class, "title")]/a'):
             title = item.xpath('./text()').extract_first()
             url = item.xpath('./@href').extract_first()
             yield scrapy.Request(url, self.js_parse, meta = {'title' : title})

        for next_page in response.xpath('//a[@href][contains(text(), "下一页")]'):
            if(len(next_page.xpath('./@href').extract_first()) != 0):
                yield response.follow(next_page, self.content_parse, meta = response.meta)

    def js_parse(self, response):
        url = response.xpath('//script/text()').re(r'window.location.href=\'(.*)\';')[0]
        if('baidu' not in url):
            yield scrapy.Request(url, self.final_parse, meta = response.meta)

    def final_parse(self, response):
        # fetch title and url
        wrapped_title = response.meta['title']
        title = response.xpath('//title/text()').extract_first()
        url = response.url
        if(title):
            title = title.strip()
        else:
            title = ""

        # filter unexcepted url
        accept_tokens = ['大学', '学院']
        except_tokens = ['私服', '澳门', '转让', '活动', '赛车', '彩票', '代孕']
        for except_token in except_tokens:
            if except_token in title:
                self.error.write('{"' + wrapped_title + '": {"' + title + '": "' + url + '"}},\n')
                return
        for accept_token in accept_tokens:
            if accept_token in title and wrapped_title in title:
                yield {
                    wrapped_title: url 
                }
                return
        if len(str(response.body)) < 1000 or title == "":
            self.warning.write('{"' + wrapped_title + '": {"' + title + '": "' + url + '"}},\n')
        else:
            self.check.write('{"' + wrapped_title + '": {"' + title + '": "' + url + '"}},\n')

    def close(self, reason):
        self.check.close()
        self.warning.close()
        self.error.close()

def main():
    result_file_name = 'result.json'
    if len(sys.argv) > 1 and sys.argv[1]:
        result_file_name = sys.argv[1]
    process = CrawlerProcess({
        # 'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)',
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
        'LOG_LEVEL': logging.WARNING,
        'FEED_FORMAT': 'json',
        'FEED_URI': result_file_name,
        'FEED_EXPORT_ENCODING': 'utf-8'
    })
    process.crawl(UniversitySpider)
    process.start()

if __name__ == '__main__':
    main()