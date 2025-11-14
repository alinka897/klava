import structs as s
import visual as v


def main():
    n = int(input("Выберете раскладку:\n1) ЙЦУКЕН\n" +
                  "2) Фонетическая\n3) Диктор\n4) Скоропись\n" +
                  "5) ANT\n6) Зубачев\n7) Вызов\n"))
    match n:
        case 1:
            layout = s.Layout()
            color = 'r' 
        case 2:
            layout = s.Layout('ю1234567890-ч', 'явертыуиопшщэ',
                              'асдфгхйкл;\'', 'зьцжбнм,./')
            color = 'm'
        case 3:
            layout = s.Layout('ё1234567890*=', 'цья,.звкдчшщ@',
                              'уиеоалнтсрй', 'фэхыюбмпгж')
            color = 'y'
        case 4:
            layout = s.Layout('*.ёъ?!@-\'()-"', 'цья,.звкдчшщ"',
                              'уиеоалнтсрй', 'фэхыюбмпгж')
            color = 'y'
        case 5:
            layout = s.Layout('\\!?\'"=+-*/%()', 'гпрдмыияухцжч',
                              'внстльоеакз', 'щйшб,.юэёф')
            color = 'g'
        case 6:
            layout = s.Layout('ё1234567890-=', 'фыая,ймрпхцщ\\',
                              'гиеоултмнзж', 'шью.эбдвкч')
            color = 'b'
        case 7:
            layout = s.Layout('@ё[{}(=*)+]!щ', 'быоуьёлдягжцъ',
                              'чиеа,.нтсвз', 'шхйк-/рмфп',
                              у='ю', ч='ц', е='э', н='щ', т='ъ')
            color = 'k'

    n = int(input("Что хотим сделать?\n1) Прогнать через файл\n" +
                  "2) Штрафы построчно\n3) Сравнение раскладок\n"))
    match n:
        case 1:
            path = input("Введите путь к файлу: ")
            penalty, fingers, arms = layout.readf(path)
            v.arm_pie(arms)
            v.fingers_bar(fingers, color)
        case 2:
            path = input("Введите путь к файлу: ")
            layout.lexeme(path)
        case 3:
            pass


if __name__ == "__main__":
    main()
