from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from fastapi.encoders import jsonable_encoder 
# module
from sql import sql_connector as sql

router = APIRouter(prefix="/api") # 此 router 內的 api 都會先加上 /api

# 連線資料庫
conn = sql.get_connection()

# class
# 設立"更新姓名" Request Body 的形式
class MemberName(BaseModel):
    name: str

# 查詢會員資料
@router.post("/member/{member_id}")
def query_member(request: Request, member_id: int):
    # 確認登入
    if request.session["LOGGED_IN"]:
        # 用id查詢會員資訊
        sql1 = "SELECT id, name, email FROM member WHERE id = %s;"
        with conn.cursor() as cursor:
            cursor.execute(sql1, (member_id, ))
            result = cursor.fetchone()

        # 有抓到資料就 1.新增查詢資料到 member_queries 2.回傳資料
        if result:
            sql2 = "INSERT INTO member_queries(member_id, target_id) VALUES(%s, %s);"
            with conn.cursor() as cursor:
                cursor.execute(sql2, (request.session["USER_ID"], member_id))
                conn.commit()
            return JSONResponse({
                "data": {
                    "id": result[0],
                    "name": result[1],
                    "email": result[2]
                }
            })
        # 沒抓到就回傳 None
        else:
            return JSONResponse({
                "data": None
            })
   
# 更新會員姓名
@router.patch("/member")
def update_name(request: Request, member: MemberName):
    try: # 嘗試更新姓名
        sql = "UPDATE member SET name = %s WHERE id = %s;"
        with conn.cursor() as cursor:
            cursor.execute(sql, (member.name, request.session["USER_ID"]))
            conn.commit()
        # 更新 session 中的姓名
        request.session["USER_NAME"] = member.name
        return JSONResponse({
            "ok": True
        })
    except Exception as e: # 出錯就報錯，但不整個crush掉
        print("更新姓名錯誤: ", e)
        return JSONResponse({
            "error": True
        })
    

# 查詢紀錄(不包括自己)
@router.get("/memberQueries")
def track_queries(request: Request):
    try: # 嘗試查詢紀錄
        id = request.session["USER_ID"]
        sql = "SELECT member.name, member_queries.time FROM member_queries " \
        "INNER JOIN member ON member_queries.member_id = member.id " \
        "WHERE member_queries.target_id = %s AND member_queries.member_id <> %s " \
        "ORDER BY member_queries.time DESC " \
        "LIMIT 10;"
        with conn.cursor() as cursor:
            cursor.execute(sql, (id, id))
            result = cursor.fetchall()
        # 轉成 jsonable 格式，datetime物件會被轉成字串
        result = jsonable_encoder(result)
        return JSONResponse({
            "data": result
        })
    except Exception as e:
        print("查詢會員紀錄錯誤", e)
        return JSONResponse({
            "data": None,
            "sql-error": True 
        })