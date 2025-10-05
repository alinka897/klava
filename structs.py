###
задача этого кода: считать штрафы от разных рук, 
прогоняя через программу лексемы из заранее заготовленного файла 
и выводит результат в отдельный файл
###

larm = []
for i in range(16, 21):
    larm += [i, i + 14, i + 28]
    i += 1


class Key():
    def __init__(self, code: int, char: str, /):
        if not (code in range(16, 54)):
            print("Неправильный номер клавиши")
        self.code = code
        self.char = char
# row

        if code in range(16, 28):
            self.row = "ur"
        elif code in range(30, 41):
            self.row = "hr"
        else:
            self.row = "lr"

# arm
        if code in larm:
            self.arm = "l"
        else:
            self.arm = "r"
# finger
        if code in [16, 30, 44, 25, 26, 27, 39, 40, 53]:
            self.finger = 'f5'
        elif code in [17, 31, 45, 24, 38, 52]:
            self.finger = 'f4'
        elif code in [18, 32, 46, 23, 37, 51]:
            self.finger = 'f3'
        else:
            self.finger = 'f2'
# penalty
        if code in list(range(30, 34)) + list(range(36, 40)):
            self.penalty = 0
        elif code in [20, 21, 48, 49, 26]:
            self.penalty = 2
        elif code in [27, 41]:
            self.penalty = 3
        else:
            self.penalty = 1


class Layout():
    def __init__(self, ur='йцукенгшщзхъ', hr='фывапролджэ', lr='ячсмитьбю.',
                 /, alt=False):
        if not ([len(r) for r in (ur, hr, lr)] == [12, 11, 10]):
            print("Ряды введены неправильно")
            return
        self.ur = ur
        self.hr = hr
        self.lr = lr
        self.alt = alt
        self.extract_keys()

    def extract_keys(self):
        d = dict(list(zip(self.ur, range(16, 28))) +
                 list(zip(self.hr, range(30, 41))) +
                 list(zip(self.lr, range(44, 54))))
        keys = dict()
        for k in d.keys():
            keys[k] = Key(d[k], k)
        self.keys = keys

    def readf(self, filename, /):
        pen_counter = 0
        with open(filename) as f:
            text = f.readlines()
            for line in text:
                pen_counter += self.pen_count(line)
        print(f'Кол-во штрафов: {pen_counter}')

    def lexeme(self, filename, /):
        with open(filename) as f:
            text = f.readlines()
        with open("result.txt", 'w') as f:
            for line in text:
                penalty = self.pen_count(line)
                f.write(line[:-1] + ' ' + str(penalty) + '\n')

    def pen_count(self, line: str, /):
        pen_counter = 0
        for ch in line:
            k = self.keys.get(ch, 0)
            if k == 0:
                pass
            else:
                pen_counter += k.penalty
        return pen_counter
