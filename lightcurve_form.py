from PyQt5 import QtWidgets, QtCore, QtGui
from datetime import datetime
from time_period import *
from prediction_form_2 import *
from variables import *


class LightCurveWindow(QtWidgets.QWidget):

    def __init__(self, *args, **kwargs):
        super(LightCurveWindow, self).__init__(*args, **kwargs)

        self.fixed_position = False
        self.point_position = []
        self.position = [0, 501]

        self.setWindowTitle("Lightcurve")
        self.setWindowIcon(QtGui.QIcon("chart-down-color.png"))
        self.setMouseTracking(True)
        self.setMinimumWidth(1501)
        self.setContentsMargins(0, 520, 0, 0)

        self.__time_period_visibility = [True] * 1500
        self.__day_night = []
        self.system_name = ""
        self.time_point = []
        self.point_line_jd = None
        self.point_line_coor = None


        # widgets and layouts
        self.lc_current_position_time_utc = QtWidgets.QLabel("")
        self.lc_current_position_time_utc.setFixedWidth(85)
        self.lc_current_position_time_jd = QtWidgets.QLabel("")
        self.lc_current_position_time_jd.setFixedWidth(85)
        self.lc_current_position_amplitude = QtWidgets.QLabel("")
        self.lc_current_position_amplitude.setFixedWidth(105)
        self.lc_current_position_pair = QtWidgets.QLabel("")
        self.lc_current_position_pair.setFixedWidth(105)
        self.lc_fixed_point_utc = QtWidgets.QLabel("")
        self.lc_fixed_point_utc.setFixedWidth(85)
        self.lc_fixed_point_jd = QtWidgets.QLabel("")
        self.lc_fixed_point_jd.setFixedWidth(85)
        self.lc_fixed_point_distance_time = QtWidgets.QLabel("")
        self.lc_fixed_point_distance_time.setFixedWidth(100)
        self.lc_fixed_point_distance_amplitude = QtWidgets.QLabel("")
        self.lc_fixed_point_distance_amplitude.setFixedWidth(100)
        self.lc_time_start_doublespinbox = QtWidgets.QDoubleSpinBox()
        self.lc_time_end_doublespinbox = QtWidgets.QDoubleSpinBox()
        self.variables_information = []

        self.lc_time_forward_button = QtWidgets.QPushButton("Forward")
        self.lc_time_back_button = QtWidgets.QPushButton("Back")
        self.lc_time_home_button = QtWidgets.QPushButton("Home")
        self.lc_time_position_label = QtWidgets.QLabel("")
        self.time_shift_days = 0
        self.lc_current_position_time_utc.setAlignment(QtCore.Qt.AlignLeft)
        self.lc_current_position_time_jd.setAlignment(QtCore.Qt.AlignLeft)
        self.lc_current_position_amplitude.setAlignment(QtCore.Qt.AlignLeft)
        self.lc_current_position_pair.setAlignment(QtCore.Qt.AlignLeft)
        self.lc_fixed_point_utc.setAlignment(QtCore.Qt.AlignLeft)
        self.lc_fixed_point_jd.setAlignment(QtCore.Qt.AlignLeft)
        self.lc_fixed_point_distance_time.setAlignment(QtCore.Qt.AlignLeft)
        self.lc_fixed_point_distance_amplitude.setAlignment(QtCore.Qt.AlignLeft)

        self.lc_time_area_star_info_label = QtWidgets.QLabel("")
        self.lc_time_area_star_info_label.setFixedWidth(85)
        self.lc_time_area_end_info_label = QtWidgets.QLabel("")
        self.lc_time_area_end_info_label.setFixedWidth(85)
        self.lc_current_time_checkbox = QtWidgets.QCheckBox("Show current time line")
        self.lc_current_time_checkbox.setChecked(True)
        self.lc_object_name_info = QtWidgets.QLabel("")


        lc_info_time_layout = QtWidgets.QFormLayout()
        lc_info_time_layout.addRow(QtWidgets.QLabel("Time UTC: "), self.lc_current_position_time_utc)
        lc_info_time_layout.addRow(QtWidgets.QLabel("Time JD: "), self.lc_current_position_time_jd)

        lc_info_amp_layout = QtWidgets.QFormLayout()
        lc_info_amp_layout.addRow(QtWidgets.QLabel("Amplitude(mag): "), self.lc_current_position_amplitude)
        lc_info_amp_layout.addRow(QtWidgets.QLabel("Pair without model: "), self.lc_current_position_pair)

        lc_point_time_layout = QtWidgets.QFormLayout()
        lc_point_time_layout.addRow(QtWidgets.QLabel("Selected point UTC: "), self.lc_fixed_point_utc)
        lc_point_time_layout.addRow(QtWidgets.QLabel("Selected point JD: "), self.lc_fixed_point_jd)

        lc_point_amp_layout = QtWidgets.QFormLayout()
        lc_point_amp_layout.addRow(QtWidgets.QLabel("Distance(time): "), self.lc_fixed_point_distance_time)
        lc_point_amp_layout.addRow(QtWidgets.QLabel("Distance(mag): "), self.lc_fixed_point_distance_amplitude)

        lc_set_time_layout = QtWidgets.QFormLayout()
        lc_set_time_layout.addRow(QtWidgets.QLabel("Time extension start(days): "), self.lc_time_start_doublespinbox)
        lc_set_time_layout.addRow(QtWidgets.QLabel("time extension end(days): "), self.lc_time_end_doublespinbox)

        lc_time_aria_info_layout = QtWidgets.QFormLayout()
        lc_time_aria_info_layout.addRow(QtWidgets.QLabel("Start UTC: "), self.lc_time_area_star_info_label)
        lc_time_aria_info_layout.addRow(QtWidgets.QLabel("End UTC: "), self.lc_time_area_end_info_label)

        lc_name_and_current_time_layout = QtWidgets.QVBoxLayout()
        lc_name_and_current_time_first_line_layout = QtWidgets.QHBoxLayout()

        lc_name_and_current_time_first_line_layout.addWidget(self.lc_current_time_checkbox)
        lc_name_and_current_time_first_line_layout.addWidget(self.lc_time_home_button)

        lc_name_and_current_time_second_line_layout = QtWidgets.QHBoxLayout()
        lc_name_and_current_time_second_line_layout.addWidget(self.lc_time_back_button)
        lc_name_and_current_time_second_line_layout.addWidget(self.lc_time_forward_button)
        lc_name_and_current_time_second_line_layout.addWidget(self.lc_time_position_label)
        lc_name_and_current_time_layout.addLayout(lc_name_and_current_time_first_line_layout)
        lc_name_and_current_time_layout.addLayout(lc_name_and_current_time_second_line_layout)

        logo_button = QtWidgets.QPushButton("")
        logo_button.setIcon(QtGui.QIcon("lightcurve.png"))
        logo_button.setIconSize(QtCore.QSize(70, 20))
        logo_button.setFixedSize(80, 25)

        lc_info_time_groupbox = QtWidgets.QGroupBox("current cursor position - time / amp")
        lc_info_time_amp_layout = QtWidgets.QHBoxLayout()
        lc_info_time_groupbox.setLayout(lc_info_time_amp_layout)
        lc_info_time_amp_layout.addWidget(logo_button)
        lc_info_time_amp_layout.addLayout(lc_info_time_layout)
        lc_info_time_amp_layout.addLayout(lc_info_amp_layout)


        lc_info_point_groupbox = QtWidgets.QGroupBox("position of selected point - time")
        lc_point_time_amp_layout = QtWidgets.QHBoxLayout()
        lc_info_point_groupbox.setLayout(lc_point_time_amp_layout)
        lc_point_time_amp_layout.addLayout(lc_point_time_layout)
        lc_point_time_amp_layout.addLayout(lc_point_amp_layout)

        lc_info_time_aria_groupbox = QtWidgets.QGroupBox("time aria info")
        lc_info_time_aria_groupbox.setLayout(lc_time_aria_info_layout)


        lc_set_time_groupbox = QtWidgets.QGroupBox("change time start or time end")
        lc_set_time_groupbox.setLayout(lc_set_time_layout)

        lc_info_layout = QtWidgets.QHBoxLayout() # infolayout
        lc_info_layout.addWidget(lc_info_time_groupbox)
        lc_info_layout.addWidget(lc_set_time_groupbox)
        lc_info_layout.addWidget(lc_info_time_aria_groupbox)
        lc_info_layout.addLayout(lc_name_and_current_time_layout)
        lc_info_layout.addStretch()
        lc_info_layout.addWidget(lc_info_point_groupbox)

        lc_window_layout = QtWidgets.QVBoxLayout()  # main layout
        self.setLayout(lc_window_layout)
        lc_window_layout.addLayout(lc_info_layout)
        lc_window_layout.addStretch()


    def setup(self):
        from step_application import root
        self.step_main_form = root.step_main_form
        self.database = root.database
        self.time_period = root.database.time_period
        self.minimum_form = root.prediction2
        self.sun = root.database.sun
        self.lightcurves_points = []
        self.steps = 1500
        self.systems = []
        self.system_without_model = []

        self.save_action = self.step_main_form.save_action
        self.photometry_action = self.step_main_form.photometry_action
        self.star_edit_action = self.step_main_form.star_edit_action
        self.show_observation_action = self.step_main_form.observation_action
        self.addAction(self.save_action)
        self.addAction(self.photometry_action)
        self.addAction(self.star_edit_action)
        self.addAction(self.show_observation_action)

        self.lc_time_start_doublespinbox.valueChanged.connect(self.time_start_was_changed)
        self.lc_time_end_doublespinbox.valueChanged.connect(self.time_end_was_changed)
        self.lc_time_start_doublespinbox.setValue(float(self.database.user.time_extension_setup()[0]))
        self.lc_time_end_doublespinbox.setValue(float(self.database.user.time_extension_setup()[1]))
        self.lc_time_forward_button.clicked.connect(self.time_forward)
        self.lc_time_back_button.clicked.connect(self.time_backward)
        self.lc_time_home_button.clicked.connect(self.time_home)

    def time_start_was_changed(self):
        self.minimum_form.show_lightcurve()
        self.clear_point_position()
        self.data_was_changed()
        self.update()

    def time_end_was_changed(self):
        self.minimum_form.show_lightcurve()
        self.clear_point_position()
        self.data_was_changed()
        self.update()


    def time_forward(self):
        start = self.time_period.jd_start() - self.lc_time_start_doublespinbox.value()
        end = self.time_period.jd_end() + self.lc_time_end_doublespinbox.value()

        self.time_shift_days = self.time_shift_days + (end - start) / 2
        self.set_time_shift()
        self.minimum_form.show_lightcurve()
        self.clear_point_position()
        self.data_was_changed()
        self.set_selected_point_position()
        self.update()

    def time_backward(self):
        start = self.time_period.jd_start() - self.lc_time_start_doublespinbox.value()
        end = self.time_period.jd_end() + self.lc_time_end_doublespinbox.value()

        self.time_shift_days = self.time_shift_days - (end - start) / 2
        self.set_time_shift()
        self.minimum_form.show_lightcurve()
        self.clear_point_position()
        self.data_was_changed()
        self.set_selected_point_position()
        self.update()

    def set_time_shift(self):
        shift = str(round(self.time_shift_days, 2))
        if self.time_shift_days < 0:
            self.lc_time_position_label.setText("Past:{0}d".format(shift))
        elif self.time_shift_days > 0:
            self.lc_time_position_label.setText("Future:{0}d".format(shift))
        else:
            self.lc_time_position_label.setText("")


    def time_home(self):
        self.time_shift_days = 0
        self.lc_time_position_label.setText("")
        self.minimum_form.show_lightcurve()
        self.clear_point_position()
        self.data_was_changed()
        self.set_selected_point_position()
        self.update()

    def change_visibility(self, new_visibility):
        self.__time_period_visibility = new_visibility

    def change_day_night(self, new_day_night):
        self.__day_night = new_day_night

    def check_lightcurves_and_fill(self, star_system):
        self.lightcurves_points.clear()
        self.systems.clear()
        self.system_without_model.clear()
        self.system_without_model.append(star_system[0].name())
        self.variables_information = []
        system_amplitude = 0
        self.time_point = []
        if star_system:
            start = self.time_period.jd_start() - self.lc_time_start_doublespinbox.value() + self.time_shift_days
            end = self.time_period.jd_end() + self.lc_time_end_doublespinbox.value() + self.time_shift_days
            for s in range(0, self.steps):
                self.time_point.append(start + (end - start)/self.steps * s)
            for i, variable in enumerate(star_system):
                lightcurve_points = []
                model = variable.lightcurve(start, end, self.steps)
                if model:
                    lightcurve_points.append(model)  # index 0
                    max_amplitude = max(model)
                    min_amplitude = min(model)
                    amplitude = max_amplitude - min_amplitude
                    system_amplitude = system_amplitude + amplitude
                    lightcurve_points.append(variable.name())  # index 1
                    lightcurve_points.append(variable.pair())  # index 2
                    lightcurve_points.append(min_amplitude)  # index 3
                    lightcurve_points.append(max_amplitude)  # index 4
                    lightcurve_points.append(amplitude)  # index 5
                    self.systems.append(variable.pair())
                    self.variables_information.append(variable)
                    self.lightcurves_points.append(lightcurve_points)
                else:
                    self.system_without_model.append(variable.pair())
            if self.systems:
                self.systems.sort(reverse=True)
                self.lightcurves_points.sort(key=lambda row: row[2], reverse=True)
                if len(self.systems) > 1:
                    self.systems.insert(0, "All stars")
                    final_curve = []
                    final_information =[]
                    for j in range (len(self.lightcurves_points[0][0])):
                        final_point = 0
                        for curve in self.lightcurves_points:
                            final_point = final_point + curve[0][j]
                        final_curve.append(final_point)
                    final_max = max(final_curve)
                    final_min = min(final_curve)
                    final_information.append(final_curve)
                    final_information.append(self.lightcurves_points[0][1])
                    final_information.append("final")
                    final_information.append(final_min)
                    final_information.append(final_max)
                    final_information.append(final_max - final_min)
                    self.lightcurves_points.insert(0, final_information)
                    system_amplitude = system_amplitude + final_max - final_min
            if self.lightcurves_points:
                self.lightcurves_points[0].append(system_amplitude)  # index 6
            self.system_name = self.system_without_model.pop(0)
            self.setWindowTitle("Lightcurve " + self.system_name)
            if self.system_without_model:
                self.lc_current_position_pair.setText(",".join(self.system_without_model))
            else:
                self.lc_current_position_pair.setText("all models are defined")

    def closeEvent(self, a0: QtGui.QCloseEvent):
        self.minimum_form.graph_lightcurve_button.setChecked(False)
        self.step_main_form.show_lightcurve_checkbox.setChecked(False)

    def paintEvent(self, event):
        # night / day
        p = QtGui.QPainter(self)
        night_colour = QtGui.QBrush(QtCore.Qt.gray)
        night_colour.setStyle(QtCore.Qt.Dense6Pattern)
        p.fillRect(0, 0, 1500, 500, night_colour)
        if self.__day_night:
            for i in range(0, len(self.__day_night), 2):
                sunset = int(
                    (self.__day_night[i] - self.time_period.jd_start() + self.lc_time_start_doublespinbox.value()
                     - self.time_shift_days) /
                    (self.time_period.jd_end() - self.time_period.jd_start() + self.lc_time_start_doublespinbox.value()
                     + self.lc_time_end_doublespinbox.value()) * 1500)
                sunrise = int(
                    (self.__day_night[i+1] - self.time_period.jd_start() + self.lc_time_start_doublespinbox.value()
                     - self.time_shift_days) /
                    (self.time_period.jd_end() - self.time_period.jd_start() + self.lc_time_start_doublespinbox.value()
                     + self.lc_time_end_doublespinbox.value()) * 1500)
                p.fillRect(sunset, 0, sunrise - sunset, 500, QtGui.QBrush(QtCore.Qt.white))
        # cursor position - horizontal
        if self.position[1] < 500:
            line_pen = QtGui.QPen(QtCore.Qt.black)
            line_pen.setWidth(1)
            p.setPen(line_pen)
            if self.position[0] < 1350:
                p.drawStaticText(self.position[0] + 5, 460,
                                 QtGui.QStaticText("UTC :" + self.lc_current_position_time_utc.text()))
                p.drawStaticText(self.position[0] + 5, 480,
                                 QtGui.QStaticText("JD :" + self.lc_current_position_time_jd.text()))

            else:
                p.drawStaticText(self.position[0] - 149, 460,
                                 QtGui.QStaticText("UTC :" + self.lc_current_position_time_utc.text()))
                p.drawStaticText(self.position[0] - 149, 480,
                                 QtGui.QStaticText("JD :" + self.lc_current_position_time_jd.text()))
            # cursor position amplitude
            if self.systems and self.position[1]:
                calculate_position = 500 - self.position[1]
                part_amplitude = (calculate_position / 500) * self.lightcurves_points[0][6]
                system_index = -1
                while part_amplitude - self.lightcurves_points[system_index][5] > 0:
                    part_amplitude = part_amplitude - self.lightcurves_points[system_index][5]
                    system_index = system_index - 1
                part_amplitude = self.lightcurves_points[system_index][5] - part_amplitude
                phase_text = ""
                for variable in self.variables_information:
                    if variable.pair() == self.systems[system_index]:
                        current_jd = float(self.lc_current_position_time_jd.text())
                        phase = str(round((((current_jd - variable.epoch()) / variable.period()) % 1) * 100, 2)) + "%"
                        phase_text = "Phase " + self.systems[system_index] + " " + phase
                if self.position[1] > 420:
                    p.drawStaticText(5, self.position[1] - 20, QtGui.QStaticText(
                        "Amplitude " + self.systems[system_index] + " " + str(round(part_amplitude, 3)) + " mag"))
                    if self.position[0] < 1350:
                        p.drawStaticText(self.position[0] + 5, self.position[1] - 20,
                                         QtGui.QStaticText(phase_text))
                    else:
                        p.drawStaticText(self.position[0] - 149, self.position[1] - 20,
                                         QtGui.QStaticText(phase_text))


                else:
                    p.drawStaticText(5, self.position[1] + 5, QtGui.QStaticText(
                        "Amplitude " + self.systems[system_index] + " " + str(round(part_amplitude, 3)) + " mag"))
                    if self.position[0] < 1350:
                        p.drawStaticText(self.position[0] + 5, self.position[1] + 5,
                                         QtGui.QStaticText(phase_text))
                    else:
                        p.drawStaticText(self.position[0] - 149, self.position[1] + 5,
                                         QtGui.QStaticText(phase_text))


            # current time line
            if self.lc_current_time_checkbox.isChecked():
                start = self.time_period.jd_start() - self.lc_time_start_doublespinbox.value() + self.time_shift_days
                end = self.time_period.jd_end() + self.lc_time_end_doublespinbox.value() + self.time_shift_days
                current = float(self.step_main_form.local_jd_now_label.text())
                if start <= current <= end:
                    line_pen = QtGui.QPen(QtCore.Qt.red)
                    line_pen.setStyle(QtCore.Qt.DashLine)
                    line_pen.setWidth(2)
                    p.setPen(line_pen)
                    x_coordinate = int((current - start) / (end - start) * 1500)
                    p.drawLine(x_coordinate, 0, x_coordinate, 500)

            line_pen = QtGui.QPen(QtCore.Qt.black)
            line_pen.setStyle(QtCore.Qt.DashLine)
            line_pen.setWidth(1)
            p.setPen(line_pen)
            p.drawLine(self.position[0], 0, self.position[0], 500)
            p.drawLine(0, self.position[1], 1500, self.position[1])
            if self.fixed_position and (self.position[1] != self.point_position[1] or
                                        self.position[0] != self.point_position[0]):
                line_pen = QtGui.QPen(QtCore.Qt.black)
                line_pen.setStyle(QtCore.Qt.DashDotLine)
                line_pen.setWidth(1)
                p.setPen(line_pen)
                p.drawLine(self.position[0], self.position[1], self.point_position[0], self.position[1])
                p.drawLine(self.position[0], self.position[1], self.position[0], self.point_position[1])
                p.drawLine(self.point_position[0], self.position[1], self.point_position[0], self.point_position[1])
                p.drawLine(self.position[0], self.point_position[1], self.point_position[0], self.point_position[1])

        # point_line
        if self.point_line_coor:
            line_pen = QtGui.QPen(QtCore.Qt.darkBlue)
            line_pen.setStyle(QtCore.Qt.DashLine)
            line_pen.setWidth(2)
            p.setPen(line_pen)
            p.drawLine(self.point_line_coor, 0, self.point_line_coor, 500)

            if self.point_line_coor < 1350:
                p.drawStaticText(self.point_line_coor + 5, 460,
                                 QtGui.QStaticText(self.point_line_jd))
            else:
                p.drawStaticText(self.point_line_coor - 149, 460,
                                 QtGui.QStaticText(self.point_line_jd))

        # lightcurves
        if self.systems:
            amplitude_border = 0
            for i, curve in enumerate(self.lightcurves_points):
                if self.systems[i] == "A":
                    line_pen = QtGui.QPen(QtCore.Qt.blue)
                    show_visibility = False
                elif self.systems[i] == "B":
                    line_pen = QtGui.QPen(QtCore.Qt.darkGreen)
                    show_visibility = False
                elif self.systems[i] == "C":
                    line_pen = QtGui.QPen(QtCore.Qt.darkRed)
                    show_visibility = False
                elif self.systems[i] == "D":
                    line_pen = QtGui.QPen(QtCore.Qt.darkMagenta)
                    show_visibility = False
                elif self.systems[i] == "E":
                    line_pen = QtGui.QPen(QtCore.Qt.darkBlue)
                    show_visibility = False
                elif self.systems[i] == "F":
                    line_pen = QtGui.QPen(QtCore.Qt.darkCyan)
                    show_visibility = False
                else:
                    line_pen = QtGui.QPen(QtCore.Qt.black)
                    show_visibility = True
                if len(self.lightcurves_points) == 1:
                    show_visibility = True
                line_pen.setWidth(2)
                p.setPen(line_pen)
                y0 = int((curve[4] - curve[0][0] + amplitude_border) / self.lightcurves_points[0][6] * 500)
                p.drawStaticText(1350, y0, QtGui.QStaticText("Lightcurve " + self.systems[i]))
                for j in range(1, len(curve[0])):
                    if show_visibility:
                        if self.__time_period_visibility[j-1]:
                            line_pen = QtGui.QPen(QtCore.Qt.black)
                            line_pen.setWidth(2)
                            p.setPen(line_pen)
                        else:
                            line_pen = QtGui.QPen(QtCore.Qt.yellow)
                            line_pen.setWidth(2)
                            line_pen.setStyle(QtCore.Qt.DotLine)
                            p.setPen(line_pen)
                    y1 = int((curve[4] - curve[0][j] + amplitude_border) / self.lightcurves_points[0][6] * 500)
                    p.drawLine(j-1, y0, j, y1)
                    y0 = y1
                amplitude_border = amplitude_border + curve[5]
        p.end()

    def mouseMoveEvent(self, event):
        if event.y() < 501:
            self.position[0] = event.x()
            self.position[1] = event.y()
            self.update()
        self.data_was_changed()

    def data_was_changed(self):
        if self.systems:
            system_amplitude = self.lightcurves_points[0][6]
        else:
            system_amplitude = 0
        time_aria = self.time_period.jd_end() - self.time_period.jd_start() + self.lc_time_end_doublespinbox.value() + self.lc_time_start_doublespinbox.value()

        x = time_aria / 1500 * self.position[0] + self.time_period.jd_start() - self.lc_time_start_doublespinbox.value() + self.time_shift_days
        cursor_date = jd_to_date(x).strftime("%d %m %Y %H:%M")
        x = round(x, 4)
        y = system_amplitude / 500 * (500 - self.position[1])
        if y < 0:
            y = 0
        else:
            y = round(y, 3)
        self.lc_current_position_time_jd.setText(str(x))
        self.lc_current_position_amplitude.setText(str(y))
        self.lc_current_position_time_utc.setText(cursor_date)
        self.lc_object_name_info.setText(self.system_name)
        self.lc_time_area_star_info_label.setText(jd_to_date(self.time_period.jd_start() - self.lc_time_start_doublespinbox.value() + self.time_shift_days).strftime("%d %m %Y %H:%M"))
        self.lc_time_area_end_info_label.setText(jd_to_date(self.time_period.jd_end()+ self.lc_time_end_doublespinbox.value() + self.time_shift_days).strftime("%d %m %Y %H:%M"))
        if self.fixed_position:
            difference_amplitude = self.point_position[1] - self.position[1]
            distance_amplitude = str(round(1.5 / 500 * difference_amplitude, 3))
            self.lc_fixed_point_distance_amplitude.setText(distance_amplitude)
            time_distance = timedelta(seconds=int(time_aria * 57.6 * fabs((self.position[0] - self.point_position[0]))))
            self.lc_fixed_point_distance_time.setText(str(time_distance))
        else:
            self.lc_fixed_point_distance_amplitude.setText("")
            self.lc_fixed_point_distance_time.setText("")


    def set_selected_point_position(self):
        pass

    def mousePressEvent(self, event):
        if event.y() < 501:
            if event.button() == QtCore.Qt.LeftButton:
                if self.fixed_position:
                    self.clear_point_position()
                else:
                    self.point_position.append(event.x())
                    self.point_position.append(event.y())
                    x = (self.time_period.jd_end() - self.time_period.jd_start() + self.lc_time_start_doublespinbox.value() + self.lc_time_end_doublespinbox.value())/1500 * event.x() + self.time_period.jd_start() - self.lc_time_start_doublespinbox.value() + self.time_shift_days
                    cursor_date = jd_to_date(x).strftime("%d %m %Y %H:%M")
                    x = round(x, 4)
                    self.lc_fixed_point_jd.setText(str(x))
                    self.lc_fixed_point_utc.setText(cursor_date)
                    self.fixed_position = True
            if event.button() == QtCore.Qt.RightButton:
                if self.point_line_coor:
                    self.point_line_coor = None
                else:
                    self.point_line_coor = event.x()
                    time_point = (self.time_period.jd_end() - self.time_period.jd_start() + self.lc_time_start_doublespinbox.value() + self.lc_time_end_doublespinbox.value())/1500 * event.x() + self.time_period.jd_start() - self.lc_time_start_doublespinbox.value() + self.time_shift_days
                    self.point_line_jd = jd_to_date(time_point).strftime("%d %m %Y %H:%M")
            self.update()


    def clear_point_position(self):
        self.lc_fixed_point_jd.clear()
        self.lc_fixed_point_utc.clear()
        self.lc_fixed_point_distance_time.clear()
        self.lc_fixed_point_distance_amplitude.clear()
        self.fixed_position = False
        self.point_position.clear()




