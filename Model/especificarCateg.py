import sqlite3
from . import conectarBD

def especificarCateg(categID: int):
    conexao = conectarBD.conectarBanco()
    conexao.row_factory = sqlite3.Row

    cursor = conexao.cursor()
    cursor.execute('''
    SELECT
    *
    FROM CATEGORIAS_TRANSFERENCIA
    where categID = ?
''', (categID,))

    resultado = cursor.fetchone()

    return dict(resultado)