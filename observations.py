from datetime import *

from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import QTime, QDate
from slunce_mesic import *
from time_period import *
from object import *
from astropy.coordinates import angular_separation



class ObservationLogsWindow(QtWidgets.QWidget):

    def __init__(self, *args, **kwargs):
        super(ObservationLogsWindow, self).__init__(*args, **kwargs)

        self.selected_star_name = ""
        self.selected_date = datetime.now()
        self.object_list = []
        self.object_type_list = [""]
        self.place_list = []
        self.instrument_list_id = []
        self.star = None
        self.place_latitude = None
        self.place_longitude = None
        self.filters_list = ["Clear", "Johnson B", "Johnson V", "Johnson R", "Johnson I", "Sloan u", "Sloan g",
                             "Sloan r", "Sloan i", "L", "R", "G", "B", "H-alfa", "S II", "O III"]

        self.setWindowTitle("Observation Logs")
        self.setWindowIcon(QtGui.QIcon("binocular--exclamation.png"))
        self.observation_window_layout = QtWidgets.QGridLayout()
        self.setLayout(self.observation_window_layout)

        self.find_variable_lineedit = QtWidgets.QLineEdit()
        self.find_variable_lineedit.setMinimumWidth(180)
        self.find_date_start_date_edit = QtWidgets.QDateEdit()
        self.find_date_start_date_edit.setDate(self.selected_date)
        self.find_date_end_date_edit = QtWidgets.QDateEdit()
        self.find_date_end_date_edit.setDate(self.selected_date)
        self.find_full_text_lineedit = QtWidgets.QLineEdit()
        self.find_full_text_lineedit.setMinimumWidth(200)
        self.find_by_filter_combobox = QtWidgets.QComboBox()
        self.find_by_filter_combobox.addItems([""] + self.filters_list)

        self.choice_place_combobox = QtWidgets.QComboBox()
        self.choice_instrument_combobox = QtWidgets.QComboBox()
        self.choice_instrument_combobox.setMinimumWidth(200)
        self.choice_star_combobox = QtWidgets.QComboBox()
        self.choice_star_combobox.setMinimumWidth(200)

        self.sunset_date_date_edit = QtWidgets.QDateEdit()
        self.time_time_edit = QtWidgets.QTimeEdit()
        self.time_time_edit.setTime(QTime(23, 59, 0))
        self.name_lineedit = QtWidgets.QLineEdit()
        self.pair_combobox = QtWidgets.QComboBox()
        self.p_s_combobox = QtWidgets.QComboBox()
        self.star_type_combobox = QtWidgets.QComboBox()
        self.star_type_lineedit = QtWidgets.QLineEdit()
        self.star_type_lineedit.setMaximumWidth(80)
        self.const_combobox = QtWidgets.QComboBox()
        self.telescope_lineedit = QtWidgets.QLineEdit()
        self.mount_lineedit = QtWidgets.QLineEdit()
        self.camera_lineedit = QtWidgets.QLineEdit()
        self.photometric_filter_combobox = QtWidgets.QComboBox()
        self.place_lineedit = QtWidgets.QLineEdit()
        self.place_latitude_lineedit = QtWidgets.QLineEdit()
        self.place_longitude_lineedit = QtWidgets.QLineEdit()
        self.weather_textedit = QtWidgets.QTextEdit()
        self.moon_distance_lineedit = QtWidgets.QLineEdit()
        self.moon_lineedit = QtWidgets.QLineEdit()
        self.h_at_min_lineedit = QtWidgets.QLineEdit()
        self.processed_combobox = QtWidgets.QComboBox()
        self.select_by_processed_combobox = QtWidgets.QComboBox()
        self.note1_textedit = QtWidgets.QTextEdit()
        self.note2_textedit = QtWidgets.QTextEdit()
        self.note3_textedit = QtWidgets.QTextEdit()
        self.note4_textedit = QtWidgets.QTextEdit()
        self.note5_textedit = QtWidgets.QTextEdit()
        self.new_log_radiobutton = QtWidgets.QRadioButton("New log")
        self.edit_log_radiobutton = QtWidgets.QRadioButton("Edit log")
        self.save_button = QtWidgets.QPushButton("SAVE")
        self.delete_button = QtWidgets.QPushButton("DELETE")
        self.log_table_widget = QtWidgets.QTableWidget()
        self.log_table_widget.setMinimumHeight(300)
        self.binning_combobox = QtWidgets.QComboBox()
        self.binning_combobox.addItems(["1", "2", "3", "4", "5"])
        self.exposure_label = QtWidgets.QLineEdit()
        self.by_prediction_checkbox = QtWidgets.QCheckBox("by predictions")

        self.build()

    def build(self):
        log_find_groupbox = QtWidgets.QGroupBox("Select log")
        log_find_layout = QtWidgets.QHBoxLayout()
        log_find_groupbox.setLayout(log_find_layout)

        log_find_layout.addWidget(QtWidgets.QLabel("Star:"))
        log_find_layout.addWidget(self.find_variable_lineedit)
        log_find_layout.addWidget(self.by_prediction_checkbox)
        log_find_layout.addWidget(QtWidgets.QLabel("Start:"))
        log_find_layout.addWidget(self.find_date_start_date_edit)
        log_find_layout.addWidget(QtWidgets.QLabel("End:"))
        log_find_layout.addWidget(self.find_date_end_date_edit)
        log_find_layout.addWidget(QtWidgets.QLabel("Star type:"))
        log_find_layout.addWidget(self.star_type_lineedit)
        log_find_layout.addWidget(QtWidgets.QLabel("Filter:"))
        log_find_layout.addWidget(self.find_by_filter_combobox)
        log_find_layout.addWidget(QtWidgets.QLabel("Processed:"))
        log_find_layout.addWidget(self.select_by_processed_combobox)
        log_find_layout.addWidget(QtWidgets.QLabel("Full text:"))
        log_find_layout.addWidget(self.find_full_text_lineedit)

        choice_groupbox = QtWidgets.QGroupBox("Choice item from database")
        choice_layout = QtWidgets.QHBoxLayout()
        choice_groupbox.setLayout(choice_layout)

        choice_layout.addWidget(self.new_log_radiobutton)
        self.new_log_radiobutton.setChecked(True)
        choice_layout.addWidget(self.edit_log_radiobutton)
        choice_layout.addWidget(QtWidgets.QLabel("Place:"))
        choice_layout.addWidget(self.choice_place_combobox)
        choice_layout.addWidget(QtWidgets.QLabel("Instrument:"))
        choice_layout.addWidget(self.choice_instrument_combobox)
        choice_layout.addWidget(QtWidgets.QLabel("Star:"))
        choice_layout.addWidget(self.choice_star_combobox)

        edit_groupbox = QtWidgets.QGroupBox("Add or Edit log")
        edit_layout = QtWidgets.QGridLayout()
        edit_groupbox.setLayout(edit_layout)

        edit_layout.addWidget(QtWidgets.QLabel("Date:"), 0, 0)
        edit_layout.addWidget(self.sunset_date_date_edit, 0, 1)
        edit_layout.addWidget(self.time_time_edit, 0, 2)
        edit_layout.addWidget(QtWidgets.QLabel("Star name:"), 0, 3)
        edit_layout.addWidget(self.name_lineedit, 0, 4, 1, 2)
        edit_layout.addWidget(QtWidgets.QLabel("Pair:"), 0, 6)
        edit_layout.addWidget(self.pair_combobox, 0, 7)
        edit_layout.addWidget(QtWidgets.QLabel("p/s:"), 0, 8)
        edit_layout.addWidget(self.p_s_combobox, 0, 9)
        edit_layout.addWidget(QtWidgets.QLabel("Star type:"), 0, 10)
        edit_layout.addWidget(self.star_type_combobox, 0, 11, 1, 2)
        edit_layout.addWidget(QtWidgets.QLabel("Const.:"), 0, 13)
        edit_layout.addWidget(self.const_combobox, 0, 14)
        edit_layout.addWidget(QtWidgets.QLabel("Processed:"), 0, 15)
        edit_layout.addWidget(self.processed_combobox, 0, 16)
        edit_layout.addWidget(self.save_button, 0, 17)

        edit_layout.addWidget(QtWidgets.QLabel("Place:"), 1, 0)
        edit_layout.addWidget(self.place_lineedit, 1, 1, 1, 2)
        edit_layout.addWidget(QtWidgets.QLabel("Latitude:"), 1, 3)
        edit_layout.addWidget(self.place_latitude_lineedit, 1, 4)
        edit_layout.addWidget(QtWidgets.QLabel("Longitude:"), 1, 5)
        edit_layout.addWidget(self.place_longitude_lineedit, 1, 6, 1, 2)
        edit_layout.addWidget(QtWidgets.QLabel("Moon dist.:"), 1, 8, 1, 2)
        edit_layout.addWidget(self.moon_distance_lineedit, 1, 10, 1, 3)
        edit_layout.addWidget(QtWidgets.QLabel("Moon phase:"), 1, 13)
        edit_layout.addWidget(self.moon_lineedit, 1, 14, 1, 2)
        edit_layout.addWidget(self.delete_button, 1, 17)

        edit_layout.addWidget(QtWidgets.QLabel("Telescope:"), 2, 0)
        edit_layout.addWidget(self.telescope_lineedit, 2, 1, 1, 2)
        edit_layout.addWidget(QtWidgets.QLabel("Mount:"), 2, 3)
        edit_layout.addWidget(self.mount_lineedit, 2, 4)
        edit_layout.addWidget(QtWidgets.QLabel("Camera:"), 2, 5)
        edit_layout.addWidget(self.camera_lineedit, 2, 6, 1, 2)
        edit_layout.addWidget(QtWidgets.QLabel("Filter:"), 2, 8, 1, 2)
        edit_layout.addWidget(self.photometric_filter_combobox, 2, 10)
        edit_layout.addWidget(QtWidgets.QLabel("Bin:"), 2, 11)
        edit_layout.addWidget(self.binning_combobox, 2, 12)
        edit_layout.addWidget(QtWidgets.QLabel("Exposure:"), 2, 13)
        edit_layout.addWidget(self.exposure_label, 2, 14, 1, 2)
        edit_layout.addWidget(QtWidgets.QLabel("h at min.:"), 2, 16)
        edit_layout.addWidget(self.h_at_min_lineedit, 2, 17)

        note_groupbox = QtWidgets.QGroupBox("Notes")
        note_layout = QtWidgets.QGridLayout()
        note_groupbox.setLayout(note_layout)

        note_layout.addWidget(QtWidgets.QLabel("Weather:"), 0, 0)
        note_layout.addWidget(QtWidgets.QLabel("Note1:"), 0, 1)
        note_layout.addWidget(QtWidgets.QLabel("Note2:"), 0, 2)
        note_layout.addWidget(self.weather_textedit, 1, 0)
        note_layout.addWidget(self.note1_textedit, 1, 1)
        note_layout.addWidget(self.note2_textedit, 1, 2)

        table_groupbox = QtWidgets.QGroupBox("Log table")
        table_layout = QtWidgets.QHBoxLayout()
        table_groupbox.setLayout(table_layout)

        table_layout.addWidget(self.log_table_widget)

        self.observation_window_layout.addWidget(log_find_groupbox, 0, 0, 1, 2)
        self.observation_window_layout.addWidget(choice_groupbox, 1, 0, 1, 2)
        self.observation_window_layout.addWidget(edit_groupbox, 2, 0, 1, 2)
        self.observation_window_layout.addWidget(note_groupbox, 3, 0, 1, 2)
        self.observation_window_layout.addWidget(table_groupbox, 4, 0, 1, 2)

    def setup(self):
        from step_application import root
        self.database = root.database
        self.step_main_form = root.step_main_form
        self.prediction2 = self.step_main_form.prediction2
        self.places = self.database.places
        self.stars = root.database.stars
        self.variables = root.database.variables
        self.instruments = root.database.instruments
        self.instrument = root.database.instrument
        self.user = root.database.user
        self.observation_logs = root.database.observation_logs
        self.const_abbrs = root.database.const_abbrs
        self.moon = root.database.moon
        self.save_action = self.step_main_form.save_action
        self.exit_action = self.step_main_form.quit_action
        self.addAction(self.save_action)
        self.addAction(self.exit_action)
        self.const_combobox.addItems(self.const_abbrs)
        self.p_s_combobox.addItems(["", "P", "S"])
        self.pair_combobox.addItems(["", "A", "B", "C", "D", "E", "F"])
        self.processed_combobox.addItems(["No", "Yes"])
        self.photometric_filter_combobox.addItems(self.filters_list)
        self.select_by_processed_combobox.addItems(["All", "No", "Yes"])
        self.sunset_date_date_edit.setDate(self.selected_date)
        self.fill_form()
        self.fill_table()
        self.choice_place_combobox.currentTextChanged.connect(self.place_was_changed)
        self.choice_star_combobox.currentTextChanged.connect(self.star_was_changed)
        self.choice_instrument_combobox.currentTextChanged.connect(self.instrument_was_changed)
        self.new_log_radiobutton.clicked.connect(self.new_or_edit_radio_box_was_clicked)
        self.edit_log_radiobutton.clicked.connect(self.new_or_edit_radio_box_was_clicked)
        self.save_button.clicked.connect(self.save_log)
        self.sunset_date_date_edit.dateChanged.connect(self.moon_phase)
        self.time_time_edit.timeChanged.connect(self.time_was_changed)
        self.name_lineedit.textChanged.connect(self.star_on_lineedit_was_change)
        self.log_table_widget.itemSelectionChanged.connect(self.log_in_table_was_changed)
        self.delete_button.clicked.connect(self.delete_log)
        self.place_latitude_lineedit.textChanged.connect(self.latitude_was_changed)
        self.place_longitude_lineedit.textChanged.connect(self.longitude_was_changed)
        self.find_variable_lineedit.textChanged.connect(self.select_log)
        self.find_date_start_date_edit.dateChanged.connect(self.select_log)
        self.find_date_end_date_edit.dateChanged.connect(self.select_log)
        self.star_type_lineedit.textChanged.connect(self.select_log)
        self.find_full_text_lineedit.textChanged.connect(self.select_log)
        self.select_by_processed_combobox.currentTextChanged.connect(self.select_log)
        self.by_prediction_checkbox.clicked.connect(self.by_prediction_was_checked)

    def by_prediction_was_checked(self):
        if self.by_prediction_checkbox.isChecked():
            if self.step_main_form.objects_table.currentRow() > -1:
                row = self.step_main_form.objects_table.currentRow()
                self.find_variable_lineedit.setText(self.step_main_form.filtered_stars.stars[row].name())
        else:
            self.find_variable_lineedit.setText("")


    def fill_table(self):
        self.log_table_widget.clear()
        self.log_table_widget.setColumnCount(len(self.observation_logs.log_keys()))
        self.log_table_widget.setHorizontalHeaderLabels(self.observation_logs.log_keys())
        self.log_table_widget.setRowCount(len(self.observation_logs.logs()))
        # 0-user, 1-sunset_date, 2-name, 3-pair, 4-p_s, 5-star_type, 6-const, 7-telescope, 8-mount, 9-camera,
        # 10-photometric_filter, 11-binning, 12-exposure, 13-processed, 14-observation_place, 15-place_latitude,
        # 16-place_longitude, 17-moon_distance, 18-moon, 19-h_at_min, 20-weather, 21-note1, 22-note2, 23-note3,
        # 24-note4, 25-note5

        self.log_table_widget.hideColumn(0)
        self.log_table_widget.hideColumn(15)
        self.log_table_widget.hideColumn(16)
        self.log_table_widget.hideColumn(17)
        self.log_table_widget.hideColumn(18)
        self.log_table_widget.hideColumn(19)
        self.log_table_widget.hideColumn(22)
        self.log_table_widget.hideColumn(23)
        self.log_table_widget.hideColumn(24)
        self.log_table_widget.hideColumn(25)
        for i, obs_log in enumerate(self.observation_logs.logs()):
            log_list = obs_log.to_text().split(";")
            log_list[1] = log_list[1][0:log_list[1].find(" ")]
            for j, log_item in enumerate(log_list):
                item = QtWidgets.QTableWidgetItem(log_item)
                item.setFlags(QtCore.Qt.ItemIsEnabled)
                if j < 2:
                    item.setFlags(QtCore.Qt.ItemIsSelectable)
                self.log_table_widget.setItem(i, j, item)
        self.log_table_widget.resizeColumnsToContents()

    def fill_object_and_type_list(self):
        object_list = []
        object_type_list = []
        self.choice_star_combobox.clear()
        self.star_type_combobox.clear()
        for star in self.stars.stars:
            if star.variability():
                if star.name() not in object_list:
                    object_list.append(star.name())
                if star.type() not in object_type_list:
                    object_type_list.append(star.type())
        for observation in self.observation_logs.logs():
            if observation.name() not in object_list:
                object_list.append(observation.name())
            if observation.star_type() not in object_type_list:
                object_type_list.append(observation.star_type())
        self.object_list = sorted(object_list)
        self.object_type_list = sorted(object_type_list)
        self.choice_star_combobox.addItems(self.object_list)
        self.star_type_combobox.addItems(self.object_type_list)

    def fill_form(self):
        self.fill_object_and_type_list()
        for obs_place in self.places.observers():
            if obs_place[2] == self.user.name():
                self.place_list.append(obs_place[1])
                for instrument in self.instruments.instruments():
                    if instrument[1] == obs_place[0]:
                        self.instrument_list_id.append(instrument[0] + ": " + instrument[2] + " + "
                                                       + instrument[5] + " + " + instrument[6])
        self.choice_place_combobox.addItems(self.place_list)
        self.choice_instrument_combobox.addItems(sorted(self.instrument_list_id))

    def place_was_changed(self):
        for obs_place in self.places.observers():
            if obs_place[1] == self.choice_place_combobox.currentText():
                self.place_lineedit.setText(obs_place[1])
                self.place_latitude: float = float(obs_place[5])
                self.place_latitude_lineedit.setText(str(round(degrees(self.place_latitude), 6)))
                self.place_longitude: float = float(obs_place[6])
                self.place_longitude_lineedit.setText(str(round(degrees(self.place_longitude), 6)))

                return
            else:
                self.place_longitude = None
                self.place_latitude = None

    def star_was_changed(self):
        self.name_lineedit.disconnect()
        self.name_lineedit.setText(self.choice_star_combobox.currentText())
        self.name_lineedit.textChanged.connect(self.star_on_lineedit_was_change)
        self.star_type_combobox.setCurrentText("")
        self.const_combobox.setCurrentText("")
        self.star = None
        for star in self.stars.stars:
            if star.name() == self.choice_star_combobox.currentText():
                self.star = star
                self.h_at_min()
                self.moon_angular_distance()
                self.star_type_combobox.setCurrentText(star.type())
                self.const_combobox.setCurrentText(star.constellation())
                return

    def star_on_lineedit_was_change(self):
        self.star = None
        for star in self.stars.stars:
            if star.name() == self.name_lineedit.text():
                self.star = star
                self.h_at_min()
                self.moon_angular_distance()
                self.star_type_combobox.setCurrentText(star.type())
                self.const_combobox.setCurrentText(star.constellation())
                return
        if not self.star:
            self.moon_distance_lineedit.setText("")
            self.h_at_min_lineedit.setText("")
            self.star_type_combobox.setCurrentText("")
            self.const_combobox.setCurrentText("")

    def instrument_was_changed(self):
        instrument_text = self.choice_instrument_combobox.currentText()
        colon_position = instrument_text.find(":")
        instrument_id = instrument_text[0:colon_position]

        for instrument in self.instruments.instruments():
            if instrument[0] == instrument_id:
                self.telescope_lineedit.setText(instrument[2])
                self.mount_lineedit.setText(instrument[5])
                self.camera_lineedit.setText(instrument[6])
                return

    def new_or_edit_radio_box_was_clicked(self):
        if self.new_log_radiobutton.isChecked():
            self.instrument_was_changed()
            self.star_was_changed()
            self.place_was_changed()
            self.processed_combobox.setCurrentIndex(0)
            self.photometric_filter_combobox.setCurrentIndex(0)
            self.exposure_label.clear()
            self.note1_textedit.clear()
            self.note2_textedit.clear()
            self.weather_textedit.clear()
        else:
            self.delete_button.setEnabled(True)
            if self.log_table_widget.currentRow() > -1:
                index = self.log_table_widget.currentRow()
                log_datetime = self.observation_logs.logs()[index].sunset_date()
                log_date = log_datetime[0:log_datetime.find(" ")].split(".")
                log_time = log_datetime[log_datetime.find(" ")+1: len(log_datetime)].split(":")
                self.sunset_date_date_edit.setDate(QDate(int(log_date[2]), int(log_date[1]), int(log_date[0])))
                self.time_time_edit.setTime(QTime(int(log_time[0]), int(log_time[1]), 0))
                self.name_lineedit.setText(self.observation_logs.logs()[index].name())
                self.pair_combobox.setCurrentText(self.observation_logs.logs()[index].pair())
                self.p_s_combobox.setCurrentText(self.observation_logs.logs()[index].p_s())
                self.star_type_combobox.setCurrentText(self.observation_logs.logs()[index].star_type())
                self.const_combobox.setCurrentText(self.observation_logs.logs()[index].const())
                self.place_lineedit.setText(self.observation_logs.logs()[index].place())
                self.place_latitude_lineedit.setText(self.observation_logs.logs()[index].place_latitude())
                self.place_longitude_lineedit.setText(self.observation_logs.logs()[index].place_longitude())
                self.moon_distance_lineedit.setText(self.observation_logs.logs()[index].moon_distance())
                self.moon_lineedit.setText(self.observation_logs.logs()[index].moon())
                self.h_at_min_lineedit.setText(self.observation_logs.logs()[index].h_at_min())
                self.telescope_lineedit.setText(self.observation_logs.logs()[index].telescope())
                self.mount_lineedit.setText(self.observation_logs.logs()[index].mount())
                self.camera_lineedit.setText(self.observation_logs.logs()[index].camera())
                self.binning_combobox.setCurrentText(self.observation_logs.logs()[index].binning())
                self.exposure_label.setText(self.observation_logs.logs()[index].exposure())
                self.photometric_filter_combobox.\
                    setCurrentText(self.observation_logs.logs()[index].photometric_filter())
                self.processed_combobox.setCurrentText(self.observation_logs.logs()[index].processed())
                self.weather_textedit.setText(self.observation_logs.logs()[index].weather())
                self.note1_textedit.setText(self.observation_logs.logs()[index].note1())
                self.note2_textedit.setText(self.observation_logs.logs()[index].note2())
            else:
                self.new_log_radiobutton.setChecked(True)

    def sunset_time_to_datetime(self):
        date_info = self.sunset_date_date_edit.date()
        year_info = date_info.year()
        month_info = date_info.month()
        day_info = date_info.day()
        time_info = self.time_time_edit.time()
        hour_info = time_info.hour()
        minute_info = time_info.minute()
        return datetime(year_info, month_info, day_info, hour_info, minute_info, tzinfo=timezone.utc)

    def save_log(self):
        user = self.user.name()
        sunset_date = self.sunset_time_to_datetime().strftime("%d.%m.%Y %H:%M")
        name = self.name_lineedit.text()
        pair = self.pair_combobox.currentText()
        p_s = self.p_s_combobox.currentText()
        star_type = self.star_type_combobox.currentText()
        const = self.const_combobox.currentText()
        telescope = self.telescope_lineedit.text()
        mount = self.mount_lineedit.text()
        camera = self.camera_lineedit.text()
        photometric_filter = self.photometric_filter_combobox.currentText()
        observation_place = self.place_lineedit.text()
        binning = self.binning_combobox.currentText()
        exposure = self.exposure_label.text()
        place_latitude = self.place_latitude_lineedit.text()
        place_longitude = self.place_longitude_lineedit.text()
        weather = self.weather_textedit.toPlainText()
        moon_distance = self.moon_distance_lineedit.text()
        moon = self.moon_lineedit.text()
        h_at_min = self.h_at_min_lineedit.text()
        processed = self.processed_combobox.currentText()
        note1 = self.note1_textedit.toPlainText().replace(";", ", ").replace("\n", " ")
        note2 = self.note2_textedit.toPlainText().replace(";", ", ").replace("\n", " ")
        note3 = ""
        note4 = ""
        note5 = ""
        observation_log = ObservationLog(user, sunset_date, name, pair, p_s, star_type, const, telescope, mount, camera,
                                         photometric_filter, binning, exposure, processed, observation_place,
                                         place_latitude, place_longitude, moon_distance, moon, h_at_min, weather, note1,
                                         note2, note3, note4, note5)
        if self.new_log_radiobutton.isChecked():
            the_same_observation_exist = False
            for observation in self.observation_logs.logs():
                if observation.compare_observation(observation_log):
                    the_same_observation_exist = True
            if the_same_observation_exist:
                from step_main_form import Popup
                save_window = Popup("Already exist",
                                    "The same observation already exist. Do you want to save the observation anyway?",
                                    buttons="Save,Cancel".split(","))
                if save_window.do() == 0:
                    self.observation_logs.add_log(observation_log)
                else:
                    return
            else:
                self.observation_logs.add_log(observation_log)
        else:
            if self.log_table_widget.currentRow() > -1:
                self.observation_logs.edit_log(observation_log, self.log_table_widget.currentRow())
        self.fill_table()
        if name not in self.object_list:
            self.object_list.append(name)
            self.object_list = sorted(self.object_list)
            self.choice_star_combobox.clear()
            self.choice_star_combobox.addItems(self.object_list)
            self.choice_star_combobox.setCurrentText(name)
        if star_type not in self.object_type_list:
            self.object_type_list.append(star_type)
            self.object_type_list = sorted(self.object_type_list)
            self.star_type_combobox.clear()
            self.star_type_combobox.addItems(self.object_type_list)
            self.star_type_combobox.setCurrentText(star_type)
        self.select_log()

    def info_window(self, i):
        print("Clicked:", i.text())


    def moon_phase(self):
        jd = date_to_jd(self.sunset_time_to_datetime())
        phase = self.moon.moon_phase(jd) * 180 / pi
        phase_proc = int((180 - fabs(180 - phase)) / 1.8)
        self.moon_lineedit.setText(str(int(phase_proc)) + "%")

    def h_at_min(self):
        jd = date_to_jd(self.sunset_time_to_datetime())
        if self.star and self.place_latitude and self.place_longitude:
            h_at_min = int(self.star.horizon_coordinates_h(jd, self.place_longitude, self.place_latitude) * 180 / pi)
            self.h_at_min_lineedit.setText(str(h_at_min))
        else:
            self.h_at_min_lineedit.setText("")

    def time_was_changed(self):
        self.moon_phase()
        self.h_at_min()
        self.moon_angular_distance()

    def latitude_was_changed(self):
        try:
            if -90 < float(self.place_latitude_lineedit.text()) < 90:
                self.place_latitude = radians(float(self.place_latitude_lineedit.text()))
            else:
                self.place_latitude = None
        except:
            self.place_latitude = None
        if self.place_latitude and self.place_longitude and self.star:
            self.time_was_changed()
        else:
            self.moon_distance_lineedit.setText("")
            self.h_at_min_lineedit.setText("")

    def longitude_was_changed(self):
        try:
            if -180 < float(self.place_longitude_lineedit.text()) < 180:
                self.place_longitude = radians(float(self.place_longitude_lineedit.text()))
            else:
                self.place_longitude = None
        except:
            self.place_longitude = None
        if self.place_latitude and self.place_longitude and self.star:
            self.time_was_changed()
        else:
            self.moon_distance_lineedit.setText("")
            self.h_at_min_lineedit.setText("")

    def log_in_table_was_changed(self):
        if self.edit_log_radiobutton.isChecked():
            self.new_or_edit_radio_box_was_clicked()

    def moon_angular_distance(self):
        jd = date_to_jd(self.sunset_time_to_datetime())
        moon_coor = self.moon.coordinates(jd)
        moon_rec = moon_coor[0]
        moon_dec = moon_coor[1]
        if self.place_longitude and self.place_longitude and self.star:
            moon_h = self.moon.h(jd, self.place_latitude, self.place_longitude)
            if moon_h > 0:
                distance_num = angular_separation(self.star.coordinate().rektascenze(),
                                                  self.star.coordinate().deklinace(),
                                                  moon_rec, moon_dec)
                distance = str(round(degrees(distance_num), 2))
            else:
                distance = "under horizon"
            self.moon_distance_lineedit.setText(distance)
        else:
            self.moon_distance_lineedit.setText("")

    def delete_log(self):
        if self.log_table_widget.currentRow() > -1 and self.edit_log_radiobutton.isChecked():
            self.observation_logs.delete_log(self.log_table_widget.currentRow())
        self.log_table_widget.disconnect()
        self.sunset_date_date_edit.setDate(self.selected_date)
        self.time_time_edit.setTime(QTime(23, 59, 0))
        self.name_lineedit.clear()
        self.pair_combobox.setCurrentText("")
        self.p_s_combobox.setCurrentText("")
        self.star_type_combobox.setCurrentText("")
        self.const_combobox.setCurrentText("")
        self.place_lineedit.clear()
        self.place_latitude_lineedit.clear()
        self.place_longitude_lineedit.clear()
        self.star = None
        self.place_latitude = None
        self.place_longitude = None
        self.moon_distance_lineedit.clear()
        self.moon_lineedit.clear()
        self.h_at_min_lineedit.clear()
        self.telescope_lineedit.clear()
        self.mount_lineedit.clear()
        self.camera_lineedit.clear()
        self.binning_combobox.setCurrentIndex(0)
        self.exposure_label.clear()
        self.photometric_filter_combobox.setCurrentIndex(0)
        self.processed_combobox.setCurrentIndex(0)
        self.weather_textedit.clear()
        self.note1_textedit.clear()
        self.note2_textedit.clear()
        self.fill_object_and_type_list()
        self.fill_table()
        self.log_table_widget.itemSelectionChanged.connect(self.log_in_table_was_changed)

    def select_log(self):
        for i, obs_log in enumerate(self.observation_logs.logs()):
            name_visibility = False
            time_visibility = False
            full_text_visibility = False
            type_visibility = False
            process_visibility = False
            filter_visibility = False
            if self.find_variable_lineedit.text() == "" or (self.find_variable_lineedit.text() != ""
                                                            and self.find_variable_lineedit.text() in obs_log.name()):
                name_visibility = True
            obs_date = datetime.strptime(obs_log.sunset_date(), "%d.%m.%Y %H:%M")
            if self.find_date_start_date_edit.date() >= self.find_date_end_date_edit.date() \
                    or self.find_date_start_date_edit.date() <= obs_date <= self.find_date_end_date_edit.date():
                time_visibility = True
            if self.star_type_lineedit.text() == "" or (self.star_type_lineedit.text() != ""
                                                        and self.star_type_lineedit.text() in obs_log.star_type()):
                type_visibility = True
            if self.select_by_processed_combobox.currentIndex() == 0 \
                    or (self.select_by_processed_combobox.currentIndex() > 0
                        and self.select_by_processed_combobox.currentText() == obs_log.processed()):
                process_visibility = True
            if self.find_full_text_lineedit.text() == "":
                full_text_visibility = True
            else:
                full_text = self.find_full_text_lineedit.text()
                if full_text in obs_log.telescope() or full_text in obs_log.mount() or full_text in obs_log.camera():
                    full_text_visibility = True
                elif full_text in obs_log.place() or full_text in obs_log.weather():
                    full_text_visibility = True
                elif full_text in obs_log.note1() or full_text in obs_log.note2():
                    full_text_visibility = True
                else:
                    pass
            if self.find_by_filter_combobox.currentIndex() == 0:
                filter_visibility = True
            else:
                if self.find_by_filter_combobox.currentText() == obs_log.photometric_filter():
                    filter_visibility = True

            if name_visibility and time_visibility and type_visibility and \
                    process_visibility and full_text_visibility and filter_visibility:
                self.log_table_widget.showRow(i)
            else:
                self.log_table_widget.hideRow(i)
        self.log_table_widget.resizeColumnsToContents()


