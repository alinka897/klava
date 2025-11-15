import structs as s
import visual as v


def check_nums(n, *nums):
    if any(n == num for num in nums):
        return 1
    else:
        print("Введите цифру из меню!")
        return 0


def choose_l(num: int) -> s.Layout:
    match num:
        case 1:
            layout = s.Layout(color='r')
            layout.name = 'ЙЦУКЕН'
        case 2:
            layout = s.Layout('ю1234567890-ч', 'явертыуиопшщэ',
                              'асдфгхйкл;\'', 'зьцжбнм,./', color='m')
            layout.name = 'Фонетическая'

        case 3:
            layout = s.Layout('ё1234567890*=', 'цья,.звкдчшщ@',
                              'уиеоалнтсрй', 'фэхыюбмпгж', color='y')
            layout.name = 'Диктор'
        case 4:
            layout = s.Layout('*.ёъ?!@-\'()-"', 'цья,.звкдчшщ"',
                              'уиеоалнтсрй', 'фэхыюбмпгж', color='y')
            layout.name = 'Скоропись'
        case 5:
            layout = s.Layout('\\!?\'"=+-*/%()', 'гпрдмыияухцжч',
                              'внстльоеакз', 'щйшб,.юэёф', color='g')
            layout.name = 'ANT'
        case 6:
            layout = s.Layout('ё1234567890-=', 'фыая,ймрпхцщ\\',
                              'гиеоултмнзж', 'шью.эбдвкч', color='b')
            layout.name = 'Зубачев'
        case 7:
            layout = s.Layout('@ё[{}(=*)+]!щ', 'быоуьёлдягжцъ',
                              'чиеа,.нтсвз', 'шхйк-/рмфп',
                              у='ю', ч='ц', е='э', н='щ', т='ъ')
            layout.name = 'Вызов'
    return layout


def main():
    while True:
        try:
            while True:
                n = int(input("Что хотим сделать?\n1) Проанализировать" +
                              " одну раскладку\n2) Сравнить несколько" +
                              " раскладок\n"))
                if check_nums(n, 1, 2):
                    break
            if n == 1:
                while True:
                    n = int(input("Выберете раскладку:\n1) ЙЦУКЕН\n" +
                                  "2) Фонетическая\n3) Диктор\n4) Скоропись\n" +
                                  "5) ANT\n6) Зубачев\n7) Вызов\n"))
                    if check_nums(n, *range(1, 8)):
                        break
                layout = choose_l(n)
                while True:
                    n = int(input("Что хотим сделать?\n1) Прогнать через файл\n" +
                                  "2) Штрафы построчно\n"))
                    if check_nums(n, 1, 2):
                        break
                match n:
                    case 1:
                        path = input("Введите путь к файлу: ")
                        penalty, fingers, arms = layout.readf(path)
                        v.arm_pie(arms)
                        v.fingers_bar(fingers, layout.color)
                    case 2:
                        path = input("Введите путь к файлу: ")
                        layout.lexeme(path)
            else:
                while True:
                    print("1) ЙЦУКЕН\n" +
                          "2) Фонетическая\n3) Диктор\n4) Скоропись\n" +
                          "5) ANT\n6) Зубачев\n7) Вызов\n")
                    lo_nums = [int(i) for i in input("Введите номера" +
                               " нужных раскладок(через пробел): ").split()]
                    if all(check_nums(i, *range(1, 8)) for i in lo_nums):
                        break
                los = []
                for num in lo_nums:
                    los.append(choose_l(num))
                path = input("Введите путь к файлу: ")
                l_fingers = []
                colors = []
                names = []
                for lo in los:
                    l_fingers.append(lo.readf(path)[1])
                    colors.append(lo.color)
                    names.append(lo.name)
                v.compare(names, colors, l_fingers)
        except ValueError:
            print("Введите число!")


if __name__ == "__main__":
    main()
