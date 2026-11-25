import os
from dotenv import load_dotenv
import telebot
from datetime import datetime
from telebot import types
from Model.transferenciaBanco import transferenciaBanco
from Model.transferenciaBanco import saqueBanco
from Model.transferenciaBanco import depositoBanco
from Model.transferenciaBanco import guardarDinheiro
from Model.transferenciaBanco import sacarCofre
from Model.listarBancos import listarBancos
from Model.listarCategoriasTransf import listarCategoriasTransf
from Model.buscarUltMov import buscarUltMov
from Model.especificarBanco import especificarBanco
from Model.especificarTipoTransfCateg import especificarTipoTransfCateg
from Model.especificarCateg import especificarCateg
from Model.buscarMovTipoOper import buscarMovTipoOper


load_dotenv()

bot = telebot.TeleBot(os.getenv("tokenAPI"))

@bot.message_handler(['start'])
def testeMenu(msg: types.Message):
    tecladoTeste = types.InlineKeyboardMarkup(row_width=3)
    
    botoes = []
    for categoria in especificarTipoTransfCateg(0):
        botao = types.InlineKeyboardButton(
            f"{categoria['nomeCategoria']}",
            callback_data=str({categoria['categID']})
        )
        botoes.append(botao)

    tecladoTeste.add(*botoes)

    bot.send_message(msg.chat.id,
                     "Fala meu Teste",
                     reply_markup=tecladoTeste)


