from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging
import json, requests
import telegram.bot
from telegram.ext import messagequeue as mq

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)

'''updater = Updater(token='*************')
dispatcher = updater.dispatcher
updater.start_polling()

def start(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="I'm a bot, please talk to me!")

def echo(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text=update.message.text)

def caps(bot, update, args):
    text_caps = ' '.join(args).upper()
    bot.send_message(chat_id=update.message.chat_id, text=text_caps)


start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

echo_handler = MessageHandler(Filters.text, echo)
dispatcher.add_handler(echo_handler)

caps_handler = CommandHandler('caps', caps, pass_args=True)
dispatcher.add_handler(caps_handler)'''


def goo_url(url):
    post_url = 'https://www.googleapis.com/urlshortener/v1/url?key=**********************+'
    payload = {'longUrl': url}
    headers = {'content-type': 'application/json'}
    r = requests.post(post_url, data=json.dumps(payload), headers=headers)
    d = json.loads(r.text)
    return d['id']
    
    
class MQBot(telegram.bot.Bot):
    '''A subclass of Bot which delegates send method handling to MQ'''
    def __init__(self, *args, is_queued_def=True, mqueue=None, **kwargs):
        super(MQBot, self).__init__(*args, **kwargs)
        # below 2 attributes should be provided for decorator usage
        self._is_messages_queued_default = is_queued_def
        self._msg_queue = mqueue or mq.MessageQueue()

    def __del__(self):
        try:
            self._msg_queue.stop()
        except:
            pass
        super(MQBot, self).__del__()

    @mq.queuedmessage
    def send_message(self, *args, **kwargs):
        '''Wrapped method would accept new `queued` and `isgroup`
        OPTIONAL arguments'''
        super(MQBot, self).send_message(*args, **kwargs)


q = mq.MessageQueue(all_burst_limit=3, all_time_limit_ms=3000)
testbot = MQBot("***********", mqueue=q)
upd = telegram.ext.updater.Updater(bot=testbot)

def reply(bot, update):
    # tries to echo 10 msgs at once
    chatid = update.message.chat_id
    msgt = update.message.text
    print(msgt, chatid)
    for ix in range(10):
        bot.send_message(chat_id=chatid, text='%s) %s' % (ix + 1, msgt))
        
        
hdl = MessageHandler(Filters.text, reply)
upd.dispatcher.add_handler(hdl)
upd.start_polling()      



