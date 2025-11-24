import matplotlib.pyplot as plt
import numpy as np
import pandas
import structs as s

for_title = dict(fontsize=18, color='k', fontweight='bold')
size = '14'


def arm_pie(arms: list, name: list, /, ax=''):
    """
    Создание круговой диаграммы для рук (левая, правая, двуручие)
    """
    if ax == '':
        fig, ax = plt.subplots()
        title = f"Нагрузка на руки в тексте\n{name}"
    else:
        title = f"\n{name}"

    def abs(pct, arms):
        absolute = int(np.round(pct/100. * np.sum(arms)))
        return f'{pct: .1f}%\n({absolute: d})'

    labels = ["Левая рука", "Двуручие", "Правая рука"]
    filtr_lab = [labels[i] for i in range(len(arms)) if arms[i] != 0]
    filtr_arms = [arms[i] for i in range(len(arms)) if arms[i] != 0]
    wedges, texts, autotexts = ax.pie(filtr_arms, labels=filtr_lab,
                                      autopct=lambda pct: abs(pct, arms),
                                      textprops={'fontsize': size})
    plt.setp(autotexts, size=size)
    ax.set_title(title, **for_title)
    ax.text(0.9, 1.1, f'Всего штрафов: {sum(arms)}', fontsize=size,
             color='black', bbox=dict(boxstyle='round', facecolor='wheat',
             alpha=0.5))


def arm_pies(l_arms, names):
    col = round(len(l_arms) / 2)
    fig, axs = plt.subplots(2, col)
    
    for i in 0, 1:
        for j in range(col):
            index = i*col + j
            if col == 1:
                arm_pie(l_arms[index], names[index],
                        ax=axs[i]) 
            else:
                if index > (len(l_arms) - 1):
                    fig.delaxes(axs[i, j]) 
                    continue
                arm_pie(l_arms[index], names[index],
                        ax=axs[i, j]) 
    plt.tight_layout()


def hbars(data, colors, names, ylabels, /, title=''):
    """
    Создание столбчатых диаграмм
    """
    y = ylabels

    fig, ax = plt.subplots()

    if isinstance(colors, str):
        x = data
        y_pos = np.arange(len(y))
        ax.barh(y_pos, x, color=colors, height=0.5, label=names)
        ax.set_title(title, **for_title)
        for i, v in enumerate(x):
            if v == 0:
                continue
            ax.text(v, i, str(v), size=size, va='center')
        ax.set_yticks(ticks=y_pos, labels=y, size=size)

    else:
        d = dict(graph=y)
        for i in range(len(names)):
            d[names[i]] = data[i]

        df = pandas.DataFrame(d)

        ind = np.arange(len(df))
        width = 0.2

        for i in range(len(names)):
            ax.barh(ind + i * width, getattr(df, names[i]),
                    width, color=colors[i], label=names[i])
            for index, value in enumerate(data[i]):
                if value == 0:
                    continue
                ax.text(value, index + width * i, str(value), va='center')

        ax.set_title(title, **for_title)
        ax.set_yticks(ind + width, labels=df.graph, size=size)
    ax.legend()

    ax.set_xlabel("Кол-во штрафов", size=size)
    ax.ticklabel_format(axis='x', style='plain')
    ax.invert_yaxis()
    ax.tick_params(axis='x', labelsize=size)
    ax.set_axisbelow(True)
    ax.grid(axis='x', ls='dashed')
