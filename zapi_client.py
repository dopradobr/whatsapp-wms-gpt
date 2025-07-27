import httpx
import os

async def enviar_whatsapp(phone: str, message: str):
    """
    Envia uma mensagem de texto via Z-API para o número de WhatsApp informado.
    """

    # Monta a URL completa da Z-API com instance_id e token
    url = f"https://api.z-api.io/instances/{os.getenv('ZAPI_INSTANCE_ID')}/token/{os.getenv('ZAPI_TOKEN')}/send-text"

    payload = {
        "phone": phone,
        "message": message
    }

    try:
        async with httpx.AsyncClient() as client:
            await client.post(url, json=payload)
    except Exception as e:
        print(f"[ERRO] Falha ao enviar WhatsApp: {e}")
