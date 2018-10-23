import scrapy
import logging
from scrapy.crawler import CrawlerProcess

class BlogSpider(scrapy.Spider):
    name = 'blogspider'
    base_url = 'https://www.sinoss.net/'
    # start_urls = ['http://www.sinoss.net/guanli/tzgg/qitatz/1.html']
    start_urls = ['https://www.sinoss.net/guanli/xmgl/tzgg/1.html']
    result = {}

    def parse(self, response):
        for title in response.xpath('//div[@class="listCont"]/ul/li'):
            # print(title.xpath('./p/a/text()').extract_first())
            # print(title.xpath('./p/a/@href').extract_first())
            url = title.xpath('./p/a/@href').extract_first()
            if url.endswith('html'):
                yield response.follow(url, self.content_parse)

        for next_page in response.xpath('//div[@class="contLeft"]/a[3]/@href'):
            print(next_page)
            yield response.follow(next_page, self.parse)

    def content_parse(self, response):
        full_title = ""
        for idx, val in enumerate(response.xpath('//h3/text()').extract()):
            full_title += val
            # print(str(idx) + ": " + val.strip())
        full_title = full_title.strip()
        url = response.url
        date = url.split("/")[3] + url.split("/")[4]
        compoundStr = full_title + ": " + url;
        self.result[compoundStr] = date;

    def close(self, reason):
        filterResult = dict(item for item in self.result.items() if "结项" in item[0])
        filterResult = sorted(filterResult.items(), key=lambda d:d[1], reverse=True)
        for compoundStr in filterResult:
            print(compoundStr)

def main():
    process = CrawlerProcess({
        'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)',
        'LOG_LEVEL': logging.WARNING
    })
    process.crawl(BlogSpider)
    process.start()

if __name__ == '__main__':
    main()