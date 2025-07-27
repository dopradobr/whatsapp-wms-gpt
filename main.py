from fastapi import FastAPI, Request
from gpt_intent import interpretar_intencao
from oracle_wms_client import consultar_saldo
from gpt_response import gerar_resposta_consultiva
from zapi_client import enviar_whatsapp

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "API de atendimento WhatsApp + GPT + Oracle WMS Cloud"}

@app.post("/webhook")
async def receber_mensagem(request: Request):
    """
    Endpoint que recebe mensagens do WhatsApp (via Z-API webhook).
    A mensagem é interpretada pelo GPT, que decide se deve consultar o WMS ou responder direto.
    """

    try:
        payload = await request.json()

        # 🔹 Extração da mensagem e número
        mensagem = payload.get("message", {}).get("text", "")
        telefone = payload.get("message", {}).get("phone", "")

        print("[📩 RECEBIDO] Mensagem:", mensagem)
        print("[📞 TELEFONE]", telefone)

        if not mensagem or not telefone:
            print("[⚠️ ERRO] Mensagem ou telefone ausente no payload.")
            return {"status": "ignorado"}

        # 🧠 1. GPT interpreta a intenção
        intencao = await interpretar_intencao(mensagem)
        print("[🔎 INTENÇÃO DETECTADA]", intencao)

        # ⚙️ 2. Se for uma consulta ao WMS
        if intencao.get("acao") == "consultar_wms":
            item_code = intencao.get("item", "")

            if not item_code:
                resposta = "Não consegui identificar o item. Pode enviar o código novamente?"
            else:
                # 📦 3. Consultar o Oracle WMS Cloud
                dados = await consultar_saldo(item_code)
                print("[📦 DADOS DO WMS]", dados)

                # 🤖 4. GPT gera uma resposta consultiva com base nos dados
                resposta = await gerar_resposta_consultiva(item_code, dados)
                print("[🤖 RESPOSTA GERADA]", resposta)
        else:
            # 💬 5. Resposta direta do GPT
            resposta = intencao.get("resposta", "Desculpe, não entendi. Pode reformular?")
            print("[💬 RESPOSTA DIRETA]", resposta)

        # 📤 6. Enviar a resposta pelo WhatsApp via Z-API
        await enviar_whatsapp(telefone, resposta)
        print("[✅ ENVIADO PARA WHATSAPP]", telefone)

        return {"status": "ok"}

    except Exception as e:
        print("[❌ ERRO GERAL NO WEBHOOK]", str(e))
        return {"status": "erro", "mensagem": str(e)}
