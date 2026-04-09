from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime, timedelta
from jose import jwt

app = FastAPI(title="Auth Service")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

SECRET_KEY = "iau_secret"
ALGORITHM = "HS256"

@app.get("/")
async def root():
    """Servisin ana dizinine erişildiğinde çalışır."""
    return {"message": "Auth Service Online"}

@app.get("/health")
async def health_check():
    """Docker Healthcheck'in sorguladığı özel adres."""
    return {"status": "healthy", "service": "auth-service"}

@app.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    print(f"DEBUG: {form_data.username} giriş yapmaya çalışıyor...")
    
    if form_data.username == "admin" and form_data.password == "1234":
        expire = datetime.utcnow() + timedelta(minutes=30)
        token = jwt.encode({"sub": form_data.username, "exp": expire}, SECRET_KEY, algorithm=ALGORITHM)
        return {"access_token": token, "token_type": "bearer"}
    
    raise HTTPException(status_code=401, detail="Hatalı giriş")

@app.get("/verify")
async def verify(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return {"status": "valid", "user": payload.get("sub")}
    except:
        raise HTTPException(401, "Geçersiz token")