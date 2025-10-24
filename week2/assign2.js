//#region  Task1
function func1(name){ 
    // 建立各 point 座標
    let points = [
        {name: "辛巴", x: -3, y: 3, side: "L"},
        {name: "貝吉塔", x: -4, y: -1, side: "L"},
        {name: "悟空", x: 0, y: 0, side: "L"},
        {name: "特南克斯", x: 1, y: -2, side: "L"},
        {name: "丁滿", x: -1, y: 4, side: "R"},
        {name: "弗利沙", x: 4, y: -1, side: "R"},
    ];
    // 在陣列中依序尋找第一個符合角色名稱的 Object
    const target = points.find(p => p.name === name);
    // 沒找到就 return
    if (target === undefined) {
        return console.log("抱歉，無此角色。");
    }

    let shortestPoint = []; // 最短距離角色array
    let longestPoint = []; // 最長距離角色array
    let shortestDistance = 10000000; // 預設初始最短距
    let longestDistance = -1; // 預設初始最長距
    // 遍歷每個 Object
    for (let i=0; i < points.length; i++) {

        // 先排除 target 本身
        if (target.name != points[i].name) {
            // 計算兩點距離
            let distance = Math.abs(target.x - points[i].x) + Math.abs(target.y - points[i].y);
            if (target.side != points[i].side) {
                distance +=2;
            }

            // 比較最短距離
            if (distance < shortestDistance) { // 若 distance 小於至今最短距，則汰換"最短距"跟"最短point"
                shortestDistance = distance;
                // 清空 shortestPoint
                shortestPoint.length = 0; // shortestPoint=[]; 是把 shortestPoint 指到新陣列，舊陣列會保留
                shortestPoint.push(points[i].name);
            } else if (distance == shortestDistance) { // 若 distance 等於至今最短距，將 point 加入"最短point"
                shortestPoint.push(points[i].name);
            }

            // 比較最長距離
            if (distance > longestDistance) { // 若 distance 大於至今最長距，則汰換"最長距"跟"最長point"
                longestDistance = distance;
                // 清空 longestPoint
                longestPoint.length = 0;
                longestPoint.push(points[i].name);
            } else if (distance == longestDistance) { // 若 distance 等於至今最長距，將 point 加入"最長point"
                longestPoint.push(points[i].name);
            }
        }
    }

    return console.log(`最遠${longestPoint.join("、")};最近${shortestPoint.join("、")}`);
} 

func1("辛巴");  // print 最遠弗利沙；最近丁滿、⾙吉塔
 
func1("悟空");  // print 最遠丁滿、弗利沙；最近特南克斯
 
func1("弗利沙");  // print 最遠⾟巴，最近特南克斯
 
func1("特南克斯");  // print 最遠丁滿，最近悟空

//#endregion

console.log("======================================")

//#region Task2
let bookings = []; //已預約的時段 [{start: xx, end: xx, service: xx}]

function func2(ss, start, end, criteria){ 
    // 用正則表達式分開 criteria，"key"、"<= >= ="、"value"
    // arrMatch.match()回傳規則 -> arrMatch[0]=整個匹配的字串、arrMatch[1]=第一個()裡的部分1、arrMatch[1]=第二個()裡的部分...
    const match = criteria.match(/^\s*(r|c|name)\s*(>=|<=|=)\s*(.+)\s*$/);
    if (!match) 
        return console.log("條件式不符合規則。");
    const [, key, operations, value] = match; // 指派各項常數
    
    // 查詢特定服務是否可預約
    let isBooking = (name) => {
        // 用 .filter 篩選指定 service
        let serviceBookings = bookings.filter(b => b.service == name);
        // 遍歷每個已預約時段
        for (let b of serviceBookings) {
            // 判斷時段是否重疊
            if (start < b.end && end > b.start)
                return false;
        }
        return true;
    }

    // 開始判斷條件
    if (key === "name") {
        // 偵測指定 service 是否有空缺時間
        if (isBooking(value)) { 
            // 紀錄預約時間及服務項目
            bookings.push({start: start, end: end, service: value});
            return console.log(value); // 回傳結果
        }
    }
    else if (key === "r" || key === "c") {
        // 用 .filter 依照條件篩選可行的服務
        let availableServices = ss.filter(s => {
            if (operations === ">=") return s[key] >= value;  // Object[key] -> 會找 key 常數內的值來對應 Object 中的屬性
            else if (operations === "<=") return s[key] <= value;
        })

        // 用 .sort 排序，與條件 value 越靠近排越前面
        availableServices.sort((a, b) => Math.abs(a[key] - value) - Math.abs(b[key] - value));

        // 遍歷可行的服務
        for (let s of availableServices) {
            // 偵測對應 service 是否有空缺時間
            if (isBooking(s.name)) {
                // 有就紀錄並回傳
                bookings.push({start: start, end: end, service: s.name});
                return console.log(s.name);
            }
        }
    }

    return console.log("sorry");
} 

