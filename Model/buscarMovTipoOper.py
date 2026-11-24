import sqlite3
from . import conectarBD

def buscarMovTipoOper(tipoOper: int):
    conexao = conectarBD.conectarBanco()
    conexao.row_factory = sqlite3.Row

    cursor = conexao.cursor()

    cursor.execute('''
    SELECT
    (
        substr(data_hora,7,4) || '-' ||
        substr(data_hora,4,2) 
    ) as mes,
    sum(valorMov) as total
    FROM VIEW_MOVIMENTACOES
    WHERE tipoOperID = ?
    group by
    mes
    order by
    mes
''', (tipoOper,))

    resultado = cursor.fetchone()

    cursor.close()
    conexao.close()

    return dict(resultado)