@bot.message_handler(["menu"])
def mostrarMenuPrincipal(msg:types.Message): #Define que o menu vai abrir quando for digitado /menu
    tecladoMenuPrincipal = types.InlineKeyboardMarkup(row_width=2) #Cria teclado do Menu

    saldoPrincipal = 0
    cofre = 0

    for banco in listarBancos():
        saldoPrincipal += banco['saldoBanco']
        cofre += banco['cofrinhoBanco']

    patrimonio = saldoPrincipal + cofre

    botao_nome = types.InlineKeyboardButton(
        "Bancos 🪙",
        callback_data="manager_banco" #ID do Botão
    )
    botao_sobre = types.InlineKeyboardButton(
        "Editar descrição",
        callback_data="editar_descricao"
    )

    tecladoMenuPrincipal.add(botao_nome, botao_sobre) #Adiciona os botões

    bot.send_message(msg.chat.id, #Informa o chat que o Bot vai enviar a mensagem
                     f"<b>PENGUIN BOT - MENU PRINCIPAL</b>\nFala meu nobre, seja Bem-vindo!\nSou o PenguinBot 🐧. Do que precisas hoje?\n\n━━━━━━━━━━━━━━\n💰 Patrimônio: R$ {patrimonio}\n💵 Em contas: R$ {saldoPrincipal}\n🐷 Nos cofres: R$ {cofre}\n━━━━━━━━━━━━━━\n\n🕐 Última: {buscarUltMov()['emojiCategoria']} {buscarUltMov()['categoria']} · R$ {buscarUltMov()['valorMov']}\n", 
                     reply_markup=tecladoMenuPrincipal, #Aplica o teclaod na mensagem
                     parse_mode="HTML") #Faz aceitar marcações HTML

    @bot.callback_query_handler(func=lambda clique: clique.data  == 'manager_banco') #Executa essa função quando o clique for no botao de callback_data = manager_banco
    def gerBancoMenu(clique: types.CallbackQuery): #informa a função que vai ser chamada quando o filtro aceitar o clique
        mes_ano = datetime.now().strftime('%Y-%m') #Formata no formato '2026-11'
        bot.answer_callback_query(clique.id) #Para o carregamento quando o bot receber o clique.id
        tecladoBancoMenu = types.InlineKeyboardMarkup(row_width=2)
        resposta = []

        for banco in listarBancos():
            resposta.append(f"{banco['nomeBanco']} {banco['emojiBanco']}\n💵 Conta : R$ {banco['saldoBanco']}\n🐷 Cofre: R$ {banco['cofrinhoBanco']}\n")

            botaoBanco = types.InlineKeyboardButton(
                f"{banco['nomeBanco']} {banco['emojiBanco']}",
                callback_data=str(banco['bancoID'])
            )
            tecladoBancoMenu.add(botaoBanco) #Faz um for percorrendo cada banco no BD e criando um botao para o mesmo
            #Além disso, adiciona o callback_data como sendo o id do banco, callback_data só aceita TEXTOS

        textoFinal = "\n".join(resposta)


        bot.send_message(clique.message.chat.id,f"<b>PENGUIN BOT - MENU BANCOS</b>\nCOLÔNIA DE CONTAS\n\n━━━━━━━━━━━━━━\n{textoFinal}━━━━━━━━━━━━━━\n\n<b>Dados Mensais:</b>\n✅ Entrada: R$ {buscarMovTipoOper(1,mes_ano)['total']}\n❌ Saida: R$ {buscarMovTipoOper(0,mes_ano)['total']} \n\nEscolha o banco de sua preferência:",
                         reply_markup=tecladoBancoMenu,
                         parse_mode="HTML")
        # ---- MENU GERAL BANCOS -- 
        @bot.callback_query_handler(func=lambda clique: clique.data.isdigit())
        def menuEspecBanco(clique: types.CallbackQuery):
            bot.answer_callback_query(clique.id)
            mes_ano = datetime.now().strftime('%Y-%m')
            bancoID = int(clique.data) #Passa o ID do Banco na variavel
            saldo = especificarBanco(bancoID)['saldoBanco']
            cofre = especificarBanco(bancoID)['cofrinhoBanco']
            patrimonio = saldo + cofre

            tecladoEspecBanco = types.InlineKeyboardMarkup(row_width=2)

            botaoSaque = types.InlineKeyboardButton(
                "Saque 💵⛔",
                callback_data=f"saque:{bancoID}"
            )

            botaoDeposito = types.InlineKeyboardButton(
                "Depósito 💵❇️",
                callback_data=f"deposito:{bancoID}"
            )

            botaoGuardarDin = types.InlineKeyboardButton(
                "Guardar R$ 🐖❇️",
                callback_data=f"guardardin:{bancoID}"
            )

            botaoResgatarCofre = types.InlineKeyboardButton(
                "Sacar Cofre ⛔🐖",
                callback_data=f"resgatarcofre:{bancoID}"
            )

            botaoTransfBanco = types.InlineKeyboardButton(
                "Transf. Entre Bancos 🏦➡️🏦",
                callback_data=f"transfbanco:{bancoID}"
            )

            tecladoEspecBanco.add(botaoSaque, botaoDeposito,botaoGuardarDin,botaoResgatarCofre,botaoTransfBanco)

            bot.send_message(clique.message.chat.id,f"<b>PENGUIN BOT - {especificarBanco(bancoID)['nomeBanco'].upper()} {especificarBanco(bancoID)['emojiBanco']}</b>\n<i>Olá, Seja Bem-vindo ao {especificarBanco(bancoID)['nomeBanco']}!</i>\n\n━━━━━━━━━━━━━━\n💰 Patrimônio: R$ {patrimonio}\n💵 Conta: R$ {saldo}\n🐷 Cofre: R$ {cofre}\n✅ Entrada: R$ {buscarMovTipoOper(1,mes_ano,bancoID)['total']}\n❌ Saida: R$ {buscarMovTipoOper(0,mes_ano,bancoID)['total']}\n🕐 Última: {buscarUltMov(bancoID)['emojiCategoria']} <b>{buscarUltMov(bancoID)['categoria']} · R$ {buscarUltMov(bancoID)['valorMov']}</b>\n━━━━━━━━━━━━━━\n\nQual operação deseja realizar?",
                             reply_markup=tecladoEspecBanco,
                             parse_mode="HTML")

            ## ----- FUNÇÃO SAQUE ----
            @bot.callback_query_handler(func=lambda clique: clique.data.startswith('saque'))
            def menuCategSaque(clique: types.CallbackQuery):
                bot.answer_callback_query(clique.id)
                bancoID = int(clique.data.split(':')[1]) # Manipulação de String, divindo em indice a cada ":" para puxar o id do banco

                tecladoCategSaque = types.InlineKeyboardMarkup(row_width=2)

                botoes = []

                for categ in especificarTipoTransfCateg(0):
                    botaoCateg = types.InlineKeyboardButton(
                        categ['nomeCategoria'],
                        callback_data=f"{categ['categID']}:{bancoID}"
                    )
                    botoes.append(botaoCateg)

                tecladoCategSaque.add(*botoes)

                bot.send_message(clique.message.chat.id,f"<b>PENGUIN BOT - SAQUE 💵⛔</b>\nEscolha a categória para qual você vai investir\no valor do Saque:",
                                reply_markup=tecladoCategSaque,
                                parse_mode="HTML")

                @bot.callback_query_handler(func=lambda clique: especificarCateg(int(clique.data.split(':')[0]))['tipoTransf'] == 0)
                def digitarValorSaque(clique: types.CallbackQuery):
                    bot.answer_callback_query(clique.id)
                    bancoID = int(clique.data.split(':')[1])
                    categID = int(clique.data.split(':')[0])

                    mensagem = bot.send_message(clique.message.chat.id,f"<b>PENGUIN BOT - SAQUE 💵⛔</b>\nSaldo Atual: R${especificarBanco(bancoID)['saldoBanco']}\n\nDigite o valor do Saque que deseja realizar:",
                                                parse_mode="HTML")

                    bot.register_next_step_handler(mensagem, processarValorSaque, bancoID, categID)
                    # Registra uma função para processar a próxima mensagem pelo usuário, passa
                    # as variaveis bancoID e categID como parametros

                def processarValorSaque(msg: types.Message, bancoID: int, categID: int):
                    saldoAtual = especificarBanco(bancoID)['saldoBanco']
                    valorSaque = float(msg.text)

                    if (valorSaque > saldoAtual):
                        bot.send_message(msg.chat.id,f'<b>PENGUIN BOT - FALHA NO SAQUE 💵⛔</b>\n\nSaldo Atual: {saldoAtual}\nValor Saque: {valorSaque}\n\nSaldo Insuficiente para realização do Saque.',
                                         parse_mode="HTML")
                    elif (valorSaque <= 0):
                        bot.send_message(msg.chat.id,f"<b>PENGUIN BOT - FALHA NO SAQUE 💵⛔</b>\n\nValor do Saque não pode ser menor ou igual a 0",
                                         parse_mode="HTML")
                    else:
                        saqueBanco(valorSaque,bancoID, categID)
                        bot.send_message(msg.chat.id,f"<b>PENGUIN BOT - SAQUE REALIZADO 💵⛔</b>\n\nBanco: {especificarBanco(bancoID)['nomeBanco']} {especificarBanco(bancoID)['emojiBanco']}\nCategoria: {especificarCateg(categID)['nomeCategoria']} {especificarCateg(categID)['emojiCategoria']}\nSaque: R${valorSaque}\nSaldo Atual: R${especificarBanco(bancoID)['saldoBanco']}",
                                         parse_mode="HTML")

            ## ----- FUNÇÃO DEPOSITO ----
            @bot.callback_query_handler(func=lambda clique: clique.data.startswith('deposito'))    
            def menuCategDepos(clique: types.CallbackQuery):
                bot.answer_callback_query(clique.id)
                bancoID = int(clique.data.split(':')[1])

                tecladoCategDepos = types.InlineKeyboardMarkup(row_width=3)

                botoes = []

                for categoria in especificarTipoTransfCateg(1):
                    botaoCateg = types.InlineKeyboardButton(
                        f"{categoria['nomeCategoria']}",
                        callback_data=f"{categoria['categID']}:{bancoID}"
                    )
                    botoes.append(botaoCateg)

                tecladoCategDepos.add(*botoes)

                bot.send_message(clique.message.chat.id,f"<b>PENGUIN BOT - DEPÓSITO 💵❇️</b>\n\nEscolha a categória para qual você vai investir\no valor do Depósito:",
                                 parse_mode="HTML",
                                 reply_markup=tecladoCategDepos)

                print(clique.data.split(':')[0] == '11')
                # -- SALDO EM CONTA
                @bot.callback_query_handler(func=lambda clique: int(clique.data.split(':')[0]) == 11)
                def digitarValorDepSald(clique: types.CallbackQuery):
                    bot.answer_callback_query(clique.id)
                    bancoID = int(clique.data.split(':')[1])
                    categID = int(clique.data.split(':')[0])

                    mensagem = bot.send_message(clique.message.chat.id,f"<b>PENGUIN BOT - SALDO EM CONTA 💵❇️</b>\nDigite o valor do depósito:",
                                                parse_mode="HTML")

                    bot.register_next_step_handler(mensagem, processarValorDepSald, bancoID, categID)
                def processarValorDepSald(msg: types.Message, bancoID: int, categID: int):
                    saldoAtual = especificarBanco(bancoID)['saldoBanco']
                    valorDep = float(msg.text)

                    if (valorDep <= 0):
                        bot.send_message(msg.chat.id,f"<b>PENGUIN BOT - SALDO EM CONTA 💵❇️</b>\n\n<b>FALHA NO DEPOSITO ❌</b>\n<i>Log: Depósito não pode ser realizado com valor negativo ou 0</i>",
                                         parse_mode="HTML")
                    else:
                        depositoBanco(valorDep, bancoID, categID)
                        bot.send_message(msg.chat.id,f"<b>PENGUIN BOT - SALDO EM CONTA 💵❇️</b>\nSaldo Anterior: {saldoAtual}\nSaldo Atual: {especificarBanco(bancoID)['saldoBanco']}",
                                        parse_mode="HTML")
                ## -- PORQUINHO
                @bot.callback_query_handler(func=lambda clique: int(clique.data.split(':')[0]) == 12)
                def digitarValorDepPorq(clique: types.CallbackQuery):
                    bot.answer_callback_query(clique.id)
                    bancoID = int(clique.data.split(':')[1])
                    categID = int(clique.data.split(':')[0])

                    mensagem = bot.send_message(clique.message.chat.id,f"<b>PENGUIN BOT - PORQUINHO 💵❇️</b>\nDigite o valor do depósito:",
                                                parse_mode="HTML")

                    bot.register_next_step_handler(mensagem, processarValorDepPorq, bancoID, categID)

                def processarValorDepPorq(msg: types.Message, bancoID: int, categID: int):
                    saldoAtual = especificarBanco(bancoID)['saldoBanco']
                    cofreAtual = especificarBanco(bancoID)['cofrinhoBanco']
                    valorDep = float(msg.text)

                    if (valorDep <= 0):
                        bot.send_message(msg.chat.id,f"<b>PENGUIN BOT - PORQUINHO 💵❇️</b>\n\n<b>FALHA NO DEPOSITO ❌</b>\n<i>Log: Depósito não pode ser realizado com valor negativo ou 0</i>",
                                         parse_mode="HTML")
                    else:
                        depositoBanco(valorDep, bancoID, categID)
                        bot.send_message(msg.chat.id,f'<b>PENGUIN BOT - PORQUINHO 💵❇️</b>\nSaldo Anterior: {saldoAtual}\nSaldo Atual: {especificarBanco(bancoID)['saldoBanco']}\nCofre Anterior: {cofreAtual}\nCofre Atual: {especificarBanco(bancoID)['cofrinhoBanco']}',
                                         parse_mode="HTML")

            @bot.callback_query_handler(func=lambda clique: clique.data.startswith('guardardin'))
            def digitarValorGuardar(clique: types.CallbackQuery):
                bot.answer_callback_query(clique.id)
                bancoID = int(clique.data.split(':')[1])
                saldoDisponivel = especificarBanco(bancoID)['saldoBanco']

                mensagem = bot.send_message(clique.message.chat.id,f"<b>PENGUIN BOT - GUARDAR R$ 🐖❇️</b>\n\nSaldo Disponível: R${saldoDisponivel}\nDigite o valor que deseja transferir para o cofre:",
                                            parse_mode="HTML")

                bot.register_next_step_handler(mensagem,processarValorGuardar,bancoID)

            def processarValorGuardar(msg: types.Message, bancoID: int):
                valorGuardar = float(msg.text)
                saldoAtual = especificarBanco(bancoID)['saldoBanco']
                cofreAtual = especificarBanco(bancoID)['cofrinhoBanco']

                if (valorGuardar > saldoAtual):
                    bot.send_message(msg.chat.id,f"<b>PENGUIN BOT - GUARDAR R$ 🐖❇️</b>\n\n<b>FALHA AO INVESTIR ❌</b>\n<i>O valor informado é maior que o Saldo em conta</i>",
                                     parse_mode="HTML")
                else:
                    guardarDinheiro(valorGuardar,bancoID)
                    bot.send_message(msg.chat.id,f"<b>PENGUIN BOT - GUARDAR R$ 🐖❇️</b>\n\n<b>Investimento Realizado</b>",
                                                         parse_mode="HTML")

            @bot.callback_query_handler(func=lambda clique: clique.data.startswith('resgatarcofre'))
            def digitarValorResgatar(clique:types.CallbackQuery):
                bot.answer_callback_query(clique.id)
                bancoID = int(clique.data.split(':')[1])
                cofreDisponivel = especificarBanco(bancoID)['cofrinhoBanco']

                mensagem = bot.send_message(clique.message.chat.id,f"<b>PENGUIN BOT - SACAR COFRE ⛔🐖</b>\n\nSaldo Disponível: R${cofreDisponivel}\nDigite o valor que deseja resgatar no cofre:",
                                            parse_mode="HTML")

                bot.register_next_step_handler(mensagem, processarValorResgatar, bancoID)

            def processarValorResgatar(msg: types.Message, bancoID: int):
                valorResgatado = float(msg.text)
                saldoAtual = especificarBanco(bancoID)['saldoBanco']
                cofreAtual = especificarBanco(bancoID)['cofrinhoBanco']

                if (valorResgatado > cofreAtual):
                    bot.send_message(msg.chat.id, f"<b>PENGUIN BOT - SACAR COFRE ⛔🐖</b>\n\n<b>FALHA AO SACAR ❌</b>\n<i>O valor informado é maior que o Saldo no Cofre</i>",
                                     parse_mode="HTML")
                else:
                    sacarCofre(valorResgatado,bancoID)
                    bot.send_message(msg.chat.id,f"<b>PENGUIN BOT - SACAR COFRE ⛔🐖</b>\n\nSaldo Anterior: {saldoAtual}\nSaldo Atual: {especificarBanco(bancoID)['saldoBanco']}\nCofre Anterior: {cofreAtual}\nCofre Atual: {especificarBanco(bancoID)['cofrinhoBanco']}",
                                     parse_mode="HTML")




                #@bot.callback_query_handler(func=lambda clique: clique.data == 'transferenciaData' bancoID: bancoID)
            #def digitarValorTransf(bancoID: bancoID, clique: types.CallbackQuery):

            

    #bot.answer_callback_query(chamada.id)
    #bot.send_message(chamada.message.chat.id, resposta)

bot.infinity_polling()