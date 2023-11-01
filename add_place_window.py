from PyQt5 import QtWidgets,QtGui
from math import *
from step_main_form import Popup
from database import check_input


class AddPlaceWindow(QtWidgets.QWidget):

    def __init__(self, **kvargs):
        super(AddPlaceWindow, self).__init__(**kvargs)

        self.setWindowTitle("Add new observation site")
        self.setWindowIcon(QtGui.QIcon("store--plus.png"))
        add_place_window_layout = QtWidgets.QGridLayout()
        self.setLayout(add_place_window_layout)

        self.add_place_lineedit = QtWidgets.QLineEdit()
        self.add_latitude_h_sign_combobox = QtWidgets.QComboBox()
        self.add_latitude_h_sign_combobox.addItems(["+", "-"])
        self.add_latitude_h_spinbox = QtWidgets.QSpinBox()
        self.add_latitude_h_spinbox.setRange(0, 89)
        self.add_latitude_m_spinbox = QtWidgets.QSpinBox()
        self.add_latitude_m_spinbox.setRange(0, 59)
        self.add_latitude_s_doublespinbox = QtWidgets.QDoubleSpinBox()
        self.add_latitude_s_doublespinbox.setRange(0, 59.99)
        self.add_longitude_h_lineedit = QtWidgets.QLineEdit()
        self.add_longitude_h_lineedit.setInputMask("B99")
        self.add_longitude_h_lineedit.setText("000")
        self.add_longitude_sign_combobox = QtWidgets.QComboBox()
        self.add_longitude_sign_combobox.addItems(["+", "-"])
        self.add_longitude_m_spinbox = QtWidgets.QSpinBox()
        self.add_longitude_m_spinbox.setRange(0, 59)
        self.add_longitude_s_doublespinbox = QtWidgets.QDoubleSpinBox()
        self.add_longitude_s_doublespinbox.setRange(0, 59.99)
        self.add_min_h_spinbox = QtWidgets.QSpinBox()
        self.add_min_h_spinbox.setRange(0, 70)
        self.add_max_sun_h_spinbox = QtWidgets.QSpinBox()
        self.add_max_sun_h_spinbox.setRange(-30, 50)
        self.add_place_ok_button = QtWidgets.QPushButton("OK")

        add_place_label = QtWidgets.QLabel("Observatine site: ")
        add_latitude_label = QtWidgets.QLabel("Latitude: ")
        add_longitude_label = QtWidgets.QLabel("Longitude: ")
        add_min_h_label = QtWidgets.QLabel("Min.object h: ")
        add_max_sun_h_label = QtWidgets.QLabel("Max Sun h:")



        add_latitude_h_label = QtWidgets.QLabel("°")
        add_latitude_m_label = QtWidgets.QLabel("'")
        add_latitude_s_label = QtWidgets.QLabel('"')
        add_longitude_h_label = QtWidgets.QLabel("°")
        add_longitude_m_label = QtWidgets.QLabel("'")
        add_longitude_s_label = QtWidgets.QLabel('"')


        add_place_window_layout.addWidget(add_place_label, 0, 0)
        add_place_window_layout.addWidget(self.add_place_lineedit, 0, 1, 1, 8)
        add_place_window_layout.addWidget(add_latitude_label, 1, 0)
        add_place_window_layout.addWidget(self.add_latitude_h_sign_combobox, 1, 1)
        add_place_window_layout.addWidget(self.add_latitude_h_spinbox, 1, 2, 1, 2)
        add_place_window_layout.addWidget(add_latitude_h_label, 1, 4)
        add_place_window_layout.addWidget(self.add_latitude_m_spinbox, 1, 5)
        add_place_window_layout.addWidget(add_latitude_m_label, 1, 6)
        add_place_window_layout.addWidget(self.add_latitude_s_doublespinbox, 1, 7)
        add_place_window_layout.addWidget(add_latitude_s_label, 1, 8)
        add_place_window_layout.addWidget(add_longitude_label, 2, 0)
        add_place_window_layout.addWidget(self.add_longitude_sign_combobox, 2, 1)
        add_place_window_layout.addWidget(self.add_longitude_h_lineedit, 2, 2, 1, 2)
        add_place_window_layout.addWidget(add_longitude_h_label, 2, 4)
        add_place_window_layout.addWidget(self.add_longitude_m_spinbox, 2, 5)
        add_place_window_layout.addWidget(add_longitude_m_label, 2, 6)
        add_place_window_layout.addWidget(self.add_longitude_s_doublespinbox, 2, 7)
        add_place_window_layout.addWidget(add_longitude_s_label, 2, 8)
        add_place_window_layout.addWidget(add_min_h_label, 3, 0)
        add_place_window_layout.addWidget(self.add_min_h_spinbox, 3, 1)
        add_place_window_layout.addWidget(add_max_sun_h_label, 3, 2, 1, 3)
        add_place_window_layout.addWidget(self.add_max_sun_h_spinbox, 3, 5)
        add_place_window_layout.addWidget(self.add_place_ok_button, 4, 0, 1, 7)

    def setup(self):
        from step_application import root
        self.step_main_form = root.step_main_form
        self.places = root.database.places
        self.user = root.database.user
        self.add_place_ok_button.clicked.connect(self.save_new_place)

    def save_new_place(self):
        name = self.add_place_lineedit.text()
        latitude_h = self.add_latitude_h_spinbox.value()
        latitude_m = self.add_latitude_m_spinbox.value()
        latitude_s = self.add_latitude_s_doublespinbox.value()
        latitude = radians(latitude_h + latitude_m/60 + latitude_s/3600)
        if self.add_latitude_h_sign_combobox.currentText() == "-":
            latitude = -latitude
        try:
            longitude_h = int(self.add_longitude_h_lineedit.text().strip())
        except:
            longitude_h = 0
        if longitude_h >= 180:
            longitude_h = 179
        longitude_m = self.add_longitude_m_spinbox.value()
        longitude_s = self.add_longitude_s_doublespinbox.value()
        longitude = radians(longitude_h + longitude_m / 60 + longitude_s / 3600)
        if self.add_longitude_sign_combobox.currentText() == "-":
            longitude = -longitude
        h = radians(self.add_min_h_spinbox.value())
        sun_h = radians(self.add_max_sun_h_spinbox.value())

        if check_input(name) and name:
            for place in self.places.observers():
                if place[1] == name:
                    a = Popup("Name exist", "This place name already exist. I can´t save it again",
                              buttons="Exit w/o save, Try again".split(","))
                    if a.do() == 0:
                        self.close()
                        return
                    else:
                        return
            self.places.add_observer(name, latitude, longitude, self.user.name(), sun_h, h)
            self.step_main_form.observer_combobox.addItem(name)
            self.step_main_form.observer_combobox.setCurrentText(name)
            self.step_main_form.observer_combobox.setEnabled(True)
            self.step_main_form.h_spinbox.setEnabled(True)
        else:
            a = Popup("Name error", "The name contains forbidden characters or it´s empty and will not be saved")
            a.do()
        self.close()

    def closeEvent(self, event):
        self.step_main_form.setEnabled(True)

