# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText 
from subprocess import Popen, PIPE

me = "xxxxxxxxxxx@email.com"
you = "xxxxxxxxxxxxx@email.com"

from datetime import datetime
timeNow = str(datetime.now())

class StockxreleasecalendarV2Pipeline(object):
	def process_item(self, item, spider):
		with open('backup/release_calendar_{}_{}.txt'.format(timeNow[0:10], timeNow[11:19]), 'a') as f:
			f.write(item["single_product"])
			f.write('\n')
			f.close
		if 'profit' in item['single_product']:
			msg = MIMEText(item['single_product'])
			# Create message container - the correct MIME type is multipart/alternative.
			msg['Subject'] = "{}: {}".format(item['date'], item["title"][0])
			msg['From'] = me
			msg['To'] = you
			p = Popen(["/usr/sbin/sendmail", "-t", "-oi"], stdin=PIPE, universal_newlines=True)
			p.communicate(msg.as_string())
	
		return item


