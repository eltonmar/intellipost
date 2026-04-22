
from services.intellipost import consultar_pedido
from dados.consulta import buscar_orders

def main():
    orders = buscar_orders()

    resultados = consultar_pedido(orders)

    for pedido in resultados:
        print(pedido["status"])
        print(pedido["invoice_key"])
        print('-' * 88)

        for k, v in pedido.items():
            if k not in ['status_code', 'url']:
                print(f'{k}: {v}')

if __name__ == '__main__':
    main()

