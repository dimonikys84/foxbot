import telegram
from telegram.ext import CommandHandler, Updater
import ts3
from tools import ChannelTreeNode
from time import gmtime, strftime
import time
import logging
import anims, settings

token = settings.token
ts3adress = settings.ts3adress
ts3username = settings.ts3username
ts3password = settings.ts3password
announceMembers = settings.announceMembers

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

print(
    '******Bot started******',
    '\nToken: {}'.format(token),
    '\nts3adress: {}'.format(ts3adress),
    '\nts3username: {}'.format(ts3username),
    '\nts3password: {}'.format(ts3password),
    '\n\n'
    )

bot = telegram.Bot(token=token)
updater = Updater(token=token)
dispatcher = updater.dispatcher

def getNow():
    return strftime("%Y-%m-%d %H:%M:%S", gmtime())

def stat(bot, update):
    print(getNow(),'requested command /stat')
    print('Chat id is: ',update.message.chat_id)
    text_caps = "I'm good"
    bot.sendMessage(chat_id=update.message.chat_id, text=text_caps)

def pokeAll(bot, update):
    print(getNow(),'requested command /pokeall')
    pokeText = update.message.text.replace('/pokeAll','')
    print('update text: ',update);
    with ts3.query.TS3Connection(ts3adress) as ts3conn:
        ts3conn.login(
                client_login_name=ts3username,
                client_login_password=ts3password
        )
        ts3conn.use(sid=1)
        for client in ts3conn.clientlist():
            print('client', client)
            if client['client_type'] != '1':
                msg = "{}".format(pokeText)
                ts3conn.clientpoke(clid=client["clid"], msg=msg)
    bot.sendMessage(chat_id=update.message.chat_id, text='Вы покнули на сервер: {}'.format(pokeText))

def getList(bot, update):
    print(getNow(),'requested command /getlist')
    with ts3.query.TS3Connection(ts3adress) as ts3conn:
        ts3conn.login(
                        client_login_name=ts3username,
                        client_login_password=ts3password
                    )

        TreeNode = ChannelTreeNode.ChannelTreeNode
        tree = TreeNode.build_tree(ts3conn, sid=1).string()
        bot.sendMessage(chat_id=update.message.chat_id, text=tree)

def fun(bot,update):
    print(getNow(),'requested command /fun')
    msg = ''
    first = False
    for an in anims.funAnim:
        if first == False:
            msg = bot.sendMessage(chat_id=update.message.chat_id, text=an)
            first = True
        else:
            bot.editMessageText(chat_id=msg.chat.id,message_id=msg.message_id, text=an)
        time.sleep(1)

def announce(bot,update):
    print(getNow(),'requested command /announce')
    AnnText = '{}\n'.format(announceMembers)
    AnnText += update.message.text.replace('/announce', '')
    bot.sendMessage(chat_id=update.message.chat_id, text=AnnText)

def guardians(bot,update):
    print(getNow(),'requested command /guardians')
    AnnText = '{}\n'.format(announceMembers)
    AnnText += update.message.text.replace('/guardians', '')
    bot.sendMessage(chat_id=update.message.chat_id, text=AnnText)

dispatcher.addHandler(CommandHandler('stat', stat))
dispatcher.addHandler(CommandHandler('getlist', getList))
dispatcher.addHandler(CommandHandler('fun', fun))
dispatcher.addHandler(CommandHandler('pokeall', pokeAll))
dispatcher.addHandler(CommandHandler('announce', announce))
dispatcher.addHandler(CommandHandler('guardians', guardians))
updater.start_polling()

updater.idle()
