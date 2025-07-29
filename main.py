from fastapi import FastAPI, Request
from services.gpt_service import interpretar_intencao
from services.wms_service import consultar_wms
from services.zapi_service import enviar_mensagem

app = FastAPI()

@app.post("/webhook")
async def webhook(request: Request):
    dados = await request.json()
    mensagem = dados.get("message", "")
    telefone = dados.get("phone", "")

    intencao = await interpretar_intencao(mensagem)

    if intencao["acao"] == "consultar_wms":
        resposta_wms = await consultar_wms(intencao["item"])
        await enviar_mensagem(telefone, resposta_wms)

    elif intencao["acao"] == "responder":
        await enviar_mensagem(telefone, intencao["resposta"])

    return {"status": "ok"}
