from fastapi import FastAPI, Request
from gpt_intent import interpretar_intencao
from oracle_wms_client import consultar_saldo
from gpt_response import gerar_resposta_consultiva
from zapi_client import enviar_whatsapp

app = FastAPI()

@app.post("/webhook")
async def receber_mensagem(request: Request):
    payload = await request.json()
    texto = payload.get("message", {}).get("text", "")
    telefone = payload.get("message", {}).get("phone", "")
    
    intencao = await interpretar_intencao(texto)
    
    if intencao["acao"] == "consultar_wms":
        dados = await consultar_saldo(intencao["item"])
        resposta = await gerar_resposta_consultiva(intencao["item"], dados)
    else:
        resposta = intencao["resposta"]
    
    await enviar_whatsapp(telefone, resposta)
    return {"status": "ok"}
