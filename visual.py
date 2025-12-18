import matplotlib.pyplot as plt
import numpy as np
import pandas
import structs as s

for_title = dict(fontsize=18, color='k', fontweight='bold')
for_mult = dict(fontsize=14, color='k', fontweight='bold')
size = '14'
pie_colors = ['#90369c', '#55bda4', '#e88f2a']


def for_text(text: str) -> str:
    if text.isnumeric():
        if 3 < len(text) < 7:
            text = text[:-3] + '.' + text[-3] + 'k'
        if 6 < len(text) < 10:
            text = text[:-6] + '.' + text[-3] + 'M'
    return text


def arm_pie(data: list, name: list, title: str, labels: list, /, ax='',
            mult=False):
    """
    Создание круговой диаграммы для рук (левая, правая, двуручие) и переборов
    """
    if ax == '':
        fig, ax = plt.subplots()
        title = title + f"{name}\nВсего: {sum(data)}"

    if mult:
        title = f"{name}\nВсего: " + for_text(str(sum(data)))
    filtr_lab = [labels[i] for i in range(len(data)) if data[i] != 0]
    filtr_data = [data[i] for i in range(len(data)) if data[i] != 0]
    wedges, texts, autotexts = ax.pie(filtr_data, colors=pie_colors,
                                      autopct='%1.1f%%',
                                      textprops={'fontsize': size})
    if mult:
        ax.set_title(title, **for_mult, y=-0.2)
    else:
        ax.set_title(title, **for_title)
    lbs = [filtr_lab[i] + f' ({filtr_data[i]})'
           for i in range(len(filtr_data))] 
    if mult:
        return lbs, wedges
    else:
        ax.legend(wedges, labels=lbs, loc='upper right')
        plt.tight_layout()


def arm_pies(l_arms, names, /, labels=["Левая", "Обе", "Правая"],
             title=''):
    if len(l_arms) < 5:
        axs_num = len(l_arms) * 2
        row = 2
    else:
        row = 4
        axs_num = 16
    col = axs_num // row
    ratios = [2 if i % 2 == 0 else 1 for i in range(row)]
    fig, axs = plt.subplots(nrows=row, ncols=col,
                            gridspec_kw={'height_ratios': ratios})
    
    for i in range(row):
        for j in range(col):
            index = i*col + j
            if (i % 2 == 1):
                continue
            else:
                if index >= (len(l_arms) + col):
                    fig.delaxes(axs[i, j]) 
                    fig.delaxes(axs[i + 1, j]) 
                    continue
                if i == 2:
                    index -= col
                lbs, wedges = arm_pie(l_arms[index],
                                       names[index], title, labels,
                                       ax=axs[i, j], mult=True) 
                axs[i + 1, j].axis('off')
                axs[i + 1, j].legend(wedges, lbs, prop={'size':10},
                                     loc='upper center')

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
            ax.text(v, i, for_text(str(v)), size=size, va='center')
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
            ax.text(i, v, for_text(for_text(str(v))), size=size, ha='center')
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
    ax.tick_params(axis='y', labelsize=size)
    ax.set_axisbelow(True)
    ax.grid(axis='y', ls='dashed')

def sum_bars(data, colors, names, title):
    x = names
    fig, ax = plt.subplots()
    y = data
    x_pos = np.arange(len(x))
    ax.bar(x_pos, y, color=colors, width=0.1, label=names)
    ax.set_title(title, **for_title)
    for i, v in enumerate(y):
        if v == 0:
            continue
        ax.text(i, v, for_text(for_text(str(v))), size=size, ha='center')
    ax.set_xticks(ticks=x_pos, labels=x, size=size)
    ax.legend()

    ax.set_ylabel("Кол-во штрафов", size=size)
    ax.tick_params(axis='y', labelsize=size)
    ax.set_axisbelow(True)
    ax.grid(axis='y', ls='dashed')


