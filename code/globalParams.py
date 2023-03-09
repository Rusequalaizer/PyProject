import telebot
from classes import ERROR, LastFunc, SwitchParameter

API_TOKEN = '12345678' # Input here Yuor token
bot = telebot.TeleBot(API_TOKEN)

switchParam = SwitchParameter('-NONE-')
lf = LastFunc()
err = ERROR()

PATH_TO_TXT_FILES = 'q/w/e/r/t/y' # Input here path to texts folder
NAMES_OF_TXT_FILES = ['help.txt', 'plot.txt', 'approx.txt', 'interp.txt', 'func.txt', 'integ.txt', 'interv.txt', 'sko.txt']
NUMBER_OF_FILES = len(NAMES_OF_TXT_FILES)
