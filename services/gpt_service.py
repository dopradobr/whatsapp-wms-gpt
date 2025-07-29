"""
Serviço GPT: interpreta perguntas do usuário e gera respostas consultivas.
"""

import os
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")

def interpret_question(user_message):
    """
    Usa GPT para entender a intenção do usuário e extrair parâmetros de consulta.
    """
    prompt = f"""
    Analise a pergunta abaixo e identifique:
    - Se o usuário quer consultar saldo, LPNs ou itens no recebimento
    - O item, se informado
    Pergunta: "{user_message}"
    """
    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )
    return response.choices[0].message["content"].strip()

def generate_consultative_response(original_question, wms_data):
    """
    Usa GPT para transformar os dados do WMS em uma resposta consultiva e clara.
    """
    prompt = f"""
    O usuário fez a pergunta: "{original_question}".
    Os dados retornados do WMS foram:
    {wms_data}

    Crie uma resposta consultiva, clara e organizada para o usuário.
    """
    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3
    )
    return response.choices[0].message["content"].strip()
