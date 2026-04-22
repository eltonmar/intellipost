from dados.conexao import getConexaoE

def atualizar_base(pedido):
    conn = getConexaoE()
    cursor = conn.cursor()

    # verifica se existe
    cursor.execute("SELECT 1 FROM INTELLIPOST_RECEBIMENTO WHERE CHAVE = ?", pedido.get("invoice_key"))
    existe = cursor.fetchone()

    if existe:
        cursor.execute("""
            UPDATE INTELLIPOST_RECEBIMENTO
            SET 
            , ENTREGA = ?
            , PREV_ENTREGA = ?
            , MICROSTATUS = ?
            WHERE CHAVE = ?
        """,
                pedido.get("delivered_at"),
                pedido.get("estimated_delivery"),
                pedido.get("status"),
                pedido.get("invoice_key")
                       )

    else:
        cursor.execute("""
            INSERT INTO INTELLIPOST_RECEBIMENTO 
            (SERIE, NOTA, ENTREGA, PREV_ENTREGA, MICROSTATUS,CHAVE)
            VALUES (?, ?, ?, ?, ?, ?)
        """,
                       pedido.get("invoice_series"),
                       pedido.get("invoice_number"),
                       pedido.get("delivered_at"),
                       pedido.get("estimated_delivery"),
                       pedido.get("status"),
                       pedido.get("invoice_key"),
                       )

    conn.commit()
    cursor.close()
    conn.close()
