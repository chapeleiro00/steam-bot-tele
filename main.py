import telebot
from telebot import types
from games import games_all

bot_token = "5872441280:AAGeSuGexyNIWniOhsag-bBLdXQmZIlnWnQ"
bot = telebot.TeleBot(bot_token)

jogos = games_all

@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    button1 = types.KeyboardButton('Ver jogos disponíveis')
    button2 = types.KeyboardButton('Tutorial')
    markup.add(button1, button2)
    bot.send_message(message.chat.id, '''Bem-vindo!\n\nEsse bot é totalmente grátis e você não precisa pagar por nada! 😁\nUtilizamos um encurtador de link para manter o bot, para chegar até o login e senha de cada conta você deve primeiro passar por 2 links de encurtador.\n\nSe você não sabe como passar pelo encurtador, clique no botão de tutorial para aprender.''', reply_markup=markup)

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    if message.text == 'Ver jogos disponíveis':
        markup = types.InlineKeyboardMarkup(row_width=1)
        for jogo in jogos:
            button = types.InlineKeyboardButton(jogo, callback_data=jogo)
            markup.add(button)
        bot.send_message(message.chat.id, 'Selecione um jogo:', reply_markup=markup)
    elif message.text == 'Tutorial':
        bot.send_message(message.chat.id, 'esse é o tutorial para passar pelo primeiro link: https://www.youtube.com/shorts/jZZ20hKqby0')
        bot.send_message(message.chat.id, 'assista para passar pelo segundo link: https://www.youtube.com/shorts/MXnjF2_-Qoc')
    else:
        bot.send_message(message.chat.id, 'Desculpe, não entendi sua mensagem, eu sou um bot portanto so posso te ajudar atravez de comandos🙁. Por favor, selecione uma opção válida, ou clique aqui: /start.')

@bot.callback_query_handler(func=lambda call: True)
def handle_callback(call):
    jogo = call.data
    if jogo in jogos:
        game_info = jogos[jogo]
        photo_url = game_info["link da imagem"]
        description = game_info["descrição"]
        shortener_link = game_info["link do encurtador"]

        photo_message = bot.send_photo(call.message.chat.id, photo_url)
        bot.send_message(call.message.chat.id, description)

        markup = types.InlineKeyboardMarkup(row_width=1)
        button = types.InlineKeyboardButton("LINK PARA SUA CONTA", url=shortener_link)
        markup.add(button)
        bot.send_message(call.message.chat.id, "Obs: Você deverá passar pelos links do encurtador até chegar no final onde estarão os dados de login e senha da sua conta.", reply_markup=markup)

bot.polling()