class EditPlaceWindow(QtWidgets.QWidget):

    def __init__(self, **kvargs):
        super(EditPlaceWindow, self).__init__(**kvargs)

        self.setWindowTitle("Edit observation site")
        self.setWindowIcon(QtGui.QIcon("store-open.png"))
        add_place_window_layout = QtWidgets.QGridLayout()
        self.setLayout(add_place_window_layout)

        self.add_place_lineedit = QtWidgets.QLineEdit()
        self.add_latitude_h_sign_combobox = QtWidgets.QComboBox()
        self.add_latitude_h_sign_combobox.addItems(["+", "-"])
        self.add_latitude_h_spinbox = QtWidgets.QSpinBox()
        self.add_latitude_h_spinbox.setRange(0, 89)
        self.add_latitude_m_spinbox = QtWidgets.QSpinBox()
        self.add_latitude_m_spinbox.setRange(0, 59)
        self.add_latitude_s_doublespinbox = QtWidgets.QDoubleSpinBox()
        self.add_latitude_s_doublespinbox.setRange(0, 59.99)
        self.add_longitude_h_lineedit = QtWidgets.QLineEdit()
        self.add_longitude_h_lineedit.setInputMask("B99")
        self.add_longitude_h_lineedit.setText("000")
        self.add_longitude_sign_combobox = QtWidgets.QComboBox()
        self.add_longitude_sign_combobox.addItems(["+", "-"])
        self.add_longitude_m_spinbox = QtWidgets.QSpinBox()
        self.add_longitude_m_spinbox.setRange(0, 59)
        self.add_longitude_s_doublespinbox = QtWidgets.QDoubleSpinBox()
        self.add_longitude_s_doublespinbox.setRange(0, 59.99)
        self.add_min_h_spinbox = QtWidgets.QSpinBox()
        self.add_min_h_spinbox.setRange(0, 70)
        self.add_max_sun_h_spinbox = QtWidgets.QSpinBox()
        self.add_max_sun_h_spinbox.setRange(-30, 50)
        self.add_place_ok_button = QtWidgets.QPushButton("OK")

        add_place_label = QtWidgets.QLabel("Observatine site: ")
        add_latitude_label = QtWidgets.QLabel("Latitude: ")
        add_longitude_label = QtWidgets.QLabel("Longitude: ")
        add_min_h_label = QtWidgets.QLabel("Min.object h: ")
        add_max_sun_h_label = QtWidgets.QLabel("Max Sun h:")



        add_latitude_h_label = QtWidgets.QLabel("°")
        add_latitude_m_label = QtWidgets.QLabel("'")
        add_latitude_s_label = QtWidgets.QLabel('"')
        add_longitude_h_label = QtWidgets.QLabel("°")
        add_longitude_m_label = QtWidgets.QLabel("'")
        add_longitude_s_label = QtWidgets.QLabel('"')


        add_place_window_layout.addWidget(add_place_label, 0, 0)
        add_place_window_layout.addWidget(self.add_place_lineedit, 0, 1, 1, 8)
        add_place_window_layout.addWidget(add_latitude_label, 1, 0)
        add_place_window_layout.addWidget(self.add_latitude_h_sign_combobox, 1, 1)
        add_place_window_layout.addWidget(self.add_latitude_h_spinbox, 1, 2, 1, 2)
        add_place_window_layout.addWidget(add_latitude_h_label, 1, 4)
        add_place_window_layout.addWidget(self.add_latitude_m_spinbox, 1, 5)
        add_place_window_layout.addWidget(add_latitude_m_label, 1, 6)
        add_place_window_layout.addWidget(self.add_latitude_s_doublespinbox, 1, 7)
        add_place_window_layout.addWidget(add_latitude_s_label, 1, 8)
        add_place_window_layout.addWidget(add_longitude_label, 2, 0)
        add_place_window_layout.addWidget(self.add_longitude_sign_combobox, 2, 1)
        add_place_window_layout.addWidget(self.add_longitude_h_lineedit, 2, 2, 1, 2)
        add_place_window_layout.addWidget(add_longitude_h_label, 2, 4)
        add_place_window_layout.addWidget(self.add_longitude_m_spinbox, 2, 5)
        add_place_window_layout.addWidget(add_longitude_m_label, 2, 6)
        add_place_window_layout.addWidget(self.add_longitude_s_doublespinbox, 2, 7)
        add_place_window_layout.addWidget(add_longitude_s_label, 2, 8)
        add_place_window_layout.addWidget(add_min_h_label, 3, 0)
        add_place_window_layout.addWidget(self.add_min_h_spinbox, 3, 1)
        add_place_window_layout.addWidget(add_max_sun_h_label, 3, 2, 1, 3)
        add_place_window_layout.addWidget(self.add_max_sun_h_spinbox, 3, 5)
        add_place_window_layout.addWidget(self.add_place_ok_button, 4, 0, 1, 7)

    def setup(self):
        from step_application import root
        self.step_main_form = root.step_main_form
        self.places = root.database.places
        self.user = root.database.user
        self.add_place_ok_button.clicked.connect(self.edit_place)
        self.place = root.database.place

    def fill_place(self):
        self.add_place_lineedit.setText(self.place.name)
        latitude_text = self.place.latitude_text()
        longitude_text = self.place.longitude_text()
        self.add_latitude_h_sign_combobox.setCurrentText(latitude_text[0])
        self.add_longitude_sign_combobox.setCurrentText(longitude_text[0])
        latitude_list = latitude_text.split(" ")
        longitude_list = longitude_text.split(" ")
        self.add_latitude_h_spinbox.setValue(int(fabs(int(latitude_list[0]))))
        self.add_latitude_m_spinbox.setValue(int(latitude_list[1]))
        self.add_latitude_s_doublespinbox.setValue(float(latitude_list[2]))
        longitude_list[0] = longitude_list[0][1:len(longitude_list[0])]
        if len(longitude_list[0]) == 2:
            longitude_list[0] = "0" + longitude_list[0]
        self.add_longitude_h_lineedit.setText(str(longitude_list[0]))
        self.add_longitude_m_spinbox.setValue(int(longitude_list[1]))
        self.add_longitude_s_doublespinbox.setValue(float(longitude_list[2]))
        self.add_min_h_spinbox.setValue(int(self.step_main_form.h_spinbox.value()))
        self.add_max_sun_h_spinbox.setValue(int(self.step_main_form.sun_h_set_spinbox.value()))

    def edit_place(self):
        name = self.add_place_lineedit.text()
        latitude_h = self.add_latitude_h_spinbox.value()
        latitude_m = self.add_latitude_m_spinbox.value()
        latitude_s = self.add_latitude_s_doublespinbox.value()
        latitude = radians(latitude_h + latitude_m/60 + latitude_s/3600)
        if self.add_latitude_h_sign_combobox.currentText() == "-":
            latitude = -latitude
        try:
            longitude_h = int(self.add_longitude_h_lineedit.text().strip())
        except:
            longitude_h = 0
        if longitude_h >= 180:
            longitude_h = 179
        longitude_m = self.add_longitude_m_spinbox.value()
        longitude_s = self.add_longitude_s_doublespinbox.value()
        longitude = radians(longitude_h + longitude_m / 60 + longitude_s / 3600)
        if self.add_longitude_sign_combobox.currentText() == "-":
            longitude = -longitude
        h = radians(self.add_min_h_spinbox.value())
        sun_h = radians(self.add_max_sun_h_spinbox.value())

        if check_input(name) and name:
            for place in self.places.observers():
                if place[1] == name and name != self.place.name:
                    a = Popup("Name exist", "This place name already exist. I can´t save it again",
                              buttons="Exit w/o save, Try again".split(","))
                    if a.do() == 0:
                        self.close()
                        return
                    else:
                        return
            self.places.edit_place(name, self.place.name, longitude, latitude, h, sun_h)
            self.step_main_form.stars.change_place_in_place_list(name, self.place.name)
            self.step_main_form.observer_combobox.clear()
            self.step_main_form.observer_combobox.addItems(self.places.place_list(self.user.name()))
            self.step_main_form.observer_combobox.setCurrentText(name)
        else:
            a = Popup("Name error", "The name contains forbidden characters or it´s empty and will not be saved")
            a.do()
        self.close()

    def closeEvent(self, event):
        self.step_main_form.setEnabled(True)

