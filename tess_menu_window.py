import csv
import lightkurve as lk
import astropy.units as u
from PyQt5 import QtWidgets, QtCore, QtGui

import tess_photometry_edit_window
from coordinate import *
import os
import sys
import warnings
from lightkurve import LightkurveWarning
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
from tess_cut_info import *
from time_period import jd_to_date
from datetime import datetime
from copy import *
import matplotlib
from step_main_form import Popup
matplotlib.use('Qt5Agg')


def find_path_to_file(current_path="", window_table="Select the file", mask="*.csv *.sif *.sfd", path_to_file=True):
    if not os.path.exists(current_path):
        current_path = os.getenv("APPDATA")
    if path_to_file:
        path_to_file = QtWidgets.QFileDialog.getOpenFileName(caption=window_table, directory=current_path,
                                                             filter=mask)
    else:
        path_to_file = QtWidgets.QFileDialog.getExistingDirectory(caption=window_table, directory=current_path)
    return path_to_file


class TESSMenuWindow(QtWidgets.QWidget):

    def __init__(self, *args, **kvargs):
        super(TESSMenuWindow, self).__init__(*args, **kvargs)

        self.setWindowTitle("TESS photometry")
        self.setWindowIcon(QtGui.QIcon("star-small.png"))
        main_layout = QtWidgets.QGridLayout()
        self.setLayout(main_layout)
        self.__photometry_cut = []
        self.__mask_desintegration_set1 = []
        self.__mask_desintegration_set2 = []
        self.setMinimumHeight(580)

        self.period_multiplicity = 0
        self.slider_history = 0
        self.slider_range = 0.0001
        self.origin_period = 1
        self.origin_epoch = 2459000
        self.new_epoch = 2459000
        self.current_period = 1
        self.perioda_slider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.perioda_slider.setMinimum(-1000)
        self.perioda_slider.setMaximum(1000)
        self.multiplication_period_plus = QtWidgets.QPushButton("P*2")
        self.multiplication_period_minus = QtWidgets.QPushButton("P/2")
        self.period_slider_range_combobox = QtWidgets.QComboBox()
        self.period_slider_range_combobox.addItems(["0.0000001", "0.000001", "0.00001", "0.0001", "0.001", "0.01", "0.1", "1", "10"])
        self.period_slider_range_combobox.setCurrentIndex(3)
        self.zero_pushbutton = QtWidgets.QPushButton("set zero")
        self.set_period_pushbutton = QtWidgets.QPushButton("Set new period")
        self.clear_changes_pushbutton = QtWidgets.QPushButton("Clear changes")
        self.current_period_label = QtWidgets.QLabel("")

        graph1_object_label = QtWidgets.QLabel("Star:")
        graph1_sector_label = QtWidgets.QLabel("Sector:")
        graph1_zoom_label = QtWidgets.QLabel("Part:")
        graph2_object_label = QtWidgets.QLabel("Star:")
        graph2_sector_label = QtWidgets.QLabel("Sector:")
        graph2_zoom_label = QtWidgets.QLabel("Part:")
        star_without_data_label = QtWidgets.QLabel("Star without data")
        star_with_mistake_data_transfer_label = QtWidgets.QLabel("Data transfer error")
        graph1_disintegrated_pixel_label = QtWidgets.QLabel("mask pixel:")
        graph1_period_label = QtWidgets.QLabel("Period:")
        graph1_epoch_label = QtWidgets.QLabel("Epoch:")
        graph1_start_label = QtWidgets.QLabel("Date start JD:")
        graph1_end_label = QtWidgets.QLabel("End JD:")
        graph2_disintegrated_pixel_label = QtWidgets.QLabel("mask pixel:")
        graph2_period_label = QtWidgets.QLabel("Period:")
        graph2_epoch_label = QtWidgets.QLabel("Epoch:")
        graph2_start_label = QtWidgets.QLabel("Date start JD:")
        graph2_end_label = QtWidgets.QLabel("End JD:")

        # Photometry setting
        self.photometry_setting_pushbutton = QtWidgets.QPushButton("Photometry setting")
        self.edit_tess_data_pushbutton = QtWidgets.QPushButton("Edit photometry")
        self.edit_tess_data_pushbutton.setEnabled(False)
        self.start_pushbutton = QtWidgets.QPushButton("UPLOAD Objects")
        self.save_pushbutton = QtWidgets.QPushButton("SAVE ALL")
        self.save_pushbutton.setEnabled(False)
        self.save_star_pushbutton = QtWidgets.QPushButton("SAVE STAR")
        self.save_star_pushbutton.setEnabled(False)
        self.save_sector_pushbutton = QtWidgets.QPushButton("SAVE SECTOR")
        self.save_sector_pushbutton.setEnabled(False)
        self.create_fild_pushbutton = QtWidgets.QPushButton("Create field")
        self.create_fild_pushbutton.setEnabled(False)
        self.add_to_fild_pushbutton = QtWidgets.QPushButton("Add to field")
        self.add_to_fild_pushbutton.setEnabled(False)
        self.add_all_to_fild_pushbutton = QtWidgets.QPushButton("Add all to field")
        self.add_all_to_fild_pushbutton.setEnabled(False)
        self.metadata_checkbox = QtWidgets.QCheckBox("metadata")
        self.metadata_checkbox.setChecked(False)


        # Canvas
        self.graph1 = MplCanvas(self, width=10, height=4, dpi=100)
        self.toolbar_graf1 = NavigationToolbar(self.graph1, self)
        self.toolbar1_layout = QtWidgets.QGridLayout()
        self.toolbar1_layout.addWidget(self.toolbar_graf1, 0, 0)
        self.toolbar1_layout.addWidget(self.graph1, 1, 0)

        self.graph2 = MplCanvas(self, width=10, height=4, dpi=100)
        self.toolbar_graf2 = NavigationToolbar(self.graph2, self)
        self.toolbar2_layout = QtWidgets.QGridLayout()
        self.toolbar2_layout.addWidget(self.toolbar_graf2, 0, 0)
        self.toolbar2_layout.addWidget(self.graph2, 1, 0)

        # graphs
        self.graph1_object_combobox = QtWidgets.QComboBox()
        self.graph1_object_combobox.setFixedWidth(300)
        self.graph1_sector_combobox = QtWidgets.QComboBox()
        self.graph1_type_combobox = QtWidgets.QComboBox()
        self.graph1_type_combobox.setFixedWidth(150)
        self.graph1_fix_type_checkbox = QtWidgets.QCheckBox("Fix graph type")
        self.graph1_forward_button = QtWidgets.QPushButton("Forward")
        self.graph1_del_star_pushbutton = QtWidgets.QPushButton("Delete star")
        self.graph1_del_sector_pushbutton = QtWidgets.QPushButton("Delete star sector")
        self.graph1_zoom_combobox = QtWidgets.QComboBox()
        self.graph1_mask_position_label = QtWidgets.QLabel("")
        self.graph1_mask_size_label = QtWidgets.QLabel("")
        self.graph1_tess_cut_size_label = QtWidgets.QLabel("")
        self.graph_same_star_checkbox = QtWidgets.QCheckBox("Keep same star")
        self.graph_double_period_checkbox = QtWidgets.QCheckBox("Show 2x Period")
        self.graph1_period_label = QtWidgets.QLabel("")
        self.graph1_epoch_label = QtWidgets.QLabel("")
        self.graph1_disintegrated_x_combobox = QtWidgets.QComboBox()
        self.graph1_disintegrated_x_combobox.setFixedWidth(40)
        self.graph1_disintegrated_y_combobox = QtWidgets.QComboBox()
        self.graph1_disintegrated_y_combobox.setFixedWidth(40)
        self.graph1_start_date_label = QtWidgets.QLabel("")
        self.graph1_end_date_label = QtWidgets.QLabel("")
        self.window_length_combobox1 = QtWidgets.QComboBox()
        self.window_length_combobox1.addItems(["101", "201", "301", "401", "501", "601", "701", "801", "901", "1001",
                                              "1101", "1201", "1301", "1401", "1501", "1601", "1701", "1801", "1901",
                                              "2001", "2101", "2201", "2301", "2401", "2501", "2601", "2701", "2801",
                                              "2901"])
        self.window_length_combobox1.setCurrentText("101")
        self.polyorder_combobox1 = QtWidgets.QComboBox()
        self.break_tolerance_combobox1 = QtWidgets.QComboBox()
        self.niters_combobox1 = QtWidgets.QComboBox()
        self.sigma_combobox1 = QtWidgets.QComboBox()
        for i in range(1, 101):
            self.polyorder_combobox1.addItem(str(i))
            self.break_tolerance_combobox1.addItem(str(i))
            self.niters_combobox1.addItem(str(i))
            self.sigma_combobox1.addItem(str(i))
        self.polyorder_combobox1.setCurrentText("2")
        self.break_tolerance_combobox1.setCurrentText("5")
        self.niters_combobox1.setCurrentText("3")
        self.sigma_combobox1.setCurrentText("3")


        self.graph2_object_combobox = QtWidgets.QComboBox()
        self.graph2_object_combobox.setFixedWidth(300)
        self.graph2_sector_combobox = QtWidgets.QComboBox()
        self.graph2_type_combobox = QtWidgets.QComboBox()
        self.graph2_type_combobox.setFixedWidth(150)
        self.graph2_fix_type_checkbox = QtWidgets.QCheckBox("Fix graph type")
        self.graph2_forward_button = QtWidgets.QPushButton("Forward")
        self.graph2_del_star_pushbutton = QtWidgets.QPushButton("Del star")
        self.graph2_del_sector_pushbutton = QtWidgets.QPushButton("Del star sector")
        self.graph2_zoom_combobox = QtWidgets.QComboBox()
        self.graph2_mask_position_label = QtWidgets.QLabel("")
        self.graph2_mask_size_label = QtWidgets.QLabel("")
        self.graph2_tess_cut_size_label = QtWidgets.QLabel("")
        self.graph2_period_label = QtWidgets.QLabel("")
        self.graph2_epoch_label = QtWidgets.QLabel("")
        self.graph2_disintegrated_x_combobox = QtWidgets.QComboBox()
        self.graph2_disintegrated_x_combobox.setFixedWidth(40)
        self.graph2_disintegrated_y_combobox = QtWidgets.QComboBox()
        self.graph2_disintegrated_y_combobox.setFixedWidth(40)
        self.graph2_start_date_label = QtWidgets.QLabel("")
        self.graph2_end_date_label = QtWidgets.QLabel("")

        self.window_length_combobox2 = QtWidgets.QComboBox()
        self.window_length_combobox2.addItems(["101", "201", "301", "401", "501", "601", "701", "801", "901", "1001",
                                              "1101", "1201", "1301", "1401", "1501", "1601", "1701", "1801", "1901",
                                              "2001", "2101", "2201", "2301", "2401", "2501", "2601", "2701", "2801",
                                              "2901"])
        self.window_length_combobox2.setCurrentText("101")
        self.polyorder_combobox2 = QtWidgets.QComboBox()
        self.break_tolerance_combobox2 = QtWidgets.QComboBox()
        self.niters_combobox2 = QtWidgets.QComboBox()
        self.sigma_combobox2 = QtWidgets.QComboBox()
        for i in range(1, 101):
            self.polyorder_combobox2.addItem(str(i))
            self.break_tolerance_combobox2.addItem(str(i))
            self.niters_combobox2.addItem(str(i))
            self.sigma_combobox2.addItem(str(i))
        self.polyorder_combobox2.setCurrentText("2")
        self.break_tolerance_combobox2.setCurrentText("5")
        self.niters_combobox2.setCurrentText("3")
        self.sigma_combobox2.setCurrentText("3")


        self.star_without_data_combobox = QtWidgets.QComboBox()
        self.star_with_mistake_data_combobox = QtWidgets.QComboBox()

        star_without_data_groupbox = QtWidgets.QGroupBox("Star without data or with data transfer error")
        star_without_data_layout = QtWidgets.QHBoxLayout()
        star_without_data_groupbox.setLayout(star_without_data_layout)

        save_groupbox = QtWidgets.QGroupBox("Load and edit photometry, save stars or create Silicups field")
        save_groupbox.setMaximumHeight(90)
        save_layout = QtWidgets.QHBoxLayout()
        save_groupbox.setLayout(save_layout)


        star_without_data_layout.addWidget(star_without_data_label)
        star_without_data_layout.addWidget(self.star_without_data_combobox)
        star_without_data_layout.addWidget(star_with_mistake_data_transfer_label)
        star_without_data_layout.addWidget(self.star_with_mistake_data_combobox)

        self.graph1_group_box = QtWidgets.QGroupBox("Graph one setting")
        self.graph1_layout = QtWidgets.QGridLayout()
        self.graph1_group_box.setLayout(self.graph1_layout)

        self.graph2_group_box = QtWidgets.QGroupBox("Graph two setting")
        self.graph2_layout = QtWidgets.QGridLayout()
        self.graph2_group_box.setLayout(self.graph2_layout)

        self.detrend_layout1 = QtWidgets.QHBoxLayout()

        label_w1 = QtWidgets.QLabel("Window length:")
        label_p1 = QtWidgets.QLabel("Polyorder:")
        label_b1 = QtWidgets.QLabel("Break toler.:")
        label_n1 = QtWidgets.QLabel("Niters:")
        label_s1 = QtWidgets.QLabel("Sigma:")
        label_w2 = QtWidgets.QLabel("Window length:")
        label_p2 = QtWidgets.QLabel("Polyorder:")
        label_b2 = QtWidgets.QLabel("Break toler.:")
        label_n2 = QtWidgets.QLabel("Niters:")
        label_s2 = QtWidgets.QLabel("Sigma:")

        self.detrend_layout1.addWidget(label_w1)
        self.detrend_layout1.addWidget(self.window_length_combobox1)
        self.detrend_layout1.addWidget(label_p1)
        self.detrend_layout1.addWidget(self.polyorder_combobox1)
        self.detrend_layout1.addWidget(label_b1)
        self.detrend_layout1.addWidget(self.break_tolerance_combobox1)
        self.detrend_layout1.addWidget(label_n1)
        self.detrend_layout1.addWidget(self.niters_combobox1)
        self.detrend_layout1.addWidget(label_s1)
        self.detrend_layout1.addWidget(self.sigma_combobox1)

        self.detrend_layout2 = QtWidgets.QHBoxLayout()

        self.detrend_layout2.addWidget(label_w2)
        self.detrend_layout2.addWidget(self.window_length_combobox2)
        self.detrend_layout2.addWidget(label_p2)
        self.detrend_layout2.addWidget(self.polyorder_combobox2)
        self.detrend_layout2.addWidget(label_b2)
        self.detrend_layout2.addWidget(self.break_tolerance_combobox2)
        self.detrend_layout2.addWidget(label_n2)
        self.detrend_layout2.addWidget(self.niters_combobox2)
        self.detrend_layout2.addWidget(label_s2)
        self.detrend_layout2.addWidget(self.sigma_combobox2)


        self.graph1_layout.addWidget(graph1_object_label, 0, 0, 1, 1)
        self.graph1_layout.addWidget(self.graph1_object_combobox, 0, 1, 1, 5)
        self.graph1_layout.addWidget(graph1_sector_label, 0, 6, 1, 1)
        self.graph1_layout.addWidget(self.graph1_sector_combobox, 0, 7, 1, 2)
        self.graph1_layout.addWidget(self.graph_double_period_checkbox, 0, 9, 1, 3)
        self.graph1_layout.addWidget(self.graph1_forward_button, 1, 0, 1, 2)
        self.graph1_layout.addWidget(self.graph1_del_star_pushbutton, 1, 2, 1, 2)
        self.graph1_layout.addWidget(self.graph1_del_sector_pushbutton, 1, 4, 1, 2)
        self.graph1_layout.addWidget(graph1_zoom_label, 1, 6, 1, 1)
        self.graph1_layout.addWidget(self.graph1_zoom_combobox, 1, 7, 1, 2)
        self.graph1_layout.addWidget(self.graph1_fix_type_checkbox, 1, 9, 1, 3)
        self.graph1_layout.addWidget(self.graph1_tess_cut_size_label, 2, 0, 1, 3)
        self.graph1_layout.addWidget(self.graph1_mask_position_label, 2, 3, 1, 2)
        self.graph1_layout.addWidget(self.graph1_mask_size_label, 2, 5, 1, 2)
        self.graph1_layout.addWidget(self.graph1_type_combobox, 2, 7, 1, 5)
        self.graph1_layout.addWidget(graph1_period_label, 3, 0, 1, 1)
        self.graph1_layout.addWidget(self.graph1_period_label, 3, 1, 1, 2)
        self.graph1_layout.addWidget(graph1_epoch_label, 3, 3, 1, 1)
        self.graph1_layout.addWidget(self.graph1_epoch_label, 3, 4, 1, 3)
        self.graph1_layout.addWidget(graph1_disintegrated_pixel_label, 3, 7, 1, 3)
        self.graph1_layout.addWidget(self.graph1_disintegrated_x_combobox, 3, 10, 1, 1)
        self.graph1_layout.addWidget(self.graph1_disintegrated_y_combobox, 3, 11, 1, 1)
        self.graph1_layout.addWidget(graph1_start_label, 4, 0, 1, 2)
        self.graph1_layout.addWidget(self.graph1_start_date_label, 4, 2, 1, 3)
        self.graph1_layout.addWidget(graph1_end_label, 4, 5, 1, 1)
        self.graph1_layout.addWidget(self.graph1_end_date_label, 4, 6, 1, 6)
        self.graph1_layout.addLayout(self.detrend_layout1, 5, 0, 1, 12)
        self.graph1_layout.addLayout(self.toolbar1_layout, 6, 0, 48, 12)

        self.graph2_layout.addWidget(graph2_object_label, 0, 0, 1, 1)
        self.graph2_layout.addWidget(self.graph2_object_combobox, 0, 1, 1, 5)
        self.graph2_layout.addWidget(graph2_sector_label, 0, 6, 1, 1)
        self.graph2_layout.addWidget(self.graph2_sector_combobox, 0, 7, 1, 2)
        self.graph2_layout.addWidget(self.graph_same_star_checkbox, 0, 9, 1, 3)
        self.graph2_layout.addWidget(self.graph2_forward_button, 1, 0, 1, 2)
        self.graph2_layout.addWidget(self.graph2_del_star_pushbutton, 1, 2, 1, 2)
        self.graph2_layout.addWidget(self.graph2_del_sector_pushbutton, 1, 4, 1, 2)
        self.graph2_layout.addWidget(graph2_zoom_label, 1, 6, 1, 1)
        self.graph2_layout.addWidget(self.graph2_zoom_combobox, 1, 7, 1, 2)
        self.graph2_layout.addWidget(self.graph2_fix_type_checkbox, 1, 9, 1, 3)
        self.graph2_layout.addWidget(self.graph2_tess_cut_size_label, 2, 0, 1, 3)
        self.graph2_layout.addWidget(self.graph2_mask_position_label, 2, 3, 1, 2)
        self.graph2_layout.addWidget(self.graph2_mask_size_label, 2, 5, 1, 2)
        self.graph2_layout.addWidget(self.graph2_type_combobox, 2, 7, 1, 5)
        self.graph2_layout.addWidget(graph2_period_label, 3, 0, 1, 1)
        self.graph2_layout.addWidget(self.graph2_period_label, 3, 1, 1, 2)
        self.graph2_layout.addWidget(graph2_epoch_label, 3, 3, 1, 1)
        self.graph2_layout.addWidget(self.graph2_epoch_label, 3, 4, 1, 3)
        self.graph2_layout.addWidget(graph2_disintegrated_pixel_label, 3, 7, 1, 3)
        self.graph2_layout.addWidget(self.graph2_disintegrated_x_combobox, 3, 10, 1, 1)
        self.graph2_layout.addWidget(self.graph2_disintegrated_y_combobox, 3, 11, 1, 1)
        self.graph2_layout.addWidget(graph2_start_label, 4, 0, 1, 2)
        self.graph2_layout.addWidget(self.graph2_start_date_label, 4, 2, 1, 3)
        self.graph2_layout.addWidget(graph2_end_label, 4, 5, 1, 1)
        self.graph2_layout.addWidget(self.graph2_end_date_label, 4, 6, 1, 6)
        self.graph2_layout.addLayout(self.detrend_layout2, 5, 0, 1, 12)
        self.graph2_layout.addLayout(self.toolbar2_layout, 6, 0, 48, 12)

        save_layout.addWidget(self.save_pushbutton)
        save_layout.addWidget(self.save_star_pushbutton)
        save_layout.addWidget(self.save_sector_pushbutton)
        save_layout.addWidget(self.create_fild_pushbutton)
        save_layout.addWidget(self.add_to_fild_pushbutton)
        save_layout.addWidget(self.add_all_to_fild_pushbutton)
        save_layout.addWidget(self.metadata_checkbox)
        save_layout.addStretch()
        save_layout.addWidget(self.edit_tess_data_pushbutton)
        save_layout.addStretch()
        save_layout.addWidget(self.start_pushbutton)
        save_layout.addWidget((self.photometry_setting_pushbutton))

        period_groupbox = QtWidgets.QGroupBox("Period changes")
        period_groupbox.setMaximumHeight(85)
        period_layout = QtWidgets.QHBoxLayout()
        period_groupbox.setLayout(period_layout)

        slider_groupbox = QtWidgets.QGroupBox("Slider")
        slider_groupbox.setMaximumHeight(85)
        slider_layout = QtWidgets.QHBoxLayout()
        slider_groupbox.setLayout(slider_layout)

        slider_layout.addWidget(self.perioda_slider)

        period_layout.addWidget(self.multiplication_period_plus)
        period_layout.addWidget(self.multiplication_period_minus)
        period_layout.addWidget(QtWidgets.QLabel("Slider range:"))
        period_layout.addWidget(self.period_slider_range_combobox)
        period_layout.addWidget(self.zero_pushbutton)
        period_layout.addWidget(QtWidgets.QLabel("current period"))
        period_layout.addWidget(self.current_period_label)
        period_layout.addWidget(self.set_period_pushbutton)
        period_layout.addWidget(self.clear_changes_pushbutton)


        main_layout.addWidget(self.graph1_group_box, 0, 0, 5, 10)
        main_layout.addWidget(self.graph2_group_box, 0, 10, 5, 10)
        main_layout.addWidget(period_groupbox, 5, 0, 1, 10)
        main_layout.addWidget(slider_groupbox, 5, 10, 1, 10)
        main_layout.addWidget(save_groupbox, 6, 0, 1, 15)
        main_layout.addWidget(star_without_data_groupbox, 6, 15, 1, 5)

    def setup(self):
        from step_application import root
        self.step_main_form = root.step_main_form
        self.tess_import = root.tess_import
        self.user = root.database.user
        self.tess_photometry_edit_window = root.tess_photometry_edit_window
        self.silicups_window = root.silicups_window
        self.photometry_star_list_window = root.photometry_star_list_window
        self.tess_menu_window_setting = root.tess_menu_window_setting
        self.set_photometry_setting()

        self.save_action = self.step_main_form.save_action
        self.prediction_action = self.step_main_form.prediction_action
        self.star_edit_action = self.step_main_form.star_edit_action
        self.show_observation_action = self.step_main_form.observation_action
        self.show_lightcurve_action = self.step_main_form.lightcurve_action
        self.tess_setting_action = self.step_main_form.tess_setting_action
        self.check_variability_action = self.step_main_form.check_variability_action
        self.addAction(self.save_action)
        self.addAction(self.prediction_action)
        self.addAction(self.star_edit_action)
        self.addAction(self.show_observation_action)
        self.addAction(self.show_lightcurve_action)
        self.addAction(self.tess_setting_action)
        self.addAction(self.check_variability_action)

        self.start_pushbutton.clicked.connect(self.upload_photometry)
        self.photometry_setting_pushbutton.clicked.connect(self.photometry_setting)
        self.connect_graph()
        self.graph_same_star_checkbox.clicked.connect(self.set_same_star)
        self.graph_double_period_checkbox.clicked.connect(self.double_period)
        self.graph1_forward_button.clicked.connect(self.forward1_part1_desintegration)
        self.graph2_forward_button.clicked.connect(self.forward2_part1_desintegration)
        self.graph1_del_star_pushbutton.clicked.connect(self.delete1_star)
        self.graph1_del_sector_pushbutton.clicked.connect(self.delete1_sector)
        self.graph2_del_star_pushbutton.clicked.connect(self.delete2_star)
        self.graph2_del_sector_pushbutton.clicked.connect(self.delete2_sector)
        self.save_pushbutton.clicked.connect(self.save_all)
        self.edit_tess_data_pushbutton.clicked.connect(self.edit_tess_data)
        self.save_star_pushbutton.clicked.connect(self.save_current_star)
        self.save_sector_pushbutton.clicked.connect(self.save_current_sector)
        self.create_fild_pushbutton.clicked.connect(self.create_field)
        self.add_to_fild_pushbutton.clicked.connect(self.add_to_silicups_field)
        self.add_all_to_fild_pushbutton.clicked.connect(self.add_all_to_silicups_field)

    def photometry_setting(self):
        self.tess_menu_window_setting.show()

    def add_to_silicups_field(self):
        if self.__photometry_cut[0]:
            star_index = self.graph1_object_combobox.currentIndex()
            self.silicups_window.object1_name_line_edit.setText(self.__photometry_cut[0][star_index].var_id())
            self.silicups_window.object1_name_line_edit.setEnabled(True)
            self.silicups_window.object1_data_name_line_edit.setText(self.__photometry_cut[0][star_index].name())
            self.silicups_window.object1_data_name_line_edit.setEnabled(True)
            self.silicups_window.path_absolute_path_pushbutton.setText(self.tess_import.file_path())
            self.silicups_window.show()

    def add_all_to_silicups_field(self):
        if self.__photometry_cut[0]:
            self.silicups_window.object1_name_line_edit.setText("Add all - Star name")
            self.silicups_window.object1_name_line_edit.setEnabled(False)
            self.silicups_window.object1_data_name_line_edit.setText("Star datafile name")
            self.silicups_window.object1_data_name_line_edit.setEnabled(False)
            self.silicups_window.path_absolute_path_pushbutton.setText(self.tess_import.file_path())
            self.silicups_window.show()

    def create_field(self):
        if self.__photometry_cut[0]:
            self.silicups_window.object1_name_line_edit.setText("Star name")
            self.silicups_window.object1_name_line_edit.setEnabled(False)
            self.silicups_window.object1_data_name_line_edit.setText("Star datafile name")
            self.silicups_window.object1_data_name_line_edit.setEnabled(False)
            self.silicups_window.path_absolute_path_pushbutton.setText(self.tess_import.file_path())
            self.silicups_window.show()

    def edit_tess_data(self):
        star_index = self.graph1_object_combobox.currentIndex()
        if star_index > -1:
            star_photometry = self.__photometry_cut[0][star_index]
            self.tess_photometry_edit_window.sector_index_combobox.clear()
            self.tess_photometry_edit_window.sector_index_combobox.addItems(
                self.__photometry_cut[0][star_index].sectors())
            self.tess_photometry_edit_window.sector_index_combobox.setCurrentIndex(
                self.graph1_sector_combobox.currentIndex())
            self.tess_photometry_edit_window.setWindowTitle("TESS Photometry of the star " + star_photometry.name())
            self.tess_photometry_edit_window.fill(star_photometry)

    def connect_graph(self):
        self.graph1_object_combobox.currentTextChanged.connect(self.star1_was_changed)
        self.graph2_object_combobox.currentTextChanged.connect(self.star2_was_changed)
        self.graph1_sector_combobox.currentTextChanged.connect(self.sector1_changed)
        self.graph2_sector_combobox.currentTextChanged.connect(self.sector2_changed)
        self.graph1_type_combobox.currentTextChanged.connect(self.graf1_changed)
        self.graph2_type_combobox.currentTextChanged.connect(self.graf2_changed)
        self.graph1_zoom_combobox.currentTextChanged.connect(self.graf1_changed)
        self.graph2_zoom_combobox.currentTextChanged.connect(self.graf2_changed)
        self.graph1_disintegrated_x_combobox.currentTextChanged.connect(self.graf1_changed)
        self.graph2_disintegrated_x_combobox.currentTextChanged.connect(self.graf2_changed)
        self.graph1_disintegrated_y_combobox.currentTextChanged.connect(self.graf1_changed)
        self.graph2_disintegrated_y_combobox.currentTextChanged.connect(self.graf2_changed)
        self.window_length_combobox1.currentTextChanged.connect(self.detrend1_was_changed)
        self.polyorder_combobox1.currentTextChanged.connect(self.detrend1_was_changed)
        self.break_tolerance_combobox1.currentTextChanged.connect(self.detrend1_was_changed)
        self.niters_combobox1.currentTextChanged.connect(self.detrend1_was_changed)
        self.sigma_combobox1.currentTextChanged.connect(self.detrend1_was_changed)
        self.window_length_combobox2.currentTextChanged.connect(self.detrend1_was_changed)
        self.polyorder_combobox2.currentTextChanged.connect(self.detrend1_was_changed)
        self.break_tolerance_combobox2.currentTextChanged.connect(self.detrend1_was_changed)
        self.niters_combobox2.currentTextChanged.connect(self.detrend1_was_changed)
        self.sigma_combobox2.currentTextChanged.connect(self.detrend1_was_changed)
        self.perioda_slider.valueChanged.connect(self.slider_was_changed)
        self.multiplication_period_plus.clicked.connect(self.multiply_period)
        self.multiplication_period_minus.clicked.connect(self.period_division)
        self.zero_pushbutton.clicked.connect(self.zero_set)
        self.period_slider_range_combobox.currentTextChanged.connect(self.slider_range_combobox_changed)
        self.clear_changes_pushbutton.clicked.connect(self.clear_changes_clicked)
        self.set_period_pushbutton.clicked.connect(self.set_new_period)

    def disconnect_graph(self):
        self.graph1_object_combobox.disconnect()
        self.graph2_object_combobox.disconnect()
        self.graph1_sector_combobox.disconnect()
        self.graph2_sector_combobox.disconnect()
        self.graph1_type_combobox.disconnect()
        self.graph2_type_combobox.disconnect()
        self.graph1_zoom_combobox.disconnect()
        self.graph2_zoom_combobox.disconnect()
        self.graph1_disintegrated_x_combobox.disconnect()
        self.graph2_disintegrated_x_combobox.disconnect()
        self.graph1_disintegrated_y_combobox.disconnect()
        self.graph2_disintegrated_y_combobox.disconnect()
        self.window_length_combobox1.disconnect()
        self.polyorder_combobox1.disconnect()
        self.break_tolerance_combobox1.disconnect()
        self.niters_combobox1.disconnect()
        self.sigma_combobox1.disconnect()
        self.window_length_combobox2.disconnect()
        self.polyorder_combobox2.disconnect()
        self.break_tolerance_combobox2.disconnect()
        self.niters_combobox2.disconnect()
        self.sigma_combobox2.disconnect()
        self.perioda_slider.disconnect()
        self.multiplication_period_plus.disconnect()
        self.multiplication_period_minus.disconnect()
        self.zero_pushbutton.disconnect()
        self.period_slider_range_combobox.disconnect()
        self.clear_changes_pushbutton.disconnect()
        self.set_period_pushbutton.disconnect()

    def set_photometry_setting(self):
        photometry_setting = []
        for i in range(len(self.user.photometry_setting())):
            if i > 15:
                if self.user.photometry_setting()[i] == "1":
                    photometry_setting.append(True)
                else:
                    photometry_setting.append(False)
            else:
                photometry_setting.append(self.user.photometry_setting()[i])
        self.tess_menu_window_setting.folder_data_pushbutton.setText(photometry_setting[0])
        self.tess_import.change_data_path(photometry_setting[0])
        self.tess_menu_window_setting.folder_files_pushbutton.setText(photometry_setting[1])
        self.tess_import.change_file_path(photometry_setting[1])
        self.tess_menu_window_setting.folder_pictures_pushbutton.setText(photometry_setting[2])
        self.tess_import.change_graph_path(photometry_setting[2])
        self.tess_menu_window_setting.start_position_editline.setText(photometry_setting[3])
        self.tess_menu_window_setting.end_position_editline.setText(photometry_setting[4])
        self.tess_menu_window_setting.percentage_of_erroneous_points_double_spinbox.setValue(float(photometry_setting[5]))
        self.tess_menu_window_setting.extend_mask_spinbox.setValue(int(photometry_setting[8]))
        self.tess_menu_window_setting.quality_bitmask_combobox.setCurrentText(photometry_setting[9])
        self.tess_menu_window_setting.first_downloaded_sector_spinbox.setValue(int(photometry_setting[10]))
        self.tess_menu_window_setting.test_only_sectors_quantity_spinbox.setValue(int(photometry_setting[11]))
        self.tess_menu_window_setting.data_focus_spinbox.setValue(int(photometry_setting[12]))
        self.tess_menu_window_setting.input_file_group_checkbox.setChecked(photometry_setting[16])
        self.tess_menu_window_setting.input_file_format_standard_checkbox.setChecked(photometry_setting[17])
        self.tess_menu_window_setting.input_file_format_sips_checkbox.setChecked(photometry_setting[18])
        self.tess_menu_window_setting.input_file_format_silicups_checkbox.setChecked(photometry_setting[19])
        self.tess_menu_window_setting.input_file_format_field_description_checkbox.setChecked(photometry_setting[20])
        self.tess_menu_window_setting.save_original_data_checkbox.setChecked(photometry_setting[21])
        self.tess_menu_window_setting.save_norm_data_checkbox.setChecked(photometry_setting[22])
        self.tess_menu_window_setting.norm_data_checkbox_changed()
        self.tess_menu_window_setting.save_detrend_data_checkbox.setChecked(photometry_setting[23])
        self.tess_menu_window_setting.save_pictures_checkbox.setChecked(photometry_setting[24])
        self.tess_menu_window_setting.show_picture_origin_checkbox.setChecked(photometry_setting[25])
        self.tess_menu_window_setting.show_picture_detrend_checkbox.setChecked(photometry_setting[26])
        self.tess_menu_window_setting.show_picture_faze_checkbox.setChecked(photometry_setting[27])
        self.tess_menu_window_setting.show_picture_detrend_faze_checkbox.setChecked(photometry_setting[28])
        self.tess_menu_window_setting.show_picture_all_faze_checkbox.setChecked(photometry_setting[29])
        self.tess_menu_window_setting.show_picture_all_detrend_faze_checkbox.setChecked(photometry_setting[30])
        self.tess_menu_window_setting.show_mask_desintegration_checkbox.setChecked(photometry_setting[31])
        self.tess_menu_window_setting.mask_desintegration_checkbox_change()
        self.tess_menu_window_setting.only_new_data_checkbox.setChecked(photometry_setting[33])
        self.tess_menu_window_setting.test_only_checkbox.setChecked(photometry_setting[34])
        self.tess_menu_window_setting.change_focus_by_period.setChecked(photometry_setting[35])
        self.tess_menu_window_setting.find_max_power_period_checkbox.setChecked(photometry_setting[36])
        self.tess_menu_window_setting.change_detrend_parameters_by_period_checkbox.setChecked(photometry_setting[37])
        self.graph1_fix_type_checkbox.setChecked(photometry_setting[38])
        self.graph_same_star_checkbox.setChecked(photometry_setting[39])
        self.graph_double_period_checkbox.setChecked(photometry_setting[40])
        self.graph2_fix_type_checkbox.setChecked(photometry_setting[41])
        self.tess_menu_window_setting.new_data_checkbox_changed()
        self.tess_menu_window_setting.test_only_checkbox_changed()

    def closeEvent(self, a0: QtGui.QCloseEvent):
        self.save_photometry_setting()

    def save_photometry_setting(self):
        photometry_setting = ["", "", "", "0", "0", "0.1", "", "18", "1", "default", "0", "1", "1", "0", "0", "0", True,
                              True, False, False, False, True, True, True, True, True, True, True, True, False, True,
                              False, False, False, False, True, True, True, True, True, True, True]
        photometry_setting[0] = self.tess_menu_window_setting.folder_data_pushbutton.text()
        photometry_setting[1] = self.tess_menu_window_setting.folder_files_pushbutton.text()
        photometry_setting[2] = self.tess_menu_window_setting.folder_pictures_pushbutton.text()
        photometry_setting[3] = self.tess_menu_window_setting.start_position_editline.text()
        photometry_setting[4] = self.tess_menu_window_setting.end_position_editline.text()
        photometry_setting[5] = str(self.tess_menu_window_setting.percentage_of_erroneous_points_double_spinbox.value())
        photometry_setting[8] = str(self.tess_menu_window_setting.extend_mask_spinbox.value())
        photometry_setting[9] = self.tess_menu_window_setting.quality_bitmask_combobox.currentText()
        photometry_setting[10] = str(self.tess_menu_window_setting.first_downloaded_sector_spinbox.value())
        photometry_setting[11] = str(self.tess_menu_window_setting.test_only_sectors_quantity_spinbox.value())
        photometry_setting[12] = str(self.tess_menu_window_setting.data_focus_spinbox.value())
        photometry_setting[16] = self.tess_menu_window_setting.input_file_group_checkbox.isChecked()
        photometry_setting[17] = self.tess_menu_window_setting.input_file_format_standard_checkbox.isChecked()
        photometry_setting[18] = self.tess_menu_window_setting.input_file_format_sips_checkbox.isChecked()
        photometry_setting[19] = self.tess_menu_window_setting.input_file_format_silicups_checkbox.isChecked()
        photometry_setting[20] = self.tess_menu_window_setting.input_file_format_field_description_checkbox.isChecked()
        photometry_setting[21] = self.tess_menu_window_setting.save_original_data_checkbox.isChecked()
        photometry_setting[22] = self.tess_menu_window_setting.save_norm_data_checkbox.isChecked()
        photometry_setting[23] = self.tess_menu_window_setting.save_detrend_data_checkbox.isChecked()
        photometry_setting[24] = self.tess_menu_window_setting.save_pictures_checkbox.isChecked()
        photometry_setting[25] = self.tess_menu_window_setting.show_picture_origin_checkbox.isChecked()
        photometry_setting[26] = self.tess_menu_window_setting.show_picture_detrend_checkbox.isChecked()
        photometry_setting[27] = self.tess_menu_window_setting.show_picture_faze_checkbox.isChecked()
        photometry_setting[28] = self.tess_menu_window_setting.show_picture_detrend_faze_checkbox.isChecked()
        photometry_setting[29] = self.tess_menu_window_setting.show_picture_all_faze_checkbox.isChecked()
        photometry_setting[30] = self.tess_menu_window_setting.show_picture_all_detrend_faze_checkbox.isChecked()
        photometry_setting[31] = self.tess_menu_window_setting.show_mask_desintegration_checkbox.isChecked()
        photometry_setting[33] = self.tess_menu_window_setting.only_new_data_checkbox.isChecked()
        photometry_setting[34] = self.tess_menu_window_setting.test_only_checkbox.isChecked()
        photometry_setting[35] = self.tess_menu_window_setting.change_focus_by_period.isChecked()
        photometry_setting[36] = self.tess_menu_window_setting.find_max_power_period_checkbox.isChecked()
        photometry_setting[37] = self.tess_menu_window_setting.change_detrend_parameters_by_period_checkbox.isChecked()
        photometry_setting[38] = self.graph1_fix_type_checkbox.isChecked()
        photometry_setting[39] = self.graph_same_star_checkbox.isChecked()
        photometry_setting[40] = self.graph_double_period_checkbox.isChecked()
        photometry_setting[41] = self.graph2_fix_type_checkbox.isChecked()
        for i in range(len(photometry_setting)):
            if i > 15:
                if photometry_setting[i]:
                    photometry_setting[i] = "1"
                else:
                    photometry_setting[i] = "0"
        self.user.change_photometry_setting(photometry_setting)

    def forward1_part1_desintegration(self):
        if self.__photometry_cut[0]:
            graph_type = self.graph1_type_combobox.currentText()
            if graph_type == "Mask desintegration":
                y_index = self.graph1_disintegrated_y_combobox.currentIndex()
                y_count = self.graph1_disintegrated_y_combobox.count()
                x_index = self.graph1_disintegrated_x_combobox.currentIndex()
                x_count = self.graph1_disintegrated_x_combobox.count()
                if y_index < y_count - 1:
                    self.graph1_disintegrated_y_combobox.setCurrentIndex(y_index + 1)
                    return
                elif y_index == y_count - 1 and x_index < x_count - 1:
                    self.graph1_disintegrated_y_combobox.setCurrentIndex(0)
                    self.graph1_disintegrated_x_combobox.setCurrentIndex(x_index + 1)
                    return
                else:
                    self.graph1_disintegrated_y_combobox.setCurrentIndex(0)
                    self.graph1_disintegrated_x_combobox.setCurrentIndex(0)
                    self.forward1_part2_graph()
                    return
            else:
                self.forward1_part2_graph()
                return

    def forward1_part2_graph(self):
        if self.graph1_fix_type_checkbox.isChecked():
            self.forward1_part3_part()
            return
        else:
            type_index = self.graph1_type_combobox.currentIndex()
            type_count = self.graph1_type_combobox.count()
            if type_index < type_count - 1:
                self.graph1_type_combobox.setCurrentIndex(type_index + 1)
                return
            else:
                self.graph1_type_combobox.setCurrentIndex(0)
                self.forward1_part3_part()
                return

    def forward1_part3_part(self):
        part_index = self.graph1_zoom_combobox.currentIndex()
        part_count = self.graph1_zoom_combobox.count()
        if part_index < part_count - 1:
            self.graph1_zoom_combobox.setCurrentIndex(part_index + 1)
            return
        else:
            self.graph1_zoom_combobox.setCurrentIndex(0)
            sector_index = self.graph1_sector_combobox.currentIndex()
            sector_count = self.graph1_sector_combobox.count()
            if sector_index < sector_count - 1:
                self.graph1_sector_combobox.setCurrentIndex(sector_index + 1)
                return
            else:
                self.graph1_sector_combobox.setCurrentIndex(0)
                star_index = self.graph1_object_combobox.currentIndex()
                star_count = self.graph1_object_combobox.count()
                if star_index < star_count - 1:
                    self.graph1_object_combobox.setCurrentIndex(star_index + 1)
                    return
                else:
                    r = Popup("The last graph", "This is the last position", buttons="OK".split(","))
                    r.do()
                    return

    def forward2_part1_desintegration(self):
        if self.__photometry_cut[0]:
            graph_type = self.graph2_type_combobox.currentText()
            if graph_type == "Mask desintegration":
                y_index = self.graph2_disintegrated_y_combobox.currentIndex()
                y_count = self.graph2_disintegrated_y_combobox.count()
                x_index = self.graph2_disintegrated_x_combobox.currentIndex()
                x_count = self.graph2_disintegrated_x_combobox.count()
                if y_index < y_count - 1:
                    self.graph2_disintegrated_y_combobox.setCurrentIndex(y_index + 1)
                    return
                elif y_index == y_count - 1 and x_index < x_count - 1:
                    self.graph2_disintegrated_y_combobox.setCurrentIndex(0)
                    self.graph2_disintegrated_x_combobox.setCurrentIndex(x_index + 1)
                    return
                else:
                    self.graph2_disintegrated_y_combobox.setCurrentIndex(0)
                    self.graph2_disintegrated_x_combobox.setCurrentIndex(0)
                    self.forward2_part2_graph()
                    return
            else:
                self.forward2_part2_graph()
                return

    def forward2_part2_graph(self):
        if self.graph2_fix_type_checkbox.isChecked():
            self.forward2_part3_part()
            return
        else:
            type_index = self.graph2_type_combobox.currentIndex()
            type_count = self.graph2_type_combobox.count()
            if type_index < type_count - 1:
                self.graph2_type_combobox.setCurrentIndex(type_index + 1)
                return
            else:
                self.graph2_type_combobox.setCurrentIndex(0)
                self.forward2_part3_part()
                return

    def forward2_part3_part(self):
        part_index = self.graph2_zoom_combobox.currentIndex()
        part_count = self.graph2_zoom_combobox.count()
        if part_index < part_count - 1:
            self.graph2_zoom_combobox.setCurrentIndex(part_index + 1)
            return
        else:
            self.graph2_zoom_combobox.setCurrentIndex(0)
            sector_index = self.graph2_sector_combobox.currentIndex()
            sector_count = self.graph2_sector_combobox.count()
            if sector_index < sector_count - 1:
                self.graph2_sector_combobox.setCurrentIndex(sector_index + 1)
                return
            else:
                self.graph2_sector_combobox.setCurrentIndex(0)
                star_index = self.graph2_object_combobox.currentIndex()
                star_count = self.graph2_object_combobox.count()
                if star_index < star_count - 1:
                    self.graph2_object_combobox.setCurrentIndex(star_index + 1)
                    return
                else:
                    r = Popup("The last graph", "This is the last position", buttons="OK".split(","))
                    r.do()
                    return

    def delete1_star(self):
        if self.__photometry_cut[0]:
            self.disconnect_graph()
            star_index = self.graph1_object_combobox.currentIndex()
            star2_index = self.graph2_object_combobox.currentIndex()
            star2_text = self.graph2_object_combobox.currentText()
            del self.__photometry_cut[0][star_index]
            del self.__photometry_cut[3][star_index]
            self.graph1_object_combobox.clear()
            self.graph2_object_combobox.clear()
            if self.__photometry_cut[0]:
                self.graph1_object_combobox.addItems(self.__photometry_cut[3])
                self.graph2_object_combobox.addItems(self.__photometry_cut[3])
                if star_index < len(self.__photometry_cut[3]):
                    self.graph1_object_combobox.setCurrentIndex(star_index)
                else:
                    self.graph1_object_combobox.setCurrentIndex(0)
                self.connect_graph()
                self.fill_graph1()
                if star_index == star2_index:
                    self.graph2_object_combobox.setCurrentText(self.graph1_object_combobox.currentText())
                    self.fill_graph2()
                else:
                    self.graph2_object_combobox.setCurrentText(star2_text)
            else:
                self.graph1_sector_combobox.clear()
                self.graph1_zoom_combobox.clear()
                self.graph1_type_combobox.clear()
                self.graph1_disintegrated_x_combobox.clear()
                self.graph1_disintegrated_y_combobox.clear()
                self.graph2_sector_combobox.clear()
                self.graph2_zoom_combobox.clear()
                self.graph2_type_combobox.clear()
                self.graph2_disintegrated_x_combobox.clear()
                self.graph2_disintegrated_y_combobox.clear()
                self.graph2.figure.clear()
                self.graph1.figure.clear()
                self.connect_graph()

    def delete2_star(self):
        if self.__photometry_cut[0]:
            self.disconnect_graph()
            star_index = self.graph2_object_combobox.currentIndex()
            star2_index = self.graph1_object_combobox.currentIndex()
            star2_text = self.graph1_object_combobox.currentText()
            del self.__photometry_cut[0][star_index]
            del self.__photometry_cut[3][star_index]
            self.graph2_object_combobox.clear()
            self.graph1_object_combobox.clear()
            if self.__photometry_cut[0]:
                self.graph2_object_combobox.addItems(self.__photometry_cut[3])
                self.graph1_object_combobox.addItems(self.__photometry_cut[3])
                if star_index < len(self.__photometry_cut[3]):
                    self.graph2_object_combobox.setCurrentIndex(star_index)
                else:
                    self.graph2_object_combobox.setCurrentIndex(0)
                self.connect_graph()
                self.fill_graph2()
                if star_index == star2_index:
                    self.graph1_object_combobox.setCurrentText(self.graph2_object_combobox.currentText())
                    self.fill_graph1()
                else:
                    self.graph1_object_combobox.setCurrentText(star2_text)
            else:
                self.graph2_sector_combobox.clear()
                self.graph2_zoom_combobox.clear()
                self.graph2_type_combobox.clear()
                self.graph2_disintegrated_x_combobox.clear()
                self.graph2_disintegrated_y_combobox.clear()
                self.graph1_sector_combobox.clear()
                self.graph1_zoom_combobox.clear()
                self.graph1_type_combobox.clear()
                self.graph1_disintegrated_x_combobox.clear()
                self.graph1_disintegrated_y_combobox.clear()
                self.graph1.figure.clear()
                self.graph2.figure.clear()
                self.connect_graph()

    def delete1_sector(self):
        if self.__photometry_cut[0]:
            if self.graph1_sector_combobox.count() == 1:
                self.delete1_star()
            else:
                self.disconnect_graph()
                sector_index = self.graph1_sector_combobox.currentIndex()
                star_index = self.graph1_object_combobox.currentIndex()
                del self.__photometry_cut[0][star_index].sectors()[sector_index]
                del self.__photometry_cut[0][star_index].lightcurves()[sector_index]
                del self.__photometry_cut[0][star_index].tess_cut_set()[sector_index]
                self.graph1_sector_combobox.clear()
                self.graph1_sector_combobox.addItems(self.__photometry_cut[0][star_index].sectors())
                star_graph_2_index = self.graph2_object_combobox.currentIndex()
                self.connect_graph()
                if len(self.__photometry_cut[0][star_graph_2_index].sectors()) != self.graph2_sector_combobox.count():
                    self.graph2_sector_combobox.clear()
                    self.graph2_sector_combobox.addItems(self.__photometry_cut[0][star_index].sectors())
                self.show_graph1()

    def delete2_sector(self):
        if self.__photometry_cut[0]:
            if self.graph2_sector_combobox.count() == 1:
                self.delete2_star()
            else:
                self.disconnect_graph()
                sector_index = self.graph2_sector_combobox.currentIndex()
                star_index = self.graph2_object_combobox.currentIndex()
                del self.__photometry_cut[0][star_index].sectors()[sector_index]
                del self.__photometry_cut[0][star_index].lightcurves()[sector_index]
                del self.__photometry_cut[0][star_index].tess_cut_set()[sector_index]
                self.graph2_sector_combobox.clear()
                self.graph2_sector_combobox.addItems(self.__photometry_cut[0][star_index].sectors())
                star_graph_1_index = self.graph1_object_combobox.currentIndex()
                self.connect_graph()
                if len(self.__photometry_cut[0][star_graph_1_index].sectors()) != self.graph1_sector_combobox.count():
                    self.graph1_sector_combobox.clear()
                    self.graph1_sector_combobox.addItems(self.__photometry_cut[0][star_index].sectors())
                self.show_graph2()

    def double_period(self):
        self.show_graph1()
        self.show_graph2()

    def set_same_star(self):
        star_index = self.graph1_object_combobox.currentIndex()
        if self.graph_same_star_checkbox.isChecked() and star_index != self.graph2_object_combobox.currentIndex():
            self.graph2_object_combobox.setCurrentIndex(star_index)

    def graf1_changed(self):
        self.show_graph1()

    def graf2_changed(self):
        self.show_graph2()

    def sector1_changed(self):
        self.__mask_desintegration_set1.clear()
        self.fill_period_window()
        self.show_graph1()

    def sector2_changed(self):
        self.__mask_desintegration_set2.clear()
        self.show_graph2()

    def mask_desintegration_set1(self):
        return self.__mask_desintegration_set1

    def change_mask_desintegration_set1(self, new):
        self.__mask_desintegration_set1 = new

    def mask_desintegration_set2(self):
        return self.__mask_desintegration_set2

    def change_mask_desintegration_set2(self, new):
        self.__mask_desintegration_set2 = new

    def photometry_cut(self):
        return self.__photometry_cut

    def change_photometry_cut(self, new):
        self.__photometry_cut = new

    def lc_part(self, corr_lc, data_focus, part_lc_number):
        lc_part_length = int(len(corr_lc) / data_focus)
        if lc_part_length < 100:
            lc_part_length = 100
        start_of_part = 0
        part = 1
        part_lc = corr_lc
        while start_of_part < len(corr_lc):
            end_of_part = start_of_part + lc_part_length
            if end_of_part + data_focus * 20 > len(corr_lc):
                end_of_part = len(corr_lc)
            part_lc = corr_lc[start_of_part:end_of_part]
            if part == part_lc_number:
                return part_lc
            start_of_part = end_of_part
            part = part + 1
        return part_lc

    def save_all(self):
        self.__save_star(-1)

    def save_current_star(self):
        self.__save_star(self.graph1_object_combobox.currentIndex())

    def save_current_sector(self):
        self.__save_star(self.graph1_object_combobox.currentIndex(),
                         saved_sector=self.graph1_sector_combobox.currentText())

    def __save_star(self, star_index, saved_sector="all"):
        current_coor = self.__photometry_cut[0][star_index].coor()
        origin = self.tess_menu_window_setting.save_original_data_checkbox.isChecked()
        normalized = self.tess_menu_window_setting.save_norm_data_checkbox.isChecked()
        detrended = self.tess_menu_window_setting.save_detrend_data_checkbox.isChecked()
        pictures = self.tess_menu_window_setting.save_pictures_checkbox.isChecked()
        pictures_folder = self.tess_menu_window_setting.folder_pictures_pushbutton.text()
        if not os.path.exists(pictures_folder):
            mistake = Popup("Saving error",
                            "Failed to create folder\n{0}\nPlease check your permissions.".format(pictures_folder),
                            buttons="OK".split(","))
            mistake.do()
            return
        file_folder = self.tess_menu_window_setting.folder_files_pushbutton.text()
        if not os.path.exists(file_folder):
            mistake = Popup("Saving error",
                            "Failed to create folder\n{0}\nPlease check your permissions.".format(file_folder),
                            buttons="OK".split(","))
            mistake.do()
            return
        graph_origin = self.tess_menu_window_setting.show_picture_origin_checkbox.isChecked()
        graph_detrended = self.tess_menu_window_setting.show_picture_detrend_checkbox.isChecked()
        graph_faze = self.tess_menu_window_setting.show_picture_faze_checkbox.isChecked()
        graph_detrended_faze = self.tess_menu_window_setting.show_picture_detrend_faze_checkbox.isChecked()
        graph_faze_all = self.tess_menu_window_setting.show_picture_all_faze_checkbox.isChecked()
        graph_detrended_faze_all = self.tess_menu_window_setting.show_picture_all_detrend_faze_checkbox.isChecked()
        for k, star in enumerate(self.__photometry_cut[0]):
            if star_index >= 0:
                p_value = int(self.polyorder_combobox1.currentText())
                b_value = int(self.break_tolerance_combobox1.currentText())
                n_value = int(self.niters_combobox1.currentText())
                s_value = int(self.sigma_combobox1.currentText())
                w_value = int(self.window_length_combobox1.currentText())
            else:
                p_value = 2
                b_value = 5
                n_value = 3
                s_value = 3
                w_value = -1
            if star_index < 0 or current_coor == self.__photometry_cut[0][k].coor():
                pair_a = True


                if k > 0:
                    if star.coor() == self.__photometry_cut[0][k-1].coor() and star_index < 0:
                        pair_a = False
                zoom_list = self.__zoom_list(star.lightcurves()[0][4])
                aperture_star = int(star.mx()) * int(star.my())
                aperture_cmp = int(star.cut_size())**2
                star_name = star.var_id()
                star_mag = str(star.mag())
                coor_list = star.coor().split(" ")
                if '' in coor_list:
                    index = coor_list.index('')
                    del (coor_list[index])
                rektascenze = coor_list[0] + ":" + coor_list[1] + ":" + coor_list[2]
                declination = coor_list[3] + ":" + coor_list[4] + ":" + coor_list[5]

                if self.metadata_checkbox.isChecked():
                    metadata_text = "VarAperture: " + str(aperture_star) \
                                    + "CmpAperture: " + str(aperture_cmp) \
                                    + "JD: heliocentric Unit: flux Filter: Lum\n VAR Name: " + star_name \
                                    + "RA: " + rektascenze \
                                    + "Dec: " + declination \
                                    + "Catalog: TIC CatalogRA: " + rektascenze + " CatalogDec: " + declination \
                                    + "CatalogMag: " + star_mag
                else:
                    metadata_text = None

                star.save_all(origin=origin, normalized=normalized, detrended=detrended, pictures=pictures,
                              pictures_folder=pictures_folder, file_folder=file_folder, graph_origin=graph_origin,
                              graph_detrended=graph_detrended, graph_faze=graph_faze, graph_faze_all=graph_faze_all,
                              graph_detrended_faze=graph_detrended_faze, graph_detrended_faze_all=graph_detrended_faze_all,
                              part_info=zoom_list, pair_a=pair_a, metadata=metadata_text, wl=w_value, p=p_value,
                              b=b_value, n=n_value, s=s_value, saved_sector=saved_sector)
        mistake = Popup("File was saved",
                        "Photometric protocols were stored",
                        buttons="OK".split(","))
        mistake.do()

    def upload_photometry(self):
        self.tess_import.set_photometry_parameters()
        self.tess_import.select_star_for_photometry()


    def show_photometry(self):
        self.change_photometry_cut([self.tess_import.tpfs_list, self.tess_import.stars_without_data,
                                    self.tess_import.stars_with_error, self.tess_import.star_names])
        self.photometry_star_list_window.photometry_button.setText("Start Upload")
        self.graph1_object_combobox.clear()
        self.graph2_object_combobox.clear()
        self.star_without_data_combobox.clear()
        self.star_with_mistake_data_combobox.clear()
        if self.__photometry_cut[0]:
            self.graph1_object_combobox.addItems(self.__photometry_cut[3])
            self.graph2_object_combobox.addItems(self.__photometry_cut[3])
            self.edit_tess_data_pushbutton.setEnabled(True)
            self.save_pushbutton.setEnabled(True)
            self.save_star_pushbutton.setEnabled(True)
            self.save_sector_pushbutton.setEnabled(True)
            self.add_to_fild_pushbutton.setEnabled(True)
            self.add_all_to_fild_pushbutton.setEnabled(True)
            self.create_fild_pushbutton.setEnabled(True)
        else:
            self.graph1_sector_combobox.clear()
            self.graph1_zoom_combobox.clear()
            self.graph1_type_combobox.clear()
            self.graph1.axes.cla()
            self.graph2_sector_combobox.clear()
            self.graph2_zoom_combobox.clear()
            self.graph2_type_combobox.clear()
            self.graph2.axes.cla()
            self.edit_tess_data_pushbutton.setEnabled(False)
            self.save_pushbutton.setEnabled(False)
            self.save_star_pushbutton.setEnabled(False)
            self.save_sector_pushbutton.setEnabled(False)
            self.add_to_fild_pushbutton.setEnabled(False)
            self.add_all_to_fild_pushbutton.setEnabled(False)
            self.create_fild_pushbutton.setEnabled(False)
            info = Popup("No star", "There are no stars or coordinates in file\nor or the wrong format was selected", buttons="OK".split(","))
            info.do()
        if self.__photometry_cut[1]:
            self.star_without_data_combobox.addItems(self.__photometry_cut[1])
        if self.__photometry_cut[2]:
            self.star_with_mistake_data_combobox.addItems(self.__photometry_cut[2])

    def star1_was_changed(self):
        self.fill_graph1()

    def star2_was_changed(self):
        self.fill_graph2()

    def __zoom_list(self, period):
        zoom_list = []
        if self.tess_menu_window_setting.change_focus_by_period.isChecked() and period:
            if period < 0.15:
                zoom_list = ["1", "2", "3", "4", "5", "6", "7"]
            elif 0.15 <= period < 0.2:
                zoom_list = ["1", "2", "3", "4", "5", "6"]
            elif 0.2 <= period < 0.25:
                zoom_list = ["1", "2", "3", "4", "5"]
            elif 0.25 <= period < 0.3:
                zoom_list = ["1", "2", "3", "4"]
            elif 0.3 <= period < 0.5:
                zoom_list = ["1", "2", "3"]
            elif 0.5 <= period < 1:
                zoom_list = ["1", "2"]
            else:
                zoom_list = ["1"]
        else:
            for i in range(1, self.tess_menu_window_setting.data_focus_spinbox.value() + 1):
                zoom_list.append(str(i))
        return zoom_list

    def fill_graph1(self):
        if self.__photometry_cut[0]:
            self.disconnect_graph()
            star_index = self.graph1_object_combobox.currentIndex()
            if self.graph1_type_combobox.count():
                current_graph_type = self.graph1_type_combobox.currentText()
            else:
                current_graph_type = None
            self.graph1_sector_combobox.clear()
            self.graph1_zoom_combobox.clear()
            self.graph1_type_combobox.clear()
            self.graph1_disintegrated_x_combobox.clear()
            self.graph1_disintegrated_y_combobox.clear()
            self.graph1_sector_combobox.addItems(self.__photometry_cut[0][star_index].sectors())
            sector_index = self.graph1_sector_combobox.currentIndex()
            period = self.__photometry_cut[0][star_index].lightcurves()[sector_index][4]
            zoom_list = self.__zoom_list(period)
            self.graph1_zoom_combobox.addItems(zoom_list)
            self.graph1_type_combobox.addItem("TESS cut view")
            if self.tess_menu_window_setting.show_picture_origin_checkbox.isChecked():
                self.graph1_type_combobox.addItem("Original data")
            if self.tess_menu_window_setting.show_picture_detrend_checkbox.isChecked():
                self.graph1_type_combobox.addItem("Detrended data")
            if self.tess_menu_window_setting.show_picture_faze_checkbox.isChecked():
                self.graph1_type_combobox.addItem("Phased")
            if self.tess_menu_window_setting.show_picture_detrend_faze_checkbox.isChecked():
                self.graph1_type_combobox.addItem("Phased and detrended")
            if self.tess_menu_window_setting.show_picture_all_faze_checkbox.isChecked():
                self.graph1_type_combobox.addItem("Phased All")
            if self.tess_menu_window_setting.show_picture_all_detrend_faze_checkbox.isChecked():
                self.graph1_type_combobox.addItem("Phased and detrended all")
            if self.tess_menu_window_setting.show_mask_desintegration_checkbox.isChecked():
                self.graph1_type_combobox.addItem("Mask desintegration")
            if self.graph1_fix_type_checkbox.isChecked() and current_graph_type:
                self.graph1_type_combobox.setCurrentText(current_graph_type)
            x = self.__photometry_cut[0][star_index].x()
            y = self.__photometry_cut[0][star_index].y()
            mx = self.__photometry_cut[0][star_index].mx()
            my = self.__photometry_cut[0][star_index].my()
            cut_size = self.__photometry_cut[0][star_index].cut_size()
            self.window_length_combobox1.setCurrentText(str(self.__photometry_cut[0][star_index].lightcurves()[sector_index][6]))
            self.polyorder_combobox1.setCurrentText("2")
            self.break_tolerance_combobox1.setCurrentText("5")
            self.niters_combobox1.setCurrentText("3")
            self.sigma_combobox1.setCurrentText("3")

            self.graph1_mask_position_label.setText("Mask coor(x,y): " + str(x) + "," + str(y))
            self.graph1_mask_size_label.setText("Mask size: " + str(mx) + "x" + str(my) + " px")
            self.graph1_tess_cut_size_label.setText("Cut size: " + str(cut_size) + "x" + str(cut_size) + " px")
            x_pixels = []
            y_pixels = []
            extend_mask = self.tess_menu_window_setting.extend_mask_spinbox.value()
            for i in range(x - extend_mask, x + mx + extend_mask):
                x_pixels.append(str(i))
            for j in range(y - extend_mask, y + my + extend_mask):
                y_pixels.append(str(j))
            self.graph1_disintegrated_x_combobox.addItems(x_pixels)
            self.graph1_disintegrated_y_combobox.addItems(y_pixels)
            self.graph1_disintegrated_x_combobox.setEnabled(False)
            self.graph1_disintegrated_y_combobox.setEnabled(False)
            self.__mask_desintegration_set1.clear()
            self.connect_graph()
            if self.graph_same_star_checkbox.isChecked() and star_index != self.graph2_object_combobox.currentIndex():
                self.graph2_object_combobox.setCurrentIndex(star_index)
            self.fill_period_window()
            self.show_graph1()

    def set_new_period(self):
        star_index = self.graph1_object_combobox.currentIndex()
        if star_index > -1:
            sector_quantity = len(self.__photometry_cut[0][star_index].lightcurves())
            for i in range(sector_quantity):
                self.__photometry_cut[0][star_index].lightcurves()[i][4] = self.current_period
            self.star1_was_changed()
            self.clear_changes_clicked()


    def fill_period_window(self):
        if self.__photometry_cut[0]:
            star_index = self.graph1_object_combobox.currentIndex()
            sector_index = self.graph1_sector_combobox.currentIndex()
            period = self.__photometry_cut[0][star_index].lightcurves()[sector_index][4]
            try:
                epoch = float(self.__photometry_cut[0][star_index].epoch())

                # ochrana proti dvojnásobné a nebo žádné redukci
                if epoch < 1000000:
                    epoch = epoch -2457000
                elif epoch < -1000000:
                    epoch = epoch + 2457000
            except:
                epoch = 2457000
            self.origin_epoch = epoch
            self.new_epoch = epoch
            self.origin_period = period
            self.current_period = period
            self.fill_period_changer()
            jd_start = self.__photometry_cut[0][star_index].lightcurves()[sector_index][1]
            self.new_epoch = ceil((jd_start - epoch) / epoch) * period + epoch

    def show_graph1(self):
        if self.__photometry_cut[0]:
            self.toolbar_graf1.hide()
            self.graph1.figure.clear()
            self.graph1 = MplCanvas(self, width=10, height=4, dpi=100)
            self.toolbar_graf1 = NavigationToolbar(self.graph1, self)
            self.toolbar1_layout.addWidget(self.toolbar_graf1, 0, 0)
            self.toolbar1_layout.addWidget(self.graph1, 1, 0)

            self.graph1_disintegrated_x_combobox.setEnabled(False)
            self.graph1_disintegrated_y_combobox.setEnabled(False)
            star_index = self.graph1_object_combobox.currentIndex()
            sector_index = self.graph1_sector_combobox.currentIndex()
            graph_type = self.graph1_type_combobox.currentText()
            part = self.graph1_zoom_combobox.currentText()
            coor = self.__photometry_cut[0][star_index].coor()
            jd_start = self.__photometry_cut[0][star_index].lightcurves()[sector_index][1]
            jd_end = self.__photometry_cut[0][star_index].lightcurves()[sector_index][2]
            sector = self.__photometry_cut[0][star_index].lightcurves()[sector_index][3]
            w_value = int(self.window_length_combobox1.currentText())
            p_value = int(self.polyorder_combobox1.currentText())
            b_value = int(self.break_tolerance_combobox1.currentText())
            n_value = int(self.niters_combobox1.currentText())
            s_value = int(self.sigma_combobox1.currentText())

            period = self.__photometry_cut[0][star_index].lightcurves()[sector_index][4]

            if self.graph_double_period_checkbox.isChecked():
                period_graph = self.current_period * 2
            else:
                period_graph = self.current_period
            try:
                epoch = self.new_epoch

                # ochrana proti dvojnásobné a nebo žádné redukci
                if epoch < 1000000:
                    epoch = epoch -2457000
                elif epoch < -1000000:
                    epoch = epoch + 2457000
            except:
                epoch = 2457000

            description = self.__photometry_cut[0][star_index].description()
            lightcurve = self.__photometry_cut[0][star_index].lightcurves()[sector_index][0]
            if self.graph1_zoom_combobox.count() > 1:
                lc_part = self.lc_part(lightcurve, self.graph1_zoom_combobox.count(), self.graph1_zoom_combobox.currentIndex())
            else:
                lc_part = lightcurve

            target_mask = self.__photometry_cut[0][star_index].lightcurves()[sector_index][5]
            self.graph1_period_label.setText(str(period))
            self.graph1_epoch_label.setText(str(epoch))
            self.graph1_start_date_label.setText(str(jd_start) + "  UTC: " + jd_to_date(jd_start).strftime("%d.%m.%Y %H:%M"))
            self.graph1_end_date_label.setText(str(jd_end) + "  UTC: " + jd_to_date(jd_end).strftime("%d.%m.%Y %H:%M"))

            self.graph1.axes.set_title(description)
            if graph_type == "Original data":
                lc_part.plot(ax=self.graph1.axes, ylabel=coor + "\nJD:" + str(jd_start) + "-" + str(jd_end),
                                xlabel="Data sector " + str(sector) + "_" + str(part))

            if graph_type == "Detrended data":
                lc_part.flatten(window_length=w_value,
                                polyorder=p_value,
                                break_tolerance=b_value,
                                niters=n_value,
                                sigma=s_value).plot(ax=self.graph1.axes, ylabel=coor + "\nJD:" + str(jd_start)
                                                                                           + "-" + str(jd_end),
                                                               xlabel="Detrended data sector " + str(sector) + "_"
                                                                      + str(part))

            if graph_type == "Phased":
                lightcurve.fold(period_graph, epoch_time=float(epoch) - 2457000, normalize_phase=True).scatter(
                    ax=self.graph1.axes, xlabel="Phased data sector " + str(sector))



            if graph_type == "Phased and detrended":
                lightcurve.flatten(window_length=w_value,
                                   polyorder=p_value,
                                   break_tolerance=b_value,
                                   niters=n_value,
                                   sigma=s_value).fold(
                    period_graph, epoch_time=float(epoch) - 2457000, normalize_phase=True).scatter(
                    ax=self.graph1.axes, xlabel="Phased and detrend data sector " + str(sector))

            if graph_type == "Phased All" or graph_type == "Phased and detrended all":
                lightcurve_set = self.__photometry_cut[0][star_index].lightcurves()
                main_lc = lightcurve_set[0][0]
                if len(lightcurve_set) > 1:
                    for i in range(1, len(lightcurve_set)):
                        main_lc = main_lc.append(lightcurve_set[i][0])
                if graph_type == "Phased All":
                    main_lc.fold(period_graph, epoch_time=float(epoch) - 2457000, normalize_phase=True).scatter(
                        ax=self.graph1.axes, xlabel="Phased data all sectors ")
                else:
                    main_lc.flatten(window_length=w_value,
                                    polyorder=p_value,
                                    break_tolerance=b_value,
                                    niters=n_value,
                                    sigma=s_value).\
                        fold(period_graph, epoch_time=float(epoch) - 2457000, normalize_phase=True).\
                        scatter(ax=self.graph1.axes, xlabel="Phased detrended data all sectors ")

            if graph_type == "TESS cut view":
                self.__photometry_cut[0][star_index].tess_cut_set()[sector_index].plot(ax=self.graph1.axes, aperture_mask=target_mask, mask_color='r')
                matplotlib.pyplot.close(1)

            if graph_type == "Mask desintegration":
                self.graph1_disintegrated_x_combobox.setEnabled(True)
                self.graph1_disintegrated_y_combobox.setEnabled(True)
                x = self.graph1_disintegrated_x_combobox.currentText()
                y = self.graph1_disintegrated_y_combobox.currentText()
                extend_mask = self.tess_menu_window_setting.extend_mask_spinbox.value()
                x_zero = self.__photometry_cut[0][star_index].x() - extend_mask
                y_zero = self.__photometry_cut[0][star_index].y() - extend_mask
                x_index = self.graph1_disintegrated_x_combobox.currentIndex()
                y_index = self.graph1_disintegrated_y_combobox.currentIndex()
                x_count = self.graph1_disintegrated_x_combobox.count()
                y_count = self.graph1_disintegrated_y_combobox.count()
                lc_index = x_index * y_count + y_index
                name = self.graph1_object_combobox.currentText()
                if not self.__mask_desintegration_set1:
                    tpfs = self.__photometry_cut[0][star_index]
                    tpfs.set_lc_parameters()
                    for i in range(x_count):
                        for j in range(y_count):
                            self.__mask_desintegration_set1.append(
                                tpfs.give_lightcurve(sector_index, lightcurve_type="desintegration",
                                                     pixel_x=x_zero + i, pixel_y=y_zero + j))
                if self.graph1_zoom_combobox.count() > 1:
                    lc_part = self.lc_part(self.__mask_desintegration_set1[lc_index], self.graph1_zoom_combobox.count(),
                                      self.graph1_zoom_combobox.currentIndex())
                else:
                    lc_part = self.__mask_desintegration_set1[lc_index]

                lc_part.plot(ax=self.graph1.axes, ylabel="Mask desintegration\nPixel:" + x + ";" + y + "  SECTOR:"
                                                         + str(sector), xlabel=name + "  part:" + part)
            if graph_type == "Gaia interaction":
                pass
            self.graph1.draw()

    def fill_graph2(self):
        if self.__photometry_cut[0]:
            self.disconnect_graph()
            star_index = self.graph2_object_combobox.currentIndex()
            if self.graph2_type_combobox.count():
                current_graph_type = self.graph2_type_combobox.currentText()
            else:
                current_graph_type = None
            self.graph2_sector_combobox.clear()
            self.graph2_zoom_combobox.clear()
            self.graph2_type_combobox.clear()
            self.graph2_disintegrated_x_combobox.clear()
            self.graph2_disintegrated_y_combobox.clear()
            self.graph2_sector_combobox.addItems(self.__photometry_cut[0][star_index].sectors())
            sector_index = self.graph2_sector_combobox.currentIndex()
            period = self.__photometry_cut[0][star_index].lightcurves()[sector_index][4]
            zoom_list = self.__zoom_list(period)
            self.graph2_zoom_combobox.addItems(zoom_list)
            self.graph2_type_combobox.addItem("TESS cut view")
            if self.tess_menu_window_setting.show_picture_origin_checkbox.isChecked():
                self.graph2_type_combobox.addItem("Original data")
            if self.tess_menu_window_setting.show_picture_detrend_checkbox.isChecked():
                self.graph2_type_combobox.addItem("Detrended data")
            if self.tess_menu_window_setting.show_picture_faze_checkbox.isChecked():
                self.graph2_type_combobox.addItem("Phased")
            if self.tess_menu_window_setting.show_picture_detrend_faze_checkbox.isChecked():
                self.graph2_type_combobox.addItem("Phased and detrended")
            if self.tess_menu_window_setting.show_picture_all_faze_checkbox.isChecked():
                self.graph2_type_combobox.addItem("Phased All")
            if self.tess_menu_window_setting.show_picture_all_detrend_faze_checkbox.isChecked():
                self.graph2_type_combobox.addItem("Phased and detrended all")
            if self.tess_menu_window_setting.show_mask_desintegration_checkbox.isChecked():
                self.graph2_type_combobox.addItem("Mask desintegration")
            if self.graph2_fix_type_checkbox.isChecked() and current_graph_type:
                self.graph2_type_combobox.setCurrentText(current_graph_type)
            x = self.__photometry_cut[0][star_index].x()
            y = self.__photometry_cut[0][star_index].y()
            mx = self.__photometry_cut[0][star_index].mx()
            my = self.__photometry_cut[0][star_index].my()
            cut_size = self.__photometry_cut[0][star_index].cut_size()
            self.window_length_combobox2.setCurrentText(str(self.__photometry_cut[0][star_index].lightcurves()[sector_index][6]))
            self.polyorder_combobox2.setCurrentText("2")
            self.break_tolerance_combobox2.setCurrentText("5")
            self.niters_combobox2.setCurrentText("3")
            self.sigma_combobox2.setCurrentText("3")
            self.graph2_mask_position_label.setText("Mask coor(x,y): " + str(x) + "," + str(y))
            self.graph2_mask_size_label.setText("Mask size: " + str(mx) + "x" + str(my) + " px")
            self.graph2_tess_cut_size_label.setText("Cut size: " + str(cut_size) + "x" + str(cut_size) + " px")
            x_pixels = []
            y_pixels = []
            extend_mask = self.tess_menu_window_setting.extend_mask_spinbox.value()
            for i in range(x - extend_mask, x + mx + extend_mask):
                x_pixels.append(str(i))
            for j in range(y - extend_mask, y + my + extend_mask):
                y_pixels.append(str(j))
            self.graph2_disintegrated_x_combobox.addItems(x_pixels)
            self.graph2_disintegrated_y_combobox.addItems(y_pixels)
            self.graph2_disintegrated_x_combobox.setEnabled(False)
            self.graph2_disintegrated_y_combobox.setEnabled(False)
            self.__mask_desintegration_set2.clear()
            self.connect_graph()
            if self.graph_same_star_checkbox.isChecked() and star_index != self.graph1_object_combobox.currentIndex():
                self.graph1_object_combobox.setCurrentIndex(star_index)
            self.show_graph2()

    def detrend1_was_changed(self):
        if self.graph1_type_combobox.currentText() in ["Detrended data", "Phased and detrended",
                                                       "Phased and detrended all"]:
            self.show_graph1()

    def multiply_period(self):
        if self.graph1_period_label.text() != "":
            self.period_multiplicity = self.period_multiplicity + 1
            self.period_was_changed()
            self.change_graph()

    def period_division(self):
        if self.graph1_period_label.text() != "":
            self.period_multiplicity = self.period_multiplicity - 1
            self.period_was_changed()
            self.change_graph()

    def zero_set(self):
       self.perioda_slider.setValue(0)
       self.period_was_changed()
       self.change_graph()

    def period_was_changed(self):
        self.current_period = self.perioda_slider.value() * self.slider_range / 1000 + self.slider_history + self.origin_period * 2 ** self.period_multiplicity
        self.current_period_label.setText(str(self.current_period))

    def slider_was_changed(self):
       self.period_was_changed()
       self.change_graph()

    def change_graph(self):
        if self.graph1_type_combobox.currentText() in ["Phased", "Phased and detrended", "Phased All",
                                                           "Phased and detrended all"]:
            self.show_graph1()

    def slider_range_combobox_changed(self):
        self.slider_history = self.slider_history + self.slider_range * self.perioda_slider.value() / 1000
        self.slider_range = float(self.period_slider_range_combobox.currentText())
        self.perioda_slider.setValue(0)

    def clear_changes_clicked(self):
        self.slider_history = 0
        self.period_multiplicity = 0
        self.zero_set()

    def fill_period_changer(self):
        self.clear_changes_clicked()
        self.current_period_label.setText(str(self.origin_period))

    def show_graph2(self):
        if self.__photometry_cut[0]:
            self.toolbar_graf2.hide()
            self.graph2.figure.clear()
            self.graph2 = MplCanvas(self, width=10, height=4, dpi=100)
            self.toolbar_graf2 = NavigationToolbar(self.graph2, self)
            self.toolbar2_layout.addWidget(self.toolbar_graf2, 0, 0)
            self.toolbar2_layout.addWidget(self.graph2, 1, 0)
            self.graph2_disintegrated_x_combobox.setEnabled(False)
            self.graph2_disintegrated_y_combobox.setEnabled(False)
            star_index = self.graph2_object_combobox.currentIndex()
            sector_index = self.graph2_sector_combobox.currentIndex()
            graph_type = self.graph2_type_combobox.currentText()
            part = str(self.graph2_zoom_combobox.currentText())
            coor = self.__photometry_cut[0][star_index].coor()
            jd_start = self.__photometry_cut[0][star_index].lightcurves()[sector_index][1]
            jd_end = self.__photometry_cut[0][star_index].lightcurves()[sector_index][2]
            sector = self.__photometry_cut[0][star_index].lightcurves()[sector_index][3]
            w_value = int(self.window_length_combobox2.currentText())
            p_value = int(self.polyorder_combobox2.currentText())
            b_value = int(self.break_tolerance_combobox2.currentText())
            n_value = int(self.niters_combobox2.currentText())
            s_value = int(self.sigma_combobox2.currentText())

            period = self.__photometry_cut[0][star_index].lightcurves()[sector_index][4]
            period_slider = 0 # period + self.perioda2_slider.value() * float(self.period_slider_range_combobox2.currentText()) / 1000
            if self.graph_double_period_checkbox.isChecked():
                period_graph = (period + period_slider) * 2
            else:
                period_graph = period + period_slider
            try:
                epoch = float(self.__photometry_cut[0][star_index].epoch())

                # ochrana proti dvojnásobné a nebo žádné redukci
                if epoch < 1000000:
                    epoch = epoch -2457000
                elif epoch < -1000000:
                    epoch = epoch + 2457000

            except:
                epoch = 2457000

            description = self.__photometry_cut[0][star_index].description()
            lightcurve = self.__photometry_cut[0][star_index].lightcurves()[sector_index][0]
            if self.graph2_zoom_combobox.count() > 1:
                lc_part = self.lc_part(lightcurve, self.graph2_zoom_combobox.count(),
                                       self.graph2_zoom_combobox.currentIndex())
            else:
                lc_part = lightcurve
            target_mask = self.__photometry_cut[0][star_index].lightcurves()[sector_index][5]
            self.graph2_period_label.setText(str(period))
            self.graph2_epoch_label.setText(str(epoch))
            self.graph2_start_date_label.setText(str(jd_start)
                                                 + "  UTC: " + jd_to_date(jd_start).strftime("%d.%m.%Y %H:%M"))
            self.graph2_end_date_label.setText(str(jd_end)
                                               + "  UTC: " + jd_to_date(jd_end).strftime("%d.%m.%Y %H:%M"))

            self.graph2.axes.set_title(description)
            if graph_type == "Original data":
                lc_part.plot(ax=self.graph2.axes, ylabel=coor + "\nJD:" + str(jd_start) + "-" + str(jd_end),
                             xlabel="Data sector " + str(sector) + "_" + str(part))
            if graph_type == "Detrended data":
                lc_part.flatten(window_length=w_value,
                                polyorder=p_value,
                                break_tolerance=b_value,
                                niters=n_value,
                                sigma=s_value).plot(
                    ax=self.graph2.axes, ylabel=coor + "\nJD:" + str(jd_start) + "-" + str(jd_end),
                    xlabel="Detrended data sector " + str(sector) + "_" + str(part))
            if graph_type == "Phased":
                lightcurve.fold(period_graph, epoch_time=float(epoch) - 2457000, normalize_phase=True).scatter(
                    ax=self.graph2.axes, xlabel="Phased data sector " + str(sector))

            if graph_type == "Phased and detrended":
                lightcurve.flatten(window_length=w_value,
                                   polyorder=p_value,
                                   break_tolerance=b_value,
                                   niters=n_value,
                                   sigma=s_value).fold(period_graph, epoch_time=float(epoch) - 2457000,
                                                       normalize_phase=True).scatter(
                    ax=self.graph2.axes, xlabel="Phased and detrend data sector " + str(sector))

            if graph_type == "Phased All" or graph_type == "Phased and detrended all":
                lightcurve_set = self.__photometry_cut[0][star_index].lightcurves()
                main_lc = lightcurve_set[0][0]
                if len(lightcurve_set) > 1:
                    for i in range (1, len(lightcurve_set)):
                        main_lc = main_lc.append(lightcurve_set[i][0])
                if graph_type == "Phased All":
                    main_lc.fold(period_graph, epoch_time=float(epoch) - 2457000, normalize_phase=True).scatter(
                        ax=self.graph2.axes, xlabel="Phased data sector " + str(sector))
                else:
                    main_lc.flatten(window_length=w_value,
                                    polyorder=p_value,
                                    break_tolerance=b_value,
                                    niters=n_value,
                                    sigma=s_value).fold(period_graph, epoch_time=float(epoch) - 2457000,
                                                        normalize_phase=True).scatter(
                      ax=self.graph2.axes, xlabel="Phased data sector " + str(sector))

            if graph_type == "TESS cut view":
                self.__photometry_cut[0][star_index].tess_cut_set()[sector_index].plot(ax=self.graph2.axes,
                                                                                       aperture_mask=target_mask,
                                                                                       mask_color='r')
                matplotlib.pyplot.close(1)

            if graph_type == "Mask desintegration":
                self.graph2_disintegrated_x_combobox.setEnabled(True)
                self.graph2_disintegrated_y_combobox.setEnabled(True)
                x = self.graph2_disintegrated_x_combobox.currentText()
                y = self.graph2_disintegrated_y_combobox.currentText()
                extend_mask = self.tess_menu_window_setting.extend_mask_spinbox.value()
                x_zero = self.__photometry_cut[0][star_index].x() - extend_mask
                y_zero = self.__photometry_cut[0][star_index].y() - extend_mask
                x_index = self.graph2_disintegrated_x_combobox.currentIndex()
                y_index = self.graph2_disintegrated_y_combobox.currentIndex()
                x_count = self.graph2_disintegrated_x_combobox.count()
                y_count = self.graph2_disintegrated_y_combobox.count()
                lc_index = x_index * y_count + y_index
                name = self.graph2_object_combobox.currentText()
                if not self.__mask_desintegration_set2:
                    tpfs = self.__photometry_cut[0][star_index]
                    tpfs.set_lc_parameters()
                    for i in range(x_count):
                        for j in range(y_count):
                            self.__mask_desintegration_set2.append(
                                tpfs.give_lightcurve(sector_index, lightcurve_type="desintegration",
                                                     pixel_x=x_zero + i, pixel_y=y_zero + j))
                if self.graph2_zoom_combobox.count() > 1:
                    lc_part = self.lc_part(self.__mask_desintegration_set2[lc_index], self.graph2_zoom_combobox.count(),
                                           self.graph2_zoom_combobox.currentIndex())
                else:
                    lc_part = self.__mask_desintegration_set2[lc_index]

                lc_part.plot(ax=self.graph2.axes, ylabel="Mask desintegration\nPixel:" + x + ";" + y + "  SECTOR:"
                                                         + str(sector), xlabel=name + "  part:" + part)
            if graph_type == "Gaia interaction":
                pass
            self.graph2.draw()


