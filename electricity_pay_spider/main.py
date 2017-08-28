# api way of main
import logging
from electricity_spider.spiders.electricity_spider import ElectricitySpider
from scrapy.crawler import CrawlerProcess


def main():
    process = CrawlerProcess({
        'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)',
        'LOG_LEVEL': logging.WARNING
    })
    process.crawl(ElectricitySpider)
    process.start()


if __name__ == '__main__':
    main()

# cmdline of main
# set PATH=c:\App\Python\Python3.6\Scripts;C:\App\Git\bin;%PATH%
# set PATH=c:\App\Python\Python3.5\Scripts;C:\App\Git\bin;%PATH%
# import sys
#
# from scrapy.cmdline import execute
# if __name__ == '__main__':
#     argv = sys.argv
#     argv[0] = 'scrapy'
#     print(argv)
#     sys.exit(execute(argv))

# import win10toast
#
# toast = win10toast.ToastNotifier()
# toast.show_toast("Running Python", "qwq")
