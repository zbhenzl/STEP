from PyQt5 import QtWidgets
from database import *

class AddInstrumentWindow(QtWidgets.QWidget):

    def __init__(self, **kvargs):
        super(AddInstrumentWindow, self).__init__(**kvargs)

        self.setWindowTitle("Add telescope and equipment parameters")
        self.setWindowIcon(QtGui.QIcon("binocular--plus.png"))
        add_instrument_window_layout = QtWidgets.QFormLayout()
        self.setLayout(add_instrument_window_layout)

        self.add_telescop_name_lineedit = QtWidgets.QLineEdit()
        self.add_telescop_d_spinbox = QtWidgets.QSpinBox()
        self.add_telescop_d_spinbox.setRange(10, 5000)
        self.add_telescop_f_spinbox = QtWidgets.QSpinBox()
        self.add_telescop_f_spinbox.setRange(10, 10000)
        self.add_mount_name_lineedit = QtWidgets.QLineEdit()
        self.add_camera_name_lineedit = QtWidgets.QLineEdit()
        self.add_sensor_width_doublespinbox = QtWidgets.QDoubleSpinBox()
        self.add_sensor_width_doublespinbox.setRange(1, 50)
        self.add_sensor_height_doublespinbox = QtWidgets.QDoubleSpinBox()
        self.add_sensor_height_doublespinbox.setRange(1, 50)
        self.add_pixel_width_doublespinbox = QtWidgets.QDoubleSpinBox()
        self.add_pixel_width_doublespinbox.setRange(1, 20)
        self.add_pixel_height_doublespinbox = QtWidgets.QDoubleSpinBox()
        self.add_pixel_height_doublespinbox.setRange(1, 20)
        self.add_filter_set_lineedit = QtWidgets.QLineEdit()
        self.add_instrument_ok_button = QtWidgets.QPushButton("OK")

        add_instrument_window_layout.addRow(QtWidgets.QLabel("Telescope name: "), self.add_telescop_name_lineedit)
        add_instrument_window_layout.addRow(QtWidgets.QLabel("Mirror diameter(mm): "), self.add_telescop_d_spinbox)
        add_instrument_window_layout.addRow(QtWidgets.QLabel("Focal length(mm): "), self.add_telescop_f_spinbox)
        add_instrument_window_layout.addRow(QtWidgets.QLabel("Mount type: "), self.add_mount_name_lineedit)
        add_instrument_window_layout.addRow(QtWidgets.QLabel("Camera name: "), self.add_camera_name_lineedit)
        add_instrument_window_layout.addRow(QtWidgets.QLabel("Sensor Width(mm): "), self.add_sensor_width_doublespinbox)
        add_instrument_window_layout.addRow(QtWidgets.QLabel("Sensor Height(mm): "), self.add_sensor_height_doublespinbox)
        add_instrument_window_layout.addRow(QtWidgets.QLabel("Pixel Width(μm): "), self.add_pixel_width_doublespinbox)
        add_instrument_window_layout.addRow(QtWidgets.QLabel("Pixel Height(μm): "), self.add_pixel_height_doublespinbox)
        add_instrument_window_layout.addRow(QtWidgets.QLabel("Filter set: "), self.add_filter_set_lineedit)
        add_instrument_window_layout.addRow(None, self.add_instrument_ok_button)



    def setup(self):
        from step_application import root
        self.step_main_form = root.step_main_form
        self.database = root.database
        self.add_instrument_ok_button.clicked.connect(self.save_new_instrument)

    def save_new_instrument(self):
        if self.add_telescop_name_lineedit.text() == "" or self.add_telescop_name_lineedit.text() == " " \
                * len(self.add_telescop_name_lineedit.text()):
            msg_save = QtWidgets.QMessageBox()
            msg_save.setText("The marking of the telescope must be indicated")
            msg_save.exec()
        else:
            if check_input(self.add_telescop_name_lineedit.text(), special_characters=True, plus_minus=True) and \
                    check_input(self.add_mount_name_lineedit.text(), special_characters=True, plus_minus=True) and \
                    check_input(self.add_camera_name_lineedit.text(), special_characters=True, plus_minus=True) and \
                    check_input(self.add_filter_set_lineedit.text(), special_characters=True, plus_minus=True):
                observer_id = self.database.place.id
                name = self.add_telescop_name_lineedit.text()
                mirror = self.add_telescop_d_spinbox.value()
                focus = self.add_telescop_f_spinbox.value()
                mount = self.add_mount_name_lineedit.text()
                camera = self.add_camera_name_lineedit.text()
                sensor_w = self.add_sensor_width_doublespinbox.value()
                sensor_h = self.add_sensor_height_doublespinbox.value()
                pixel_w = self.add_pixel_width_doublespinbox.value()
                pixel_h = self.add_pixel_height_doublespinbox.value()
                filter_set = self.add_filter_set_lineedit.text()
                self.database.instruments.add_instrument(observer_id, name, mirror, focus, mount, camera, sensor_w, sensor_h, pixel_w, pixel_h, filter_set)
                new_text = name + " + " + mount + " + " + camera
                if self.step_main_form.instrument_combobox.currentText() == "add instrument":
                    self.step_main_form.instrument_combobox.clear()
                self.step_main_form.instrument_combobox.addItem(new_text)
                self.step_main_form.instrument_combobox.setEnabled(True)
                self.step_main_form.instrument_delete.setEnabled(True)
                self.step_main_form.instrument_combobox.setCurrentText(new_text)
            else:
                msg = QtWidgets.QMessageBox()
                msg.setText("Prohibited characters(only letters, numbers, space and +,-,/,{,},[,],|,<,>,% are allowed)")
                msg.exec()
            self.close()

    def closeEvent(self, event):
        self.step_main_form.setEnabled(True)
        # self.step_main_form.instrument_combobox.addItem(self.add_instrument_lineedit.text())
        # self.step_main_form.instrument_combobox.setCurrentText(self.add_instrument_lineedit.text())

