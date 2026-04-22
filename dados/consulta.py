from dados.conexao import getConexao

def buscar_orders ():
    conn = getConexao()
    cursor = conn.cursor()

    query = ("""
             SELECT
	            CASE 
		            WHEN L1_XNUMECO = '' THEN CONCAT(RTRIM(L1_FILIAL),RTRIM(L1_DOC))
		            ELSE RTRIM(L1_XNUMECO) 
		            END AS CODIN
		                FROM SL1010
                            WHERE L1_EMISNF = '20260410'
                            AND D_E_L_E_T_ = ''
                            AND L1_FILIAL IN ('011005', '011324')
            """
             )
    cursor.execute(query)

    orders =  [row[0] for row in cursor.fetchall()]

    cursor.close()
    conn.close()

    return orders

