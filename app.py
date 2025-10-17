import structs as s
# import visual

def main():
    n = int(input("Выберете раскладку:\n1) ЙЦУКЕН\n2) Фонетическая\n"))
    match n:
        case 1:
            l = s.Layout()
        case 2:
            l = s.Layout('ю1234567890-ч', 'явертыуиопшщэ', 'асдфгхйкл;\'', 'зьцжбнм,./')
    n = int(input("Что хотим сделать?\n1) Прогнать через файл\n2) Штрафы построчно\n"))
    match n:
        case 1:
            filename = input("Введите путь к файлу: ")
            l.readf(filename)
        case 2:
            filename = input("Введите путь к файлу: ")
            l.lexeme(filename)
    #l1.lexeme("1grams-3.txt")
    #l1.readf("voina-i-mir.txt")

    
if __name__ == "__main__":
    main()
