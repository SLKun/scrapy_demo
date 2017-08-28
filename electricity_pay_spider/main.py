# api way of main
import sys
import logging
from electricity_spider.spiders.electricity_spider import ElectricitySpider
from scrapy.crawler import CrawlerProcess


def main(arg):
    process = CrawlerProcess({
        'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)',
        'LOG_LEVEL': logging.WARNING
    })
    process.crawl(ElectricitySpider, **arg)
    process.start()


if __name__ == '__main__':
    arg = {'cookie': 'BAh7CCIMdXNlcl9pZGk7Ig9zZXNzaW9uX2lkIiU1NWU0YWI3MDE1OTZhMDgwMzBmNzVjODJjNTA3NzEyNiIQX2NzcmZfdG9rZW4iMTEvVElyRWxRWi9Tb25ScURaUThIYWVTSURXOWxWNVBuVzFaNmFuS0YyUHc9--c8b2eb677f716add656a6ec0e532d55f1848efc1'}
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
