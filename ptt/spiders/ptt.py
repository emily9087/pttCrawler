import logging
from datetime import datetime
import time

import scrapy
from scrapy.http import FormRequest

from ptt import settings
from ptt.items import PostItem

class PTTSpider(scrapy.Spider):
    name = 'ptt'
    allowed_domains = ['ptt.cc']
    start_urls = ('https://www.ptt.cc/bbs/%s/index.html' % settings.BOARD_NAME,)

    # 針對「年齡是否滿18歲」之頁面，設定重試次數
    _retries = 0
    MAX_RETRY = 3

    # 設定擷取頁面的上限值
    _pages = 0
    MAX_PAGES = 200

    # 記錄爬取的貼文篇數
    # _post = 0

    def parse(self, response):
        if len(response.xpath('//div[@class="over18-notice"]')) > 0:
            # 有「年齡是否滿18歲」的頁面
            if self._retries < PTTSpider.MAX_RETRY:
                self._retries += 1
                logging.warning('retry {} times...'.format(self._retries))
                yield FormRequest.from_response(response,
                                                formdata={'yes': 'yes'},
                                                callback=self.parse)
            else:
                logging.warning('Over MAX_RETRY')

        else:
            # 記錄存取的頁面數量
            self._pages += 1
            for href in response.css('.r-ent > div.title > a::attr(href)'):
                url = response.urljoin(href.extract())
                yield scrapy.Request(url, callback=self.parse_post)

            if self._pages < PTTSpider.MAX_PAGES:
                # 往下一頁繼續撈取（在 ptt 頁面當中，顯示為「上頁」）
                next_page = response.xpath(
                    '//div[@id="action-bar-container"]//a[contains(text(), "上頁")]/@href')
                if next_page:
                    url = response.urljoin(next_page[0].extract())
                    logging.warning('follow {}'.format(url))
                    yield scrapy.Request(url, self.parse)
                else:
                    logging.warning('There is no next page')
            else:
                logging.warning('Max pages reached')

    def parse_post(self, response):
        # 解析貼文的資訊與內容
        try:
            item = PostItem()

            authorId = response.xpath('//div[@class="article-metaline"]/span[text()="作者"]/following-sibling::span[1]/text()')[0].extract().split(' ')[0]
            title = response.xpath('//meta[@property="og:title"]/@content')[0].extract()
            
            # 先檢查該貼文日期是否符合我們欲截取的日期區間中
            datetime_str = response.xpath('//div[@class="article-metaline"]/span[text()="時間"]/following-sibling::span[1]/text()')[0].extract()
            
            # datetime_str 格式範例：Sat Feb 29 11:52:22 2020
            # 貼文完整的 datetime（取名為 post_datetime，避免與 datetime() 撞名） 
            post_datetime = datetime.strptime(datetime_str, '%a %b %d %H:%M:%S %Y')

            print('%s %-14s %s' % (post_datetime, authorId, title))
            
            year = datetime_str.split(' ')[-1]
            month = datetime_str.split(' ')[1]
            day = datetime_str.split(' ')[2]

            # 貼文的日期（只有日期，沒有時間）
            date_str = f'{year}-{month}-{day}'
            date = post_datetime.strptime(date_str, '%Y-%b-%d') # 該貼文的日期（轉成 datetime 格式）
            start_date = post_datetime.strptime(settings.START_DATE, '%Y-%m-%d') # 日期區間的起始日期（轉成 datetime 格式）
            end_date = post_datetime.strptime(settings.END_DATE, '%Y-%m-%d') # 日期區間的終止日期（轉成 datetime 格式）

            print(f'本篇貼文日期：{date}', end='，')
            print(f'規範區間：{start_date}~{end_date}')

            # 比較時，僅以日期為比較準則，不納入時間
            if start_date <= date <= end_date:
                # 如果該貼文符合日期區間

                # 將資料依序輸入至 item 當中
                item['authorId'] = authorId
                name_beforeRegex = response.xpath('//div[@class="article-metaline"]/span[text()="作者"]/following-sibling::span[1]/text()')[0].extract().split(' ')
                name = ''.join(name_beforeRegex[1:])
                item['authorName'] = name[1:-1]
                item['title'] = title
                
                item['publishedTime'] = post_datetime.timestamp()
                content_elems = response.xpath(
                    '//div[@id="main-content"]'
                    '/text()['
                    'not(contains(@class, "push")) and '
                    'not(contains(@class, "article-metaline")) and '
                    'not(contains(@class, "f2"))'
                    ']')
                item['content'] = ''.join([c.extract() for c in content_elems])
                item['canonicalUrl'] = response.url
                item['createdTime'] = post_datetime
                item['updateTime'] = post_datetime

                # 解析回應
                comments = []
                for comment in response.xpath('//div[@class="push"]'):
                    push_user = comment.css('span.push-userid::text')[0].extract()
                    push_content = comment.css('span.push-content::text')[0].extract()
                    push_ipdatetime = comment.css('span.push-ipdatetime::text')[0].extract()
                    comment_date = push_ipdatetime.strip().split(' ')[1] # mm/dd
                    comment_time = push_ipdatetime.strip().split(' ')[2] # hh/mm
                    comment_month, comment_day = comment_date.split('/')
                    comment_hour, comment_minute = comment_time.split(':')
                    # 因為 ptt 網頁並沒有記載回應的「年份」，因此暫時以貼文的年份代替
                    comment_year = year
                    comment_datetime_str = f'{comment_year} {comment_month} {comment_day} {comment_hour}:{comment_minute}'
                    push_time = datetime.strptime(comment_datetime_str, '%Y %m %d %H:%M')

                    comments.append({'commentId': push_user,
                                    'commentContent': push_content,
                                    'commentTime': push_time})

                item['comments'] = comments

                # 記錄爬取的貼文數量
                # self._post += 1
                # logging.warning(f'已爬取 {self._post} 篇貼文\n')
                
                yield item
            else:
                # 該貼文不在日期區間內
                print(f'{post_datetime} is not in the date range. Please check settings.py\n')
                return
            
        except:
            return