class ObservationLogs:

    def __init__(self, logs: list, log_keys):
        self.__logs = logs
        self.__log_keys = log_keys

    def add_log(self, observation_log):
        self.__logs.append(observation_log)
        self.__logs = sorted(self.__logs, key=lambda x: datetime.strptime(x.sunset_date(), "%d.%m.%Y %H:%M"),
                             reverse=True)
    def add_logs(self, observation_logs):
        self.__logs = self.__logs + observation_logs
        self.__logs = sorted(self.__logs, key=lambda x: datetime.strptime(x.sunset_date(), "%d.%m.%Y %H:%M"),
                             reverse=True)

    def edit_log(self, observation_log, position):
        self.__logs[position] = observation_log
        self.__logs = sorted(self.__logs, key=lambda x: datetime.strptime(x.sunset_date(), "%d.%m.%Y %H:%M"),
                             reverse=True)

    def delete_log(self, index):
        del(self.__logs[index])

    def total_number(self):
        return len(self.__logs)

    def give_observation(self, index):
        return self.__logs[index]

    def log_keys(self):
        return self.__log_keys

    def logs(self):
        return self.__logs

    def change_user(self, new_user, last_user):
        for obs_log in self.__logs:
            if obs_log.user() == last_user:
                obs_log.change_user(new_user)


