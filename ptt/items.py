# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

# 定義資料類別（欄位）
class PostItem(scrapy.Item):
    authorId = scrapy.Field()
    authorName = scrapy.Field()
    title = scrapy.Field()
    publishedTime = scrapy.Field()
    content = scrapy.Field()
    canonicalUrl = scrapy.Field()
    createdTime = scrapy.Field()
    updateTime = scrapy.Field()
    comments = scrapy.Field()
    
