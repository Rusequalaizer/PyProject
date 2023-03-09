import os
import scipy as sp
import matplotlib.pyplot as plt
import matplotlib
import numpy as np
from sympy import Symbol, sympify
from scipy.interpolate import Rbf
from globalParams import bot
matplotlib.use('Agg')

def isFloat(value):
    try:
        float(value)
        return True
    except ValueError:
        return False

def createGraphicFromUserInput(msg, message, param):
    if (param == '-INTEG-'):
        array = message.split()
        expr = array[0]
        dx = (float(array[1]) - float(array[2])) / 10000
        points = np.arange(float(array[2]), float(array[1]), dx)
        
        x = Symbol('x')
        points_1 = []
        for i in range(len(points)):
            prom = sympify(expr)
            prom1 = float(prom.subs(x, points[i]))
            points_1.append(prom1)

        figure = plt.figure()
        axes = plt.axes()
        axes.set_xlabel('x')
        axes.set_ylabel('y')
        plt.plot(points, points_1, linewidth=2)
        plt.grid(True)

        p = len(os.listdir(path="."))
        nameOfGraphic = f'x_y_{p}_INTERP.png'
        figure.savefig(nameOfGraphic)
        plt.close('all')

        sendGraphic = open(nameOfGraphic, 'rb')
        bot.send_photo(msg.chat.id, sendGraphic)
        sendGraphic.close()
        os.remove(nameOfGraphic)

        res = []
        for i in range(len(points_1)):
            res.append(dx * points_1[i])
        
        return res
    
    elif (param == '-FUNC-'):
        y = ''
        array = message.split()
        expr = array[0]
        points = []
        sx = ''
        for i in range(1, len(array)):
            if (isFloat(array[i])):
                points.append(float(array[i]))
        for i in range(1, len(array)):
            if (isFloat(array[i])):
                sx += f'{array[i]} '

        x = Symbol('x')
        for i in range(len(points)):
            prom = sympify(expr)
            prom1 = str(prom.subs(x, points[i]))
            y += f' {prom1}'
        points_1 = []
        for i in range(len(points)):
            prom = sympify(expr)
            prom1 = float(prom.subs(x, points[i]))
            points_1.append(prom1)
        
        return sx, y, points, points_1
    

    elif (param == '-INTERV-'):
        array = message.split()
        expr = array[0]
        dx = (float(array[1]) - float(array[2])) / 1000
        points = np.arange(float(array[2]), float(array[1]), dx)

        x = Symbol('x')
        points_1 = []
        for i in range(len(points)):
            prom = sympify(expr)
            prom1 = float(prom.subs(x, points[i]))
            points_1.append(prom1)

        f = Rbf(points, points_1)

        figure = plt.figure()
        axes = plt.axes()
        axes.set_xlabel('x')
        axes.set_ylabel('y')
        plt.plot(points, f(points), linewidth=2)
        plt.grid(True)

        p = len(os.listdir(path="."))
        nameOfGraphic = f'x_y_{p}_INTERV.png'
        figure.savefig(nameOfGraphic)
        plt.close('all')

        sendGraphic = open(nameOfGraphic, 'rb')
        bot.send_photo(msg.chat.id, sendGraphic)
        sendGraphic.close()
        os.remove(nameOfGraphic)

def aboutGraphic(fp, deg, dev, msg):
    eqImage = 'Уравнение функции:\n'
    skoImage = 'СКО построенного графика:\n'
    sko = f'{dev}'
    equation = ''
    if (deg == 1):
        a = '%s'%round(fp[0], 4)
        b = '%s'%round(fp[1], 4)
        equation = f'y = {a}x + {b}\n'
    elif (deg == 2):
        a = '%s'%round(fp[0], 4)
        b = '%s'%round(fp[1], 4)
        c = '%s'%round(fp[2], 4)
        equation = f'y = {a}x^2 + {b}x + {c}\n'
    elif (deg == 3):
        a = '%s'%round(fp[0], 4)
        b = '%s'%round(fp[1], 4)
        c = '%s'%round(fp[2], 4)
        d = '%s'%round(fp[3], 4)
        equation = f'y = {a}x^3 + {b}x^2 + {c}x + {d}\n'
    elif (deg == 4):
        a = '%s'%round(fp[0], 4)
        b = '%s'%round(fp[1], 4)
        c = '%s'%round(fp[2], 4)
        d = '%s'%round(fp[3], 4)
        e = '%s'%round(fp[4], 4)
        equation = f'y = {a}x^4 + {b}x^3 + {c}x^2 + {d}x + {e}\n'
    about = eqImage + equation + skoImage + sko
    bot.send_message(msg.chat.id, about)
    

