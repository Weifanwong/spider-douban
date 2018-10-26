from douban.items import DoubanItem
import scrapy
from urllib.parse import urlencode
import urllib.request
import json


class DouBanSpider(scrapy.Spider):

	name = 'douban'
	def start_requests(self):
		#base_url = 'https://www.douban.com/gallery/'
		url = 'https://m.douban.com/rexxar/api/v2/gallery/hot_items?'
		param = {'ck':'null','count':20}
		for page in range(0,1):
			param['start'] = page * 20
			full_url = url + urlencode(param)

			headers = {
	'Accept': 'application/json, text/javascript, */*; q=0.01',
	'Accept-Encoding': 'gzip deflate br',
	'Accept-Language': 'zh-CN zh;q=0.8 en;q=0.8',
	'Connection': 'keep-alive',
	'Content-Type': 'application/x-www-form-urlencoded',
	'Cookie': 'bid=xJ55aenBWk8; gr_user_id=907dd229-4c03-470a-becd-8c9beab8a80d; _vwo_uuid_v2=DBC7EFF871EB072FE541212E6F890B661|f0af014940967be9220329bc43c6b6c7; ll="118371"; douban-fav-remind=1; __utmz=30149280.1539521166.25.24.utmcsr=blog.csdn.net|utmccn=(referral)|utmcmd=referral|utmcct=/lionel_fengj/article/details/72904843; viewed="26958126_26286154_20432061_2157831_4328644"; ps=y; as="https://www.douban.com/people/122310507/"; __utma=30149280.1986362691.1511832885.1539583156.1540306775.28; __utmc=30149280; ap_v=0,6.0; __utmt=1; __utmb=30149280.6.10.1540306775',
	'Host': 'm.douban.com',
	'Origin': 'https://www.douban.com',
	'Referer': 'https://www.douban.com/gallery/',
	'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.67 Safari/537.36',
	}

			req = urllib.request.Request(full_url,None,headers)
			response = urllib.request.urlopen(req) 
			the_page = response.read()	#取出来是byte类型
			data = json.loads(the_page) #用loads函数换成json类型
			for ele in data['items']:
				yield scrapy.Request(url = ele['target']['url'],callback=self.parse,
					meta={'nums_dz':ele['target']['likers_count'],
				'nums_intro':ele['target']['timeline_share_count'],
				'nums_comment':ele['target']['comments_count'],'topic_name':ele['topic']['name']})
				


	def parse(self,response):
		item = DoubanItem()
		title = response.xpath('//div[@class="note-header note-header-container"]/h1/text()').extract()
		author = response.xpath('//div[@class="note-header note-header-container"]/div/a[@class="note-author"]/text()').extract()
		content_body = ''.join(response.xpath('//div[@class="note"]//p/text()').extract())
		tags = response.xpath('//div[@class="mod-tags"]/a/text()').extract()
		comment_body = response.xpath('//div[@id="comments"]//div[@class="content report-comment"]/p/text()').extract()
		nums_dz = response.meta['nums_dz']
		nums_intro = response.meta['nums_intro']
		nums_comment = response.meta['nums_comment']
		topic_from = response.meta['topic_name']
		item['title'] = title
		item['author'] = author
		item['content'] = content_body
		item['tags'] = tags
		item['comment'] = comment_body
		item['nums_dz'] = nums_dz
		item['nums_comment'] = nums_comment
		item['nums_intro'] = nums_intro
		item['topic_from'] = topic_from
		#print(item['nums_comment'])
		yield item
		#print(type(item['comment']))


	# def parse_1(self,response):
	# 	content1 = response.xpath('//')



