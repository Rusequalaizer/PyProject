from globalParams import bot, err, lf, switchParam, PATH_TO_TXT_FILES, NAMES_OF_TXT_FILES, NUMBER_OF_FILES
from plot import approxGraph, interpGraph, createGraphicFromUserInput
from math import sqrt

def isFloat(value):
    try:
        float(value)
        return True
    except ValueError:
        return False
    
def sko(data):
    mean = 0
    square = 0
    length = len(data)
    for i in range(length):
        mean += data[i]
    mean /= length
    for i in range(length):
        square += (mean - data[i])**2
    skoUnbiasedVariance = sqrt(square/length)
    skoWithOffsetVariance = sqrt(square/(length - 1))
    return f'Стандартный ответ:\n{mean} +- {skoUnbiasedVariance}\n\nСо смещенной дисперсией:\n{mean} +- {skoWithOffsetVariance}'
    
def createMsg(fromFile):
    messageToUser = ''
    for i in range(len(fromFile)):
        messageToUser = messageToUser + fromFile[i]
    return messageToUser
  
def setPositions(message):
    lengthOfMessage = len(message)
    positionsOfNewString = [0]
    positionsOfDoubleDots = []
    for i in range(lengthOfMessage):
        if (message[i] == '\n'):
            positionsOfNewString.append(i + 1)
        elif (message[i] == ':'):
            positionsOfDoubleDots.append(i)
    return positionsOfNewString, positionsOfDoubleDots

def setTitles(message, numberOfTitles, positionsOfDoubleDots, positionsOfNewString):
    titles = []
    for i in range(numberOfTitles):
        nameOfTitle = ''
        for j in range(positionsOfNewString[i], positionsOfDoubleDots[i]):
            nameOfTitle += message[j]
        titles.append(nameOfTitle)
    return titles[0], titles[1]

def setData(message):
    splittedMessage = message.split()
    data = []
    for i in range(len(splittedMessage)):
        if (isFloat(splittedMessage[i])):
            data.append(float(splittedMessage[i]))
    return data

def setXY(data):
    x = []
    y = []
    checkData = False
    lengthOfData = len(data)
    halfOfDataSize = int(lengthOfData / 2)
    if (lengthOfData % 2 == 0.0):
        for i in range(halfOfDataSize):
            x.append(data[i])
        for i in range(halfOfDataSize, lengthOfData):
            y.append(data[i])
        checkData = True
    else:
        checkData = False
    return x, y, checkData

def goToCreatePlot(checkData, message, msg, param, x, y, xTitle, yTitle):
    if (checkData and message != '/approx' and param == '-APPROX-'):
        approxGraph(xTitle, yTitle, x, y, msg)
    elif (checkData and message != '/interp' and param == '-INTERP-'):
        interpGraph(xTitle, yTitle, x, y, msg)
    else:
        bot.send_message(msg.chat.id, err.UnknownWords('goToCreatePlot'))

def searchAndReturnText(message, unknownName):
    for i in range(NUMBER_OF_FILES):
        if (f'{unknownName}.txt' == f'/{NAMES_OF_TXT_FILES[i]}'):
            trueName = PATH_TO_TXT_FILES + NAMES_OF_TXT_FILES[i]
            messageFromFile = open(trueName, 'r', encoding = 'utf8').readlines()
            messageToUser = createMsg(messageFromFile)
            bot.send_message(message.chat.id, messageToUser)

def checkAndProcessMsg(message, param, msg):
    positionsOfNewString, positionsOfDoubleDots = setPositions(message)
    numberOfTitles = len(positionsOfDoubleDots)

    if (numberOfTitles == 2 and (param == '-APPROX-' or param == '-INTERP-')):
        xTitle, yTitle = setTitles(message, numberOfTitles, positionsOfDoubleDots, positionsOfNewString)
        data = setData(message)
        if(len(data) == 0):
            bot.send_message(msg.chat.id, err.BadValues('checkAndProcessMsg: if_1'))
        else:
            x, y, checkData = setXY(data)
            goToCreatePlot(checkData, message, msg, param, x, y, xTitle, yTitle)
    
    elif (message != '/func' and param == '-FUNC-'):
        try:
            sx, y, points, points_1 = createGraphicFromUserInput(msg, message, param)
            bot.send_message(msg.chat.id, f'y = {y}\nx = {sx}\n\nПостроить график: /create')
            lf.setX = points
            lf.setY = points_1
        except Exception:
            bot.send_message(msg.chat.id, err.BadValues('checkAndProcessMsg: elif_1'))

    elif (message == '/create' and param == '-CREATE-'):
        if (len(lf.setX) == 0):
            bot.send_message(msg.chat.id, 'Для начала введите функцию и её значения')
        elif (len(lf.setX) != 0):
            approxGraph('x', 'y', lf.setX, lf.setY, msg)
            interpGraph('x', 'y', lf.setX, lf.setY, msg)
            param = switchParam.changeParam('/func')

    elif (message != '/integ' and param == '-INTEG-'):
        try:
            res = createGraphicFromUserInput(msg, message, param)
            bot.send_message(msg.chat.id, 'Результат: %.4f' % sum(res))
        except Exception:
            bot.send_message(msg.chat.id, err.BadValues('checkAndProcessMsg: elif_3'))

    elif (message != '/interv' and param == '-INTERV-'):
        try:
            createGraphicFromUserInput(msg, message, param)
        except Exception:
            bot.send_message(msg.chat.id, err.BadValues('checkAndProcessMsg: elif_4'))
    
    elif (message != '/sko' and param == '-SKO-'):
        try:
            data = setData(message)
            res = sko(data)
            bot.send_message(msg.chat.id, res)
        except Exception:
            bot.send_message(msg.chat.id, err.BadValues('checkAndProcessMsg: elif_5'))
        
