import telebot
from games import games_all_ordenado
import os
# Token do seu bot do Telegram
TOKEN = os.environ.get('API_KEY')

# Criação do objeto bot
bot = telebot.TeleBot(TOKEN)

# Dicionário com os jogos disponíveis
jogos = games_all_ordenado
numero_de_jogos = len(jogos)
def format_error_message(error, button):
    return f"Ocorreu um erro no bot!\n\nBotão de jogo: {button}\n\nDetalhes do erro:\n{str(error)}"
def exibir_lista_jogos(chat_id, message_id, pagina_atual):
    try:
        jogos_list = list(jogos.keys())
        total_jogos = len(jogos_list)

        max_jogos_por_pagina = 20

        markup = telebot.types.InlineKeyboardMarkup(row_width=2)
        total_paginas = (total_jogos + max_jogos_por_pagina - 1) // max_jogos_por_pagina
        # Calcular o índice inicial e final da lista de jogos para a página atual
        inicio = (pagina_atual - 1) * max_jogos_por_pagina
        fim = inicio + max_jogos_por_pagina

        # Adicionar botões para os jogos da página atual
        button_row = []
        for i in range(inicio, fim):
            if i >= total_jogos:
                break
            jogo = jogos_list[i]
            button_row.append(telebot.types.InlineKeyboardButton(jogo, callback_data=jogo))

            # Adicionar os botões em pares de dois
            if len(button_row) == 2 or i == fim - 1:
                markup.add(*button_row)
                button_row = []

        # Verificar se há mais jogos para exibir
        if fim < total_jogos:
            markup.add(telebot.types.InlineKeyboardButton("Avançar", callback_data=f"avançar:{pagina_atual}"))
        if pagina_atual > 1:
            markup.add(telebot.types.InlineKeyboardButton("Voltar", callback_data=f"voltar:{pagina_atual}"))

        mensagem = f"Lista de Jogos Disponíveis (Página {pagina_atual} de {total_paginas}):"
        bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=mensagem, reply_markup=markup)
    except Exception as e:
        bot.send_message(chat_id, f"AH NÃO!!! PARECE QUE OCORREU UM ERRO AO EXIBIR A LISTA DE JOGOS DISPONIVEIS😕\n\nnão se preocupe estamos cientes do erro e vamos resolver o problema o mais rapido possivel!")
        # Envia mensagem de erro para o administrador com as informações relevantes
        error_message = format_error_message(e, "Lista de Jogos Disponíveis")
        bot.send_message(os.environ.get('id_adm'), error_message)


# Comando /start
@bot.message_handler(commands=['start'])
def start(message):
    chat_id = message.chat.id
    try:
        bot.send_message(chat_id, (f"""Bem-vindo!

Eu sou um bot gratuito, desenvolvido para tornar sua experiência gamer ainda mais incrível. Aqui, você não precisa pagar nada! 😎

Utilizamos um encurtador de link para manter o bot ativo e garantir o acesso às contas. Antes de obter o login e a senha de cada conta, é necessário passar pelo encurtador.

Para mais informações sobre o bot e como passar pelo encurtador, clique aqui: /help.

No momento tenho mais de {numero_de_jogos} jogos disponives e futuramente suportarei mais!!
Estou aqui para tornar sua jornada gamer mais acessível e emocionante. Aproveite ao máximo essa oportunidade!"""))

        markup = telebot.types.InlineKeyboardMarkup()
        markup.add(telebot.types.InlineKeyboardButton("Ver Jogos Disponíveis", callback_data="ver_jogos"))
        bot.send_message(chat_id, "Selecione uma opção:", reply_markup=markup)
    except Exception as e:
        bot.send_message(chat_id, f"Ocorreu um erro ao iniciar o bot")


