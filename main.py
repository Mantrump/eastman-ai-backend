import os
import requests
from fastapi import FastAPI
from fastapi.responses import RedirectResponse, JSONResponse
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

APS_CLIENT_ID = os.getenv("APS_CLIENT_ID")
APS_CLIENT_SECRET = os.getenv("APS_CLIENT_SECRET")
APS_CALLBACK_URL = os.getenv("APS_CALLBACK_URL")

@app.get("/")
def root():
    return {"message": "Eastman AI Backend Running"}

@app.get("/auth/start")
def auth_start():
    auth_url = (
        "https://developer.api.autodesk.com/authentication/v2/authorize"
        f"?response_type=code"
        f"&client_id={APS_CLIENT_ID}"
        f"&redirect_uri={APS_CALLBACK_URL}"
        f"&scope=data:read data:write"
    )
    return RedirectResponse(auth_url)

@app.get("/auth/callback")
def auth_callback(code: str):
    token_url = "https://developer.api.autodesk.com/authentication/v2/token"
    response = requests.post(
        token_url,
        data={
            "grant_type": "authorization_code",
            "code": code,
            "client_id": APS_CLIENT_ID,
            "client_secret": APS_CLIENT_SECRET,
            "redirect_uri": APS_CALLBACK_URL,
        },
    )
    return JSONResponse(response.json())
