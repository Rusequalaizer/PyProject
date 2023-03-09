class SwitchParameter:
    def __init__(self, firstName) -> None:
        self.param = firstName

    def changeParam(self, whichType):
        if (whichType == '/help'):
            self.param = '-NONE-'
            return self.param
        elif (whichType == '/approx'):
            self.param = '-APPROX-'
            return self.param
        elif (whichType == '/interp'):
            self.param = '-INTERP-'
            return self.param
        elif (whichType == '/func'):
            self.param = '-FUNC-'
            return self.param
        elif (whichType == '/create'):
            self.param = '-CREATE-'
            return self.param
        elif (whichType == '/integ'):
            self.param = '-INTEG-'
            return self.param
        elif (whichType == '/interv'):
            self.param = '-INTERV-'
            return self.param
        elif (whichType == '/sko'):
            self.param = '-SKO-'
            return self.param
        return self.param
    
class ERROR:
    def __init__(self) -> None:
        self.badValues = 'Введенные значения не распознанны, введите значения заново'
        self.unknownWords = 'Количество значений X не совпадает с количеством значений Y, введите значения заново'

    def BadValues(self, nameOfFunction):
        print(f'Error: BadValues ({nameOfFunction})')
        return self.badValues
    
    def UnknownWords(self, nameOfFunction):
        print(f'Error: UnknownWords ({nameOfFunction})')
        return self.unknownWords

class LastFunc:
    def __init__(self) -> None:
        self.setX = []
        self.setY = []
