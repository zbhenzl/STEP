from database import *
from PyQt5 import QtWidgets
from astropy.coordinates import angular_separation



class PredictionTwo(QtWidgets.QWidget):

    def __init__(self, *args, **kwargs):
        super(PredictionTwo, self).__init__(*args, **kwargs)

        self.a_now = 0
        self.h_now = 0
        self.a_minimum = 0
        self.h_minimum = 0
        self.a_moon_minimum = 0
        self.h_moon_minimum = 0
        self.x_size_horizon = 1080
        self.y_size_horizon = 360
        self.dec_spinbox = 45
        self.meridian = 0
        self.faze = ""
        self.moon_phase = "Moon"
        self.year_sunset_sunrise_table = []
        self.horizon_visibility_table = []
        self.point_list = [[], [], [], []]
        self.__current_info = [0, 0, "00 00 0000", "00:00"]
        self.setWindowTitle("Predictions and lightcurves for the ordered time period")
        self.setWindowIcon(QtGui.QIcon("chart-up.png"))
        self.setMouseTracking(True)
        self.setContentsMargins(0, 360, 0, 0)
        self.setMinimumWidth(1445)
        self.setMinimumHeight(600)
        self.visibility_graph_column = 365 # MinimumWeight - self.x_size_horizon
        self.day_lightcurve_data_set_point = [0] * self.visibility_graph_column
        self.current_sunrise_jd = None
        self.current_sunset_jd = None
        self.star_time_sunrise = None
        self.star_time_sunset = None
        self.prediction_table = []
        self.star_system = []
        self.selected_star = None
        self.north_latitude = True
        self.prediction_key = ["ID", "Name", "Pair", "P/S", "Alt.name", "Const.", "Type", "RA", "DE", "Mag.",
                               "UCAC4 No.", "USNO B1.0 No.", "Meridian", "Starrise", "Starset", "D entry", "D output",
                               "d entry", "d output", "Minimum JD", "Minimum UTC", "h at min.", "Moon distance",
                               "Amplitude", "sec. phase", "Epoch 0", "Period", "Note1", "Note2", "Note3", "model_mag0",
                               "a_pri", "d_pri", "g_pri", "c_pri", "sin1", "sin2", "sin3", "coef.apsid", "sec_phase",
                               "a_sec", "d_sec", "g_sec", "c_sec", "cos1", "cos2", "cos3", "lc_offset"]
        self.sort_by_list = ["Minimum (JD)", "Name", "Alt.name", "Rektascenze", "Declination", "Constellation + Name",
                             "Type+Name", "Magnitude", "Starrise", "Starset", "D-entry", "D-output", "Star h",
                             "Moon(dist)", "Amplitude", "Period"]
        self.columns_setup = ["1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1",
                              "1", "1", "1", "1", "1", "1"]

        # widgets and layouts
        self.visibility_sun_checkbox = QtWidgets.QCheckBox("Sun")
        self.visibility_horizon_checkbox = QtWidgets.QCheckBox("Horizon")
        self.visibility_moon_checkbox = QtWidgets.QCheckBox("Moon")
        self.visibility_year_checkbox = QtWidgets.QRadioButton("Year")
        self.visibility_night_checkbox = QtWidgets.QRadioButton("Night")
        self.visibility_night_checkbox.setChecked(True)

        self.predictions_layout = QtWidgets.QVBoxLayout()
        self.setLayout(self.predictions_layout)
        self.build()

    def build(self):
        visibility_groupbox = QtWidgets.QGroupBox("Visibility in relation to")
        visibility_layout = QtWidgets.QHBoxLayout()
        visibility_groupbox.setLayout(visibility_layout)
        visibility_layout.addWidget(self.visibility_sun_checkbox)
        visibility_layout.addWidget(self.visibility_horizon_checkbox)
        visibility_layout.addWidget(self.visibility_moon_checkbox)

        column_groupbox = QtWidgets.QGroupBox("Select columns")
        column_layout = QtWidgets.QGridLayout()
        column_groupbox.setLayout(column_layout)

        sort_groupbox = QtWidgets.QGroupBox("Sort by")
        #sort_groupbox.setMinimumWidth(50)
        sort_layout = QtWidgets.QHBoxLayout()
        sort_groupbox.setLayout(sort_layout)
        sort_by_label = QtWidgets.QLabel("Sort by:")
        self.sort_by_combobox = QtWidgets.QComboBox()
        self.sort_by_combobox.addItems(self.sort_by_list)

        self.select_column_combobox = QtWidgets.QComboBox()
        self.select_column_combobox.addItems(["Id", "Name", "Pair", "Prim/sec", "Alt.name", "Const.", "Type", "RA/DE",
                                              "Mag", "Cross Id.", "Merid.time", "Rise/Set", "D info", "d info",
                                              "min.JD", "min.UTC", "Star h", "Moon dist.", "Amp.P/S", "Sec.min",
                                              "Epoch", "Period", "Notes", "Model"])
        self.select_column_button = QtWidgets.QPushButton("")

        column_layout.addWidget(self.select_column_combobox, 0, 0)
        column_layout.addWidget(self.select_column_button, 0, 1)


        sort_layout.addWidget(sort_by_label)
        sort_layout.addWidget(self.sort_by_combobox)

        prediction_table_groupbox = QtWidgets.QGroupBox("Prediction Table")
        prediction_table_layout = QtWidgets.QHBoxLayout()
        prediction_table_groupbox.setLayout(prediction_table_layout)

        self.prediction_table_widget = QtWidgets.QTableWidget()
        prediction_table_layout.addWidget(self.prediction_table_widget)

        hide_groupbox = QtWidgets.QGroupBox("Hide / Show Selected Item")
        hide_layout = QtWidgets.QHBoxLayout()
        hide_groupbox.setLayout(hide_layout)

        self.hide_item_checkbox = QtWidgets.QCheckBox("Item visibility")
        self.hide_item_checkbox.setChecked(False)
        self.show_all_checkbox = QtWidgets.QCheckBox("Show All / Hide")
        self.show_all_checkbox.setChecked(True)

        hide_layout.addWidget(self.hide_item_checkbox)
        hide_layout.addWidget(self.show_all_checkbox)

        observed_groupbox = QtWidgets.QGroupBox("Observation log")
        observed_layout = QtWidgets.QHBoxLayout()
        observed_groupbox.setLayout(observed_layout)

        self.add_to_log_button = QtWidgets.QPushButton("Add")
        self.show_observation_log_button = QtWidgets.QPushButton("Show")

        observed_layout.addWidget(self.add_to_log_button)
        observed_layout.addWidget(self.show_observation_log_button)

        note_groupbox = QtWidgets.QGroupBox("Notes")
        note_layout = QtWidgets.QVBoxLayout()
        note_groupbox.setLayout(note_layout)

        self.save_notes_pushbutton = QtWidgets.QPushButton("Save Notes")

        self.note1 = QtWidgets.QTextEdit()
        self.note2 = QtWidgets.QTextEdit()
        self.note3 = QtWidgets.QTextEdit()
        note_layout.addWidget(self.save_notes_pushbutton)
        note_layout.addWidget(self.note1)
        note_layout.addWidget(self.note2)
        note_layout.addWidget(self.note3)

        graph_groupbox = QtWidgets.QGroupBox("Show graph")
        graph_layout = QtWidgets.QHBoxLayout()
        graph_groupbox.setLayout(graph_layout)

        visibility_day_groupbox = QtWidgets.QGroupBox("Visibility year/night")
        visibility_day_layout = QtWidgets.QHBoxLayout()
        visibility_day_groupbox.setLayout(visibility_day_layout)
        visibility_day_layout.addWidget(self.visibility_year_checkbox)
        visibility_day_layout.addWidget(self.visibility_night_checkbox)

        moon_setup_groupbox = QtWidgets.QGroupBox("Moon setup")
        moon_setup_layout = QtWidgets.QHBoxLayout()
        moon_setup_groupbox.setLayout(moon_setup_layout)
        self.moon_distance_spinbox = QtWidgets.QSpinBox()
        self.moon_distance_spinbox.setValue(0)
        self.moon_phase_spinbox = QtWidgets.QSpinBox()
        self.moon_phase_spinbox.setValue(99)
        moon_setup_layout.addWidget(QtWidgets.QLabel("Distance(°)"))
        moon_setup_layout.addWidget(self.moon_distance_spinbox)
        moon_setup_layout.addWidget(QtWidgets.QLabel("and Phase(%)"))
        moon_setup_layout.addWidget(self.moon_phase_spinbox)


        self.graph_lightcurve_button = QtWidgets.QCheckBox("LightCurve")

        graph_layout.addWidget(self.graph_lightcurve_button)

        self.minimum_window_layout = QtWidgets.QGridLayout()
        self.minimum_window_layout.addWidget(column_groupbox, 0, 0, 2, 2)
        self.minimum_window_layout.addWidget(sort_groupbox, 0, 2, 2, 2)
        self.minimum_window_layout.addWidget(visibility_groupbox, 0, 4, 2, 3)
        self.minimum_window_layout.addWidget(moon_setup_groupbox, 0, 7, 2, 2)
        self.minimum_window_layout.addWidget(visibility_day_groupbox, 0, 9, 2, 2)
        self.minimum_window_layout.addWidget(hide_groupbox, 0, 11, 2, 2)
        self.minimum_window_layout.addWidget(graph_groupbox, 0, 13, 2, 1)
        self.minimum_window_layout.addWidget(observed_groupbox, 0, 14, 2, 2)
        self.minimum_window_layout.addWidget(prediction_table_groupbox, 2, 0, 7, 13)
        self.minimum_window_layout.addWidget(note_groupbox, 2, 13, 7, 3)


        self.predictions_layout.addLayout(self.minimum_window_layout)

    def setup(self):
        from step_application import root
        self.database = root.database
        self.important_predictions = self.database.important_predictions
        self.place = self.database.place
        self.instrument = self.database.instrument
        self.horizon = self.database.horizon
        self.azimuth = self.horizon.azimuth()
        self.h_altitude = self.horizon.h_altitude()
        self.step_main_form = root.step_main_form
        self.time_period = root.database.time_period
        self.filtered_star = root.step_main_form.filtered_stars
        self.sun = root.database.sun
        self.moon = root.database.moon
        self.variables = root.database.variables
        self.lightcurve_window = root.lightcurve_window
        self.user = root.database.user
        self.observation_logs = root.database.observation_logs
        self.observation_log_window = root.observation_log_window
        self.save_action = self.step_main_form.save_action
        self.photometry_action = self.step_main_form.photometry_action
        self.star_edit_action = self.step_main_form.star_edit_action
        self.show_observation_action = self.step_main_form.observation_action
        self.show_lightcurve_action = self.step_main_form.lightcurve_action

        self.item_visibility_action = QtWidgets.QAction("Set Item Visibility", self)
        self.item_visibility_action.triggered.connect((self.hide_button_is_checked_by_shortcut))
        self.item_visibility_action.setShortcut(QtGui.QKeySequence(QtCore.Qt.ALT + QtCore.Qt.Key_V))

        self.addAction(self.item_visibility_action)
        self.addAction(self.save_action)
        self.addAction(self.photometry_action)
        self.addAction(self.star_edit_action)
        self.addAction(self.show_observation_action)
        self.addAction(self.show_lightcurve_action)
        self.columns_setup = self.user.prediction_select_column_setup()
        self.fill_form()
        self.visibility_sun_checkbox.clicked.connect(self.fill_prediction)
        self.visibility_moon_checkbox.clicked.connect(self.fill_prediction)
        self.visibility_horizon_checkbox.clicked.connect(self.fill_prediction)
        self.sort_by_combobox.currentTextChanged.connect(self.sort_prediction_table)
        self.prediction_table_widget.itemSelectionChanged.connect(self.table_item_changed)
        self.fill_prediction()
        self.graph_lightcurve_button.clicked.connect(self.show_lightcurve)
        self.save_notes_pushbutton.clicked.connect(self.save_notes)
        self.hide_item_checkbox.clicked.connect(self.hide_button_is_checked)
        self.show_all_checkbox.clicked.connect(self.hide_row_and_column)
        self.show_observation_log_button.clicked.connect(self.show_observations)
        self.add_to_log_button.clicked.connect(self.add_to_log)
        self.select_column_combobox.currentIndexChanged.connect(self.column_combobox_changed)
        self.select_column_combobox.setCurrentIndex(0)
        self.column_combobox_changed()
        self.select_column_button.clicked.connect(self.column_button_clicked)
        self.visibility_night_checkbox.clicked.connect(self.visibility_night_checkbox_was_changed)
        self.visibility_year_checkbox.clicked.connect(self.visibility_night_checkbox_was_changed)

    def visibility_night_checkbox_was_changed(self):
        self.paint_changed(0, 0)

    def column_button_clicked(self):
        column_combobox_index = self.select_column_combobox.currentIndex()
        # if column_combobox_index == 0:
        if self.columns_setup[column_combobox_index] == "1":
            self.columns_setup[column_combobox_index] = "0"
        else:
            self.columns_setup[column_combobox_index] = "1"

        if self.select_column_button.text() == "Show":
            self.select_column_button.setText("Hide")
        else:
            self.select_column_button.setText("Show")

        self.hide_column()


    def column_combobox_changed(self):
        column_combobox_index = self.select_column_combobox.currentIndex()
        if self.columns_setup[column_combobox_index] == "1":
            self.select_column_button.setText("Hide")
        else:
            self.select_column_button.setText("Show")


    def add_to_log(self):
        """
         "Name"1    "Pair"2    "Alt.name"4    "Const."5    "Type"6    "Rec."7    "Dec."8  "Mag."9 N    "Starrise"13
         "Starset"14    "D entry"15    "D output"16    "Minimum JD"19    "h at min."21    "Moon distance"22
         "Amplitude"23    "Epoch 0"25    "Period"26

         "Mag."9 N , "Starrise"13
         "Starset"14    "D entry"15    "D output"16    "Minimum JD"19    "h at min."21    "Moon distance"22
         "Amplitude"23    "Epoch 0"25    "Period"26
 like number and date :
         "Mag." -48, "Starrise"-49, "Starset"-50, "D entry"-51, "D output"-52, "Minimum JD"-53, "h at min.-54",
         "Moon distance"-55, "Amplitude"-56, "Period-57"
         """
        if self.prediction_table_widget.currentRow() > -1:
            self.observation_log_window.new_log_radiobutton.setChecked(True)
            row_index = self.prediction_table_widget.currentRow()
            self.observation_log_window.choice_star_combobox.setCurrentText(self.prediction_table[row_index][1])
            self.observation_log_window.choice_place_combobox.setCurrentText(self.place.name)
            instrument = str(self.instrument.id) + ": " \
                         + self.instrument.telescope() + " + " \
                         + self.instrument.mount() + " + " \
                         + self.instrument.camera()
            self.observation_log_window.choice_instrument_combobox.setCurrentText(instrument)
            minimum_date = jd_to_date(self.prediction_table[row_index][53])
            hour = minimum_date.hour
            minute = minimum_date.minute
            second = minimum_date.second
            self.observation_log_window.sunset_date_date_edit.setDate(minimum_date)
            self.observation_log_window.time_time_edit.setTime(QTime(hour, minute, second))
            self.observation_log_window.name_lineedit.setText(self.prediction_table[row_index][1])
            self.observation_log_window.pair_combobox.setCurrentText(self.prediction_table[row_index][2])
            self.observation_log_window.p_s_combobox.setCurrentText(self.prediction_table[row_index][3])
            self.observation_log_window.star_type_combobox.setCurrentText(self.prediction_table[row_index][6])
            self.observation_log_window.const_combobox.setCurrentText(self.prediction_table[row_index][5])
            self.observation_log_window.photometric_filter_combobox.setCurrentIndex(0)
            self.observation_log_window.binning_combobox.setCurrentIndex(0)
            self.observation_log_window.exposure_label.setText("")
            self.observation_log_window.processed_combobox.setCurrentIndex(0)
            if self.prediction_table[row_index][22]:
                self.observation_log_window.moon_distance_lineedit.setText(self.prediction_table[row_index][22])
            else:
                self.observation_log_window.moon_distance_lineedit.setText("under horizon")
            self.observation_log_window.h_at_min_lineedit.setText(self.prediction_table[row_index][21])
            self.observation_log_window.telescope_lineedit.setText(self.instrument.telescope())
            self.observation_log_window.mount_lineedit.setText(self.instrument.mount())
            self.observation_log_window.camera_lineedit.setText(self.instrument.camera())
            self.observation_log_window.place_lineedit.setText(self.place.name)
            self.observation_log_window.place_latitude_lineedit.setText(str(round(degrees(self.place.latitude), 6)))
            self.observation_log_window.place_longitude_lineedit.setText(str(round(degrees(self.place.longitude), 6)))
            self.observation_log_window.show()

    def show_observations(self):
        self.observation_log_window.show()

    def save_notes(self):
        if self.prediction_table_widget.currentRow() > -1:
            row = self.prediction_table_widget.currentRow()
            name = self.prediction_table[row][1]
            for prediction in self.prediction_table:
                if prediction[1] == name:
                    prediction[27] = self.note1.toPlainText().replace(";", ", ").replace("\n", " ")
                    prediction[28] = self.note2.toPlainText().replace(";", ", ").replace("\n", " ")
                    prediction[29] = self.note3.toPlainText().replace(";", ", ").replace("\n", " ")

            for star in self.database.stars.stars:
                if star.name() == name:
                    star.change_note1(self.note1.toPlainText().replace(";", ", ").replace("\n", " "))
                    star.change_note2(self.note2.toPlainText().replace(";", ", ").replace("\n", " "))
                    star.change_note3(self.note3.toPlainText().replace(";", ", ").replace("\n", " "))

    def change_meridian(self, new_meridian):
        self.meridian = new_meridian

    def change_current_info(self, new_info):
        self.__current_info = new_info

    def rise_set(self):
        self.change_meridian(self.sun.meridian(self.time_period.jd_start(), self.place.longitude))
        self.year_sunset_sunrise_table.clear()
        for i in range(365):
            sunset = self.sun.sunrise_h(self.place.min_sunset, self.meridian + i, self.place.longitude,
                                        self.place.latitude, is_sunrise=False)
            rise = self.sun.sunrise_h(self.place.min_sunset, self.meridian + i, self.place.longitude,
                                      self.place.latitude, is_sunrise=True)
            if sunset == "No sunset" or rise == "No sunset":
                self.year_sunset_sunrise_table.append([i, 0, i, self.y_size_horizon])
            elif sunset == "No sunrise" or rise == "No sunrise":
                pass
            else:
                y0 = int((sunset - self.meridian - i) * self.y_size_horizon)
                if y0 > 0:
                    self.year_sunset_sunrise_table.append([i, 0, i, y0])
                y0 = int((rise - self.meridian - i) * self.y_size_horizon)
                if y0 < self.y_size_horizon:
                    self.year_sunset_sunrise_table.append([i, y0, i, self.y_size_horizon])

    def horizon_set(self, star):
        self.horizon_visibility_table.clear()
        point_set = []
        self.change_meridian(self.sun.meridian(self.time_period.jd_start(), self.place.longitude))
        start = self.time_period.jd_start() - self.meridian
        end = self.meridian - self.time_period.jd_end() + 2
        horizon_day_set = self.time_period.interact_horizon(self.place, star, extend_time_start=start,
                                                            extend_time_end=end)
        visible = True

        while horizon_day_set:
            point = int((horizon_day_set.pop(0) - self.meridian)*self.y_size_horizon)
            point_set.append([point, visible])
            if visible:
                visible = False
            else:
                visible = True
        if point_set:
            if point_set[0][0] > 0:
                point_set.insert(0, [0, False])
            if point_set[-1][0] < 2 * self.y_size_horizon:
                point_set.append([2 * self.y_size_horizon, False])
        else:
            point_set = [[0, False], [2 * self.y_size_horizon, False]]
        for i in range(365):
            for j in range(len(point_set)-1):
                point0 = point_set[j]
                point1 = point_set[j+1]
                if point0[0] - i <= 0 < point1[0] - i < self.y_size_horizon + 1:
                    self.horizon_visibility_table.append([i, 0, i, point1[0]-i, point0[1]])
                elif 0 < point0[0] - i < point1[0] - i < self.y_size_horizon + 1:
                    self.horizon_visibility_table.append([i, point0[0] - i, i, point1[0] - i, point0[1]])
                elif 0 < point0[0] - i < self.y_size_horizon < point1[0] - i:
                    self.horizon_visibility_table.append([i, point0[0] - i, i, self.y_size_horizon, point0[1]])
                elif point0[0] - i <= 0 < self.y_size_horizon < point1[0] - i:
                    self.horizon_visibility_table.append([i, 0, i, self.y_size_horizon, point0[1]])
                else:
                    pass
        self.update()

    def closeEvent(self, event):
        try:
            self.lightcurve_window.close()
        except:
            pass
        try:
            self.step_main_form.object_show_detail_checkbox.setChecked(False)
        except:
            pass

    def paintEvent(self, event):
        x_scale = self.x_size_horizon / 360
        y_scale = self.y_size_horizon / 90
        q = 1
        p = QtGui.QPainter(self)
        self.azimuth = self.horizon.azimuth()
        self.h_altitude = self.horizon.h_altitude()

        # background
        for j in range(360):
            for i in range(90):
                if self.azimuth[q] == j:
                    q = q+1
                h0 = self.h_altitude[q]
                h1 = self.h_altitude[q-1]
                a0 = self.azimuth[q]
                a1 = self.azimuth[q-1]
                akt_h_altitude = (h1 - h0) / (a1 - a0) * (j - a1) + h1
                if akt_h_altitude < i:
                     colour_background = QtCore.Qt.cyan
                     size = 4
                else:
                    colour_background = QtCore.Qt.green
                    size = 4
                if self.north_latitude:
                    p.fillRect(int(j * x_scale), int((89 - i) * y_scale), size, size, QtGui.QBrush(colour_background))
                else:
                    if j < 180:
                        x_fill = int((j + 180) * x_scale)
                    else:
                        x_fill = int((j - 180) * x_scale)
                    p.fillRect(x_fill, int((89 - i) * y_scale), size, size, QtGui.QBrush(colour_background))

        # horizon line
        for i in range(len(self.azimuth)-1):
            y1_coor = int((89 - self.h_altitude[i]) * y_scale)
            y2_coor = int((89 - self.h_altitude[i + 1]) * y_scale)
            if self.north_latitude:
                x1_coor = int(self.azimuth[i] * x_scale)
                x2_coor = int(self.azimuth[i+1] * x_scale)
            else:
                if self.azimuth[i] < 180 and self.azimuth[i+1] < 180:
                    x1_coor = int((self.azimuth[i] + 180) * x_scale)
                    x2_coor = int((self.azimuth[i + 1] + 180) * x_scale)
                elif self.azimuth[i] >= 180 and self.azimuth[i+1] >= 180:
                    x1_coor = int((self.azimuth[i] - 180) * x_scale)
                    x2_coor = int((self.azimuth[i + 1] - 180) * x_scale)
                else:
                    x1_coor = int((self.azimuth[i] + 180) * x_scale)
                    y_center = int((180 - self.azimuth[i]) *
                                   (y2_coor - y1_coor) / (self.azimuth[i + 1] - self.azimuth[i])) + y1_coor
                    x2_coor = int(359 * x_scale)
                    if x1_coor == x2_coor and y1_coor == y_center:
                        pass
                    else:
                        p.drawLine(x1_coor, y1_coor, x2_coor, y_center)
                    x1_coor = 0
                    x2_coor = int((self.azimuth[i + 1] - 180) * x_scale)
                    y1_coor = y_center
            if x1_coor == x2_coor and y1_coor == y2_coor:
                pass
            else:
                p.drawLine(x1_coor, y1_coor, x2_coor, y2_coor)

        # minimum object latitude line and meridian line
        min_h = int((89 - self.step_main_form.h_spinbox.value()) * y_scale)
        if min_h > 60 * y_scale:
            min_h_text = int(min_h - 5 * y_scale)
        else:
            min_h_text = int(min_h + 5 * y_scale)
        p.drawStaticText(30, min_h_text, QtGui.QStaticText("Minimum object altitude"))
        if self.north_latitude:
            meridian_text = "Meridian line - South"
        else:
            meridian_text = "Meridian line - North"
        p.drawStaticText(int(180 * x_scale) + 10, 30, QtGui.QStaticText(meridian_text))
        if self.visibility_night_checkbox.isChecked():
            h_line = QtCore.QLine(0, min_h, self.x_size_horizon + 365, min_h)
        else:
            h_line = QtCore.QLine(0, min_h, self.x_size_horizon, min_h)
        meridian_line = QtCore.QLine(int(180 * x_scale), 0, int(180 * x_scale), int(89 * y_scale))
        l_line_pen = QtGui.QPen(QtCore.Qt.blue)
        l_line_pen.setWidth(1)
        p.setPen(l_line_pen)
        p.drawLine(h_line)
        p.drawLine(meridian_line)

        # day visibility backgroun
        if self.visibility_night_checkbox.isChecked():
            l_line_pen = QtGui.QPen(QtCore.Qt.yellow)
            l_line_pen.setWidth(1)
            p.setPen(l_line_pen)
            for j in range(0, 365):
                p.drawLine(j + self.x_size_horizon, int(90 * y_scale), j + self.x_size_horizon, min_h + 1)
            l_line_pen = QtGui.QPen(QtCore.Qt.lightGray)
            l_line_pen.setWidth(1)
            p.setPen(l_line_pen)
            for j in range(0, 365):
                p.drawLine(j + self.x_size_horizon, 0, j + self.x_size_horizon, min_h - 1)

        if self.prediction_table_widget.currentRow() > -1:
            # star arc
            l_line_pen = QtGui.QPen(QtCore.Qt.red)
            l_line_pen.setWidth(2)
            p.setPen(l_line_pen)
            if self.selected_star:
                for i in range(1, len(self.point_list[0])):
                    x1: int = int(self.point_list[0][i - 1] * x_scale)
                    y1: int = int((89 - self.point_list[1][i - 1]) * y_scale)
                    x2: int = int(self.point_list[0][i] * x_scale)
                    y2: int = int((89 - self.point_list[1][i]) * y_scale)
                    if x1 - x2 < -2 * self.y_size_horizon:
                        pass
                    elif x1 - x2 > 2 * self.y_size_horizon:
                        pass
                    else:
                        if x1 == x2 and y1 == y2:
                            pass
                        else:
                            if self.north_latitude:
                                p.drawLine(x1, y1, x2, y2)
                            else:
                                if x1 < 180 * x_scale and x2 < 180 * x_scale:
                                    p.drawLine(int(x1 + 180 * x_scale), y1, int(x2 + 180 * x_scale), y2)
                                elif x1 >= 180 * x_scale and x2 >= 180 * x_scale:
                                    p.drawLine(int(x1 - 180 * x_scale), y1, int(x2 - 180 * x_scale), y2)
                                else:
                                    pass
                                # možno doplnit přechod přes meridian (x1 < 180 * x_scale and x2 >= 180 * x_scale)

                # current position
                l_line_pen = QtGui.QPen(QtCore.Qt.blue)
                l_line_pen.setWidth(3)
                p.setPen(l_line_pen)
                x_now = int(self.a_now * x_scale - 5)
                if x_now < 0:
                    x_now = 0
                if not self.north_latitude:
                    if x_now < 180 * x_scale:
                        x_now = int(x_now + 180 * x_scale)
                    else:
                        x_now = int(x_now - 180 * x_scale)
                y_now = int((89 - self.h_now) * y_scale - 5)
                if y_now < 0:
                    y_now = 0
                p.drawEllipse(x_now, y_now, 10, 10)
                p.drawStaticText(x_now + 10, y_now + 10, QtGui.QStaticText("Current position"))

                # minimum position
                l_line_pen = QtGui.QPen(QtCore.Qt.red)
                l_line_pen.setWidth(3)
                p.setPen(l_line_pen)
                x_minimum = int(self.a_minimum * x_scale - 5)
                y_minimum = int((89 - self.h_minimum) * y_scale - 5)
                if x_minimum < 0:
                    x_minimum = 0
                if y_minimum < 0:
                    y_minimum = 0
                if not self.north_latitude:
                    if x_minimum < 180 * x_scale:
                        x_minimum = int(x_minimum + 180 * x_scale)
                    else:
                        x_minimum = int(x_minimum - 180 * x_scale)
                p.drawEllipse(x_minimum, y_minimum, 10, 10)
                p.drawStaticText(x_minimum + 10, y_minimum + 10, QtGui.QStaticText("Minimum position"))

                # moon position
                if self.h_moon_minimum > -15:
                    l_line_pen = QtGui.QPen(QtCore.Qt.yellow)
                    l_line_pen.setWidth(6)
                    p.setPen(l_line_pen)
                    x_moon_minimum = int(self.a_moon_minimum * x_scale - 5)
                    y_moon_minimum = int((89 - self.h_moon_minimum) * y_scale - 5)
                    if x_moon_minimum < 0:
                        x_moon_minimum = 0
                    if not self.north_latitude:
                        if x_moon_minimum < 180 * x_scale:
                            x_moon_minimum = int(x_moon_minimum + 180 * x_scale)
                        else:
                            x_moon_minimum = int(x_moon_minimum - 180 * x_scale)

                    if y_moon_minimum < 0:
                        y_moon_minimum = 0
                    p.drawEllipse(x_moon_minimum, y_moon_minimum, 10, 10)
                    l_line_pen = QtGui.QPen(QtCore.Qt.darkYellow)
                    l_line_pen.setWidth(6)
                    p.setPen(l_line_pen)
                    p.drawStaticText(x_moon_minimum + 10, y_moon_minimum + 10, QtGui.QStaticText(self.moon_phase))

                    # distance line
                    if self.h_moon_minimum > 0 and self.a_minimum > 0:
                        line_pen = QtGui.QPen(QtCore.Qt.red)
                        line_pen.setStyle(QtCore.Qt.DashLine)
                        line_pen.setWidth(1)
                        p.setPen(line_pen)
                        p.drawLine(x_moon_minimum + 5, y_moon_minimum + 5, x_minimum + 5, y_minimum + 5)

            if self.visibility_night_checkbox.isChecked():
                # visibility day
                if self.point_list[2]:
                    line_pen = QtGui.QPen(QtCore.Qt.darkBlue)
                    line_pen.setWidth(2)
                    p.setPen(line_pen)
                    h_set = self.point_list[1] * 2
                    for j, point in enumerate(self.point_list[2]):
                        if h_set[j] >= 0 and self.star_time_sunset <= point <= self.star_time_sunrise:
                            x = int((point - self.star_time_sunset) / (self.star_time_sunrise - self.star_time_sunset) * 365) + self.x_size_horizon
                            y = int((89 - h_set[j]) * y_scale)
                            p.drawPoint(x, y)
                    if self.lightcurve_window.lightcurves_points:
                        line_pen = QtGui.QPen(QtCore.Qt.red)
                        line_pen.setWidth(2)
                        p.setPen(line_pen)

                        curve_points = self.day_lightcurve_data_set_point
                        curve_min = min(curve_points)
                        curve_max = max(curve_points)

                        for m, curve_point in enumerate(curve_points):
                            x = m + self.x_size_horizon
                            y = 120 - int((curve_point - curve_min) / (curve_max - curve_min) * 120)
                            p.drawPoint(x, y)
                if self.prediction_table_widget.currentRow() > -1:
                    row = self.prediction_table_widget.currentRow()
                    minimum_jd = float(self.prediction_table[row][53])
                    minimum_h = int(self.prediction_table[row][54])
                    if self.current_sunset_jd < minimum_jd < self.current_sunrise_jd and minimum_h > 0:
                        x = int((minimum_jd - self.current_sunset_jd) / (self.current_sunrise_jd - self.current_sunset_jd) * 365 + self.x_size_horizon) - 5
                        y = int((89 - minimum_h) * y_scale) - 5
                        if x >= 0 and y >= 0:
                            line_pen = QtGui.QPen(QtCore.Qt.red)
                            line_pen.setWidth(2)
                            p.setPen(line_pen)
                            p.drawEllipse(x, y, 10, 10)



            else:
                # visibility year
                for point in self.horizon_visibility_table:
                    if point[4]:
                        line_pen = QtGui.QPen(QtCore.Qt.yellow)
                    else:
                        line_pen = QtGui.QPen(QtCore.Qt.gray)
                    line_pen.setWidth(1)
                    p.setPen(line_pen)
                    p.drawLine(point[0] + self.x_size_horizon, point[1], point[2] + self.x_size_horizon, point[3])
                line_pen = QtGui.QPen(QtCore.Qt.lightGray)
                line_pen.setWidth(1)
                p.setPen(line_pen)
                for point in self.year_sunset_sunrise_table:
                    p.drawLine(point[0] + self.x_size_horizon, point[1], point[2] + self.x_size_horizon, point[3])

        # cursor line
        line_pen = QtGui.QPen(QtCore.Qt.black)
        line_pen.setStyle(QtCore.Qt.DashLine)
        line_pen.setWidth(1)
        p.setPen(line_pen)
        p.drawLine(0, self.__current_info[1], self.x_size_horizon + 365, self.__current_info[1])
        p.drawLine(self.__current_info[0], 0, self.__current_info[0], self.y_size_horizon)
        if self.__current_info[0] < self.y_size_horizon * 0.75:
            date_position = self.__current_info[0] + 5
        else:
            date_position = self.__current_info[0] - 120
        if self.__current_info[1] < 330:
            time_position = self.__current_info[1] + 15
        else:
            time_position = self.__current_info[1] - 35
        p.drawStaticText(10 + self.x_size_horizon, time_position, QtGui.QStaticText(self.__current_info[3]))
        p.drawStaticText(date_position, 10, QtGui.QStaticText(self.__current_info[2]))
        p.drawStaticText(date_position + 20, 340, QtGui.QStaticText(self.faze))
        p.end()

    def mouseMoveEvent(self, event):
        x = event.x()
        y = event.y()
        self.paint_changed(x, y)

    def paint_changed(self, x, y):
        if y < self.y_size_horizon:
            if x < self.x_size_horizon or self.visibility_night_checkbox.isChecked():
                if x < self.x_size_horizon:
                    self.faze = ""
                    x_scale = self.x_size_horizon / 360
                    azimuth = int(x / x_scale)  #
                    if not self.north_latitude:
                        if azimuth < 180:
                            azimuth = azimuth + 180
                        else:
                            azimuth = azimuth - 180
                    azimuth_text = "Azimuth: " + str(azimuth)
                else:
                    if self.current_sunrise_jd and self.current_sunset_jd:
                        jd = (x - self.x_size_horizon) / 365 * (self.current_sunrise_jd - self.current_sunset_jd) + self.current_sunset_jd
                        if self.prediction_table_widget.currentRow() > -1:
                            row = self.prediction_table_widget.currentRow()
                            period = float(self.prediction_table[row][57])
                            epoch = float(self.prediction_table[row][25])
                            self.faze = "star phase: " + str(round((((jd - epoch) / period) % 1) * 100, 1)) + "%"
                        day = jd_to_date(jd)
                        azimuth_text = "UTC: " + day.strftime("%d %m %Y %H %M")
                    else:
                        azimuth_text = ""
                y_scale = self.y_size_horizon / 90
                h = 89 - int(y / y_scale)  #
                if h < 0:
                    h = 0
                h_text = "h: " + str(h)
                self.change_current_info([x, y, azimuth_text, h_text])
            else:
                if self.meridian:
                    x_visibility = x - self.x_size_horizon
                    day = jd_to_date(self.meridian + x_visibility + y/self.y_size_horizon)
                    day_text = "Date: " + day.strftime("%d %m %Y")
                    day_hour = "UTC: " + day.strftime("%H %M")
                    self.change_current_info([x, y, day_text, day_hour])
            self.update()

        else:
            pass

    def fill_form(self):
        self.hide_column()
        visibility_setup = self.user.prediction_visibility_setup()
        for i, column_setup in enumerate(visibility_setup):
            if column_setup == "1":
                if i == 0:
                    self.visibility_sun_checkbox.setChecked(True)
                elif i == 1:
                    self.visibility_horizon_checkbox.setChecked(True)
                else:
                    self.visibility_moon_checkbox.setChecked(True)
            else:
                if i == 0:
                    self.visibility_sun_checkbox.setChecked(False)
                elif i == 1:
                    self.visibility_horizon_checkbox.setChecked(False)
                else:
                    self.visibility_moon_checkbox.setChecked(False)

        self.sort_by_combobox.setCurrentText(self.user.prediction_sort_column_setup())

    def show_lightcurve(self):
        extend_time_start = self.lightcurve_window.lc_time_start_doublespinbox.value() - self.lightcurve_window.time_shift_days
        extend_time_end = self.lightcurve_window.lc_time_end_doublespinbox.value() + self.lightcurve_window.time_shift_days
        if self.prediction_table_widget.currentRow() > -1 and not self.isHidden():
            self.star_system.clear()
            row = self.prediction_table_widget.currentRow()
            for variable in self.variables.variables:
                if variable.name() == self.prediction_table[row][1]:
                    self.star_system.append(variable)
            for star in self.filtered_star.stars:
                if star.name() == self.prediction_table[row][1]:
                    self.lightcurve_window.change_visibility(self.time_period.visibility_point
                                                             (self.place,
                                                              star, self.sun,
                                                              sun_visibility=self.visibility_sun_checkbox.isChecked(),
                                                              moon_visibility=self.visibility_moon_checkbox.isChecked(),
                                                              horizon_visibility=self.visibility_horizon_checkbox.
                                                              isChecked(),
                                                              extend_time_start=extend_time_start,
                                                              extend_time_end=extend_time_end))
            self.lightcurve_window.check_lightcurves_and_fill(self.star_system)
            self.lightcurve_window.change_day_night(self.time_period.interact_sun(self.sun, self.place,
                                                                                  extend_time_start=extend_time_start,
                                                                                  extend_time_end=extend_time_end))
            if self.graph_lightcurve_button.isChecked():
                self.lightcurve_window.show()
            else:
                self.lightcurve_window.close()
        else:
            if self.step_main_form.show_lightcurve_checkbox.isChecked() and self.step_main_form.objects_table.currentRow() > -1:
                self.star_system.clear()
                row = self.step_main_form.objects_table.currentRow()
                for variable in self.variables.variables:
                    if variable.name() == self.filtered_star.stars[row].name():
                        self.star_system.append(variable)
                self.lightcurve_window.change_visibility(self.time_period.visibility_point
                                                         (self.place,
                                                          self.filtered_star.stars[row], self.sun,
                                                          sun_visibility=self.visibility_sun_checkbox.isChecked(),
                                                          moon_visibility=self.visibility_moon_checkbox.isChecked(),
                                                          horizon_visibility=self.visibility_horizon_checkbox.
                                                          isChecked(),
                                                          extend_time_start=extend_time_start,
                                                          extend_time_end=extend_time_end))
                self.lightcurve_window.check_lightcurves_and_fill(self.star_system)
                self.lightcurve_window.change_day_night(self.time_period.interact_sun(self.sun, self.place,
                                                                                      extend_time_start=extend_time_start,
                                                                                      extend_time_end=extend_time_end))
                self.lightcurve_window.update()
                self.lightcurve_window.show()
            else:
                self.lightcurve_window.close()

    def hide_button_is_checked_by_shortcut(self):
        if self.prediction_table_widget.currentRow() > -1:
            if self.hide_item_checkbox.isChecked():
                self.hide_item_checkbox.setChecked(False)
            else:
                self.hide_item_checkbox.setChecked(True)
        self.hide_button_is_checked()

    def hide_button_is_checked(self):
        if self.prediction_table_widget.currentRow() > -1:
            row = self.prediction_table_widget.currentRow()
            if self.hide_item_checkbox.isChecked():
                self.prediction_table[row][58] = True
                important_prediction = ImportantPrediction(self.user.name(), self.place.name, str(self.instrument.id),
                                                           self.prediction_table[row][1], self.prediction_table[row][2],
                                                           self.prediction_table[row][19])
                self.important_predictions.add_prediction(important_prediction)
            else:
                self.prediction_table[row][58] = False
                self.important_predictions.delete_prediction(self.user.name(), self.place.name,
                                                             self.prediction_table[row][1],
                                                             self.prediction_table[row][19])
        self.hide_row_and_column()

    def table_item_changed(self):
        self.lightcurve_window.time_home()
        star_system = []
        if self.place.latitude > 0:
            self.north_latitude = True
        else:
            self.north_latitude = False
        if self.prediction_table_widget.currentRow() > -1:
            row = self.prediction_table_widget.currentRow()
            for variable in self.variables.variables:
                if variable.name() == self.prediction_table[row][1]:
                    star_system.append(variable)
            self.note1.setText(self.prediction_table[row][27])
            self.note2.setText(self.prediction_table[row][28])
            self.note3.setText(self.prediction_table[row][29])
            self.hide_item_checkbox.setChecked(self.prediction_table[row][58])
            jd_minimum = float(self.prediction_table[row][19])
            try:
                is_set = False
                for i, star in enumerate(self.step_main_form.filtered_stars.stars):
                    if not is_set and star.name() == self.prediction_table[row][1]:
                        self.step_main_form.objects_table.selectRow(i)
                        self.selected_star = self.filtered_star.stars[i]
                        is_set = True
            except:
                pass
            self.point_list = half_arc_A_h(self.database.place.latitude, self.selected_star.declination(),
                                           self.selected_star.rektascenze(), 300)
            self.current_sunrise_jd = self.sun.sunrise_h(self.place.min_sunset, jd_minimum, self.place.longitude,
                                                         self.place.latitude, is_sunrise=True)
            self.current_sunset_jd = self.sun.sunrise_h(self.place.min_sunset, jd_minimum, self.place.longitude,
                                                        self.place.latitude, is_sunrise=False)
            if self.current_sunrise_jd == "No sunrise" or self.current_sunset_jd == "No sunrise":
                self.current_sunrise_jd = self.time_period.jd_start() + 1
                self.current_sunset_jd = self.time_period.jd_start()
                self.star_time_sunrise = (21.9433888888 + degrees(self.place.longitude) / 15 +
                                          (self.current_sunrise_jd - 2458534) * 24 * 1.0027379093) % 24
                self.star_time_sunset = (21.9433888888 + degrees(self.place.longitude) / 15 +
                                         (self.current_sunset_jd - 2458534) * 24 * 1.0027379093) % 24
            elif self.current_sunrise_jd == "No sunset" or self.current_sunset_jd == "No sunset":
                self.current_sunrise_jd = None
                self.current_sunset_jd = None
                self.star_time_sunrise = None
                self.star_time_sunset = None
            else:
                self.star_time_sunrise = (21.9433888888 + degrees(self.place.longitude) / 15 +
                                          (self.current_sunrise_jd - 2458534) * 24 * 1.0027379093) % 24
                self.star_time_sunset = (21.9433888888 + degrees(self.place.longitude) / 15 +
                                         (self.current_sunset_jd - 2458534) * 24 * 1.0027379093) % 24

            self.point_list[2] = self.point_list[2] * 2
            self.day_lightcurve_data_set_point = [0] * self.visibility_graph_column
            if self.current_sunrise_jd and self.current_sunset_jd:
                for i, variable in enumerate(star_system):
                    model = variable.lightcurve(self.current_sunset_jd, self.current_sunrise_jd,
                                                self.visibility_graph_column)
                    if model:
                        for j in range(0, len(model)):
                            self.day_lightcurve_data_set_point[j] = self.day_lightcurve_data_set_point[j] + model[j]
                    else:
                        pass

            for i in range(1, len(self.point_list[2])):
                if self.point_list[2][i] < self.point_list[2][i - 1]:
                    self.point_list[2][i] = self.point_list[2][i] + 2 * pi
                    if self.point_list[2][i] < self.point_list[2][i - 1]:
                        self.point_list[2][i] = self.point_list[2][i] + 2 * pi
            if self.current_sunrise_jd:
                self.star_time_sunrise = radians(self.star_time_sunrise * 15)
                self.star_time_sunset = radians(self.star_time_sunset * 15)
                if self.star_time_sunrise < self.star_time_sunset:
                    self.star_time_sunrise = self.star_time_sunrise + 2 * pi
                if self.star_time_sunset < self.point_list[2][0]:
                    self.star_time_sunrise = self.star_time_sunrise + 2 * pi
                    self.star_time_sunset = self.star_time_sunset + 2 * pi

            self.a_now = degrees(self.selected_star.horizon_coordinates_a(
                float(self.step_main_form.local_jd_now_label.text()), self.place.longitude, self.place.latitude))
            self.h_now = degrees(self.selected_star.horizon_coordinates_h(
                float(self.step_main_form.local_jd_now_label.text()), self.place.longitude, self.place.latitude))
            self.a_minimum = degrees(self.selected_star.horizon_coordinates_a(jd_minimum, self.place.longitude,
                                                                              self.place.latitude))
            self.h_minimum = degrees(self.selected_star.horizon_coordinates_h(jd_minimum, self.place.longitude,
                                                                              self.place.latitude))
            self.a_moon_minimum = degrees(self.moon.azimuth(jd_minimum, self.place.latitude, self.place.longitude))
            self.h_moon_minimum = degrees(self.moon.h(jd_minimum, self.place.latitude, self.place.longitude))
            self.moon_distance = angular_separation(radians(self.a_minimum), radians(self.h_minimum),
                                                    radians(self.a_moon_minimum), radians(self.h_moon_minimum))
            phase = self.moon.moon_phase(jd_minimum) / pi
            if phase > 1:
                phase = 2 - phase
            self.moon_phase = "Moon faze:" + str(int(phase * 100)) + "% angular sep:" + str(int(degrees(self.moon_distance))) + "°"
            self.lightcurve_window.update()
            self.update()
            self.show_lightcurve()
            self.show_prediction2()
        else:
            self.selected_star = None

    def show_prediction2(self):
        if self.place.latitude > 0:
            self.north_latitude = True
        else:
            self.north_latitude = False
        if self.prediction_table_widget.currentRow() > -1:
            row = self.prediction_table_widget.currentRow()
            for star in self.filtered_star.stars:
                if star.name() == self.prediction_table[row][1]:
                    self.rise_set()
                    self.horizon_set(star)
                    self.update()

    def fill_prediction(self):
        if self.place.latitude > 0:
            self.north_latitude = True
        else:
            self.north_latitude = False
        self.prediction_table_widget.clear()
        visibility_sun = self.visibility_sun_checkbox.isChecked()
        visibility_moon = self.visibility_moon_checkbox.isChecked()
        visibility_horizon = self.visibility_horizon_checkbox.isChecked()
        moon_min_distance = radians(self.moon_distance_spinbox.value())
        moon_max_phase = self.moon_phase_spinbox.value()
        self.prediction_table = self.filtered_star.prediction(visibility_sun=visibility_sun,
                                                              visibility_horizon=visibility_horizon,
                                                              visibility_moon=visibility_moon,
                                                              moon_max_phase=moon_max_phase,
                                                              moon_min_distance=moon_min_distance)
        self.sort_prediction_table()


    def fill_table(self):
        self.prediction_table_widget.setRowCount(len(self.prediction_table))
        self.prediction_table_widget.setColumnCount(len(self.prediction_key))
        self.prediction_table_widget.setHorizontalHeaderLabels(self.prediction_key)
        for i in range(len(self.prediction_table)):
            for j in range(len(self.prediction_key)):
                self.prediction_table_widget.setItem(i, j, QtWidgets.QTableWidgetItem(self.prediction_table[i][j]))
        self.prediction_table_widget.resizeColumnsToContents()
        self.hide_row_and_column()

    def hide_row_and_column(self):
        self.hide_column()
        self.hide_row()
        self.prediction_table_widget.resizeColumnsToContents()
        try:
            self.lightcurve_window.update()
        except:
            pass
        try:
            self.update()
        except:
            pass


    def hide_row(self):
        for i, prediction in enumerate(self.prediction_table):
            if prediction[58] or self.show_all_checkbox.isChecked():
                self.prediction_table_widget.showRow(i)
            else:
                self.prediction_table_widget.hideRow(i)

    def hide_column(self):
        if self.columns_setup[0] == "1":
            self.prediction_table_widget.showColumn(0)
        else:
            self.prediction_table_widget.hideColumn(0)
        if self.columns_setup[1] == "1":
            self.prediction_table_widget.showColumn(1)
        else:
            self.prediction_table_widget.hideColumn(1)
        if self.columns_setup[2] == "1":
            self.prediction_table_widget.showColumn(2)
        else:
            self.prediction_table_widget.hideColumn(2)
        if self.columns_setup[3] == "1":
            self.prediction_table_widget.showColumn(3)
        else:
            self.prediction_table_widget.hideColumn(3)
        if self.columns_setup[4] == "1":
            self.prediction_table_widget.showColumn(4)
        else:
            self.prediction_table_widget.hideColumn(4)
        if self.columns_setup[5] == "1":
            self.prediction_table_widget.showColumn(5)
        else:
            self.prediction_table_widget.hideColumn(5)
        if self.columns_setup[6] == "1":
            self.prediction_table_widget.showColumn(6)
        else:
            self.prediction_table_widget.hideColumn(6)
        if self.columns_setup[7] == "1":
            self.prediction_table_widget.showColumn(7)
            self.prediction_table_widget.showColumn(8)
        else:
            self.prediction_table_widget.hideColumn(7)
            self.prediction_table_widget.hideColumn(8)
        if self.columns_setup[8] == "1":
            self.prediction_table_widget.showColumn(9)
        else:
            self.prediction_table_widget.hideColumn(9)
        if self.columns_setup[9] == "1":
            self.prediction_table_widget.showColumn(10)
            self.prediction_table_widget.showColumn(11)
        else:
            self.prediction_table_widget.hideColumn(10)
            self.prediction_table_widget.hideColumn(11)
        if self.columns_setup[10] == "1":
            self.prediction_table_widget.showColumn(12)
        else:
            self.prediction_table_widget.hideColumn(12)
        if self.columns_setup[11] == "1":
            self.prediction_table_widget.showColumn(13)
            self.prediction_table_widget.showColumn(14)
        else:
            self.prediction_table_widget.hideColumn(13)
            self.prediction_table_widget.hideColumn(14)
        if self.columns_setup[12] == "1":
            self.prediction_table_widget.showColumn(15)
            self.prediction_table_widget.showColumn(16)
        else:
            self.prediction_table_widget.hideColumn(15)
            self.prediction_table_widget.hideColumn(16)
        if self.columns_setup[13] == "1":
            self.prediction_table_widget.showColumn(17)
            self.prediction_table_widget.showColumn(18)
        else:
            self.prediction_table_widget.hideColumn(17)
            self.prediction_table_widget.hideColumn(18)
        if self.columns_setup[14] == "1":
            self.prediction_table_widget.showColumn(19)
        else:
            self.prediction_table_widget.hideColumn(19)
        if self.columns_setup[15] == "1":
            self.prediction_table_widget.showColumn(20)
        else:
            self.prediction_table_widget.hideColumn(20)
        if self.columns_setup[16] == "1":
            self.prediction_table_widget.showColumn(21)
        else:
            self.prediction_table_widget.hideColumn(21)
        if self.columns_setup[17] == "1":
            self.prediction_table_widget.showColumn(22)
        else:
            self.prediction_table_widget.hideColumn(22)
        if self.columns_setup[18] == "1":
            self.prediction_table_widget.showColumn(23)
        else:
            self.prediction_table_widget.hideColumn(23)
        if self.columns_setup[19] == "1":
            self.prediction_table_widget.showColumn(24)
        else:
            self.prediction_table_widget.hideColumn(24)
        if self.columns_setup[20] == "1":
            self.prediction_table_widget.showColumn(25)
        else:
            self.prediction_table_widget.hideColumn(25)
        if self.columns_setup[21] == "1":
            self.prediction_table_widget.showColumn(26)
        else:
            self.prediction_table_widget.hideColumn(26)
        if self.columns_setup[22] == "1":
            self.prediction_table_widget.showColumn(27)
            self.prediction_table_widget.showColumn(28)
            self.prediction_table_widget.showColumn(29)
        else:
            self.prediction_table_widget.hideColumn(27)
            self.prediction_table_widget.hideColumn(28)
            self.prediction_table_widget.hideColumn(29)
        if self.columns_setup[23] == "1":
            self.prediction_table_widget.showColumn(30)
            self.prediction_table_widget.showColumn(31)
            self.prediction_table_widget.showColumn(32)
            self.prediction_table_widget.showColumn(33)
            self.prediction_table_widget.showColumn(34)
            self.prediction_table_widget.showColumn(35)
            self.prediction_table_widget.showColumn(36)
            self.prediction_table_widget.showColumn(37)
            self.prediction_table_widget.showColumn(38)
            self.prediction_table_widget.showColumn(39)
            self.prediction_table_widget.showColumn(40)
            self.prediction_table_widget.showColumn(41)
            self.prediction_table_widget.showColumn(42)
            self.prediction_table_widget.showColumn(43)
            self.prediction_table_widget.showColumn(44)
            self.prediction_table_widget.showColumn(45)
            self.prediction_table_widget.showColumn(46)
            self.prediction_table_widget.showColumn(47)
        else:
            self.prediction_table_widget.hideColumn(30)
            self.prediction_table_widget.hideColumn(31)
            self.prediction_table_widget.hideColumn(32)
            self.prediction_table_widget.hideColumn(33)
            self.prediction_table_widget.hideColumn(34)
            self.prediction_table_widget.hideColumn(35)
            self.prediction_table_widget.hideColumn(36)
            self.prediction_table_widget.hideColumn(37)
            self.prediction_table_widget.hideColumn(38)
            self.prediction_table_widget.hideColumn(39)
            self.prediction_table_widget.hideColumn(40)
            self.prediction_table_widget.hideColumn(41)
            self.prediction_table_widget.hideColumn(42)
            self.prediction_table_widget.hideColumn(43)
            self.prediction_table_widget.hideColumn(44)
            self.prediction_table_widget.hideColumn(45)
            self.prediction_table_widget.hideColumn(46)
            self.prediction_table_widget.hideColumn(47)


    def sort_prediction_table(self):

        """
        "Name"1    "Pair"2    "Alt.name"4    "Const."5    "Type"6    "Rec."7    "Dec."8  "Mag."9 N    "Starrise"13
        "Starset"14    "D entry"15    "D output"16    "Minimum JD"19    "h at min."21    "Moon distance"22
        "Amplitude"23    "Epoch 0"25    "Period"26

        "Mag."9 N , "Starrise"13
        "Starset"14    "D entry"15    "D output"16    "Minimum JD"19    "h at min."21    "Moon distance"22
        "Amplitude"23    "Epoch 0"25    "Period"26
like number and date :
        "Mag." -48, "Starrise"-49, "Starset"-50, "D entry"-51, "D output"-52, "Minimum JD"-53, "h at min.-54",
        "Moon distance"-55, "Amplitude"-56, "Period-57"
        """


        if self.sort_by_combobox.currentText() == "Minimum (JD)":
            s1, s2, s3, s4 = 53, 1, 2, None
        elif self.sort_by_combobox.currentText() == "Name":
            s1, s2, s3, s4 = 1, 2, 53, None
        elif self.sort_by_combobox.currentText() == "Alt.name":
            s1, s2, s3, s4 = 4, 2, 53, None
        elif self.sort_by_combobox.currentText() == "Rektascenze":
            s1, s2, s3, s4 = 7, 2, 53, None
        elif self.sort_by_combobox.currentText() == "Declination":
            s1, s2, s3, s4 = 8, 2, 53, None
        elif self.sort_by_combobox.currentText() == "Constellation + Name":
            s1, s2, s3, s4 = 5, 1, 2, 53
        elif self.sort_by_combobox.currentText() == "Type+Name":
            s1, s2, s3, s4 = 6, 1, 2, 53
        elif self.sort_by_combobox.currentText() == "Magnitude":
            s1, s2, s3, s4 = 48, 1, 2, 53
        elif self.sort_by_combobox.currentText() == "Starrise":
            s1, s2, s3, s4 = 49, 1, 2, 53
        elif self.sort_by_combobox.currentText() == "Starset":
            s1, s2, s3, s4 = 50, 1, 2, 53
        elif self.sort_by_combobox.currentText() == "D-entry":
            s1, s2, s3, s4 = 51, 1, 2, 53
        elif self.sort_by_combobox.currentText() == "D-output":
            s1, s2, s3, s4 = 52, 1, 2, 53
        elif self.sort_by_combobox.currentText() == "Star h":
            s1, s2, s3, s4 = 54, 1, 2, 53
        elif self.sort_by_combobox.currentText() == "Moon(dist)":
            s1, s2, s3, s4 = 55, 1, 2, 53
        elif self.sort_by_combobox.currentText() == "Amplitude":
            s1, s2, s3, s4 = 56, 1, 2, 53
        elif self.sort_by_combobox.currentText() == "Period":
            s1, s2, s3, s4 = 57, 1, 2, 53
        else:
            return
        for i in range(len(self.prediction_table) - 1):
            for j in range(i + 1, len(self.prediction_table)):
                if self.prediction_table[i][s1] >= self.prediction_table[j][s1]:
                    if self.prediction_table[i][s1] == self.prediction_table[j][s1] and s2:
                        # level 2
                        if self.prediction_table[i][s2] >= self.prediction_table[j][s2]:
                            if self.prediction_table[i][s2] == self.prediction_table[j][s2] and s3:
                                # level 3
                                if self.prediction_table[i][s3] >= self.prediction_table[j][s3]:
                                    if self.prediction_table[i][s3] == self.prediction_table[j][s3] and s4:
                                        # level 4
                                        if self.prediction_table[i][s4] > self.prediction_table[j][s4]:
                                            new_max = self.prediction_table.pop(j)
                                            self.prediction_table.insert(i, new_max)
                                    else:
                                        new_max = self.prediction_table.pop(j)
                                        self.prediction_table.insert(i, new_max)
                            else:
                                new_max = self.prediction_table.pop(j)
                                self.prediction_table.insert(i, new_max)
                    else:
                        new_max = self.prediction_table.pop(j)
                        self.prediction_table.insert(i, new_max)
        self.fill_table()

