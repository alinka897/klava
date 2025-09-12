def mkdict(wtraf, ls, v, /):
    d = dict()
    for k in ls:
        d[k] = v
    wtraf.update(d)

    
def rasklad():
    regular = dict(list(zip('йцукенгшщзхъ', range(16, 28))) +
                   list(zip('фывапролджэ', range(30, 41))) +
                   list(zip('ячсмитьбю.', range(44, 54))))
    return regular


def mkwtraf():
    wtraf = dict()
    l1 = (list(range(16, 20)) + list(range(22, 26)) +
          list(range(44, 48)) + list(range(50, 54)) + [34, 35, 41])
    mkdict(wtraf, l1, 1)
    l0 = list(range(30,34)) + list(range(36, 40))
    mkdict(wtraf, l0, 0)
    l2 = [20, 21, 48, 49, 26]
    mkdict(wtraf, l2, 2)
    return wtraf


def readf(filename, wtraf, rasklad, /):
    counter = 0
    with open(filename) as f:
        text = f.readlines()
        for line in text:
            for ch in line:
                if not(ch in rasklad.keys()):
                    pass
                else:
                    nomer = rasklad[ch]
                    counter = counter + wtraf[nomer]
    print(f'Кол-во штрафов: {counter}')


def main():
    readf('test.txt', mkwtraf(), rasklad())

if __name__ == '__main__':
    main()
