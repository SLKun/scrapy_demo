import re
import sys
import scrapy
import logging
from scrapy.crawler import CrawlerProcess

class UniversitySpider(scrapy.Spider):
    name = 'universityspider'
    start_urls = ['http://gaokao.chsi.com.cn/sch/search--ss-on,searchType-1,option-qg,start-0.dhtml']

    def __init__(self):
        self.primitive = open('primitive.log', 'a')
        self.check = open('check.log', 'a')
        self.warning = open('warning.log', 'a')
        self.error = open('error.log', 'a')

    def parse(self, response):
        for uni in response.xpath('//a[@title="点击查看院校信息"]'):
            yield response.follow(uni, self.content_parse)
        for next_page in response.xpath('//a[@href][contains(text(), "下一页")]'):
            yield response.follow(next_page, self.parse)

    def content_parse(self, response):
        title = response.xpath('//div[contains(@class, "topImg")]/text()').extract_first()
        for url in response.xpath('//div[span[contains(text(), "网址")]]/a/@href'):
            url = url.extract() 
            self.primitive.write('{"' + title + '": "' + url + '"},\n')
            yield scrapy.Request(url, self.final_parse, meta = {'title' : title})

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
        accept_tokens = ['大学', '学院', '学校']
        except_tokens = ['私服', '澳门', '转让', '活动', '赛车', '彩票', '代孕', '香港', '色图', '股票', '菲律宾', '娱乐', '域名', '黄页', '投注', '排行', '游戏', '折扣', '开奖']
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