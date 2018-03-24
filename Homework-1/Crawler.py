import scrapy

class Crawler(scrapy.Spider):
	name = "mySpider"
	allowed_domains = ["https://finn.no"]
	start_urls = ['https://finn.no', "https://www.finn.no/bap/browse.html"]

	custom_settings = {
		'DOWNLOAD_DELAY' : 0.10
	}

	def parse(self, response):
		SET_SELECTOR = '//html'

		for brickset in response.xpath(SET_SELECTOR):

			NAME_SELECTOR = '//title/text()'# 'h1 a ::text'

			yield {
				'title': brickset.xpath(NAME_SELECTOR).extract_first()
			}

		NEXT_PAGE_SELECTOR = ' a ::attr(href)'
		next_page = response.css(NEXT_PAGE_SELECTOR).extract_first()

		#NEXT_PAGE_SELECTOR = 'a[contains(@href)]/@href'
		#next_page = response.xpath(NEXT_PAGE_SELECTOR).extract_first()

		if next_page:
			yield scrapy.Request(
				response.urljoin(next_page),
				callback=self.parse
			)
