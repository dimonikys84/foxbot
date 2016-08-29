import telegram
import ts3
import logging
from configparser import SafeConfigParser

parser = SafeConfigParser()
parser.read('settings.ini')

token = parser.get('main','token')
ts3adress = parser.get('main','ts3adress')
ts3username = parser.get('main','ts3username')
ts3password = parser.get('main','ts3password')

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

print('Watcher started')

def enterwatcherbot(ts3conn, msg=None):

    # Register for the event.
    ts3conn.servernotifyregister(event="server")

    while True:
        ts3conn.send_keepalive()

        try:
            # This method blocks, but we must sent the keepalive message at
            # least once in 10 minutes. So we set the timeout parameter to
            # 9 minutes.
            event = ts3conn.wait_for_event(timeout=550)
        except ts3.query.TS3TimeoutError:
            pass
        else:
            # Greet new clients.
            if (str(event.event) == "notifycliententerview") and '9' in event.parsed[0]['client_servergroups'].split(','):
                # -32821639
                lstTxt = '\n<b>' + event.parsed[0]['client_nickname'] + '</b> зашел на сервер ts'
                mes = bot.sendMessage(chat_id=-1001051221798, text=lstTxt, parse_mode=telegram.ParseMode.HTML)
    return None

with ts3.query.TS3Connection(ts3adress) as ts3conn:
        ts3conn.login(client_login_name=ts3username, client_login_password=ts3password)
        ts3conn.use(sid=1)
        enterwatcherbot(ts3conn)
