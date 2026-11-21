import sqlite3

def transferenciaBanco(valor: float, idBanco: int):
    conexao = sqlite3.connect('bot.db')
    cursor = conexao.cursor()

    cursor.execute('''
    UPDATE BANCOS_USUARIO set saldoBanco = saldoBanco + ? where bancoID = ?
''', (valor, idBanco))

    conexao.commit()
    cursor.close()
    conexao.close()

def depositoBanco(valor: float, idBanco: int, categID: int):
    conexao = sqlite3.connect('bot.db')
    cursor = conexao.cursor()

    cursor.execute('''
    UPDATE BANCOS_USUARIO set saldoBanco = saldoBanco + ? where bancoID = ?
''', (valor, idBanco))

    if cursor.rowcount > 0:
        cursor.execute('''
        INSERT INTO RELATORIO_MOVIMENTACOES (valorMov, categID, bancoID) values (?,?,?)
''', (valor, categID, idBanco))

    conexao.commit()
    
    cursor.close()
    conexao.close()

def saqueBanco(valor: float, idBanco: int, categID: int):
    conexao = sqlite3.connect('bot.db')
    cursor = conexao.cursor()

    cursor.execute('''
    UPDATE BANCOS_USUARIO set saldoBanco = saldoBanco - ? where bancoID = ? and saldoBanco >= ?
''', (valor, idBanco, valor))

    if cursor.rowcount > 0:
        cursor.execute('''
        INSERT INTO RELATORIO_MOVIMENTACOES (valorMov, categID, bancoID) values (?,?,?)
    ''', (valor, categID, idBanco))

    conexao.commit()

    cursor.close()
    conexao.close()

    return cursor.rowcount == 1
