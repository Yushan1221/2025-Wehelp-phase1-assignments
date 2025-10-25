import re
#region Task1
def func1(name): 
    points = [{"name": "辛巴", "x": -3, "y": 3, "side": "L"},
        {"name": "貝吉塔", "x": -4, "y": -1, "side": "L"},
        {"name": "悟空", "x": 0, "y": 0, "side": "L"},
        {"name": "特南克斯", "x": 1, "y": -2, "side": "L"},
        {"name": "丁滿", "x": -1, "y": 4, "side": "R"},
        {"name": "弗利沙", "x": 4, "y": -1, "side": "R"}]
    
    # 指派 target 的資料
    target = None
    for point in points:  # 用name找對應字典
        if point["name"] == name:
            target = point
            break
    if target is None:
        return print("抱歉，無此角色。")
    
    # 初始最短、最長 distance 與 point
    shortestPoint = []
    longestPoint = []
    shortestDist = 10000
    longestDist = -1
    # 遍歷 points 算最大最小距離
    for point in points:
        # 排除 target 本身
        if point != target:
            # 計算距離
            distance = abs(point["x"] - target["x"]) + abs(point["y"] - target["y"])
            if point["side"] != target["side"]:
                distance += 2

            # 比較最短距離
            if distance < shortestDist:
                shortestPoint.clear() # 清空 list
                shortestPoint.append(point["name"])
                shortestDist = distance
            elif distance == shortestDist:
                shortestPoint.append(point["name"])

            # 比較最長距離
            if distance > longestDist:
                longestPoint.clear() # 清空 list
                longestPoint.append(point["name"])
                longestDist = distance
            elif distance == longestDist:
                longestPoint.append(point["name"])
    
    # python 中 .join() 是 string 的 methods
    return print("最遠" + "、".join(longestPoint) + ";最近" + "、".join(shortestPoint))


func1("辛巴")  # print 最遠弗利沙；最近丁滿、⾙吉塔
func1("悟空")  # print 最遠丁滿、弗利沙；最近特南克斯
func1("弗利沙")  # print 最遠⾟巴，最近特南克斯
func1("特南克斯")  # print 最遠丁滿，最近悟空

#endregion

print("=====================================")

#region Task2
bookings = [] # 已預約的時段 [{start: xx, end: xx, service: xx}]
def func2(ss, start, end, criteria): 
    # 用正則表達式區分criteria中的 key、operations、value
    match = re.match(r"^\s*(r|c|name)\s*(>=|<=|=)\s*(.+)\s*$", criteria)
    if match:
        key, operations, value = match.groups()
        # python 不會自動轉型，所以要先轉成數字型態，已利之後比大小
        if key in ("r", "c"):
            value = float(value) if "." in value else int(value) # 三元運算子: A(true) if 條件 else B(false)
    else: 
        return print("條件式不符合規則。")
    
    # 查詢特定服務是否有時段可預約
    def canBooking(service):
        # 篩選特定服務的已預約時段
        serviceBooking = [b for b in bookings if b["service"] == service] # 列表生成式 -> 可以下條件篩選element並建立new list
        for b in serviceBooking:
            # 判斷時段是否重疊
            if b["start"] < end and b["end"] > start:
                return False
        return True
    
    # 開始判斷條件
    if key == "name":
        # 檢查時段是否可預約
        if canBooking(value):
            # 紀錄本次預約時間及服務
            bookings.append({"start": start, "end": end, "service": value})
            return print(value)          
    elif key in ("r", "c"):
        # 篩選符合條件的服務(分<=、>=)
        if operations == "<=":
            availableServices = [s for s in ss if s[key] <= value]
        elif operations == ">=":
            availableServices = [s for s in ss if s[key] >= value]

        # 依照"各服務數值"與"條件數值"接近程度排序 .sort(key= 函式)
        availableServices.sort(key= lambda s: abs(s[key] - value))

        # 檢查"符合條件的服務"是否有時段可預約
        for s in availableServices:
            if canBooking(s["name"]):
                # 紀錄本次預約時間及服務
                bookings.append({"start": start, "end": end, "service": s["name"]})
                return print(s["name"])
    
    return print("sorry")

services=[ 
{"name":"S1", "r":4.5, "c":1000}, 
{"name":"S2", "r":3, "c":1200}, 
{"name":"S3", "r":3.8, "c":800} 
] 
func2(services, 15, 17, "c>=800")  # S3 
func2(services, 11, 13, "r<=4")  # S3 
func2(services, 10, 12, "name=S3")  # Sorry 
func2(services, 15, 18, "r>=4.5")  # S1 
func2(services, 16, 18, "r>=4")  # Sorry 
func2(services, 13, 17, "name=S1")  # Sorry 
func2(services, 8, 9, "c<=1500")  # S2
#endregion

print("=====================================")

#region Task3
def func3(index): 
    if type(index) != int or index <= 0:
        return print("不符合格式。")
    number = 25 # 初始數字
    patterns = [-2, -3, +1, +2] # 序列規律

    # 首項 + (一次循環總和 * 幾次循環) + (剩下不足循環的部分)
    element = number + sum(patterns) * (index // 4) + sum(patterns[0: index % 4])

    return print(element);

func3(1)  # print 23 
func3(5)  # print 21 
func3(10)  # print 16 
func3(30)  # print 6
#endregion

print("=====================================")

#region Task4
def func4(sp, stat, n): 
    bestSpaces = None  # 紀錄"最佳"車廂位置數
    bestSpacesIndex = None  # 紀錄"最佳"車廂索引
    for i, s in enumerate(stat): # 同時拿取索引值(i)跟元素(s)
        # 篩選可用車廂
        if s == "0":
            # 如果 bestSpaces 還是預設值，直接汰換初始值
            if bestSpaces is None:
                bestSpaces = sp[i]
                bestSpacesIndex = i
            
            if sp[i] == n: # 最符合，直接輸出結果 index
                return print(i)
            elif sp[i] < n: # 座位數比乘客數少
                # 且至今"最佳座位數"還少於"此車廂座位數"，調換優先集
                if bestSpaces < sp[i]: 
                    bestSpaces = sp[i]
                    bestSpacesIndex = i
            elif sp[i] > n: # 座位數比乘客數多
                # 至今"最佳座位數"少於"乘客數"或多於"此車廂座位數"，調換優先集
                if bestSpaces < n or bestSpaces > sp[i]:
                    bestSpaces = sp[i]
                    bestSpacesIndex = i
    
    return print(bestSpacesIndex)


# your code here 
func4([3, 1, 5, 4, 3, 2], "101000", 2)  # print 5 
func4([1, 0, 5, 1, 3], "10100", 4)  # print 4 
func4([4, 6, 5, 8], "1000", 4)  # print 2 
#endregion