class TessImport:
    """
    INPUT PARAMETERS
     Input file structure:
     1.column - coordinate: xx xx xx.xx +xx xx xx.xx or xx:xx:xx.xx +xx:xx:xx.xx
     2.column - name
     3.column - variability type - optional
     4.column - magnitude - optional - default 2x2px
     5.column - epoch - optional - default 2459000
     6.period - period - optional (if period isn´t set and  "find_max_power_period = True" period will be found.
                                     if "find_max_power_period = False",  phased curve shapes will not be printed.)

    """
    def __init__(self):
        self.__deny = ""
        self.__data_path = ""
        self.__end = 0
        self.__field_description = False
        self.__first_downloaded_sector = 1
        self.__group_of_star = False
        self.__only_new_data = False
        self.__quality_bitmask_list = ['default', 'none', 'hard', 'hardest']
        self.__quality_bitmask = 'default'
        self.__sips_format = False
        self.__silicups_format = False
        self.__standard_format = False
        # self.__description_format = False
        self.__stars = []
        self.__start = 0
        self.__sectors_for_test = 1
        self.__test_only = False
        self.tpfs_list = []
        self.stars_without_data = []
        self.stars_with_error = []
        self.__files_path = ""
        self.__graph_path = ""
        self.__choice_from_description = 0
        self.tasked_sector = []
        self.star_names = []



    def file_path(self):
        return self.__files_path

    def graph_path(self):
        return self.__graph_path

    #def description_format(self):
    #    return self.__description_format
    #
    #def change_description_format(self, new):
    #    self.__description_format = new

    def change_choice_from_description(self, new):
        self.__choice_from_description = new

    def change_file_path(self, new):
        self.__files_path = new

    def change_graph_path(self, new):
        self.__graph_path = new

    def setup(self):
        from step_application import root
        self.tess_menu_window = root.tess_menu_window
        self.tess_menu_window_setting = root.tess_menu_window_setting
        self.filtered_stars = root.step_main_form.filtered_stars
        self.variables = root.database.variables
        self.photometry_star_list_window = root.photometry_star_list_window

    def standard_format(self):
        return self.__standard_format

    def quality_bitmask_list(self):
        return self.__quality_bitmask_list

    def tpfs_list(self):
        return self.tpfs_list

    def data_path(self):
        return self.__data_path

    def deny(self):
        return self.__deny

    def end(self):
        return self.__end

    def field_description(self):
        return self.__field_description

    def first_downloaded_sector(self):
        return self.__first_downloaded_sector

    def group_of_star(self):
        return self.__group_of_star

    def only_new_data(self):
        return self.__only_new_data

    def quality_bitmask(self):
        return self.__quality_bitmask

    def sips_format(self):
        return self.__sips_format

    def silicups_format(self):
        return self.__silicups_format

    def stars(self):
        return self.__stars

    def start(self):
        return self.__start

    def sectors_for_test(self):
        return self.__sectors_for_test

    def test_only(self):
        return self.__test_only

    def change_standard_format(self, new):
        self.__standard_format = new

    def change_data_path(self, new):
        self.__data_path = new

    def change_tpfs_list(self, new):
        self.tpfs_list = new

    def change_quality_bitmask_list(self, new):
        self.__quality_bitmask_list = new

    def change_deny(self, new):
        self.__deny = new

    def change_end(self, new):
        self.__end = new

    def change_field_description(self, new):
        self.__field_description = new

    def change_first_downloaded_sector(self, new):
        self.__first_downloaded_sector = new

    def change_group_of_star(self, new):
        self.__group_of_star = new

    def change_only_new_data(self, new):
        self.__only_new_data = new

    def change_quality_bitmask(self, new):
        self.__quality_bitmask = new

    def change_sips_format(self, new):
        self.__sips_format = new

    def change_silicups_format(self, new):
        self.__silicups_format = new

    def change_stars(self, new):
        self.__stars = new

    def change_start(self, new):
        self.__start = new

    def change_sectors_for_test(self, new):
        self.__sectors_for_test = new

    def change_test_only(self, new):
        self.__test_only = new

    def set_photometry_parameters(self):
        self.change_standard_format(self.tess_menu_window_setting.input_file_format_standard_checkbox.isChecked())
        self.change_data_path(self.tess_menu_window_setting.folder_data_pushbutton.text())
        try:
            self.change_end(int(self.tess_menu_window_setting.end_position_editline.text().strip(" ")))
        except:
            self.change_end(0)
        self.change_field_description(self.tess_menu_window_setting.input_file_format_field_description_checkbox.isChecked())
        self.change_sips_format(self.tess_menu_window_setting.input_file_format_sips_checkbox.isChecked())
        self.change_silicups_format(self.tess_menu_window_setting.input_file_format_silicups_checkbox.isChecked())
        try:
            self.change_start(int(self.tess_menu_window_setting.start_position_editline.text().strip(" ")))
        except:
            self.change_start(0)
        self.change_choice_from_description(self.tess_menu_window_setting.choice_star_from_description_combobox.currentIndex())
        self.change_group_of_star(self.tess_menu_window_setting.input_file_group_checkbox.isChecked())
        self.change_quality_bitmask(self.tess_menu_window_setting.quality_bitmask_combobox.currentText())
        self.change_first_downloaded_sector(self.tess_menu_window_setting.first_downloaded_sector_spinbox.value())
        self.change_only_new_data(self.tess_menu_window_setting.only_new_data_checkbox.isChecked())
        self.change_sectors_for_test(self.tess_menu_window_setting.test_only_sectors_quantity_spinbox.value())
        self.change_test_only(self.tess_menu_window_setting.test_only_checkbox.isChecked())

    def upload_field_description(self, description_file):
        self.tess_menu_window.start_pushbutton.setText("Reading 0%")
        QtWidgets.QApplication.processEvents()

        if self.__data_path[len(self.__data_path)-3:len(self.__data_path)] != "sfd":
            return [[], "It is not field description file"]
        star_list = []
        variable_list = []
        while "[Stars]" not in description_file[0] and len(description_file) > 1:
            del(description_file[0])
        del(description_file[0])
        i = 0
        while "[Variables]" not in description_file[0] and len(description_file) > 1:
            star = []
            if description_file[0]:
                star_first_item = description_file[0][0].split(sep="=")
                star.append(star_first_item[0].strip())
                star.append(float(star_first_item[1].strip()))
                star.append(float(description_file[0][1].strip()))
                if description_file[0][2] not in ["", " "]:
                    star.append((description_file[0][2].strip()))
                    star.append(float(description_file[0][3].strip()))
                    star.append(float(description_file[0][4].strip()))
                else:
                    star.append("")
                    star.append("")
                    star.append("")
                star_list.append(star)
            del(description_file[0])
        del(description_file[0])
        while len(description_file) > 0:
            if description_file[0]:
                variable_first_item = description_file[0][0].split(sep="=")
                variable_list.append(variable_first_item[0].strip())
            del(description_file[0])
        if self.__choice_from_description == 0:
            new_star_list = []
            for star_item in star_list:
                if star_item[0] in variable_list:
                    new_star_list.append(star_item)
            star_list = new_star_list

        star_quantity = len(star_list)
        modified_file = []
        for k, star in enumerate(star_list):
            a = ("Readind {0}%".format(int(100 * (k / star_quantity))))
            self.tess_menu_window.start_pushbutton.setText(a)
            QtWidgets.QApplication.processEvents()
            if len(star[3]) == 10:
                mag = self.__download_mag_from_ucac(star[3])
                rec_txt = coordinate_to_text(star[4], coordinate_format="hours",
                                             delimiters=(" ", " ", ' '),
                                             decimal_numbers=3)
                dec_txt = coordinate_to_text(star[5], coordinate_format="degree",
                                             delimiters=(" ", " ", ' '),
                                             decimal_numbers=3)
            elif len(star[3]) == 12:
                mag = self.__download_mag_from_usno(star[3])
                rec_txt = coordinate_to_text(star[4], coordinate_format="hours",
                                             delimiters=(" ", " ", ' '),
                                             decimal_numbers=3)
                dec_txt = coordinate_to_text(star[5], coordinate_format="degree",
                                             delimiters=(" ", " ", ' '),
                                             decimal_numbers=3)
            else:
                mag = 15
                rec_txt = coordinate_to_text(star[1], coordinate_format="hours",
                                             delimiters=(" ", " ", ' '),
                                             decimal_numbers=3)
                dec_txt = coordinate_to_text(star[2], coordinate_format="degree",
                                             delimiters=(" ", " ", ' '),
                                             decimal_numbers=3)

            modified_file.append([rec_txt + dec_txt, str(star[0]), "", str(mag)])
        a = ("UPLOAD Objects")
        self.tess_menu_window.start_pushbutton.setText(a)
        QtWidgets.QApplication.processEvents()

        if modified_file:
            return [modified_file, ""]
        else:
            return [modified_file, "There are no stars"]

    def __download_mag_from_ucac(self, cross_id: str):
        fmag = 13
        try:
            agn = Vizier(catalog="I/322A", columns=["*"]).query_constraints(UCAC4=cross_id)[0]
            for x in agn:
                fmag = x["f.mag"]
                vmag = x["Vmag"]
                try:
                    fmag = round(float(fmag), 3)
                except:
                    try:
                        fmag = round(float(vmag), 3)
                    except:
                        fmag = 13
                if isnan(fmag):
                    fmag = 13
        except:
            pass
        return fmag

    def __download_mag_from_usno(self, cross_id: str):
        r_mag = 13
        try:
            agn = Vizier(catalog="I/284", columns=["*"]).query_constraints(USNO_B1_0=cross_id)[0]
            for x in agn:
                b1mag = x["B1mag"]
                r1mag = x["R1mag"]
                try:
                    r_mag = round(float(r1mag), 3)
                except:
                    try:
                        r_mag = round(float(b1mag), 3)
                    except:
                        r_mag = 13
                if isnan(r_mag):
                    r_mag = 13
        except:
            pass
        return r_mag

    def upload_sips_format(self, sips_file):
        modified_file = []
        is_magnitude = True
        end = False
        while "CatalogRA" not in sips_file[0] and len(sips_file) > 1:
            del (sips_file[0])
        if len(sips_file) < 2:
            return [modified_file, "The file generated by SIPS does not contain rektascenze"]
        else:
            column_rektascenze: int = sips_file[0].index("CatalogRA")
            if "CatalogDec" in sips_file[0]:
                column_declination: int = sips_file[0].index("CatalogDec")
            else:
                return [modified_file, "The file generated by SIPS does not contain declination"]
            if "CatalogId" in sips_file[0]:
                column_id: int = sips_file[0].index("CatalogId")
            else:
                return [modified_file, "The file generated by SIPS does not contain id"]
            if "CatalogMag" in sips_file[0]:
                column_magnitude: int = sips_file[0].index("CatalogMag")
            else:
                is_magnitude = False
        del (sips_file[0])
        for line in sips_file:
            if ((line[0] == "" or (self.__deny in line[0] and self.__deny)) and self.__field_description) or line[column_rektascenze] == "" or line[column_declination] == "" or line[column_id] == "":
                pass
            else:
                line_modified_file = []
                if line[column_rektascenze][0:2] == "24":
                    line[column_rektascenze] = "00" + line[column_rektascenze][2:11]
                else:
                    line[column_rektascenze] = line[column_rektascenze][0:11]
                coordinate = line[column_rektascenze] + " " + line[column_declination]
                line_modified_file.append(coordinate)
                if line[0] == "":
                    line_modified_file.append(line[column_id])
                else:
                    line_modified_file.append(line[0])
                line_modified_file.append("")
                if is_magnitude:
                    line_modified_file.append(line[column_magnitude])
                else:
                    line_modified_file.append("")
                modified_file.append(line_modified_file)
        if modified_file:
            return [modified_file, ""]
        else:
            return [modified_file, "There is no stars in selected file"]

    def upload_silicups_file(self, silicups_file):
        modified_file = []
        while ['\tobject'] in silicups_file:
            name = None
            star_rektascenze = None
            star_declination = None
            mag_catalog = ""
            object_id = None
            variability_type = ""
            m0 = ""
            period = ""
            object_start = silicups_file.index(['\tobject'])
            object_end = silicups_file.index(['\tend_object'])
            for line_in_silicups_file in range(object_start, object_end):
                if "\t\tname = " in silicups_file[line_in_silicups_file][0][0:9]:
                    object_id = silicups_file[line_in_silicups_file][0][10:len(silicups_file[line_in_silicups_file][0])
                                                                           - 1]
                if "\t\tvariability_type = " in silicups_file[line_in_silicups_file][0][0:21]:
                    variability_type = silicups_file[line_in_silicups_file][0][
                                       22:len(silicups_file[line_in_silicups_file][0]) - 1]
                if "\t\tm0 = " in silicups_file[line_in_silicups_file][0][0:7]:
                    m0 = silicups_file[line_in_silicups_file][0][7:len(silicups_file[line_in_silicups_file][0])]
                    if m0 == "0":
                        m0 = "2457000"
                if "\t\tperiod = " in silicups_file[line_in_silicups_file][0][0:11]:
                    period = silicups_file[line_in_silicups_file][0][11:len(silicups_file[line_in_silicups_file][0])]
                    if period == "0":
                        period = ""
                if "\t\tseries" in silicups_file[line_in_silicups_file][0] and not star_rektascenze:
                    series = silicups_file[line_in_silicups_file + 1][0][20:len(silicups_file[line_in_silicups_file + 1]
                                                                                [0]) - 1]
                    with open(series, "r", encoding="utf-8") as ser:
                        read_file = csv.reader(ser, delimiter=" ")
                        series_file = [row for row in read_file]
                    try:
                        for line_in_protocol in range(0, 10):
                            if series_file[line_in_protocol][1] == "VAR" and series_file[line_in_protocol][2] == "Name:":
                                name = series_file[line_in_protocol][3]
                                star_rektascenze = series_file[line_in_protocol][5][0:11]
                                star_declination = series_file[line_in_protocol][7][0:12]
                                try:
                                    mag_catalog = str(float(series_file[line_in_protocol][17]))
                                except:
                                    mag_catalog = ""
                    except:
                        pass
            if name and star_rektascenze and star_declination:
                modified_file.append([star_rektascenze + " " + star_declination, name, variability_type, mag_catalog,
                                      m0, period])
            del (silicups_file[0:object_end + 1])
        if modified_file:
            return [modified_file, ""]
        else:
            return [modified_file, "There are no stars"]

    def group_of_stars(self):
        modified_file = []
        filtered_stars = self.filtered_stars.stars
        variables = self.variables
        for star in filtered_stars:
            star_rektascenze = coordinate_to_text(star.coordinate().rektascenze(), coordinate_format="hours")
            star_declination = coordinate_to_text(star.coordinate().deklinace())
            star_name = star.name()
            star_magnitude = str(star.mag())
            variable = variables.find_variable(star_name, "A")
            if variable:
                period = str(variable.period())
                epoch = str(variable.epoch())
            else:
                period = ""
                epoch = "2457000"
            modified_file.append([star_rektascenze + " " + star_declination, star_name, "", star_magnitude, epoch,
                                  period])
        if modified_file:
            return [modified_file, ""]
        else:
            return [modified_file, "There are no stars"]

    def check_coordinate(self, coor):
        coor_list = coor.split(" ")
        while "" in coor_list:
            coor_list.remove("")
        if len(coor_list) == 2:
            coor_list = coor_list[0].split(":") + coor_list[1].split(":")
        if len(coor_list) == 6:
            try:
                if "." in coor_list[0] or "-" in coor_list[0] or int(coor_list[0]) > 23:
                    return False
                elif "." in coor_list[1] or "-" in coor_list[1] or int(coor_list[1]) > 59:
                    return False
                elif "-" in coor_list[2] or float(coor_list[2]) >= 60:
                    return False
                elif "." in coor_list[3] or int(coor_list[3]) > 89 or int(coor_list[3]) < -89:
                    return False
                elif "." in coor_list[4] or "-" in coor_list[4] or int(coor_list[4]) > 59:
                    return False
                elif "-" in coor_list[5] or float(coor_list[5]) >= 60:
                    return False
                else:
                    return True
            except:
                return False
        else:
            return False

    def select_star_for_photometry(self):
        warnings.simplefilter("ignore", category=LightkurveWarning)
        self.tpfs_list.clear()
        self.stars_without_data = []
        self.stars_with_error = []
        self.star_names = []
        # LightkurveWarning
        if self.__group_of_star:
            stars_info = self.group_of_stars()
        else:
            try:
                with open(self.__data_path) as data_file:
                    read_file = csv.reader(data_file, delimiter=";")
                    stars = [row for row in read_file]
            except:
                r = Popup("File error", "File access denied or path not specified", buttons="OK".split(","))
                r.do()
                self.tess_menu_window.show_photometry()
                return
            if self.__sips_format:
                stars_info = self.upload_sips_format(stars)
            elif self.__field_description:
                stars_info = self.upload_field_description(stars)
            elif self.__silicups_format:
                stars_info = self.upload_silicups_file(stars)
            else:
                stars_info = [stars, ""]
        stars = stars_info[0]
        if not stars:
            r = Popup("File error", stars_info[1], buttons="OK".split(","))
            r.do()
            self.tess_menu_window.show_photometry()
            return # [self.tpfs_list, self.stars_without_data, self.stars_with_error]
        else:
            if not self.__only_new_data:
                self.change_first_downloaded_sector(1)
            self.tasked_sector = list(range(self.first_downloaded_sector(), 69))
            if self.__start > len(stars):
                self.change_start(len(stars)-1)
            if self.__end == 0 or self.__end > len(stars):
                self.change_end(len(stars))
            if self.__start >= self.__end:
                self.change_start(self.__end - 1)
            if self.__end - self.__start > 0:
                self.photometry_star_list_window.fill_stars(stars[self.__start:self.__end])
                self.photometry_star_list_window.show()
            else:
                self.tess_menu_window.show_photometry()

    def load_photometry(self, stars):
        self.set_photometry_parameters()
        for line_in_file in range(len(stars)):
            import_ok = True
            star_quantity = len(stars)
            if star_quantity < 1:
                star_quantity = 1
            a = ("Processing:  {0}% ready, downloading star: {1}".format(int(100 * line_in_file / star_quantity), stars[line_in_file][1]))
            self.photometry_star_list_window.info_label.setText(a)
            self.photometry_star_list_window.photometry_button.setText("Downloading")
            QtWidgets.QApplication.processEvents()
            star = stars[line_in_file]
            while len(star) < 6:
                star.append("")
            coor = star[0].strip()
            if self.check_coordinate(coor):
                var_id = star[1].strip()
                name = var_id.replace(".", "_").replace("+", "_").replace("-", "_").replace(" ", "_").replace("*", "_")
                if star[3] == "":
                    mag, x, y, mx, my, m, n, cut_size = "", 4, 4, 2, 2, 4, 7, 10
                else:
                    mag = float(star[3])
                    # left, down, size x, size y, star and end for desintegration, cut_size
                    if mag < 4:
                        x, y, mx, my, m, n, cut_size = 45, 45, 10, 10, 43, 57, 99
                    elif 4 <= mag < 6.5:
                        x, y, mx, my, m, n, cut_size = 7, 7, 6, 6, 6, 15, 20
                    elif 6.5 <= mag < 10:
                        x, y, mx, my, m, n, cut_size = 8, 8, 5, 5, 8, 13, 20
                    elif 10 <= mag < 13:
                        x, y, mx, my, m, n, cut_size = 6, 6, 3, 3, 6, 9, 14
                    elif 13 <= mag < 15.5:
                        x, y, mx, my, m, n, cut_size = 4, 4, 2, 2, 4, 7, 10
                    else:
                        x, y, mx, my, m, n, cut_size = 5, 5, 1, 1, 4, 7, 10
                if star[4] == "":
                    epoch = 2000
                else:
                    epoch = float(star[4]) - 2457000
                if star[5] == "":
                    period = None
                else:
                    period = float(star[5])
                description = var_id + " VAR: " + star[2] + "\n" + star[3] + " mag P:" + star[5] + " dne JD0: " \
                              + star[4]
                try:
                    search_results = lk.search_tesscut(coor, sector=self.tasked_sector)
                except:
                    import_ok = False
                    self.stars_with_error.append(var_id)
                if import_ok:
                    if len(search_results) == 0:
                        self.stars_without_data.append(var_id)
                    else:
                        all_sectors_str = ""
                        for one_sector in range(len(search_results)):
                            all_sectors_str = all_sectors_str + (str(search_results[one_sector].mission[0])[12:14]) + ","
                        if len(search_results) > self.__sectors_for_test and self.__test_only:
                            sector_tested = []
                            for one_sector in range(self.__sectors_for_test):
                                sector_tested.append(int(str(search_results[one_sector].mission[0])[12:14]))
                            search_results = lk.search_tesscut(coor, sector=sector_tested)
                        sector_tested_str = ""
                        for one_sector in range(len(search_results)):
                            sector_tested_str = sector_tested_str + (str(search_results[one_sector].mission[0])[12:14]) + ","
                        a = a + "   Existing sectors:" + all_sectors_str + "  Downloading sectors: " + sector_tested_str
                        self.photometry_star_list_window.info_label.setText(a)
                        QtWidgets.QApplication.processEvents()
                        try:
                            tpfs = search_results.download_all(cutout_size=cut_size,
                                                               quality_bitmask=self.__quality_bitmask)
                        except:
                            import_ok = False
                            self.stars_with_error.append(var_id)
                        if import_ok:
                            if len(tpfs) > 0:
                                sectors = []
                                lightcurves = []
                                tpfs_list = []
                                for tpf in tpfs:
                                    tpfs_list.append(tpf)
                                a = TessCutInfo(lightcurves, coor, var_id, name, mag, period, star[4], tpfs_list,
                                                sectors, x, y, mx, my, m, n, cut_size, description, "", var_id)
                                a.set_lc_parameters()
                                tess_cut_without_data_set = []
                                for i in range(len(a.tess_cut_set())):
                                    lightcurve = a.give_lightcurve(i)
                                    if lightcurve:
                                        lightcurves.append(lightcurve)
                                        sectors.append(str(lightcurve[3]))
                                    else:
                                        tess_cut_without_data_set.append(i)
                                for j in range(0, len(tess_cut_without_data_set), -1):
                                    index = tess_cut_without_data_set[j]
                                    a.del_index_in_tess_cut_set(index)
                                if lightcurves:
                                    self.star_names.append(var_id)
                                    a.change_lightcurves(lightcurves)
                                    a.change_sectors(sectors)
                                    self.tpfs_list.append(a)
                                else:
                                    self.stars_without_data.append(var_id)
                            else:
                                self.stars_without_data.append(var_id)
        self.photometry_star_list_window.info_label.setText("")


        if self.__group_of_star:
            new_tpfs = []
            self.star_names = []
            for star in self.tpfs_list:
                for variable in self.variables.variables:
                    if star.var_id() == variable.name():
                        lightcurves = deepcopy(star.lightcurves())
                        coor = star.coor()
                        var_id = star.var_id() + " " + variable.pair()
                        name = star.name()
                        mag = star.mag()
                        pair = variable.pair()
                        if variable.period():
                            period = float(variable.period())
                            for lightcurve in lightcurves:
                                lightcurve[4] = float(variable.period())
                        else:
                            period = star.lightcurves()[0][4]
                        e0 = float(variable.epoch())
                        tpfs = star.tess_cut_set()
                        sectors = star.sectors()
                        x1 = star.x()
                        y1 = star.y()
                        mx = star.mx()
                        my = star.my()
                        m = star.m()
                        n = star.n()
                        name_origin = variable.name()
                        cut_size = star.cut_size()
                        description = star.description()
                        new_star = TessCutInfo(lightcurves, coor, var_id, name, mag, period, e0, tpfs, sectors, x1, y1,
                                               mx, my, m, n, cut_size, description, pair, name_origin)
                        new_tpfs.append(new_star)
                        self.star_names.append(var_id)
            self.change_tpfs_list(new_tpfs)
        self.tess_menu_window.show_photometry()



