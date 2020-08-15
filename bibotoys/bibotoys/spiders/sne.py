import scrapy


class ToysSpider(scrapy.Spider):
    name = "toys"

    def start_requests(self):
        urls = [
            'https://sneducare.or.kr/echild/html/sub/index.php?pno=02010102&page=2',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        self.log('Parse toy list')
        toylist = response.css('td.bold')
        for aToy in toylist:
            toy_detail = aToy.css('a::attr(href)').get()
            yield response.follow(toy_detail, callback=self.parse_toy_detail)
        pages = response.css('td.text_gray a::attr(href)').getall()
        for page in pages:
            yield response.follow(page, callback=self.parse)

        '''
        quotes = response.css('div.quote')
        for quote in quotes:
            yield {
                'text': quote.css('span.text::text').get(),
                'author': quote.css('.author::text').get(),
                'tags' : quote.css('.tag::text').getall(),
                    }
        '''

        '''
        nextpage = response.css('.next a::attr(href)').get()
        if nextpage is not None:
            yield response.follow(nextpage, callback=self.parse)
        '''

    def parse_toy_detail(self, response):
        self.log('=== Parse toy detail')
        attr_list = response.css('td.pdt2.bdb')
        self.log("Name %s" % attr_list[0].xpath('text()').get())
        self.log("Type %s" % attr_list[1].xpath('text()').get())
        self.log("Ages %s" % attr_list[2].xpath('text()').get())
        self.log("Lend times %s" % attr_list[5].xpath('text()').get())
                                                                      
