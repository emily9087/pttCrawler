BOT_NAME = 'ptt'

# 設定「欲撈取的看板」
BOARD_NAME = 'Gossiping'

# 設定撈取區間
START_DATE = '2020-02-29'
END_DATE = '2020-03-01'

LOG_LEVEL = 'WARN'

SPIDER_MODULES = ['ptt.spiders']
NEWSPIDER_MODULE = 'ptt.spiders'

USER_AGENT = ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:73.0) Gecko/20100101 Firefox/73.0')

# Obey robots.txt rules
ROBOTSTXT_OBEY = True

# MongoDB Database 設定
MONGO_URI = 'localhost'
MONGO_DATABASE = 'ptt'

# Pipelines
ITEM_PIPELINES = {
   'ptt.pipelines.MongoPipeline': 300,
}

# Configure maximum concurrent requests performed by Scrapy (default: 16)
# CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See http://scrapy.readthedocs.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
DOWNLOAD_DELAY = 1.25
# The download delay setting will honor only one of:
CONCURRENT_REQUESTS_PER_DOMAIN = 16
CONCURRENT_REQUESTS_PER_IP = 16
