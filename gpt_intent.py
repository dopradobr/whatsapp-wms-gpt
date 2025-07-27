import openai
import os

# Define a chave da API da OpenAI com base nas variáveis de ambiente do Render
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
      "resposta": "Mensagem direta do GPT sem consulta"
    }
    """
    
    prompt = f"""
Você é um assistente inteligente que interpreta mensagens recebidas no WhatsApp.  
Seu trabalho é analisar o que o usuário quer e responder em formato JSON.

Se a mensagem for uma consulta de saldo ou status de um item, responda assim:
{{
  "acao": "consultar_wms",
  "item": "TESTRM"
}}

Se for uma pergunta geral (ex: o que é picking?), responda assim:
{{
  "acao": "responder",
  "resposta": "Explicação em linguagem simples"
}}

Mensagem recebida: "{mensagem}"
"""
    
    try:
        # Faz a chamada à API do ChatGPT
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        # Extrai o conteúdo de texto gerado pelo GPT
        conteudo = response["choices"][0]["message"]["content"]

        # Tenta interpretar como dicionário Python (o GPT responde em JSON)
        return eval(conteudo)
    
    except Exception as e:
        # Se falhar, responde com uma mensagem padrão
        return {
            "acao": "responder",
            "resposta": "Desculpe, não entendi. Pode reformular sua pergunta?"
        }
