import sys
from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QFileDialog, QLabel, QComboBox,
    QListWidget, QListWidgetItem, QRadioButton,
    QTabWidget, QMessageBox
)
from PySide6.QtCore import Qt

import structs as s
import visual as v
from plot_widget import PlotWidget
from PySide6.QtWidgets import QScrollArea


LAYOUTS = {
    "ЙЦУКЕН": 1,
    "Фонетическая": 2,
    "Диктор": 3,
    "Скоропись": 4,
    "ANT": 5,
    "Зубачев": 6,
    "Вызов": 7,
}

# --- Helper: make scrollable ---
def make_scrollable(widget: QWidget) -> QScrollArea:
    scroll = QScrollArea()
    scroll.setWidgetResizable(True)
    scroll.setWidget(widget)
    scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
    scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
    widget.setMinimumSize(800, 600)
    return scroll

def scale_fonts(ax, num_items):
    size = max(6, 12 - num_items)  # decrease font if many items
    for label in ax.get_xticklabels() + ax.get_yticklabels():
        label.set_fontsize(size)
    if ax.get_legend() is not None:
        for text in ax.get_legend().get_texts():
            text.set_fontsize(size)


def create_layout(num: int) -> s.Layout:
    from app import choose_l  # reuse your existing function
    return choose_l(num)


