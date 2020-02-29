# 【電獺面試】pttCrawler
電獺 Python 工程師招募筆試題目

## 使用到的套件
- Python 3.7
- Scrapy
- PyMongo
- MongoDB

## Python 環境設置
使用 Anaconda 建置一個名為 aotter 的虛擬環境，依據題目要求，Python 版本指定為 3.7：
```bash
conda create -n aotter python=3.7
```

進入虛擬環境，並安裝 `scrapy` 與 `pymongo`：
```bash
pip install scrapy
pip install pymongo
```

## MongoDB 安裝
使用 Homebrew 安裝 MongoDB，
安裝與啟用指令，請參考 [The MongoDB Homebrew Tap](https://github.com/mongodb/homebrew-brew)。

## 開發環境
- 作業系統：macOS Catalina 10.15.3
- 編輯器：VScode 1.42.1

程式寫完之後，將目錄設定好，並在終端機執行以下指令，便會開始從 ptt 頁面當中撈取資料，並存入 MongoDB：
```bash
scrapy crawl ptt
```
- 備註：最大上限為擷取 200 頁，如需手動停止，請於終端機按下 `Ctrl + C`。

## 參數設定
於 `settings.py` 檔案中，可以設定欲撈取之看板，以及設定撈取的日期區間：
```bash
# 設定「欲撈取的看板」
BOARD_NAME = 'Gossiping'

# 設定撈取區間
# 格式：Y-m-d
START_DATE = '2020-02-29'
END_DATE = '2020-03-01'
```

## Demo 影片
我有錄製一段一分鐘的 [Demo 影片](https://youtu.be/u_8_h_oSHsk)，呈現實際運作時的狀況，請參考。

## 參考資料
- [leVirve-arxiv / ptt-scrapy](https://github.com/leVirve-arxiv/ptt-scrapy)
- [Scraping Websites into MongoDB using Scrapy Pipelines](https://alysivji.github.io/mongodb-pipelines-in-scrapy.html)
- [比 Selenium 還強大的網路爬蟲：Scrapy 一本就精通](https://www.tenlong.com.tw/products/9789863796619)
