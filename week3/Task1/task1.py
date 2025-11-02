import urllib.request as request
import json
import csv
import time

hotels_ch_url = "https://resources-wehelp-taiwan-b986132eca78c0b5eeb736fc03240c2ff8b7116.gitlab.io/hotels-ch"
hotels_en_url = "https://resources-wehelp-taiwan-b986132eca78c0b5eeb736fc03240c2ff8b7116.gitlab.io/hotels-en"

# 讀取網址中的資料
def load_url(url):
    with request.urlopen(url) as response: # 這樣讀可以自動 close，比較安全
        return json.load(response) # 用 Json 模組處理 json 資料格式

hlist_ch = load_url(hotels_ch_url)["list"] # 旅店中文list
hlist_en = load_url(hotels_en_url)["list"] # 旅店英文list

# 列出所有旅館到 hotels.csv，O(m*n)版本
def list_hotels1():
    # 創建或開啟 hotels.csv，會是文字檔物件
    with open("hotels.csv", "w", encoding="utf-8-sig", newline="") as file:  # utf-8-sig 避免 Excel 開啟讀錯編碼模式變亂碼
        writer = csv.writer(file) # 將file封裝成會處理csv格式的物件

        # 遍歷中文跟英文list，找id相同的兩筆資料，填寫所需項目到一列
        for h_ch in hlist_ch:
            for h_en in hlist_en:
                if h_ch["_id"] == h_en["_id"]:
                    # 寫完一列會自動換行，每筆資料中間會自動,，有,的資料外面加""
                    writer.writerow([
                        h_ch["旅宿名稱"],
                        h_en["hotel name"],
                        h_ch["地址"],
                        h_en["address"],
                        h_ch["電話或手機號碼"],
                        h_ch["房間數"]
                    ])
                    break

# 列出所有旅館到 hotels.csv，O(m+n)版本
def list_hotels2():
    # 先用 _id 為key設一個查找用的字典
    en_dict = {h["_id"]: h for h in hlist_en} # 字典生成式 {id1: {旅館資料1}, id2: {旅館資料2},...}
    with open("hotels.csv", "w", encoding="utf-8-sig", newline="") as file:
        writer = csv.writer(file)

        for h_ch in hlist_ch:
            # 直接用 key 找需要的en資料
            h_en = en_dict.get(h_ch["_id"]) # 找到key=h_ch["_id"]的value，沒有的話回傳 None
            if h_en:
                writer.writerow([
                        h_ch["旅宿名稱"],
                        h_en["hotel name"],
                        h_ch["地址"],
                        h_en["address"],
                        h_ch["電話或手機號碼"],
                        h_ch["房間數"]
                    ])

# 分類各區域旅館數及房間數
def group_hotels_by_district():
    districts = [] # 紀錄各區域總數 {"district": , "hotels": , "rooms": }
    # 遍歷每筆中文旅館資料
    for h in hlist_ch:
        # 找是否有"所在區域"的紀錄
        for d in districts:
            # "有"就疊加
            if d["district"] == h["地址"][3:6]:
                d["hotels"] += 1
                d["rooms"] += int(h["房間數"])
                break # 找到後直接跳出迴圈
        else:  # 全部找完都沒有就新增資料
            districts.append({"district": h["地址"][3:6], "hotels": 1, "rooms": int(h["房間數"])})
    
    # 創建或覆蓋 districts.csv
    with open("districts.csv", "w", encoding="utf-8-sig", newline="") as file:  # utf-8-sig 避免 Excel 開啟讀錯編碼模式變亂碼
        writer = csv.writer(file)
        # 寫入 districts 的每筆資料 value
        for d in districts:
            writer.writerow(list(d.values())) # list() 把所有 value 包成 list

# 呼叫函式
# a=time.perf_counter()
list_hotels2()
# b=time.perf_counter()
group_hotels_by_district()
# c=time.perf_counter()
# print(b-a)
# print(c-b)