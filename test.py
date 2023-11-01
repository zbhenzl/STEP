import cv2
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
from astropy.io import fits
from astropy.wcs import WCS
import imexam
from PyQt5 import QtWidgets, QtCore, QtGui
import sys
from datetime import *
import os
import threading
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
import matplotlib
matplotlib.use('Qt5Agg')
from scipy.optimize import least_squares


class SunMainForm(QtWidgets.QMainWindow):

    def __init__(self, **kvargs):
        super(SunMainForm, self).__init__(**kvargs)

        self.__author = "Zbynek Henzl"
        self.__version = "0.9"
        self.setWindowTitle("SUN - Analyzer")

        # Main Widget a layout
        main_page = QtWidgets.QWidget()
        self.main_page_layout = QtWidgets.QGridLayout()
        self.main_page_layout.setSpacing(10)
        self.main_page_layout.setContentsMargins(10, 10, 10, 10)
        main_page.setLayout(self.main_page_layout)
        self.setCentralWidget(main_page)
        # self.setWindowIcon(QtGui.QIcon("stairs.png"))
        self.folder = "H:\\astro\\Sun\\fotosféra"
        self.average = 0
        self.data = []
        self.header = []
        self.border_set = []
        self.__build()
        self.p = [0,0,1]
        self.active_areas_list = []


    def setup(self):
        self.show()
        self.folder_button.clicked.connect(self.new_folder)
        self.file_combobox.currentTextChanged.connect(self.new_image)
        self.circle_slider.valueChanged.connect(self.fit_curve)
        self.line_slider.valueChanged.connect(self.fit_curve)
        self.show_line_or_circle_checkbox.clicked.connect(self.fit_curve)
        self.line_border_spinbox.valueChanged.connect(self.fit_curve)
        self.details_combobox.currentIndexChanged.connect(self.__show_aria_detail)
        self.detail_or_graph_checkbox.clicked.connect(self.fit_curve)

    def __build(self):
        self.graph_original_groupbox = QtWidgets.QGroupBox("Original data")
        self.graph_clipped_groupbox = QtWidgets.QGroupBox("Clipped data")
        self.graph_detail_groupbox = QtWidgets.QGroupBox("Detail")

        self.graph_original_canvas = MplCanvas(self, width=10, height=4, dpi=100)
        self.graph_clipped_canvas = MplCanvas(self, width=10, height=4, dpi=100)
        self.graph_detail_canvas = MplCanvas(self, width=10, height=4, dpi=100)
        self.toolbar_original = NavigationToolbar(self.graph_original_canvas, self)
        self.toolbar_clipped = NavigationToolbar(self.graph_clipped_canvas, self)
        self.toolbar_detail = NavigationToolbar(self.graph_detail_canvas, self)
        self.toolbar_original_layout = QtWidgets.QGridLayout()
        self.toolbar_clipped_layout = QtWidgets.QGridLayout()
        self.toolbar_detail_layout = QtWidgets.QGridLayout()
        self.graph_original_groupbox.setLayout(self.toolbar_original_layout)
        self.graph_clipped_groupbox.setLayout(self.toolbar_clipped_layout)
        self.graph_detail_groupbox.setLayout(self.toolbar_detail_layout)

        self.header_text_edit = QtWidgets.QTextEdit()
        self.text = ""

        self.circle_slider = QtWidgets.QSlider(QtCore.Qt.Orientation.Vertical, self)
        self.circle_slider.setRange(10, 1000)
        self.circle_slider.setValue(1000)

        self.line_slider = QtWidgets.QSlider(QtCore.Qt.Orientation.Vertical, self)
        self.line_slider.setRange(0, 1000)
        self.line_slider.setValue(500)

        self.reserv_slider = QtWidgets.QSlider(QtCore.Qt.Orientation.Horizontal, self)
        self.show_line_or_circle_checkbox = QtWidgets.QCheckBox("circle / line")
        self.show_line_or_circle_checkbox.setChecked(True)
        self.line_border_spinbox = QtWidgets.QSpinBox()
        self.line_border_spinbox.setValue(10)
        self.line_border_spinbox.setRange(0, 45)


        self.toolbar_original_layout.addWidget(self.toolbar_original, 0, 0)
        self.toolbar_original_layout.addWidget(self.graph_original_canvas, 1, 0)
        self.toolbar_clipped_layout.addWidget(self.toolbar_clipped, 0, 0)
        self.toolbar_clipped_layout.addWidget(self.graph_clipped_canvas, 1, 0)
        self.toolbar_detail_layout.addWidget(self.toolbar_detail, 0, 0)
        self.toolbar_detail_layout.addWidget(self.graph_detail_canvas, 1, 0)



        self.info_label = QtWidgets.QLabel("choice_item:")
        self.file_combobox = QtWidgets.QComboBox()
        self.folder_button = QtWidgets.QPushButton("")

        self.detail_or_graph_checkbox = QtWidgets.QCheckBox("graph/detais")
        self.detail_or_graph_checkbox.setChecked(True)

        self.active_part_difference_spinbox = QtWidgets.QSpinBox()
        self.active_part_difference_spinbox.setRange(5, 95)
        self.active_part_difference_spinbox.setValue(20)

        self.details_combobox = QtWidgets.QComboBox()
        self.details_combobox.setMinimumWidth(250)


        # self.main_page_layout.addWidget(self.info_label, 0, 0)

        self.main_page_layout.addWidget(self.folder_button, 0, 1)
        self.main_page_layout.addWidget(self.show_line_or_circle_checkbox, 0, 0)
        self.main_page_layout.addWidget(self.file_combobox, 0, 3)
        self.main_page_layout.addWidget(self.detail_or_graph_checkbox, 0, 2)
        self.main_page_layout.addWidget(QtWidgets.QLabel("line border %:"), 0, 4)
        self.main_page_layout.addWidget(self.line_border_spinbox, 0, 5)
        self.main_page_layout.addWidget(QtWidgets.QLabel("active part difference %:"), 0, 6)
        self.main_page_layout.addWidget(self.active_part_difference_spinbox, 0, 7)
        self.main_page_layout.addWidget(QtWidgets.QLabel("active area:"), 0, 8)
        self.main_page_layout.addWidget(self.details_combobox, 0, 9)

        self.main_page_layout.addWidget(QtWidgets.QLabel("circle range"), 1, 0)
        self.main_page_layout.addWidget(self.circle_slider, 2, 0)
        self.main_page_layout.addWidget(QtWidgets.QLabel("line range"), 1, 1)
        self.main_page_layout.addWidget(self.line_slider, 2, 1)
        self.main_page_layout.addWidget(QtWidgets.QLabel("sieve coarseness"), 1, 4)
        self.main_page_layout.addWidget(self.reserv_slider, 1, 5, 1, 5)

        self.main_page_layout.addWidget(self.header_text_edit, 3, 0, 1, 2)
        self.main_page_layout.addWidget(self.graph_original_groupbox, 2, 2, 1, 2)
        self.main_page_layout.addWidget(self.graph_clipped_groupbox, 3, 2, 1, 2)
        self.main_page_layout.addWidget(self.graph_detail_groupbox, 2, 4, 2, 6)


    def new_folder(self):
        folder = QtWidgets.QFileDialog.getExistingDirectory(caption="Select directory", directory= self.folder)
        if not folder:
            return
        else:
            self.folder = folder
        self.fill()
        if self.file_combobox.currentText() != "No file":
            self.show_origin()

    def new_image(self):
        if self.file_combobox.currentIndex() > -1:
            if self.file_combobox.currentText() != "No file":
                self.show_origin()
                self.find_border_set()



    def files_in_folder(self, filter=".fits"):
        files_in_folder= os.listdir(self.folder)
        filtered_file = []
        for file in files_in_folder:
            if filter in file:
                filtered_file.append(file)
        if not filtered_file:
            filtered_file = ["No file"]
        return filtered_file

    def fill(self):
        self.folder_button.setText(self.folder)
        file_list = self.files_in_folder()
        self.file_combobox.clear()
        self.file_combobox.addItems(file_list)


    def fits_open(self, file):
        with fits.open(file) as hdu:
            info = hdu.info()
            data = hdu[0].data
            keys = hdu[0].header
            self.text = "Header is:\n"
            for i, key in enumerate(keys):
                self.text = self.text + str(key) + ":  " + str(keys[i]) + "\n"
            self.text = self.text + "End"
            self.header_text_edit.setText(self.text)
            return [data, keys, info]

    def show_origin(self):
        file = self.file_combobox.currentText()
        path = self.folder_button.text()
        file_path = path + "\\" + file
        hdu = self.fits_open(file_path)
        self.data = hdu[0]
        self.header = hdu[1]

        picture = Image.fromarray(self.data)
        self.find_average()

        # picture.show()
        self.toolbar_original.hide()
        self.graph_original_canvas.figure.clear()
        self.graph_original_canvas = MplCanvas(self, width=10, height=4, dpi=100)
        self.toolbar_original = NavigationToolbar(self.graph_original_canvas, self)
        self.toolbar_original_layout.addWidget(self.toolbar_original, 0, 0)
        self.toolbar_original_layout.addWidget(self.graph_original_canvas, 1, 0)

        self.graph_original_canvas.axes.imshow(picture, cmap="gray" )
        plt.close()

    def find_average(self):
        frequency_width = int(len(self.data[0]) / 10)
        if frequency_width < 1:
            frequency_width = 1
        frequency_high = int(len(self.data) / 10)
        if frequency_high < 1:
            frequency_high = 1
        sum_pixels = 0
        for i in range(0, len(self.data[0]), frequency_width):
           for j in range(0, len(self.data), frequency_high):
               sum_pixels = sum_pixels + self.data[j][i]
        average = sum_pixels / len(self.data[0]) * frequency_high * frequency_width / len(self.data)
        return average

    def find_border_set(self):
        average = self.find_average()
        border_set = []
        picture_width = len(self.data[0])
        picture_high = len(self.data)
        for i in range(0, picture_high, 20):
           for j in range(0, picture_width - 1, 20):
               if j + 20 > picture_width - 1:
                   j1 = picture_width
               else:
                   j1 = j + 20
               if self.data[i][j] < average:
                   if self.data[i][j1-1] > average:
                       for k in range(j, j1 - 1):
                           if self.data[i][k] < average:
                               if self.data[i][k + 1] > average:
                                   border_set.append([i,k])
               if self.data[i][j] > average:
                   if self.data[i][j1] < average:
                       for k in range(j, j1 - 1):
                           if self.data[i][k] > average:
                               if self.data[i][k + 1] < average:
                                   border_set.append([i,k])
        self.border_set = border_set
        self.fit_curve()


    # Define the residual function
    def __fun(self, parameters):
        res = []
        for x in self.border_set:
            res.append((x[0] - parameters[0]) ** 2 + (x[1] - parameters[1]) ** 2 - parameters[2] ** 2)
        return res

    def fit_curve(self):
        if len(self.border_set) < 2:
            print( "There is no Sun")
            return
        if self.border_set[0][0] == self.border_set[1][0]:
            y0 = (self.border_set[0][1] + self.border_set[1][1]) / 2
        else:
            y0 = self.border_set[0][1]
        index_center = int(len(self.border_set) / 2)
        x0 = self.border_set[index_center][0]
        p = [x0, y0, 900]
        res1 = least_squares(self.__fun, p)
        p0 = [res1.x[0], res1.x[1], res1.x[2]]
        self.p = p0
        self.data_clipped = self.data[int(p0[0] - p0[2] - 100):int(p0[0] + p0[2] + 100), int(p0[1] - p0[2] - 100):int(p0[1] + p0[2] + 100)]
        picture = Image.fromarray(self.data_clipped)

        # self.find_average()

        # picture.show()
        self.toolbar_clipped.hide()
        self.graph_clipped_canvas.figure.clear()
        self.graph_clipped_canvas = MplCanvas(self, width=10, height=4, dpi=100)
        self.toolbar_clipped = NavigationToolbar(self.graph_clipped_canvas, self)
        self.toolbar_clipped_layout.addWidget(self.toolbar_clipped, 0, 0)
        self.toolbar_clipped_layout.addWidget(self.graph_clipped_canvas, 1, 0)

        circle_points = np.linspace(0, 2 * np.pi, 1000)
        x_circle = p0[2] * np.cos(circle_points) + int(p0[1])
        y_circle = p0[2] * np.sin(circle_points) + int(p0[0])
        # x_inner = (p0[2] - 10) * np.cos(circle_points) + p0[2] + 100
        # y_inner = (p0[2] - 10) * np.sin(circle_points) + p0[2] + 100
        # x_outer = (p0[2] + 90) * np.cos(circle_points) + p0[2] + 100
        # y_outer = (p0[2] + 90) * np.sin(circle_points) + p0[2] + 100
        self.graph_clipped_canvas.axes.imshow(picture, cmap="gray" )
        self.graph_original_canvas.axes.plot(x_circle, y_circle, c="r")
        # self.graph_clipped_canvas.axes.plot(x_inner, y_inner)
        # self.graph_clipped_canvas.axes.plot(x_outer, y_outer)

        if self.show_line_or_circle_checkbox.isChecked():
            r = int((self.p[2]+99) / 1000 * self.circle_slider.value())
            points = self.__find_circle_points(r)
            self.graph_clipped_canvas.axes.plot(points[0], points[1], c="r")
            intensity_points = self.__find_intensity(points)
            # self.__check_intensity(r)

            if self.detail_or_graph_checkbox.isChecked():
                self.detail_graph_clear()
                self.graph_detail_canvas.axes.plot(intensity_points[1], intensity_points[0])
            else:
                self.detail_graph_clear()
                self.__check_intensity(r)
                self.__show_aria_detail()
        else:
            y_position = int(len(self.data_clipped) / 1000 * self.line_slider.value())
            start_position = int(self.line_border_spinbox.value() / 100 * len(self.data_clipped))
            end_position = len(self.data_clipped) - start_position
            intensity_points_x = []
            intensity_points_y = []
            for i in range(start_position,end_position):
                intensity_points_x.append(i)
                intensity_points_y.append(self.data_clipped[y_position][i])
            self.detail_graph_clear()
            self.graph_detail_canvas.axes.plot(intensity_points_x, intensity_points_y)
            self.graph_clipped_canvas.axes.plot(intensity_points_x, [y_position] * len(intensity_points_x), c="r")
        plt.close()

    def __show_aria_detail(self):
        if self.details_combobox.currentIndex() > -1 and not self.detail_or_graph_checkbox.isChecked():
            self.detail_graph_clear()
            index_aria = self.details_combobox.currentIndex()
            xmin = self.active_areas_list[index_aria][0]
            xmax = self.active_areas_list[index_aria][1]
            ymin = self.active_areas_list[index_aria][2]
            ymax = self.active_areas_list[index_aria][3]
            detail_area_data = self.data_clipped[xmin - 30 : xmax + 30, ymin - 30 : ymax + 30]
            picture = Image.fromarray(detail_area_data)
            self.graph_detail_canvas.axes.imshow(picture, cmap="gray")
        else:
            return

    def detail_graph_clear(self):
        self.toolbar_detail.hide()
        self.graph_detail_canvas.figure.clear()
        self.graph_detail_canvas = MplCanvas(self, width=10, height=4, dpi=100)
        self.toolbar_detail = NavigationToolbar(self.graph_detail_canvas, self)
        self.toolbar_detail_layout.addWidget(self.toolbar_detail, 0, 0)
        self.toolbar_detail_layout.addWidget(self.graph_detail_canvas, 1, 0)

    def __find_circle_points(self, r):
        circle_pointsx_1 = np.linspace(0, r - 1, int(r / 1))
        circle_pointsx_2 = r - circle_pointsx_1
        circle_pointsx_3 = -1 * circle_pointsx_1
        circle_pointsx_4 = -1 * circle_pointsx_2
        circle_pointsx = np.array(list(circle_pointsx_1) + list(circle_pointsx_2) + list(circle_pointsx_3)
                                  + list(circle_pointsx_4)) + self.p[2] + 100
        circle_pointsy_1 = r * np.sin(np.arccos(circle_pointsx_1 / r))
        circle_pointsy_2 = - r * np.sin(np.arccos(circle_pointsx_2 / r))
        circle_pointsy_3 = - r * np.sin(np.arccos(circle_pointsx_3 / r))
        circle_pointsy_4 = r * np.sin(np.arccos(circle_pointsx_4 / r))
        circle_pointsy = np.array(list(circle_pointsy_1) + list(circle_pointsy_2) + list(circle_pointsy_3)
                                  + list(circle_pointsy_4)) + self.p[2] + 100
        return [circle_pointsx, circle_pointsy]

    def __find_intensity(self, points):
        intensity_points_x = []
        intensity_points_y = []
        for i, x in enumerate(points[0]):
            intensity_points_x.append(self.data_clipped[int(x)][int(points[1][i])])
            intensity_points_y.append(i)
        intensity_points_x = np.array(intensity_points_x)
        intensity_points_y = np.array(intensity_points_y)

        return [intensity_points_x, intensity_points_y]

    def __check_intensity(self, r):
        self.active_areas_list = []
        active_areas_list_text = []
        circle_range_1 = list(range(10, int(r) - 7, 7))
        circle_range_2 = list(range(int(r) + 5, int(r) + 49, 5))
        total_range = circle_range_1 + circle_range_2

        for k in circle_range_1:
            points = self.__find_circle_points(k)
            intensity = self.__find_intensity(points)
            intensity_border_low = np.median(intensity[0]) * (1 - self.active_part_difference_spinbox.value() / 100)
            intensity_border_hi = np.median(intensity[0]) * (1 + self.active_part_difference_spinbox.value() / 200)
            for i in range(0, len(intensity[0]), 7):
                if intensity[0][i] < intensity_border_low: # or intensity[0][i] > intensity_border_hi:
                    save = True
                    xmin = int(points[0][i])
                    xmax = int(points[0][i])
                    ymin = int(points[1][i])
                    ymax = int(points[1][i])
                    for area in self.active_areas_list:
                        if area[0] <= xmin <= area[1] and area[2] <= ymin <= area[3]:
                            save = False
                    if save:
                        for j in range (int(points[0][i]) - 50, int(points[0][i]) + 50):
                            for k in range (int(points[1][i]) - 50, int(points[1][i]) + 50):
                                if self.data_clipped[j][k] < intensity_border_low: # or self.data_clipped[j][k] > intensity_border_hi:
                                    if xmin > j:
                                        xmin = j
                                    if xmax < j:
                                        xmax = j
                                    if ymin > k:
                                        ymin = k
                                    if ymax < k:
                                        ymax = k
                        save1 = True
                        for area in self.active_areas_list:
                            if ((area[0] <= xmin <= area[1]) or (area[0] <= xmax <= area[1]) or
                                    (xmin <= area[0] <= xmax) or (xmin <= area[1] <= xmax)) and (
                                    (area[2] <= ymin <= area[3]) or (area[2] <= ymax <= area[3]) or
                                    (ymin <= area[2] <= ymax) or (ymin <= area[3] <= ymax)):
                                save1 = False
                                area[0] = min(xmin, area[0])
                                area[1] = min(xmax, area[1])
                                area[2] = min(ymin, area[2])
                                area[3] = min(ymax, area[3])
                        if save1:
                            self.active_areas_list.append([xmin,xmax,ymin,ymax])
        for area in self.active_areas_list:
            active_areas_list_text.append("x: {0} to {1}, y: {2} to {3}".format(area[0],area[1],area[2],area[3]))
        self.details_combobox.clear()
        self.details_combobox.addItems(active_areas_list_text)

class MplCanvas(FigureCanvasQTAgg):

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super(MplCanvas, self).__init__(fig)


class SunApplication(QtWidgets.QApplication):

    def __init__(self):
        super(SunApplication, self).__init__(sys.argv)

        self.sun_main_window = SunMainForm()

    def build(self):
        self.sun_main_window.setup()
        self.sun_main_window.fill()
        self.sun_main_window.find_border_set()

        sys.exit(self.exec())


root = SunApplication()
root.build()

