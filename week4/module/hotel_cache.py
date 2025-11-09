import urllib.request as urlreq
import json

hotels_ch_url = "https://resources-wehelp-taiwan-b986132eca78c0b5eeb736fc03240c2ff8b7116.gitlab.io/hotels-ch"
hotels_en_url = "https://resources-wehelp-taiwan-b986132eca78c0b5eeb736fc03240c2ff8b7116.gitlab.io/hotels-en"
# 全域變數
ch_dict = {}
en_dict = {}

# 讀取網址中的資料
def load_url(url):
    with urlreq.urlopen(url) as response: # 這樣讀可以自動 close，比較安全
        return json.load(response) # 用 Json 模組處理 json 資料格式

# 更新資料
def update_cache():  
    # 抓全域變數
    global ch_dict, en_dict

    hlist_ch = load_url(hotels_ch_url)["list"]
    hlist_en = load_url(hotels_en_url)["list"]
    ch_dict = {h["_id"]: h for h in hlist_ch}
    en_dict = {h["_id"]: h for h in hlist_en}

update_cache()


