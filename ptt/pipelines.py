import pymongo

from ptt import settings

class PTTPipeline(object):
    def process_item(self, item, spider):
        return item


class MongoPipeline(object):

    def __init__(self, mongo_uri, mongo_db):
        # 資料庫 URI 位址
        self.mongo_uri = mongo_uri
        # 資料庫名稱（ptt）
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABASE')
        )

    def open_spider(self, spider):
        # 資料庫的連結
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        # 資料庫的關閉
        self.client.close()

    def process_item(self, item, spider):
        # 透過 ptt 貼文網址，判斷該貼文是否已存在資料庫當中
        if self.db[settings.BOARD_NAME].find({'canonicalUrl':item['canonicalUrl']}).count() >= 1:
            print("Already in the database!")
        else:
            # 將該筆貼文存入資料庫當中，以「看板名稱」作為 collection 名稱
            self.db[settings.BOARD_NAME].insert(dict(item))
        
        return item
