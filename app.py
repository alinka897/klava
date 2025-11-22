import structs as s
import visual as v
import matplotlib.pyplot as plt


def show(layout: list | s.Layout, path: str, /, static=True,
         linemode=False) -> None:
    """
    Отображение графиков в зависимости от параметров
    """
    if isinstance(layout, s.Layout):
        if linemode:
            penalty, fingers, arms = layout.readf(path, linemode=True)
        else:
            if static:
                penalty, fingers, arms = layout.readf(path)
            else:
                penalty, fingers, arms = layout.per_readf(path)
        v.arm_pie(arms, layout.name)
        v.fingers_bar(fingers, layout.color, layout.name)
        plt.show()
        return
    los = layout
    colors = [lo.color for lo in los]
    names = [lo.name for lo in los]
    if static:
        rets = [lo.readf(path) for lo in los]
        l_fingers = [ret[1] for ret in rets]
        l_arms = [ret[2] for ret in rets]
        v.arm_pies(l_arms, names)
        v.fingers_bar(l_fingers, colors, names)
        plt.show()
        return
    rets = [lo.per_readf(path) for lo in los]
    l_arms = [ret[0] for ret in rets]
    l_convs = [ret[1] for ret in rets]
    l_l = [ret[2] for ret in rets]
    l_r = [ret[3] for ret in rets]
    

def check_nums(n, *nums) -> None:
    if any(n == num for num in nums):
        return 1
    else:
        print("\nВведите цифру из меню!")
        return 0


def ask(text: str, *nums) -> int:
    while True:
        n = int(input(text))
        if check_nums(n, *nums):
            break
    return n


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


def main() -> None:
    while True:
        try:
            text = "\nКак считаем штрафы?\n1) Статически\n2) Динамически\n"
            n = ask(text, 1, 2)
            static = True if n == 1 else False
            text = ("\nЧто хотим сделать?\n1) Проанализировать" +
                    " одну раскладку\n2) Сравнить несколько" +
                    " раскладок\n")
            n = ask(text, 1, 2)
            if n == 1:
                text = ("\nВыберете раскладку:\n1) ЙЦУКЕН\n" +
                        "2) Фонетическая\n3) Диктор\n" +
                        "4) Скоропись\n5) ANT\n6) Зубачев\n" +
                        "7) Вызов\n")
                n = ask(text, *range(1, 8))
                layout = choose_l(n)
                text = ("\nЧто хотим сделать?\n" +
                       "1) Прогнать через файл\n" +
                       "2) Штрафы построчно\n")
                n = ask(text, 1, 2)
                    
                if n == 1:
                    path = input("\nВведите путь к файлу: ")
                    
                    if static:
                        show(layout, path)
                    else:
                        print(layout.per_readf(path))

                else:
                    path = input("\nВведите путь к файлу: ")
                    if static:
                        show(layout, path, linemode=True)
                    else:
                        layout.per_readf(path)
            else:
                while True:
                    print("\n1) ЙЦУКЕН\n" +
                          "2) Фонетическая\n3) Диктор\n4) Скоропись\n" +
                          "5) ANT\n6) Зубачев\n7) Вызов\n")
                    lo_nums = set(int(i) for i in input("Введите номера" +
                                  " нужных раскладок(через пробел): ").split())
                    if len(lo_nums) == 1:
                        print("\nВведите еще одну цифру!")
                        continue
                    if all(check_nums(i, *range(1, 8)) for i in lo_nums):
                        break
                los = []
                for num in lo_nums:
                    los.append(choose_l(num))

                path = input("\nВведите путь к файлу: ")
                show(los, path, static=static)

        except ValueError:
            print("\nВведите число!")

        except FileNotFoundError:
            print("\nФайл не найден!")

if __name__ == "__main__":
    main()
