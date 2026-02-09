import requests
import os
from dotenv import load_dotenv

load_dotenv()

url = "https://api.intelipost.com.br/api/v1/shipment_order/0110050004291665"

headers = {
    "api-key": os.getenv("API_KEY"),
    "Accept": "application/json"
}

response = requests.get(url, headers=headers)
print(response.status_code)

data = response.json()
content = data.get("content", {})

# Volume (pega o primeiro)
volumes = content.get("shipment_order_volume_array", [])
volume = volumes[0] if volumes else {}

# Cliente final
end_customer = content.get("end_customer", {})

pedido = {
    "order_number": content.get("order_number"),
    "tracking_url": content.get("tracking_url"),
    "erp_order": content.get("external_order_numbers", {}).get("erp"),
    "marketplace_order": content.get("external_order_numbers", {}).get("marketplace"),
    "sales_order": content.get("sales_order_number"),
    "logistic_provider": content.get("logistic_provider_name"),
    "delivery_method": content.get("delivery_method_name"),
    "created_at": content.get("created_iso"),
    "shipped_at": content.get("shipped_date_iso"),
    "estimated_delivery": content.get("estimated_delivery_date_lp_iso"),
    "delivered_at": content.get("delivered_date_iso"),
    "delivered": content.get("shipment_order_volume_state") == "DELIVERED",
    "status": content.get("shipment_order_volume_state"),
    "cnpj": end_customer.get("federal_tax_payer_id"),
    "shipment_volume_micro_state_description": volume
        .get("shipment_volume_micro_state", {})
        .get("description"),
    "shipment_volume_micro_state_default_name": volume
        .get("shipment_volume_micro_state", {})
        .get("default_name"),
    "status_pt": volume.get("shipment_order_volume_state_localized"),
    "tracking_code": volume.get("tracking_code"),
    "origin_city": content.get("origin_city"),
    "origin_state": content.get("origin_state_code"),
    "destination_city": end_customer.get("shipping_city"),
    "destination_state": end_customer.get("shipping_state_code")
}

# Nota fiscal
invoice = volume.get("shipment_order_volume_invoice", {})
pedido["invoice_number"] = invoice.get("invoice_number")
pedido["invoice_series"] = invoice.get("invoice_series")
pedido["invoice_key"] = invoice.get("invoice_key")
pedido["invoice_total_value"] = invoice.get("invoice_total_value")
pedido["invoice_date"] = invoice.get("invoice_date_iso")

print("\n📦 Pedido normalizado:\n")
for k, v in pedido.items():
    print(f"{k}: {v}")
