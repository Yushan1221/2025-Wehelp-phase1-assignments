import urllib.request as request
import csv
import bs4
import re
from datetime import datetime
import os

# 讀取網址中的資料並解析
def get_data(url):
    # 建立 req 物件，附加 Request headers 資訊
    req = request.Request(url, headers={
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36 Edg/141.0.0.0"
    })

    # 讀取網址中的資料
    with request.urlopen(req) as response:
        data = response.read().decode("utf-8")
    # 用 beautifulSoup 解析抓到的網站
    root=bs4.BeautifulSoup(data, "html.parser")
    return root

# 爬 PPT網站的"標題","讚數","發帖時間"
def get_title_like_date(url):
    # 解析網址得到資料
    root = get_data(url)
    # 尋找所有 class="title" 的 div 標籤集成一個list
    titles = root.find_all("div", class_="title")
    # 所有標題的按讚數
    likes = root.find_all("div", class_="nrec")

    # 開一個"articles.csv"檔案，"a"是續寫模式
    with open("articles.csv", "a", encoding="utf-8-sig", newline="") as file:
        writer = csv.writer(file)

        for i, title in enumerate(titles):
            if title.a != None: # 如果標題包含 a 標籤(沒被刪除)
                # 如果有沒有顯示讚數，要換成""
                if likes[i].span != None:
                    like = likes[i].span.string
                else: like = ""

                # 找"發帖時間"
                href = title.a["href"] # 帖子連結
                title_url = "https://www.ptt.cc"+href # 完整帖子連結
                title_root = get_data(title_url) # 用get_data解析連結
                # 正則表達式的時間規則，因為有的帖子"分隔時間的空格"不一定只有一個，所以要寫\s+，避免抓不到
                pattern = re.compile(r"[A-Z][a-z]{2}\s+[A-Z][a-z]{2}\s+\d{1,2}\s+\d{2}:\d{2}:\d{2}\s+\d{4}")
                span_date = title_root.find("span", string=pattern) # 抓符合"時間格式規則"的span
                if span_date:
                    date = " ".join(span_date.string.split()) # 把多餘的空格去除(split去除所有空格，join再用" "連接所有字元)
                    dt = datetime.strptime(date, "%a %b %d %H:%M:%S %Y") # 再用strptime解析原本的時間字串成 datetime 物件
                    date = dt.strftime("%a %b %d %H:%M:%S %Y") # 重新格式化，因為有些資料是不會顯示兩位數日期，像是 Nov 1，格式化後就會顯示兩位數 Nov 01
                else: date = "" # 沒找到就替換成""

                # 一行寫入csv
                writer.writerow([
                    title.a.string,
                    like,
                    date
                ])

    # 抓上一頁連結
    last_page = root.find("a", string="‹ 上頁")
    return last_page["href"] # 並且回傳連結，達成多頁面迴圈

# 初始化先刪除既有檔案，以免續寫舊檔案
if os.path.exists("articles.csv"):
    os.remove("articles.csv")
# 要抓的連結
page_url = "https://www.ptt.cc/bbs/Steam/index.html"
# 迴圈三次 抓連結以及前兩頁
for i in range(3):
    page_url = "https://www.ptt.cc"+get_title_like_date(page_url)
