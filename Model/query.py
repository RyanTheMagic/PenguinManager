import sqlite3
from . import conectarBD

def query():
    conexao = conectarBD.conectarBanco()
    cursor = conexao.cursor()

    cursor.execute('''
    insert into CATEGORIAS_TIPOOPER (tipooperID, nomeTipoOper) values (?,?)
''', (4,'Transf. Entre Bancos'))

    conexao.commit()

query()