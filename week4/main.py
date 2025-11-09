from fastapi import FastAPI, Form, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware
from module import hotel_cache


app = FastAPI()

# 用靜態網頁引入 css，讓 html 可以抓到路徑
app.mount("/css", StaticFiles(directory="css"), name="css")

# 指定 jinja2 模板到這個資料夾(裡面是會用到jinja2的所有html網頁)
templates = Jinja2Templates(directory="html")

# 使用密鑰(一串亂碼)，用來簽章，會儲存在 cookie
app.add_middleware(SessionMiddleware, secret_key="tshaktilg")

# 登入頁面，首頁
@app.get("/", response_class=HTMLResponse)
def home(request: Request): # request 再 template 導入模式是必要的
    return templates.TemplateResponse("index.html",{"request": request})

# 登入認證
@app.post("/login", response_class=HTMLResponse)
def login(request: Request, email: str = Form(...), password: str = Form(...)):
    # 檢查帳密是否有空白
    if email == "" or password == "":
        return RedirectResponse(url="/ohoh?msg=請輸入帳號或密碼", status_code=303) # 303是確定以 GET 請求重新導回要求路徑
    # 帳密皆正確
    elif email == "abc@abc.com" and password == "abc":
        request.session["LOGGED_IN"] = True
        return RedirectResponse(url="/member", status_code=303) 
    # 帳密有錯誤
    else:
        return RedirectResponse(url="/ohoh?msg=信箱或密碼輸入錯誤", status_code=303)

# 登入成功頁面
@app.get("/member", response_class=HTMLResponse)
def member(request: Request):
    # 先檢測有沒有這個key值，不然沒有會出錯
    if "LOGGED_IN" not in request.session:
        return RedirectResponse(url="/", status_code=303)
    
    # 檢查有沒有簽章，有才能進入登入成功頁面
    if request.session["LOGGED_IN"]:
        return templates.TemplateResponse("member.html",{"request": request})
    else:
        return RedirectResponse(url="/", status_code=303)

# 登入失敗頁面
@app.get("/ohoh", response_class=HTMLResponse)
def ohoh(request: Request, msg: str):
    # 避免直接修改網址導到其他網頁呈現，要確認一下msg是不是為這兩個訊息
    if (msg == "信箱或密碼輸入錯誤" or msg == "請輸入帳號或密碼"):
        return templates.TemplateResponse("ohoh.html",{"request": request, "msg": msg})
    else:
        return RedirectResponse(url="/", status_code=303)

# 登出
@app.get("/logout")
def logout(request: Request):
    # 讓key值換成"非登入"狀態
    request.session["LOGGED_IN"] = False
    # 導回首頁
    return RedirectResponse(url="/", status_code=303)


# 旅館資訊頁面
@app.get("/hotel/{id}", name="hotel")
def hotel(request: Request, id):
    # 已在 hotel_cache.py 抓取旅館資訊並且整理出旅館字典，不用每次請求都抓一遍，加快查找速度

    # 從旅館字典找到對應id的物件
    h_en = hotel_cache.en_dict.get(int(id))
    h_ch = hotel_cache.ch_dict.get(int(id))

    # 確認是否抓取到資料，改變回傳資料
    if h_en and h_ch:
        hotel_info = h_ch["旅宿名稱"] + "、" + h_en["hotel name"] + "、" + h_ch["電話或手機號碼"]
        return templates.TemplateResponse("hotel.html",{"request": request, "hotel_info": hotel_info})
    else:
        return templates.TemplateResponse("hotel.html",{"request": request, "hotel_info": "查詢不到相關資料"})
    


