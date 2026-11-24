import sqlite3
from . import conectarBD

def buscarUltMov():
    conexao = conectarBD.conectarBanco()
    conexao.row_factory = sqlite3.Row

    cursor = conexao.cursor()

    cursor.execute('''
    SELECT
    datetime(
    substr(data_hora,7,4) || '-' ||
    substr(data_hora,4,2) || '-' ||
    substr(data_hora,1,2) || ' ' ||
    substr(data_hora,12,8)
    ) as data_hora_convertida,
    VIEW_MOVIMENTACOES.categID,
    VIEW_MOVIMENTACOES.valorMov,
    VIEW_MOVIMENTACOES.categoria,
    categorias_transferencia.emojiCategoria,
    VIEW_MOVIMENTACOES.banco,
    VIEW_MOVIMENTACOES.tipoOperacao
    from VIEW_MOVIMENTACOES

    left join categorias_transferencia
    on categorias_transferencia.categID = VIEW_MOVIMENTACOES.categID

    ORDER BY
    data_hora_convertida desc
    limit 1
''')

    resultado = cursor.fetchone()

    cursor.close()
    conexao.close()

    return dict(resultado)