from fastapi import FastAPI, Form, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse, HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from routers.api_router import router as api_router
# 處理金鑰
from starlette.middleware.sessions import SessionMiddleware
from dotenv import load_dotenv 
import os 
load_dotenv()
# module
from sql import sql_connector as sql

app = FastAPI()

# router
app.include_router(api_router)

# 連線資料庫
conn = sql.get_connection()

# 用靜態網頁引入 css，讓 html 可以抓到路徑
app.mount("/css", StaticFiles(directory="css"), name="css")
# 指定 jinja2 模板到這個資料夾(裡面是會用到jinja2的所有html網頁)
templates = Jinja2Templates(directory="html")

# 使用密鑰(一串亂碼)，用來簽章，會儲存在 cookie
API_SECRETKEY = os.getenv("API_SECRETKEY") # 抓.env的金鑰
if API_SECRETKEY is None: # 因為secret_key只能接收str或secret，如果有None會出錯
    raise ValueError("API_SECRETKEY not found in .env file!")
app.add_middleware(SessionMiddleware, secret_key=API_SECRETKEY)


# 註冊登入頁面，首頁
@app.get("/", response_class=HTMLResponse)
def home(request: Request): # request 再 template 導入模式是必要的
    return templates.TemplateResponse("index.html",{"request": request})

# 註冊認證
@app.post("/signup", response_class=HTMLResponse)
def signup(
    request: Request, 
    name: str = Form(...), 
    email: str = Form(...), 
    password: str = Form(...)):
    # 資料庫尋找帳號對應的資料
    sql = "SELECT * FROM member WHERE email=%s"
    with conn.cursor() as cursor: # 用 with 可以安全關閉
        cursor.execute(sql, (email.lower(), )) # 信箱全部都以小寫判斷
        result = cursor.fetchone()
    
    if result is None: # 沒有重複信箱，可以註冊
        sql = "INSERT INTO member(name, email, password) VALUES(%s, %s, %s);"
        with conn.cursor() as cursor:
            cursor.execute(sql, (name, email.lower(), password))
            conn.commit()
        return RedirectResponse(url="/", status_code=303)
    else: # 有重複信箱，不能註冊
        return RedirectResponse(url="/ohoh?msg=重複的電子郵件", status_code=303)

# 登入認證
@app.post("/login", response_class=HTMLResponse)
def login(request: Request, email: str = Form(...), password: str = Form(...)):
    # 資料庫尋找帳密對應的資料
    sql = "SELECT id, name, email FROM member WHERE email=%s AND password=%s"
    with conn.cursor() as cursor: # 用 with 可以安全關閉
        cursor.execute(sql, (email.lower(), password))
        result = cursor.fetchone()

    if result is None: # 找不到對應資料
        return RedirectResponse(url="/ohoh?msg=電子郵件或密碼錯誤", status_code=303)
    else: # 找到對應資料
        request.session["LOGGED_IN"] = True
        request.session["USER_ID"] = result[0]
        request.session["USER_NAME"] = result[1]
        request.session["USER_EMAIL"] = result[2]
        return RedirectResponse(url="/member", status_code=303)


# 登入成功頁面
@app.get("/member", response_class=HTMLResponse)
def member(request: Request):
    # 先檢測有沒有這個key值，不然沒有會出錯
    if "LOGGED_IN" not in request.session:
        return RedirectResponse(url="/", status_code=303)
    
    # 檢查有沒有簽章，有才能進入登入成功頁面
    if request.session["LOGGED_IN"]:
        sql = "SELECT member.name, message.content, message.member_id, message.id FROM message " \
              "INNER JOIN member ON message.member_id = member.id " \
              "ORDER BY message.time;"
        with conn.cursor() as cursor:
            cursor.execute(sql)
            comments = cursor.fetchall()
        request.session["comments"] = comments

        return templates.TemplateResponse(
            "member.html",
            {
                "request": request, 
                "id": request.session["USER_ID"],
                "name": request.session["USER_NAME"],
                "email": request.session["USER_EMAIL"],
                "comments": request.session["comments"]
            })
    else:
        return RedirectResponse(url="/", status_code=303)

# 登入失敗頁面
@app.get("/ohoh", response_class=HTMLResponse)
def ohoh(request: Request, msg: str):
    # 避免直接修改網址導到其他網頁呈現，要確認一下msg是不是為這兩個訊息
    if (msg == "電子郵件或密碼錯誤" or msg == "重複的電子郵件"):
        return templates.TemplateResponse("ohoh.html",{"request": request, "msg": msg})
    else:
        return RedirectResponse(url="/", status_code=303)

# 登出
@app.get("/logout", response_class=HTMLResponse)
def logout(request: Request):
    # 將使用者狀態及資料清除
    request.session.clear()
    # 導回首頁
    return RedirectResponse(url="/", status_code=303)


# 創建留言
@app.post("/createMessage", response_class=HTMLResponse)
def create_message(request: Request, comment: str = Form(...)):
    sql = "INSERT INTO message (member_id, content) " \
          "VALUES(%s, %s);"
    with conn.cursor() as cursor:
        cursor.execute(sql, (request.session["USER_ID"], comment))
        conn.commit()
    return RedirectResponse(url="/member", status_code=303)

# 刪除留言
@app.post("/deleteMessage", response_class=HTMLResponse)
async def delete_message(request: Request):
    data = await request.json()
    comment_id = int(data.get("id"))
    if (comment_id):
        sql = "DELETE FROM message WHERE id = %s"
        with conn.cursor() as cursor:
            cursor.execute(sql, (comment_id, ))
            conn.commit()
        return JSONResponse({"success": True})
    else: return JSONResponse({"success": False, "message": "找不到這則留言"})