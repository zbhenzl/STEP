from PyQt5.QtCore import Qt
import os
from copy import deepcopy
from math import *

import matplotlib.pyplot as plt
import numpy as np
from PyQt5.QtCore import Qt
from scipy.optimize import least_squares

from step_main_form import Popup
from tess_menu_window import *
from variables import *


class TessPhotometryEditWindow(QtWidgets.QWidget):

    def __init__(self, *args, **kwargs):
        super(TessPhotometryEditWindow, self).__init__(*args, **kwargs)

        self.printy = False
        self.fixed_position = []
        self.point_position = []
        self.position = [0, 0, 0, 0]
        self.current_amplitude = 0
        self.system_name = ""
        self.jd_start = 0
        self.jd_end = 0
        self.lightcurves_points = []
        self.steps = 1500
        self.systems = []
        self.system_without_model = []
        self.photometry = None
        self.variable_systems = []
        self.existing_pair = []
        self.offset = 0
        self.origin = False
        self.window_length = 101
        self.polyorder = 2
        self.break_tolerance = 5
        self.niters = 3
        self.sigma = 3
        self.third_light = 0
        self.sector_index = 0
        self.clear_lightcurve_parameters()
        self.model_changed = False
        self.current_model = None
        self.forbidden_time_list = []
        self.width_prim_fit = None
        self.e0_prim_fit = None
        self.width_sec_fit = None
        self.e0_sec_fit = None
        self.trend_list = []
        self.visible_part_of_trend_list = []
        self.visible_part_of_trend_list_altitude = []


        self.setWindowTitle("TESS Photometry Edit Window")
        self.setWindowIcon(QtGui.QIcon("star--exclamation.png"))
        self.setMouseTracking(True)
        self.setMinimumWidth(1000)
        self.setMinimumHeight(500)
        self.side_panel_width = 175
        self.down_panel_width = 250
        self.graph_width = self.width() - self.side_panel_width
        self.graph_height = self.height() - self.down_panel_width

        self.lc_current_position_time_jd = "0"
        self.lc_current_position_amplitude = "0"
        self.lc_current_position_time_utc = "1.1.1900"
        self.lc_object_name_info = "Amplitude"
        self.__build()

    def __build(self):
        if self.printy:
            print("Tess_photometry_edit_window, build")
        # widgets and layouts
        self.lc_time_area_star_info_label = QtWidgets.QLabel("")
        self.lc_time_area_star_info_label.setFixedWidth(85)
        self.lc_time_area_end_info_label = QtWidgets.QLabel("")
        self.lc_time_area_end_info_label.setFixedWidth(85)
        self.third_light_slider = QtWidgets.QSlider(Qt.Horizontal)
        self.third_light_slider.setMinimum(-1000)
        self.third_light_slider.setMaximum(1000)
        self.offset_slider = QtWidgets.QSlider(Qt.Horizontal)
        self.offset_slider.setMinimum(-1000)
        self.offset_slider.setMaximum(1000)
        self.start_slider = QtWidgets.QSlider(Qt.Horizontal)
        self.end_slider = QtWidgets.QSlider(Qt.Horizontal)
        self.model_slider = QtWidgets.QSlider(Qt.Horizontal)
        self.offset_slider.setMinimum(-10000)
        self.offset_slider.setMaximum(10000)

        self.fine_sliders_chechkbox = QtWidgets.QCheckBox("Fine sliders")
        self.quick_display_combobox = QtWidgets.QComboBox()
        self.quick_display_combobox.addItems(["1", "Full view", "0.5", "1.5", "2", "3"])
        self.quick_display_combobox.setCurrentIndex(0)

        self.home_pushbutton = QtWidgets.QPushButton("Home")
        self.forward = QtWidgets.QPushButton("Forward")
        self.backward = QtWidgets.QPushButton("Backward")
        sector_index_label = QtWidgets.QLabel("Sector:")
        third_label = QtWidgets.QLabel("Third light: ")
        offset_label = QtWidgets.QLabel("Offset: ")
        self.third_button = QtWidgets.QPushButton("Set Third Light")
        self.offset_button = QtWidgets.QPushButton("Set Offset")
        self.save_lc_button = QtWidgets.QPushButton("SAVE LC")
        self.save_final_model_button = QtWidgets.QPushButton("SAVE MODEL")
        self.save_model_button = QtWidgets.QPushButton("Keep")
        self.other_data_button = QtWidgets.QPushButton("Input other data")
        self.sector_index_combobox = QtWidgets.QComboBox()
        self.model_mag0_doulespinbox = QtWidgets.QDoubleSpinBox(decimals=7)
        self.model_sec_phase_doulespinbox = QtWidgets.QDoubleSpinBox(decimals=7)
        self.model_a_pri_doulespinbox = QtWidgets.QDoubleSpinBox(decimals=7)
        self.model_d_pri_doulespinbox = QtWidgets.QDoubleSpinBox(decimals=7)
        self.model_g_pri_doulespinbox = QtWidgets.QDoubleSpinBox(decimals=7)
        self.model_c_pri_doulespinbox = QtWidgets.QDoubleSpinBox(decimals=7)
        self.model_a_sec_doulespinbox = QtWidgets.QDoubleSpinBox(decimals=7)
        self.model_d_sec_doulespinbox = QtWidgets.QDoubleSpinBox(decimals=7)
        self.model_g_sec_doulespinbox = QtWidgets.QDoubleSpinBox(decimals=7)
        self.model_c_sec_doulespinbox = QtWidgets.QDoubleSpinBox(decimals=7)
        self.model_sin1_doulespinbox = QtWidgets.QDoubleSpinBox(decimals=7)
        self.model_sin2_doulespinbox = QtWidgets.QDoubleSpinBox(decimals=7)
        self.model_sin3_doulespinbox = QtWidgets.QDoubleSpinBox(decimals=7)
        self.model_cos1_doulespinbox = QtWidgets.QDoubleSpinBox(decimals=7)
        self.model_cos2_doulespinbox = QtWidgets.QDoubleSpinBox(decimals=7)
        self.model_cos3_doulespinbox = QtWidgets.QDoubleSpinBox(decimals=7)
        self.model_apsid_coef_doulespinbox = QtWidgets.QDoubleSpinBox(decimals=7)
        self.period_doublespinbox = QtWidgets.QDoubleSpinBox(decimals=7)
        self.epoch_doublespinbox = QtWidgets.QDoubleSpinBox(decimals=7)
        self.model_mag0_doulespinbox.setRange(-20, 20)
        self.model_sec_phase_doulespinbox.setRange(0, 1)
        self.model_a_pri_doulespinbox.setRange(0, 99.99)
        self.model_d_pri_doulespinbox.setRange(0, 99.99)
        self.model_g_pri_doulespinbox.setRange(-99.99, 99.99)
        self.model_c_pri_doulespinbox.setRange(-99.99, 99.99)
        self.model_a_sec_doulespinbox.setRange(0, 99.99)
        self.model_d_sec_doulespinbox.setRange(0, 99.99)
        self.model_g_sec_doulespinbox.setRange(-99.99, 99.99)
        self.model_c_sec_doulespinbox.setRange(-99.99, 99.99)
        self.model_sin1_doulespinbox.setRange(-1, 1)
        self.model_sin2_doulespinbox.setRange(-1, 1)
        self.model_sin3_doulespinbox.setRange(-1, 1)
        self.model_cos1_doulespinbox.setRange(-1, 1)
        self.model_cos2_doulespinbox.setRange(-1, 1)
        self.model_cos3_doulespinbox.setRange(-1, 1)
        self.model_apsid_coef_doulespinbox.setRange(-1, 1)
        self.period_doublespinbox.setRange(0.00001, 99.99)
        self.epoch_doublespinbox.setRange(-1, 1)

        self.model_mag0_label = QtWidgets.QRadioButton("mag0:")
        self.model_sec_phase_label = QtWidgets.QRadioButton("s_ph:")
        self.model_a_pri_label = QtWidgets.QRadioButton("a_pri:")
        self.model_d_pri_label = QtWidgets.QRadioButton("d_pri:")
        self.model_g_pri_label = QtWidgets.QRadioButton("g_pri:")
        self.model_c_pri_label = QtWidgets.QRadioButton("c_pri:")
        self.model_a_sec_label = QtWidgets.QRadioButton("a_sec:")
        self.model_d_sec_label = QtWidgets.QRadioButton("d_sec:")
        self.model_g_sec_label = QtWidgets.QRadioButton("g_sec:")
        self.model_c_sec_label = QtWidgets.QRadioButton("c_sec:")
        self.model_sin1_label = QtWidgets.QRadioButton("sin1:")
        self.model_sin2_label = QtWidgets.QRadioButton("sin2:")
        self.model_sin3_label = QtWidgets.QRadioButton("sin3:")
        self.model_cos1_label = QtWidgets.QRadioButton("cos1:")
        self.model_cos2_label = QtWidgets.QRadioButton("cos2:")
        self.model_cos3_label = QtWidgets.QRadioButton("cos3:")
        self.model_apsid_coef_label = QtWidgets.QRadioButton("ap_c:")
        self.model_period_label = QtWidgets.QRadioButton("P(d):")
        self.model_epoch_label = QtWidgets.QRadioButton("E0(+/-):")
        self.model_a = QtWidgets.QRadioButton("Pair A")
        self.model_a.setChecked(True)
        self.visible_a = QtWidgets.QCheckBox("")
        self.model_b = QtWidgets.QRadioButton("Pair B")
        self.visible_b = QtWidgets.QCheckBox("")
        self.model_c = QtWidgets.QRadioButton("Pair C")
        self.visible_c = QtWidgets.QCheckBox("")
        self.model_d = QtWidgets.QRadioButton("Pair D")
        self.visible_d = QtWidgets.QCheckBox("")
        self.model_e = QtWidgets.QRadioButton("Pair E")
        self.visible_e = QtWidgets.QCheckBox("")
        self.model_f = QtWidgets.QRadioButton("Pair F")
        self.visible_f = QtWidgets.QCheckBox("")
        self.all = QtWidgets.QCheckBox("All")
        self.residua = QtWidgets.QCheckBox("Residua")
        self.trend = QtWidgets.QCheckBox("Trend")
        self.origin_detrended_combobox = QtWidgets.QComboBox()
        self.origin_detrended_combobox.addItems(["Original", "Detrended"])
        self.window_length_combobox = QtWidgets.QComboBox()
        self.window_length_combobox.addItems(["101", "201", "301", "401", "501", "601", "701", "801", "901", "1001",
                                              "1101", "1201", "1301", "1401", "1501", "1601", "1701", "1801", "1901",
                                              "2001", "2101", "2201", "2301", "2401", "2501", "2601", "2701", "2801",
                                              "2901"])
        self.window_length_combobox.setCurrentText("101")
        self.polyorder_combobox = QtWidgets.QComboBox()
        self.break_tolerance_combobox = QtWidgets.QComboBox()
        self.niters_combobox = QtWidgets.QComboBox()
        self.sigma_combobox = QtWidgets.QComboBox()
        for i in range(1, 101):
            self.polyorder_combobox.addItem(str(i))
            self.break_tolerance_combobox.addItem(str(i))
            self.niters_combobox.addItem(str(i))
            self.sigma_combobox.addItem(str(i))
        self.polyorder_combobox.setCurrentText("2")
        self.break_tolerance_combobox.setCurrentText("5")
        self.niters_combobox.setCurrentText("3")
        self.sigma_combobox.setCurrentText("3")
        self.model_back_button = QtWidgets.QPushButton("Back")
        self.action_button = QtWidgets.QPushButton("Delete")
        self.action_combobox = QtWidgets.QComboBox()
        self.action_combobox.addItems(["Delete Point", "Delete trend", "D(prim)", "D(sec)",  "d(prim)", "d(sec)", "Range(prim)",
                                       "Range(sec)",  "Amp(prim)", "Amp(sec)"])

        self.models_groupbox = QtWidgets.QGroupBox("Model")
        self.models_groupbox.setFixedWidth(150)
        models_layout = QtWidgets.QFormLayout()
        self.models_groupbox.setLayout(models_layout)
        self.residua_amplitude_label = QtWidgets.QLabel("")
        models_layout.addRow(QtWidgets.QLabel("Model"), QtWidgets.QLabel("Visible"))
        models_layout.addRow(self.model_a, self.visible_a)
        models_layout.addRow(self.model_b, self.visible_b)
        models_layout.addRow(self.model_c, self.visible_c)
        models_layout.addRow(self.model_d, self.visible_d)
        models_layout.addRow(self.model_e, self.visible_e)
        models_layout.addRow(self.model_f, self.visible_f)
        models_layout.addRow(self.residua, self.trend)

        self.model_parametr_groupbox = QtWidgets.QGroupBox("Model parametrs")
        self.model_parametr_groupbox.setFixedWidth(160)
        model_parametr_layout = QtWidgets.QFormLayout()
        self.model_parametr_groupbox.setLayout(model_parametr_layout)
        model_parametr_layout.addRow(self.model_mag0_label, self.model_mag0_doulespinbox)
        model_parametr_layout.addRow(self.model_sec_phase_label, self.model_sec_phase_doulespinbox)
        model_parametr_layout.addRow(self.model_a_pri_label, self.model_a_pri_doulespinbox)
        model_parametr_layout.addRow(self.model_d_pri_label, self.model_d_pri_doulespinbox)
        model_parametr_layout.addRow(self.model_g_pri_label, self.model_g_pri_doulespinbox)
        model_parametr_layout.addRow(self.model_c_pri_label, self.model_c_pri_doulespinbox)
        model_parametr_layout.addRow(self.model_a_sec_label, self.model_a_sec_doulespinbox)
        model_parametr_layout.addRow(self.model_d_sec_label, self.model_d_sec_doulespinbox)
        model_parametr_layout.addRow(self.model_g_sec_label, self.model_g_sec_doulespinbox)
        model_parametr_layout.addRow(self.model_c_sec_label, self.model_c_sec_doulespinbox)
        model_parametr_layout.addRow(self.model_sin1_label, self.model_sin1_doulespinbox)
        model_parametr_layout.addRow(self.model_sin2_label, self.model_sin2_doulespinbox)
        model_parametr_layout.addRow(self.model_sin3_label, self.model_sin3_doulespinbox)
        model_parametr_layout.addRow(self.model_cos1_label, self.model_cos1_doulespinbox)
        model_parametr_layout.addRow(self.model_cos2_label, self.model_cos2_doulespinbox)
        model_parametr_layout.addRow(self.model_cos3_label, self.model_cos3_doulespinbox)
        model_parametr_layout.addRow(self.model_apsid_coef_label, self.model_apsid_coef_doulespinbox)
        model_parametr_layout.addRow(self.model_period_label, self.period_doublespinbox)
        model_parametr_layout.addRow(self.model_epoch_label, self.epoch_doublespinbox)
        self.info_groupbox = QtWidgets.QGroupBox("Set parameters")
        info_layout = QtWidgets.QGridLayout()
        self.info_groupbox.setLayout(info_layout)
        info_layout.addWidget(QtWidgets.QLabel("Period start:"), 0, 0)
        info_layout.addWidget(self.start_slider, 0, 1, 1, 17)
        info_layout.addWidget(self.lc_time_area_star_info_label, 0, 18, 1, 2)

        info_layout.addWidget(QtWidgets.QLabel("Period end:"), 1, 0)
        info_layout.addWidget(self.end_slider, 1, 1, 1, 17)
        info_layout.addWidget(self.lc_time_area_end_info_label, 1, 18, 1, 2)

        info_layout.addWidget(third_label, 2, 0)
        info_layout.addWidget(self.third_light_slider, 2, 1, 1, 17)
        info_layout.addWidget(self.third_button, 2, 18, 1, 2)

        info_layout.addWidget(offset_label, 3, 0)
        info_layout.addWidget(self.offset_slider, 3, 1, 1, 17)
        info_layout.addWidget(self.offset_button, 3, 18, 1, 2)

        info_layout.addWidget(self.backward, 4, 0)
        info_layout.addWidget(self.forward, 4, 1)
        info_layout.addWidget(self.home_pushbutton, 4, 2)
        #info_layout.addWidget(self.other_data_button, 4, 6)
        info_layout.addWidget(QtWidgets.QLabel("Model:"), 4, 3)
        info_layout.addWidget(self.model_slider, 4, 4, 1, 14)
        info_layout.addWidget(self.model_back_button, 4, 18, 1, 1)
        info_layout.addWidget(self.save_model_button, 4, 19, 1, 1)


        info_layout.addWidget(self.origin_detrended_combobox, 5, 0)
        info_layout.addWidget(QtWidgets.QLabel("Window length:"), 5, 1)
        info_layout.addWidget(self.window_length_combobox, 5, 2)
        info_layout.addWidget(QtWidgets.QLabel("Polyorder:"), 5, 3)
        info_layout.addWidget(self.polyorder_combobox, 5, 4)
        info_layout.addWidget(QtWidgets.QLabel("Break toler.:"), 5, 5)
        info_layout.addWidget(self.break_tolerance_combobox, 5, 6)
        info_layout.addWidget(QtWidgets.QLabel("Niters:"), 5, 7)
        info_layout.addWidget(self.niters_combobox, 5, 8)
        info_layout.addWidget(QtWidgets.QLabel("Sigma:"), 5, 9)
        info_layout.addWidget(self.sigma_combobox, 5, 10)
        info_layout.addWidget(sector_index_label, 5, 11)
        info_layout.addWidget(self.sector_index_combobox, 5, 12)
        info_layout.addWidget(self.action_combobox, 5, 13)
        info_layout.addWidget(self.action_button, 5, 14)
        info_layout.addWidget(self.save_lc_button, 5, 18)
        info_layout.addWidget(self.save_final_model_button, 5, 19)

        self.model_amplitude_label = QtWidgets.QLabel()
        self.data_amplitude_label = QtWidgets.QLabel()
        self.area_hours = QtWidgets.QLabel()
        self.area_amp_label = QtWidgets.QLabel()
        self.area_pri_label = QtWidgets.QLabel("")
        self.area_sec_label = QtWidgets.QLabel()

        info_layout.addWidget(QtWidgets.QLabel("Quick display:"), 6, 0)
        info_layout.addWidget(self.quick_display_combobox, 6, 1)
        info_layout.addWidget(QtWidgets.QLabel("data point/graph column"), 6, 2, 1, 2)
        info_layout.addWidget(self.fine_sliders_chechkbox, 6, 4, 1, 2)

        info_layout.addWidget(QtWidgets.QLabel("Model amp:"), 7, 0)
        info_layout.addWidget(self.model_amplitude_label, 7, 1)
        info_layout.addWidget(QtWidgets.QLabel("Data amp:"), 7, 2)
        info_layout.addWidget(self.data_amplitude_label, 7, 3, 1, 2)
        info_layout.addWidget(QtWidgets.QLabel("Area(mag):"), 7, 5)
        info_layout.addWidget(self.area_amp_label, 7, 6)
        info_layout.addWidget(QtWidgets.QLabel("Area(h):"), 7, 7)
        info_layout.addWidget(self.area_hours, 7, 8)
        info_layout.addWidget(QtWidgets.QLabel("Primary"), 7, 9)
        info_layout.addWidget(self.area_pri_label, 7, 10, 1, 3)
        info_layout.addWidget(QtWidgets.QLabel("Secondary:"), 7, 13)
        info_layout.addWidget(self.area_sec_label, 7, 14, 1, 3)
        info_layout.addWidget(QtWidgets.QLabel("Residua(%):"), 7, 18)
        info_layout.addWidget(self.residua_amplitude_label, 7, 19)

        info_graf_layout = QtWidgets.QVBoxLayout()
        info_graf_layout.addStretch()
        info_graf_layout.addWidget(self.info_groupbox)

        self.info_model_column_layout = QtWidgets.QVBoxLayout()
        self.info_model_column_layout.addWidget(self.models_groupbox)
        self.info_model_column_layout.addWidget(self.model_parametr_groupbox)
        self.info_model_column_layout.addStretch()

        lc_window_layout = QtWidgets.QHBoxLayout()  # main layout
        self.setLayout(lc_window_layout)
        lc_window_layout.addLayout(info_graf_layout)
        lc_window_layout.addLayout(self.info_model_column_layout)

        self.start_slider.setMinimum(0)
        self.end_slider.setMinimum(1)
        self.start_slider.setMaximum(999)
        self.end_slider.setMaximum(1000)
        self.start_slider.setValue(0)
        self.end_slider.setValue(1000)

    def set_model_slider_range(self):
        if self.printy:
            print("Tess_photometry_edit_window, set_model_slider_range")

        self.connect_window(False)
        if self.fine_sliders_chechkbox.isChecked():
            fine_sliders_coefficient = 100000000
        else:
            fine_sliders_coefficient = 10000000

        if self.model_mag0_label.isChecked():
            self.model_slider.setRange(int(self.model_mag0_doulespinbox.value() * fine_sliders_coefficient) - 1000000,
                                       int(self.model_mag0_doulespinbox.value() * fine_sliders_coefficient) + 1000000)
            self.model_slider.setValue(int(self.model_mag0_doulespinbox.value() * fine_sliders_coefficient))
        elif self.model_sec_phase_label.isChecked():
            range_minimum = int(self.model_sec_phase_doulespinbox.value() * fine_sliders_coefficient) - 1000000
            range_maximum = int(self.model_sec_phase_doulespinbox.value() * fine_sliders_coefficient) + 1000000
            if range_minimum < 0:
                range_minimum = 0
            if range_maximum > fine_sliders_coefficient:
                range_maximum = fine_sliders_coefficient
            self.model_slider.setRange(range_minimum, range_maximum)
            self.model_slider.setValue(int(self.model_sec_phase_doulespinbox.value() * fine_sliders_coefficient))
        elif self.model_a_pri_label.isChecked():
            self.model_slider.setRange(int(self.model_a_pri_doulespinbox.value() * fine_sliders_coefficient) - 1000000,
                                       int(self.model_a_pri_doulespinbox.value() * fine_sliders_coefficient) + 1000000)
            self.model_slider.setValue(int(self.model_a_pri_doulespinbox.value() * fine_sliders_coefficient))
        elif self.model_d_pri_label.isChecked():
            self.model_slider.setRange(int(self.model_d_pri_doulespinbox.value() * fine_sliders_coefficient) - 50000,
                                       int(self.model_d_pri_doulespinbox.value() * fine_sliders_coefficient) + 50000)
            self.model_slider.setValue(int(self.model_d_pri_doulespinbox.value() * fine_sliders_coefficient))
        elif self.model_g_pri_label.isChecked():
            self.model_slider.setRange(int(self.model_g_pri_doulespinbox.value() * fine_sliders_coefficient) - 1000000,
                                       int(self.model_g_pri_doulespinbox.value() * fine_sliders_coefficient) + 1000000)
            self.model_slider.setValue(int(self.model_g_pri_doulespinbox.value() * fine_sliders_coefficient))
        elif self.model_c_pri_label.isChecked():
            self.model_slider.setRange(int(self.model_c_pri_doulespinbox.value() * fine_sliders_coefficient) - 1000000,
                                       int(self.model_c_pri_doulespinbox.value() * fine_sliders_coefficient) + 1000000)
            self.model_slider.setValue(int(self.model_c_pri_doulespinbox.value() * fine_sliders_coefficient))
        elif self.model_a_sec_label.isChecked():
            self.model_slider.setRange(int(self.model_a_sec_doulespinbox.value() * fine_sliders_coefficient) - 1000000,
                                       int(self.model_a_sec_doulespinbox.value() * fine_sliders_coefficient) + 1000000)
            self.model_slider.setValue(int(self.model_a_sec_doulespinbox.value() * fine_sliders_coefficient))
        elif self.model_d_sec_label.isChecked():
            self.model_slider.setRange(int(self.model_d_sec_doulespinbox.value() * fine_sliders_coefficient) - 50000,
                                       int(self.model_d_sec_doulespinbox.value() * fine_sliders_coefficient) + 50000)
            self.model_slider.setValue(int(self.model_d_sec_doulespinbox.value() * fine_sliders_coefficient))
        elif self.model_g_sec_label.isChecked():
            self.model_slider.setRange(int(self.model_g_sec_doulespinbox.value() * fine_sliders_coefficient) - 1000000,
                                       int(self.model_g_sec_doulespinbox.value() * fine_sliders_coefficient) + 1000000)
            self.model_slider.setValue(int(self.model_g_sec_doulespinbox.value() * fine_sliders_coefficient))
        elif self.model_c_sec_label.isChecked():
            self.model_slider.setRange(int(self.model_c_sec_doulespinbox.value() * fine_sliders_coefficient) - 1000000,
                                       int(self.model_c_sec_doulespinbox.value() * fine_sliders_coefficient) + 1000000)
            self.model_slider.setValue(int(self.model_c_sec_doulespinbox.value() * fine_sliders_coefficient))
        elif self.model_sin1_label.isChecked():
            range_minimum = int(self.model_sin1_doulespinbox.value() * fine_sliders_coefficient) - 1000000
            range_maximum = int(self.model_sin1_doulespinbox.value() * fine_sliders_coefficient) + 1000000
            if range_minimum < -fine_sliders_coefficient:
                range_minimum = -fine_sliders_coefficient
            if range_maximum > fine_sliders_coefficient:
                range_maximum = fine_sliders_coefficient
            self.model_slider.setRange(range_minimum, range_maximum)
            self.model_slider.setValue(int(self.model_sin1_doulespinbox.value() * fine_sliders_coefficient))
        elif self.model_sin2_label.isChecked():
            range_minimum = int(self.model_sin2_doulespinbox.value() * fine_sliders_coefficient) - 1000000
            range_maximum = int(self.model_sin2_doulespinbox.value() * fine_sliders_coefficient) + 1000000
            if range_minimum < -fine_sliders_coefficient:
                range_minimum = -fine_sliders_coefficient
            if range_maximum > fine_sliders_coefficient:
                range_maximum = fine_sliders_coefficient
            self.model_slider.setRange(range_minimum, range_maximum)
            self.model_slider.setValue(int(self.model_sin2_doulespinbox.value() * fine_sliders_coefficient))
        elif self.model_sin3_label.isChecked():
            range_minimum = int(self.model_sin3_doulespinbox.value() * fine_sliders_coefficient) - 1000000
            range_maximum = int(self.model_sin3_doulespinbox.value() * fine_sliders_coefficient) + 1000000
            if range_minimum < -fine_sliders_coefficient:
                range_minimum = -fine_sliders_coefficient
            if range_maximum > fine_sliders_coefficient:
                range_maximum = fine_sliders_coefficient
            self.model_slider.setRange(range_minimum, range_maximum)
            self.model_slider.setValue(int(self.model_sin3_doulespinbox.value() * fine_sliders_coefficient))
        elif self.model_cos1_label.isChecked():
            range_minimum = int(self.model_cos1_doulespinbox.value() * fine_sliders_coefficient) - 1000000
            range_maximum = int(self.model_cos1_doulespinbox.value() * fine_sliders_coefficient) + 1000000
            if range_minimum < -fine_sliders_coefficient:
                range_minimum = -fine_sliders_coefficient
            if range_maximum > fine_sliders_coefficient:
                range_maximum = fine_sliders_coefficient
            self.model_slider.setRange(range_minimum, range_maximum)
            self.model_slider.setValue(int(self.model_cos1_doulespinbox.value() * fine_sliders_coefficient))
        elif self.model_cos2_label.isChecked():
            range_minimum = int(self.model_cos2_doulespinbox.value() * fine_sliders_coefficient) - 1000000
            range_maximum = int(self.model_cos2_doulespinbox.value() * fine_sliders_coefficient) + 1000000
            if range_minimum < -fine_sliders_coefficient:
                range_minimum = -fine_sliders_coefficient
            if range_maximum > fine_sliders_coefficient:
                range_maximum = fine_sliders_coefficient
            self.model_slider.setRange(range_minimum, range_maximum)
            self.model_slider.setValue(int(self.model_cos2_doulespinbox.value() * fine_sliders_coefficient))
        elif self.model_cos3_label.isChecked():
            range_minimum = int(self.model_cos3_doulespinbox.value() * fine_sliders_coefficient) - 1000000
            range_maximum = int(self.model_cos3_doulespinbox.value() * fine_sliders_coefficient) + 1000000
            if range_minimum < -fine_sliders_coefficient:
                range_minimum = -fine_sliders_coefficient
            if range_maximum > fine_sliders_coefficient:
                range_maximum = fine_sliders_coefficient
            self.model_slider.setRange(range_minimum, range_maximum)
            self.model_slider.setValue(int(self.model_cos3_doulespinbox.value() * fine_sliders_coefficient))
        elif self.model_apsid_coef_label.isChecked():
            self.model_slider.setRange(int(self.model_apsid_coef_doulespinbox.value() * fine_sliders_coefficient) - 10000, int(self.model_apsid_coef_doulespinbox.value() * fine_sliders_coefficient) + 10000)
            self.model_slider.setValue(int(self.model_apsid_coef_doulespinbox.value() * fine_sliders_coefficient))
        elif self.model_period_label.isChecked():
            self.model_slider.setRange(int(self.period_doublespinbox.value() * fine_sliders_coefficient) - 1000, int(self.period_doublespinbox.value() * fine_sliders_coefficient) + 1000)
            self.model_slider.setValue(int(self.period_doublespinbox.value() * fine_sliders_coefficient))
        elif self.model_epoch_label.isChecked():
            self.model_slider.setRange(int(float(self.epoch_doublespinbox.text()) * fine_sliders_coefficient) - 100000, int(float(self.epoch_doublespinbox.text()) * fine_sliders_coefficient) + 100000)
            self.model_slider.setValue(int(float(self.epoch_doublespinbox.text()) * fine_sliders_coefficient))
        else:
            pass
        self.connect_window(True)

    def origin_changed(self):
        if self.printy:
            print("Tess_photometry_edit_window, origin_changed")


        if self.origin_detrended_combobox.currentIndex() == 0:
            self.origin = False
            if self.action_combobox.currentText() == "Delete trend":
                self.action_button.setText("Delete trend")
        else:
            self.origin = True
            if self.action_combobox.currentText() == "Delete trend":
                self.action_button.setText("None")
        self.clear_lightcurve_parameters()
        self.lightcurve_and_model_was_changed()
        self.update()

    def window_length_changed(self):
        if self.printy:
            print("Tess_photometry_edit_window, window_length_changed")

        self.window_length = int(self.window_length_combobox.currentText())
        self.clear_lightcurve_parameters()
        self.lightcurve_and_model_was_changed()
        self.update()

    def polyorder_changed(self):
        if self.printy:
            print("Tess_photometry_edit_window, polyorder_changed")

        self.polyorder = int(self.polyorder_combobox.currentText())
        self.clear_lightcurve_parameters()
        self.lightcurve_and_model_was_changed()
        self.update()

    def break_tolerance_changed(self):
        if self.printy:
            print("Tess_photometry_edit_window, break_tolerance_changed")

        self.break_tolerance = int(self.break_tolerance_combobox.currentText())
        self.clear_lightcurve_parameters()
        self.lightcurve_and_model_was_changed()
        self.update()

    def quick_display_was_changed(self):
        self.clear_lightcurve_parameters()
        self.lightcurve_and_model_was_changed()
        self.update()

    def niters_changed(self):
        if self.printy:
            print("Tess_photometry_edit_window, niters_changed")

        self.niters = int(self.niters_combobox.currentText())
        self.clear_lightcurve_parameters()
        self.lightcurve_and_model_was_changed()
        self.update()

    def sigma_changed(self):
        if self.printy:
            print("Tess_photometry_edit_window, sigma_changed")

        self.sigma = int(self.sigma_combobox.currentText())
        self.clear_lightcurve_parameters()
        self.lightcurve_and_model_was_changed()
        self.update()

    def change_graph_width(self, new):
        if self.printy:
            print("Tess_photometry_edit_window, change_graph_width")

        self.graph_width = new

    def change_graph_height(self, new):
        if self.printy:
            print("Tess_photometry_edit_window, change_graph_height")

        self.graph_height = new

    def change_variable_systems(self, new):
        if self.printy:
            print("Tess_photometry_edit_window, change_variable_systems")
        self.variable_systems = []
        if new:
            for variable in new:
                new_variable = deepcopy(variable)
                self.variable_systems.append(new_variable)

    def change_offset(self, new):
        if self.printy:
            print("Tess_photometry_edit_window, change_offset")

        self.offset = new

    def change_existing_pair(self, new):
        if self.printy:
            print("Tess_photometry_edit_window, change_existing_pair")

        self.existing_pair = new

    def change_photometry(self, new):
        if self.printy:
            print("Tess_photometry_edit_window, change_photometry")
        lightcurves = []
        for lightcurve in new.lightcurves():
            lightcurves.append(lightcurve)
        coor = new.coor()
        var_id = new.var_id()
        name = new.name()
        mag = new.mag()
        period = new.period()
        epoch = new.epoch()
        if not epoch:
            epoch = "2460000"
        tess_cut_set = []
        for tes_cut in new.tess_cut_set():
            tess_cut_set.append(tes_cut)
        sectors = []
        for sector in new.sectors():
            sectors.append(sector)
        x = new.x()
        y = new.y()
        mx = new.mx()
        my = new.my()
        m = new.m()
        n = new.n()
        cut_size = new.cut_size()
        description = new.description()
        pair = new.pair()
        if not pair:
            pair = "X"
        name_origin = new.name_origin()
        from tess_menu_window import TessCutInfo
        self.photometry = TessCutInfo(lightcurves, coor, var_id, name, mag, period, epoch, tess_cut_set, sectors, x, y,
                                      mx, my, m, n, cut_size, description, pair, name_origin)

    def change_jd_start(self, new):
        if self.printy:
            print("Tess_photometry_edit_window, change_jd_start")

        self.jd_start = new

    def change_jd_end(self, new):
        if self.printy:
            print("Tess_photometry_edit_window, change_jd_end")

        self.jd_end = new

    def setup(self):
        if self.printy:
            print("Tess_photometry_edit_window, setup")

        from step_application import root
        self.variables = root.database.variables
        self.connect_window(True)
        self.tess_menu_window = root.tess_menu_window
        self.tess_menu_window_setting = root.tess_menu_window_setting

    def connect_window(self, on: bool):
        if self.printy:
            print("Tess_photometry_edit_window, connect_window")

        if on:
            self.start_slider.valueChanged.connect(self.start)
            self.end_slider.valueChanged.connect(self.end)
            self.third_light_slider.valueChanged.connect(self.third_light_changed)
            self.offset_slider.valueChanged.connect(self.offset_changed)
            self.home_pushbutton.clicked.connect(self.home)
            self.offset_button.clicked.connect(self.set_offset)
            self.third_button.clicked.connect(self.set_third_light)
            self.forward.clicked.connect(self.go_forward)
            self.backward.clicked.connect(self.go_backward)
            self.sector_index_combobox.currentTextChanged.connect(self.change_sector)
            self.origin_detrended_combobox.currentTextChanged.connect(self.origin_changed)
            self.visible_a.clicked.connect(self.pair_visibility_changed)
            self.visible_b.clicked.connect(self.pair_visibility_changed)
            self.visible_c.clicked.connect(self.pair_visibility_changed)
            self.visible_d.clicked.connect(self.pair_visibility_changed)
            self.visible_e.clicked.connect(self.pair_visibility_changed)
            self.visible_f.clicked.connect(self.pair_visibility_changed)
            self.all.clicked.connect(self.pair_visibility_changed)
            self.residua.clicked.connect(self.pair_visibility_changed)
            self.trend.clicked.connect(self.pair_visibility_changed)
            self.window_length_combobox.currentTextChanged.connect(self.window_length_changed)
            self.polyorder_combobox.currentTextChanged.connect(self.polyorder_changed)
            self.break_tolerance_combobox.currentTextChanged.connect(self.break_tolerance_changed)
            self.niters_combobox.currentTextChanged.connect(self.niters_changed)
            self.sigma_combobox.currentTextChanged.connect(self.sigma_changed)
            self.model_mag0_doulespinbox = QtWidgets.QDoubleSpinBox(decimals=8)
            self.model_sec_phase_doulespinbox.valueChanged.connect(self.model_parameters_was_changed)
            self.model_a_pri_doulespinbox.valueChanged.connect(self.model_parameters_was_changed)
            self.model_d_pri_doulespinbox.valueChanged.connect(self.model_parameters_was_changed)
            self.model_g_pri_doulespinbox.valueChanged.connect(self.model_parameters_was_changed)
            self.model_c_pri_doulespinbox.valueChanged.connect(self.model_parameters_was_changed)
            self.model_a_sec_doulespinbox.valueChanged.connect(self.model_parameters_was_changed)
            self.model_d_sec_doulespinbox.valueChanged.connect(self.model_parameters_was_changed)
            self.model_g_sec_doulespinbox.valueChanged.connect(self.model_parameters_was_changed)
            self.model_c_sec_doulespinbox.valueChanged.connect(self.model_parameters_was_changed)
            self.model_sin1_doulespinbox.valueChanged.connect(self.model_parameters_was_changed)
            self.model_sin2_doulespinbox.valueChanged.connect(self.model_parameters_was_changed)
            self.model_sin3_doulespinbox.valueChanged.connect(self.model_parameters_was_changed)
            self.model_cos1_doulespinbox.valueChanged.connect(self.model_parameters_was_changed)
            self.model_cos2_doulespinbox.valueChanged.connect(self.model_parameters_was_changed)
            self.model_cos3_doulespinbox.valueChanged.connect(self.model_parameters_was_changed)
            self.model_apsid_coef_doulespinbox.valueChanged.connect(self.model_parameters_was_changed)
            self.period_doublespinbox.valueChanged.connect(self.model_parameters_was_changed)
            self.epoch_doublespinbox.valueChanged.connect(self.model_parameters_was_changed)
            self.model_slider.valueChanged.connect(self.model_was_changed)
            self.model_mag0_label.clicked.connect(self.set_model_slider_range)
            self.model_sec_phase_label.clicked.connect(self.set_model_slider_range)
            self.model_a_pri_label.clicked.connect(self.set_model_slider_range)
            self.model_d_pri_label.clicked.connect(self.set_model_slider_range)
            self.model_g_pri_label.clicked.connect(self.set_model_slider_range)
            self.model_c_pri_label.clicked.connect(self.set_model_slider_range)
            self.model_a_sec_label.clicked.connect(self.set_model_slider_range)
            self.model_d_sec_label.clicked.connect(self.set_model_slider_range)
            self.model_g_sec_label.clicked.connect(self.set_model_slider_range)
            self.model_c_sec_label.clicked.connect(self.set_model_slider_range)
            self.model_sin1_label.clicked.connect(self.set_model_slider_range)
            self.model_sin2_label.clicked.connect(self.set_model_slider_range)
            self.model_sin3_label.clicked.connect(self.set_model_slider_range)
            self.model_cos1_label.clicked.connect(self.set_model_slider_range)
            self.model_cos2_label.clicked.connect(self.set_model_slider_range)
            self.model_cos3_label.clicked.connect(self.set_model_slider_range)
            self.model_apsid_coef_label.clicked.connect(self.set_model_slider_range)
            self.model_period_label.clicked.connect(self.set_model_slider_range)
            self.model_epoch_label.clicked.connect(self.set_model_slider_range)
            self.model_a.clicked.connect(self.change_model)
            self.model_b.clicked.connect(self.change_model)
            self.model_c.clicked.connect(self.change_model)
            self.model_d.clicked.connect(self.change_model)
            self.model_e.clicked.connect(self.change_model)
            self.model_f.clicked.connect(self.change_model)
            self.save_model_button.clicked.connect(self.save_model)
            self.model_back_button.clicked.connect(self.set_model_parameter_back)
            self.action_button.clicked.connect(self.make_action)
            self.save_lc_button.clicked.connect(self.save_lc_data)
            self.save_final_model_button.clicked.connect(self.save_model_changes_into_variable)
            self.action_combobox.currentTextChanged.connect(self.action_combobox_was_changed)
            self.fine_sliders_chechkbox.clicked.connect(self.fine_sliders_checkbox_was_checked)
            self.quick_display_combobox.currentTextChanged.connect(self.quick_display_was_changed)
        else:
            self.home_pushbutton.disconnect()
            self.offset_button.disconnect()
            self.forward.disconnect()
            self.backward.disconnect()
            self.sector_index_combobox.disconnect()
            self.origin_detrended_combobox.disconnect()
            self.visible_a.disconnect()
            self.visible_b.disconnect()
            self.visible_c.disconnect()
            self.visible_d.disconnect()
            self.visible_e.disconnect()
            self.visible_f.disconnect()
            self.all.disconnect()
            self.residua.disconnect()
            self.trend.disconnect()
            self.window_length_combobox.disconnect()
            self.polyorder_combobox.disconnect()
            self.break_tolerance_combobox.disconnect()
            self.niters_combobox.disconnect()
            self.sigma_combobox.disconnect()
            self.start_slider.disconnect()
            self.end_slider.disconnect()
            self.third_light_slider.disconnect()
            self.offset_slider.disconnect()
            self.model_sec_phase_doulespinbox.disconnect()
            self.model_a_pri_doulespinbox.disconnect()
            self.model_d_pri_doulespinbox.disconnect()
            self.model_g_pri_doulespinbox.disconnect()
            self.model_c_pri_doulespinbox.disconnect()
            self.model_a_sec_doulespinbox.disconnect()
            self.model_d_sec_doulespinbox.disconnect()
            self.model_g_sec_doulespinbox.disconnect()
            self.model_c_sec_doulespinbox.disconnect()
            self.model_sin1_doulespinbox.disconnect()
            self.model_sin2_doulespinbox.disconnect()
            self.model_sin3_doulespinbox.disconnect()
            self.model_cos1_doulespinbox.disconnect()
            self.model_cos2_doulespinbox.disconnect()
            self.model_cos3_doulespinbox.disconnect()
            self.model_apsid_coef_doulespinbox.disconnect()
            self.period_doublespinbox.disconnect()
            self.model_slider.disconnect()
            self.model_mag0_label.disconnect()
            self.model_sec_phase_label.disconnect()
            self.model_a_pri_label.disconnect()
            self.model_d_pri_label.disconnect()
            self.model_g_pri_label.disconnect()
            self.model_c_pri_label.disconnect()
            self.model_a_sec_label.disconnect()
            self.model_d_sec_label.disconnect()
            self.model_g_sec_label.disconnect()
            self.model_c_sec_label.disconnect()
            self.model_sin1_label.disconnect()
            self.model_sin2_label.disconnect()
            self.model_sin3_label.disconnect()
            self.model_cos1_label.disconnect()
            self.model_cos2_label.disconnect()
            self.model_cos3_label.disconnect()
            self.model_apsid_coef_label.disconnect()
            self.model_period_label.disconnect()
            self.model_a.clicked.disconnect()
            self.model_b.clicked.disconnect()
            self.model_c.clicked.disconnect()
            self.model_d.clicked.disconnect()
            self.model_e.clicked.disconnect()
            self.model_f.clicked.disconnect()
            self.save_model_button.disconnect()
            self.model_back_button.disconnect()
            self.model_epoch_label.disconnect()
            self.action_button.disconnect()
            self.epoch_doublespinbox.disconnect()
            self.save_lc_button.disconnect()
            self.save_final_model_button.disconnect()
            self.action_combobox.disconnect()
            self.fine_sliders_chechkbox.disconnect()
            self.quick_display_combobox.disconnect()

    def fine_sliders_checkbox_was_checked(self):
        if self.fine_sliders_chechkbox.isChecked():
            fine_slider = 1
        else:
            fine_slider = 0.1
        self.set_model_slider_range()
        self.connect_window(False)
        self.third_light = self.third_light + self.third_light_slider.value() * fine_slider
        self.third_light_slider.setValue(0)
        self.change_offset(self.offset + self.offset_slider.value() * fine_slider / 100000)
        self.offset_slider.setValue(0)
        self.connect_window(True)

    def action_combobox_was_changed(self):
        self.trend_list = []
        self.recalibrate_trend_line()
        action_text = self.action_combobox.currentText()
        if action_text == "D(prim)":
            self.action_button.setText("Set duration")
        elif action_text == "D(sec)":
            self.action_button.setText("Set duration")
        elif action_text == "d(prim)":
            self.action_button.setText("Set duration")
        elif action_text == "d(sec)":
            self.action_button.setText("Set duration")
        elif action_text == "Amp(prim)":
            self.action_button.setText("Set amplitude")
        elif action_text == "Amp(sec)":
            self.action_button.setText("Set amplitude")
        elif action_text == "Range(prim)":
            self.action_button.setText("Set fit")
        elif action_text == "Range(sec)":
            self.action_button.setText("Set fit")
        elif action_text == "Delete trend":
            if self.origin:
                self.action_button.setText("None")
            else:
                self.action_button.setText("Delete trend")
        else:
            self.action_button.setText("Delete")

    def save_lc_data(self):
        from step_main_form import Popup
        save_window = Popup("Save data", "Do you want to save LC data?",
                            buttons="Save LC (mag), Back, Exit without save".split(","))
        save_window_result = save_window.do()
        if save_window_result == 1:
            return
        elif save_window_result == 2:
            self.close()
            return
        else:
            file_folder = self.tess_menu_window_setting.folder_files_pushbutton.text()
            if not os.path.exists(file_folder):
                mistake = Popup("Saving error",
                                "Failed to create folder\n{0}\nPlease check your permissions of fill path to existing folder.".format(
                                    file_folder),
                                buttons="OK".split(","))
                mistake.do()
                return
            sector = self.sector_index_combobox.currentText()
            new_data_file = self.photometry.name() + "_" + sector + "_TESS_MAG.txt"
            quick_display_index = self.quick_display_combobox.currentIndex()
            if quick_display_index != 1:
                self.quick_display_combobox.setCurrentIndex(1)
            try:
                aperture_star = str(int(self.photometry.mx()) * int(self.photometry.my()))
                aperture_cmp = str(int(self.photometry.cut_size())**2)
                star_name = self.photometry.var_id()
                star_mag = str(self.photometry.mag())
                coor_list = self.photometry.coor().split(" ")
                if '' in coor_list:
                    index = coor_list.index('')
                    del (coor_list[index])
                rektascenze = coor_list[0] + ":" + coor_list[1] + ":" + coor_list[2]
                declination = coor_list[3] + ":" + coor_list[4] + ":" + coor_list[5]

                metadata_text = " HJD flux flux_err\n VarAperture: {0} CmpAperture: {1} JD: heliocentric Unit: flux " \
                                "Filter: Lum\n VAR Name: {2} RA: {3} Dec: {4} Catalog: TIC CatalogId: CatalogRA: {5} " \
                                "CatalogDec: {6} CatalogMag: {7} CatalogJ-K:".format(aperture_star, aperture_cmp,
                                                                                     star_name, rektascenze,
                                                                                     declination, rektascenze,
                                                                                     declination, star_mag)
                #self.all_curve_point_set[1].append(int((jd_time - self.jd_start) / (self.jd_end - self.jd_start) * self.graph_width))
                #self.all_curve_point_set[2].append(int(self.graph_height / self.current_amplitude *
                #                                       (self.border_set[4][i] - self.border_set[2])))
                if len(self.visible_part_of_trend_list) > 1 and not self.origin:
                    t = 0
                    trend_minimum = 0
                    visible_part_of_trend_list_all_points = []
                    magnitude_list = []
                    trend_list = []
                    trend_point_jd = []
                    trend_point_y = []
                    for point in self.visible_part_of_trend_list:
                        point_jd = point[0] / self.graph_width * (self.jd_end - self.jd_start) + self.jd_start
                        trend_point_jd.append(point_jd)
                        trend_point_y.append(point[1])
                    for i, jd_point in enumerate(self.lightcurve_set[0]):
                        while jd_point >= trend_point_jd[t + 1]:
                            t = t + 1
                        jd_range = trend_point_jd[t + 1] - trend_point_jd[t]
                        jd_part_range = jd_point - trend_point_jd[t]
                        jd_part = jd_part_range / jd_range
                        altitude = trend_point_y[t + 1] - trend_point_y[t]
                        part_altitude = altitude * jd_part + trend_point_y[t]
                        if self.all_curve_point_set[2][i] - part_altitude < trend_minimum:
                            trend_minimum = self.all_curve_point_set[2][i] - part_altitude
                        visible_part_of_trend_list_all_points.append(part_altitude)
                    for j in range(len(visible_part_of_trend_list_all_points)):
                        visible_part_of_trend_list_all_points[j] = (visible_part_of_trend_list_all_points[j]
                                                                    + trend_minimum)
                        trend_list.append(visible_part_of_trend_list_all_points[j] * self.current_amplitude \
                                          / self.graph_height + self.lightcurve_set[1][j])
                        magnitude_list.append(self.lightcurve_set[1][j] + trend_list[j])
                else:
                    magnitude_list = self.lightcurve_set[1]
                    trend_list = [0] * len(self.lightcurve_set[1])

                with open(os.path.join(file_folder, new_data_file), "w", encoding="utf-8") as f:
                    if self.tess_menu_window.metadata_checkbox.isChecked():
                        f.write(metadata_text + "\n")
                    for i, jd_time in enumerate(self.lightcurve_set[0]):
                        jd_time_text = str(round(jd_time, 6))
                        mag = str(round(magnitude_list[i], 4))
                        mag_error = str(round(self.lightcurve_set[2][i], 4))
                        detrend = str(round(trend_list[i], 4))
                        radek = jd_time_text + " " + mag + " " + mag_error + " " + detrend
                        f.write(radek + "\n")
            except:
                mistake = Popup("Data saving error",
                                "Failed to create file\n{0}\n{1}\nPlease check your permissions.".format(
                                    file_folder, new_data_file), buttons="OK".split(","))
                mistake.do()
                return
            if quick_display_index != 1:
                self.quick_display_combobox.setCurrentIndex(quick_display_index)

    def save_model_changes_into_variable(self):
        save_window = Popup("Save model", "Do you want to save all model changes?",
                            buttons="Save model, Back".split(","))
        if save_window.do() == 0:
            if self.current_model:
                self.model_changed = False
                if self.current_model in self.existing_pair:
                    model_index = self.existing_pair.index(self.current_model)
                    self.variable_systems[model_index].change_mag0(self.model_mag0_doulespinbox.value())
                    self.variable_systems[model_index].change_sec_phase(self.model_sec_phase_doulespinbox.value())
                    self.variable_systems[model_index].change_a_pri(self.model_a_pri_doulespinbox.value())
                    self.variable_systems[model_index].change_d_pri(self.model_d_pri_doulespinbox.value())
                    self.variable_systems[model_index].change_g_pri(self.model_g_pri_doulespinbox.value())
                    self.variable_systems[model_index].change_c_pri(self.model_c_pri_doulespinbox.value())
                    self.variable_systems[model_index].change_a_sec(self.model_a_sec_doulespinbox.value())
                    self.variable_systems[model_index].change_d_sec(self.model_d_sec_doulespinbox.value())
                    self.variable_systems[model_index].change_g_sec(self.model_g_sec_doulespinbox.value())
                    self.variable_systems[model_index].change_c_sec(self.model_c_sec_doulespinbox.value())
                    self.variable_systems[model_index].change_a_sin1(self.model_sin1_doulespinbox.value())
                    self.variable_systems[model_index].change_a_sin2(self.model_sin2_doulespinbox.value())
                    self.variable_systems[model_index].change_a_sin3(self.model_sin3_doulespinbox.value())
                    self.variable_systems[model_index].change_a_cos1(self.model_cos1_doulespinbox.value())
                    self.variable_systems[model_index].change_a_cos2(self.model_cos2_doulespinbox.value())
                    self.variable_systems[model_index].change_a_cos3(self.model_cos3_doulespinbox.value())
                    self.variable_systems[model_index].change_apsidal_movement_correction(self.model_apsid_coef_doulespinbox.value())
                    self.variable_systems[model_index].change_period(self.period_doublespinbox.value())
                    self.variable_systems[model_index].change_epoch(self.variable_systems[model_index].epoch() +
                                                                    self.epoch_doublespinbox.value())
                    self.epoch_doublespinbox.setValue(0)
            for variable in self.variables.variables:
                for modify_variable in self.variable_systems:
                    if variable.name() == modify_variable.name() and variable.pair() == modify_variable.pair():
                        variable.change_mag0(modify_variable.mag0())
                        variable.change_sec_phase(modify_variable.sec_phase())
                        variable.change_a_pri(modify_variable.a_pri())
                        variable.change_d_pri(modify_variable.d_pri())
                        variable.change_g_pri(modify_variable.g_pri())
                        variable.change_c_pri(modify_variable.c_pri())
                        variable.change_a_sec(modify_variable.a_sec())
                        variable.change_d_sec(modify_variable.d_sec())
                        variable.change_g_sec(modify_variable.g_sec())
                        variable.change_c_sec(modify_variable.c_sec())
                        variable.change_a_sin1(modify_variable.a_sin1())
                        variable.change_a_sin2(modify_variable.a_sin2())
                        variable.change_a_sin3(modify_variable.a_sin3())
                        variable.change_a_cos1(modify_variable.a_cos1())
                        variable.change_a_cos2(modify_variable.a_cos2())
                        variable.change_a_cos3(modify_variable.a_cos3())
                        variable.change_apsidal_movement_correction(modify_variable.apsidal_movement_correction())
                        variable.change_period(modify_variable.period())
                        variable.change_epoch(modify_variable.epoch())

    def make_action(self):
        action_text = self.action_combobox.currentText()
        if self.fixed_position and self.point_position:
            if action_text == "Delete Point":
                if self.fixed_position[0] != self.point_position[0]:
                    if self.fixed_position[0] < self.point_position[0]:
                        x0 = self.fixed_position[0]
                        x1 = self.point_position[0]
                    else:
                        x1 = self.fixed_position[0]
                        x0 = self.point_position[0]
                    jd_delete_start = (self.jd_end - self.jd_start) * x0 / self.graph_width + self.jd_start
                    jd_delete_end = (self.jd_end - self.jd_start) * x1 / self.graph_width + self.jd_start
                    self.forbidden_time_list.append(jd_delete_start)
                    self.forbidden_time_list.append(jd_delete_end)
                    self.fixed_position = []
                    self.point_position = []
                    self.lightcurve_and_model_was_changed()
            elif action_text == "Range(prim)":
                if self.fixed_position[0] != self.point_position[0]:
                    range = (self.jd_end - self.jd_start) / self.graph_width
                    self.width_prim_fit = fabs(self.fixed_position[0] - self.point_position[0]) / 2 * range
                    self.e0_prim_fit = (self.fixed_position[0] + self.point_position[0]) / 2 * range + self.jd_start
                    self.area_pri_label.setText("E0:" + str(round(self.e0_prim_fit, 4)) + "+/-"
                                                + str(round(self.width_prim_fit * 24, 3)) + "h")
            elif action_text == "Range(sec)":
                range = (self.jd_end - self.jd_start) / self.graph_width
                self.width_sec_fit = fabs(self.fixed_position[0] - self.point_position[0]) / 2 * range
                self.e0_sec_fit = (self.fixed_position[0] + self.point_position[0]) / 2 * range + self.jd_start
                self.area_sec_label.setText("E0:" + str(round(self.e0_sec_fit, 4)) + "+/-"
                                            + str(round(self.width_sec_fit * 24, 3)) + "h")
            elif action_text in ["D(prim)", "D(sec)", "d(prim)", "d(sec)"]:
                area_width = round((self.jd_end - self.jd_start) / self.graph_width * fabs(self.fixed_position[0] -
                                                                                           self.point_position[0]) * 24
                                   , 3)
                if self.variable_systems:
                    for variable in self.variables.variables:
                        if variable.name() == self.variable_systems[0].name() and variable.name() == self.current_model:
                            if action_text == "D(prim)":
                                variable.change_d_eclipse_prim(area_width)
                            elif action_text == "D(sec)":
                                variable.change_d_eclipse_sec(area_width)
                            elif action_text == "d(prim)":
                                variable.change_d_minimum_prim(area_width)
                            elif action_text == "d(sec)":
                                variable.change_d_minimum_sec(area_width)
                            else:
                                pass
                        info_window = Popup("Save LC parametr",
                                            "{0} was saved to star {1} pair {2}.".format(action_text,
                                                                                         variable.name(),
                                                                                         variable.pair()),
                                            buttons="OK".split(","))
                        info_window.do()

            elif action_text in ["Amp(prim)", "Amp(sec)"]:
                area_altitude = round(self.current_amplitude / self.graph_height * fabs(self.point_position[1] -
                                                                                        self.fixed_position[1]), 3)
                for variable in self.variables.variables:
                    if variable.name() == self.variable_systems[0].name() and variable.pair() == self.current_model:
                        if action_text == "Amp(prim)":
                            variable.change_amplitude_p(area_altitude)
                        elif action_text == "Amp(sec)":
                            variable.change_amplitude_s(area_altitude)
                        else:
                            pass
                        info_window = Popup("Save LC parametr",
                                            "{0} was saved to star {1} pair {2}.".format(action_text,
                                                                                         variable.name(),
                                                                                         variable.pair()),
                                            buttons="OK".split(","))
                        info_window.do()

            else:
                pass
        elif action_text == "Delete trend":
            print("a")
        else:
            pass

    def set_model_parameter_back(self):
        if self.model_a.isChecked():
            pair_index = "A"
        elif self.model_b.isChecked():
            pair_index = "B"
        elif self.model_c.isChecked():
            pair_index = "C"
        elif self.model_d.isChecked():
            pair_index = "D"
        elif self.model_e.isChecked():
            pair_index = "E"
        else:
            pair_index = "F"
        variable_index = self.existing_pair.index(pair_index)
        variable: VariableStar = self.variable_systems[variable_index]
        if self.model_mag0_label.isChecked():
            self.model_mag0_doulespinbox.setValue(variable.mag0())
        elif self.model_sec_phase_label.isChecked():
            self.model_sec_phase_doulespinbox.setValue(variable.sec_phase())
        elif self.model_a_pri_label.isChecked():
            self.model_a_pri_doulespinbox.setValue(variable.a_pri())
        elif self.model_d_pri_label.isChecked():
            self.model_d_pri_doulespinbox.setValue(variable.d_pri())
        elif self.model_g_pri_label.isChecked():
            self.model_g_pri_doulespinbox.setValue(variable.g_pri())
        elif self.model_c_pri_label.isChecked():
            self.model_c_pri_doulespinbox.setValue(variable.c_pri())
        elif self.model_a_sec_label.isChecked():
            self.model_a_sec_doulespinbox.setValue(variable.a_sec())
        elif self.model_d_sec_label.isChecked():
            self.model_d_sec_doulespinbox.setValue(variable.d_sec())
        elif self.model_g_sec_label.isChecked():
            self.model_g_sec_doulespinbox.setValue(variable.g_sec())
        elif self.model_c_sec_label.isChecked():
            self.model_c_sec_doulespinbox.setValue(variable.c_sec())
        elif self.model_sin1_label.isChecked():
            self.model_sin1_doulespinbox.setValue(variable.a_sin1())
        elif self.model_sin2_label.isChecked():
            self.model_sin2_doulespinbox.setValue(variable.a_sin2())
        elif self.model_sin3_label.isChecked():
            self.model_sin3_doulespinbox.setValue(variable.a_sin3())
        elif self.model_cos1_label.isChecked():
            self.model_cos1_doulespinbox.setValue(variable.a_cos1())
        elif self.model_cos2_label.isChecked():
            self.model_cos2_doulespinbox.setValue(variable.a_cos2())
        elif self.model_cos3_label.isChecked():
            self.model_cos3_doulespinbox.setValue(variable.a_cos3())
        elif self.model_apsid_coef_label.isChecked():
            self.model_apsid_coef_doulespinbox.setValue(variable.apsidal_movement_correction())
        elif self.model_period_label.isChecked():
            self.period_doublespinbox.setValue(variable.period())
        elif self.model_epoch_label.isChecked():
            self.epoch_doublespinbox.setValue(0)
        else:
            pass
        self.set_model_slider_range()

    def change_model(self):
        if self.printy:
            print("Tess_photometry_edit_window, change_model")

        self.connect_window(False)
        if self.model_changed:
            self.save_model()
            self.model_changed = False
        if self.model_a.isChecked():
            pair_index = "A"
        elif self.model_b.isChecked():
            pair_index = "B"
        elif self.model_c.isChecked():
            pair_index = "C"
        elif self.model_d.isChecked():
            pair_index = "D"
        elif self.model_e.isChecked():
            pair_index = "E"
        else:
            pair_index = "F"
        self.fill_model(pair_index)
        self.connect_window(True)
        self.model_mag0_label.setChecked(True)

    def set_third_light(self):
        if self.printy:
            print("Tess_photometry_edit_window, set_third_light")

        if self.fine_sliders_chechkbox.isChecked():
            fine_slider = 0.1
        else:
            fine_slider = 1
        self.third_light = self.third_light + self.third_light_slider.value() * fine_slider
        self.third_light_slider.setValue(0)

    def save_model(self):
        if self.printy:
            print("Tess_photometry_edit_window, save_model")

        save_window = Popup("Keep changes", "Do you want to keep model parameter changes?",
                            buttons="OK, Don´t keep".split(","))
        if save_window.do() == 1:
            return
        if self.current_model and self.model_changed:
            self.model_changed = False
            if self.current_model in self.existing_pair:
                model_index = self.existing_pair.index(self.current_model)
                self.variable_systems[model_index].change_mag0(self.model_mag0_doulespinbox.value())
                self.variable_systems[model_index].change_sec_phase(self.model_sec_phase_doulespinbox.value())
                self.variable_systems[model_index].change_a_pri(self.model_a_pri_doulespinbox.value())
                self.variable_systems[model_index].change_d_pri(self.model_d_pri_doulespinbox.value())
                self.variable_systems[model_index].change_g_pri(self.model_g_pri_doulespinbox.value())
                self.variable_systems[model_index].change_c_pri(self.model_c_pri_doulespinbox.value())
                self.variable_systems[model_index].change_a_sec(self.model_a_sec_doulespinbox.value())
                self.variable_systems[model_index].change_d_sec(self.model_d_sec_doulespinbox.value())
                self.variable_systems[model_index].change_g_sec(self.model_g_sec_doulespinbox.value())
                self.variable_systems[model_index].change_c_sec(self.model_c_sec_doulespinbox.value())
                self.variable_systems[model_index].change_a_sin1(self.model_sin1_doulespinbox.value())
                self.variable_systems[model_index].change_a_sin2(self.model_sin2_doulespinbox.value())
                self.variable_systems[model_index].change_a_sin3(self.model_sin3_doulespinbox.value())
                self.variable_systems[model_index].change_a_cos1(self.model_cos1_doulespinbox.value())
                self.variable_systems[model_index].change_a_cos2(self.model_cos2_doulespinbox.value())
                self.variable_systems[model_index].change_a_cos3(self.model_cos3_doulespinbox.value())
                self.variable_systems[model_index].change_apsidal_movement_correction(self.model_apsid_coef_doulespinbox.value())
                self.variable_systems[model_index].change_period(self.period_doublespinbox.value())
                self.variable_systems[model_index].change_epoch(self.variable_systems[model_index].epoch() +
                                                                self.epoch_doublespinbox.value())
                self.epoch_doublespinbox.setValue(0)

    def model_was_changed(self):
        if self.printy:
            print("Tess_photometry_edit_window, model_was_changed")

        self.model_changed = True
        if self.fine_sliders_chechkbox.isChecked():
            fine_sliders_coefficient = 100000000
        else:
            fine_sliders_coefficient = 10000000
        if self.model_mag0_label.isChecked():
            self.model_mag0_doulespinbox.setValue(self.model_slider.value() / fine_sliders_coefficient)
        elif self.model_sec_phase_label.isChecked():
            self.model_sec_phase_doulespinbox.setValue(self.model_slider.value() / fine_sliders_coefficient)
        elif self.model_a_pri_label.isChecked():
            self.model_a_pri_doulespinbox.setValue(self.model_slider.value() / fine_sliders_coefficient)
        elif self.model_d_pri_label.isChecked():
            self.model_d_pri_doulespinbox.setValue(self.model_slider.value() / fine_sliders_coefficient)
        elif self.model_g_pri_label.isChecked():
            self.model_g_pri_doulespinbox.setValue(self.model_slider.value() / fine_sliders_coefficient)
        elif self.model_c_pri_label.isChecked():
            self.model_c_pri_doulespinbox.setValue(self.model_slider.value() / fine_sliders_coefficient)
        elif self.model_a_sec_label.isChecked():
            self.model_a_sec_doulespinbox.setValue(self.model_slider.value() / fine_sliders_coefficient)
        elif self.model_d_sec_label.isChecked():
            self.model_d_sec_doulespinbox.setValue(self.model_slider.value() / fine_sliders_coefficient)
        elif self.model_g_sec_label.isChecked():
            self.model_g_sec_doulespinbox.setValue(self.model_slider.value() / fine_sliders_coefficient)
        elif self.model_c_sec_label.isChecked():
            self.model_c_sec_doulespinbox.setValue(self.model_slider.value() / fine_sliders_coefficient)
        elif self.model_sin1_label.isChecked():
            self.model_sin1_doulespinbox.setValue(self.model_slider.value() / fine_sliders_coefficient)
        elif self.model_sin2_label.isChecked():
            self.model_sin2_doulespinbox.setValue(self.model_slider.value() / fine_sliders_coefficient)
        elif self.model_sin3_label.isChecked():
            self.model_sin3_doulespinbox.setValue(self.model_slider.value() / fine_sliders_coefficient)
        elif self.model_cos1_label.isChecked():
            self.model_cos1_doulespinbox.setValue(self.model_slider.value() / fine_sliders_coefficient)
        elif self.model_cos2_label.isChecked():
            self.model_cos2_doulespinbox.setValue(self.model_slider.value() / fine_sliders_coefficient)
        elif self.model_cos3_label.isChecked():
            self.model_cos3_doulespinbox.setValue(self.model_slider.value() / fine_sliders_coefficient)
        elif self.model_apsid_coef_label.isChecked():
            self.model_apsid_coef_doulespinbox.setValue(self.model_slider.value() / fine_sliders_coefficient)
        elif self.model_period_label.isChecked():
            self.period_doublespinbox.setValue(self.model_slider.value() / fine_sliders_coefficient)
        elif self.model_epoch_label.isChecked():
            self.epoch_doublespinbox.setValue(self.model_slider.value() / fine_sliders_coefficient)
        else:
            pass

    def fill_model(self, pair):
        if self.printy:
            print("Tess_photometry_edit_window, fill_model")

        if self.existing_pair:
            self.model_mag0_doulespinbox.setEnabled(True)
            self.model_sec_phase_doulespinbox.setEnabled(True)
            self.model_a_pri_doulespinbox.setEnabled(True)
            self.model_d_pri_doulespinbox.setEnabled(True)
            self.model_g_pri_doulespinbox.setEnabled(True)
            self.model_c_pri_doulespinbox.setEnabled(True)
            self.model_a_sec_doulespinbox.setEnabled(True)
            self.model_d_sec_doulespinbox.setEnabled(True)
            self.model_g_sec_doulespinbox.setEnabled(True)
            self.model_c_sec_doulespinbox.setEnabled(True)
            self.model_sin1_doulespinbox.setEnabled(True)
            self.model_sin2_doulespinbox.setEnabled(True)
            self.model_sin3_doulespinbox.setEnabled(True)
            self.model_cos1_doulespinbox.setEnabled(True)
            self.model_cos2_doulespinbox.setEnabled(True)
            self.model_cos3_doulespinbox.setEnabled(True)
            self.model_apsid_coef_doulespinbox.setEnabled(True)
            self.model_slider.setEnabled(True)
            self.save_final_model_button.setEnabled(True)
            self.model_back_button.setEnabled(True)
            self.save_model_button.setEnabled(True)
            self.residua.setEnabled(True)
            self.residua.setChecked(True)

            if pair in self.existing_pair:
                model_index = self.existing_pair.index(pair)
            else:
                model_index = 0
            self.model_mag0_doulespinbox.setValue(float(self.variable_systems[model_index].mag0()))
            self.model_sec_phase_doulespinbox.setValue(float(self.variable_systems[model_index].sec_phase()))
            self.model_a_pri_doulespinbox.setValue(float(self.variable_systems[model_index].a_pri()))
            self.model_d_pri_doulespinbox.setValue(float(self.variable_systems[model_index].d_pri()))
            self.model_g_pri_doulespinbox.setValue(float(self.variable_systems[model_index].g_pri()))
            self.model_c_pri_doulespinbox.setValue(float(self.variable_systems[model_index].c_pri()))
            self.model_a_sec_doulespinbox.setValue(float(self.variable_systems[model_index].a_sec()))
            self.model_d_sec_doulespinbox.setValue(float(self.variable_systems[model_index].d_sec()))
            self.model_g_sec_doulespinbox.setValue(float(self.variable_systems[model_index].g_sec()))
            self.model_c_sec_doulespinbox.setValue(float(self.variable_systems[model_index].c_sec()))
            self.model_sin1_doulespinbox.setValue(float(self.variable_systems[model_index].a_sin1()))
            self.model_sin2_doulespinbox.setValue(float(self.variable_systems[model_index].a_sin2()))
            self.model_sin3_doulespinbox.setValue(float(self.variable_systems[model_index].a_sin3()))
            self.model_cos1_doulespinbox.setValue(float(self.variable_systems[model_index].a_cos1()))
            self.model_cos2_doulespinbox.setValue(float(self.variable_systems[model_index].a_cos2()))
            self.model_cos3_doulespinbox.setValue(float(self.variable_systems[model_index].a_cos3()))
            self.model_apsid_coef_doulespinbox.setValue(float(self.variable_systems[model_index].apsidal_movement_correction()))
            self.period_doublespinbox.setValue(float(self.variable_systems[model_index].period()))
            self.epoch_doublespinbox.setValue(0)
            self.current_model = pair
        else:
            self.model_mag0_doulespinbox.setValue(0)
            self.model_sec_phase_doulespinbox.setValue(0)
            self.model_a_pri_doulespinbox.setValue(0.1)
            self.model_d_pri_doulespinbox.setValue(0.1)
            self.model_g_pri_doulespinbox.setValue(1)
            self.model_c_pri_doulespinbox.setValue(0)
            self.model_a_sec_doulespinbox.setValue(0.1)
            self.model_d_sec_doulespinbox.setValue(0.1)
            self.model_g_sec_doulespinbox.setValue(1)
            self.model_c_sec_doulespinbox.setValue(0)
            self.model_sin1_doulespinbox.setValue(0)
            self.model_sin2_doulespinbox.setValue(0)
            self.model_sin3_doulespinbox.setValue(0)
            self.model_cos1_doulespinbox.setValue(0)
            self.model_cos2_doulespinbox.setValue(0)
            self.model_cos3_doulespinbox.setValue(0)
            self.model_apsid_coef_doulespinbox.setValue(0)
            self.period_doublespinbox.setValue(0.3)
            self.model_mag0_doulespinbox.clear()
            self.model_sec_phase_doulespinbox.clear()
            self.model_a_pri_doulespinbox.clear()
            self.model_d_pri_doulespinbox.clear()
            self.model_g_pri_doulespinbox.clear()
            self.model_c_pri_doulespinbox.clear()
            self.model_a_sec_doulespinbox.clear()
            self.model_d_sec_doulespinbox.clear()
            self.model_g_sec_doulespinbox.clear()
            self.model_c_sec_doulespinbox.clear()
            self.model_sin1_doulespinbox.clear()
            self.model_sin2_doulespinbox.clear()
            self.model_sin3_doulespinbox.clear()
            self.model_cos1_doulespinbox.clear()
            self.model_cos2_doulespinbox.clear()
            self.model_cos3_doulespinbox.clear()
            self.model_apsid_coef_doulespinbox.clear()
            self.period_doublespinbox.clear()
            self.epoch_doublespinbox.clear()
            self.current_model = ""
            self.model_mag0_doulespinbox.setEnabled(False)
            self.model_sec_phase_doulespinbox.setEnabled(False)
            self.model_a_pri_doulespinbox.setEnabled(False)
            self.model_d_pri_doulespinbox.setEnabled(False)
            self.model_g_pri_doulespinbox.setEnabled(False)
            self.model_c_pri_doulespinbox.setEnabled(False)
            self.model_a_sec_doulespinbox.setEnabled(False)
            self.model_d_sec_doulespinbox.setEnabled(False)
            self.model_g_sec_doulespinbox.setEnabled(False)
            self.model_c_sec_doulespinbox.setEnabled(False)
            self.model_sin1_doulespinbox.setEnabled(False)
            self.model_sin2_doulespinbox.setEnabled(False)
            self.model_sin3_doulespinbox.setEnabled(False)
            self.model_cos1_doulespinbox.setEnabled(False)
            self.model_cos2_doulespinbox.setEnabled(False)
            self.model_cos3_doulespinbox.setEnabled(False)
            self.model_apsid_coef_doulespinbox.setEnabled(False)
            self.model_slider.setEnabled(False)
            self.save_final_model_button.setEnabled(False)
            self.model_back_button.setEnabled(False)
            self.save_model_button.setEnabled(False)
            self.residua.setEnabled(False)
            self.residua.setChecked(False)

    def set_pair(self):
        if self.printy:
            print("Tess_photometry_edit_window, set_pair")

        self.model_a.setEnabled(False)
        self.visible_a.setEnabled(False)
        self.model_b.setEnabled(False)
        self.visible_b.setEnabled(False)
        self.model_c.setEnabled(False)
        self.visible_c.setEnabled(False)
        self.model_d.setEnabled(False)
        self.visible_d.setEnabled(False)
        self.model_e.setEnabled(False)
        self.visible_e.setEnabled(False)
        self.model_f.setEnabled(False)
        self.visible_f.setEnabled(False)
        self.visible_a.setChecked(False)
        self.visible_b.setChecked(False)
        self.visible_c.setChecked(False)
        self.visible_d.setChecked(False)
        self.visible_e.setChecked(False)
        self.visible_f.setChecked(False)

        if self.existing_pair:
            if "A" in self.existing_pair:
                self.model_a.setEnabled(True)
                self.visible_a.setEnabled(True)
                self.visible_a.setChecked(True)
            if "B" in self.existing_pair:
                self.model_b.setEnabled(True)
                self.visible_b.setEnabled(True)
                self.visible_b.setChecked(True)
            if "C" in self.existing_pair:
                self.model_c.setEnabled(True)
                self.visible_c.setEnabled(True)
                self.visible_c.setChecked(True)
            if "D" in self.existing_pair:
                self.model_d.setEnabled(True)
                self.visible_d.setEnabled(True)
                self.visible_d.setChecked(True)
            if "E" in self.existing_pair:
                self.model_e.setEnabled(True)
                self.visible_e.setEnabled(True)
                self.visible_e.setChecked(True)
            if "F" in self.existing_pair:
                self.model_f.setEnabled(True)
                self.visible_f.setEnabled(True)
                self.visible_f.setChecked(True)
            if len(self.variable_systems) == 1:
                self.all.setEnabled(False)
                self.all.setChecked(False)
            else:
                self.all.setEnabled(True)
                self.all.setChecked(True)
            self.residua.setChecked(True)
        else:
            self.residua.setChecked(False)
        self.trend.setChecked(True)

    def fill(self, photometry):
        if self.printy:
            print("Tess_photometry_edit_window, fill")

        try:
            self.connect_window(False)
        except:
            pass
        self.change_photometry(photometry)
        self.sector_index_combobox.clear()
        for sector in self.photometry.sectors():
            self.sector_index_combobox.addItem(str(sector))
        self.sector_index = 0
        self.third_light = 0
        self.third_light_slider.setValue(0)
        self.fixed_position = []
        self.point_position = []
        self.model_changed = False
        self.forbidden_time_list = []
        self.change_jd_start(photometry.lightcurves()[0][1])
        self.change_jd_end(photometry.lightcurves()[0][2])
        self.lc_time_area_star_info_label.setText(jd_to_date(self.jd_start).strftime("%d %m %Y %H:%M"))
        self.lc_time_area_end_info_label.setText(jd_to_date(self.jd_end).strftime("%d %m %Y %H:%M"))
        self.third_light_slider.setValue(0)
        self.offset_slider.setValue(0)
        self.start_slider.setValue(0)
        self.end_slider.setValue(1000)
        variable_system = self.photometry.give_system_models(self.variables)
        self.change_variable_systems(variable_system[0])
        self.change_existing_pair(variable_system[1])
        self.fill_model("A")
        self.set_pair()
        self.clear_lightcurve_parameters()
        self.lightcurve_and_model_was_changed()

        self.connect_window(True)
        self.show()

    def clear_lightcurve_parameters(self):
        if self.printy:
            print("Tess_photometry_edit_window, clear_lightcurve_parameters")

        self.lightcurve_set = [None] * 13
        self.min_set = [None] * 13
        self.max_set = [None] * 13
        self.amplitude_set = [0] * 13
        self.system_amplitude = 0
        self.data_amplitude = 0
        self.data_min = 0
        self.data_max = 0
        self.current_amplitude = 0
        self.border_set = []
        self.all_curve_point_set = []

    def change_sector(self):
        if self.printy:
            print("Tess_photometry_edit_window, change_sector")

        if self.photometry:
            self.trend_list = []
            self.visible_part_of_trend_list_altitude = []
            self.visible_part_of_trend_list = []
            self.sector_index = self.sector_index_combobox.currentIndex()
            self.change_jd_start(self.photometry.lightcurves()[self.sector_index][1])
            self.change_jd_end(self.photometry.lightcurves()[self.sector_index][2])
            self.forbidden_time_list = []
            self.lc_time_area_star_info_label.setText(jd_to_date(self.jd_start).strftime("%d %m %Y %H:%M"))
            self.lc_time_area_end_info_label.setText(jd_to_date(self.jd_end).strftime("%d %m %Y %H:%M"))
            self.connect_window(False)
            self.third_light_slider.setValue(0)
            self.offset_slider.setValue(0)
            self.start_slider.setValue(0)
            self.end_slider.setValue(1000)
            self.connect_window(True)
            self.lightcurve_and_model_was_changed()
            self.update()

    def go_forward(self):
        if self.printy:
            print("Tess_photometry_edit_window, go_forward")

        start_position = self.start_slider.value()
        end_position = self.end_slider.value()
        step = end_position - start_position
        if end_position + int(step/2) > 1000:
            end_position = 1000
        else:
            end_position = end_position + int(step/2)
        self.end_slider.setValue(end_position)
        self.start_slider.setValue(end_position - step)

    def go_backward(self):
        if self.printy:
            print("Tess_photometry_edit_window, go_backward")

        start_position = self.start_slider.value()
        end_position = self.end_slider.value()
        step = end_position - start_position
        if start_position - int(step/2) < 0:
            start_position = 0
        else:
            start_position = start_position - int(step/2)
        self.start_slider.setValue(start_position)
        self.end_slider.setValue(start_position + step)

    def start(self):
        if self.printy:
            print("Tess_photometry_edit_window, start")

        sector_index = int(self.sector_index_combobox.currentIndex())
        start = self.photometry.lightcurves()[sector_index][1]
        end = self.photometry.lightcurves()[sector_index][2]
        self.jd_start = (end - start) / 1000 * self.start_slider.value() + start
        if self.jd_start > self.jd_end:
            new_jd_end = self.start_slider.value() + 5
            if new_jd_end > 1000:
                new_jd_end = 1000
            self.end_slider.setValue(new_jd_end)
        self.lc_time_area_star_info_label.setText(jd_to_date(self.jd_start).strftime("%d %m %Y %H:%M"))
        self.lc_time_area_end_info_label.setText(jd_to_date(self.jd_end).strftime("%d %m %Y %H:%M"))
        self.clear_lightcurve_parameters()
        self.lightcurve_and_model_was_changed()
        self.recalibrate_trend_line()
        self.update()

    def end(self):
        if self.printy:
            print("Tess_photometry_edit_window, end")

        sector_index = int(self.sector_index_combobox.currentIndex())
        start = self.photometry.lightcurves()[sector_index][1]
        end = self.photometry.lightcurves()[sector_index][2]
        self.jd_end = (end - start) / 1000 * self.end_slider.value() + start
        if self.jd_end < self.jd_start:
            new_jd_start = self.end_slider.value() - 5
            if new_jd_start < 0:
                new_jd_start = 0
            self.start_slider.setValue(new_jd_start)
        self.lc_time_area_star_info_label.setText(jd_to_date(self.jd_start).strftime("%d %m %Y %H:%M"))
        self.lc_time_area_end_info_label.setText(jd_to_date(self.jd_end).strftime("%d %m %Y %H:%M"))
        self.clear_lightcurve_parameters()
        self.lightcurve_and_model_was_changed()
        self.recalibrate_trend_line()
        self.update()

    def set_offset(self):
        if self.printy:
            print("Tess_photometry_edit_window, set_offset")

        if self.fine_sliders_chechkbox.isChecked():
            fine_slider = 0.1
        else:
            fine_slider = 1
        self.change_offset(self.offset + self.offset_slider.value() * fine_slider / 100000)
        self.offset_slider.setValue(0)

    def model_parameters_was_changed(self):
        if self.printy:
            print("Tess_photometry_edit_window, model_parameters_was_changed")

        self.clear_lightcurve_parameters()
        self.lightcurve_and_model_was_changed()
        self.update()

    def third_light_changed(self):
        if self.printy:
            print("Tess_photometry_edit_window, third_light_changed")

        self.clear_lightcurve_parameters()
        self.lightcurve_and_model_was_changed()
        self.update()

    def offset_changed(self):
        if self.printy:
            print("Tess_photometry_edit_window, offset_changed")

        self.clear_lightcurve_parameters()
        self.lightcurve_and_model_was_changed()
        self.update()

    def home(self):
        if self.printy:
            print("Tess_photometry_edit_window, home")

        sector_index = self.sector_index_combobox.currentIndex()
        self.jd_start = self.photometry.lightcurves()[sector_index][1]
        self.jd_end = self.photometry.lightcurves()[sector_index][2]
        self.start_slider.setValue(0)
        self.end_slider.setValue(1000)
        self.update()

    def lightcurve_and_model_was_changed(self):
        if self.printy:
            print("Tess_photometry_edit_window, lightcurve_and_model_was_changed")

        self.fixed_position = []
        self.point_position = []
        self.area_amp_label.setText("")
        self.area_hours.setText("")
        if self.quick_display_combobox.currentIndex() == 1:
            quick_display_point = None
        else:
            quick_display_point = int(self.graph_width * float(self.quick_display_combobox.currentText()))
        if self.fine_sliders_chechkbox.isChecked():
            fine_slider = 0.1
        else:
            fine_slider = 1

        if self.photometry:
            lightcurve = (self.photometry.flux_to_mag(self.jd_start, self.jd_end, self.sector_index,
                                                      self.third_light_slider.value() * fine_slider + self.third_light,
                                                      self.offset + self.offset_slider.value() * fine_slider / 100000,
                                                      detrend=self.origin,
                                                      window_length=self.window_length, polyorder=self.polyorder,
                                                      return_trend=True, break_tolerance=self.break_tolerance,
                                                      niters=self.niters, sigma=self.sigma, mask=None,
                                                      forbidden_time_list=self.forbidden_time_list,
                                                      quick_display_point=quick_display_point))
            self.offset_button.setText("Set Offset " + str(round(self.offset + self.offset_slider.value()
                                                                 * fine_slider / 100000, 4)) + " mag")
            if self.origin:
                self.third_button.setText(
                    "Set Third Light " + str(round((self.third_light_slider.value() * fine_slider + self.third_light)
                                                   / 10, 2)) + " %")
            else:
                self.third_button.setText(
                    "Set Third Light " + str(round(self.third_light_slider.value() * fine_slider + self.third_light, 1))
                    + " fx")

            self.lightcurve_set[0] = lightcurve[0]
            self.lightcurve_set[1] = lightcurve[1]
            self.lightcurve_set[2] = lightcurve[2]
            self.lightcurve_set[3] = lightcurve[3]
            if self.lightcurve_set[1]:
                self.min_set[1] = min(self.lightcurve_set[1])
                self.max_set[1] = max(self.lightcurve_set[1])
                self.amplitude_set[1] = self.max_set[1] - self.min_set[1]
                self.min_set[3] = min(self.lightcurve_set[3])
                self.max_set[3] = max(self.lightcurve_set[3])
                self.amplitude_set[3] = self.max_set[3] - self.min_set[3]
            else:
                self.min_set[1] = None
                self.max_set[1] = None
                self.amplitude_set[1] = 0
                self.min_set[3] = None
                self.max_set[3] = None
                self.amplitude_set[3] = 0
            self.lightcurve_set[10] = [0] * len(self.lightcurve_set[0])
        else:
            self.close()
            return

        if self.existing_pair:
            model = [self.model_mag0_doulespinbox.value(),
                     self.model_sec_phase_doulespinbox.value(),
                     self.model_a_pri_doulespinbox.value(),
                     self.model_d_pri_doulespinbox.value(),
                     self.model_g_pri_doulespinbox.value(),
                     self.model_c_pri_doulespinbox.value(),
                     self.model_a_sec_doulespinbox.value(),
                     self.model_d_sec_doulespinbox.value(),
                     self.model_g_sec_doulespinbox.value(),
                     self.model_c_sec_doulespinbox.value(),
                     self.model_sin1_doulespinbox.value(),
                     self.model_sin2_doulespinbox.value(),
                     self.model_sin3_doulespinbox.value(),
                     self.model_cos1_doulespinbox.value(),
                     self.model_cos2_doulespinbox.value(),
                     self.model_cos3_doulespinbox.value(),
                     self.model_apsid_coef_doulespinbox.value(),
                     self.period_doublespinbox.value(),
                     self.epoch_doublespinbox.value()]
            another_model_a = False
            another_model_b = False
            another_model_c = False
            another_model_d = False
            another_model_e = False
            another_model_f = False

            if "A" in self.existing_pair:
                if self.model_a.isChecked():
                    another_model_a = True
                pair_index = self.existing_pair.index("A")
                self.lightcurve_set[4] = self.variable_systems[pair_index].lightcurve(self.jd_start, self.jd_end,
                                                                                      self.steps,
                                                                                      another_model=another_model_a,
                                                                                      model=model,
                                                                                      add_mag_and_offset=False,
                                                                                      time_points=self.lightcurve_set[0])
                if self.lightcurve_set[4]:
                    self.max_set[4] = max(self.lightcurve_set[4])
                    self.min_set[4] = min(self.lightcurve_set[4])
                    self.amplitude_set[4] = self.max_set[4] - self.min_set[4]
            if "B" in self.existing_pair:
                if self.model_b.isChecked():
                    another_model_b = True
                pair_index = self.existing_pair.index("B")
                self.lightcurve_set[5] = self.variable_systems[pair_index].lightcurve(self.jd_start, self.jd_end,
                                                                                      self.steps,
                                                                                      another_model=another_model_b,
                                                                                      model=model,
                                                                                      add_mag_and_offset=False,
                                                                                      time_points=self.lightcurve_set[0])
                if self.lightcurve_set[5]:
                    self.max_set[5] = max(self.lightcurve_set[5])
                    self.min_set[5] = min(self.lightcurve_set[5])
                    self.amplitude_set[5] = self.max_set[5] - self.min_set[5]
            if "C" in self.existing_pair:
                if self.model_c.isChecked():
                    another_model_c = True
                pair_index = self.existing_pair.index("C")
                self.lightcurve_set[6] = self.variable_systems[pair_index].lightcurve(self.jd_start, self.jd_end,
                                                                                      self.steps,
                                                                                      another_model=another_model_c,
                                                                                      model=model,
                                                                                      add_mag_and_offset=False,
                                                                                      time_points=self.lightcurve_set[0])
                if self.lightcurve_set[6]:
                    self.max_set[6] = max(self.lightcurve_set[6])
                    self.min_set[6] = min(self.lightcurve_set[6])
                    self.amplitude_set[6] = self.max_set[6] - self.min_set[6]
            if "D" in self.existing_pair:
                if self.model_d.isChecked():
                    another_model_d = True
                pair_index = self.existing_pair.index("D")
                self.lightcurve_set[7] = self.variable_systems[pair_index].lightcurve(self.jd_start, self.jd_end,
                                                                                      self.steps,
                                                                                      another_model=another_model_d,
                                                                                      model=model,
                                                                                      add_mag_and_offset=False,
                                                                                      time_points=self.lightcurve_set[0])
                if self.lightcurve_set[7]:
                    self.max_set[7] = max(self.lightcurve_set[7])
                    self.min_set[7] = min(self.lightcurve_set[7])
                    self.amplitude_set[7] = self.max_set[7] - self.min_set[7]
            if "E" in self.existing_pair:
                if self.model_e.isChecked():
                    another_model_e = True
                pair_index = self.existing_pair.index("E")
                self.lightcurve_set[8] = self.variable_systems[pair_index].lightcurve(self.jd_start, self.jd_end,
                                                                                      self.steps,
                                                                                      another_model=another_model_e,
                                                                                      model=model,
                                                                                      add_mag_and_offset=False,
                                                                                      time_points=self.lightcurve_set[0])
                if self.lightcurve_set[8]:
                    self.max_set[8] = max(self.lightcurve_set[8])
                    self.min_set[8] = min(self.lightcurve_set[8])
                    self.amplitude_set[8] = self.max_set[8] - self.min_set[8]
            if "F" in self.existing_pair:
                if self.model_f.isChecked():
                    another_model_f = True
                pair_index = self.existing_pair.index("F")
                self.lightcurve_set[9] = self.variable_systems[pair_index].lightcurve(self.jd_start, self.jd_end,
                                                                                      self.steps,
                                                                                      another_model=another_model_f,
                                                                                      model=model,
                                                                                      add_mag_and_offset=False,
                                                                                      time_points=self.lightcurve_set[0])
                if self.lightcurve_set[9]:
                    self.max_set[9] = max(self.lightcurve_set[9])
                    self.min_set[9] = min(self.lightcurve_set[9])
                    self.amplitude_set[9] = self.max_set[9] - self.min_set[9]
            for i in range(len(self.lightcurve_set[0])):
                for j in range(4, 10):
                    if self.lightcurve_set[j]:
                        self.lightcurve_set[10][i] = self.lightcurve_set[10][i] + self.lightcurve_set[j][i]

            self.max_set[10] = max(self.lightcurve_set[10])
            self.min_set[10] = min(self.lightcurve_set[10])
            self.amplitude_set[10] = self.max_set[10] - self.min_set[10]

            self.lightcurve_set[11] = []

            for i in range(0, len(self.lightcurve_set[0])):
                residuum_value = self.lightcurve_set[1][i] - self.lightcurve_set[10][i]
                self.lightcurve_set[11].append(residuum_value)
            self.max_set[11] = max(self.lightcurve_set[11])
            self.min_set[11] = min(self.lightcurve_set[11])
            self.amplitude_set[11] = self.max_set[11] - self.min_set[11]
        self.new_amplitude()

    def open_tess_data(self):
        if self.printy:
            print("Tess_photometry_edit_window, open_tess_data")

    def new_amplitude(self):
        if self.printy:
            print("Tess_photometry_edit_window, new_amplitude")

        self.current_amplitude = 0
        if len(self.existing_pair) < 2:
            if self.visible_a.isChecked() and self.amplitude_set[4]:
                if self.min_set[1] < self.min_set[4]:
                    self.data_min = self.min_set[1]
                else:
                    self.data_min = self.min_set[4]
                if self.max_set[1] > self.max_set[4]:
                    self.data_max = self.max_set[1]
                else:
                    self.data_max = self.max_set[4]
            else:
                    self.data_min = self.min_set[1]
                    self.data_max = self.max_set[1]
            self.border_set = ["A"]
        else:
            if self.all.isChecked() and self.amplitude_set[10]:
                if self.min_set[1] < self.min_set[10]:
                    self.data_min = self.min_set[1]
                else:
                    self.data_min = self.min_set[10]
                if self.max_set[1] > self.max_set[10]:
                    self.data_max = self.max_set[1]
                else:
                    self.data_max = self.max_set[10]
            else:
                    self.data_min = self.min_set[1]
                    self.data_max = self.max_set[1]
            self.border_set = ["All systems"]
        self.border_set.append(self.data_max - self.data_min)
        self.border_set.append(self.data_min)
        self.border_set.append(self.lightcurve_set[0])
        self.border_set.append(self.lightcurve_set[1])
        self.border_set.append(self.lightcurve_set[10])
        self.border_set.append((self.lightcurve_set[12]))
        self.current_amplitude = self.data_max - self.data_min
        if self.visible_a.isChecked() and self.amplitude_set[4] > 0:
            self.border_set.append("A")
            self.border_set.append(self.current_amplitude + self.amplitude_set[4])
            self.border_set.append(self.min_set[4])
            self.border_set.append(self.lightcurve_set[4])
            self.current_amplitude = self.current_amplitude + self.amplitude_set[4]
        if self.visible_b.isChecked() and self.amplitude_set[5] > 0:
            self.border_set.append("B")
            self.border_set.append(self.current_amplitude + self.amplitude_set[5])
            self.border_set.append(self.min_set[5])
            self.border_set.append(self.lightcurve_set[5])
            self.current_amplitude = self.current_amplitude + self.amplitude_set[5]
        if self.visible_c.isChecked() and self.amplitude_set[6] > 0:
            self.border_set.append("C")
            self.border_set.append(self.current_amplitude + self.amplitude_set[6])
            self.border_set.append(self.min_set[6])
            self.border_set.append(self.lightcurve_set[6])
            self.current_amplitude = self.current_amplitude + self.amplitude_set[6]
        if self.visible_d.isChecked() and self.amplitude_set[7] > 0:
            self.border_set.append("D")
            self.border_set.append(self.current_amplitude + self.amplitude_set[7])
            self.border_set.append(self.min_set[7])
            self.border_set.append(self.lightcurve_set[7])
            self.current_amplitude = self.current_amplitude + self.amplitude_set[7]
        if self.visible_e.isChecked() and self.amplitude_set[8] > 0:
            self.border_set.append("E")
            self.border_set.append(self.current_amplitude + self.amplitude_set[8])
            self.border_set.append(self.min_set[8])
            self.border_set.append(self.lightcurve_set[8])
            self.current_amplitude = self.current_amplitude + self.amplitude_set[8]
        if self.visible_f.isChecked() and self.amplitude_set[9] > 0:
            self.border_set.append("F")
            self.border_set.append(self.current_amplitude + self.amplitude_set[9])
            self.border_set.append(self.min_set[9])
            self.border_set.append(self.lightcurve_set[9])
            self.current_amplitude = self.current_amplitude + self.amplitude_set[9]
        if self.residua.isChecked() and self.amplitude_set[11] > 0:
            self.border_set.append("Residua")
            self.border_set.append(self.current_amplitude + self.amplitude_set[11])
            self.residua_amplitude_label.setText(str(round(100 * self.amplitude_set[11] / self.amplitude_set[1], 2))
                                                 + "%")
            self.border_set.append(self.min_set[11])
            self.border_set.append(self.lightcurve_set[11])
            self.current_amplitude = self.current_amplitude + self.amplitude_set[11]
        if self.trend.isChecked() and self.amplitude_set[3] > 0:
            self.border_set.append("Trend")
            self.border_set.append(self.current_amplitude + self.amplitude_set[3])
            self.border_set.append(self.min_set[3])
            self.border_set.append(self.lightcurve_set[3])
            self.current_amplitude = self.current_amplitude + self.amplitude_set[3]
        self.model_amplitude_label.setText(str(round(self.amplitude_set[10], 3)) + " mag ")
        try:
            self.data_amplitude_label.setText(str(round(self.amplitude_set[1], 3)) + " mag " +
                                              str(round(self.amplitude_set[10] / self.amplitude_set[1] * 100, 2)) + "%")
        except:
            self.data_amplitude_label.setText(str(round(self.amplitude_set[1], 3)) + " mag ")
        self.new_coordinate()

    def new_coordinate(self):
        if self.printy:
            print("Tess_photometry_edit_window, new_coordinate")

        points = len(self.border_set[3])

        self.all_curve_point_set = ["dataset", [], []]
        for i, jd_time in enumerate(self.border_set[3]):
            if self.jd_start <= jd_time <= self.jd_end:
                self.all_curve_point_set[1].append(int((jd_time - self.jd_start) / (self.jd_end - self.jd_start) * self.graph_width))
                self.all_curve_point_set[2].append(int(self.graph_height / self.current_amplitude *
                                                       (self.border_set[4][i] - self.border_set[2])))
        if self.border_set[5]:
            self.all_curve_point_set.append(self.border_set[0])
            self.all_curve_point_set.append(self.all_curve_point_set[1])
            self.all_curve_point_set.append([])
            for i in range(0, points):
                self.all_curve_point_set[-1].append(int(self.graph_height / self.current_amplitude
                                                        * (self.border_set[5][i] - self.border_set[2])))
        current_border = self.border_set[1]
        if len(self.border_set) > 7:
            for i in range(7, len(self.border_set), 4):
                self.all_curve_point_set.append(self.border_set[i])
                self.all_curve_point_set.append(self.all_curve_point_set[1])
                self.all_curve_point_set.append([])
                for y in self.border_set[i + 3]:
                    self.all_curve_point_set[-1].append(int(self.graph_height / self.current_amplitude *
                                                            (y - self.border_set[i + 2] + current_border)))
                current_border = self.border_set[i + 1]
        pass

    def pair_visibility_changed(self):
        if self.printy:
            print("Tess_photometry_edit_window, pair_visibility_changed")

        if self.photometry:
            self.new_amplitude()
            self.trend_list = []
            self.update()

    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        if self.printy:
            print("Tess_photometry_edit_window, closeEvent")

    def paintEvent(self, event):
        if self.printy:
            print("Tess_photometry_edit_window, paintEvent")

        p = QtGui.QPainter(self)
        if len(self.all_curve_point_set[1]) == len(self.visible_part_of_trend_list_altitude):
            trend_exist = True
        else:
            trend_exist = False
        for i in range(0, len(self.all_curve_point_set), 3):
            if self.all_curve_point_set[i] in ["dataset", "Residua", "Trend"]:
                line_pen = QtGui.QPen(QtCore.Qt.red)
                line_pen.setWidth(1)
                p.setPen(line_pen)
            else:
                line_pen = QtGui.QPen(QtCore.Qt.blue)
                line_pen.setWidth(1)
                p.setPen(line_pen)
            if len(self.all_curve_point_set[i+1]) > 0:
                for j in range(1, len(self.all_curve_point_set[i+1])):
                    if i == 0 and trend_exist:
                        y0 = self.all_curve_point_set[i + 2][j - 1] - self.visible_part_of_trend_list_altitude[j-1]
                        y1 = self.all_curve_point_set[i + 2][j] - self.visible_part_of_trend_list_altitude[j]
                    else:
                        y0 = self.all_curve_point_set[i + 2][j - 1]
                        y1 = self.all_curve_point_set[i + 2][j]
                    x0 = self.all_curve_point_set[i+1][j-1]
                    x1 = self.all_curve_point_set[i+1][j]
                    if x0 != x1 or y0 != y1:
                        p.drawLine(x0, y0, x1, y1)

        line_pen = QtGui.QPen(QtCore.Qt.black)
        line_pen.setStyle(QtCore.Qt.DashLine)
        line_pen.setWidth(1)
        p.setPen(line_pen)
        if self.position[1] < self.graph_height + 1:
            p.drawLine(0, self.position[1], self.graph_width, self.position[1])
        if self.position[0] < self.graph_width + 1:
            p.drawLine(self.position[0], 0, self.position[0], self.graph_height)

        if self.fixed_position:
            if self.point_position:
                p.drawLine(self.fixed_position[0], self.fixed_position[1], self.fixed_position[0],
                           self.point_position[1])
                p.drawLine(self.fixed_position[0], self.fixed_position[1], self.point_position[0],
                           self.fixed_position[1])
                p.drawLine(self.point_position[0], self.point_position[1], self.fixed_position[0],
                           self.point_position[1])
                p.drawLine(self.point_position[0], self.point_position[1], self.point_position[0],
                           self.fixed_position[1])
            else:
                p.drawLine(self.fixed_position[0], self.fixed_position[1], self.fixed_position[0],
                           self.position[1])
                p.drawLine(self.fixed_position[0], self.fixed_position[1], self.position[0],
                           self.fixed_position[1])
                p.drawLine(self.position[0], self.position[1], self.fixed_position[0],
                           self.position[1])
                p.drawLine(self.position[0], self.position[1], self.position[0],
                           self.fixed_position[1])
        line_pen = QtGui.QPen(QtCore.Qt.darkBlue)
        line_pen.setWidth(3)
        p.setPen(line_pen)
        if self.position[3] > 0:
            p.drawStaticText(20, self.graph_height, QtGui.QStaticText("cursor position  x:"
                                                                      + str(self.position[0])
                                                                      + "  y:"
                                                                      + str(self.position[1])
                                                                      + "   mag:"
                                                                      + str(round(self.position[2], 3))
                                                                      + "   JD:"
                                                                      + str(round(self.position[3], 4))
                                                                      + "  UTC:"
                                                                      + jd_to_date(self.position[3]).strftime
                                                                      ("%d %m %Y %H:%M")))
        if self.action_combobox.currentText() == "Delete trend":
            line_pen = QtGui.QPen(QtCore.Qt.green)
            line_pen.setWidth(1)
            p.setPen(line_pen)
            if self.visible_part_of_trend_list:
                for i in range(len(self.visible_part_of_trend_list) - 1):
                    p.drawLine(self.visible_part_of_trend_list[i][0], self.visible_part_of_trend_list[i][1],
                               self.visible_part_of_trend_list[i+1][0], self.visible_part_of_trend_list[i+1][1])
                line_pen = QtGui.QPen(QtCore.Qt.red)
                line_pen.setWidth(3)
                p.setPen(line_pen)
                for i in range(len(self.visible_part_of_trend_list)):
                    p.drawPoint(self.visible_part_of_trend_list[i][0], self.visible_part_of_trend_list[i][1])

        p.end()

    def mouseMoveEvent(self, event):
        self.position[0] = event.x()
        self.position[1] = event.y()
        self.position[2] = self.current_amplitude / self.graph_height * event.y()
        self.position[3] = (self.jd_end - self.jd_start) / self.graph_width * event.x() + self.jd_start
        if self.fixed_position:
            if not self.point_position:
                self.area_hours.setText(str(round((self.jd_end - self.jd_start) / self.graph_width *
                                            fabs(self.position[0] - self.fixed_position[0]) * 24, 3)))
                self.area_amp_label.setText(str(round(self.current_amplitude / self.graph_height *
                                                      fabs(self.position[1] - self.fixed_position[1]), 3)))

        self.update()

    def recalibrate_trend_line(self):
        self.visible_part_of_trend_list = []
        self.visible_part_of_trend_list_altitude = []
        if self.trend_list:
            visible_part_of_trend_list_x = []
            visible_part_of_trend_list_y = []
            visible_part_index = []
            for i in range(len(self.trend_list)):
                if self.jd_start <= self.trend_list[i][0] <= self.jd_end:
                    point_x = int((self.trend_list[i][0] - self.jd_start) / (self.jd_end - self.jd_start)
                                  * self.graph_width)
                    if not point_x in visible_part_of_trend_list_x:
                        visible_part_of_trend_list_x.append(point_x)
                        visible_part_of_trend_list_y.append(self.trend_list[i][1])
                        visible_part_index.append(i)
                        self.visible_part_of_trend_list.append([point_x, self.trend_list[i][1]])
            if visible_part_of_trend_list_x:
                if visible_part_of_trend_list_x[0] > 0:
                    if visible_part_index[0] > 0:
                        i = visible_part_index[0]
                        zero_point_y = (self.jd_start - self.trend_list[i-1][0]) / (self.trend_list[i][0] -
                                                                                    self.trend_list[i-1][0]) * \
                                       (self.trend_list[i][1] - self.trend_list[i-1][1]) + self.trend_list[i-1][1]
                        visible_part_of_trend_list_x.insert(0, 0)
                        visible_part_of_trend_list_y.insert(0, zero_point_y)
                        visible_part_index.insert(0, -1)
                        self.visible_part_of_trend_list.insert(0, [0, zero_point_y])
                    else:
                        visible_part_of_trend_list_x.insert(0, 0)
                        visible_part_of_trend_list_y.insert(0, visible_part_of_trend_list_y[0])
                        visible_part_index.insert(0, -1)
                        self.visible_part_of_trend_list.insert(0, [0, visible_part_of_trend_list_y[0]])
                if visible_part_of_trend_list_x[-1] < self.graph_width:
                    if visible_part_index[-1] < len(self.trend_list) - 1:
                        i = visible_part_index[-1]
                        end_point_y = (self.jd_end - self.trend_list[i][0]) / (self.trend_list[i + 1][0] -
                                                                                      self.trend_list[i][0]) * \
                                       (self.trend_list[i + 1][1] - self.trend_list[i][1]) + self.trend_list[i][1]
                        visible_part_of_trend_list_x.append(self.graph_width)
                        visible_part_of_trend_list_y.append(end_point_y)
                        visible_part_index.append(-1)
                        self.visible_part_of_trend_list.append([self.graph_width, end_point_y])
                    else:
                        visible_part_of_trend_list_x.append(self.graph_width)
                        visible_part_of_trend_list_y.append(visible_part_of_trend_list_y[-1])
                        visible_part_index.append(-1)
                        self.visible_part_of_trend_list.append([self.graph_width, visible_part_of_trend_list_y[-1]])
            else:
                if len(self.trend_list) == 1:
                    self.visible_part_of_trend_list.append([0, self.trend_list[0][1]])
                    self.visible_part_of_trend_list.append([self.graph_width, self.trend_list[0][1]])
                else:
                    if self.jd_end < self.trend_list[0][0]:
                        self.visible_part_of_trend_list.append([0, self.trend_list[0][1]])
                        self.visible_part_of_trend_list.append([self.graph_width, self.trend_list[0][1]])
                    elif self.jd_start > self.trend_list[-1][0]:
                        self.visible_part_of_trend_list.append([0, self.trend_list[-1][1]])
                        self.visible_part_of_trend_list.append([self.graph_width, self.trend_list[-1][1]])
                    else:
                        for l in range(len(self.trend_list)):
                            if self.trend_list[l][0] < self.jd_start < self.trend_list[l + 1][0]:
                                zero_point_y = (self.jd_start - self.trend_list[l][0]) \
                                               / (self.trend_list[l + 1][0] - self.trend_list[l][0]) \
                                               * (self.trend_list[l + 1][1] - self.trend_list[l][1]) \
                                               + self.trend_list[l][1]
                                end_point_y = (self.jd_end - self.trend_list[l][0]) \
                                               / (self.trend_list[l + 1][0] - self.trend_list[l][0]) \
                                               * (self.trend_list[l + 1][1] - self.trend_list[l][1]) \
                                               + self.trend_list[l][1]
                                self.visible_part_of_trend_list.append([0, int(zero_point_y)])
                                self.visible_part_of_trend_list.append([self.graph_width, int(end_point_y)])
            if len(self.visible_part_of_trend_list) > 1:
                t = 0
                trend_minimum = 0
                for i, jd_point in enumerate(self.all_curve_point_set[1]):
                    while jd_point >= self.visible_part_of_trend_list[t+1][0]:
                        t = t + 1
                    jd_range = self.visible_part_of_trend_list[t+1][0] - self.visible_part_of_trend_list[t][0]
                    jd_part_range = jd_point - self.visible_part_of_trend_list[t][0]
                    jd_part = jd_part_range / jd_range
                    altitude = self.visible_part_of_trend_list[t+1][1] - self.visible_part_of_trend_list[t][1]
                    part_altitude = int(altitude * jd_part + self.visible_part_of_trend_list[t][1])
                    if self.all_curve_point_set[2][i] - part_altitude < trend_minimum:
                        trend_minimum = self.all_curve_point_set[2][i] - part_altitude
                    self.visible_part_of_trend_list_altitude.append(part_altitude)
                for j in range(len(self.visible_part_of_trend_list_altitude)):
                    self.visible_part_of_trend_list_altitude[j] = self.visible_part_of_trend_list_altitude[j] \
                                                                  + trend_minimum




    def mousePressEvent(self, event):
        if event.y() < self.graph_height + 40 and event.x() < self.graph_width + 40:
            x_position = event.x()
            y_position = event.y()
            if x_position < 5:
                x_position = 0
            if y_position < 5:
                y_position = 0

            if x_position > self.graph_width:
                x_position = self.graph_width
            if y_position > self.graph_height:
                y_position = self.graph_height
            if self.action_combobox.currentText() == "Delete trend":
                date_jd = (x_position / self.graph_width) * (self.jd_end - self.jd_start) + self.jd_start
                delete_index = -1
                jd_time_range = (self.jd_end - self.jd_start) / 500
                for i, point in enumerate(self.trend_list):
                    if point[0] - jd_time_range <= date_jd <= point[0] + jd_time_range:
                        delete_index = i
                if delete_index > -1:
                    del(self.trend_list[delete_index])
                else:
                    self.trend_list.append([date_jd, y_position])
                    self.trend_list.sort(key=lambda x: x[0])
                self.recalibrate_trend_line()
            else:
                if self.fixed_position:
                    if self.point_position:
                        self.fixed_position = []
                        self.point_position = []
                        self.area_hours.setText("")
                        self.area_amp_label.setText("")
                    else:
                        self.point_position = [x_position, y_position]
                else:
                    self.fixed_position = [x_position, y_position]
        self.update()

    def resizeEvent(self, a0: QtGui.QResizeEvent) -> None:
        if self.printy:
            print("Tess_photometry_edit_window, resizeEvent")

        if self.graph_height != self.height() - self.down_panel_width:
            self.trend_list = []

        self.change_graph_width(self.width() - self.side_panel_width)
        self.change_graph_height(self.height() - self.down_panel_width)
        self.fixed_position = []
        self.point_position = []
        self.area_hours.setText("")
        self.area_amp_label.setText("")
        self.new_coordinate()
        self.recalibrate_trend_line()
        self.update()


