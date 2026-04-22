
from services.intellipost import consultar_pedido
from dados.consulta import buscar_orders

def main():
    orders = buscar_orders()

    resultados = consultar_pedido(orders)

    for pedido in resultados:

        #print(pedido["status"])
        #print(pedido["invoice_key"])
        #print(pedido["status_code"])
        #print('-' * 88)

        #for k, v in pedido.items():
        #    if k not in ['status_code', 'url']:
        #        print(f'{k}: {v}')

        if pedido.get("status_code") == 200:
            print(pedido["invoice_key"])
            print(pedido["status_code"])
            print('-' * 88)
        else:
            print(f"{orders} - NAO")


if __name__ == '__main__':
    main()
