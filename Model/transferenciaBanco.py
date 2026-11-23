import sqlite3
from . import especificarBanco

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

    if categID == 11:
        cursor.execute('''
        UPDATE BANCOS_USUARIO set saldoBanco = saldoBanco + ? where bancoID = ?
    ''', (valor, idBanco))
    elif categID == 12:
        cursor.execute('''
        UPDATE BANCOS_USUARIO set cofrinhoBanco = cofrinhoBanco + ? where bancoID = ?
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

def guardarDinheiro(valor: float, idBanco: int):
    conexao = sqlite3.connect('bot.db')
    cursor = conexao.cursor()

    saldoAtual = especificarBanco.especificarBanco(idBanco)['saldoBanco']

    if (valor > saldoAtual):
        cursor.close()
        conexao.close()
        return False
    else:
        cursor.execute('''
        UPDATE BANCOS_USUARIO set 
        saldoBanco = saldoBanco - ?,
        cofrinhoBanco = cofrinhoBanco + ?
        WHERE bancoID = ? and saldoBanco >= ?
    ''', (valor, valor, idBanco, valor))
        if cursor.rowcount > 0:
            cursor.execute('''
            INSERT INTO RELATORIO_MOVIMENTACOES (valorMov, categID, bancoID) values (?,?,?)
        ''', (valor, 8 ,idBanco))

        conexao.commit()

    cursor.close()
    conexao.close()

    return cursor.rowcount == 1

def sacarCofre(valor: float, idBanco: int):
    conexao = sqlite3.connect('bot.db')
    cursor = conexao.cursor()
    cofreAtual = especificarBanco.especificarBanco(idBanco)['cofrinhoBanco']

    if (valor > cofreAtual):
        cursor.close()
        conexao.close()
        return False
    else:
        cursor.execute('''
        UPDATE BANCOS_USUARIO set
        saldoBanco = saldoBanco + ?,
        cofrinhoBanco = cofrinhoBanco - ?
        WHERE bancoID = ? and cofrinhoBanco >= ?
        ''', (valor,valor,idBanco,valor))
        if cursor.rowcount > 0:
            cursor.execute('''
            INSERT INTO RELATORIO_MOVIMENTACOES (valorMov, categID, bancoID) values(?,?,?)
            ''', (valor,10,idBanco))

        conexao.commit()

    cursor.close()
    conexao.close()
    return cursor.rowcount == 1