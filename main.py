from fastapi import FastAPI, Request
from gpt_intent import interpretar_intencao
from oracle_wms_client import consultar_saldo
from gpt_response import gerar_resposta_consultiva
from zapi_client import enviar_whatsapp

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "API do atendimento GPT + Oracle WMS via WhatsApp"}

@app.post("/webhook")
async def receber_mensagem(request: Request):
    """
    Endpoint que recebe mensagens da Z-API via webhook.
    A Z-API envia um JSON com a mensagem e telefone do remetente.
    """
    payload = await request.json()

    # 🟡 Extração segura do conteúdo da mensagem
    mensagem = payload.get("message", {}).get("text", "")
    telefone = payload.get("message", {}).get("phone", "")

    if not mensagem or not telefone:
        return {"status": "ignorado"}

    # 🧠 1. O GPT interpreta o que o usuário quer
    intencao = await interpretar_intencao(mensagem)

    # ⚙️ 2. Se o GPT identificou que é uma consulta ao WMS
    if intencao.get("acao") == "consultar_wms":
        item_code = intencao.get("item", "")
        if not item_code:
            resposta = "Não consegui identificar o código do item. Pode mandar novamente?"
        else:
            # 🔍 3. Consulta real ao Oracle WMS Cloud
            dados = await consultar_saldo(item_code)

            # 🤖 4. GPT gera a resposta consultiva com base nos dados do WMS
            resposta = await gerar_resposta_consultiva(item_code, dados)
    else:
        # 💬 5. Caso o GPT diga que não precisa consultar o WMS, responde diretamente
        resposta = intencao.get("resposta", "Desculpe, não entendi. Pode repetir?")

    # 📲 6. Envia a resposta final pelo WhatsApp usando a Z-API
    await enviar_whatsapp(telefone, resposta)

    return {"status": "ok"}
