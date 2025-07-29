"""
Funções auxiliares para formatação de dados do WMS.
"""

def format_wms_data(raw_data):
    """
    Recebe os dados crus do WMS e organiza para leitura mais fácil.
    """
    formatted = []
    for item in raw_data.get("items", []):
        formatted.append(f"LPN: {item.get('lpn')} | Item: {item.get('item_code')} | Qtd: {item.get('quantity')}")
    return "\n".join(formatted)
