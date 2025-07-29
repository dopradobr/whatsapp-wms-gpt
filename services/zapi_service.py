"""
Serviço para enviar mensagens via Z-API.
"""

import os
import requests

def send_whatsapp_message(phone, text):
    """
    Envia mensagem para o número informado usando Z-API.
    """
    zapi_url = os.getenv("ZAPI_URL")
    payload = {"phone": phone, "message": text}
    try:
        requests.post(zapi_url, json=payload)
    except Exception as e:
        print(f"Erro ao enviar mensagem: {e}")
