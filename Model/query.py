import sqlite3
from . import conectarBD

#Arquivo de query rápidas!
#Comando para executar:python -m Model.query

def query():
    conexao = conectarBD.conectarBanco()
    cursor = conexao.cursor()

    cursor.execute('''
    update categorias_transferencia set emojiCategoria = ? where categID = ?
''', ('🐷',12))

    conexao.commit()

query()