def whichDev(fp, x, y, i):
    if (i == 1):
        y1 = [fp[0] * x[i] + fp[1] for i in range(0, len(x))] # значения функции a*x+b
        so = round(sum([abs(y[i] - y1[i]) for i in range(0, len(x))]) / (len(x) * sum(y)) * 100, 4) # средняя ошибка
        return float(so)
    elif (i == 2):
        y1 = [fp[0] * x[i]**2 + fp[1] * x[i] + fp[2] for i in range(0, len(x))] # значения функции a*x**2+b*x+c
        so = round(sum([abs(y[i] - y1[i]) for i in range(0, len(x))]) / (len(x) * sum(y)) * 100, 4) # средняя ошибка
        return float(so)
    elif (i == 3):
        y1 = [fp[0] * x[i]**3 + fp[1] * x[i]**2 + fp[2] * x[i] + fp[3] for i in range(0, len(x))] # значения функции a*x**3+b*x**2+c*x+d
        so = round(sum([abs(y[i] - y1[i]) for i in range(0, len(x))]) / (len(x) * sum(y))*100, 4) # средняя ошибка
        return float(so)
    elif (i == 4):
        y1 = [fp[0] * x[i]**4 + fp[1] * x[i]**3 + fp[2] * x[i]**2 + fp[3] * x[i] + fp[4] for i in range(0, len(x))] # значения функции a*x**4+b*x**3+c*x**2+d*x+e
        so = round(sum([abs(y[i]-y1[i]) for i in range(0,len(x))]) / (len(x) * sum(y)) * 100, 4) # средняя ошибка
        return float(so)


def approxGraph(xLabel, yLabel, x, y, msg):
    polyDegree = 4
    avgQuadraticDev = []
    for i in range(1, polyDegree + 1):
        fp, residuals, rank, sv, rcond = sp.polyfit(x, y, i, full=True)
        avgQuadraticDev.append(whichDev(fp, x, y, i))
    bestDev = 1000
    bestDegree = 1
    for i in range(polyDegree):
        if (bestDev > avgQuadraticDev[i]):
            bestDev = avgQuadraticDev[i]
            bestDegree = i + 1
    
    fp, residuals, rank, sv, rcond = sp.polyfit(x, y, bestDegree, full=True)
    f = sp.poly1d(fp)
    fx = np.arange(x[0], x[-1] + 1, 0.001)

    figure = plt.figure()
    axes = plt.axes()
    axes.set_xlabel(xLabel)
    axes.set_ylabel(yLabel)
    plt.scatter(x, y)
    plt.plot(fx, f(fx), linewidth=2)
    plt.grid(True)

    p = len(os.listdir(path="."))
    nameOfGraphic = f'{xLabel}_{yLabel}_{p}_APROX.png'
    figure.savefig(nameOfGraphic)
    plt.close('all')

    sendGraphic = open(nameOfGraphic, 'rb')
    bot.send_photo(msg.chat.id, sendGraphic)
    sendGraphic.close()
    os.remove(nameOfGraphic)

    aboutGraphic(fp, bestDegree, bestDev, msg)

def interpGraph(xLabel, yLabel, x, y, msg):
    f = Rbf(x, y)
    newX = np.arange(min(x), max(x), 0.001)
    newY = f(newX)

    figure = plt.figure()
    axes = plt.axes()
    axes.set_xlabel(xLabel)
    axes.set_ylabel(yLabel)
    plt.scatter(x, y)
    plt.plot(newX, newY, linewidth=2)
    plt.grid(True)

    p = len(os.listdir(path="."))
    nameOfGraphic = f'{xLabel}_{yLabel}_{p}_INTERP.png'
    figure.savefig(nameOfGraphic)
    plt.close('all')

    sendGraphic = open(nameOfGraphic, 'rb')
    bot.send_photo(msg.chat.id, sendGraphic)
    sendGraphic.close()
    os.remove(nameOfGraphic)
