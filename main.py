import os
from dotenv import load_dotenv
import telebot
from telebot import types
from Model.transferenciaBanco import transferenciaBanco
from Model.transferenciaBanco import saqueBanco
from Model.transferenciaBanco import depositoBanco
from Model.listarBancos import listarBancos
from Model.listarCategoriasTransf import listarCategoriasTransf
from Model.especificarBanco import especificarBanco
from Model.especificarTipoTransfCateg import especificarTipoTransfCateg
from Model.especificarCateg import especificarCateg

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
                     f"<b>PENGUIN BOT - MENU PRINCIPAL</b>\nFala meu nobre, seja Bem-vindo, \nsou o PenguinBot.🐧 Do que precisas hoje?", 
                     reply_markup=tecladoMenuPrincipal, #Aplica o teclaod na mensagem
                     parse_mode="HTML") #Faz aceitar marcações HTML

    @bot.callback_query_handler(func=lambda clique: clique.data  == 'manager_banco') #Executa essa função quando o clique for no botao de callback_data = manager_banco
    def gerBancoMenu(clique: types.CallbackQuery): #informa a função que vai ser chamada quando o filtro aceitar o clique
        bot.answer_callback_query(clique.id) #Para o carregamento quando o bot receber o clique.id
        tecladoBancoMenu = types.InlineKeyboardMarkup(row_width=2)
        resposta = []

        for banco in listarBancos():
            resposta.append(f"{banco['nomeBanco']} {banco['emojiBanco']} - Saldo 💵: <b>R${banco['saldoBanco']}</b>")

            botaoBanco = types.InlineKeyboardButton(
                f"{banco['nomeBanco']} {banco['emojiBanco']}",
                callback_data=str(banco['bancoID'])
            )
            tecladoBancoMenu.add(botaoBanco) #Faz um for percorrendo cada banco no BD e criando um botao para o mesmo
            #Além disso, adiciona o callback_data como sendo o id do banco, callback_data só aceita TEXTOS

        textoFinal = "\n".join(resposta)


        bot.send_message(clique.message.chat.id,f"<b>PENGUIN BOT - MENU BANCO</b>\nSALDOS BANCÁRIOS\n\n{textoFinal}\n\nEscolha o banco de sua preferência:",
                         reply_markup=tecladoBancoMenu,
                         parse_mode="HTML")

        @bot.callback_query_handler(func=lambda clique: clique.data.isdigit())
        def menuEspecBanco(clique: types.CallbackQuery):
            bot.answer_callback_query(clique.id)
            bancoID = clique.data

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

            bot.send_message(clique.message.chat.id,f"<b>PENGUIN BOT - {especificarBanco(int(bancoID))['nomeBanco'].upper()} {especificarBanco(int(bancoID))['emojiBanco']}</b>\nOlá, você está realizando Operações no Banco do {especificarBanco(int(bancoID))['nomeBanco']} {especificarBanco(int(bancoID))['emojiBanco']}",
                             reply_markup=tecladoEspecBanco,
                             parse_mode="HTML")

            ## ----- FUNÇÃO SAQUE ----
            @bot.callback_query_handler(func=lambda clique: clique.data.startswith('saque'))
            def menuCategSaque(clique: types.CallbackQuery):
                bot.answer_callback_query(clique.id)
                bancoID = int(clique.data.split(':')[1])

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
                @bot.callback_query_handler(func=lambda clique: True)
                def digitarValor(clique: types.CallbackQuery):
                    bot.answer_callback_query(clique.id)
                    bancoID = int(clique.data.split(':')[1])
                    categID = int(clique.data.split(':')[0])

                    mensagem = bot.send_message(clique.message.chat.id,f"<b>PENGUIN BOT - SAQUE 💵⛔</b>\nSaldo Atual: R${especificarBanco(bancoID)['saldoBanco']}\n\nDigite o valor do Saque que deseja realizar:",
                                                parse_mode="HTML")

                    bot.register_next_step_handler(mensagem, processarValor, bancoID, categID)

                def processarValor(msg: types.Message, bancoID: int, categID: int):
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

                bot.send_message(clique.message.chat.id,f"<b>PENGUIN BOT - DEPÓSITO 💵❇️</b>\nEscolha a categória para qual você vai investir\no valor do Depósito:",
                                 parse_mode="HTML",
                                 reply_markup=tecladoCategDepos)

                @bot.callback_query_handler(func=lambda clique: int(clique.data.split(':')[0]) == 11)
                def digitarValor(clique: types.CallbackQuery):
                    bot.answer_callback_query(clique.id)
                    bancoID = int(clique.data.split(':')[1])
                    categID = int(clique.data.split(':')[0])

                    mensagem = bot.send_message(clique.message.chat.id,f"<b>PENGUIN BOT - SALDO EM CONTA 💵❇️</b>\nDigite o valor do depósito:",
                                                parse_mode="HTML")

                    bot.register_next_step_handler(mensagem, processarValor, bancoID, categID)
                def processarValor(msg: types.Message, bancoID: int, categID: int):
                    saldoAtual = especificarBanco(bancoID)['saldoBanco']
                    valorDep = float(msg.text)
                    depositoBanco(valorDep, bancoID, categID)

                    if (valorDep <= 0):
                        bot.send_message(msg.chat.id,f"<b>PENGUIN BOT - SALDO EM CONTA 💵❇️</b>\nDepósito não pode ser realizado com valor negativo ou 0",
                                         parse_mode="HTML")
                    else:
                        bot.send_message(msg.chat.id,f"<b>PENGUIN BOT - SALDO EM CONTA 💵❇️</b>\nSaldo Anterior: {saldoAtual}\nSaldo Atual: {especificarBanco(bancoID)['saldoBanco']}",
                                        parse_mode="HTML")


                #@bot.callback_query_handler(func=lambda clique: clique.data == 'transferenciaData' bancoID: bancoID)
            #def digitarValorTransf(bancoID: bancoID, clique: types.CallbackQuery):

            

    #bot.answer_callback_query(chamada.id)
    #bot.send_message(chamada.message.chat.id, resposta)

bot.infinity_polling()