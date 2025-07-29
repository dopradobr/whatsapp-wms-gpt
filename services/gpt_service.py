import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

def gerar_resposta_gpt(mensagem_usuario):
    """
    Gera uma resposta consultiva usando GPT para complementar o atendimento.
    """

    try:
        prompt = f"""
        Você é um consultor especialista em Oracle WMS Cloud.
        O usuário enviou: "{mensagem_usuario}".
        Responda de forma amigável, curta e consultiva, convidando a explicar o desafio dele.
        """

        resposta = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Você é um especialista em Oracle WMS Cloud, consultivo e prestativo."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=150,
            temperature=0.7
        )

        return resposta.choices[0].message["content"].strip()

    except Exception as e:
        print(f"Erro ao gerar resposta GPT: {e}")
        return "Sou especialista em Oracle WMS Cloud — posso ajudar com dúvidas sobre inventário, recebimento, expedição, integrações e boas práticas. Qual é o seu desafio no momento?"
