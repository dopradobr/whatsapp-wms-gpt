import openai
import os
openai.api_key = os.getenv("OPENAI_API_KEY")

async def interpretar_intencao(mensagem):
    prompt = f"""
Você é um assistente que interpreta mensagens de WhatsApp.  
Classifique a intenção do usuário e retorne em JSON.  
Exemplo de saída:

{{
  "acao": "consultar_wms",
  "item": "TESTRM"
}}

Mensagem: "{mensagem}"
    """
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
    )
    try:
        conteudo = response["choices"][0]["message"]["content"]
        return eval(conteudo)
    except:
        return {"acao": "responder", "resposta": "Desculpe, não entendi. Pode reformular sua pergunta?"}