class EditInstrumentWindow(QtWidgets.QWidget):

    def __init__(self, **kvargs):
        super(EditInstrumentWindow, self).__init__(**kvargs)

        self.setWindowTitle("Edit telescope and equipment parameters")
        self.setWindowIcon(QtGui.QIcon("binocular--pencil.png"))
        add_instrument_window_layout = QtWidgets.QFormLayout()
        self.setLayout(add_instrument_window_layout)

        self.add_telescop_name_lineedit = QtWidgets.QLineEdit()
        self.add_telescop_d_spinbox = QtWidgets.QSpinBox()
        self.add_telescop_d_spinbox.setRange(10, 5000)
        self.add_telescop_f_spinbox = QtWidgets.QSpinBox()
        self.add_telescop_f_spinbox.setRange(10, 10000)
        self.add_mount_name_lineedit = QtWidgets.QLineEdit()
        self.add_camera_name_lineedit = QtWidgets.QLineEdit()
        self.add_sensor_width_doublespinbox = QtWidgets.QDoubleSpinBox()
        self.add_sensor_width_doublespinbox.setRange(1, 50)
        self.add_sensor_height_doublespinbox = QtWidgets.QDoubleSpinBox()
        self.add_sensor_height_doublespinbox.setRange(1, 50)
        self.add_pixel_width_doublespinbox = QtWidgets.QDoubleSpinBox()
        self.add_pixel_width_doublespinbox.setRange(1, 20)
        self.add_pixel_height_doublespinbox = QtWidgets.QDoubleSpinBox()
        self.add_pixel_height_doublespinbox.setRange(1, 20)
        self.add_filter_set_lineedit = QtWidgets.QLineEdit()
        self.add_instrument_ok_button = QtWidgets.QPushButton("OK")

        add_instrument_window_layout.addRow(QtWidgets.QLabel("Telescope name: "), self.add_telescop_name_lineedit)
        add_instrument_window_layout.addRow(QtWidgets.QLabel("Mirror diameter(mm): "), self.add_telescop_d_spinbox)
        add_instrument_window_layout.addRow(QtWidgets.QLabel("Focal length(mm): "), self.add_telescop_f_spinbox)
        add_instrument_window_layout.addRow(QtWidgets.QLabel("Mount type: "), self.add_mount_name_lineedit)
        add_instrument_window_layout.addRow(QtWidgets.QLabel("Camera name: "), self.add_camera_name_lineedit)
        add_instrument_window_layout.addRow(QtWidgets.QLabel("Sensor Width(mm): "), self.add_sensor_width_doublespinbox)
        add_instrument_window_layout.addRow(QtWidgets.QLabel("Sensor Height(mm): "), self.add_sensor_height_doublespinbox)
        add_instrument_window_layout.addRow(QtWidgets.QLabel("Pixel Width(μm): "), self.add_pixel_width_doublespinbox)
        add_instrument_window_layout.addRow(QtWidgets.QLabel("Pixel Height(μm): "), self.add_pixel_height_doublespinbox)
        add_instrument_window_layout.addRow(QtWidgets.QLabel("Filter set: "), self.add_filter_set_lineedit)
        add_instrument_window_layout.addRow(None, self.add_instrument_ok_button)



    def setup(self):
        from step_application import root
        self.step_main_form = root.step_main_form
        self.database = root.database
        self.add_instrument_ok_button.clicked.connect(self.edit_instrument)
        self.instrument = root.database.instrument
        self.instruments = root.database.instruments
        self.place = root.database.place

    def fill_instrument(self):
        self.add_telescop_name_lineedit.setText(self.instrument.telescope())
        self.add_telescop_d_spinbox.setValue(int(self.instrument.diameter()))
        self.add_telescop_f_spinbox.setValue(int(self.instrument.focus()))
        self.add_mount_name_lineedit.setText(self.instrument.mount())
        self.add_camera_name_lineedit.setText(self.instrument.camera())
        self.add_sensor_width_doublespinbox.setValue(float(self.instrument.sensor_w()))
        self.add_sensor_height_doublespinbox.setValue(float(self.instrument.sensor_h()))
        self.add_pixel_width_doublespinbox.setValue(float(self.instrument.pixel_width()))
        self.add_pixel_height_doublespinbox.setValue(float(self.instrument.pixel_high()))
        self.add_filter_set_lineedit.setText(self.instrument.filter())

    def edit_instrument(self):
        if self.add_telescop_name_lineedit.text() == "" or self.add_telescop_name_lineedit.text() == " " \
                * len(self.add_telescop_name_lineedit.text()):
            msg_save = QtWidgets.QMessageBox()
            msg_save.setText("The marking of the telescope must be indicated")
            msg_save.exec()
        else:
            if check_input(self.add_telescop_name_lineedit.text(), special_characters=True, plus_minus=True) and \
                    check_input(self.add_mount_name_lineedit.text(), special_characters=True, plus_minus=True) and \
                    check_input(self.add_camera_name_lineedit.text(), special_characters=True, plus_minus=True) and \
                    check_input(self.add_filter_set_lineedit.text(), special_characters=True, plus_minus=True):
                name = self.add_telescop_name_lineedit.text()
                mirror = self.add_telescop_d_spinbox.value()
                focus = self.add_telescop_f_spinbox.value()
                mount = self.add_mount_name_lineedit.text()
                camera = self.add_camera_name_lineedit.text()
                sensor_w = self.add_sensor_width_doublespinbox.value()
                sensor_h = self.add_sensor_height_doublespinbox.value()
                pixel_w = self.add_pixel_width_doublespinbox.value()
                pixel_h = self.add_pixel_height_doublespinbox.value()
                filter_set = self.add_filter_set_lineedit.text()
                self.instruments.edit_instrument(self.instrument.id, name, mirror, focus, mount, camera, sensor_w, sensor_h, pixel_w, pixel_h, filter_set)
                new_text = name + " + " + mount + " + " + camera
                self.step_main_form.instrument_combobox.clear()
                self.step_main_form.instrument_combobox.addItems(self.instruments.instrument_list(self.place.id))
                self.step_main_form.instrument_combobox.setCurrentText(new_text)
            else:
                msg = QtWidgets.QMessageBox()
                msg.setText("Prohibited characters(only letters, numbers, space and +,-,/,{,},[,],|,<,>,% are allowed)")
                msg.exec()
            self.close()

    def closeEvent(self, event):
        self.step_main_form.setEnabled(True)
        # self.step_main_form.instrument_combobox.addItem(self.add_instrument_lineedit.text())
        # self.step_main_form.instrument_combobox.setCurrentText(self.add_instrument_lineedit.text())