class DataFit:

    def __init__(self, jd_time_list, mag_list, error_list=[], mag0=0.0, a=0.5, c=0.0, d=0.1, g=1.0, phase=0.0):
        self.__jd_time_list = jd_time_list
        self.__mag_list = mag_list
        self.__error_list = error_list
        self.__p = [mag0, a, c, d, g, phase]
        self.__min = min(self.__jd_time_list)
        self.__max = max(self.__jd_time_list)
        self.__time_range = self.__max - self.__min

    # Define the model function mag0 + a * (1 + c * phase ** 2 / d ** 2) * (1 - ((1 - exp(1 - cosh(phase / d))) ** g))
    def __model(self, x, parameters):
        p1 = parameters
        f = (x - self.__min) / self.__time_range * 0.5 * pi - pi / 4
        v1 = p1[1] * (1 + p1[2] * (f - p1[5]) ** 2 / p1[3] ** 2) * (1 - ((1 - exp(1 - cosh((f - p1[5]) / p1[3]))) ** p1[4]))
        v = p1[0] + v1
        return v

    # Define the residual function
    def __fun(self, parameters):
        res = []
        for i, x in enumerate(self.__jd_time_list):
            res.append(self.__model(x, parameters) - self.__mag_list[i])
        return res

    def fit_curve(self):
        res1 = least_squares(self.__fun, self.__p)
        p0 = [res1.x[0], res1.x[1], res1.x[2], res1.x[3], res1.x[4], res1.x[5]]
        return p0

    def fit_curve_points(self, points=100):
        x_test = np.linspace(self.__min, self.__max, points)
        y_test = []
        parameters = self.fit_parameters()
        for x in x_test:
            y_test.append(self.__model(x, parameters))
        return [x_test, y_test]

    def print_curve(self, x_test, y_test):
        plt.plot(self.__jd_time_list, self.__mag_list, '.', label='data')
        plt.plot(x_test, y_test, 'r-', label='fit')
        plt.xlabel('x')
        plt.ylabel('y')
        plt.legend()
        plt.show()
