import httpx
import os
from base64 import b64encode

async def consultar_saldo(item_code):
    auth = b64encode(f"{os.getenv('ORACLE_USER')}:{os.getenv('ORACLE_PASSWORD')}".encode()).decode()
    headers = {
        "Authorization": f"Basic {auth}",
        "Content-Type": "application/json"
    }

    url = f"{os.getenv('ORACLE_BASE_URL')}/entity/inventory?item_id__code={item_code}&values_list=container_id__status_id__description,curr_qty,location_id__locn_str,container_id__container_nbr"
    
    async with httpx.AsyncClient() as client:
        r = await client.get(url, headers=headers)
        return r.json().get("results", [])
