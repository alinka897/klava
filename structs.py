import csv
from time import time


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
    def __init__(self, code: int, char: str, /, alt=False, shift=False):
        if not (code in range(1, 54)):
            print("Неправильный номер клавиши")
        self.code = code
        self.char = char
        self.alt = alt
        self.shift = shift
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
                 hr='фывапролджэ', lr='ячсмитьбю.', color='k', name='',
                 shifts=dict(zip('1234567890-=\\.','!"№;%:?*()_+/,')),
                 **alts):
        if not ([len(r) for r in (tr, ur, hr, lr)] == [13, 13, 11, 10]):
            print("Ряды введены неправильно")
            return
        self.better_keys=dict()
        self.tr = tr
        self.ur = ur
        self.hr = hr
        self.lr = lr
        self.name = name
        self.color = color
        self.extract_keys(alts, shifts)

    def extract_keys(self, alts: dict, shifts: dict):
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
        shift_keys = dict()
        for k in d:
            if k in alts:
                alt_keys[alts[k]] = Key(d[k], alts[k], alt=True)
            if k in shifts:
                shift_keys[shifts[k]] = Key(d[k], shifts[k], shift=True)
            else:
                if k.isalpha():
                    shift_keys[k.upper()] = Key(d[k], k.upper(), shift=True)
            keys[k] = Key(d[k], k)
        self.keys = keys
        self.alts = alt_keys
        self.shifts = shift_keys

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
        fingers_count = [0] * 10
        arms_count = [0] * 3
        lines = []
        if ext != 'csv':
            with open(path) as f:
                for line in f:
                    pc, fc, ac = self.line_penalty_counter(line)
                    pen_count += pc
                    fingers_count = [fingers_count[i] + fc[i] for i in range(10)]
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
                    fingers_count = [fc[i] + fingers_count[i] for i in range(10)]
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
        if ch in self.better_keys:
            return self.better_keys[ch]
        k1 = self.keys.get(ch, 0)
        k2 = self.alts.get(ch, 0)
        k3 = self.shifts.get(ch, 0)
        d = dict()
        pens = []
        for k in (k1, k2, k3):
            if k != 0:
                if k.alt or k.shift:
                    d[k.penalty + 1] = k
                    pens.append(k.penalty + 1)
                else:
                    d[k.penalty] = k 
                    pens.append(k.penalty)
        if pens == []:
            return 
        k1 = d[min(pens)]
        self.better_keys[ch] = k1
        return k1

    def line_penalty_counter(self, line: str, /) -> tuple:
        """
        Считает штрафы для рук и пальцев в строке
        """
        arm_count = [0] * 3  # левая, двуручие, правая
        pen_counter = 0
        fingers_count = [0] * 10  # 0 - 7 левый мизинец - правый 8 - правый большой
        prev_arm = ''
        for ch in line:
            if ch == ' ':
                if prev_arm == 'r':
                    fingers_count[9] += 1
                    arm_count[0] += 1
                else:
                    fingers_count[8] += 1
                    arm_count[2] += 1
                continue
            k = self.choose_key(ch)
            if k is None:
                continue
            pen = k.penalty

            if k.shift:
                pen_counter += 1  # shift
                if k.arm == 'l':
                    fingers_count[7] += 1
                else:
                    fingers_count[0] += 1
                arm_count[1] += 1

            if k.alt:
                fingers_count[8] += 1
                pen_counter += 1  # alt
                if k.arm == 'l':
                    arm_count[1] += 1
                else:
                    arm_count[2] += 1
            pen_counter += pen

            d = dict(zip('lf5 lf4 lf3 lf2 rf2 rf3 rf4 rf5'.split(),
                         range(8)))
            fingers_count[d[k.arm + k.finger]] += pen  

            if k.shift or (k.alt and k.arm == 'l'):
                arm_count[1] += pen
            elif k.arm == 'r' or (k.alt and k.arm == 'r'):
                arm_count[2] += pen
            else:
                arm_count[0] += pen
            prev_arm = k.arm

        return (pen_counter, fingers_count, arm_count)

    def check_direction(self, k1: Key, k2: Key) -> bool:
        """
        Проверка направления от внешнего к внутреннему (от клавиши 1 до 2) 
        """
        if k1.code == k2.code:
            return True
        comp = dict(zip('f2 f3 f4 f5'.split(), range(2, 6)))
        f1, f2 = comp[k1.finger], comp[k2.finger]
        if f1 > f2:
            return True
        if f1 < f2:
            return False
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
        if k1.arm == 'r':
            if codes[0] > codes[1]:
                return True
            else:
                return False
        else:
            if codes[0] < codes[1]:
                return True
            else:
                return False

    def perebor(self, word: str , /) -> tuple | None:
        """
        Анализ слова по путям пальцев
        """
        if len(word) <= 1:
            return
        # кол-во удобных двухсимвольных, трех-... переборов
        chr_count = dict(ch2=0, ch3=0, ch4=0, ch5=0)
        chl_count = dict(ch2=0,ch3=0, ch4=0, ch5=0)
        conv = '' # удобство перебора 
        prev_conv = '' #удобство пред перебора
        conv_map = dict(zip('bad ok good'.split(), range(3)))
        convs = [0] * 3
        streak = 2 # сколько символов в удобном переборе 
        arm = ''
        def count(arm: str, conv: str) -> None:
            nonlocal streak
            if streak > 5:
                streak = 5
            orig_streak = streak
            if conv == 'good':
                while streak > 1:
                    if arm == 'r':
                        chr_count[f'ch{streak}'] += orig_streak - streak + 1
                        convs[conv_map[conv]] += chr_count[f'ch{streak}'] 
                    else:
                        chl_count[f'ch{streak}'] += orig_streak - streak + 1
                        convs[conv_map[conv]] += chl_count[f'ch{streak}'] 
                    streak -= 1
            else:
                for i in range(1, streak):
                    convs[conv_map[conv]] += i 
            streak = 2
        k2 = None
        for i in range(len(word) - 1):
            k1 = k2
            if k1 is None:
                k1 = self.choose_key(word[i])


            k2 = self.choose_key(word[i + 1])
            if k2 is None or k1 is None:
                if prev_conv != '':
                    count(arm, prev_conv)
                continue

            arm = k1.arm
            # руки меняются -> неудобство
            if arm != k2.arm:
                conv = 'bad'
            # на одной стороне
            else:
                if self.check_direction(k1, k2): # направление сохранено
                    conv = 'good'
                else:
                    conv = 'ok'
            # если перебор остается по удобству таким же то повышем стрик, иначе
            # считаем все подпреборы в нем и обнуляемся
            
            if prev_conv == conv:
                streak += 1
            else:
                if prev_conv != '':
                    count(arm, prev_conv)
            prev_conv = conv
        # учет последнего длинного перебора
        if prev_conv != '':
            count(arm, prev_conv)
        return (convs, chl_count, chr_count) 

    def per_readf(self, path: str, /, linemode=False) -> tuple:
        """
        Анализ текста по путям пальцев
        """
        gconvs = [0]*3
        l_ch = dict(ch2=0, ch3=0, ch4=0, ch5=0)
        r_ch = dict(ch2=0,ch3=0, ch4=0, ch5=0)
        ext = path.split('/')[-1].split('.')[-1]
        lines = []
        if ext != 'csv':
            with open(path) as f:
                for line in f:
                    for word in line.split():
                        ret = self.perebor(word)
                        if ret is None:
                            continue
                        convs, chl_cnt, chr_cnt = ret
                        gconvs = [convs[i] + gconvs[i] for i in
                                  range(len(gconvs))]
                        for k in chl_cnt.keys():
                            l_ch[k] += chl_cnt[k]
                            r_ch[k] += chr_cnt[k]
                    if linemode:
                        lines.append(line[:-1] + ' ' + str(convs) + '\n')
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
                        convs, chl_cnt, chr_cnt = ret
                        gconvs = [convs[i] + gconvs[i] for i in
                                  range(len(gconvs))]
                        for k in chl_cnt.keys():
                            l_ch[k] += chl_cnt[k]
                            r_ch[k] += chr_cnt[k]
                        if linemode:
                            row.append(str(convs))
                            lines.append(row)
                        break
            if linemode:
                self.writef(ext, lines)
   
        l_ch = [l_ch[k] for k in 'ch2 ch3 ch4 ch5'.split()]
        r_ch = [r_ch[k] for k in 'ch2 ch3 ch4 ch5'.split()]

        return (gconvs, l_ch, r_ch)
