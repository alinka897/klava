import csv
from time import time
from string import punctuation as punc


def timeit(func):
    def wrapper(*args):
        start = time()
        result = func(*args)
        end = time()
        print(f"Выполнено за {end - start}")
        return result
    return wrapper

class Key():
    """
    Класс Key в зависимости от кода клавиши
    определяет ряд клавиши:
    tr - ряд с цифрами
    ur - верхний ряд
    hr - домашний ряд
    lr - нижний ряд
    Определяет руку(arm) и пальцы(f2-5),
    которые нажимают на клавишу,
    и штраф для нее(penalty)
    """
    def __init__(self, code: int, char: str, /, alt=False):
        if not (code in range(1, 54)):
            print("Неправильный номер клавиши")
        self.code = code
        self.char = char
        self.alt = alt
# 1 - ~ 28 - \
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
        larm = [1]
        for i in range(2, 7):
            larm += [i, i + 14, i + 28, i + 42]
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
    """
    Класс Layout определяет раскладку, т.е. сопоставляет значения клавиш
    с соответствующим экземпляром класса Key
    """
    def __init__(self, /, tr='ё1234567890-=', ur='йцукенгшщзхъ\\',
                 hr='фывапролджэ', lr='ячсмитьбю.', color='k', name='', **alts):
        if not ([len(r) for r in (tr, ur, hr, lr)] == [13, 13, 11, 10]):
            print("Ряды введены неправильно")
            return
        self.tr = tr
        self.ur = ur
        self.hr = hr
        self.lr = lr
        self.name = name
        self.color = color
        self.extract_keys(alts)

    def extract_keys(self, alts: dict):
        """
        Получает словари с клавишами раскладки и
        альтовыми клавишами
        """
        d = dict(list(zip(self.tr, range(1, 14))) +
                 list(zip(self.ur, range(16, 29))) +
                 list(zip(self.hr, range(30, 41))) +
                 list(zip(self.lr, range(44, 54))))
        keys = dict()
        alt_keys = dict()
        for k in d:
            if k in alts:
                alt_keys[alts[k]] = Key(d[k], alts[k], alt=True)
            keys[k] = Key(d[k], k)
        self.keys = keys
        self.alts = alt_keys

    def writef(self, ext: str, data: list, /) -> None:
        """
        Запись в файл штрафов построчно
        """
        if ext != 'csv':
            with open('result.txt', 'w') as f:
                f.write(''.join(data))
            print("Штрафы записаны в файл result.txt")
            return
        with open('result.csv', 'w', newline='') as f:
            csv_w = csv.writer(f)
            csv_w.writerows(data)
            print("Штрафы записаны в файл result.csv")

    def readf(self, path: str, /, linemode=False) -> tuple:
        """
        Считает нагрузку на руки, пальцы для всего файла
        """
        ext = path.split('/')[-1].split('.')[-1]
        pen_count = 0
        fingers_count = [0] * 8
        arms_count = [0] * 3
        lines = []
        if ext != 'csv':
            with open(path) as f:
                for line in f:
                    pc, fc, ac = self.line_penalty_counter(line)
                    pen_count += pc
                    fingers_count = [fingers_count[i] + fc[i] for i in range(8)]
                    arms_count = [x + y for x, y in zip(arms_count, ac)]
                    if linemode:
                        lines.append(line[:-1] + ' ' + str(pc) + '\n')
            if linemode:
                self.writef(ext, lines)
            return (pen_count, fingers_count, arms_count)

        with open(path, newline='') as f:
            csv_r = csv.reader(f)
            rows = []
            for row in csv_r:
                for item in row:
                    if item.isnumeric():
                        continue
                    pc, fc, ac = self.line_penalty_counter(item)
                    pen_count += pc
                    fingers_count = [fc[i] + fingers_count[i] for i in range(8)]
                    arms_count = [ac[i] + arms_count[i] for i in range(3)]
                    if linemode:
                        row.append(pc)
                        rows.append(row)
                    break
        if linemode:
            self.writef(ext, rows)
        return (pen_count, fingers_count, arms_count)

    def choose_key(self, ch: str, /) -> Key | None:
        """
        Выбор клавиши альтовой или обычной
        """
        k1 = self.keys.get(ch.lower(), 0)
        k2 = self.alts.get(ch.lower(), 0)
        # определение ближней клавиши
        if k1 == 0 and k2 == 0:
            return
        elif k1 != 0 and k2 != 0:
            if k2.penalty < k1.penalty:
                k1 = k2
        elif k1 == 0 and k2 != 0:
            k1 = k2
        return k1

    def line_penalty_counter(self, line: str, /) -> tuple:
        """
        Считает штрафы для рук и пальцев в строке
        """
        arm_count = [0] * 3  # левая, двуручие, правая
        pen_counter = 0
        fingers_count = [0] * 8  # 0 - 7 левый мизинец - правый
        for ch in line:
            if not ch.isalpha():
                continue

            k = self.choose_key(ch)
            if k is None:
                continue
            pen = k.penalty

            if ch.isupper():
                pen_counter += 1  # shift
                if k.arm == 'l':
                    fingers_count[7] += 1
                else:
                    fingers_count[0] += 1
                arm_count[1] += 1

            if k.alt:
                pen_counter += 1  # alt
                if k.arm == 'l':
                    arm_count[1] += 1
                else:
                    arm_count[2] += 1
            pen_counter += pen

            d = dict(zip('lf5 lf4 lf3 lf2 rf2 rf3 rf4 rf5'.split(),
                         range(8)))
            fingers_count[d[k.arm + k.finger]] += pen  

            if ch.isupper() or (k.alt and k.arm == 'l'):
                arm_count[1] += pen
            elif k.arm == 'r' or (k.alt and k.arm == 'r'):
                arm_count[2] += pen
            else:
                arm_count[0] += pen

        return (pen_counter, fingers_count, arm_count)


    def perebor(self, word: str , /) -> tuple | None:
        """
        Анализ слова по путям пальцев
        """
        word = word.strip(punc)
        if len(word) <= 1:
            return
        # кол-во удобных двухсимвольных, трех-... переборов
        chr_count = dict(ch2=0, ch3=0, ch4=0, ch5=0)
        chl_count = dict(ch2=0,ch3=0, ch4=0, ch5=0)
        conv = '' # удобство набития слова
        conv_ch = '' # удобство набития символов 
        streak = 1 # сколько символов в удобном переборе 
        two_arms = False
        arm = ''
        for i in range(len(word) - 1):

            k1 = self.choose_key(word[i])
            if k1 is None:
                return
            k2 = self.choose_key(word[i + 1])
            if k2 is None:
                return

            arm = k1.arm
            # руки меняются -> неудобство, пред сост сохраняем в словарь
            if arm != k2.arm:
                # cлово бьется двумя руками
                two_arms = True
                # добавляем только удобные переборы
                if conv_ch == 'good':
                    if arm == 'r':
                        chr_count[f'ch{streak}'] += 1
                    else:
                        chl_count[f'ch{streak}'] += 1
                streak = 1
                conv_ch = ''
                conv = 'bad' # слово неудобно

            # переход на другой ряд на той же стороне
            elif k1.row != k2.row:
                # для сравнения проекция на хоум ряд
                codes = [0] * 2
                i = 0 
                for k in (k1, k2):
                    if k.row == 'hr':
                        codes[i] = k.code
                    elif k.row == 'ur':
                        codes[i] = k.code + 14
                    elif k.row == 'lr':
                        codes[i] = k.code - 14
                    else:
                        codes[i] = k.code + 2 * 14
                    i += 1

                if arm == 'r':
                    if conv_ch == 'good':
                        chr_count[f'ch{streak}'] += 1
                        conv_ch = ''
                    if (codes[0] - codes[1]) > 0: # если направление сохранено
                        conv = 'ok'
                    else:
                        conv = 'bad'
                else:
                    if (codes[0] - codes[1]) < 0:
                        conv = 'ok' # частично удобно
                    else:
                        conv = 'bad'
                    if conv_ch == 'good':
                        chl_count[f'ch{streak}'] += 1
                        conv_ch = ''
                streak = 1

            # удобная последовательность
            elif arm == 'l':
                if k1.code <= k2.code:
                    streak += 1
                    conv_ch = 'good'
                else:
                    if conv_ch == 'good':
                        chl_count[f'ch{streak}'] += 1
                        conv_ch = ''
                    conv = 'bad'
                    streak = 1
            else:
                if k1.code >= k2.code:
                    streak += 1
                    conv_ch = 'good'
                else:
                    if conv_ch == 'good':
                        chr_count[f'ch{streak}'] += 1
                        conv_ch = ''
                    conv = 'bad'
                    streak = 1
        if conv == '':
            conv = 'good'
        # последняя последовательно не обработанная в цикле
        if streak != 1:
            if arm == 'r':
                chr_count[f'ch{streak}'] += 1
            else:
                chl_count[f'ch{streak}'] += 1
        if two_arms:
            arm = 'both'
        return (arm, conv, chl_count, chr_count) 

    def per_readf(self, path: str, /, linemode=False) -> tuple:
        """
        Анализ текста по путям пальцев
        """
        arms = dict(r=0, both=0, l=0) 
        convs = dict(good=0, bad=0, ok=0)
        l_ch = dict(ch2=0, ch3=0, ch4=0, ch5=0)
        r_ch = dict(ch2=0,ch3=0, ch4=0, ch5=0)
        ext = path.split('/')[-1].split('.')[-1]
        lines = []
        if ext != 'csv':
            with open(path) as f:
                text = f.readlines()
            for line in text:
                for word in line.split():
                    if word.isdigit():
                        continue
                    ret = self.perebor(word)
                    if ret is None:
                        continue
                    arm, conv, chl_cnt, chr_cnt = ret
                    arms[arm] += 1
                    convs[conv] += 1
                    for k in chl_cnt.keys():
                        l_ch[k] += chl_cnt[k]
                        r_ch[k] += chr_cnt[k]
                if linemode:
                    lines.append(line[:-1] + ' ' + conv + '\n')
            if linemode:
                self.writef(ext, lines)
        else:
            with open(path, newline='') as f:
                csv_r = csv.reader(f)
                for row in csv_r:
                    for word in row:
                        if word.isdigit():
                            continue
                        ret = self.perebor(word)
                        if ret is None:
                            continue
                        arm, conv, chl_cnt, chr_cnt = ret
                        arms[arm] += 1
                        convs[conv] += 1
                        for k in chl_cnt.keys():
                            l_ch[k] += chl_cnt[k]
                            r_ch[k] += chr_cnt[k]
                        if linemode:
                            row.append(conv)
                            lines.append(row)
                        break
            if linemode:
                self.writef(ext, lines)
   
        arms = [arms[k] for k in 'l both r'.split()]
        convs = [convs[k] for k in 'bad ok good'.split()]
        l_ch = [l_ch[k] for k in 'ch2 ch3 ch4 ch5'.split()]
        r_ch = [r_ch[k] for k in 'ch2 ch3 ch4 ch5'.split()]

        return (arms, convs, l_ch, r_ch)
