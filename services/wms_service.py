"""
Serviço para consultar dados do Oracle WMS Cloud.
"""

import os
import requests

def query_wms(query_params):
    """
    Realiza a consulta ao WMS de acordo com os parâmetros extraídos pelo GPT.
    """
    base_url = os.getenv("ORACLE_BASE_URL")
    user = os.getenv("ORACLE_USER")
    password = os.getenv("ORACLE_PASSWORD")

    try:
        response = requests.get(base_url, auth=(user, password))
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": f"Erro {response.status_code} ao consultar o WMS."}
    except Exception as e:
        return {"error": str(e)}
