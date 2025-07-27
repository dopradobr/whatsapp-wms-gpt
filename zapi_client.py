import httpx
import os

async def enviar_whatsapp(phone, message):
    url = f"{os.getenv('ZAPI_URL')}/{os.getenv('ZAPI_INSTANCE_ID')}/token/{os.getenv('ZAPI_TOKEN')}/sendText"
    payload = {
        "phone": phone,
        "message": message
    }
    async with httpx.AsyncClient() as client:
        await client.post(url, json=payload)
