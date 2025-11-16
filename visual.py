import matplotlib.pyplot as plt
import numpy as np
import pandas
import structs as s

for_title = dict(fontsize=20, color='k', fontweight='bold')
size = '14'


def arm_pie(arms: list):
    """
    Создание круговой диаграммы для рук (левая, правая, двуручие)
    """
    fig, ax = plt.subplots()

    def abs(pct, arms):
        absolute = int(np.round(pct/100. * np.sum(arms)))
        return f'{pct: .1f}%\n({absolute: d})'

    labels = ["Левая рука", "Двуручие", "Правая рука"]
    filtr_lab = [labels[i] for i in range(len(arms)) if arms[i] != 0]
    filtr_arms = [arms[i] for i in range(len(arms)) if arms[i] != 0]
    wedges, texts, autotexts = ax.pie(filtr_arms, labels=filtr_lab,
                                      autopct=lambda pct: abs(pct, arms),
                                      textprops={'fontsize': size})
    plt.setp(autotexts, size=14)
    ax.set_title("Нагрузка на руки в тексте", **for_title)
#    plt.legend(title=f"Всего штрафов: {sum(arms)}")
    plt.text(0.9, 1.1, f'Всего штрафов: {sum(arms)}', fontsize=size,
             color='black', bbox=dict(boxstyle='round', facecolor='wheat',
             alpha=0.5))
    plt.show()


def fingers_bar(l_fingers, colors, names):

    y = ['Мизинец л', 'Безымянный л', 'Средний л', 'Указательный л',
         'Указательный п', 'Средний п', 'Безымянный п', 'Мизинец п']

    fig, ax = plt.subplots()

    if isinstance(colors, str):
        x = l_fingers
        y_pos = np.arange(len(y))
        ax.barh(y_pos, x, color=colors, height=0.5, label=names)
        ax.set_title("Нагрузка на пальцы в тексте", **for_title)
        for i, v in enumerate(x):
            if v == 0:
                continue
            ax.text(v, i, str(v), size=size, va='center')
        ax.set_yticks(ticks=y_pos, labels=y, size=size)

    else:
        d = dict(graph=y)
        for i in range(len(names)):
            d[names[i]] = l_fingers[i]

        df = pandas.DataFrame(d)

        ind = np.arange(len(df))
        width = 0.2

        for i in range(len(names)):
            ax.barh(ind + i * width, getattr(df, names[i]),
                    width, color=colors[i], label=names[i])
            for index, value in enumerate(l_fingers[i]):
                if value == 0:
                    continue
                ax.text(value, index + width * i, str(value), va='center')

        ax.set_title("Нагрузка на пальцы. Сравнение раскладок", **for_title)
        ax.set_yticks(ind + width, labels=df.graph, size=size)
    ax.legend()

    ax.set_xlabel("Кол-во штрафов", size=size)
    ax.ticklabel_format(axis='x', style='plain')
    ax.invert_yaxis()
    ax.tick_params(axis='x', labelsize=size)
    ax.set_axisbelow(True)
    ax.grid(axis='x', ls='dashed')
    plt.show()