class MplCanvas(FigureCanvasQTAgg):

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super(MplCanvas, self).__init__(fig)


class SilicupsFieldWindow(QtWidgets.QWidget):

    def __init__(self, *args, **kvargs):
        super(SilicupsFieldWindow, self).__init__(*args, **kvargs)

        self.setWindowTitle("Silicups field parameters")
        self.main_layout = QtWidgets.QGridLayout()
        self.setLayout(self.main_layout)

        data_postfix_list = ["*.txt", "*_TESS.txt", "*_flat.txt", "*_NORM.txt", "*_MAG.txt"]

        self.path_silicups_field_pushbutton = QtWidgets.QPushButton("")
        self.path_absolute_path_pushbutton = QtWidgets.QPushButton("")
        self.ok_button = QtWidgets.QPushButton("OK")
        self.exit_button = QtWidgets.QPushButton("Exit")

        self.object1_name_line_edit = QtWidgets.QLineEdit()
        self.object1_name_line_edit.setEnabled(False)
        self.object1_postfix_line_edit = QtWidgets.QLineEdit()
        self.object1_data_name_line_edit = QtWidgets.QLineEdit()
        self.object1_data_name_line_edit.setEnabled(False)
        self.object1_data_prefix_line_edit = QtWidgets.QLineEdit()
        self.object1_data_postfix_combobox = QtWidgets.QComboBox()
        self.object1_data_postfix_combobox.addItems(data_postfix_list)

        self.object2_check_box = QtWidgets.QCheckBox("2nd variant")
        self.object2_check_box.setChecked(False)
        self.object2_postfix_line_edit = QtWidgets.QLineEdit()
        self.object2_postfix_line_edit.setEnabled(False)
        self.object2_data_prefix_line_edit = QtWidgets.QLineEdit()
        self.object2_data_prefix_line_edit.setEnabled(False)
        self.object2_data_postfix_combobox = QtWidgets.QComboBox()
        self.object2_data_postfix_combobox.addItems(data_postfix_list)
        self.object2_data_postfix_combobox.setEnabled(False)

        self.object3_check_box = QtWidgets.QCheckBox("3nd variant")
        self.object3_check_box.setChecked(False)
        self.object3_postfix_line_edit = QtWidgets.QLineEdit()
        self.object3_postfix_line_edit.setEnabled(False)
        self.object3_data_prefix_line_edit = QtWidgets.QLineEdit()
        self.object3_data_prefix_line_edit.setEnabled(False)
        self.object3_data_postfix_combobox = QtWidgets.QComboBox()
        self.object3_data_postfix_combobox.addItems(data_postfix_list)
        self.object3_data_postfix_combobox.setEnabled(False)

        self.build()

    def build(self):
        self.main_layout.addWidget(QtWidgets.QLabel("Silicups field name:"), 0, 0)
        self.main_layout.addWidget(self.path_silicups_field_pushbutton, 0, 1, 1, 2)
        self.main_layout.addWidget(QtWidgets.QLabel("Data folder:"), 0, 3)
        self.main_layout.addWidget(self.path_absolute_path_pushbutton, 0, 4, 1, 2)
        self.main_layout.addWidget(self.ok_button, 0, 6)
        self.main_layout.addWidget(self.exit_button, 0, 7)

        self.main_layout.addWidget(QtWidgets.QLabel("Star name + postfix:"), 1, 0)
        self.main_layout.addWidget(self.object1_name_line_edit, 1, 1)
        self.main_layout.addWidget(self.object1_postfix_line_edit, 1, 2)
        self.main_layout.addWidget(QtWidgets.QLabel("Data prefix:"), 1, 3)
        self.main_layout.addWidget(self.object1_data_prefix_line_edit, 1, 4)
        self.main_layout.addWidget(self.object1_data_name_line_edit, 1, 5)
        self.main_layout.addWidget(QtWidgets.QLabel("Data postfix:"), 1, 6)
        self.main_layout.addWidget(self.object1_data_postfix_combobox, 1, 7)

        self.main_layout.addWidget(self.object2_check_box, 2, 0)
        self.main_layout.addWidget(self.object2_postfix_line_edit, 2, 2)
        self.main_layout.addWidget(QtWidgets.QLabel("Data prefix:"), 2, 3)
        self.main_layout.addWidget(self.object2_data_prefix_line_edit, 2, 4)
        self.main_layout.addWidget(QtWidgets.QLabel("Data postfix:"), 2, 6)
        self.main_layout.addWidget(self.object2_data_postfix_combobox, 2, 7)

        self.main_layout.addWidget(self.object3_check_box, 3, 0)
        self.main_layout.addWidget(self.object3_postfix_line_edit, 3, 2)
        self.main_layout.addWidget(QtWidgets.QLabel("Data prefix:"), 3, 3)
        self.main_layout.addWidget(self.object3_data_prefix_line_edit, 3, 4)
        self.main_layout.addWidget(QtWidgets.QLabel("Data postfix:"), 3, 6)
        self.main_layout.addWidget(self.object3_data_postfix_combobox, 3, 7)

    def setup(self):
        from step_application import root
        self.tess_menu_window = root.tess_menu_window
        self.tess_import = root.tess_import
        self.object2_check_box.clicked.connect(self.object2_check_box_was_checked)
        self.object3_check_box.clicked.connect(self.object3_check_box_was_checked)
        self.path_absolute_path_pushbutton.clicked.connect(self.give_data_folder)
        self.path_silicups_field_pushbutton.clicked.connect(self.give_silicups_file_name)
        self.exit_button.clicked.connect(self.close)
        self.ok_button.clicked.connect(self.save_field)


    def object2_check_box_was_checked(self):
        if self.object2_check_box.isChecked():
            self.object2_postfix_line_edit.setEnabled(True)
            self.object2_data_prefix_line_edit.setEnabled(True)
            self.object2_data_postfix_combobox.setEnabled(True)
        else:
            if self.object3_check_box.isChecked():
                self.object3_check_box.setChecked(False)
                self.object3_check_box_was_checked()
                self.object3_data_postfix_combobox.setEnabled(False)
            self.object2_postfix_line_edit.setEnabled(False)
            self.object2_data_prefix_line_edit.setEnabled(False)
            self.object2_data_postfix_combobox.setEnabled(False)

    def object3_check_box_was_checked(self):
        if not self.object2_check_box.isChecked():
            self.object3_check_box.setChecked(False)

        if self.object3_check_box.isChecked():
            self.object3_postfix_line_edit.setEnabled(True)
            self.object3_data_prefix_line_edit.setEnabled(True)
            self.object3_data_postfix_combobox.setEnabled(True)
        else:
            self.object3_postfix_line_edit.setEnabled(False)
            self.object3_data_prefix_line_edit.setEnabled(False)
            self.object3_data_postfix_combobox.setEnabled(False)

    def give_silicups_file_name(self):
        current_path = self.path_silicups_field_pushbutton.text()
        if not os.path.exists(current_path):
            current_path = self.tess_import.file_path()
        if not os.path.exists(current_path):
            current_path = os.getenv("APPDATA")
        if self.object1_name_line_edit.text() == "Star name":
            path_to_file = QtWidgets.QFileDialog.getSaveFileName(caption="Create Silicups field",
                                                                 directory=current_path, filter="*.sif")
        else:
            path_to_file = find_path_to_file(current_path=current_path, window_table="Choice Silicups field",
                                             mask="*.sif", path_to_file=True)
        self.path_silicups_field_pushbutton.setText(path_to_file[0])

    def give_data_folder(self):
        current_path = self.path_absolute_path_pushbutton.text()
        if not os.path.exists(current_path):
            current_path = self.tess_import.file_path()
        if not os.path.exists(current_path):
            current_path = os.getenv("APPDATA")
        path_to_folder = find_path_to_file(current_path=current_path, window_table="Select data folder", path_to_file=False)
        self.path_absolute_path_pushbutton.setText(path_to_folder)

    def save_field(self):
        file_path = self.path_silicups_field_pushbutton.text()
        if file_path:
            if self.object1_name_line_edit.text() == "Star name":
                if os.path.exists(file_path):
                    name_exist_window = Popup("File already exist",
                                              "File {0} will be lost.\nDo you want to re-write it?".format(file_path),
                                              buttons="Continue,Exit".split(","))
                    if name_exist_window.do() == 1:
                        return
            else:
                if not os.path.exists(file_path):
                    name_exist_window = Popup("File does not exist",
                                              "Path to file {0} does not exist".format(file_path),
                                              buttons="OK".split(","))
                    name_exist_window.do()
                    return


        else:
            name_exist_window = Popup("Set name",
                                      "You have to set Silicups field name. It is empty now",
                                      buttons="OK".split(","))
            name_exist_window.do()
            return
        absolute_path = self.path_absolute_path_pushbutton.text()
        if not os.path.exists(absolute_path):
            name_exist_window = Popup("Data folder error",
                                      "File {0} does not exist.".format(absolute_path),
                                      buttons="OK".split(","))
            name_exist_window.do()
            return
        new_file_object_list = []
        if self.object1_name_line_edit.text() == "Star name" \
                or self.object1_name_line_edit.text() == "Add all - Star name":
            photometry_cut = self.tess_menu_window.photometry_cut()[0]
        else:
            star_index = self.tess_menu_window.graph1_object_combobox.currentIndex()
            photometry_cut = [self.tess_menu_window.photometry_cut()[0][star_index]]

        for object_photometry in photometry_cut:
            coor_list = object_photometry.coor().split(" ")
            if '' in coor_list:
                index = coor_list.index('')
                del(coor_list[index])
            if " " in coor_list:
                index = coor_list.index(" ")
                del(coor_list[index])
            rektascenze = coor_list[0] + " " + coor_list[1] + " " + coor_list[2]
            declination = coor_list[3] + " " + coor_list[4] + " " + coor_list[5]
            star_data_name = object_photometry.name()
            star_name = object_photometry.var_id()
            period = object_photometry.period()
            if not period:
                period = object_photometry.lightcurves()[0][4]
            epoch = object_photometry.epoch()
            if not epoch:
                epoch = "2460000"
            magnitude = object_photometry.mag()
            star_data_file_name_mask = self.object1_data_prefix_line_edit.text() \
                                       + star_data_name + self.object1_data_postfix_combobox.currentText()
            star_name_with_postfix = star_name + self.object1_postfix_line_edit.text()
            object_row = self.__create_silicups_object(star_name_with_postfix, period, epoch, rektascenze,
                                                       declination, magnitude, absolute_path,
                                                       star_data_file_name_mask)
            new_file_object_list.append(object_row)
            if self.object2_check_box.isChecked():
                star_data_file_name_mask = self.object2_data_prefix_line_edit.text() \
                                           + star_data_name + self.object2_data_postfix_combobox.currentText()
                star_name_with_postfix = star_name + self.object2_postfix_line_edit.text()
                object_row = self.__create_silicups_object(star_name_with_postfix, period, epoch, rektascenze,
                                                           declination, magnitude, absolute_path,
                                                           star_data_file_name_mask)
                new_file_object_list.append(object_row)
            if self.object3_check_box.isChecked():
                star_data_file_name_mask = self.object3_data_prefix_line_edit.text() \
                                           + star_data_name + self.object3_data_postfix_combobox.currentText()
                star_name_with_postfix = star_name + self.object3_postfix_line_edit.text()
                object_row = self.__create_silicups_object(star_name_with_postfix, period, epoch, rektascenze,
                                                           declination, magnitude, absolute_path,
                                                           star_data_file_name_mask)
                new_file_object_list.append(object_row)
        start_text = "silicups\n\tversion = 3\n\tobjects = " + str(len(new_file_object_list)) + "\n"
        end_text = "end_silicups"
        if self.object1_name_line_edit.text() == "Star name":
            try:
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(start_text)
                    for object_text in new_file_object_list:
                        for row in object_text:
                            f.write(row)
                    f.write(end_text)
            except:
                mistake = Popup("Star saving error",
                                "Failed to create file\n{0}\nPlease check your permissions."
                                .format(file_path), buttons="EXIT".split(","))
                mistake.do()
                return
        else:
            try:
                with open(file_path, "r", encoding="utf-8") as data:
                    rows = reader(data)
                    original_file = [row for row in rows]
            except:
                mistake = Popup("Star reading error",
                                "Failed to create file\n{0}\nPlease check your permissions."
                                .format(file_path), buttons="EXIT".split(","))
                mistake.do()
                return
            if original_file[0] == ['silicups'] and original_file[1] == ['\tversion = 3']:
                third_row_length = len(original_file[2][0])
                new_object_quantity = int(original_file[2][0][11:third_row_length]) + len(new_file_object_list)
                original_file[2][0] = original_file[2][0][0:11] + str(new_object_quantity)
                del(original_file[-1])
                with open(file_path, "w", encoding="utf-8") as f:
                    for object_text in original_file:
                        for row in object_text:
                            f.write(row)
                            f.write("\n")
                    for object_text in new_file_object_list:
                        for row in object_text:
                            f.write(row)
                    f.write(end_text)
            else:
                mistake = Popup("Silicups field file error",
                                "This file is not Silicups file version 3 or more"
                                , buttons="EXIT".split(","))
                mistake.do()
                return
        mistake = Popup("Silicups field saved",
                        "New file was saved. You can check it!"
                        , buttons="OK".split(","))
        mistake.do()
        self.close()

    def __create_silicups_object(self, name, period, epoch, rektascenze, declination, magnitude, absolute_path,
                                 file_mask):
        rektascenze_rad = read_coordinate(rektascenze, coor_format="rektascenze_hours")[3]
        declination_rad = read_coordinate(declination, coor_format="declination_degrees")[3]
        object_row_list = ['\tobject\n']
        object_row_list.append('\t\tname = "' + name + '"\n')
        object_row_list.append('\t\tm0 = ' + str(epoch) + '\n')
        object_row_list.append('\t\tperiod = ' + str(period) + '\n')
        object_row_list.append('\t\tsaved_m0 = ' + str(epoch) + '\n')
        object_row_list.append('\t\tsaved_period = ' + str(period) + '\n')
        object_row_list.append('\t\tperiod = ' + str(period) + '\n')
        object_row_list.append('\t\tabsolute_path = "' + absolute_path + '"\n')
        object_row_list.append('\t\trelative_path = ""\n')
        object_row_list.append('\t\tdir_key = ""\n')
        object_row_list.append('\t\tfile_names = "' + file_mask + '"\n')
        object_row_list.append('\t\toffset_amplitude = 0.100000\n')
        object_row_list.append('\t\tperiod_amplitude = 0.100000\n')
        object_row_list.append('\t\tmeta_data\n')
        object_row_list.append('\t\t\tjd_type = heliocentric\n')
        object_row_list.append('\t\t\tvar\n')
        object_row_list.append('\t\t\t\tstar_name = "' + name + '"\n')
        object_row_list.append('\t\t\t\tstar_ra = "' + rektascenze + '"\n')
        object_row_list.append('\t\t\t\tstar_dec = "' + declination + '"\n')
        object_row_list.append('\t\t\t\tcatalog_ra = ' + str(rektascenze_rad) + '\n')
        object_row_list.append('\t\t\t\tcatalog_dec = ' + str(declination_rad) + '\n')
        object_row_list.append('\t\t\t\tcatalog_mag = ' + str(magnitude) + '\n')
        object_row_list.append('\t\t\tend_var\n')
        object_row_list.append('\t\tend_meta_data\n')
        object_row_list.append('\tend_object\n')
        return object_row_list


