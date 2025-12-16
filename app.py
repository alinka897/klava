import structs as s
import visual as v
import matplotlib.pyplot as plt


def show(layout: list | s.Layout, path: str, /, static=True,
         linemode=False) -> None:
    """
    Отображение графиков в зависимости от параметров
    """
    filename = path.split('/')[-1]
    y = ['Мизинец л', 'Безымянный л', 'Средний л', 'Указательный л',
         'Указательный п', 'Средний п', 'Безымянный п', 'Мизинец п', 
         'Большой п', 'Большой л']
    if isinstance(layout, s.Layout):
        if static:
            penalty, fingers, arms = layout.readf(path, linemode=linemode)
            title = f"Нагрузка на пальцы в {filename}\n{layout.name}" 
            v.hbars(fingers, layout.color, layout.name, y, title)
            title = f"Нагрузка на руки в {filename}\n"
            labels = ["Левая", "Обе", "Правая"]
            v.arm_pie(arms, layout.name, title, labels)
        else:
            y = ['2 символа', '3 символа', '4 символа', '5 символов']
            convs, l_ch, r_ch = layout.per_readf(path, linemode=linemode)
            all_ch = [l_ch[i] + r_ch[i] for i in range(len(l_ch))]
            title = f"Удобные переборы. {filename}"
            v.bars(all_ch, layout.color, layout.name, y, title)
            title = "Кол-во удобных переборов\n"
            v.arm_pie(convs, layout.name, title, ['НУ', 'ЧУ', 'У'])
        plt.show()
        return
    los = layout
    colors = [lo.color for lo in los]
    names = [lo.name for lo in los]
    if static:
        rets = []
        for lo in los:
            ret = lo.readf(path)
            rets.append(ret)
            print(f"{lo.name} ☑")
        l_fingers = [ret[1] for ret in rets]
        l_sums = [sum(item) for item in l_fingers]
        l_arms = [ret[2] for ret in rets]
        v.arm_pies(l_arms, names)
        title = f"Общее кол-во штрафов. Сравнение раскладок в {filename}\n"
        v.sum_bars(l_sums, colors, names, title)
        plt.show()
        return
    y = ['2 символа', '3 символа', '4 символа', '5 символов']
    rets = []
    for lo in los:
        ret = lo.per_readf(path)
        rets.append(ret)
        print(f"{lo.name} ☑")
    l_convs = [ret[0] for ret in rets]
    l_l = [ret[1] for ret in rets]
    l_r = [ret[2] for ret in rets]
    l_all = []
    for litem, ritem in zip(l_l, l_r):
        item = []
        for i in range(len(litem)):
            item.append(litem[i] + ritem[i])
        l_all.append(item)
    labels = ['НУ', 'ЧУ', 'У']
    v.arm_pies(l_convs, names, labels=labels)
    title = f"Удобные переборы. {filename}"
    v.bars(l_all, colors, names, y, title) 
    plt.show()
    

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
            shifts = dict(zip('1234567890-;\',./', '!@ёЁъЪ&*()_:"<>?'))
            name = 'Фонетическая'
            layout = s.Layout('ю1234567890-ч', 'явертыуиопшщэ',
                              'асдфгхйкл;\'', 'зьцжбнм,./', name=name,
                              color=colors.get(name),
                              shifts=shifts)

        case 3:
            shifts = dict(zip('1234567890*=ь,.', 'ЪЬ№%:;-*()_+ъ?!'))
            name = 'Диктор'
            layout = s.Layout('ё1234567890*=', 'цья,.звкдчшщ😀',
                              'уиеоалнтсрй', 'фэхыюбмпгж', name=name,
                              color=colors.get(name),
                              shifts=shifts)
        case 4:
            name = 'Скоропись'
            layout = s.Layout('*.ёъ?!😀-\'()-«', 'цья,.звкдчшщ„',
                              'уиеоалнтсрй', 'фэхыюбмпгж', name=name,
                              color=colors.get(name))
        case 5:
            shifts = dict(zip('\\!?\'"=+-*/%(),.', '_9753102468«»;:'))
            name = 'ANT'
            layout = s.Layout('\\!?\'"=+-*/%()', 'гпрдмыияухцжч',
                              'внстльоеакз', 'щйшб,.юэёф', name=name,
                              color=colors.get(name),
                              shifts=shifts)
        case 6:
            shifts = dict(zip('1234567890-=,\\ь.', '!"№;%:?*()_+Ъ/ъЬ'))
            name = 'Зубачев'
            layout = s.Layout('ё1234567890-=', 'фыая,ймрпхцщ\\',
                              'гиеоултмнзж', 'шью.эбдвкч', name=name,
                              color=colors.get(name),
                              shifts=shifts)
        case 7:
            shifts = dict(zip('₽ё[{}(=*)+]!щ', '$%7531902468\''))
            name = 'Вызов'
            layout = s.Layout('₽ё[{}(=*)+]!щ', 'быоуьёлдягжцъ',
                              'чиеа,.нтсвз', 'шхйк-/рмфп', name=name,
                              shifts=shifts,
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
                    show(layout, path, static=static)

                else:
                    path = input("\nВведите путь к файлу: ")
                    show(layout, path, linemode=True, static=static)
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

        #except ValueError:
         #   print("\nВведите число!")

        except FileNotFoundError:
            print("\nФайл не найден!")

if __name__ == "__main__":
    main()