class KeyboardAnalyzer(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Keyboard Layout Analyzer")
        self.resize(1000, 700)

        self.file_path = None

        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout(self)

        # --- Controls ---
        controls = QHBoxLayout()

        self.layout_list = QListWidget()
        self.layout_list.setSelectionMode(QListWidget.MultiSelection)
        for name in LAYOUTS:
            self.layout_list.addItem(QListWidgetItem(name))

        controls.addWidget(self.layout_list)

        right_controls = QVBoxLayout()

        self.static_radio = QRadioButton("Static")
        self.dynamic_radio = QRadioButton("Dynamic")
        self.static_radio.setChecked(True)

        right_controls.addWidget(self.static_radio)
        right_controls.addWidget(self.dynamic_radio)

        self.file_label = QLabel("No file selected")
        file_btn = QPushButton("Choose File")
        file_btn.clicked.connect(self.choose_file)

        right_controls.addWidget(file_btn)
        right_controls.addWidget(self.file_label)

        analyze_btn = QPushButton("Analyze")
        analyze_btn.clicked.connect(self.analyze)

        right_controls.addWidget(analyze_btn)
        right_controls.addStretch()

        controls.addLayout(right_controls)
        main_layout.addLayout(controls)

        # --- Tabs with plots ---
        self.tabs = QTabWidget()

        self.finger_plot = PlotWidget()
        self.hand_plot = PlotWidget()
        self.extra_plot = PlotWidget()

        self.tabs.addTab(make_scrollable(self.finger_plot), "Fingers")
        self.tabs.addTab(make_scrollable(self.hand_plot), "Hands")
        self.tabs.addTab(make_scrollable(self.extra_plot), "Dynamic")

        main_layout.addWidget(self.tabs)

    def choose_file(self):
        path, _ = QFileDialog.getOpenFileName(self, "Select text file")
        if path:
            self.file_path = path
            self.file_label.setText(path)

    def analyze(self):
        if not self.file_path:
            QMessageBox.warning(self, "Error", "Please choose a file")
            return

        selected = self.layout_list.selectedItems()
        if not selected:
            QMessageBox.warning(self, "Error", "Select at least one layout")
            return

        layouts = [
            create_layout(LAYOUTS[item.text()])
            for item in selected
        ]

        static = self.static_radio.isChecked()

        self.finger_plot.clear()
        self.hand_plot.clear()
        self.extra_plot.clear()

        if static:
            self.run_static(layouts)
        else:
            self.run_dynamic(layouts)
        self.tabs.setTabEnabled(0, static)  # Fingers
        self.tabs.setTabEnabled(2, not static)  # Dynamic

        self.finger_plot.draw()
        self.hand_plot.draw()
        self.extra_plot.draw()

    def run_static(self, layouts):
        filename = self.file_path.split("/")[-1]
        y = [
            'Мизинец л', 'Безымянный л', 'Средний л', 'Указательный л',
            'Указательный п', 'Средний п', 'Безымянный п', 'Мизинец п',
            'Большой п', 'Большой л'
        ]

        # ---------- SINGLE LAYOUT ----------
        if len(layouts) == 1:
            lo = layouts[0]
            _, fingers, arms = lo.readf(self.file_path)

            # Finger load (single layout)
            self.finger_plot.figure.clear()
            ax1 = self.finger_plot.figure.add_subplot(111)
            v.hbars(fingers, lo.color, lo.name, y,
                    f" \n{filename}",
                    ax=ax1,
                    height=0.8)  # <--- increase from default (~0.4)
            scale_fonts(ax1, len(y))
            self.finger_plot.figure.tight_layout()

            # Hand load
            self.hand_plot.figure.clear()
            ax2 = self.hand_plot.figure.add_subplot(111)
            v.arm_pie(arms, lo.name, " \n", ["Left", "Both", "Right"], ax=ax2)
            scale_fonts(ax2, 3)
            self.hand_plot.figure.tight_layout()
            return

        # ---------- MULTIPLE LAYOUTS ----------
        rets = [lo.readf(self.file_path) for lo in layouts]
        fingers = [r[1] for r in rets]
        arms = [r[2] for r in rets]
        names = [lo.name for lo in layouts]
        colors = [lo.color for lo in layouts]

        # Finger comparison
        self.finger_plot.figure.clear()
        ax1 = self.finger_plot.figure.add_subplot(111)
        v.hbars(fingers, colors, names, y,
                f" \n{filename}",
                ax=ax1,
                height=0.8)  # <--- increase thickness
        scale_fonts(ax1, len(y))
        self.finger_plot.figure.tight_layout()

        # Hands: multiple pies
        self.hand_plot.figure.clear()
        fig = self.hand_plot.figure
        count = len(arms)
        cols = 2
        rows = (count + 1) // 2
        fig.set_size_inches(6 * cols, 4 * rows)  # dynamic size

        for i, (arm_data, name) in enumerate(zip(arms, names)):
            ax = fig.add_subplot(rows, cols, i + 1)
            v.arm_pie(arm_data, name, " \n", ["Left", "Both", "Right"], ax=ax)
            scale_fonts(ax, 3)

        fig.tight_layout()

    # --- DYNAMIC ANALYSIS ---
    def run_dynamic(self, layouts):
        y = ['2', '3', '4', '5']

        # ---------- SINGLE LAYOUT ----------
        if len(layouts) == 1:
            lo = layouts[0]
            convs, l_ch, r_ch = lo.per_readf(self.file_path)

            # Dynamic tab: LEFT + RIGHT
            self.extra_plot.figure.clear()
            fig = self.extra_plot.figure
            fig.set_size_inches(12, 5)
            ax1 = fig.add_subplot(1, 2, 1)
            v.bars(l_ch, lo.color, lo.name, y, "Left hand sequences", ax=ax1)
            scale_fonts(ax1, len(y))
            ax2 = fig.add_subplot(1, 2, 2)
            v.bars(r_ch, lo.color, lo.name, y, "Right hand sequences", ax=ax2)
            scale_fonts(ax2, len(y))
            fig.tight_layout()

            # Hands tab: sequence comfort
            self.hand_plot.figure.clear()
            ax3 = self.hand_plot.figure.add_subplot(111)
            v.arm_pie(convs, lo.name, "Sequence comfort\n", ['Bad', 'OK', 'Good'], ax=ax3)
            scale_fonts(ax3, 3)
            self.hand_plot.figure.tight_layout()
            return

        # ---------- MULTIPLE LAYOUTS ----------
        rets = [lo.per_readf(self.file_path) for lo in layouts]
        names = [lo.name for lo in layouts]
        colors = [lo.color for lo in layouts]

        convs = [r[0] for r in rets]
        l_ch = [r[1] for r in rets]
        r_ch = [r[2] for r in rets]

        # Dynamic tab: LEFT + RIGHT sequences
        self.extra_plot.figure.clear()
        fig = self.extra_plot.figure
        fig.set_size_inches(12, 5)
        ax1 = fig.add_subplot(1, 2, 1)
        v.bars(l_ch, colors, names, y, "Left hand sequences", ax=ax1)
        scale_fonts(ax1, len(y))
        ax2 = fig.add_subplot(1, 2, 2)
        v.bars(r_ch, colors, names, y, "Right hand sequences", ax=ax2)
        scale_fonts(ax2, len(y))
        fig.tight_layout()

        # Hands tab: multiple pies
        self.hand_plot.figure.clear()
        fig = self.hand_plot.figure
        count = len(convs)
        cols = 2
        rows = (count + 1) // 2
        fig.set_size_inches(6 * cols, 4 * rows)

        for i, (data, name) in enumerate(zip(convs, names)):
            ax = fig.add_subplot(rows, cols, i + 1)
            v.arm_pie(data, name, "Sequence comfort\n", ['Bad', 'OK', 'Good'], ax=ax)
            scale_fonts(ax, 3)

        fig.tight_layout()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = KeyboardAnalyzer()
    win.show()
    sys.exit(app.exec())
