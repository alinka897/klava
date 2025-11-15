import matplotlib.pyplot as plt
import numpy as np
import pandas
import structs as s

def fingers_bar(fingers: list, color: str):
    """
    Столбчатая диаграмма с нагрузкой пальцев для одной раскладки
    """
    x = fingers
    y = ['Мизинец л', 'Безымянный л', 'Средний л', 'Указательный л',
         'Указательный п', 'Средний п', 'Безымянный п', 'Мизинец п']
    
    fig, ax = plt.subplots()
    y_pos = np.arange(len(y))
    ax.set_yticks(y_pos, labels=y)
    ax.invert_yaxis()
    ax.barh(y_pos, x, color=color)
    ax.set_xlabel("Кол-во штрафов")
    ax.set_title("Нагрузка на пальцы в тексте")
    for i, v in enumerate(x):
        ax.text(v, i, str(v))
    ax.ticklabel_format(axis='x', style='plain')
    plt.show()
    

def arm_pie(arms: list):
    """
    Создание круговой диаграммы для рук (левая, правая, двуручие)
    """
    alabels = ["Левая рука", "Двуручие", "Правая рука"]

    plt.pie(arms, labels=alabels, autopct='%.1f%%')
    plt.title("Нагрузка на руки в тексте")
    plt.show()
   
def compare(names: list, colors: list, l_fingers: list):
    
    y = ['Мизинец л', 'Безымянный л', 'Средний л', 'Указательный л',
         'Указательный п', 'Средний п', 'Безымянный п', 'Мизинец п']
    d = dict(graph=y)
    for i in range(len(names)):
        d[names[i]] = l_fingers[i]

    df = pandas.DataFrame(d) 
    
    ind = np.arange(len(df))
    width = 0.4

    fig, ax = plt.subplots()
    for i in range(len(names)):
        ax.barh(ind + i * width, getattr(df, names[i]),
                width, color=colors[i], label=names[i])

    ax.set(yticks=ind + width, yticklabels=df.graph, ylim=[2*width - 1, len(df)])
    ax.legend()

    plt.show()

