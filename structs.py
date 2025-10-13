larm = [1]
for i in range(2, 21):
    larm += [i, i + 14, i + 28]


class Key():
    def __init__(self, code: int, char: str, /, alt=False):
        if not (code in range(1, 54)):
            print("Неправильный номер клавиши")
        self.code = code
        self.char = char
        self.alt = alt
# 1 - ~ 29 - \
# row
        if code in range(1, 14):
            self.row = "tr"
        elif code in range(16, 29):
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
        if code in [1, 2, 16, 11, 12, 13, 30, 44, 25, 26, 27, 28, 39, 40, 53]:
            self.finger = 'f5'
        elif code in [3, 10, 17, 31, 45, 24, 38, 52]:
            self.finger = 'f4'
        elif code in [4, 9, 18, 32, 46, 23, 37, 51]:
            self.finger = 'f3'
        else:
            self.finger = 'f2'
# penalty
        if code in list(range(30, 34)) + list(range(36, 40)):
            self.penalty = 0
        elif code in (list(range(2, 6)) + [20, 21, 48, 49, 26] +
                      list(range(8, 12))):
            self.penalty = 2
        elif code in [27, 1, 6, 7, 12]:
            self.penalty = 3
        elif code in [13, 29]:
            self.penalty = 4
        else:
            self.penalty = 1


class Layout():
    def __init__(self, tr='ё1234567890-=', ur='йцукенгшщзхъ\\', hr='фывапролджэ',
                 lr='ячсмитьбю.'):
        if not ([len(r) for r in (tr, ur, hr, lr)] == [13, 13, 11, 10]):
            print("Ряды введены неправильно")
            return
        self.tr = tr
        self.ur = ur
        self.hr = hr
        self.lr = lr
        self.extract_keys()

    def extract_keys(self):
        d = dict(list(zip(self.tr, range(1, 14))) +
                 list(zip(self.ur, range(16, 29))) +
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
        print(f'Кол-во штрафов в файле {filename}: {pen_counter}')

    def lexeme(self, filename, /):
        with open(filename) as f:
            text = f.readlines()
        with open("result.txt", 'w') as f:
            for line in text:
                penalty = self.pen_count(line)
                f.write(line[:-1] + ' ' + str(penalty) + '\n')
        print("Штрафы записаны в файл result.txt")

    def pen_count(self, line: str, /):
        pen_counter = 0
        for ch in line:
            if not ch.isalpha():
                continue
            k = self.keys.get(ch.lower(), 0)
            if k == 0:
                continue
            else:
                if ch.isupper():
                    pen_counter += 2  # shift
                if k.alt:
                    pen_counter += 1  # alt
                pen_counter += k.penalty
            print(pen_counter)
        return pen_counter

