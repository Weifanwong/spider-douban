import pymongo
import logging 
import scrapy 




conn=pymongo.MongoClient('127.0.0.1',27017)
db = conn.wwf_database01
myset = db.DouBan_topic

class DoubanPipeline(object):
    def process_item(self, item, spider):
    	myset.insert({'author':item['author'],'topic_from':item['topic_from'],
    		'title':item['title'],'content':item['content'],
    		'tags':item['tags'],'comment':item['comment'],
    		'nums_dz':item['nums_dz'],'nums_comment':item['nums_comment'],
    		'nums_intro':item['nums_intro']})

    	return item