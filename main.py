from fastapi import FastAPI, Request
import uvicorn
from services.zapi_service import enviar_mensagem_whatsapp
from services.wms_service import consultar_wms_service
from services.gpt_service import gerar_resposta_gpt

app = FastAPI()

@app.post("/webhook")
async def webhook(req: Request):
    dados = await req.json()

    try:
        mensagem = dados["messages"][0]["text"]["body"].strip()
        numero = dados["messages"][0]["from"]

        # Se a mensagem tiver um padrão de consulta WMS
        if mensagem.lower().startswith("consulta "):
            item_id = mensagem.split(" ", 1)[1]
            resposta_wms = consultar_wms_service(item_id)

            if resposta_wms:
                enviar_mensagem_whatsapp(numero, resposta_wms)
            else:
                enviar_mensagem_whatsapp(
                    numero,
                    "Não encontrei informações para o item informado. Pode verificar o código e tentar novamente?"
                )

        else:
            # Resposta consultiva quando não é consulta WMS
            mensagem_consultiva = (
                "Sou especialista em Oracle WMS Cloud — posso ajudar com dúvidas sobre inventário, "
                "recebimento, expedição, integrações e boas práticas. Qual é o seu desafio no momento?"
            )

            # Pode também gerar algo com GPT para parecer mais humano
            resposta_gpt = gerar_resposta_gpt(mensagem)
            resposta_final = f"{mensagem_consultiva}\n\n{resposta_gpt}"

            enviar_mensagem_whatsapp(numero, resposta_final)

    except Exception as e:
        print(f"Erro no processamento: {e}")

    return {"status": "ok"}

@app.get("/")
async def home():
    return {"status": "online", "mensagem": "API do WMS WhatsApp está no ar"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=10000)