const services=[ 
{"name":"S1", "r":4.5, "c":1000}, 
{"name":"S2", "r":3, "c":1200}, 
{"name":"S3", "r":3.8, "c":800} 
];

func2(services, 15, 17, "c>=800");  // S3 
func2(services, 11, 13, "r<=4");  // S3 
func2(services, 10, 12, "name=S3");  // Sorry 
func2(services, 15, 18, "r>=4.5");  // S1 
func2(services, 16, 18, "r>=4");  // Sorry 
func2(services, 13, 17, "name=S1");  // Sorry 
func2(services, 8, 9, "c<=1500");  // S2 

//#endregion

console.log("======================================")

//#region Task3
function func3(index){ 
    if (Number.isInteger(index) === false || index < 0) 
        return console.log("不符合格式。");
    let sequence = [25];  // 初始序列
    let number = 25; // 初始數字

    // 依照規律計算序列，直到過了 index 值
    for(let i=0; i<index; i+=4) { 
        // 序列的規律是 -2, -3, +1, +2 一個循環
        number -= 2;
        sequence.push(number);
        number -= 3;
        sequence.push(number);
        number += 1;
        sequence.push(number);
        number += 2;
        sequence.push(number);
    }

    return console.log(sequence[index]);
} 
func3(1);  // print 23 
func3(5);  // print 21 
func3(10);  // print 16 
func3(30);  // print 6
//#endregion

console.log("======================================")

//#region Task4
function func4(sp, stat, n){
    const statArray = [...stat]; // 用展開運算子將 stat 拆成陣列
    let bestSub;  // 紀錄最佳"差值"的容器，用來比較"差值"
    let fitCarIndex;  // 紀錄最合適車廂編號

    // 遍歷所有車廂
    for (let i=0; i<statArray.length; i++) {
        // 篩選可用車廂
        if (statArray[i] == "0") {
            let sub = sp[i] - n;   // 計算"車廂可乘坐人數"與"乘客數"的差值

            // 如果 bestSub 還是預設值，直接汰換初始值
            if (bestSub === undefined) {
                fitCarIndex = i;
                bestSub = sub;
            }

            // 計算最合適車廂
            if (sub === 0) { // 一定是最合適的，直接輸出結果 index
                return console.log(i);
            }else if (sub > 0) { 
                // 塞的下的車廂(>0)優先於塞不下的車廂(<0) or 越接近乘車人數的優先
                if (bestSub < 0 || sub < bestSub) {
                    fitCarIndex = i;
                    bestSub = sub;
                }
            }else if (sub < 0) {
                // 越接近乘車人數的優先
                if(bestSub < sub) {
                    fitCarIndex = i;
                    bestSub = sub;
                }
            }
        }
    }
    return console.log(fitCarIndex);
    
} 
func4([3, 1, 5, 4, 3, 2], "101000", 2);  // print 5 
func4([1, 0, 5, 1, 3], "10100", 4);  // print 4 
func4([4, 6, 5, 8], "1000", 4);  // print 2 

//#endregion