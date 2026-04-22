import requests
import os
from dotenv import load_dotenv

load_dotenv()

#ATUALIZAR O MAIN PARA CONSEGUIR ATUALIZAR OS DADOS NO BANCO

#PRECISA ALTERAR A QUERY DEPOIS

def consultar(order_id):
    url = f"https://api.intelipost.com.br/api/v1/shipment_order/{order_id}"

    headers = {
        "api-key": os.getenv("API_KEY"),
        "Accept": "application/json"
    }

    response = requests.get(url, headers=headers)

    data = response.json()
    content = data.get("content", {})

    volumes = content.get("shipment_order_volume_array", [])
    volume = volumes[0] if volumes else {}

    pedido = {
        "status_code":response.status_code,
        "estimated_delivery": content.get("estimated_delivery_date_lp_iso"),
        "delivered_at": content.get("delivered_date_iso"),
        "status": content.get("shipment_order_volume_state")
    }

    # Nota fiscal
    invoice = volume.get("shipment_order_volume_invoice", {})
    pedido["invoice_number"] = invoice.get("invoice_number")
    pedido["invoice_series"] = invoice.get("invoice_series")
    pedido["invoice_key"] = invoice.get("invoice_key")

    return pedido


def consultar_pedido(orders):
    resultados = []

    for order in orders:
        resultado = consultar(order)
        resultados.append(resultado)

    return resultados