# Comando /help
@bot.message_handler(commands=['help'])
def help(message):
    try:
        bot.send_message(message.chat.id, """TERMOS DO BOT: Este bot é uma ferramenta desenvolvida independentemente e não possui nenhuma afiliação ou conexão com as contas fornecidas ou suas origens. seu propósito é proporcionar acesso a contas previamente disponibilizadas publicamente na internet, buscando ampliar a comunidade gamer e auxiliar aqueles que desejam desfrutar dos jogos, mas podem enfrentar limitações financeiras.

É importante ressaltar que o bot não é responsável pela criação ou divulgação original dessas contas. ele Apenas as reune em um único local para facilitar o acesso e fornecer uma experiência mais conveniente aos usuários.

Enquanto o bot tem como missão democratizar o acesso aos jogos, encorajamos veementemente que, caso você possua condições financeiras suficientes, adquira os jogos oficialmente na loja da Steam. Ao fazer isso, você estará apoiando os talentosos desenvolvedores e contribuindo diretamente para o crescimento e aprimoramento da indústria de jogos.

Salientamos que a utilização das contas disponibilizadas é de total responsabilidade do usuário. É imprescindível que você siga as políticas, os termos de uso e as diretrizes estabelecidas pela Steam, garantindo assim uma experiência ética e em conformidade com as regras.

Nós, criadores deste bot, visamos somente a disseminação da cultura gamer e a disseminação do acesso aos jogos, sempre respeitando os direitos autorais e a integridade dos desenvolvedores.

Aproveite ao máximo essa plataforma para se divertir com os jogos disponíveis.

_________________

TUTORIAL PARA PASSAR PELO ENCURTADOR

obs: esse é apenas um video de exemplo, você não deve baixar nada, depois que passar pelo encurtador você sera redirecionado para um site com um texto com o login e senha da sua conta.


VOCÊ NÃO PRECISA FAZER NENHUM DOWNLOAD!!

link do video de tutorial: https://www.youtube.com/shorts/mqkd4qJSGZ8""")
    except Exception as e:
        bot.send_message(message.chat.id, f"Ocorreu um erro ao exibir a mensagem de ajuda")


# Função para lidar com as mensagens do usuário
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    chat_id = message.chat.id
    try:
        # Mensagem padrão para qualquer outra mensagem irrelevante
        bot.send_message(chat_id, (f"""ola!

Eu sou um bot gratuito, desenvolvido para tornar sua experiência gamer ainda mais incrível. Aqui, você não precisa pagar nada! 😁

Utilizamos um encurtador de link para manter o bot ativo e garantir o acesso às contas. Antes de obter o login e a senha de cada conta, é necessário passar pelo encurtador.

Para mais informações sobre o bot e como passar pelo encurtador, clique aqui: /help.

No momento tenho mais de {numero_de_jogos} jogos disponives e futuramente suportarei mais!!
Estou aqui para tornar sua jornada gamer mais acessível e emocionante. Aproveite ao máximo essa oportunidade!"""))
        markup = telebot.types.InlineKeyboardMarkup()
        markup.add(telebot.types.InlineKeyboardButton("Ver Jogos Disponíveis", callback_data="ver_jogos"))
        bot.send_message(chat_id, "Selecione uma opção:", reply_markup=markup)
    except Exception as e:
        bot.send_message(chat_id, f"AH NÃO!!! PARECE QUE OCORREU UM ERRO AO LIDAR COM SUA MENSAGEM.\n\nnão se preocupe! resolveremos o problema o mais rapido posssivel😇")
        # Envia mensagem de erro para o administrador com as informações relevantes
        error_message = format_error_message(e, "Mensagem do usuário")
        bot.send_message(os.environ.get('id_adm'), error_message)


# Callback para os botões
@bot.callback_query_handler(func=lambda call: True)
def handle_callback(call):
    chat_id = call.message.chat.id
    message_id = int(call.message.message_id)
    callback_data = call.data

    try:
        if callback_data.startswith("avançar"):
            pagina_atual = int(callback_data.split(":")[1])
            exibir_lista_jogos(chat_id, message_id, pagina_atual + 1)
        elif callback_data.startswith("voltar"):
            pagina_atual = int(callback_data.split(":")[1])
            exibir_lista_jogos(chat_id, message_id, pagina_atual - 1)

        # Verificar se o botão "Ver Jogos Disponíveis" foi clicado
        if callback_data == "ver_jogos":
            exibir_lista_jogos(chat_id, message_id, 1)

        elif callback_data in jogos:
            jogo_selecionado = jogos[callback_data]
            imagem = jogo_selecionado["link da imagem"]
            descricao = jogo_selecionado["descrição"]
            link_encurtador = jogo_selecionado["link do encurtador"]
            mensagem = f"\n\n{descricao}"

            markup = telebot.types.InlineKeyboardMarkup()

            link_button = telebot.types.InlineKeyboardButton(text="LINK PARA SUA CONTA", url=link_encurtador)

            markup.add(link_button)

            bot.send_photo(chat_id, imagem, caption=mensagem, reply_markup=markup)
    except Exception as e:
        bot.send_message(chat_id, f"AH NÃO!!! PARECE QUE TEVE UM ERRO NA SOLICITAÇÃO DESSE JOGO😔\n\n por favor escolha outro jogo, resolveremos o problema o mais rapido o possivel.")
        # Envia mensagem de erro para o administrador com as informações relevantes
        error_message = format_error_message(e, callback_data)
        bot.send_message(os.environ.get('id_adm'), error_message)
try:
    # Iniciar o bot
    bot.polling()
except Exception as e:
   # Envia mensagem de erro para o administrador com as informações relevantes
    error_message = format_error_message(e, "Erro global")
    bot.send_message(os.environ.get('id_adm'), error_message)