class TESSListWindow(QtWidgets.QWidget):

    def __init__(self, *args, **kvargs):
        super(TESSListWindow, self).__init__(*args, **kvargs)

        self.old_star_list = []
        self.new_star_list = []

        self.setWindowTitle("List of star")
        self.setWindowIcon(QtGui.QIcon("star-small.png"))
        main_layout = QtWidgets.QGridLayout()
        self.setLayout(main_layout)
        self.star_list_widget = QtWidgets.QListWidget()
        self.photometry_button = QtWidgets.QPushButton("START UPLOAD PHOTOMETRY")
        self.all_checked_button = QtWidgets.QPushButton("check all")
        self.all_unchecked_button = QtWidgets.QPushButton("uncheck all")
        self.checked_groupbox = QtWidgets.QGroupBox()
        self.check_button = QtWidgets.QPushButton("Check")
        self.uncheck_button = QtWidgets.QPushButton("Uncheck")
        self.from_spinbox = QtWidgets.QSpinBox()
        self.to_spinbox = QtWidgets.QSpinBox()
        self.info_label = QtWidgets.QLabel("")
        main_layout.addWidget(self.all_checked_button, 0, 0)
        main_layout.addWidget(self.all_unchecked_button, 0, 1)
        main_layout.addWidget(self.check_button, 0, 2)
        main_layout.addWidget(self.uncheck_button, 0, 3)
        main_layout.addWidget(QtWidgets.QLabel(" from "), 0, 4)
        main_layout.addWidget(self.from_spinbox, 0, 5)
        main_layout.addWidget(QtWidgets.QLabel(" to "), 0, 6)
        main_layout.addWidget(self.to_spinbox, 0, 7)

        main_layout.addWidget(self.photometry_button, 0, 8)
        main_layout.addWidget(self.star_list_widget, 1, 0, 1, 9)
        main_layout.addWidget(self.info_label, 2, 0, 1, 9 )

    def setup(self):
        from step_application import root
        self.all_unchecked_button.clicked.connect(self.uncheck_all)
        self.all_checked_button.clicked.connect(self.check_all)
        self.uncheck_button.clicked.connect(self.uncheck_from)
        self.check_button.clicked.connect(self.check_from)
        self.photometry_button.clicked.connect(self.fix_star_list)
        self.tess_menu_window = root.tess_menu_window
        self.tess_import = root.tess_import

    def fill_stars(self, star_list):
        self.star_list_widget.clear()
        self.from_spinbox.setValue(0)
        self.to_spinbox.setValue(0)
        star_list_lenth = len(star_list)
        if star_list_lenth > 100:
            star_list_lenth = 100
        self.from_spinbox.setRange(0, len(star_list) - 2)
        self.to_spinbox.setRange(0, len(star_list) - 1)
        self.old_star_list = star_list
        for i, star in enumerate(star_list):
            star_description = star[1] + "  coordinate: " + star[0] + "  mag: " + str(star[3]) + "  item " + str(i)
            item = QtWidgets.QListWidgetItem(star_description)
            item.setFlags(item.flags() | QtCore.Qt.ItemIsUserCheckable)
            item.setCheckState(QtCore.Qt.Checked)
            self.star_list_widget.addItem(item)

    def uncheck_all(self):
        for i in range(self.star_list_widget.count()):
            self.star_list_widget.item(i).setCheckState(QtCore.Qt.Unchecked)

    def check_all(self):
        for i in range(self.star_list_widget.count()):
            self.star_list_widget.item(i).setCheckState(QtCore.Qt.Checked)

    def uncheck_from(self):
        from_star = self.from_spinbox.value()
        to_star = self.to_spinbox.value()
        if to_star < from_star:
            return
        for i in range(from_star, to_star + 1):
            self.star_list_widget.item(i).setCheckState(QtCore.Qt.Unchecked)

    def check_from(self):
        from_star = self.from_spinbox.value()
        to_star = self.to_spinbox.value()
        if to_star < from_star:
            return
        for i in range(from_star, to_star + 1):
            self.star_list_widget.item(i).setCheckState(QtCore.Qt.Checked)

    def fix_star_list(self):
        self.new_star_list = []
        for i in range(self.star_list_widget.count()):
            if self.star_list_widget.item(i).checkState():
                self.new_star_list.append(self.old_star_list[i])
        if len(self.new_star_list) > 5:
            window_title = "Photometry info"
            window_text = "Photometry contains {0} stars\nIt will take more than {1} minutes\nSet START, END " \
                          "position properly\nDo you want to continue?".format(len(self.new_star_list),
                                                                               len(self.new_star_list) * 2)
            r1 = Popup(window_title, window_text, buttons="OK,Exit".split(","))
            if r1.do() == 0:
                self.tess_import.load_photometry(self.new_star_list)
            else:
                self.tess_menu_window.show_photometry()
                return
        elif 6 > len(self.new_star_list) > 0:
            self.tess_import.load_photometry(self.new_star_list)
        else:
            self.tess_menu_window.show_photometry()


