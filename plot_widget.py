from PySide6.QtWidgets import QWidget, QVBoxLayout
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from matplotlib.figure import Figure
def resizeEvent(self, event):
    for ax in self.figure.axes:
        from visual import _auto_scale
        _auto_scale(ax)
    self.canvas.draw_idle()
    super().resizeEvent(event)


class PlotWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.figure = Figure(figsize=(8, 6))  # 👈 important
        self.canvas = FigureCanvasQTAgg(self.figure)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.canvas)

    def clear(self):
        self.figure.clear()

    def draw(self):
        self.figure.tight_layout()
        self.canvas.draw()