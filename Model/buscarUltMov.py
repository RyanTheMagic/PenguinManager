import sqlite3
from . import conectarBD

def buscarUltMov(bancoID=None):
    conexao = conectarBD.conectarBanco()
    conexao.row_factory = sqlite3.Row

    cursor = conexao.cursor()

    if bancoID is None:
        cursor.execute('''
        SELECT
        datetime(
        substr(data_hora,7,4) || '-' ||
        substr(data_hora,4,2) || '-' ||
        substr(data_hora,1,2) || ' ' ||
        substr(data_hora,12,8)
        ) as data_hora_convertida,
        VIEW_MOVIMENTACOES.categID,
        case 
        when VIEW_MOVIMENTACOES.tipoOperID = 0
        then
        -ABS(VIEW_MOVIMENTACOES.valorMov)
        else
        VIEW_MOVIMENTACOES.valorMov
        end as valorMov,
        VIEW_MOVIMENTACOES.categoria,
        categorias_transferencia.emojiCategoria,
        VIEW_MOVIMENTACOES.banco,
        VIEW_MOVIMENTACOES.tipoOperID,
        VIEW_MOVIMENTACOES.tipoOperacao
        from VIEW_MOVIMENTACOES

        left join categorias_transferencia
        on categorias_transferencia.categID = VIEW_MOVIMENTACOES.categID

        ORDER BY
        data_hora_convertida desc
        limit 1
    ''')
    else:
        cursor.execute('''
            SELECT
            datetime(
            substr(data_hora,7,4) || '-' ||
            substr(data_hora,4,2) || '-' ||
            substr(data_hora,1,2) || ' ' ||
            substr(data_hora,12,8)
            ) as data_hora_convertida,
            VIEW_MOVIMENTACOES.categID,
            case 
            when VIEW_MOVIMENTACOES.tipoOperID = 0
            then
            -ABS(VIEW_MOVIMENTACOES.valorMov)
            else
            VIEW_MOVIMENTACOES.valorMov
            end as valorMov,
            VIEW_MOVIMENTACOES.categoria,
            categorias_transferencia.emojiCategoria,
            VIEW_MOVIMENTACOES.bancoID,
            VIEW_MOVIMENTACOES.banco,
            VIEW_MOVIMENTACOES.tipoOperID,
            VIEW_MOVIMENTACOES.tipoOperacao
            from VIEW_MOVIMENTACOES
    
            left join categorias_transferencia
            on categorias_transferencia.categID = VIEW_MOVIMENTACOES.categID

            WHERE
            VIEW_MOVIMENTACOES.bancoID = ?
            ORDER BY
            data_hora_convertida desc
            limit 1
        ''', (bancoID,))

    resultado = cursor.fetchone()

    cursor.close()
    conexao.close()

    return dict(resultado)