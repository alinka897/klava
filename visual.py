import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# ---------- BASE STYLES ----------
BASE_TITLE = 18
BASE_LABEL = 14
BASE_TICK = 12
BASE_LEGEND = 12

pie_colors = ['#90369c', '#55bda4', '#e88f2a']


# ---------- ADAPTIVE SCALING ----------
def _auto_scale(ax):
    """
    Scale fonts & legend based on figure size (Qt-safe)
    """
    fig = ax.figure
    w, h = fig.get_size_inches()

    # reference ~8x6
    scale = min(w / 8, h / 6)
    scale = max(0.6, min(scale, 1.2))  # clamp

    # title
    if ax.title:
        ax.title.set_fontsize(BASE_TITLE * scale)

    # axis labels
    ax.xaxis.label.set_fontsize(BASE_LABEL * scale)
    ax.yaxis.label.set_fontsize(BASE_LABEL * scale)

    # ticks
    for t in ax.get_xticklabels() + ax.get_yticklabels():
        t.set_fontsize(BASE_TICK * scale)

    # legend
    leg = ax.get_legend()
    if leg:
        for t in leg.get_texts():
            t.set_fontsize(BASE_LEGEND * scale)

        # move legend if tight
        if w < 5:
            leg.set_bbox_to_anchor((1.02, 1))
            leg.set_loc("upper left")


# ---------- NUMBER FORMAT ----------
def for_text(text: str) -> str:
    if text.isnumeric():
        n = int(text)
        if 1_000 <= n < 1_000_000:
            return f"{n/1_000:.1f}k"
        if n >= 1_000_000:
            return f"{n/1_000_000:.1f}M"
    return text


# ---------- SUM BARS ----------
def sum_bars(data, colors, names, title, *, ax=None):
    created = ax is None
    if created:
        _, ax = plt.subplots()

    pos = np.arange(len(names))
    ax.bar(pos, data, color=colors, width=0.5)

    for i, v in enumerate(data):
        if v:
            ax.text(i, v, for_text(str(v)), ha='center', va='bottom')

    ax.set_xticks(pos, names)
    ax.set_title(title)
    ax.set_ylabel("Кол-во штрафов")
    ax.grid(axis='y', ls='dashed')

    _auto_scale(ax)
    if created:
        plt.tight_layout()


# ---------- PIE ----------
def arm_pie(data, name, title, labels, *, ax=None, mult=False):


    created = ax is None
    if created:
        _, ax = plt.subplots()

    total = sum(data)
    title = f"{name}\nВсего: {for_text(str(total))}"

    vals = [v for v in data if v != 0]
    labs = [labels[i] for i, v in enumerate(data) if v != 0]

    wedges, *_ = ax.pie(
        vals,
        colors=pie_colors,
        autopct='%1.1f%%',
        textprops={'fontsize': BASE_TICK}
    )

    ax.set_title(title)
    fig = ax.figure
    w, h = fig.get_size_inches()

    # Push legend further down for small windows
    legend_y = -0.10 if h < 4 else -0.07

    ax.legend(
        wedges,
        [f"{l} ({v})" for l, v in zip(labs, vals)],
        loc='upper center',
        bbox_to_anchor=(0.5, legend_y),
        ncol=1,
        frameon=False
    )

    ax.set_aspect('equal')
    _auto_scale(ax)

    if created:
        plt.tight_layout()


def arm_pies(l_arms, names, labels=("Левая", "Обе", "Правая"), title=""):
    count = len(l_arms)
    cols = 2
    rows = (count + 1) // 2

    fig, axs = plt.subplots(rows, cols)
    axs = np.atleast_2d(axs)

    for i, (data, name) in enumerate(zip(l_arms, names)):
        r, c = divmod(i, cols)
        arm_pie(data, name, title, labels, ax=axs[r, c])

    for i in range(count, rows * cols):
        fig.delaxes(axs.flatten()[i])

    plt.tight_layout()


# ---------- HORIZONTAL BARS ----------
def hbars(data, colors, names, ylabels, title="", *, ax=None, height=0.6):
    created = ax is None
    if created:
        _, ax = plt.subplots()

    if isinstance(colors, str):
        pos = np.arange(len(ylabels))
        ax.barh(pos, data, color=colors, height=height)

        for i, v in enumerate(data):
            if v:
                ax.text(v, i, for_text(str(v)), va='center')

        ax.set_yticks(pos, ylabels)

    else:
        df = pd.DataFrame(data, index=names, columns=ylabels).T
        scale = max(2.0, len(ylabels) * 0.6)
        ind = np.arange(len(df)) * scale
        width = scale / (len(names) + 1)

        for i, name in enumerate(names):
            ax.barh(ind + i * width, df[name], width, label=name)
            for j, v in enumerate(df[name]):
                if v:
                    ax.text(v, ind[j] + i * width, for_text(str(v)), va='center')

        ax.set_yticks(ind, df.index)

    ax.set_title(title)
    ax.set_xlabel("Кол-во штрафов")
    ax.legend()
    ax.invert_yaxis()
    ax.grid(axis='x', ls='dashed')

    _auto_scale(ax)
    if created:
        plt.tight_layout()


# ---------- VERTICAL BARS ----------
def bars(data, colors, names, xlabels, title="", *, ax=None):
    created = ax is None
    if created:
        _, ax = plt.subplots()

    if isinstance(colors, str):
        pos = np.arange(len(xlabels))
        ax.bar(pos, data, color=colors, width=0.5)

        for i, v in enumerate(data):
            if v:
                ax.text(i, v, for_text(str(v)), ha='center')

        ax.set_xticks(pos, xlabels)

    else:
        df = pd.DataFrame(data, index=names, columns=xlabels).T
        ind = np.arange(len(df)) * 2.5
        width = 0.3

        for i, name in enumerate(names):
            ax.bar(ind + i * width, df[name], width, label=name)
            for j, v in enumerate(df[name]):
                if v:
                    ax.text(ind[j] + i * width, v, for_text(str(v)), ha='center')

        ax.set_xticks(ind, df.index)

    ax.set_title(title)
    ax.set_ylabel("Кол-во")
    ax.legend()
    ax.grid(axis='y', ls='dashed')

    _auto_scale(ax)
    if created:
        plt.tight_layout()
