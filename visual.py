import matplotlib.pyplot as plt
import numpy as np
import pandas
import structs as s

for_title = dict(fontsize=18, color='k', fontweight='bold')
size = '14'
pie_colors = ['#90369c', '#55bda4', '#e88f2a']


def arm_pie(data: list, name: list, title: str, labels: list, /, ax=''):
    """
    Создание круговой диаграммы для рук (левая, правая, двуручие) и переборов
    """
    if ax == '':
        fig, ax = plt.subplots()
    title = title + f"{name}\nВсего: {sum(data)}"

    filtr_lab = [labels[i] for i in range(len(data)) if data[i] != 0]
    filtr_data = [data[i] for i in range(len(data)) if data[i] != 0]
    wedges, texts, autotexts = ax.pie(filtr_data, colors=pie_colors,
                                      autopct='%1.1f%%',
                                      textprops={'fontsize': size})
    ax.set_title(title, **for_title)
    lbs = [filtr_lab[i] + f' ({filtr_data[i]})' for i in range(len(filtr_data))] 
    ax.legend(wedges, labels=lbs, loc='upper right')


def arm_pies(l_arms, names, /, labels=["Левая", "Обе", "Правая"],
             title=''):
    col = round(len(l_arms) / 2)
    fig, axs = plt.subplots(2, col)
    
    for i in 0, 1:
        for j in range(col):
            index = i*col + j
            if col == 1:
                arm_pie(l_arms[index], names[index], title,
                        labels, ax=axs[i]) 
            else:
                if index > (len(l_arms) - 1):
                    fig.delaxes(axs[i, j]) 
                    continue
                arm_pie(l_arms[index], names[index], title,
                        labels, ax=axs[i, j]) 


def hbars(data, colors, names, ylabels, /, title=''):
    """
    Создание горизонтальных столбчатых диаграмм
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
        scale = 2.5
        ind = np.arange(len(df))*scale
        width = 0.3

        for i in range(len(names)):
            ax.barh(ind + i * width, getattr(df, names[i]),
                    width, color=colors[i], label=names[i])
            for index, value in enumerate(data[i]):
                if value == 0:
                    continue
                ax.text(value, index*scale + width * i, str(value), va='center')

        ax.set_title(title, **for_title)
        ax.set_yticks(ind, labels=df.graph, size=size)
    ax.legend()

    ax.set_xlabel("Кол-во штрафов", size=size)
    ax.ticklabel_format(axis='x', style='plain')
    ax.invert_yaxis()
    ax.tick_params(axis='x', labelsize=size)
    ax.set_axisbelow(True)
    ax.grid(axis='x', ls='dashed')


def bars(data, colors, names, xlabels, /, title=''):
    """
    Создание столбчатых диаграмм
    """
    x = xlabels

    fig, ax = plt.subplots()

    if isinstance(colors, str):
        y = data
        x_pos = np.arange(len(x))
        ax.bar(x_pos, y, color=colors, width=0.5, label=names)
        ax.set_title(title, **for_title)
        for i, v in enumerate(y):
            if v == 0:
                continue
            ax.text(i, v, str(v), size=size, ha='center')
        ax.set_xticks(ticks=x_pos, labels=x, size=size)

    else:
        d = dict(graph=x)
        for i in range(len(names)):
            d[names[i]] = data[i]

        df = pandas.DataFrame(d)
        scale = 2.5
        ind = np.arange(len(df))*scale
        width = 0.3

        for i in range(len(names)):
            ax.bar(ind + i * width, getattr(df, names[i]),
                    width, color=colors[i], label=names[i])
            for index, value in enumerate(data[i]):
                if value == 0:
                    continue
                ax.text(index*scale + width * i, value, str(value), ha='center')

        ax.set_title(title, **for_title)
        ax.set_xticks(ind, labels=df.graph, size=size)
    ax.legend()

    ax.set_ylabel("Кол-во", size=size)
    ax.ticklabel_format(axis='y', style='plain')
    ax.tick_params(axis='y', labelsize=size)
    ax.set_axisbelow(True)
    ax.grid(axis='y', ls='dashed')

def sum_bars(data, colors, names, title):
    x = names
    fig, ax = plt.subplots()
    y = data
    x_pos = np.arange(len(x))
    ax.bar(x_pos, y, color=colors, width=0.3, label=names)
    ax.set_title(title, **for_title)
    for i, v in enumerate(y):
        if v == 0:
            continue
        ax.text(i, v, str(v), size=size, ha='center')
    ax.set_xticks(ticks=x_pos, labels=x, size=size)
    ax.legend()

    ax.set_ylabel("Кол-во штрафов", size=size)
    ax.ticklabel_format(axis='y', style='plain')
    ax.tick_params(axis='y', labelsize=size)
    ax.set_axisbelow(True)
    ax.grid(axis='y', ls='dashed')


