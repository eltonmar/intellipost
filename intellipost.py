import requests, time
from datetime import datetime, timedelta

API_BASE = "https://api.intelipost.com.br/api/v1/shipment_order/set_invoice"          # ajuste se for outro host
API_KEY = "dfe114ffe1061f3efc1e4edf8bb5e3e857b1640fc2b2f5c5fa25faceb065b892"                              # header: api-key
PLATFORM_KEY = "SUA_PLATFORM_KEY"                    # header: platform (se exigido)

HEADERS = {
    "Content-Type": "application/json",
    "api-key": API_KEY,
    "platform": PLATFORM_KEY
}

def fetch_orders_by_window(start_iso, end_iso, page_size=200):
    """
    Busca pedidos por janela [start_iso, end_iso] respeitando paginação.
    Ajuste os nomes dos parâmetros conforme a doc do seu endpoint de listagem.
    """
    all_rows = []
    page = 1
    while True:
        params = {
            "updated_at_start": start_iso,   # ou created_at_start / start_date
            "updated_at_end": end_iso,       # ou created_at_end / end_date
            "page": page,
            "per_page": page_size            # ou size/limit
        }
        r = requests.get(f"{API_BASE}/orders", headers=HEADERS, params=params, timeout=60)
        if r.status_code == 429:
            time.sleep(2**min(page, 6))
            continue
        r.raise_for_status()
        data = r.json()

        # Ajuste os caminhos do payload conforme o retorno real:
        rows = data.get("content") or data.get("orders") or data
        if not rows:
            break

        all_rows.extend(rows)

        # Quebra de laço conforme o meta/paginação:
        total_pages = (data.get("total_pages") or data.get("meta", {}).get("total_pages"))
        if total_pages and page >= total_pages:
            break

        # Fallback simples: se retornou menos que page_size, acabou:
        if not total_pages and len(rows) < page_size:
            break

        page += 1
    return all_rows

def harvest_period(day_from, day_to):
    """
    Varre por janelas de 1 dia no eixo updated_at.
    """
    cur = day_from
    all_rows = []
    while cur <= day_to:
        start_iso = cur.strftime("%Y-%m-%dT00:00:00-03:00")
        end_iso   = cur.strftime("%Y-%m-%dT23:59:59-03:00")
        rows = fetch_orders_by_window(start_iso, end_iso)
        all_rows.extend(rows)
        cur += timedelta(days=1)
    return all_rows

# Exemplo: coletar de 2025-08-01 a 2025-08-24
if __name__ == "__main__":
    rows = harvest_period(datetime(2025,8,1), datetime(2025,8,01))
    print(f"Coletados {len(rows)} pedidos")
    # daqui, grave em CSV/Excel ou faça upsert no seu SQL
