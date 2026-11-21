import sqlite3
from . import conectarBD

def query():
    conexao = conectarBD.conectarBanco()
    cursor = conexao.cursor()

    cursor.execute('''
    select
    *
    from relatorio_movimentacao
''')

    conexao.commit()

query()