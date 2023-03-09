# Python version: 3.10.4 
# Made by Lazarev Kirill AMP_Graph_bot

from functions import searchAndReturnText, checkAndProcessMsg
from globalParams import bot, switchParam

@bot.message_handler(content_types=['text'])
def userMenu(message):
    searchAndReturnText(message, message.text)
    param = switchParam.changeParam(message.text)
    checkAndProcessMsg(message.text, param, message)

bot.polling(none_stop=True)
