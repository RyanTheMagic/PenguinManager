import sqlite3
from . import conectarBD

def especificarTipoTransfCateg(tipotransf: int):
    conexao = conectarBD.conectarBanco()
    conexao.row_factory = sqlite3.Row

    cursor = conexao.cursor()

    cursor.execute('''
    SELECT
    *
    FROM CATEGORIAS_TRANSFERENCIA
    WHERE tipotransf = ?
''', (tipotransf,))

    resultados = cursor.fetchall()

    if len(resultados) == 1:
        return dict(resultados[0])
    else:
        return [dict(resultado) for resultado in resultados]