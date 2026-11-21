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
        tipoTransf integer not null,
        foreign key (categID) references CATEGORIAS_TRANSFERENCIA(categID),
        foreign key (bancoID) references BANCOS_USUARIO(bancoID)
    );
''')

conexao.commit()

cursor.close()
conexao.close()

#CREATE TABLE IF NOT EXISTS BANCOS_USUARIO (
#        bancoID INTEGER PRIMARY KEY AUTOINCREMENT,
#        nomeBanco varchar(255) not null,
#        saldoBanco REAL);