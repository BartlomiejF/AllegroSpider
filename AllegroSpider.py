import scrapy

#create result.txt file to gather information
f=open('result.txt','w')

class AllegroSpider(scrapy.Spider):
	name='AllegroSpider'
	
	def start_requests(self):
  #create list of urls that will be searched
		urls=['https://allegro.pl/kategoria/wh-40000-orks-45842'
		]
    
    #initiate counter
		self.i=0
    
		for url in urls:
			yield scrapy.Request(url=url, callback=self.parse)
	
	def parse(self, response):
		for article in response.xpath('//article[@class="_8d855a8"]'):
			self.i+=1
      
      #get auction name
			name=article.xpath('.//div[@class="a703fad"]/h2/a/text()').extract_first()
      
      #get link to auction
			path=article.xpath('.//div[@class="a703fad"]/h2/a/@href').extract_first()
      
      #get price the whole(first) and the rest(sec)
			price_first=int(article.xpath('.//span[@class="fee8042"]/text()').extract_first())
			price_sec=int(article.xpath('.//span[@class="_2b88aff"]/text()').extract_first())
      
      #write info to file
			f.write('{}. {} price: {},{} See page: {}\n'.format(self.i, name, price_first, price_sec, path))
    # get link to next page
		next_page=response.xpath('//a[@class="m-pagination__nav m-pagination__nav--next"]/@href').extract_first()
    
		if next_page is not None:
			next_page=response.urljoin(next_page)
      
      #enter next page and gather information
			yield scrapy.Request(url=next_page, callback=self.parse)