class TESSMenuWindowSetting(QtWidgets.QWidget):

    def __init__(self, *args, **kvargs):
        super(TESSMenuWindowSetting, self).__init__(*args, **kvargs)

        self.setWindowTitle("TESS photometry setting")
        self.setWindowIcon(QtGui.QIcon("star--arrow.png"))
        main_layout = QtWidgets.QGridLayout()
        self.setLayout(main_layout)

        folder_files_label = QtWidgets.QLabel("path to data save folder:")
        folder_pictures_label = QtWidgets.QLabel("path to pictures save folder:")
        start_position_label = QtWidgets.QLabel("Input start position in data source:")
        end_position_label = QtWidgets.QLabel("Input end position ('0'- end of file):")
        folder_data_label = QtWidgets.QLabel("path to input data file:")
        extend_mask_label = QtWidgets.QLabel("Extend the mask(px):")
        quality_bitmask_label = QtWidgets.QLabel("Bitmask quality:")
        first_downloaded_sector_label = QtWidgets.QLabel("First downloaded sector")
        test_only_sectors_quantity_label = QtWidgets.QLabel("Quantity of tested sectors:")
        data_focus_label = QtWidgets.QLabel("Data focus:")

        # Input
        self.start_position_editline = QtWidgets.QLineEdit("")
        self.start_position_editline.setInputMask("00009")
        self.end_position_editline = QtWidgets.QLineEdit("")
        self.end_position_editline.setInputMask("00009")
        self.folder_data_pushbutton = QtWidgets.QPushButton("")
        self.folder_data_pushbutton.setFixedWidth(250)
        self.input_file_format_standard_checkbox = QtWidgets.QRadioButton("*.csv file-RA+DE,name+(type,mag,P,E0)")
        self.input_file_format_sips_checkbox = QtWidgets.QRadioButton("SIPS file")
        self.input_file_format_silicups_checkbox = QtWidgets.QRadioButton("SILICUPS file")
        self.input_file_format_field_description_checkbox = QtWidgets.QRadioButton("SIPS field description")
        self.choice_star_from_description_combobox = QtWidgets.QComboBox()
        self.choice_star_from_description_combobox.addItems(["Variables", "All stars"])
        self.input_file_deny_editline = QtWidgets.QLineEdit("")
        self.input_file_group_checkbox = QtWidgets.QRadioButton("Current selected group of stars")

        self.input_file_button_group = QtWidgets.QButtonGroup()
        self.input_file_button_group.addButton(self.input_file_format_standard_checkbox)
        self.input_file_button_group.addButton(self.input_file_format_sips_checkbox)
        self.input_file_button_group.addButton(self.input_file_format_silicups_checkbox)
        self.input_file_button_group.addButton(self.input_file_format_field_description_checkbox)
        self.input_file_button_group.addButton(self.input_file_group_checkbox)

        # Show info
        self.show_picture_origin_checkbox = QtWidgets.QCheckBox("Show original data")
        self.show_picture_detrend_checkbox = QtWidgets.QCheckBox("Show detrended data")
        self.show_picture_faze_checkbox = QtWidgets.QCheckBox("Show phased data")
        self.show_picture_detrend_faze_checkbox = QtWidgets.QCheckBox("Show phased detrended data")
        self.show_picture_all_faze_checkbox = QtWidgets.QCheckBox("Show phased data(all sectors)")
        self.show_picture_all_detrend_faze_checkbox = QtWidgets.QCheckBox("Show phased detrended data (all sectors)")
        self.show_mask_desintegration_checkbox = QtWidgets.QCheckBox("Show mask desintegration")
        self.extend_mask_spinbox = QtWidgets.QSpinBox()
        self.extend_mask_spinbox.setRange(0, 3)

        # Save info
        self.save_original_data_checkbox = QtWidgets.QCheckBox("Do you want to save the original data?")
        self.save_norm_data_checkbox = QtWidgets.QCheckBox("Do you want to save the normalized data?")
        self.save_detrend_data_checkbox = QtWidgets.QCheckBox("Do you want to save the detrended data?")
        self.percentage_of_erroneous_points_double_spinbox = QtWidgets.QDoubleSpinBox()
        self.save_pictures_checkbox = QtWidgets.QCheckBox("Do you want to save graphs into file?")
        self.folder_files_pushbutton = QtWidgets.QPushButton("")
        self.folder_pictures_pushbutton = QtWidgets.QPushButton("")

        # Photometry setting
        self.edit_tess_data_pushbutton = QtWidgets.QPushButton("Edit data")
        self.edit_tess_data_pushbutton.setEnabled(False)
        self.quality_bitmask_combobox = QtWidgets.QComboBox()
        self.only_new_data_checkbox = QtWidgets.QCheckBox("Only newly observed sectors")
        self.first_downloaded_sector_spinbox = QtWidgets.QSpinBox()
        self.test_only_checkbox = QtWidgets.QCheckBox("Show only the test sector")
        self.test_only_sectors_quantity_spinbox = QtWidgets.QSpinBox()
        self.test_only_sectors_quantity_spinbox.setRange(1, 4)
        self.change_focus_by_period = QtWidgets.QCheckBox("Change focus by period")
        self.data_focus_spinbox = QtWidgets.QSpinBox()
        self.find_max_power_period_checkbox = QtWidgets.QCheckBox("Find the period")
        self.change_detrend_parameters_by_period_checkbox = QtWidgets.QCheckBox("Change detrend parameter by period")

        input_file_groupbox = QtWidgets.QGroupBox("Input File - setting")
        show_file_groupbox = QtWidgets.QGroupBox("Displaying data - setting")
        save_file_groupbox = QtWidgets.QGroupBox("Saving data - setting")
        photometry_file_groupbox = QtWidgets.QGroupBox("Photometry - setting")

        input_file_layout = QtWidgets.QGridLayout()
        show_file_layout = QtWidgets.QGridLayout()
        save_file_layout = QtWidgets.QGridLayout()
        photometry_file_layout = QtWidgets.QGridLayout()

        input_file_groupbox.setLayout(input_file_layout)
        show_file_groupbox.setLayout(show_file_layout)
        save_file_groupbox.setLayout(save_file_layout)
        photometry_file_groupbox.setLayout(photometry_file_layout)

        input_file_layout.addWidget(folder_data_label, 0, 0, 1, 2)
        input_file_layout.addWidget(self.folder_data_pushbutton, 1, 0, 1, 2)
        input_file_layout.addWidget(start_position_label, 2, 0)
        input_file_layout.addWidget(self.start_position_editline, 2, 1)
        input_file_layout.addWidget(end_position_label, 3, 0)
        input_file_layout.addWidget(self.end_position_editline, 3, 1)
        input_file_layout.addWidget(self.input_file_group_checkbox, 4, 0, 1, 2)
        input_file_layout.addWidget(self.input_file_format_standard_checkbox, 5, 0, 1, 2)
        input_file_layout.addWidget(self.input_file_format_silicups_checkbox, 6, 0, 1, 2)
        input_file_layout.addWidget(self.input_file_format_sips_checkbox, 7, 0, 1, 2)
        input_file_layout.addWidget(self.input_file_format_field_description_checkbox, 8, 0, 1, 1)
        input_file_layout.addWidget(self.choice_star_from_description_combobox, 8, 1, 1, 1)

        show_file_layout.addWidget(self.show_picture_origin_checkbox, 0, 0, 1, 2)
        show_file_layout.addWidget(self.show_picture_detrend_checkbox, 1, 0, 1, 2)
        show_file_layout.addWidget(self.show_picture_faze_checkbox, 2, 0, 1, 2)
        show_file_layout.addWidget(self.show_picture_detrend_faze_checkbox, 3, 0, 1, 2)
        show_file_layout.addWidget(self.show_picture_all_faze_checkbox, 4, 0, 1, 2)
        show_file_layout.addWidget(self.show_picture_all_detrend_faze_checkbox, 5, 0, 1, 2)
        show_file_layout.addWidget(self.show_mask_desintegration_checkbox, 6, 0, 1, 2)
        show_file_layout.addWidget(extend_mask_label, 7, 0)
        show_file_layout.addWidget(self.extend_mask_spinbox, 7, 1)

        save_file_layout.addWidget(self.save_original_data_checkbox, 0, 0, 1, 2)
        save_file_layout.addWidget(self.save_norm_data_checkbox, 1, 0, 1, 2)
        save_file_layout.addWidget(QtWidgets.QLabel("Percentage of erroneous points:"), 2, 0, 1, 1)
        save_file_layout.addWidget(self.percentage_of_erroneous_points_double_spinbox, 2, 1, 1, 1)
        save_file_layout.addWidget(self.save_detrend_data_checkbox, 3, 0, 1, 2)
        save_file_layout.addWidget(self.save_pictures_checkbox, 4, 0, 1, 2)
        save_file_layout.addWidget(folder_files_label, 5, 0, 1, 2)
        save_file_layout.addWidget(self.folder_files_pushbutton, 6, 0, 1, 2)
        save_file_layout.addWidget(folder_pictures_label, 7, 0, 1, 2)
        save_file_layout.addWidget(self.folder_pictures_pushbutton, 8, 0, 1, 2)


        photometry_file_layout.addWidget(quality_bitmask_label, 0, 0, 1, 1)
        photometry_file_layout.addWidget(self.quality_bitmask_combobox, 0, 1, 1, 1)
        photometry_file_layout.addWidget(self.only_new_data_checkbox, 1, 0, 1, 2)
        photometry_file_layout.addWidget(first_downloaded_sector_label, 2, 0, 1, 1)
        photometry_file_layout.addWidget(self.first_downloaded_sector_spinbox, 2, 1, 1, 1)
        photometry_file_layout.addWidget(self.test_only_checkbox, 3, 0, 1, 2)
        photometry_file_layout.addWidget(test_only_sectors_quantity_label, 4, 0, 1, 1)
        photometry_file_layout.addWidget(self.test_only_sectors_quantity_spinbox, 4, 1, 1, 1)
        photometry_file_layout.addWidget(self.change_focus_by_period, 5, 0, 1, 2)
        photometry_file_layout.addWidget(data_focus_label, 6, 0, 1, 1)
        photometry_file_layout.addWidget(self.data_focus_spinbox, 6, 1, 1, 1)
        photometry_file_layout.addWidget(self.find_max_power_period_checkbox, 7, 0, 1, 2)
        photometry_file_layout.addWidget(self.change_detrend_parameters_by_period_checkbox, 8, 0, 1, 2)

        main_layout.addWidget(input_file_groupbox, 0, 0)
        main_layout.addWidget(show_file_groupbox, 0, 1)
        main_layout.addWidget(save_file_groupbox, 1, 0)
        main_layout.addWidget(photometry_file_groupbox, 1, 1)

    def setup(self):
        from step_application import root
        self.step_main_form = root.step_main_form
        self.tess_import = root.tess_import
        self.tess_menu_window = root.tess_menu_window
        self.user = root.database.user
        self.tess_photometry_edit_window = root.tess_photometry_edit_window
        self.silicups_window = root.silicups_window
        self.photometry_star_list_window = root.photometry_star_list_window
        self.quality_bitmask_combobox.addItems(self.tess_import.quality_bitmask_list())
        self.data_focus_spinbox.setRange(1, 10)
        self.percentage_of_erroneous_points_double_spinbox.setRange(0, 10)
        self.quality_bitmask_combobox.addItems(self.tess_import.quality_bitmask_list())
        self.data_focus_spinbox.setRange(1, 10)

        self.save_action = self.step_main_form.save_action
        self.prediction_action = self.step_main_form.prediction_action
        self.star_edit_action = self.step_main_form.star_edit_action
        self.show_observation_action = self.step_main_form.observation_action
        self.show_lightcurve_action = self.step_main_form.lightcurve_action
        self.addAction(self.save_action)
        self.addAction(self.prediction_action)
        self.addAction(self.star_edit_action)
        self.addAction(self.show_observation_action)
        self.addAction(self.show_lightcurve_action)

        self.folder_data_pushbutton.clicked.connect(self.set_path_input)
        self.folder_files_pushbutton.clicked.connect(self.set_path_files)
        self.folder_pictures_pushbutton.clicked.connect(self.set_path_graphs)
        self.save_norm_data_checkbox.clicked.connect(self.norm_data_checkbox_changed)
        self.show_mask_desintegration_checkbox.clicked.connect(self.mask_desintegration_checkbox_change)
        self.only_new_data_checkbox.clicked.connect(self.new_data_checkbox_changed)
        self.test_only_checkbox.clicked.connect(self.test_only_checkbox_changed)

    def norm_data_checkbox_changed(self):
        self.percentage_of_erroneous_points_double_spinbox.setEnabled(self.save_norm_data_checkbox.isChecked())

    def mask_desintegration_checkbox_change(self):
        self.extend_mask_spinbox.setEnabled(self.show_mask_desintegration_checkbox.isChecked())

    def new_data_checkbox_changed(self):
        self.first_downloaded_sector_spinbox.setEnabled(self.only_new_data_checkbox.isChecked())

    def test_only_checkbox_changed(self):
        self.test_only_sectors_quantity_spinbox.setEnabled(self.test_only_checkbox.isChecked())

    def set_path_input(self):
        new_path = find_path_to_file(current_path=self.tess_import.data_path(), window_table="Set input data file")[0]
        if os.path.exists(new_path):
            self.tess_import.change_data_path(new_path)
            self.folder_data_pushbutton.setText(self.tess_import.data_path())

    def set_path_files(self):
        new_path = find_path_to_file(current_path=self.tess_import.file_path(), window_table="Set data folder",
                                     path_to_file=False)
        if os.path.exists(new_path):
            self.tess_import.change_file_path(new_path)
            self.folder_files_pushbutton.setText(self.tess_import.file_path())

    def set_path_graphs(self):
        new_path = find_path_to_file(current_path=self.tess_import.graph_path(), window_table="Set graph folder",
                                     path_to_file=False)
        if os.path.exists(new_path):
            self.tess_import.change_graph_path(new_path)
            self.folder_pictures_pushbutton.setText(self.tess_import.graph_path())