class ImportantPrediction:

    def __init__(self, user_name, place_name, instrument_id, star_name, variable_pair, minimum_jd):
        self.__user = user_name
        self.__place = place_name
        self.__instrument = instrument_id
        self.__star = star_name
        self.__variable = variable_pair
        self.__minimum_jd = minimum_jd

    def __str__(self):
        return "user:{0}, place:{1}, instrument:{2}, star:{3}, variable:{4}, minimum_JD:{5}".format(self.__user,
                                                                                                    self.__place,
                                                                                                    self.__instrument,
                                                                                                    self.__star,
                                                                                                    self.__variable,
                                                                                                    self.__minimum_jd)

    def user(self):
        return self.__user
    def place(self):
        return self.__place
    def instrument(self):
        return self.__instrument
    def star(self):
        return self.__star
    def variable(self):
        return self.__variable
    def minimum_jd(self):
        return self.__minimum_jd

    def change_user(self, new):
        self.__user = new
    def change_place(self, new):
        self.__place = new
    def change_instrument(self, new):
        self.__instrument = new
    def change_star(self, new):
        self.__star = new
    def change_variable(self, new):
        self.__variable = new
    def change_minimum_jd(self, new):
        self.__minimum_jd = new

    def to_text(self):
        string = []
        string.append(self.__user)
        string.append(self.__place)
        string.append(self.__instrument)
        string.append(self.__star)
        string.append(self.__variable)
        string.append(self.__minimum_jd)
        return string

