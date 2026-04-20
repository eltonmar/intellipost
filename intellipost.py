import requests
import os
from dotenv import load_dotenv

load_dotenv()

orders = [
    '0110050004495625',
    'ANY324072532'
]

for order in orders:
    url = f"https://api.intelipost.com.br/api/v1/shipment_order/{order}"

    headers = {
        "api-key": os.getenv("API_KEY"),
        "Accept": "application/json"
    }

    response = requests.get(url, headers=headers)
    print(response.status_code)
    print(f"{url}")

    data = response.json()
    content = data.get("content", {})


    volumes = content.get("shipment_order_volume_array", [])
    volume = volumes[0] if volumes else {}

    pedido = {
        "estimated_delivery": content.get("estimated_delivery_date_lp_iso"),
        "delivered_at": content.get("delivered_date_iso"),
        "status": content.get("shipment_order_volume_state")
    }

    # Nota fiscal
    invoice = volume.get("shipment_order_volume_invoice", {})
    pedido["invoice_number"] = invoice.get("invoice_number")
    pedido["invoice_series"] = invoice.get("invoice_series")
    pedido["invoice_key"] = invoice.get("invoice_key")

    print('-' * 50)

    print("\n📦 Pedido normalizado:\n")
    for k, v in pedido.items():
        print(f"{k}: {v}")
