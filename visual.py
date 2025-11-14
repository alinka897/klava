import matplotlib.pyplot as plt
import numpy as np
import structs as s

def fingers_plot(fingers_count: list):
    """
    Столбчатая диаграмма с нагрузкой пальцев для одной раскладки
    """
    
def arm_pie(arms: list):
    """
    Создание круговой диаграммы для рук (левая, правая, двуручие)
    """
    alabels = ["Левая рука", "Двуручие", "Правая рука"]

    plt.pie(arms, labels=alabels)
    plt.title("Нагрузка на руки в тексте")
    plt.show()
    
