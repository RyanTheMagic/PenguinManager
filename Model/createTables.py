import sqlite3

conexao = sqlite3.connect('bot.db')
cursor = conexao.cursor()

cursor.executescript('''
    PRAGMA foreign_keys = ON;

    CREATE TABLE IF NOT EXISTS BANCOS_USUARIO (
        bancoID INTEGER PRIMARY KEY AUTOINCREMENT,
        nomeBanco varchar(255) not null,
        saldoBanco REAL not null default 0,
        cofrinhoBanco REAL not null default 0,
        emojiBanco varchar(10) not null default '🏦'
    );

    CREATE TABLE IF NOT EXISTS CATEGORIAS_TRANSFERENCIA (
        categID INTEGER PRIMARY KEY AUTOINCREMENT,
        nomeCategoria varchar(255) not null,
        tipoTransf int not null,
        emojiCategoria varchar(10) not null default '📊'
    );

    CREATE TABLE IF NOT EXISTS RELATORIO_MOVIMENTACOES (
        numped INTEGER PRIMARY KEY AUTOINCREMENT,
        valorMov REAL not null default 0,
        data_hora TEXT DEFAULT (strftime('%d-%m-%Y %H:%M:%S', 'now', 'localtime')),
        categID integer not null,
        bancoID integer not null,
        foreign key (categID) references CATEGORIAS_TRANSFERENCIA(categID),
        foreign key (bancoID) references BANCOS_USUARIO(bancoID)
    );

    CREATE TABLE IF NOT EXISTS CATEGORIAS_TIPOOPER (
        tipooperID integer primary key autoincrement,
        nomeTipoOper varchar(255) not null
    );
    DROP VIEW IF EXISTS VIEW_MOVIMENTACOES;

    create view VIEW_MOVIMENTACOES AS
    select
    RELATORIO_MOVIMENTACOES.numped,
    RELATORIO_MOVIMENTACOES.valorMov,
    RELATORIO_MOVIMENTACOES.data_hora,
    RELATORIO_MOVIMENTACOES.categID,
    CATEGORIAS_TRANSFERENCIA.nomeCategoria as categoria,
    CATEGORIAS_TRANSFERENCIA.tipoTransf as tipoOperID,
    CATEGORIAS_TIPOOPER.nomeTipoOper as tipoOperacao,
    RELATORIO_MOVIMENTACOES.bancoID,
    BANCOS_USUARIO.nomeBanco as banco
    from RELATORIO_MOVIMENTACOES

    left join BANCOS_USUARIO
    on BANCOS_USUARIO.bancoID = RELATORIO_MOVIMENTACOES.bancoID

    left join CATEGORIAS_TRANSFERENCIA
    on CATEGORIAS_TRANSFERENCIA.categID = RELATORIO_MOVIMENTACOES.categID

    left join CATEGORIAS_TIPOOPER
    on CATEGORIAS_TIPOOPER.tipooperID = CATEGORIAS_TRANSFERENCIA.tipoTransf;
''')

conexao.commit()

cursor.close()
conexao.close()

#CREATE TABLE IF NOT EXISTS BANCOS_USUARIO (
#        bancoID INTEGER PRIMARY KEY AUTOINCREMENT,
#        nomeBanco varchar(255) not null,
#        saldoBanco REAL);