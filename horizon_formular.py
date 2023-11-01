from database import *
from PyQt5 import QtWidgets

class SetHorizonWindow(QtWidgets.QWidget):

    def __init__(self, *args, **kwargs):
        super(SetHorizonWindow, self).__init__(*args, **kwargs)

        self.setWindowTitle("Horizon model")
        self.setWindowIcon(QtGui.QIcon("eye--pencil.png"))
        self.setMouseTracking(True)
        self.setFixedSize(1440, 430)

        # widgets and layouts
        horizon_window_layout = QtWidgets.QVBoxLayout()
        self.setLayout(horizon_window_layout)
        horizon_button_layout = QtWidgets.QHBoxLayout()
        add_groupbox = QtWidgets.QGroupBox("current cursor position")
        delete_groupbox = QtWidgets.QGroupBox("deleting points")
        add_layout = QtWidgets.QHBoxLayout()
        delete_layout = QtWidgets.QHBoxLayout()
        add_groupbox.setLayout(add_layout)
        delete_groupbox.setLayout(delete_layout)
        h_groupbox = QtWidgets.QGroupBox("Minimum observation altitude")
        h_layout = QtWidgets.QHBoxLayout()
        h_groupbox.setLayout(h_layout)
        self.h_label = QtWidgets.QLabel("Min.object altitude:  °")
        h_layout.addWidget(self.h_label)

        dec_groupbox = QtWidgets.QGroupBox("Star arc by declination")
        dec_layout = QtWidgets.QHBoxLayout()
        dec_groupbox.setLayout(dec_layout)
        self.dec_spinbox = QtWidgets.QSpinBox()
        self.dec_spinbox.setRange(-89,89)
        dec_label = QtWidgets.QLabel("Declination: ")
        dec_layout.addWidget(dec_label)
        dec_layout.addWidget(self.dec_spinbox)

        self.horizon_add_a_label = QtWidgets.QLabel()
        self.horizon_add_h_label = QtWidgets.QLabel()

        self.horizon_delete_point_button = QtWidgets.QPushButton("Delete Point")
        self.horizon_delete_combobox = QtWidgets.QComboBox()
        self.horizon_delete_combobox.setFixedWidth(120)

        logo_button = QtWidgets.QPushButton("")
        logo_button.setIcon(QtGui.QIcon("horizon.png"))
        logo_button.setIconSize(QtCore.QSize(230, 45))
        logo_button.setFixedSize(240, 55)

        add_layout.addWidget(self.horizon_add_a_label)
        add_layout.addWidget(self.horizon_add_h_label)
        delete_layout.addWidget(self.horizon_delete_combobox)
        delete_layout.addWidget(self.horizon_delete_point_button)

        horizon_button_layout.addWidget(logo_button)
        horizon_button_layout.addStretch()
        #horizon_button_layout.addWidget(rec_groupbox)
        horizon_button_layout.addWidget(dec_groupbox)
        horizon_button_layout.addWidget(h_groupbox)
        horizon_button_layout.addWidget(add_groupbox)
        horizon_button_layout.addWidget(delete_groupbox)
        horizon_window_layout.addStretch()
        horizon_window_layout.addLayout(horizon_button_layout)



    def setup(self):
        from step_application import root
        self.database = root.database
        self.place = self.database.place
        self.horizon = self.database.horizon
        self.azimuth = self.horizon.azimuth()
        self.h_altitude = self.horizon.h_altitude()
        self.step_main_form = root.step_main_form
        self.horizon_delete_point_button.clicked.connect(self.delete_point)

        self.dec_spinbox.setValue(30)
        self.h_label.setText("Min.object altitude: " + str(root.step_main_form.h_spinbox.value())+"°")
        self.fill_delete_combobox()

    def fill_delete_combobox(self):
        self.horizon_delete_combobox.clear()
        clear_azimuth = self.horizon.give_horizon()[0]
        clear_h = self.horizon.give_horizon()[1]
        if clear_azimuth:
            for i in range(len(clear_azimuth)):
                self.horizon_delete_combobox.addItem("A:" + str(clear_azimuth[i]) + " h:" + str(clear_h[i]))

    def delete_point(self):
            deleted_point_text = self.horizon_delete_combobox.currentText()
            h_index = deleted_point_text.index("h")
            a = int(deleted_point_text[2:h_index])
            self.horizon.delete_point(a)
            self.fill_delete_combobox()
            self.update()

    def closeEvent(self, event):
        self.database.horizons.save_horizon()

    def change_h(self, new_h):
        self.h_label.setText("Min.object altitude: " + str(new_h)+"°")

    def paintEvent(self, event):
        q = 1
        p = QtGui.QPainter(self)
        self.azimuth = self.horizon.azimuth()
        self.h_altitude = self.horizon.h_altitude()
        for j in range(360):
            for i in range(90):
                if self.azimuth[q] == j:
                    q=q+1
                h0 = self.h_altitude[q]
                h1 = self.h_altitude[q-1]
                a0 = self.azimuth[q]
                a1 = self.azimuth[q-1]
                akt_h_altitude = (h1 - h0) / (a1 - a0) * (j - a1) + h1
                if akt_h_altitude < i:
                     colour = QtCore.Qt.cyan
                     size = 4
                else:
                    colour = QtCore.Qt.green
                    size = 4
                p.fillRect(j * 4, (89 - i) * 4, size, size, QtGui.QBrush(colour))
        for i in range(len(self.azimuth)-1):
            p.drawLine(self.azimuth[i] * 4, (89 - self.h_altitude[i]) * 4, self.azimuth[i+1] * 4,
                       (89 - self.h_altitude[i+1]) * 4)
            if i > 0:
                p.fillRect(self.azimuth[i] * 4, (89 - self.h_altitude[i]) * 4 - 4, 3, 10,
                           QtGui.QBrush(QtCore.Qt.darkRed))
                p.fillRect(self.azimuth[i] * 4 - 4, (89 - self.h_altitude[i]) * 4, 10, 3,
                           QtGui.QBrush(QtCore.Qt.darkRed))
            else:
                zero_position = self.horizon.give_horizon()[0]
                if zero_position:
                    if 0 in zero_position:
                        p.fillRect(self.azimuth[i] * 4, (89 - self.h_altitude[i]) * 4 - 4, 3, 10,
                                   QtGui.QBrush(QtCore.Qt.darkRed))
                        p.fillRect(self.azimuth[i] * 4 - 4, (89 - self.h_altitude[i]) * 4, 10, 3,
                                   QtGui.QBrush(QtCore.Qt.darkRed))

        min_h = int((89 - self.step_main_form.h_spinbox.value()) * 4)
        if min_h > 250:
            min_h_text = int(min_h - 20)
        else:
            min_h_text = int(min_h + 20)

        p.drawStaticText(30, min_h_text, QtGui.QStaticText("Minimum object altitude"))
        h_line = QtCore.QLine(0, min_h, 1440, min_h)
        l_line_pen = QtGui.QPen(QtCore.Qt.blue)
        l_line_pen.setWidth(1)
        p.setPen(l_line_pen)
        p.drawLine(h_line)
        l_line_pen = QtGui.QPen(QtCore.Qt.red)
        l_line_pen.setWidth(2)
        p.setPen(l_line_pen)
        point_list = half_arc_A_h(self.database.place.latitude, radians(self.dec_spinbox.value()), 0, 300)
        for i in range(1, len(point_list[0])):

            x1: int = int(point_list[0][i - 1] * 4)
            y1: int = int((89 - point_list[1][i - 1]) * 4)
            x2: int = int(point_list[0][i] * 4)
            y2: int = int((89 - point_list[1][i]) * 4)
            if x1 - x2 < -720:
                pass
            elif x1 - x2 > 720:
                pass
            else:
                p.drawLine(x1, y1, x2, y2)

        p.end()

    def mouseMoveEvent(self, event):
        x = int(event.x() / 4)
        y = 89 - int(event.y() / 4)
        if y < 0:
            y = 0
        self.horizon_add_a_label.setText("Azimuth : " + str(x))
        self.horizon_add_h_label.setText("  h : " + str(y))

    def mousePressEvent(self, event):
        try:
            x = int(event.x() / 4)
            y = int(event.y() / 4)
            if x in self.azimuth:
                x_index = self.azimuth.index(x)
                if self.h_altitude[x_index] == 89 - y:
                    self.horizon.delete_point(x)
                else:
                    self.horizon.insert_point(x, 89 - y)
            else:
                self.horizon.insert_point(x, 89 - y)
        except IndexError:
            pass
        self.fill_delete_combobox()
        self.update()
