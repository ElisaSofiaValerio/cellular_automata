import numpy as np
from PyQt5 import QtWidgets, QtCore
import pyqtgraph as pg


from cellular_automata.algorithm.generation_computer import GenCompute


class GridInputWindow(QtWidgets.QWidget):
    def __init__(self, n=3):
        super().__init__()
        self.setWindowTitle("Input Kernel")
        self.setFixedSize(300, 300)

        self.grid_size = n
        self.layout = QtWidgets.QGridLayout(self)
        self.cells = []

        for i in range(n):
            row = []
            for j in range(n):
                cell = QtWidgets.QLineEdit(self)
                cell.setFixedSize(40, 40)
                cell.setAlignment(QtCore.Qt.AlignCenter)
                cell.setText('0')
                self.layout.addWidget(cell, i, j)
                row.append(cell)
            self.cells.append(row)

    def get_grid_data(self):
        return np.array([[float(col.text()) for col in row] for row in self.cells])


class MainWindow(QtWidgets.QWidget):

    def add_label_widget(self, name):
        self.controls.addWidget(QtWidgets.QLabel(name))
        object = QtWidgets.QSpinBox()
        object.setRange(10, 2000)
        object.setValue(10)
        self.controls.addWidget(object)
        return object

    def update_grid(self):
        # Clear old grid lines
        for line in self.grid_lines:
            self.plot.removeItem(line)
        self.grid_lines = []

        rows = self.rows.value()
        cols = self.cols.value()
        if self.grid is None:
            self.smaller_grid = np.random.choice([0, 1], size=(rows // 2, cols // 2), p=(float(self.zero_prob.text()), 1 - float(self.zero_prob.text())))
            self.grid = np.zeros(shape=(rows,cols))
            self.grid[rows//4: rows//4 + rows//2, cols // 4: cols//4 + cols//2] = self.smaller_grid
        self.update_image()
        if self.grid_active:
            pen = pg.mkPen(color=(200, 200, 200, 100), width=0.5)

            for x in range(1, cols):
                line = pg.InfiniteLine(pos=x, angle=90, pen=pen, movable=False)
                self.plot.addItem(line)
                self.grid_lines.append(line)

            for y in range(1, rows):
                line = pg.InfiniteLine(pos=y, angle=0, pen=pen, movable=False)
                self.plot.addItem(line)
                self.grid_lines.append(line)

    def update_image(self):
        display_array = self.grid * 255
        self.image_item.setImage(display_array.T, levels=(0, 255))
        self.image_item.setRect(pg.QtCore.QRectF(0, 0, self.grid.shape[1], self.grid.shape[0]))

    def on_click(self, event):
        scene_pos = event.scenePos()
        image_pos = self.image_item.mapFromScene(scene_pos)  # Apparently this is part of c++ backend for qt?

        rows, cols = self.grid.shape
        row = int(image_pos.y())
        col = int(image_pos.x())

        if 0 <= row < rows and 0 <= col < cols:
            self.grid[row, col] = 1 - self.grid[row, col]
            self.update_image()

    def on_grid_toggle(self):
        self.grid_active = not self.grid_active
        self.update_grid()

    def randoms(self):
        self.grid = None
        self.update_grid()

    def clear_screen(self):
        rows = self.rows.value()
        cols = self.cols.value()
        self.grid = np.zeros(shape=(rows, cols))
        self.update_grid()
        #print(self.grid_input_window.get_grid_data())

    def _step(self):
        bs_string = self.bs_text.text()
        b, s = bs_string.split('S')
        birth = [int(i) for i in b[1:]]
        survive = [int(i) for i in s]
        kernel = self.grid_input_window.get_grid_data()
        self.grid = self.computer.next_step(self.grid, kernel, birth, survive)
        self.update_image()

    def _start(self):
        if not self.is_running:
            self.is_running = True
            self.start_btn.setText('Stop')
            self.timer.start(self.speed.value())
        else:
            self.is_running = False
            self.start_btn.setText('Start')
            self.timer.stop()

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Cellular Automata with A LisaMasking")
        self.setGeometry(100, 100, 800, 800)
        self.computer = GenCompute()

        self.is_running = False
        self.grid = None
        self.grid_active = False
        self.main = QtWidgets.QVBoxLayout(self)
        self.controls = QtWidgets.QHBoxLayout()

        self.main.addLayout(self.controls)
        self.btn_set = QtWidgets.QPushButton("Set Grid")
        self.toggle_grid = QtWidgets.QPushButton("Toggle Grid")
        self.randomize_btn = QtWidgets.QPushButton("Randomize")
        self.clear_btn = QtWidgets.QPushButton("Clear")

        self.start_btn = QtWidgets.QPushButton("Start")
        self.step_btn = QtWidgets.QPushButton("1-Step")

        self.bs_text = QtWidgets.QLineEdit(self)
        self.bs_text.setText("BS Rule")

        self.rows = self.add_label_widget('Rows')
        self.cols = self.add_label_widget('Cols')

        self.controls.addWidget(self.btn_set)
        self.controls.addWidget(self.toggle_grid)
        self.controls.addWidget(self.randomize_btn)
        self.controls.addWidget(self.clear_btn)
        self.controls.addWidget(self.bs_text)
        self.controls.addWidget(self.start_btn)
        self.controls.addWidget(self.step_btn)
        self.speed = self.add_label_widget('Speed:')

        self.zero_prob = QtWidgets.QLineEdit(self)
        self.zero_prob.setText("0.9")

        # self.one_prob = QtWidgets.QLineEdit(self)
        # self.one_prob.setText("0.1")

        self.controls.addWidget(self.zero_prob)
        #self.controls.addWidget(self.one_prob)

        self.controls.addStretch(1)

        self.btn_set.clicked.connect(self.update_grid)
        self.toggle_grid.clicked.connect(self.on_grid_toggle)
        self.randomize_btn.clicked.connect(self.randoms)
        self.clear_btn.clicked.connect(self.clear_screen)
        self.start_btn.clicked.connect(self._start)
        self.step_btn.clicked.connect(self._step)

        self.view = pg.GraphicsLayoutWidget()
        self.main.addWidget(self.view)

        self.plot = self.view.addPlot()
        self.plot.setAspectLocked(True)
        self.plot.hideAxis('bottom')
        self.plot.hideAxis('left')
        #self.plot.vb.setMouseEnabled(x=False, y=False)
        self.image_item = pg.ImageItem()
        self.plot.addItem(self.image_item)

        self.grid_lines = []
        self.image_item.mouseClickEvent = self.on_click

        self.grid_input_window = GridInputWindow(n=3)
        self.grid_input_window.show()

        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self._step)

        self.update_grid()


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    gui = MainWindow()
    gui.resize(800, 850)
    gui.show()
    app.exec_()