class ImportantPredictions:

    def __init__(self, list_of_important_prediction: list):
        self.__predictions = list_of_important_prediction

    def important_predictions(self):
        return self.__predictions

    def add_prediction(self, important_prediction):
        self.__predictions.append(important_prediction)

    def delete_prediction(self, user, obs_place, star, jd):
        for i, p in enumerate(self.__predictions):
            if p.user() == user and p.place() == obs_place and p.star() == star and p.minimum_jd() == jd:
                del(self.__predictions[i])
                return

    def delete_old_prediction(self, current_jd, max_age_of_prediction=7):
        prediction_index_for_delete_list = []
        for i, p in enumerate(self.__predictions):
            if float(current_jd) - max_age_of_prediction > float(p.minimum_jd()):
                prediction_index_for_delete_list.append(i)
        prediction_index_for_delete_list.sort(reverse=True)
        for prediction_index in prediction_index_for_delete_list:
            del (self.__predictions[prediction_index])

    def confirm_prediction(self, user, obs_place, star, jd):
        for i, p in enumerate(self.__predictions):
            if p.user() == user and p.place() == obs_place and p.star() == star and p.minimum_jd() == jd:
                return True
        return False

    def total_number(self):
        return len(self.__predictions)

    def give_prediction(self, index):
        return self.__predictions[index]










