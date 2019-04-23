import scrapy
import helper.IterHelper


class ElectricitySpider(scrapy.Spider):
    name = "electricity"

    def fetch_option(self, response):
        # check selected options
        option_list = []
        levels = {0: 'programId', 1: 'txtyq'}
        for level in levels.values():
            xpath_str = '//select[@id="' + level + '"]/option[@selected]/@value'
            result = response.xpath(xpath_str).extract_first()
            if result and result != "-1":
                option_list.append(result)

        # decide the level of options to print
        options = []
        if len(option_list) < len(levels):
            for option in response.xpath('//select[@id="' + levels[len(option_list)] + '"]/option'):
                option_val = option.xpath('./@value').extract_first()
                if "-1" not in option_val:
                    options.append(option_val)

            # print options
            print("_".join(option_list) + " Options: " + ",".join(options))
            return options

    def fetch_data(self, response):
        data = {}

        # Data from input area
        input_list = ['__EVENTTARGET', '__EVENTARGUMENT', '__LASTFOCUS', '__VIEWSTATE', '__EVENTVALIDATION', 'Txtroom',
                      'Txtroom', 'TextBox2', 'TextBox3']
        for input in input_list:
            input_xpath = '//input[@name="' + input + '"]/@value'
            result = response.xpath(input_xpath).extract_first()
            if result:
                data[input] = result
            else:
                data[input] = ''

        # Data from select area
        select_list = ['programId', 'txtyq']
        for select in select_list:
            select_xpath = '//select[@id="' + select + '"]/option[@selected]/@value'
            result = response.xpath(select_xpath).extract_first()
            if result and result != "-1":
                data[select] = result

        # Fixed Data
        data['ImageButton1.x'] = '31'
        data['ImageButton1.y'] = '15'
        return data

    def start_requests(self):
        self.url = "http://202.114.18.218/main.aspx"
        self.param = {
            'programId': "东区",
            'txtyq': "南1舍",
            'Txtroom': "233",
        }
        yield scrapy.Request(self.url, callback=self.choose_requests)

    def choose_requests(self, response):
        data = self.fetch_data(response)
        levels = ['programId', 'txtyq']
        for level in levels:
            if level not in data.keys():
                data[level] = self.param[level]
                yield scrapy.FormRequest(self.url, formdata=data, callback=self.choose_requests)
                return
        data['Txtroom'] = self.param['Txtroom']
        yield scrapy.FormRequest(self.url, formdata=data, callback=self.fetch_result)

    def fetch_result(self, response):
        for column in response.xpath('//table[@id="GridView2"]/tr[td]'):
            time = column.xpath('./td[2]/text()').re(r'20([0-9-]*) .*')[0]
            data = column.xpath('./td[1]/text()').extract_first()
            print(time + ": " + data)
