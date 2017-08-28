import scrapy
import helper.IterHelper


class ElectricitySpider(scrapy.Spider):
    name = "electricity"
    data = {}

    def update_data(self, response):
        __EVENTTARGET = response.xpath('//input[@name="__EVENTTARGET"]/@value').extract_first()
        __EVENTARGUMENT = response.xpath('//input[@name="__EVENTARGUMENT"]/@value').extract_first()
        __LASTFOCUS = response.xpath('//input[@name="__LASTFOCUS"]/@value').extract_first()
        __VIEWSTATE = response.xpath('//input[@name="__VIEWSTATE"]/@value').extract_first()
        __EVENTVALIDATION = response.xpath('//input[@name="__EVENTVALIDATION"]/@value').extract_first()
        self.data['__EVENTTARGET'] = __EVENTTARGET
        self.data['__EVENTARGUMENT'] = __EVENTARGUMENT
        self.data['__LASTFOCUS'] = __LASTFOCUS
        self.data['__VIEWSTATE'] = __VIEWSTATE
        self.data['__EVENTVALIDATION'] = __EVENTVALIDATION


    def start_requests(self):
        self.url = "http://202.114.18.218/main.aspx"
        self.data = {}
        yield scrapy.Request(self.url, callback=self.choose_area)

    def choose_area(self, response):
        options = []
        for option in response.xpath('//select[@id="programId"]/option'):
            optionVal = option.xpath('./@value').extract_first()
            if not "-1" in optionVal:
                options.append(optionVal)
        print("Options: " + ",".join(options))

        self.update_data(response)
        self.data['__EVENTTARGET'] = 'programId'
        self.data['programId'] = '东区'
        yield scrapy.FormRequest(self.url, formdata=self.data, callback=self.choose_building)

    def choose_building(self, response):
        options = []
        for option in response.xpath('//select[@id="txtyq"]/option'):
            optionVal = option.xpath('./@value').extract_first()
            if not "-1" in optionVal:
                options.append(optionVal)
        print("Options: " + ",".join(options))

        self.update_data(response)
        self.data['__EVENTTARGET'] = 'txtyq'
        self.data['txtyq'] = '南二舍'
        yield scrapy.FormRequest(self.url, formdata=self.data, callback=self.choose_room)

    def choose_room(self, response):
        options = []
        for option in response.xpath('//select[@id="txtld"]/option'):
            optionVal = option.xpath('./@value').extract_first()
            if not "-1" in optionVal:
                options.append(optionVal)
        print("Options: " + ",".join(options))

        self.update_data(response)
        self.data['__EVENTTARGET'] = 'txtld'
        self.data['txtld'] = '4层'
        self.data['Txtroom'] = '401'
        yield scrapy.FormRequest(self.url, formdata=self.data, callback=self.fetch_result)

    def fetch_result(self, response):
        for option in response.xpath('//select[@id="txtyq"]/option'):
            if not "-1" in option.xpath('./@value').extract_first():
                print(option.xpath('./@value').extract_first())
