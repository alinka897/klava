import csv


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
                 hr='фывапролджэ', lr='ячсмитьбю.', **alts):
        if not ([len(r) for r in (tr, ur, hr, lr)] == [13, 13, 11, 10]):
            print("Ряды введены неправильно")
            return
        self.tr = tr
        self.ur = ur
        self.hr = hr
        self.lr = lr
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
        for k in d.keys():
            if k in alts.keys():
                alt_keys[alts[k]] = Key(d[k], alts[k], alt=True)
            keys[k] = Key(d[k], k)
        self.keys = keys
        self.alts = alt_keys

    def readf(self, path: str, /):
        """
        Выводит нагрузку на руки, пальцы для всего файла
        """
        pen_counter = 0
        fingers_count = [0] * 8
        arms_count = [0] * 3
        with open(path) as f:
            text = f.readlines()
        for line in text:
            pc, fc, ac = self.pen_count(line)
            pen_counter += pc
            fingers_count = [fingers_count[i] + fc[i] for i in range(8)]
            arms_count = [x + y for x, y in zip(arms_count, ac)]
        filename = path.split('/')[-1]
        print(f'Нагрузка на пальцы: {fingers_count}')
        print(f'Нагрузка на руки: левая - {sum(fingers_count[:4])}, ' +
              f'правая - {sum(fingers_count[4:])}')
        print(f'Нагрузка на руки, считая двуручие: левая - {arms_count[0]}, ' +
              f'двуручие - {arms_count[1]}, правая - {arms_count[2]}')
        print(f'Кол-во штрафов в файле {filename}: {pen_counter}')
        return arms_count

    def lexeme(self, path: str, /):
        """
        Прогоняет программу по файлу с лексемами и записывает
        штрафы для каждой в новый файл result.txt
        """
        ext = path.split('/')[-1].split('.')[-1]
        if not (ext == 'csv'):
            with open(path) as f:
                text = f.readlines()
            with open("result.txt", 'w') as f:
                for line in text:
                    penalty = self.pen_count(line)[0]
                    f.write(line[:-1] + ' ' + str(penalty) + '\n')
            print("Штрафы записаны в файл result.txt")
            return
        with open(path, newline='') as f:
            csv_r = csv.reader(f)
            rows = []
            for row in csv_r:
                rows.append(row)
            for i in range(len(rows)):
                for item in rows[i]:
                    print(item)
                    if item.isnumeric():
                        continue
                    pen = self.pen_count(item)[0]
                    rows[i].append(pen)
                    print(rows[i])
                    break
        with open("result.csv", 'w', newline='') as f:
            csv_w = csv.writer(f)
            csv_w.writerows(rows)
        print("Штрафы записаны в файл result.csv")

    def pen_count(self, line: str, /):
        """
        Считает штрафы для рук и пальцев в строке
        """
        arm_count = [0] * 3  # левая, двуручие, правая
        pen_counter = 0
        fingers_count = [0] * 8  # 0 - 7 левый мизинец - правый
        for ch in line:
            if not ch.isalpha():
                continue

            k1 = self.keys.get(ch.lower(), 0)
            k2 = self.alts.get(ch.lower(), 0)
            if k1 == 0 and k2 == 0:
                continue

            # определение ближней клавиши
            if k2 == 0:
                k = k1
            elif k1 == 0:
                k = k2
            elif k1.penalty >= k2.penalty:
                k = k2
            else:
                k = k1

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
                    arm_count[2] += 1 + pen
            pen_counter += pen

            if k.arm == 'l':
                match k.finger:
                    case 'f5':
                        fingers_count[0] += pen
                    case 'f4':
                        fingers_count[1] += pen
                    case 'f3':
                        fingers_count[2] += pen
                    case 'f2':
                        fingers_count[3] += pen
            else:
                match k.finger:
                    case 'f2':
                        fingers_count[4] += pen
                    case 'f3':
                        fingers_count[5] += pen
                    case 'f4':
                        fingers_count[6] += pen
                    case 'f5':
                        fingers_count[7] += pen

            if ch.isupper() or k.alt:
                arm_count[1] += pen
            elif k.arm == 'l':
                arm_count[0] += pen
            else:
                arm_count[2] += pen

        return (pen_counter, fingers_count, arm_count)
