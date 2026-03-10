from fastapi import FastAPI, HTTPException, Header
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import uvicorn
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# 파일들이 같은 api/ 폴더 안에 있으므로 경로가 안전하게 매핑됩니다.
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MES_FILE = os.path.join(BASE_DIR, "mes_data.csv")
ERP_FILE = os.path.join(BASE_DIR, "erp_data.csv")

ADMIN_USER = {"id": "admin", "pw": "1234"}
AUTH_TOKEN = "enterprise-ai-token-2026"

@app.post("/api/login")
def login(data: dict):
    if data.get("username") == ADMIN_USER["id"] and data.get("password") == ADMIN_USER["pw"]:
        return {"success": True, "token": AUTH_TOKEN}
    raise HTTPException(status_code=401, detail="인증 실패")

@app.get("/api/mes/all")
def get_mes_data(authorization: str = Header(None)):
    if authorization != f"Bearer {AUTH_TOKEN}":
        raise HTTPException(status_code=403, detail="인증 필요")
    df = pd.read_csv(MES_FILE, encoding='utf-8-sig')
    return df.to_dict(orient="records")

@app.get("/api/erp/trace/{lot_no}")
def trace_lot(lot_no: str, authorization: str = Header(None)):
    if authorization != f"Bearer {AUTH_TOKEN}":
        raise HTTPException(status_code=403, detail="인증 필요")
    df = pd.read_csv(ERP_FILE, encoding='utf-8-sig')
    return df[df['로트번호(Lot No)'] == lot_no].to_dict(orient="records")
