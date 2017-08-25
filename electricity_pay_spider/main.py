# api way of main
# import logging
# from electricity_spider.spiders.problem_spider import ProblemSpider
# from scrapy.crawler import CrawlerProcess
#
#
# def main():
#     process = CrawlerProcess({
#         'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)',
#         'LOG_LEVEL': logging.WARNING
#     })
#     process.crawl(ProblemSpider)
#     process.start()
#
#
# if __name__ == '__main__':
#     main()

# cmdline of main
# set PATH=c:\App\Python\Python3.6\Scripts;%PATH%
import sys
import win10toast
# from scrapy.cmdline import execute

if __name__ == '__main__':
    argv = sys.argv
    argv[0] = 'scrapy'
    toast = win10toast.ToastNotifier()
    toast.show_toast("Running Python", " ".join(argv))
    # sys.exit(execute(argv))
