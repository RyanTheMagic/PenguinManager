import sqlite3
from . import conectarBD

def query():
    conexao = conectarBD.conectarBanco()
    cursor = conexao.cursor()

    cursor.execute('''
    insert into CATEGORIAS_TRANSFERENCIA(nomeCategoria,tipoTransf,emojiCategoria) values ('Porquinho',1,'🐖');
''')

    conexao.commit()

query()