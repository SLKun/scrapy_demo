# api way of main
import sys
import logging
from electricity_spider.spiders.electricity_spider import ElectricitySpider
from scrapy.crawler import CrawlerProcess


def main(arg):
    process = CrawlerProcess({
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36',
        'LOG_LEVEL': logging.WARNING
    })
    process.crawl(ElectricitySpider, **arg)
    process.start()


if __name__ == '__main__':
    arg = {'cookie': 'test-cookie'}
    main(arg)

# cmdline of main
# set PATH=c:\App\Python\Python3.6\Scripts;C:\App\Git\bin;%PATH%
# set PATH=c:\App\Python\Python3.5\Scripts;C:\App\Git\bin;%PATH%
# export PATH=/d/DevelopmentTools/Python/Python3.5.4/Scripts:$PATH
# import sys
# from scrapy.cmdline import execute
#
# if __name__ == '__main__':
#     argv = sys.argv
#     argv[0] = 'scrapy'
#     print(argv)
#     sys.exit(execute(argv))

# import win10toast
#
# toast = win10toast.ToastNotifier()
# toast.show_toast("Running Python", "qwq")
