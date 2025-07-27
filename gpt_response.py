import openai
import os
openai.api_key = os.getenv("OPENAI_API_KEY")

async def gerar_resposta_consultiva(item, dados):
    prompt = f"""
Gere uma resposta de WhatsApp consultiva com base nos dados de saldo do item {item} abaixo:

{dados}

Use emojis, títulos e uma dica final, se possível.
    """
    resposta = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    return resposta["choices"][0]["message"]["content"]
