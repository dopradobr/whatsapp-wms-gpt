"""
Arquivo principal com FastAPI para receber mensagens do Z-API, interpretar com GPT,
consultar dados no Oracle WMS Cloud e responder de forma consultiva.
"""

from fastapi import FastAPI, Request
import os
from services.gpt_service import interpret_question, generate_consultative_response
from services.wms_service import query_wms
from services.zapi_service import send_whatsapp_message

app = FastAPI()

@app.get("/")
async def root():
    return {"status": "ok", "message": "whatsapp-wms-gpt is running"}

@app.post("/webhook")
async def webhook(request: Request):
    data = await request.json()

    # Captura a mensagem recebida
    message = data.get("message", {}).get("text", "").strip()
    phone = data.get("message", {}).get("from", "").strip()

    if not message or not phone:
        return {"status": "error", "message": "Mensagem ou telefone ausente no payload."}

    # Passo 1: Interpretar a pergunta
    interpreted_query = interpret_question(message)

    # Passo 2: Consultar o WMS
    wms_data = query_wms(interpreted_query)

    # Passo 3: Gerar resposta consultiva
    response_text = generate_consultative_response(message, wms_data)

    # Passo 4: Enviar mensagem pelo WhatsApp via Z-API
    send_whatsapp_message(phone, response_text)

    return {"status": "success"}