class ObservationLog:

    def __init__(self, user, sunset_date, name, pair, p_s, star_type, const, telescope, mount, camera,
                 photometric_filter, binning, exposure, processed, observation_place, place_latitude, place_longitude,
                 moon_distance, moon, h_at_min, weather, note1, note2, note3, note4, note5):
        self.__user = user
        self.__sunset_date = sunset_date
        self.__name = name
        self.__pair = pair
        self.__p_s = p_s
        self.__star_type = star_type
        self.__const = const
        self.__telescope = telescope
        self.__mount = mount
        self.__camera = camera
        self.__photometric_filter = photometric_filter
        self.__binning = binning
        self.__exposure = exposure
        self.__processed = processed
        self.__place = observation_place
        self.__place_latitude = place_latitude
        self.__place_longitude = place_longitude
        self.__moon_distance = moon_distance
        self.__moon = moon
        self.__h_at_min = h_at_min
        self.__weather = weather
        self.__note1 = note1
        self.__note2 = note2
        self.__note3 = note3
        self.__note4 = note4
        self.__note5 = note5

    def user(self):
        return self.__user

    def change_user(self, new):
        self.__user = new

    def sunset_date(self):
        return self.__sunset_date

    def name(self):
        return self.__name

    def pair(self):
        return self.__pair

    def p_s(self):
        return self.__p_s

    def star_type(self):
        return self.__star_type

    def const(self):
        return self.__const

    def telescope(self):
        return self.__telescope

    def mount(self):
        return self.__mount

    def binning(self):
        return self.__binning

    def exposure(self):
        return self.__exposure

    def camera(self):
        return self.__camera

    def photometric_filter(self):
        return self.__photometric_filter

    def place(self):
        return self.__place

    def place_latitude(self):
        return self.__place_latitude

    def place_longitude(self):
        return self.__place_longitude

    def weather(self):
        return self.__weather

    def moon_distance(self):
        return self.__moon_distance

    def moon(self):
        return self.__moon

    def h_at_min(self):
        return self.__h_at_min

    def processed(self):
        return self.__processed

    def note1(self):
        return self.__note1

    def note2(self):
        return self.__note2

    def note3(self):
        return self.__note3

    def note4(self):
        return self.__note4

    def note5(self):
        return self.__note5

    def change_sunset_date(self, new):
        self.__sunset_date = new

    def change_name(self, new):
        self.__name = new

    def change_pair(self, new):
        self.__pair = new

    def change_p_s(self, new):
        self.__p_s = new

    def change_star_type(self, new):
        self.__star_type = new

    def change_const(self, new):
        self.__const = new

    def change_telescope(self, new):
        self.__telescope = new

    def change_mount(self, new):
        self.__mount = new

    def change_camera(self, new):
        self.__camera = new

    def change_photometric_filter(self, new):
        self.__photometric_filter = new

    def change_place(self, new):
        self.__place = new

    def change_place_latitude(self, new):
        self.__place_latitude = new

    def change_place_longitude(self, new):
        self.__place_longitude = new

    def change_weather(self, new):
        self.__weather = new

    def change_moon_distance(self, new):
        self.__moon_distance = new

    def change_moon(self, new):
        self.__moon = new

    def change_h_at_min(self, new):
        self.__h_at_min = new

    def change_processed(self, new):
        self.__processed = new

    def change_note1(self, new):
        self.__note1 = new.replace(";", ", ").replace("\n", " ")

    def change_note2(self, new):
        self.__note2 = new.replace(";", ", ").replace("\n", " ")

    def change_note3(self, new):
        self.__note3 = new.replace(";", ", ").replace("\n", " ")

    def change_note4(self, new):
        self.__note4 = new.replace(";", ", ").replace("\n", " ")

    def change_note5(self, new):
        self.__note5 = new.replace(";", ", ").replace("\n", " ")

    def compare_observation(self, other_observation):
        if self.__sunset_date == other_observation.sunset_date():
            if self.__name == other_observation.name():
                if self.__telescope == other_observation.telescope():
                    if self.__photometric_filter == other_observation.photometric_filter():
                        if self.__pair == other_observation.pair():
                            if self.__p_s == other_observation.p_s():
                                if self.__mount == other_observation.mount():
                                    if self.__camera == other_observation.camera():
                                        if self.__binning == other_observation.binning():
                                            if self.__exposure == other_observation.exposure():
                                                if self.__place == other_observation.place():
                                                    if self.__user == other_observation.user():
                                                        return True
        return False

    def to_text(self):
        text_note = str(self.__user) + ";" + \
                    str(self.__sunset_date) + ";" + \
                    str(self.__name) + ";" + \
                    str(self.__pair) + ";" + \
                    str(self.__p_s) + ";" + \
                    str(self.__star_type) + ";" + \
                    str(self.__const) + ";" + \
                    str(self.__telescope) + ";" + \
                    str(self.__mount) + ";" + \
                    str(self.__camera) + ";" + \
                    str(self.__photometric_filter) + ";" + \
                    str(self.__binning) + ";" + \
                    str(self.__exposure) + ";" +\
                    str(self.__processed) + ";" + \
                    str(self.__place) + ";" + \
                    str(self.__place_latitude) + ";" + \
                    str(self.__place_longitude) + ";" + \
                    str(self.__moon_distance) + ";" + \
                    str(self.__moon) + ";" + \
                    str(self.__h_at_min) + ";" + \
                    str(self.__weather) + ";" + \
                    str(self.__note1).replace(";", ", ").replace("\n", " ") + ";" + \
                    str(self.__note2).replace(";", ", ").replace("\n", " ") + ";" + \
                    str(self.__note3).replace(";", ", ").replace("\n", " ") + ";" + \
                    str(self.__note4).replace(";", ", ").replace("\n", " ") + ";" + \
                    str(self.__note5).replace(";", ", ").replace("\n", " ")
        return text_note
