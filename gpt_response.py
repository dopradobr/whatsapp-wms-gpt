import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

async def gerar_resposta_consultiva(item_code: str, dados: list) -> str:
    """
    Usa o GPT para gerar uma resposta consultiva com base nos dados do item retornados pelo WMS.
    """

    # Converte os dados de inventário para um texto legível
    dados_formatados = "\n".join([str(d) for d in dados])

    # Prompt que será enviado ao GPT
    prompt = f"""
Você é um assistente de WhatsApp que responde perguntas sobre estoque.
Com base nos dados abaixo do item {item_code}, gere uma resposta consultiva, amigável e com emojis.

Exemplo de conteúdo dos dados:
{dados_formatados}

O objetivo é ajudar o usuário a entender se o item está disponível, em recebimento, onde está armazenado, e dar uma dica final se possível.

Responda como se estivesse falando no WhatsApp.
"""

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        # Retorna a resposta gerada pelo GPT
        return response["choices"][0]["message"]["content"]

    except Exception as e:
        # Retorna mensagem padrão em caso de erro
        return "Não consegui gerar a resposta agora. Pode tentar novamente em instantes?"
