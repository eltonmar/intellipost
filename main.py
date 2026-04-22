
from services.intellipost import consultar_pedido

orders = [
    '0110050004495625',
    'ANY324072532',
    'SLR-1623852461974-01'
]

def main():
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

