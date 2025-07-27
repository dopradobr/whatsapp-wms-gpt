import httpx
import os
from base64 import b64encode

async def consultar_saldo(item_code: str) -> list:
    """
    Consulta o Oracle WMS Cloud usando o código do item fornecido.
    Retorna uma lista com os dados de inventário (LPNs, localização, quantidade, status).
    """

    # Codifica usuário e senha para autenticação básica em base64
    credentials = f"{os.getenv('ORACLE_USER')}:{os.getenv('ORACLE_PASSWORD')}"
    encoded_auth = b64encode(credentials.encode()).decode()

    # Monta o cabeçalho com autenticação básica
    headers = {
        "Authorization": f"Basic {encoded_auth}",
        "Content-Type": "application/json"
    }

    # Monta a URL com base no código do item
    base_url = os.getenv("ORACLE_BASE_URL")
    url = f"{base_url}?item_id__code={item_code}&values_list=container_id__status_id__description,curr_qty,location_id__locn_str,container_id__container_nbr"

    try:
        # Faz a requisição GET usando httpx
        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=headers)
            response.raise_for_status()  # Lança erro se status != 200

            # Retorna os resultados da API do WMS
            return response.json().get("results", [])

    except Exception as e:
        # Em caso de erro, retorna lista vazia
        return []
