from PyQt5 import QtWidgets
from step_main_form import Popup
from coordinate import Coordinate, read_coordinate
from object import Star
import os
from math import radians


def strip_text(text: str):
    if text:
        text = text.strip(",").strip(";")
    return text


def mistake(title, error, button="OK"):
    mistake_window = Popup(title, error, buttons=button.split(","))
    mistake_window.do()


class ImportObjectWindow(QtWidgets.QWidget):

    def __init__(self, *args, **kvargs):
        super(ImportObjectWindow, self).__init__(*args, **kvargs)

        self.setWindowTitle("Import Star from Silicups")
        main_layout = QtWidgets.QGridLayout()
        self.setLayout(main_layout)
        main_layout.setSpacing(10)


        self.comp_list = ["", "", "", "", "", "", "", "", "", "", "", ""]

        info_label = QtWidgets.QLabel("The following objects were found in the selected file:")
        self.find_object_combobox = QtWidgets.QComboBox()
        self.select_object_button = QtWidgets.QPushButton("IMPORT")

        self.name_editline = QtWidgets.QLineEdit("")
        self.alt_name_editline = QtWidgets.QLineEdit("")
        self.period_editline = QtWidgets.QLineEdit("")
        self.m0_editline = QtWidgets.QLineEdit("")
        self.variability_type_editline = QtWidgets.QLineEdit("")
        self.mag0_editline = QtWidgets.QDoubleSpinBox(decimals=8)
        self.sec_phase_editline = QtWidgets.QDoubleSpinBox(decimals=8)
        self.a_pri_editline = QtWidgets.QDoubleSpinBox(decimals=8)
        self.d_pri_editline = QtWidgets.QDoubleSpinBox(decimals=8)
        self.g_pri_editline = QtWidgets.QDoubleSpinBox(decimals=8)
        self.c_pri_editline = QtWidgets.QDoubleSpinBox(decimals=8)
        self.a_sec_editline = QtWidgets.QDoubleSpinBox(decimals=8)
        self.d_sec_editline = QtWidgets.QDoubleSpinBox(decimals=8)
        self.g_sec_editline = QtWidgets.QDoubleSpinBox(decimals=8)
        self.c_sec_editline = QtWidgets.QDoubleSpinBox(decimals=8)
        self.a_sin1_editline = QtWidgets.QDoubleSpinBox(decimals=8)
        self.a_sin2_editline = QtWidgets.QDoubleSpinBox(decimals=8)
        self.a_sin3_editline = QtWidgets.QDoubleSpinBox(decimals=8)
        self.a_cos1_editline = QtWidgets.QDoubleSpinBox(decimals=8)
        self.a_cos2_editline = QtWidgets.QDoubleSpinBox(decimals=8)
        self.a_cos3_editline = QtWidgets.QDoubleSpinBox(decimals=8)
        self.name_checkbox = QtWidgets.QCheckBox("Name:")
        self.alt_name_checkbox = QtWidgets.QRadioButton("Alt_name:")
        self.period_checkbox = QtWidgets.QCheckBox("Period: ")
        self.m0_checkbox = QtWidgets.QCheckBox("Epoch:")
        self.variability_type_checkbox = QtWidgets.QCheckBox("type var.:")
        self.model_checkbox = QtWidgets.QCheckBox("Import model")

        mag0_editline = QtWidgets.QLabel("mag0:")
        sec_phase_editline = QtWidgets.QLabel("sec_phase")
        a_editline = QtWidgets.QLabel("a_pri/sec")
        d_editline = QtWidgets.QLabel("d_pri/sec")
        g_editline = QtWidgets.QLabel("g_pri/sec")
        c_editline = QtWidgets.QLabel("c_pri/sec")
        a_sin1_editline = QtWidgets.QLabel("a_sin1/cos1")
        a_sin2_editline = QtWidgets.QLabel("a_sin2/cos2")
        a_sin3_editline = QtWidgets.QLabel("a_sin3/cos3")


        model_group_box = QtWidgets.QGroupBox("model")
        model_group_layout = QtWidgets.QGridLayout()
        model_group_box.setLayout(model_group_layout)

        model_group_layout.addWidget(self.model_checkbox, 0, 1)
        model_group_layout.addWidget(self.mag0_editline, 1, 1, 1, 2)
        model_group_layout.addWidget(self.sec_phase_editline, 2, 1, 1, 2)
        model_group_layout.addWidget(self.a_pri_editline, 3, 1)
        model_group_layout.addWidget(self.d_pri_editline, 4, 1)
        model_group_layout.addWidget(self.g_pri_editline, 5, 1)
        model_group_layout.addWidget(self.c_pri_editline, 6, 1)
        model_group_layout.addWidget(self.a_sec_editline, 3, 2)
        model_group_layout.addWidget(self.d_sec_editline, 4, 2)
        model_group_layout.addWidget(self.g_sec_editline, 5, 2)
        model_group_layout.addWidget(self.c_sec_editline, 6, 2)
        model_group_layout.addWidget(self.a_sin1_editline, 7, 1)
        model_group_layout.addWidget(self.a_sin2_editline, 8, 1)
        model_group_layout.addWidget(self.a_sin3_editline, 9, 1)
        model_group_layout.addWidget(self.a_cos1_editline, 7, 2)
        model_group_layout.addWidget(self.a_cos2_editline, 8, 2)
        model_group_layout.addWidget(self.a_cos3_editline, 9, 2)

        model_group_layout.addWidget(mag0_editline, 1, 0)
        model_group_layout.addWidget(sec_phase_editline, 2, 0)
        model_group_layout.addWidget(a_editline, 3, 0)
        model_group_layout.addWidget(d_editline, 4, 0)
        model_group_layout.addWidget(g_editline, 5, 0)
        model_group_layout.addWidget(c_editline, 6, 0)
        model_group_layout.addWidget(a_sin1_editline, 7, 0)
        model_group_layout.addWidget(a_sin2_editline, 8, 0)
        model_group_layout.addWidget(a_sin3_editline, 9, 0)

        series_label = QtWidgets.QLabel("Select the series for import other information:")
        self.series_list_combobox = QtWidgets.QComboBox()

        self.var_name_lineedit = QtWidgets.QLineEdit()
        self.var_rec_lineedit = QtWidgets.QLineEdit()
        self.var_dec_lineedit = QtWidgets.QLineEdit()
        self.var_catalog_lineedit = QtWidgets.QLineEdit()
        self.var_cross_id_lineedit = QtWidgets.QLineEdit()
        self.var_cat_rec_lineedit = QtWidgets.QLineEdit()
        self.var_cat_dec_lineedit = QtWidgets.QLineEdit()
        self.var_cat_mag_lineedit = QtWidgets.QLineEdit()
        self.var_b_v_lineedit = QtWidgets.QLineEdit()
        self.var_j_k_lineedit = QtWidgets.QLineEdit()

        self.var_name_checkbox = QtWidgets.QRadioButton("Alt.name:")
        self.var_rec_checkbox = QtWidgets.QRadioButton("RA/DE:")
        self.var_catalog_checkbox = QtWidgets.QCheckBox("Kalalog:")
        self.var_cat_rec_checkbox = QtWidgets.QRadioButton("Kat.RA/DE:")
        self.var_cat_mag_checkbox = QtWidgets.QCheckBox("Katalog mag:")
        self.var_b_v_checkbox = QtWidgets.QCheckBox("B-V:")
        self.var_j_k_checkbox = QtWidgets.QCheckBox("J-K:")

        self.cmp_name_lineedit = QtWidgets.QLineEdit()
        self.cmp_rec_lineedit = QtWidgets.QLineEdit()
        self.cmp_dec_lineedit = QtWidgets.QLineEdit()
        self.cmp_catalog_lineedit = QtWidgets.QLineEdit()
        self.cmp_cross_id_lineedit = QtWidgets.QLineEdit()
        self.cmp_cat_rec_lineedit = QtWidgets.QLineEdit()
        self.cmp_cat_dec_lineedit = QtWidgets.QLineEdit()
        self.cmp_cat_mag_lineedit = QtWidgets.QLineEdit()
        self.cmp_b_v_lineedit = QtWidgets.QLineEdit()
        self.cmp_j_k_lineedit = QtWidgets.QLineEdit()

        self.cmp_name_label = QtWidgets.QLabel("Name:")
        self.cmp_rec_checkbox = QtWidgets.QRadioButton("RA/DE:")
        self.cmp_catalog_checkbox = QtWidgets.QCheckBox("Kalalog:")
        self.cmp_cat_rec_checkbox = QtWidgets.QRadioButton("Kat.RA/DE:")
        self.cmp_cat_mag_checkbox = QtWidgets.QCheckBox("Katalog mag:")
        self.cmp_b_v_checkbox = QtWidgets.QCheckBox("B-V:")
        self.cmp_j_k_checkbox = QtWidgets.QCheckBox("J-K:")

        cmp_groupbox = QtWidgets.QGroupBox("COMPERISON STAR - you must import separately BEFORE you import star")
        cmp_layout = QtWidgets.QVBoxLayout()
        cmp_groupbox.setLayout(cmp_layout)
        cmp_layout1 = QtWidgets.QHBoxLayout()
        cmp_layout2 = QtWidgets.QHBoxLayout()
        cmp_layout.addLayout(cmp_layout1)
        cmp_layout.addLayout(cmp_layout2)

        self.cmp0_checkbox = QtWidgets.QRadioButton("CMP0")
        self.cmp1_checkbox = QtWidgets.QRadioButton("CMP1")
        self.cmp2_checkbox = QtWidgets.QRadioButton("CMP2")
        self.cmp3_checkbox = QtWidgets.QRadioButton("CMP3")
        self.cmp4_checkbox = QtWidgets.QRadioButton("CMP4")
        self.cmp5_checkbox = QtWidgets.QRadioButton("CMP5")
        self.cmp6_checkbox = QtWidgets.QRadioButton("CMP6")
        self.cmp7_checkbox = QtWidgets.QRadioButton("CMP7")
        self.cmp8_checkbox = QtWidgets.QRadioButton("CMP8")
        self.cmp9_checkbox = QtWidgets.QRadioButton("CMP9")
        self.chk1_checkbox = QtWidgets.QRadioButton("CHK1")
        self.cmp_import_button = QtWidgets.QPushButton("Import CMP")

        cmp_layout1.addWidget(self.cmp0_checkbox)
        cmp_layout1.addWidget(self.cmp1_checkbox)
        cmp_layout1.addWidget(self.cmp2_checkbox)
        cmp_layout1.addWidget(self.cmp3_checkbox)
        cmp_layout1.addWidget(self.cmp4_checkbox)
        cmp_layout1.addWidget(self.cmp5_checkbox)
        cmp_layout2.addWidget(self.cmp6_checkbox)
        cmp_layout2.addWidget(self.cmp7_checkbox)
        cmp_layout2.addWidget(self.cmp8_checkbox)
        cmp_layout2.addWidget(self.cmp9_checkbox)
        cmp_layout2.addWidget(self.chk1_checkbox)
        cmp_layout2.addWidget(self.cmp_import_button)

        self.cmp_buttongroup = QtWidgets.QButtonGroup()
        self.cmp_buttongroup.addButton(self.cmp0_checkbox)
        self.cmp_buttongroup.addButton(self.cmp1_checkbox)
        self.cmp_buttongroup.addButton(self.cmp2_checkbox)
        self.cmp_buttongroup.addButton(self.cmp3_checkbox)
        self.cmp_buttongroup.addButton(self.cmp4_checkbox)
        self.cmp_buttongroup.addButton(self.cmp5_checkbox)
        self.cmp_buttongroup.addButton(self.cmp6_checkbox)
        self.cmp_buttongroup.addButton(self.cmp7_checkbox)
        self.cmp_buttongroup.addButton(self.cmp8_checkbox)
        self.cmp_buttongroup.addButton(self.cmp9_checkbox)
        self.cmp_buttongroup.addButton(self.chk1_checkbox)

        self.name_buttongroup = QtWidgets.QButtonGroup()
        self.name_buttongroup.addButton(self.alt_name_checkbox)
        self.name_buttongroup.addButton(self.var_name_checkbox)

        self.var_coor_buttongroup = QtWidgets.QButtonGroup()
        self.var_coor_buttongroup.addButton(self.var_cat_rec_checkbox)
        self.var_coor_buttongroup.addButton(self.var_rec_checkbox)

        self.cmp_coor_buttongroup = QtWidgets.QButtonGroup()
        self.cmp_coor_buttongroup.addButton(self.cmp_rec_checkbox)
        self.cmp_coor_buttongroup.addButton(self.cmp_cat_rec_checkbox)

        self.cmp_cons_combobox = QtWidgets.QComboBox()
        self.cmp_epoch_combobox = QtWidgets.QComboBox()
        cmp_cons_label = QtWidgets.QLabel("Constellation (if empty = filled in by software):")
        cmp_epoch_label = QtWidgets.QLabel("Eq.: ")
        input_file_label = QtWidgets.QLabel("Input File:")
        self.input_file_label = QtWidgets.QLabel()
        self.input_file_pushbutton = QtWidgets.QPushButton("Select new file")
        main_layout.addWidget(input_file_label, 0, 0, 1, 1)
        main_layout.addWidget(self.input_file_label, 0, 1, 1, 5)
        main_layout.addWidget(self.input_file_pushbutton, 0, 6, 1, 2)


        main_layout.addWidget(info_label, 1, 0, 1, 3)
        main_layout.addWidget(self.find_object_combobox, 2, 1, 1, 1)
        main_layout.addWidget(self.select_object_button, 2, 0)

        main_layout.addWidget(self.name_editline, 3, 1)
        main_layout.addWidget(self.alt_name_editline, 4, 1)
        main_layout.addWidget(self.period_editline, 5, 1)
        main_layout.addWidget(self.m0_editline, 6, 1)
        main_layout.addWidget(self.variability_type_editline, 7, 1)
        main_layout.addWidget(model_group_box, 8, 0, 9, 2)

        main_layout.addWidget(self.name_checkbox, 3, 0)
        main_layout.addWidget(self.alt_name_checkbox, 4, 0)
        main_layout.addWidget(self.period_checkbox, 5, 0)
        main_layout.addWidget(self.m0_checkbox, 6, 0)
        main_layout.addWidget(self.variability_type_checkbox, 7, 0)

        main_layout.addWidget(series_label, 1, 2, 1, 6)
        main_layout.addWidget(self.series_list_combobox, 2, 2, 1, 6)

        main_layout.addWidget(self.var_name_lineedit, 3, 3, 1, 5)
        main_layout.addWidget(self.var_rec_lineedit, 4, 3, 1, 3)
        main_layout.addWidget(self.var_dec_lineedit, 4, 6, 1, 2)
        main_layout.addWidget(self.var_catalog_lineedit, 6, 3, 1, 3)
        main_layout.addWidget(self.var_cross_id_lineedit, 6, 6, 1, 2)
        main_layout.addWidget(self.var_cat_rec_lineedit, 5, 3, 1, 3)
        main_layout.addWidget(self.var_cat_dec_lineedit, 5, 6, 1, 2)
        main_layout.addWidget(self.var_cat_mag_lineedit, 7, 3, 1, 1)
        main_layout.addWidget(self.var_b_v_lineedit, 7, 5)
        main_layout.addWidget(self.var_j_k_lineedit, 7, 7)

        main_layout.addWidget(self.var_name_checkbox, 3, 2)
        main_layout.addWidget(self.var_rec_checkbox, 4, 2)
        main_layout.addWidget(self.var_catalog_checkbox, 6, 2)
        main_layout.addWidget(self.var_cat_rec_checkbox, 5, 2)
        main_layout.addWidget(self.var_cat_mag_checkbox, 7, 2)
        main_layout.addWidget(self.var_b_v_checkbox, 7, 4)
        main_layout.addWidget(self.var_j_k_checkbox, 7, 6)

        main_layout.addWidget(cmp_groupbox, 8, 2, 3, 6)

        main_layout.addWidget(self.cmp_name_lineedit, 11, 3, 1, 5)
        main_layout.addWidget(self.cmp_rec_lineedit, 12, 3, 1, 3)
        main_layout.addWidget(self.cmp_dec_lineedit, 12, 6, 1, 2)
        main_layout.addWidget(self.cmp_catalog_lineedit, 14, 3, 1, 3)
        main_layout.addWidget(self.cmp_cross_id_lineedit, 14, 6, 1, 2)
        main_layout.addWidget(self.cmp_cat_rec_lineedit, 13, 3, 1, 3)

        main_layout.addWidget(self.cmp_name_label, 11, 2)
        main_layout.addWidget(self.cmp_rec_checkbox, 12, 2)
        main_layout.addWidget(self.cmp_catalog_checkbox, 14, 2)
        main_layout.addWidget(self.cmp_cat_rec_checkbox, 13, 2)
        main_layout.addWidget(self.cmp_cat_dec_lineedit, 13, 6, 1, 2)

        main_layout.addWidget(self.cmp_cat_mag_checkbox, 15, 2)
        main_layout.addWidget(self.cmp_cat_mag_lineedit, 15, 3, 1, 1)
        main_layout.addWidget(self.cmp_b_v_checkbox, 15, 4)
        main_layout.addWidget(self.cmp_b_v_lineedit, 15, 5)
        main_layout.addWidget(self.cmp_j_k_checkbox, 15, 6)
        main_layout.addWidget(self.cmp_j_k_lineedit, 15, 7)

        main_layout.addWidget(cmp_cons_label, 16, 2, 1, 3)
        main_layout.addWidget(self.cmp_cons_combobox, 16, 5, 1, 1)
        main_layout.addWidget(cmp_epoch_label, 16, 6)
        main_layout.addWidget(self.cmp_epoch_combobox, 16, 7, 1, 1)



    def setup(self):
        from step_application import root
        self.step_main_form = root.step_main_form
        self.object_edit_window = root.object_edit_window
        self.database = root.database
        self.all_objects = []
        self.all_names = []
        self.select_object_button.clicked.connect(self.import_data)
        self.cmp_cons_combobox.addItems(self.database.const_abbrs)
        self.cmp_epoch_combobox.addItems(self.database.possible_epoch)
        self.find_object_combobox.currentTextChanged.connect(self.fill_imported_object)
        self.series_list_combobox.currentTextChanged.connect(self.import_series)
        self.cmp0_checkbox.clicked.connect(self.fill_comp)
        self.cmp1_checkbox.clicked.connect(self.fill_comp)
        self.cmp2_checkbox.clicked.connect(self.fill_comp)
        self.cmp3_checkbox.clicked.connect(self.fill_comp)
        self.cmp4_checkbox.clicked.connect(self.fill_comp)
        self.cmp5_checkbox.clicked.connect(self.fill_comp)
        self.cmp6_checkbox.clicked.connect(self.fill_comp)
        self.cmp7_checkbox.clicked.connect(self.fill_comp)
        self.cmp8_checkbox.clicked.connect(self.fill_comp)
        self.cmp9_checkbox.clicked.connect(self.fill_comp)
        self.chk1_checkbox.clicked.connect(self.fill_comp)
        self.cmp_import_button.clicked.connect(self.save_comp)
        self.input_file_pushbutton.clicked.connect(self.set_input_file)

    def import_data(self):
        if self.name_editline.isEnabled():
            self.save_star()
        elif not self.name_editline.isEnabled() and self.period_editline.isEnabled():
            self.save_pair()
        else:
            self.save_model()

    def import_pair_active_item(self, active):
        self.name_editline.setEnabled(active)
        self.alt_name_editline.setEnabled(active)
        self.name_checkbox.setEnabled(active)
        self.alt_name_checkbox.setEnabled(active)
        self.var_name_lineedit.setEnabled(active)
        self.var_rec_lineedit.setEnabled(active)
        self.var_dec_lineedit.setEnabled(active)
        self.var_catalog_lineedit.setEnabled(active)
        self.var_cross_id_lineedit.setEnabled(active)
        self.var_cat_rec_lineedit.setEnabled(active)
        self.var_cat_dec_lineedit.setEnabled(active)
        self.var_cat_mag_lineedit.setEnabled(active)
        self.var_b_v_lineedit.setEnabled(active)
        self.var_j_k_lineedit.setEnabled(active)
        self.var_name_checkbox.setEnabled(active)
        self.var_rec_checkbox.setEnabled(active)
        self.var_catalog_checkbox.setEnabled(active)
        self.var_cat_rec_checkbox.setEnabled(active)
        self.var_cat_mag_checkbox.setEnabled(active)
        self.var_b_v_checkbox.setEnabled(active)
        self.var_j_k_checkbox.setEnabled(active)

    def import_model_active_item(self, active):
        self.period_editline.setEnabled(active)
        self.period_checkbox.setEnabled(active)
        self.m0_editline.setEnabled(active)
        self.m0_checkbox.setEnabled(active)
        self.variability_type_editline.setEnabled(active)
        self.variability_type_checkbox.setEnabled(active)

    def set_input_file(self):
        if os.path.exists(self.database.user.silicups_file_path()):
            path_to_file = self.database.user.silicups_file_path()
        else:
            path_to_file = os.path.join(os.getenv("APPDATA"), "Quadruples")
        path_to_silicups_file = QtWidgets.QFileDialog.getOpenFileName(caption="Select the file",
                                                                      directory=path_to_file,
                                                                      filter="*.sif")
        if path_to_silicups_file[0] == "":
            return
        self.database.user.change_silicups_file_path(path_to_silicups_file[0])
        self.import_stars_from_silicups()

    def import_stars_from_silicups(self):
        self.input_file_label.setText(self.database.user.silicups_file_path())
        soubor = []
        try:
            with open(self.database.user.silicups_file_path(), "r", encoding="utf-8") as f:
                for row in f.readlines():
                    soubor.append(str(row))
        except:
            mistake("Access denied", "Access to the file has been denied, check your access permissions")
            return
        self.all_objects.clear()
        self.all_names.clear()
        new_object = False
        period = None
        m0 = None
        name = None
        alt_name = None
        variability_type = None
        mag0 = None
        sec_phase = None
        a_pri = None
        d_pri = None
        g_pri = None
        c_pri = None
        a_sec = None
        d_sec = None
        g_sec = None
        c_sec = None
        a_sin1 = None
        a_sin2 = None
        a_sin3 = None
        a_cos1 = None
        a_cos2 = None
        a_cos3 = None
        series_list = []
        series = False
        for row in soubor:
            item = row.strip()
            if new_object:
                if "caption = " == item[0:10]:
                    self.all_names.append(item[11:len(item) - 1])
                    name = item[11:len(item) - 1]
                if "name = " == item[0:7]:
                    self.all_names.append(item[8:len(item) - 1])
                    name = item[8:len(item) - 1]
                if "alternate_name = " in item:
                    alt_name = item[18:len(item) - 1]
                if "alternate_caption =" in item:
                    alt_name = item[21:len(item) - 1]
                if "variability_type = " in item:
                    variability_type = item[20:len(item) - 1]
                if "period = " == item[0:9]:
                    period = item[9:len(item)]
                if "m0 = " == item[0:5]:
                    m0 = item[5:len(item)]
                if "series" == item:
                    series = True
                if "absolute_path = " in item and series:
                    series_list.append(item[17:len(item) - 1])
                if "mag0 =" in item:
                    mag0 = item[7: len(item)]
                if "sec_phase =" in item:
                    sec_phase = item[12: len(item)]
                if "a_pri =" in item:
                    a_pri = item[8: len(item)]
                if "d_pri =" in item:
                    d_pri = item[8: len(item)]
                if "g_pri =" in item:
                    g_pri = item[8: len(item)]
                if "c_pri =" in item:
                    c_pri = item[8: len(item)]
                if "a_sec =" in item:
                    a_sec = item[8: len(item)]
                if "d_sec =" in item:
                    d_sec = item[8: len(item)]
                if "g_sec =" in item:
                    g_sec = item[8: len(item)]
                if "c_sec =" in item:
                    c_sec = item[8: len(item)]
                if "a_sin1" in item:
                    a_sin1 = item[9: len(item)]
                if "a_sin2" in item:
                    a_sin2 = item[9: len(item)]
                if "a_sin3" in item:
                    a_sin3 = item[9: len(item)]
                if "a_cos1" in item:
                    a_cos1 = item[9: len(item)]
                if "a_cos2" in item:
                    a_cos2 = item[9: len(item)]
                if "a_cos3" in item:
                    a_cos3 = item[9: len(item)]
            if item == "object":
                new_object = True
            if item == "end_object":
                new_object = False
                self.all_objects.append([name, alt_name, period, m0, variability_type, mag0, sec_phase, a_pri,
                                         d_pri, g_pri, c_pri, a_sec, d_sec, g_sec, c_sec, a_sin1, a_sin2, a_sin3,
                                         a_cos1, a_cos2, a_cos3, series_list])
                new_object = False
                period = None
                m0 = None
                name = None
                alt_name = None
                variability_type = None
                mag0 = None
                sec_phase = None
                a_pri = None
                d_pri = None
                g_pri = None
                c_pri = None
                a_sec = None
                d_sec = None
                g_sec = None
                c_sec = None
                a_sin1 = None
                a_sin2 = None
                a_sin3 = None
                a_cos1 = None
                a_cos2 = None
                a_cos3 = None
                series_list = []
                series = False
        self.find_object_combobox.clear()
        if self.all_names:
            self.find_object_combobox.addItems(self.all_names)
            self.fill_imported_object()
            self.check_checkbox(True, True)

    def check_checkbox(self, star: bool, model: bool):
        self.period_checkbox.setChecked(star)
        self.m0_checkbox.setChecked(star)
        self.name_checkbox.setChecked(star)
        self.alt_name_checkbox.setChecked(star)
        self.variability_type_checkbox.setChecked(star)
        self.model_checkbox.setChecked(model)
        self.var_cat_rec_checkbox.setChecked(star)
        self.var_catalog_checkbox.setChecked(star)
        self.var_cat_mag_checkbox.setChecked(star)
        self.var_b_v_checkbox.setChecked(star)
        self.var_j_k_checkbox.setChecked(star)
        self.cmp_cat_rec_checkbox.setChecked(star)
        self.cmp_catalog_checkbox.setChecked(star)
        self.cmp_cat_mag_checkbox.setChecked(star)
        self.cmp_b_v_checkbox.setChecked(star)
        self.cmp_j_k_checkbox.setChecked(star)

    def fill_imported_object(self):
        star_index = self.find_object_combobox.currentIndex()
        self.name_editline.setText(strip_text(self.all_objects[star_index][0]))
        self.alt_name_editline.setText(strip_text(self.all_objects[star_index][1]))
        self.period_editline.setText(strip_text(self.all_objects[star_index][2]))
        self.m0_editline.setText(strip_text(self.all_objects[star_index][3]))
        self.variability_type_editline.setText(strip_text(self.all_objects[star_index][4]))
        try:
            self.mag0_editline.setValue(float(self.all_objects[star_index][5]))
        except:
            self.mag0_editline.clear()

        try:
            self.sec_phase_editline.setValue(float(self.all_objects[star_index][6]))
        except:
            self.sec_phase_editline.clear()

        try:
            self.a_pri_editline.setValue(float(self.all_objects[star_index][7]))
        except:
            self.a_pri_editline.clear()

        try:
            self.d_pri_editline.setValue(float(self.all_objects[star_index][8]))
        except:
            self.d_pri_editline.clear()

        try:
            self.g_pri_editline.setValue(float(self.all_objects[star_index][9]))
        except:
            self.g_pri_editline.clear()

        try:
            self.c_pri_editline.setValue(float(self.all_objects[star_index][10]))
        except:
            self.c_pri_editline.clear()

        try:
            self.a_sec_editline.setValue(float(self.all_objects[star_index][11]))
        except:
            self.a_sec_editline.clear()

        try:
            self.d_sec_editline.setValue(float(self.all_objects[star_index][12]))
        except:
            self.d_sec_editline.clear()

        try:
            self.g_sec_editline.setValue(float(self.all_objects[star_index][13]))
        except:
            self.g_sec_editline.clear()

        try:
            self.c_sec_editline.setValue(float(self.all_objects[star_index][14]))
        except:
            self.c_sec_editline.clear()

        try:
            self.a_sin1_editline.setValue(float(self.all_objects[star_index][15]))
        except:
            self.a_sin1_editline.clear()

        try:
            self.a_sin2_editline.setValue(float(self.all_objects[star_index][16]))
        except:
            self.a_sin2_editline.clear()

        try:
            self.a_sin3_editline.setValue(float(self.all_objects[star_index][17]))
        except:
            self.a_sin3_editline.clear()

        try:
            self.a_cos1_editline.setValue(float(self.all_objects[star_index][18]))
        except:
            self.a_cos1_editline.clear()

        try:
            self.a_cos2_editline.setValue(float(self.all_objects[star_index][19]))
        except:
            self.a_cos2_editline.clear()

        try:
            self.a_cos3_editline.setValue(float(self.all_objects[star_index][20]))
        except:
            self.a_cos3_editline.clear()

        self.series_list_combobox.clear()
        self.series_list_combobox.addItems(self.all_objects[star_index][21])

    def save_star(self):
        if not self.name_editline.text().replace(" ", ""):
            mistake("Name", "Name is empty")
            return
        if self.var_rec_checkbox.isChecked() and (not self.var_rec_lineedit.text() or not self.var_dec_lineedit.text()):
            mistake("Coordinate", "Coordinates are empty")
            return
        if self.var_cat_rec_checkbox.isChecked() and (not self.var_cat_rec_lineedit.text() or not self.var_cat_dec_lineedit.text()):
            mistake("Catalogue coordinate", "Catalogue coordinates are empty")
            return
        if self.var_rec_checkbox.isChecked():
            declination_list = read_coordinate(self.var_dec_lineedit.text(), coor_format="declination_degree")
            rektascenze_list = read_coordinate(self.var_rec_lineedit.text())
        else:
            declination_list = read_coordinate(self.var_cat_dec_lineedit.text(), coor_format="declination_degree")
            rektascenze_list = read_coordinate(self.var_cat_rec_lineedit.text())
        if declination_list[5]:
            mistake("declination reading error", declination_list[5])
            return
        if rektascenze_list[5]:
            mistake("rektascenze reading error", rektascenze_list[5])
            return
        self.object_edit_window.star_rec_h_spinbox.setValue(int(rektascenze_list[0]))
        self.object_edit_window.star_rec_m_spinbox.setValue(int(rektascenze_list[1]))
        self.object_edit_window.star_rec_s_spinbox.setValue(float(rektascenze_list[2]))
        self.object_edit_window.star_dec_h_spinbox.setValue(int(declination_list[0]))
        self.object_edit_window.star_dec_m_spinbox.setValue(int(declination_list[1]))
        self.object_edit_window.star_dec_s_spinbox.setValue(float(declination_list[2]))
        if declination_list[3] < 0:
            self.object_edit_window.dec_sign.setCurrentText("-")
        else:
            self.object_edit_window.dec_sign.setCurrentText("+")
        self.object_edit_window.star_constilation_combobox.setCurrentText(
            Coordinate(rektascenze_list[3], declination_list[3]).get_const())

        self.object_edit_window.star_name_editline.setText(strip_text(self.name_editline.text()))
        if self.alt_name_checkbox.isChecked():
            self.object_edit_window.star_alternativ_name_editline.setText(strip_text(self.alt_name_editline.text()))
        else:
            self.object_edit_window.star_alternativ_name_editline.setText(strip_text(self.var_name_lineedit.text()))
        if self.var_cat_mag_checkbox.isChecked() and self.var_cat_mag_lineedit.text().replace(" ", ""):
            try:
                self.object_edit_window.star_mag_doublespinbox.setValue(float(self.var_cat_mag_lineedit.text()))
            except:
                mistake("numer error", "Magnitude must be a number")
        else:
            self.object_edit_window.star_mag_doublespinbox.clear()
        if self.var_catalog_checkbox.isChecked():
            if self.var_catalog_lineedit.text() == "UCAC4" or self.var_catalog_lineedit.text() == "USNO-B1.0":
                self.object_edit_window.cross_type_label.setText(self.var_catalog_lineedit.text())
                self.object_edit_window.cross_number_label.setText(strip_text(self.var_cross_id_lineedit.text()))
            else:
                self.object_edit_window.cross_type_label.clear()
                self.object_edit_window.cross_number_label.clear()
                mistake("error", "Unknown catalogue")
        if self.var_b_v_checkbox.isChecked() and self.var_b_v_lineedit.text().replace(" ", ""):
            try:
                self.object_edit_window.star_b_v_doublespinbox.setValue(float(self.var_b_v_lineedit.text()))
            except:
                mistake("numer error", "B-V must be a number")
        else:
            self.object_edit_window.star_b_v_doublespinbox.clear()

        if self.var_j_k_checkbox.isChecked() and self.var_j_k_lineedit.text().replace(" ", ""):
            try:
                self.object_edit_window.star_j_k_doublespinbox.setValue(float(self.var_j_k_lineedit.text()))
            except:
                mistake("numer error", "J-K must be a number")
        else:
            self.object_edit_window.star_j_k_doublespinbox.clear()

        self.save_pair()


    def save_pair(self):
        if self.period_checkbox.isChecked() and self.period_editline.text().replace(" ", ""):
            try:
                self.object_edit_window.lightcurve_period_editline.setText(str(float(
                    self.period_editline.text().replace(" ", ""))))
            except:
                mistake("Period error", "Period must to be a number")
        if self.m0_checkbox.isChecked() and self.m0_editline.text().replace(" ", ""):
            try:
                self.object_edit_window.lightcurve_epoch_editline.setText(str(float(
                    self.m0_editline.text().replace(" ", ""))))
            except:
                mistake("Epoch error", "Epoch must to be a number")

        if self.variability_type_checkbox.isChecked() and self.variability_type_editline.text().replace(" ", ""):
            var_type = self.variability_type_editline.text().strip().replace(",", "")
            if var_type in self.database.variability_type:
                self.object_edit_window.lightcurve_type_combobox.setCurrentText(var_type)
            else:
                new_var_type = Popup('New var.type',
                                     'Unknown variability type\n{0}\nDo you want to add?'.format(var_type),
                                     buttons="OK, Not to import".split(","))
                if new_var_type.do == 0:
                    self.database.variability_type.append(var_type)
                    self.object_edit_window.lightcurve_type_combobox.addItem(var_type)
                    self.object_edit_window.lightcurve_type_combobox.setCurrentText(var_type)
        self.save_model()

    def save_model(self):
        if self.model_checkbox.isChecked():
            if self.mag0_editline:
                self.object_edit_window.model_mag0_doulespinbox.setValue(self.mag0_editline.value())
            else:
                self.object_edit_window.model_mag0_doulespinbox.clear()

            if self.sec_phase_editline:
                self.object_edit_window.model_sec_phase_doulespinbox.setValue(self.sec_phase_editline.value())
            else:
                self.object_edit_window.model_sec_phase_doulespinbox.clear()

            if self.a_pri_editline:
                self.object_edit_window.model_a_pri_doulespinbox.setValue(self.a_pri_editline.value())
            else:
                self.object_edit_window.model_a_pri_doulespinbox.clear()

            if self.d_pri_editline:
                self.object_edit_window.model_d_pri_doulespinbox.setValue(self.d_pri_editline.value())
            else:
                self.object_edit_window.model_d_pri_doulespinbox.clear()

            if self.g_pri_editline:
                self.object_edit_window.model_g_pri_doulespinbox.setValue(self.g_pri_editline.value())
            else:
                self.object_edit_window.model_g_pri_doulespinbox.clear()

            if self.c_pri_editline:
                self.object_edit_window.model_c_pri_doulespinbox.setValue(self.c_pri_editline.value())
            else:
                self.object_edit_window.model_c_pri_doulespinbox.clear()

            if self.a_sec_editline:
                self.object_edit_window.model_a_sec_doulespinbox.setValue(self.a_sec_editline.value())
            else:
                self.object_edit_window.model_a_sec_doulespinbox.clear()

            if self.d_sec_editline:
                self.object_edit_window.model_d_sec_doulespinbox.setValue(self.d_sec_editline.value())
            else:
                self.object_edit_window.model_d_sec_doulespinbox.clear()

            if self.g_sec_editline:
                self.object_edit_window.model_g_sec_doulespinbox.setValue(self.g_sec_editline.value())
            else:
                self.object_edit_window.model_g_sec_doulespinbox.clear()

            if self.c_sec_editline:
                self.object_edit_window.model_c_sec_doulespinbox.setValue(self.c_sec_editline.value())
            else:
                self.object_edit_window.model_c_sec_doulespinbox.clear()

            if self.a_sin1_editline:
                self.object_edit_window.model_sin1_doulespinbox.setValue(self.a_sin1_editline.value())
            else:
                self.object_edit_window.model_sin1_doulespinbox.clear()

            if self.a_sin2_editline:
                self.object_edit_window.model_sin2_doulespinbox.setValue(self.a_sin2_editline.value())
            else:
                self.object_edit_window.model_sin2_doulespinbox.clear()

            if self.a_sin3_editline:
                self.object_edit_window.model_sin3_doulespinbox.setValue(self.a_sin3_editline.value())
            else:
                self.object_edit_window.model_sin3_doulespinbox.clear()

            if self.a_cos1_editline:
                self.object_edit_window.model_cos1_doulespinbox.setValue(self.a_cos1_editline.value())
            else:
                self.object_edit_window.model_cos1_doulespinbox.clear()

            if self.a_cos2_editline:
                self.object_edit_window.model_cos2_doulespinbox.setValue(self.a_cos2_editline.value())
            else:
                self.object_edit_window.model_cos2_doulespinbox.clear()

            if self.a_cos3_editline:
                self.object_edit_window.model_cos3_doulespinbox.setValue(self.a_cos3_editline.value())
            else:
                self.object_edit_window.model_cos3_doulespinbox.clear()
        self.close()

    def import_series(self):
        file = self.series_list_combobox.currentText()
        row_index_list = ['Name:', 'RA:', 'Dec:', 'Catalog:', 'CatalogId:', 'CatalogRA:', 'CatalogDec:', 'CatalogMag:',
                      'CatalogB-V:', 'CatalogJ-K:']
        comp_index_list = ["VAR Name:", "CMP0 Name:", "CMP1 Name:", "CMP2 Name:", "CMP3 Name:", "CMP4 Name:", "CMP5 Name:",
                     "CMP6 Name:", "CMP7 Name:", "CMP8 Name:", "CMP9 Name:", "CHK1 Name:"]
        new_row = ["", "", "", "", "", "", "", "", "", ""]
        self.comp_list = ["", "", "", "", "", "", "", "", "", "", "", ""]
        soubor = []
        try:
            with open(file, "r", encoding="utf-8") as f:
                for row in f.readlines():
                    soubor.append(str(row))
        except:
            pass
        for row in soubor:
            for j, cmp in enumerate(comp_index_list):
                if cmp in row:
                    for i, key in enumerate(row_index_list):
                        split_row = row.split(" ")
                        if key in split_row:
                            position = split_row.index(key)
                            new_row[i] = split_row[position + 1].strip()
                    self.comp_list[j] = new_row
                    new_row = ["", "", "", "", "", "", "", "", "", ""]
        if self.comp_list[0]:
            self.var_name_lineedit.setText(strip_text(self.comp_list[0][0]))
            self.var_rec_lineedit.setText(strip_text(self.comp_list[0][1]))
            self.var_dec_lineedit.setText(strip_text(self.comp_list[0][2]))
            self.var_catalog_lineedit.setText(strip_text(self.comp_list[0][3]))
            self.var_cross_id_lineedit.setText(strip_text(self.comp_list[0][4]))
            self.var_cat_rec_lineedit.setText(strip_text(self.comp_list[0][5]))
            self.var_cat_dec_lineedit.setText(strip_text(self.comp_list[0][6]))
            self.var_cat_mag_lineedit.setText(strip_text(self.comp_list[0][7]))
            self.var_b_v_lineedit.setText(strip_text(self.comp_list[0][8]))
            self.var_j_k_lineedit.setText(strip_text(self.comp_list[0][9]))
        if self.comp_list[11]:
            self.chk1_checkbox.setEnabled(True)
            self.chk1_checkbox.setChecked(True)
        else:
            self.chk1_checkbox.setEnabled(False)

        if self.comp_list[10]:
            self.cmp9_checkbox.setEnabled(True)
            self.cmp9_checkbox.setChecked(True)
        else:
            self.cmp9_checkbox.setEnabled(False)

        if self.comp_list[9]:
            self.cmp8_checkbox.setEnabled(True)
            self.cmp8_checkbox.setChecked(True)
        else:
            self.cmp8_checkbox.setEnabled(False)

        if self.comp_list[8]:
            self.cmp7_checkbox.setEnabled(True)
            self.cmp7_checkbox.setChecked(True)
        else:
            self.cmp7_checkbox.setEnabled(False)

        if self.comp_list[7]:
            self.cmp6_checkbox.setEnabled(True)
            self.cmp6_checkbox.setChecked(True)
        else:
            self.cmp6_checkbox.setEnabled(False)

        if self.comp_list[6]:
            self.cmp5_checkbox.setEnabled(True)
            self.cmp5_checkbox.setChecked(True)
        else:
            self.cmp5_checkbox.setEnabled(False)

        if self.comp_list[5]:
            self.cmp4_checkbox.setEnabled(True)
            self.cmp4_checkbox.setChecked(True)
        else:
            self.cmp4_checkbox.setEnabled(False)

        if self.comp_list[4]:
            self.cmp3_checkbox.setEnabled(True)
            self.cmp3_checkbox.setChecked(True)
        else:
            self.cmp3_checkbox.setEnabled(False)

        if self.comp_list[3]:
            self.cmp2_checkbox.setEnabled(True)
            self.cmp2_checkbox.setChecked(True)
        else:
            self.cmp2_checkbox.setEnabled(False)

        if self.comp_list[2]:
            self.cmp1_checkbox.setEnabled(True)
            self.cmp1_checkbox.setChecked(True)
        else:
            self.cmp1_checkbox.setEnabled(False)

        if self.comp_list[1]:
            self.cmp0_checkbox.setEnabled(True)
            self.cmp0_checkbox.setChecked(True)
        else:
            self.cmp0_checkbox.setEnabled(False)
        self.fill_comp()

    def fill_comp(self):
        self.cmp_name_lineedit.clear()
        self.cmp_rec_lineedit.clear()
        self.cmp_dec_lineedit.clear()
        self.cmp_catalog_lineedit.clear()
        self.cmp_cross_id_lineedit.clear()
        self.cmp_cat_rec_lineedit.clear()
        self.cmp_cat_dec_lineedit.clear()
        self.cmp_cat_mag_lineedit.clear()
        self.cmp_b_v_lineedit.clear()
        self.cmp_j_k_lineedit.clear()
        current_cmp = ""

        if self.cmp0_checkbox.isChecked():
            current_cmp = self.comp_list[1]
        if self.cmp1_checkbox.isChecked():
            current_cmp = self.comp_list[2]
        if self.cmp2_checkbox.isChecked():
            current_cmp = self.comp_list[3]
        if self.cmp3_checkbox.isChecked():
            current_cmp = self.comp_list[4]
        if self.cmp4_checkbox.isChecked():
            current_cmp = self.comp_list[5]
        if self.cmp5_checkbox.isChecked():
            current_cmp = self.comp_list[6]
        if self.cmp6_checkbox.isChecked():
            current_cmp = self.comp_list[7]
        if self.cmp7_checkbox.isChecked():
            current_cmp = self.comp_list[8]
        if self.cmp8_checkbox.isChecked():
            current_cmp = self.comp_list[9]
        if self.cmp9_checkbox.isChecked():
            current_cmp = self.comp_list[10]
        if self.chk1_checkbox.isChecked():
            current_cmp = self.comp_list[11]
        if current_cmp:
            self.cmp_name_lineedit.setText(strip_text(current_cmp[0]))
            self.cmp_rec_lineedit.setText(strip_text(current_cmp[1]))
            self.cmp_dec_lineedit.setText(strip_text(current_cmp[2]))
            self.cmp_catalog_lineedit.setText(strip_text(current_cmp[3]))
            self.cmp_cross_id_lineedit.setText(strip_text(current_cmp[4]))
            self.cmp_cat_rec_lineedit.setText(strip_text(current_cmp[5]))
            self.cmp_cat_dec_lineedit.setText(strip_text(current_cmp[6]))
            self.cmp_cat_mag_lineedit.setText(strip_text(current_cmp[7]))
            self.cmp_b_v_lineedit.setText(strip_text(current_cmp[8]))
            self.cmp_j_k_lineedit.setText(strip_text(current_cmp[9]))

    def save_comp(self):
        if not self.cmp_name_lineedit.text():
            mistake("Name", "Name is empty")
            return
        if self.cmp_rec_checkbox.isChecked() and (not self.cmp_rec_lineedit.text() or not self.cmp_dec_lineedit.text()):
            mistake("Coordinate", "Coordinates are empty")
            return
        if self.cmp_cat_rec_checkbox.isChecked() and (not self.cmp_cat_rec_lineedit.text() or not self.cmp_cat_dec_lineedit.text()):
            mistake("Catalogue coordinate", "Catalogue coordinates are empty")
            return
        if self.cmp_rec_checkbox.isChecked():
            declination_list = read_coordinate(self.cmp_dec_lineedit.text(), coor_format="declination_degree")
            rektascenze_list = read_coordinate(self.cmp_rec_lineedit.text())
        else:
            declination_list = read_coordinate(self.cmp_cat_dec_lineedit.text(), coor_format="declination_degree")
            rektascenze_list = read_coordinate(self.cmp_cat_rec_lineedit.text())
        if declination_list[5]:
            mistake("declination reading error", declination_list[5])
            return
        if rektascenze_list[5]:
            mistake("rektascenze reading error", rektascenze_list[5])
            return

        name = self.cmp_name_lineedit.text()
        rektascenze = rektascenze_list[3]
        declination = declination_list[3]
        const = self.cmp_cons_combobox.currentText()
        eq = self.cmp_epoch_combobox.currentText()
        if self.cmp_catalog_checkbox.isChecked():
            catalog = self.cmp_catalog_lineedit.text()
            catalog_id = self.cmp_cross_id_lineedit.text()
        else:
            catalog = None
            catalog_id = None
        near_star_list = self.database.stars.already_exist(name, rektascenze, declination, catalogue=catalog,
                                                           catalogue_id=catalog_id)
        if near_star_list[1]:
            if "error" in near_star_list[1]:
                mistake("Import failed", near_star_list[1])
                return
            else:
                error = Popup("Near star",
                              "Following stars are in aperture:\n{0}\nStar may be "
                              "already exist.\nDo you want to continue".
                              format(",".join(near_star_list[0])),
                              "OK, Exit".split())
                if error.do() == 1:
                    return
        if self.cmp_cat_mag_checkbox.isChecked() and self.cmp_cat_mag_lineedit.text():
            try:
                mag = str(float(self.cmp_cat_mag_lineedit.text()))
            except:
                mistake("numer error", "Magnitude must be a number")
                return
        else:
            mag = ""

        if self.cmp_b_v_checkbox.isChecked() and self.cmp_b_v_lineedit.text():
            try:
                b_v = str(float(self.cmp_b_v_lineedit.text()))
            except:
                mistake("numer error", "B-V must be a number")
                return
        else:
            b_v = ""
        if self.cmp_j_k_checkbox.isChecked() and self.cmp_j_k_lineedit.text():
            try:
                j_k = str(float(self.cmp_j_k_lineedit.text()))
            except:
                mistake("numer error", "J-K must be a number")
                return
        else:
            j_k = ""

        if catalog:
            if catalog == "UCAC4":
                ucac4 = catalog_id
                usnob1 = ""
            else:
                ucac4 = ""
                usnob1 = catalog_id
        else:
            ucac4 = ""
            usnob1 = ""

        new_coor = Coordinate(rektascenze, declination, epoch=int(eq))
        if not const:
            const = new_coor.get_const()
        new_cmp = Star(str(self.database.next_star()), name, "", new_coor, mag, const, "", "CMP", "", "", "", b_v, j_k,
                         ucac4, usnob1, "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "",
                         variability=False)
        self.database.stars.add_star(new_cmp)
        self.database.increase_next_star()

        if self.cmp0_checkbox.isChecked():
            self.object_edit_window.pair_comp0_checkbox.setText(str(new_cmp.id()))
        if self.cmp1_checkbox.isChecked():
            self.object_edit_window.pair_comp1_checkbox.setText(str(new_cmp.id()))
        if self.cmp2_checkbox.isChecked():
            self.object_edit_window.pair_comp2_checkbox.setText(str(new_cmp.id()))
        if self.cmp3_checkbox.isChecked():
            self.object_edit_window.pair_comp3_checkbox.setText(str(new_cmp.id()))
        if self.cmp4_checkbox.isChecked():
            self.object_edit_window.pair_comp4_checkbox.setText(str(new_cmp.id()))
        if self.cmp5_checkbox.isChecked():
            self.object_edit_window.pair_comp5_checkbox.setText(str(new_cmp.id()))
        if self.cmp6_checkbox.isChecked():
            self.object_edit_window.pair_comp6_checkbox.setText(str(new_cmp.id()))
        if self.cmp7_checkbox.isChecked():
            self.object_edit_window.pair_comp7_checkbox.setText(str(new_cmp.id()))
        if self.cmp8_checkbox.isChecked():
            self.object_edit_window.pair_comp8_checkbox.setText(str(new_cmp.id()))
        if self.cmp9_checkbox.isChecked():
            self.object_edit_window.pair_comp9_checkbox.setText(str(new_cmp.id()))
        if self.chk1_checkbox.isChecked():
            self.object_edit_window.pair_chk1_checkbox.setText(str(new_cmp.id()))

