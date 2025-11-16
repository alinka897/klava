import structs as s
import visual as v


def check_nums(n, *nums):
    if any(n == num for num in nums):
        return 1
    else:
        print("\nВведите цифру из меню!")
        return 0


def choose_l(num: int) -> s.Layout:
    colors = dict(ЙЦУКЕН='#eb1535', Фонетическая='#e535fc', Диктор='#35cf06',
                  Скоропись='#22993c', ANT='#eb9409', Зубачев='#0967eb', Вызов='k')
    match num:
        case 1:
            
            name = 'ЙЦУКЕН'
            layout = s.Layout(name=name, color=colors.get(name))
        case 2:
            name = 'Фонетическая'
            layout = s.Layout('ю1234567890-ч', 'явертыуиопшщэ',
                              'асдфгхйкл;\'', 'зьцжбнм,./', name=name,
                              color=colors.get(name))

        case 3:
            name = 'Диктор'
            layout = s.Layout('ё1234567890*=', 'цья,.звкдчшщ@',
                              'уиеоалнтсрй', 'фэхыюбмпгж', name=name,
                              color=colors.get(name))
        case 4:
            name = 'Скоропись'
            layout = s.Layout('*.ёъ?!@-\'()-"', 'цья,.звкдчшщ"',
                              'уиеоалнтсрй', 'фэхыюбмпгж', name=name,
                              color=colors.get(name))
        case 5:
            name = 'ANT'
            layout = s.Layout('\\!?\'"=+-*/%()', 'гпрдмыияухцжч',
                              'внстльоеакз', 'щйшб,.юэёф', name=name,
                              color=colors.get(name))
        case 6:
            name = 'Зубачев'
            layout = s.Layout('ё1234567890-=', 'фыая,ймрпхцщ\\',
                              'гиеоултмнзж', 'шью.эбдвкч', name=name,
                              color=colors.get(name))
        case 7:
            name = 'Вызов'
            layout = s.Layout('@ё[{}(=*)+]!щ', 'быоуьёлдягжцъ',
                              'чиеа,.нтсвз', 'шхйк-/рмфп', name=name,
                              у='ю', ч='ц', е='э', н='щ', т='ъ')
    return layout


def main():
    while True:
        try:
            while True:
                n = int(input("\nЧто хотим сделать?\n1) Проанализировать" +
                              " одну раскладку\n2) Сравнить несколько" +
                              " раскладок\n"))
                if check_nums(n, 1, 2):
                    break
            if n == 1:
                while True:
                    n = int(input("\nВыберете раскладку:\n1) ЙЦУКЕН\n" +
                                  "2) Фонетическая\n3) Диктор\n" +
                                  "4) Скоропись\n5) ANT\n6) Зубачев\n" +
                                  "7) Вызов\n"))
                    if check_nums(n, *range(1, 8)):
                        break
                layout = choose_l(n)
                while True:
                    n = int(input("\nЧто хотим сделать?\n" +
                                  "1) Прогнать через файл\n" +
                                  "2) Штрафы построчно\n"))
                    if check_nums(n, 1, 2):
                        break
                    
                if n == 1:
                    path = input("\nВведите путь к файлу: ")
                    penalty, fingers, arms = layout.readf(path)
                    v.arm_pie(arms)
                    v.fingers_bar(fingers, layout.color, layout.name)
                else:
                    path = input("\nВведите путь к файлу: ")
                    layout.lexeme(path)
            else:
                while True:
                    print("\n1) ЙЦУКЕН\n" +
                          "2) Фонетическая\n3) Диктор\n4) Скоропись\n" +
                          "5) ANT\n6) Зубачев\n7) Вызов\n")
                    lo_nums = [int(i) for i in input("Введите номера" +
                               " нужных раскладок(через пробел): ").split()]
                    if all(check_nums(i, *range(1, 8)) for i in lo_nums):
                        break
                los = []
                for num in lo_nums:
                    los.append(choose_l(num))
                path = input("\nВведите путь к файлу: ")
                l_fingers = []
                colors = []
                names = []
                for lo in los:
                    l_fingers.append(lo.readf(path)[1])
                    colors.append(lo.color)
                    names.append(lo.name)
                v.fingers_bar(l_fingers, colors, names)
        except ValueError:
            print("\nВведите число!")

        except FileNotFoundError:
            print("\nФайл не найден!")

if __name__ == "__main__":
    main()
