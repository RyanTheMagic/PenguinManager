import sqlite3
from . import conectarBD
from datetime import datetime

def buscarCategMes(categID: int, mes_ano: datetime):
    conexao = conectarBD.conectarBanco()
    conexao.row_factory = sqlite3.Row
    cursor = conexao.cursor()

    cursor.execute('''
    SELECT
    (
        substr(data_hora,7,4) || '-' ||
        substr(data_hora,4,2) 
    ) as mes_ano,
    categID,
    sum(valorMov) as total
    from VIEW_MOVIMENTACOES

    where 
    categID = ?
    and mes_ano = ?

    group by
    mes_ano,
    categID
    order by
    mes_ano
''', (categID, mes_ano))

    resultado = cursor.fetchone()

    cursor.close()
    conexao.close()

    return dict(resultado)