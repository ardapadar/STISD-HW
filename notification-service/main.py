from fastapi import FastAPI
from pydantic import BaseModel
import logging


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("IAU-NotificationService")

app = FastAPI(title="Notification Service")


class NotifyData(BaseModel):
    title: str
    category: str

class EmailData(BaseModel):
    email: str
    title: str
    content: str


@app.post("/notify")
async def send_notification(data: NotifyData):
    logger.info(f"Kritik Olay Yakalandı: {data.title}")
    print(f"📧 [SİSTEM BİLDİRİMİ]: '{data.title}' ({data.category}) başlıklı kritik not kaydedildi!")
    return {"status": "notification_sent"}

@app.post("/send-email")
async def send_email(data: EmailData):
    logger.info(f"Mail İsteği Geldi: {data.email}")
   
    print(f"📬 [MAIL SUNUCUSU]: '{data.title}' içeriği '{data.email}' adresine başarıyla iletildi!")
    print(f"📝 İletilen İçerik: {data.content}")
    return {"status": "email_delivered", "recipient": data.email}