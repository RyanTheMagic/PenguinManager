import sqlite3
from . import conectarBD
from datetime import datetime

def buscarMovTipoOper(tipoOper: int, mes_ano: datetime, bancoID=None):
    conexao = conectarBD.conectarBanco()
    conexao.row_factory = sqlite3.Row
    cursor = conexao.cursor()
    if bancoID is None:
        cursor.execute('''
        SELECT
        (
            substr(data_hora,7,4) || '-' ||
            substr(data_hora,4,2) 
        ) as mes_ano,
        sum(valorMov) as total
        FROM VIEW_MOVIMENTACOES
        WHERE tipoOperID = ?
        and mes_ano = ?
        group by
        mes_ano
        order by
        mes_ano
    ''', (tipoOper, mes_ano))
    else:
        cursor.execute('''
                SELECT
                bancoID,
                (
                    substr(data_hora,7,4) || '-' ||
                    substr(data_hora,4,2) 
                ) as mes_ano,
                sum(valorMov) as total
                FROM VIEW_MOVIMENTACOES
                WHERE tipoOperID = ?
                and mes_ano = ?
                and bancoID = ?
                group by
                mes_ano,
                bancoID
                order by
                mes_ano
            ''', (tipoOper, mes_ano, bancoID))
    resultado = cursor.fetchone()

    if resultado is None:
        return {'total': 0.0}
    else:
        cursor.close()
        conexao.close()
        return dict(resultado)