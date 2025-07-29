import os
import openai
import json

openai.api_key = os.getenv("OPENAI_API_KEY")

async def interpretar_intencao(mensagem):
    """
    Usa o ChatGPT para entender a intenção do usuário.
    Retorna um dicionário como:
    {
        "acao": "consultar_wms",
        "item": "TESTRM"
    }
    ou
    {
        "acao": "responder",
        "resposta": "Mensagem consultiva"
    }
    """

    prompt = f"""
    Você é um consultor especializado em Oracle WMS Cloud.
    Sua função é interpretar mensagens recebidas no WhatsApp e:

    - Se a mensagem pedir saldo ou status de um item → responder APENAS com: 
      {{"acao": "consultar_wms", "item": "<ITEM>"}}
    
    - Caso contrário → responder APENAS com:
      {{"acao": "responder", "resposta": "Sou especialista em Oracle WMS Cloud — posso ajudar com dúvidas sobre inventário, recebimento, expedição, integrações e boas práticas. Qual é o seu desafio no momento?"}}

    Mensagem recebida: "{mensagem}"
    """

    try:
        resposta = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Você é um especialista em Oracle WMS Cloud."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.0
        )

        conteudo = resposta.choices[0].message["content"].strip()

        try:
            return json.loads(conteudo)
        except:
            return {
                "acao": "responder",
                "resposta": "Sou especialista em Oracle WMS Cloud — posso ajudar com dúvidas sobre inventário, recebimento, expedição, integrações e boas práticas. Qual é o seu desafio no momento?"
            }

    except Exception as e:
        return {
            "acao": "responder",
            "resposta": f"Não consegui processar sua solicitação no momento. Erro: {str(e)}"
        }
