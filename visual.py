import matplotlib.pyplot as plt
import numpy as np
import structs as s

def fingers_bar(fingers: list, color: str):
    """
    Столбчатая диаграмма с нагрузкой пальцев для одной раскладки
    """
    y = fingers
    x = ['f5 l', 'f4 l', 'f3 l', 'f2 l', 'f2 r', 'f3 r', 'f4 r', 'f5 r']

    plt.bar(x, y, color=color)
    plt.xlabel("Кол-во штрафов")
    plt.ylabel("Палец")
    plt.title("Нагрузка на пальцы в тексте")
    plt.show()
    

def arm_pie(arms: list):
    """
    Создание круговой диаграммы для рук (левая, правая, двуручие)
    """
    alabels = ["Левая рука", "Двуручие", "Правая рука"]

    plt.pie(arms, labels=alabels, autopct='%.1f%%')
    plt.title("Нагрузка на руки в тексте")
    plt.show()
    
