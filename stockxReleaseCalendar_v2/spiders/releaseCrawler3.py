import scrapy
from stockxReleaseCalendar_v2.items import StockxreleasecalendarV2Item
import json

class MyCrawler3(scrapy.spiders.Spider):
	name = "releasecrawler3"
	allowed_domains = ["stockx.com"]
	start_urls = ["https://stockx.com/new-releases/sneakers"]	

	def parse(self, response):
		hxs = scrapy.Selector(response)
		titles = hxs.xpath('''//*[@id="release-wrapper"]/div[2]/div/div[2]/div[1]/div[2]/a''')
		#print(titles)
		items = []
		sizes_notification = []
		for title_items in titles:
			#print(title_items)
			item = StockxreleasecalendarV2Item()
			item ["title"] = title_items.xpath("@id").extract()
			item ["link"] = "http://stockx.com" + title_items.xpath("@href").extract()[0]
			item['month'] = title_items.xpath("div/div[1]/div[1]/span/span/text()[1]").extract()
			item['day'] = title_items.xpath("div/div[1]/div[1]/span/span/text()[2]").extract()
			item ["lowestAsk"] = title_items.xpath("div/div[4]/div/div[1]/span[1]/text()").extract()
			item ["highestBid"] = title_items.xpath("div/div[4]/div/div[1]/span[3]/text()").extract()
			#print(item)
			items.append(item)
			request = scrapy.Request(item["link"], callback=self.parseProductDetails)
			request.meta['item'] = item
			yield request
			#print(item)

	def parseProductDetails(self, response):
		item = response.meta['item']
		single_product = []
		stockx_sizes = []	
		for response_script in response.xpath('//script[@type="text/javascript"]/text()').extract():
			if 'window.preLoaded' in response_script:
				response_text_tmp = response_script.replace("window.preLoaded =", "")
				response_text = response_text_tmp.replace(";", "")
				data = json.loads(response_text)
				#print(response_json)
				style_id = data['product']['styleId']
				release_date = data['product']['releaseDate']
				item['date'] = release_date
				single_product.append("{} {} release date is {}".format(item["title"][0], style_id, release_date))
				single_product.append(item["link"])
				#print("{} {} release date is {}".format(item["title"][0], style_id, release_date))
				if 'retailPrice' in data['product'].keys(): 
					retailPrice = data['product']['retailPrice']
					taxedRetail = round(retailPrice * 1.07, 2)
					single_product.append("The retail price is ${} while taxed price is ${}".format(retailPrice, taxedRetail))
					#print("{} {} retail price is ${} while taxed price is ${}".format(item["title"][0], style_id, retailPrice, taxedRetail))
					data_children = data['product']['children']
					for child in data_children.keys():
						bid_size = data_children[child]['market']['highestBidSize']
						highest_bid = data_children[child]['market']['highestBid']
						resell_gain = round(highest_bid * 0.88, 2)
						if bid_size and (resell_gain > taxedRetail + 30):
							stockx_sizes.append(bid_size)
							resell_profit = round(resell_gain - taxedRetail, 2)
							single_product.append("Size {} highest bid is ${} while resell gain is ${} and resell profit is {}".format(bid_size, highest_bid, resell_gain, resell_profit))	
							#print("{} {} size {} highest bid is ${} while resell gain is ${} and resell profit is {}".format(item["title"][0], style_id, bid_size, highest_bid, resell_gain, resell_profit))	
				stockx_sizes.sort()				
				stockx_sizes_string = 'Profitable sizes include: ' + ' '.join(stockx_sizes)
				single_product.append(stockx_sizes_string)
				single_product.append("=============================")
		item['single_product'] = '\n'.join(single_product)
		#print(item['single_product'])
		return item
