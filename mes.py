from fastapi import FastAPI, HTTPException, Header
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import uvicorn

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

MES_FILE = r"C:\Users\김대경\Desktop\시스템데모\mes_data.csv"
ERP_FILE = r"C:\Users\김대경\Desktop\시스템데모\erp_data.csv"

# 가상의 사용자 데이터 및 토큰
ADMIN_USER = {"id": "admin", "pw": "1234"}
AUTH_TOKEN = "enterprise-ai-token-2026"

# [로그인 API]
@app.post("/api/login")
def login(data: dict):
    if data.get("username") == ADMIN_USER["id"] and data.get("password") == ADMIN_USER["pw"]:
        return {"success": True, "token": AUTH_TOKEN}
    raise HTTPException(status_code=401, detail="아이디 또는 비밀번호가 틀렸습니다.")

# [데이터 API - 보안 적용]
@app.get("/api/mes/all")
def get_mes_data(authorization: str = Header(None)):
    if authorization != f"Bearer {AUTH_TOKEN}":
        raise HTTPException(status_code=403, detail="인증되지 않은 접근입니다.")
    df = pd.read_csv(MES_FILE, encoding='utf-8-sig')
    return df.to_dict(orient="records")

@app.get("/api/erp/trace/{lot_no}")
def trace_lot(lot_no: str, authorization: str = Header(None)):
    if authorization != f"Bearer {AUTH_TOKEN}":
        raise HTTPException(status_code=403, detail="인증되지 않은 접근입니다.")
    df = pd.read_csv(ERP_FILE, encoding='utf-8-sig')
    return df[df['로트번호(Lot No)'] == lot_no].to_dict(orient="records")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)