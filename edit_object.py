from PyQt5 import QtWidgets, QtCore, QtGui
from math import *
from import_star import *
from step_main_form import Popup
from variables import *
from database import check_input
from coordinate import Coordinate


class EditObjectWindow(QtWidgets.QWidget):

    def __init__(self, *args, **kvargs):
        super(EditObjectWindow, self).__init__(*args, **kvargs)

        self.__pair_was_add = ""
        self.const_abbrs = ["", "And", "Ant", "Aps", "Aql", "Aqr", "Ara", "Ari", "Aur", "Boo", "Cae", "Cam", "Cap",
                            "Car", "Cas", "Cen", "Cep", "Cet", "Cha", "Cir", "CMa", "CMi", "Cnc", "Col", "Com", "CrA",
                            "CrB", "Crt", "Cru", "Crv", "CVn", "Cyg", "Del", "Dor", "Dra", "Equ", "Eri", "For", "Gem",
                            "Gru", "Her", "Hor", "Hya", "Hyi", "Ind", "Lac", "Leo", "Lep", "Lib", "LMi", "Lup", "Lyn",
                            "Lyr", "Men", "Mic", "Mon", "Mus", "Nor", "Oct", "Oph", "Ori", "Pav", "Peg", "Per", "Phe",
                            "Pic", "PsA", "Psc", "Pup", "Pyx", "Ret", "Scl", "Sco", "Sct", "Ser", "Sex", "Sge", "Sgr",
                            "Tau", "Tel", "TrA", "Tri", "Tuc", "UMa", "UMi", "Vel", "Vir", "Vol", "Vul"]

        self.setWindowTitle("Edit Star")
        main_layout = QtWidgets.QGridLayout()
        self.setLayout(main_layout)
        self.note_widget_height = 85

        self.pair_checkgroup = QtWidgets.QGroupBox("Choice pair or pulsation in multiple eclipse star")
        pair_layout = QtWidgets.QHBoxLayout()
        self.pair_checkgroup.setLayout(pair_layout)
        self.pair_buttongroup = QtWidgets.QButtonGroup()
        self.pair_a_checkbox = QtWidgets.QRadioButton("A")
        self.pair_a_checkbox.setChecked(True)
        self.pair_b_checkbox = QtWidgets.QRadioButton("B")
        self.pair_c_checkbox = QtWidgets.QRadioButton("C")
        self.pair_d_checkbox = QtWidgets.QRadioButton("D")
        self.pair_e_checkbox = QtWidgets.QRadioButton("E")
        self.pair_f_checkbox = QtWidgets.QRadioButton("F")

        self.pair_buttongroup.addButton(self.pair_a_checkbox)
        self.pair_buttongroup.addButton(self.pair_b_checkbox)
        self.pair_buttongroup.addButton(self.pair_c_checkbox)
        self.pair_buttongroup.addButton(self.pair_d_checkbox)
        self.pair_buttongroup.addButton(self.pair_e_checkbox)
        self.pair_buttongroup.addButton(self.pair_f_checkbox)

        pair_layout.addWidget(self.pair_a_checkbox)
        pair_layout.addWidget(self.pair_b_checkbox)
        pair_layout.addWidget(self.pair_c_checkbox)
        pair_layout.addWidget(self.pair_d_checkbox)
        pair_layout.addWidget(self.pair_e_checkbox)
        pair_layout.addWidget(self.pair_f_checkbox)

        self.comp_checkgroup = QtWidgets.QGroupBox("Choice comparison star")
        comp1_layout = QtWidgets.QFormLayout()
        self.comp_checkgroup.setLayout(comp1_layout)
        self.pair_comp0_checkbox = QtWidgets.QLineEdit()
        self.pair_comp1_checkbox = QtWidgets.QLineEdit()
        self.pair_comp2_checkbox = QtWidgets.QLineEdit()
        self.pair_comp3_checkbox = QtWidgets.QLineEdit()
        self.pair_comp4_checkbox = QtWidgets.QLineEdit()
        self.pair_comp5_checkbox = QtWidgets.QLineEdit()
        self.pair_comp6_checkbox = QtWidgets.QLineEdit()
        self.pair_comp7_checkbox = QtWidgets.QLineEdit()
        self.pair_comp8_checkbox = QtWidgets.QLineEdit()
        self.pair_comp9_checkbox = QtWidgets.QLineEdit()
        self.pair_chk1_checkbox = QtWidgets.QLineEdit()

        self.pair_comp0_checkbox.setInputMask("0000")
        self.pair_comp1_checkbox.setInputMask("0000")
        self.pair_comp2_checkbox.setInputMask("0000")
        self.pair_comp3_checkbox.setInputMask("0000")
        self.pair_comp4_checkbox.setInputMask("0000")
        self.pair_comp5_checkbox.setInputMask("0000")
        self.pair_comp6_checkbox.setInputMask("0000")
        self.pair_comp7_checkbox.setInputMask("0000")
        self.pair_comp8_checkbox.setInputMask("0000")
        self.pair_comp9_checkbox.setInputMask("0000")
        self.pair_chk1_checkbox.setInputMask("0000")

        comp1_layout.addRow(QtWidgets.QLabel("Comp0"), self.pair_comp0_checkbox)
        comp1_layout.addRow(QtWidgets.QLabel("Comp1"), self.pair_comp1_checkbox)
        comp1_layout.addRow(QtWidgets.QLabel("Comp2"), self.pair_comp2_checkbox)
        comp1_layout.addRow(QtWidgets.QLabel("Comp3"), self.pair_comp3_checkbox)
        comp1_layout.addRow(QtWidgets.QLabel("Comp4"), self.pair_comp4_checkbox)
        comp1_layout.addRow(QtWidgets.QLabel("Comp5"), self.pair_comp5_checkbox)
        comp1_layout.addRow(QtWidgets.QLabel("Comp6"), self.pair_comp6_checkbox)
        comp1_layout.addRow(QtWidgets.QLabel("Comp7"), self.pair_comp7_checkbox)
        comp1_layout.addRow(QtWidgets.QLabel("Comp8"), self.pair_comp8_checkbox)
        comp1_layout.addRow(QtWidgets.QLabel("Comp9"), self.pair_comp9_checkbox)
        comp1_layout.addRow(QtWidgets.QLabel("Chk1"), self.pair_chk1_checkbox)

        # star parameters
        star_groupbox = QtWidgets.QGroupBox("Star parameters")
        star_layout = QtWidgets.QVBoxLayout()
        star_groupbox.setLayout(star_layout)
        self.star_id_editline = QtWidgets.QLineEdit()
        self.star_id_editline.setReadOnly(True)
        self.star_name_editline = QtWidgets.QLineEdit()
        self.star_alternativ_name_editline = QtWidgets.QLineEdit()
        self.star_ekvinokcium_combobox = QtWidgets.QComboBox()
        self.star_constilation_combobox = QtWidgets.QComboBox()
        self.star_constilation_combobox.addItems(self.const_abbrs)
        self.star_rec_h_spinbox = QtWidgets.QSpinBox()
        self.star_rec_m_spinbox = QtWidgets.QSpinBox()
        self.star_rec_s_spinbox = QtWidgets.QDoubleSpinBox(decimals=3)
        self.dec_sign = QtWidgets.QComboBox()
        self.dec_sign.addItems(["+", "-"])
        self.star_dec_h_spinbox = QtWidgets.QSpinBox()
        self.star_dec_m_spinbox = QtWidgets.QSpinBox()
        self.star_dec_s_spinbox = QtWidgets.QDoubleSpinBox(decimals=3)

        self.star_rec_h_spinbox.setRange(0, 23)
        self.star_rec_m_spinbox.setRange(0, 59)
        self.star_rec_s_spinbox.setRange(0, 59.999)
        self.star_dec_h_spinbox.setRange(0, 89)
        self.star_dec_m_spinbox.setRange(0, 59)
        self.star_dec_s_spinbox.setRange(0, 59.999)

        self.star_mag_doublespinbox = QtWidgets.QDoubleSpinBox(decimals=3)
        self.star_type_combobox = QtWidgets.QComboBox()
        self.star_type_add_button = QtWidgets.QPushButton("Add type")
        self.star_type_add_button.setEnabled(False)
        self.star_b_v_doublespinbox = QtWidgets.QDoubleSpinBox()
        self.star_j_k_doublespinbox = QtWidgets.QDoubleSpinBox()
        self.star_b_v_doublespinbox.setRange(-2, 3)
        self.star_j_k_doublespinbox.setRange(-2, 3)

        self.star_id_editline.setAlignment(QtCore.Qt.AlignRight)
        self.star_name_editline.setAlignment(QtCore.Qt.AlignRight)
        self.star_alternativ_name_editline.setAlignment(QtCore.Qt.AlignRight)
        self.star_mag_doublespinbox.setRange(0, 23)

        star_id_label = QtWidgets.QLabel("Star Id:")
        star_name_label = QtWidgets.QLabel("Name:")
        star_alternativ_name_label = QtWidgets.QLabel("Alt.name:")
        star_ekvinokcium_label = QtWidgets.QLabel("eq.:")
        star_constilation_label = QtWidgets.QLabel("Const:")
        star_rec_label = QtWidgets.QLabel("RA.eq.:")
        star_dec_label = QtWidgets.QLabel("DE.eq.:")
        star_mag_label = QtWidgets.QLabel("Mag:")
        star_type_label = QtWidgets.QLabel("Type:")
        star_b_v_label = QtWidgets.QLabel("B-V:")
        star_j_k_label = QtWidgets.QLabel("J-K:")

        self.star_mag_doublespinbox.setFixedWidth(55)
        self.star_type_add_button.setFixedWidth(55)
        self.star_type_combobox.setFixedWidth(150)

        star_id_layout = QtWidgets.QHBoxLayout()
        star_id_layout.addWidget(star_id_label)
        star_id_layout.addWidget(self.star_id_editline)
        star_id_layout.addWidget(star_constilation_label)
        star_id_layout.addWidget(self.star_constilation_combobox)

        star_name_layout = QtWidgets.QHBoxLayout()
        star_name_layout.addWidget(star_name_label)
        star_name_layout.addWidget(self.star_name_editline)

        star_alt_name_layout = QtWidgets.QHBoxLayout()
        star_alt_name_layout.addWidget(star_alternativ_name_label)
        star_alt_name_layout.addWidget(self.star_alternativ_name_editline)

        star_rec_layout = QtWidgets.QHBoxLayout()
        star_rec_layout.addWidget(star_rec_label)
        star_rec_layout.addWidget(self.star_rec_h_spinbox)
        star_rec_layout.addWidget(self.star_rec_m_spinbox)
        star_rec_layout.addWidget(self.star_rec_s_spinbox)
        star_dec_layout = QtWidgets.QHBoxLayout()
        star_dec_layout.addWidget(star_dec_label)
        star_dec_layout.addWidget(self.dec_sign)
        star_dec_layout.addWidget(self.star_dec_h_spinbox)
        star_dec_layout.addWidget(self.star_dec_m_spinbox)
        star_dec_layout.addWidget(self.star_dec_s_spinbox)

        star_mag_layout = QtWidgets.QHBoxLayout()
        star_mag_layout.addWidget(star_mag_label)
        star_mag_layout.addWidget(self.star_mag_doublespinbox)
        star_mag_layout.addWidget(star_ekvinokcium_label)
        star_mag_layout.addWidget(self.star_ekvinokcium_combobox)

        star_type_layout = QtWidgets.QHBoxLayout()
        star_type_layout.addWidget(star_type_label)
        star_type_layout.addWidget(self.star_type_combobox)
        star_type_layout.addWidget(self.star_type_add_button)

        star_b_v_layout = QtWidgets.QHBoxLayout()
        star_b_v_layout.addWidget(star_b_v_label)
        star_b_v_layout.addWidget(self.star_b_v_doublespinbox)
        star_b_v_layout.addWidget(star_j_k_label)
        star_b_v_layout.addWidget(self.star_j_k_doublespinbox)

        star_layout.addLayout(star_id_layout)
        star_layout.addLayout(star_name_layout)
        star_layout.addLayout(star_alt_name_layout)
        star_layout.addLayout(star_rec_layout)
        star_layout.addLayout(star_dec_layout)
        star_layout.addLayout(star_mag_layout)
        star_layout.addLayout(star_type_layout)
        star_layout.addLayout(star_b_v_layout)
        star_layout.setSpacing(10)

        # lightcurve parameters
        lightkurve_groupbox = QtWidgets.QGroupBox("lightcurve parameters")
        lightkurve_layout = QtWidgets.QFormLayout()
        lightkurve_groupbox.setLayout(lightkurve_layout)
        self.lightcurve_period_editline = QtWidgets.QLineEdit()
        self.lightcurve_epoch_editline = QtWidgets.QLineEdit()
        self.lightcurve_type_combobox = QtWidgets.QComboBox()
        self.lightcurve_type_button = QtWidgets.QPushButton("Add var.type")
        self.lightcurve_amplitude_prim_doulespinbox = QtWidgets.QDoubleSpinBox(decimals=5)
        self.lightcurve_amplitude_sec_doulespinbox = QtWidgets.QDoubleSpinBox(decimals=5)
        self.lightcurve_d_big_prim_doulespinbox = QtWidgets.QDoubleSpinBox(decimals=5)
        self.lightcurve_d_big_sec_doulespinbox = QtWidgets.QDoubleSpinBox(decimals=5)
        self.lightcurve_d_prim_doulespinbox = QtWidgets.QDoubleSpinBox(decimals=5)
        self.lightcurve_d_sec_doulespinbox = QtWidgets.QDoubleSpinBox(decimals=5)

        self.lightcurve_period_editline.setAlignment(QtCore.Qt.AlignRight)
        self.lightcurve_epoch_editline.setAlignment(QtCore.Qt.AlignRight)
        self.lightcurve_amplitude_prim_doulespinbox.setRange(0, 3)
        self.lightcurve_amplitude_sec_doulespinbox.setRange(0, 3)

        lightkurve_layout.addRow(QtWidgets.QLabel("Period: "), self.lightcurve_period_editline)
        lightkurve_layout.addRow(QtWidgets.QLabel("Epoch: "), self.lightcurve_epoch_editline)
        lightkurve_layout.addRow(QtWidgets.QLabel("Var.type: "), self.lightcurve_type_combobox)
        lightkurve_layout.addRow(None, self.lightcurve_type_button)
        lightkurve_layout.addRow(QtWidgets.QLabel("Amp.prim.: "), self.lightcurve_amplitude_prim_doulespinbox)
        lightkurve_layout.addRow(QtWidgets.QLabel("Amp.sec.: "), self.lightcurve_amplitude_sec_doulespinbox)
        lightkurve_layout.addRow(QtWidgets.QLabel("D prim.: "), self.lightcurve_d_big_prim_doulespinbox)
        lightkurve_layout.addRow(QtWidgets.QLabel("D sec.: "), self.lightcurve_d_big_sec_doulespinbox)
        lightkurve_layout.addRow(QtWidgets.QLabel("d prim.: "), self.lightcurve_d_prim_doulespinbox)
        lightkurve_layout.addRow(QtWidgets.QLabel("d. sec: "), self.lightcurve_d_sec_doulespinbox)

        # katalog
        cross_groupbox = QtWidgets.QGroupBox("cross id.")
        cross_layout = QtWidgets.QHBoxLayout()
        cross_groupbox.setLayout(cross_layout)

        self.cross_type_label = QtWidgets.QLabel("")
        self.cross_number_label = QtWidgets.QLabel("")
        cross_layout.addWidget(self.cross_type_label)
        cross_layout.addWidget(self.cross_number_label)

        # model
        model_groupbox = QtWidgets.QGroupBox("phenomenological model")
        model_layout = QtWidgets.QHBoxLayout()
        model_part1_layout = QtWidgets.QFormLayout()
        model_part2_layout = QtWidgets.QFormLayout()
        model_groupbox.setLayout(model_layout)
        model_layout.addLayout(model_part1_layout)
        model_layout.addLayout(model_part2_layout)
        self.model_mag0_doulespinbox = QtWidgets.QDoubleSpinBox(decimals=8)
        self.model_sec_phase_doulespinbox = QtWidgets.QDoubleSpinBox(decimals=8)
        self.model_a_pri_doulespinbox = QtWidgets.QDoubleSpinBox(decimals=8)
        self.model_d_pri_doulespinbox = QtWidgets.QDoubleSpinBox(decimals=8)
        self.model_g_pri_doulespinbox = QtWidgets.QDoubleSpinBox(decimals=8)
        self.model_c_pri_doulespinbox = QtWidgets.QDoubleSpinBox(decimals=8)
        self.model_a_sec_doulespinbox = QtWidgets.QDoubleSpinBox(decimals=8)
        self.model_d_sec_doulespinbox = QtWidgets.QDoubleSpinBox(decimals=8)
        self.model_g_sec_doulespinbox = QtWidgets.QDoubleSpinBox(decimals=8)
        self.model_c_sec_doulespinbox = QtWidgets.QDoubleSpinBox(decimals=8)
        self.model_sin1_doulespinbox = QtWidgets.QDoubleSpinBox(decimals=8)
        self.model_sin2_doulespinbox = QtWidgets.QDoubleSpinBox(decimals=8)
        self.model_sin3_doulespinbox = QtWidgets.QDoubleSpinBox(decimals=8)
        self.model_cos1_doulespinbox = QtWidgets.QDoubleSpinBox(decimals=8)
        self.model_cos2_doulespinbox = QtWidgets.QDoubleSpinBox(decimals=8)
        self.model_cos3_doulespinbox = QtWidgets.QDoubleSpinBox(decimals=8)
        self.model_apsid_coef_doulespinbox = QtWidgets.QDoubleSpinBox(decimals=8)
        self.model_ofset_doulespinbox = QtWidgets.QDoubleSpinBox(decimals=8)

        self.model_mag0_doulespinbox.setRange(-99, 99)
        self.model_sec_phase_doulespinbox.setRange(-99, 99)
        self.model_a_pri_doulespinbox.setRange(-99, 99)
        self.model_d_pri_doulespinbox.setRange(-99, 99)
        self.model_g_pri_doulespinbox.setRange(-99, 99)
        self.model_c_pri_doulespinbox.setRange(-99, 99)
        self.model_a_sec_doulespinbox.setRange(-99, 99)
        self.model_d_sec_doulespinbox.setRange(-99, 99)
        self.model_g_sec_doulespinbox.setRange(-99, 99)
        self.model_c_sec_doulespinbox.setRange(-99, 99)
        self.model_sin1_doulespinbox.setRange(-99, 99)
        self.model_sin2_doulespinbox.setRange(-99, 99)
        self.model_sin3_doulespinbox.setRange(-99, 99)
        self.model_cos1_doulespinbox.setRange(-99, 99)
        self.model_cos2_doulespinbox.setRange(-99, 99)
        self.model_cos3_doulespinbox.setRange(-99, 99)
        self.model_apsid_coef_doulespinbox.setRange(-99, 99)
        self.model_ofset_doulespinbox.setRange(-99, 99)

        model_part1_layout.addRow(QtWidgets.QLabel("mag0: "), self.model_mag0_doulespinbox)
        model_part1_layout.addRow(QtWidgets.QLabel("a_pri: "), self.model_a_pri_doulespinbox)
        model_part1_layout.addRow(QtWidgets.QLabel("d_pri: "), self.model_d_pri_doulespinbox)
        model_part1_layout.addRow(QtWidgets.QLabel("g_pri: "), self.model_g_pri_doulespinbox)
        model_part1_layout.addRow(QtWidgets.QLabel("c_pri: "), self.model_c_pri_doulespinbox)
        model_part1_layout.addRow(QtWidgets.QLabel("sin1: "), self.model_sin1_doulespinbox)
        model_part1_layout.addRow(QtWidgets.QLabel("sin2: "), self.model_sin2_doulespinbox)
        model_part1_layout.addRow(QtWidgets.QLabel("sin3: "), self.model_sin3_doulespinbox)
        model_part1_layout.addRow(QtWidgets.QLabel("coef.apsid: "), self.model_apsid_coef_doulespinbox)

        model_part2_layout.addRow(QtWidgets.QLabel("sec_phase: "), self.model_sec_phase_doulespinbox)
        model_part2_layout.addRow(QtWidgets.QLabel("a_sec: "), self.model_a_sec_doulespinbox)
        model_part2_layout.addRow(QtWidgets.QLabel("d_sec: "), self.model_d_sec_doulespinbox)
        model_part2_layout.addRow(QtWidgets.QLabel("g_sec: "), self.model_g_sec_doulespinbox)
        model_part2_layout.addRow(QtWidgets.QLabel("c_sec: "), self.model_c_sec_doulespinbox)
        model_part2_layout.addRow(QtWidgets.QLabel("cos1: "), self.model_cos1_doulespinbox)
        model_part2_layout.addRow(QtWidgets.QLabel("cos2: "), self.model_cos2_doulespinbox)
        model_part2_layout.addRow(QtWidgets.QLabel("cos3: "), self.model_cos3_doulespinbox)
        model_part2_layout.addRow(QtWidgets.QLabel("ofset: "), self.model_ofset_doulespinbox)

        # import
        self.import_star_button = QtWidgets.QPushButton("Import star")
        self.import_model_button = QtWidgets.QPushButton("Import model")
        self.import_pair_button = QtWidgets.QPushButton("Import pair")
        self.import_vsx_button = QtWidgets.QPushButton("Import VSX")
        self.import_asassn_button = QtWidgets.QPushButton("Import ASASSN")

        import_groupbox = QtWidgets.QGroupBox("Import from Silicups")
        import_layout = QtWidgets.QHBoxLayout()
        import_groupbox.setLayout(import_layout)
        import_layout.addWidget(self.import_star_button)
        import_layout.addWidget(self.import_pair_button)
        import_layout.addWidget(self.import_model_button)
        import_layout.addWidget(self.import_vsx_button)
        import_layout.addWidget(self.import_asassn_button)

        # save
        self.save_button = QtWidgets.QPushButton("Save changes")

        # notes
        notes_groupbox = QtWidgets.QGroupBox("Notes")
        notes_layout = QtWidgets.QVBoxLayout()
        self.notes1_textedit = QtWidgets.QTextEdit()
        self.notes2_textedit = QtWidgets.QTextEdit()
        self.notes3_textedit = QtWidgets.QTextEdit()
        self.notes1_textedit.setFixedHeight(self.note_widget_height)
        self.notes2_textedit.setFixedHeight(self.note_widget_height)
        self.notes3_textedit.setFixedHeight(self.note_widget_height)

        notes_groupbox.setLayout(notes_layout)
        notes_layout.addWidget(self.notes1_textedit)
        notes_layout.addWidget(self.notes2_textedit)
        notes_layout.addWidget(self.notes3_textedit)

        # button
        object_button_group_box = QtWidgets.QGroupBox("New / Edit")
        object_button_group_layout = QtWidgets.QHBoxLayout()
        object_button_group_box.setLayout(object_button_group_layout)
        self.new_object_checkbox = QtWidgets.QRadioButton("New Star")
        self.current_object_checkbox = QtWidgets.QRadioButton("Current Star")
        self.current_object_checkbox.setChecked(True)

        self.new_buttongroup = QtWidgets.QButtonGroup()
        self.new_buttongroup.addButton(self.new_object_checkbox)
        self.new_buttongroup.addButton(self.current_object_checkbox)

        object_button1_group_box = QtWidgets.QGroupBox("VAR/CMP")
        object_button1_group_layout = QtWidgets.QHBoxLayout()
        object_button1_group_box.setLayout(object_button1_group_layout)
        self.cmp_checkbox = QtWidgets.QRadioButton("CMP")
        self.var_checkbox = QtWidgets.QRadioButton("VAR")
        self.var_checkbox.setChecked(True)

        self.var_buttongroup = QtWidgets.QButtonGroup()
        self.var_buttongroup.addButton(self.cmp_checkbox)
        self.var_buttongroup.addButton(self.var_checkbox)

        object_button_group_layout.addWidget(self.new_object_checkbox)
        object_button_group_layout.addWidget(self.current_object_checkbox)
        object_button1_group_layout.addWidget(self.cmp_checkbox)
        object_button1_group_layout.addWidget(self.var_checkbox)

        main_layout.addWidget(self.pair_checkgroup, 0, 0, 1, 1)
        main_layout.addWidget(object_button_group_box, 0, 1, 1, 1)
        main_layout.addWidget(object_button1_group_box, 0, 2, 1, 1)
        main_layout.addWidget(import_groupbox, 0, 3, 1, 4)
        main_layout.addWidget(self.comp_checkgroup, 0, 7, 7, 1)
        main_layout.addWidget(star_groupbox, 1, 0, 8, 1)
        main_layout.addWidget(lightkurve_groupbox, 1, 1, 8, 1)
        main_layout.addWidget(model_groupbox, 1, 2, 6, 3)
        main_layout.addWidget(cross_groupbox, 7, 2, 2, 3)
        main_layout.addWidget(notes_groupbox, 1, 5, 8, 2)
        main_layout.addWidget(self.save_button, 7, 7, 2, 1)

    def setup(self):
        from step_application import root
        self.star_type_combobox.addItems(root.database.type_list)
        self.lightcurve_type_combobox.addItems(root.database.variability_type)
        self.step_main_form = root.step_main_form
        self.database = root.database
        self.object_import_window = root.object_import_window
        self.ucac4_window = root.ucac4_window
        self.star_ekvinokcium_combobox.addItems(self.database.possible_epoch)
        self.vsx_window = root.vsx_window
        self.asas_window = root.asas_window

        # connect
        self.new_object_checkbox.clicked.connect(self.new_button)
        self.current_object_checkbox.clicked.connect(self.new_button)
        self.cmp_checkbox.clicked.connect(self.cmp_button)
        self.var_checkbox.clicked.connect(self.cmp_button)
        self.pair_a_checkbox.clicked.connect(self.pair_was_changed)
        self.pair_b_checkbox.clicked.connect(self.pair_was_changed)
        self.pair_c_checkbox.clicked.connect(self.pair_was_changed)
        self.pair_d_checkbox.clicked.connect(self.pair_was_changed)
        self.pair_e_checkbox.clicked.connect(self.pair_was_changed)
        self.pair_f_checkbox.clicked.connect(self.pair_was_changed)
        self.import_model_button.clicked.connect(self.import_model)
        self.import_star_button.clicked.connect(self.import_star)
        self.star_name_editline.textChanged.connect(self.star_name_editline_changed)
        self.import_pair_button.clicked.connect(self.import_pair)
        self.lightcurve_type_button.clicked.connect(self.get_new_variability_type)
        self.save_button.clicked.connect(self.save_changes)
        self.import_vsx_button.clicked.connect(self.vsx_import)
        self.import_asassn_button.clicked.connect(self.asas_import)
        self.set_note_widget_height()

    def set_note_widget_height(self):
        self.note_widget_height = int(self.frameSize().height() / 5)
        self.notes1_textedit.setFixedHeight(self.note_widget_height)
        self.notes2_textedit.setFixedHeight(self.note_widget_height)
        self.notes3_textedit.setFixedHeight(self.note_widget_height)

    def resizeEvent(self, a0: QtGui.QResizeEvent):
        self.set_note_widget_height()

    def asas_import(self):
        self.asas_window.import_star()
        self.asas_window.show()

    def vsx_import(self):
        self.vsx_window.import_star()
        self.vsx_window.show()

    def pair_was_add(self):
        return self.__pair_was_add

    def change_pair_was_add(self, new):
        self.__pair_was_add = new

    def import_pair(self):
        if self.pair_a_checkbox.isEnabled() and self.var_checkbox.isChecked():
            if self.pair_b_checkbox.isEnabled():
                if self.pair_c_checkbox.isEnabled():
                    if self.pair_d_checkbox.isEnabled():
                        if self.pair_e_checkbox.isEnabled():
                            if self.pair_f_checkbox.isEnabled():
                                error_window = Popup("No pair is free", "All pairs are filled", "OK".split(","))
                                error_window.do()
                                self.change_pair_was_add(False)
                                return
                            else:
                                self.change_pair_was_add("F")
                                self.pair_f_checkbox.setEnabled(True)
                                self.pair_f_checkbox.setChecked(True)
                        else:
                            self.change_pair_was_add("E")
                            self.pair_e_checkbox.setEnabled(True)
                            self.pair_e_checkbox.setChecked(True)
                    else:
                        self.change_pair_was_add("D")
                        self.pair_d_checkbox.setEnabled(True)
                        self.pair_d_checkbox.setChecked(True)
                else:
                    self.change_pair_was_add("C")
                    self.pair_c_checkbox.setEnabled(True)
                    self.pair_c_checkbox.setChecked(True)
            else:
                self.change_pair_was_add("B")
                self.pair_b_checkbox.setEnabled(True)
                self.pair_b_checkbox.setChecked(True)
        else:
            error_window = Popup("Star is CMP", "Comparison star has no variability", "OK".split(","))
            error_window.do()
            return
        self.import_pair_button.setEnabled(False)
        self.object_import_window.import_pair_active_item(False)
        self.object_import_window.import_model_active_item(True)
        self.clear_variable()

        self.import_object()

    def star_name_editline_changed(self):
        if self.star_name_editline.text():
            self.import_star_button.setEnabled(False)
        else:
            self.import_star_button.setEnabled(True)

    def import_model(self, import_defined=""):
        if import_defined == "file":
            type_of_import_result = 1
        elif import_defined == "silicups":
            type_of_import_result = 0
        else:
            type_of_import_window = Popup("Import from", "Import from Silicups or saved model file?  ",
                                          buttons="Silicups,File with model,Exit".split(","))
            type_of_import_result = type_of_import_window.do()
        if type_of_import_result == 0:
            self.object_import_window.import_model_active_item(False)
            self.object_import_window.import_pair_active_item(False)
            self.import_object()
        elif type_of_import_result == 1:
            if os.path.exists(self.database.user.model_path()):
                path_to_file = self.database.user.model_path()
            else:
                path_to_file = os.path.join(os.getenv("APPDATA"), "Quadruples")
            path_to_model_file = QtWidgets.QFileDialog.getOpenFileName(caption="Select the file",
                                                                       directory=path_to_file, filter="*.txt")
            if path_to_model_file[0] == "":
                return
            self.database.user.change_model_path(path_to_model_file[0])
            with open(path_to_model_file[0], "r", encoding="utf-8") as f:
                first_row = f.readline().strip()
                second_row = f.readline().strip()
                if first_row == "SilicupsFitParameters" and second_row == "fit":
                    self.model_mag0_doulespinbox.setValue(0)
                    self.model_sec_phase_doulespinbox.setValue(0)
                    self.model_a_pri_doulespinbox.setValue(0)
                    self.model_d_pri_doulespinbox.setValue(0)
                    self.model_g_pri_doulespinbox.setValue(0)
                    self.model_c_pri_doulespinbox.setValue(0)
                    self.model_a_sec_doulespinbox.setValue(0)
                    self.model_d_sec_doulespinbox.setValue(0)
                    self.model_g_sec_doulespinbox.setValue(0)
                    self.model_c_sec_doulespinbox.setValue(0)
                    self.model_sin1_doulespinbox.setValue(0)
                    self.model_sin2_doulespinbox.setValue(0)
                    self.model_sin3_doulespinbox.setValue(0)
                    self.model_cos1_doulespinbox.setValue(0)
                    self.model_cos2_doulespinbox.setValue(0)
                    self.model_cos3_doulespinbox.setValue(0)
                    self.model_apsid_coef_doulespinbox.setValue(0)
                    self.model_ofset_doulespinbox.setValue(0)
                    for row in f.readlines():
                        clear_row = row.strip()
                        try:
                            if "mag0 =" in clear_row:
                                self.model_mag0_doulespinbox.setValue(float(clear_row[7: len(clear_row)]))
                            if "sec_phase =" in clear_row:
                                self.model_sec_phase_doulespinbox.setValue(float(clear_row[12: len(clear_row)]))
                            if "a_pri =" in clear_row:
                                self.model_a_pri_doulespinbox.setValue(float(clear_row[8: len(clear_row)]))
                            if "d_pri =" in clear_row:
                                self.model_d_pri_doulespinbox.setValue(float(clear_row[8: len(clear_row)]))
                            if "g_pri =" in clear_row:
                                self.model_g_pri_doulespinbox.setValue(float(clear_row[8: len(clear_row)]))
                            if "c_pri =" in clear_row:
                                self.model_c_pri_doulespinbox.setValue(float(clear_row[8: len(clear_row)]))
                            if "a_sec =" in clear_row:
                                self.model_a_sec_doulespinbox.setValue(float(clear_row[8: len(clear_row)]))
                            if "d_sec =" in clear_row:
                                self.model_d_sec_doulespinbox.setValue(float(clear_row[8: len(clear_row)]))
                            if "g_sec =" in clear_row:
                                self.model_g_sec_doulespinbox.setValue(float(clear_row[8: len(clear_row)]))
                            if "c_sec =" in clear_row:
                                self.model_c_sec_doulespinbox.setValue(float(clear_row[8: len(clear_row)]))
                            if "a_sin1" in clear_row:
                                self.model_sin1_doulespinbox.setValue(float(clear_row[9: len(clear_row)]))
                            if "a_sin2" in clear_row:
                                self.model_sin2_doulespinbox.setValue(float(clear_row[9: len(clear_row)]))
                            if "a_sin3" in clear_row:
                                self.model_sin3_doulespinbox.setValue(float(clear_row[9: len(clear_row)]))
                            if "a_cos1" in clear_row:
                                self.model_cos1_doulespinbox.setValue(float(clear_row[9: len(clear_row)]))
                            if "a_cos2" in clear_row:
                                self.model_cos2_doulespinbox.setValue(float(clear_row[9: len(clear_row)]))
                            if "a_cos3" in clear_row:
                                self.model_cos3_doulespinbox.setValue(float(clear_row[9: len(clear_row)]))
                            if "end_fit" in clear_row:
                                return
                        except:
                            mistake = Popup("Import Error", "Import fail", buttons="OK".split(","))
                            mistake.do()
        else:
            pass

    def import_star(self):
        self.object_import_window.import_pair_active_item(True)
        self.object_import_window.import_model_active_item(True)
        self.import_object()

    def import_object(self):
        if os.path.exists(self.database.user.silicups_file_path()):
            self.object_import_window.import_stars_from_silicups()
        else:
            self.object_import_window.set_input_file()
        self.object_import_window.show()

    def cmp_button(self):
        if self.step_main_form.star_id_editline.text():
            if self.cmp_checkbox.isChecked():
                if self.star_detail.variability() and self.current_object_checkbox.isChecked():
                    self.var_checkbox.setChecked(True)
                else:
                    self.clear_variable()
                    self.active_variability(False)
                    self.active_pairs(False)
            else:
                if not self.star_detail.variability() and self.current_object_checkbox.isChecked():
                    self.cmp_checkbox.setChecked(True)
                else:
                    self.active_variability(True)
                    self.active_pairs(False)
                    if self.current_object_checkbox.isChecked():
                        self.set_active_pair(self.star_detail.name())
                    else:
                        self.pair_a_checkbox.setEnabled(True)
        else:
            if self.cmp_checkbox.isChecked():
                self.setWindowIcon(QtGui.QIcon("star--pencil.png"))
                self.clear_variable()
                self.active_variability(False)
                self.active_pairs(False)
                if self.star_name_editline.text():
                    self.import_star_button.setEnabled(False)
                else:
                    self.import_star_button.setEnabled(True)
                self.import_model_button.setEnabled(False)
                self.import_pair_button.setEnabled(False)

            else:
                self.setWindowIcon(QtGui.QIcon("star--plus.png"))
                self.active_variability(True)
                if self.star_name_editline.text():
                    self.import_star_button.setEnabled(False)
                else:
                    self.import_star_button.setEnabled(True)
                self.import_model_button.setEnabled(True)
                self.import_pair_button.setEnabled(False)
                self.pair_a_checkbox.setEnabled(True)

    def new_button(self):
        if self.new_object_checkbox.isChecked():
            self.setWindowIcon(QtGui.QIcon("star--plus.png"))
            self.change_pair_was_add("")
            self.clear_star()
            self.clear_variable()
            self.active_pairs(False)
            self.pair_a_checkbox.setEnabled(True)
            self.pair_a_checkbox.setChecked(True)
            self.import_star_button.setEnabled(True)
            self.import_pair_button.setEnabled(False)
            self.import_model_button.setEnabled(True)
        else:
            self.setWindowIcon(QtGui.QIcon("star--pencil.png"))
            self.pair_a_checkbox.setChecked(True)
            if self.step_main_form.star_id_editline.text():
                self.fill_star()
                if self.star_detail.variability():
                    self.import_star_button.setEnabled(False)
                    self.import_pair_button.setEnabled(True)
                    self.import_model_button.setEnabled(True)
                    self.var_checkbox.setChecked(True)
                    self.active_variability(True)
                    self.active_pairs(False)
                    self.set_active_pair(self.star_detail.name())
                    pair = self.check_pair()
                    self.variable = self.database.variables.find_variable(self.star_detail.name(), pair)
                    self.fill_variable()
                else:
                    self.import_star_button.setEnabled(False)
                    self.import_pair_button.setEnabled(False)
                    self.import_model_button.setEnabled(False)
                    self.clear_variable()
                    self.active_variability(False)
                    self.cmp_checkbox.setChecked(True)
                    self.active_pairs(False)
            else:
                self.new_object_checkbox.setChecked(True)

    def check_pair(self):
        if self.pair_a_checkbox.isChecked():
            return "A"
        elif self.pair_b_checkbox.isChecked():
            return "B"
        elif self.pair_c_checkbox.isChecked():
            return "C"
        elif self.pair_d_checkbox.isChecked():
            return "D"
        elif self.pair_e_checkbox.isChecked():
            return "E"
        else:
            return "F"

    def active_pairs(self, active: bool):
        self.pair_a_checkbox.setEnabled(active)
        self.pair_b_checkbox.setEnabled(active)
        self.pair_c_checkbox.setEnabled(active)
        self.pair_d_checkbox.setEnabled(active)
        self.pair_e_checkbox.setEnabled(active)
        self.pair_f_checkbox.setEnabled(active)

    def set_active_pair(self, star_name):
        for variable in self.database.variables.variables:
            if star_name == variable.name():
                if variable.pair() == "A":
                    self.pair_a_checkbox.setEnabled(True)
                if variable.pair() == "B":
                    self.pair_b_checkbox.setEnabled(True)
                if variable.pair() == "C":
                    self.pair_c_checkbox.setEnabled(True)
                if variable.pair() == "D":
                    self.pair_d_checkbox.setEnabled(True)
                if variable.pair() == "P1":
                    self.pair_e_checkbox.setEnabled(True)
                if variable.pair() == "P2":
                    self.pair_f_checkbox.setEnabled(True)

    def fill_form(self):
        if self.step_main_form.star_id_editline.text():
            self.current_object_checkbox.setChecked(True)
            self.fill_star()
            self.active_pairs(False)
            if self.star_detail.variability():
                self.set_active_pair(self.star_detail.name())
                if self.step_main_form.pair_a_checkbox.isChecked():
                    self.pair_a_checkbox.setChecked(True)
                if self.step_main_form.pair_b_checkbox.isChecked():
                    self.pair_b_checkbox.setChecked(True)
                if self.step_main_form.pair_c_checkbox.isChecked():
                    self.pair_c_checkbox.setChecked(True)
                if self.step_main_form.pair_d_checkbox.isChecked():
                    self.pair_d_checkbox.setChecked(True)
                if self.step_main_form.pair_e_checkbox.isChecked():
                    self.pair_e_checkbox.setChecked(True)
                if self.step_main_form.pair_f_checkbox.isChecked():
                    self.pair_f_checkbox.setChecked(True)
                self.var_checkbox.setChecked(True)
                self.active_variability(True)
                self.variable = self.step_main_form.actual_variable
                self.fill_variable()
                self.import_star_button.setEnabled(False)
                self.import_model_button.setEnabled(True)
                self.import_pair_button.setEnabled(True)
            else:
                self.cmp_checkbox.setChecked(True)
                self.clear_variable()
                self.active_variability(False)
                self.import_star_button.setEnabled(False)
                self.import_model_button.setEnabled(False)
                self.import_pair_button.setEnabled(False)

        else:
            self.active_pairs(False)
            self.pair_a_checkbox.setEnabled(True)
            self.new_object_checkbox.setChecked(True)
            self.var_checkbox.setChecked(True)
            self.clear_star()
            self.clear_variable()
            self.active_variability(True)
            self.import_star_button.setEnabled(True)
            self.import_model_button.setEnabled(True)
            self.import_pair_button.setEnabled(False)

    def active_variability(self, active):
        self.lightcurve_period_editline.setEnabled(active)
        self.lightcurve_epoch_editline.setEnabled(active)
        self.lightcurve_type_combobox.setEnabled(active)
        self.lightcurve_amplitude_prim_doulespinbox.setEnabled(active)
        self.lightcurve_amplitude_sec_doulespinbox.setEnabled(active)
        self.lightcurve_d_big_prim_doulespinbox.setEnabled(active)
        self.lightcurve_d_big_sec_doulespinbox.setEnabled(active)
        self.lightcurve_d_prim_doulespinbox.setEnabled(active)
        self.lightcurve_d_sec_doulespinbox.setEnabled(active)
        self.model_mag0_doulespinbox.setEnabled(active)
        self.model_sec_phase_doulespinbox.setEnabled(active)
        self.model_a_pri_doulespinbox.setEnabled(active)
        self.model_d_pri_doulespinbox.setEnabled(active)
        self.model_g_pri_doulespinbox.setEnabled(active)
        self.model_c_pri_doulespinbox.setEnabled(active)
        self.model_a_sec_doulespinbox.setEnabled(active)
        self.model_d_sec_doulespinbox.setEnabled(active)
        self.model_g_sec_doulespinbox.setEnabled(active)
        self.model_c_sec_doulespinbox.setEnabled(active)
        self.model_sin1_doulespinbox.setEnabled(active)
        self.model_sin2_doulespinbox.setEnabled(active)
        self.model_sin3_doulespinbox.setEnabled(active)
        self.model_cos1_doulespinbox.setEnabled(active)
        self.model_cos2_doulespinbox.setEnabled(active)
        self.model_cos3_doulespinbox.setEnabled(active)
        self.model_apsid_coef_doulespinbox.setEnabled(active)
        self.model_ofset_doulespinbox.setEnabled(active)
        self.pair_comp0_checkbox.setEnabled(active)
        self.pair_comp1_checkbox.setEnabled(active)
        self.pair_comp2_checkbox.setEnabled(active)
        self.pair_comp3_checkbox.setEnabled(active)
        self.pair_comp4_checkbox.setEnabled(active)
        self.pair_comp5_checkbox.setEnabled(active)
        self.pair_comp6_checkbox.setEnabled(active)
        self.pair_comp7_checkbox.setEnabled(active)
        self.pair_comp8_checkbox.setEnabled(active)
        self.pair_comp9_checkbox.setEnabled(active)
        self.pair_chk1_checkbox.setEnabled(active)

    def fill_star(self):
        if self.step_main_form.objects_table.currentRow() > -1:
            self.star_detail = self.step_main_form.star_detail

        rektascenze = degrees(float(self.star_detail.coordinate().rektascenze()))/15
        h = floor(rektascenze)
        m = floor((rektascenze - h) * 60)
        s = round((rektascenze - h) * 3600 - m * 60, 3)

        deklinace = degrees(float(self.star_detail.coordinate().deklinace()))
        deklinace_abs = fabs(deklinace)
        st = floor(deklinace_abs)
        minuts = floor((deklinace_abs - st) * 60)
        sec = round((deklinace_abs - st) * 3600 - minuts * 60, 3)
        if deklinace < 0:
            self.dec_sign.setCurrentText("-")
        else:
            self.dec_sign.setCurrentText("+")

        self.star_id_editline.setText(str(self.star_detail.id()))
        self.star_name_editline.setText(self.star_detail.name())
        self.star_alternativ_name_editline.setText(self.star_detail.alt_name())
        self.star_ekvinokcium_combobox.setCurrentText(str(self.star_detail.coordinate().epoch()))
        self.star_constilation_combobox.setCurrentText(self.star_detail.constellation())
        self.star_rec_h_spinbox.setValue(h)
        self.star_rec_m_spinbox.setValue(m)
        self.star_rec_s_spinbox.setValue(s)
        self.star_dec_h_spinbox.setValue(st)
        self.star_dec_m_spinbox.setValue(minuts)
        self.star_dec_s_spinbox.setValue(sec)
        try:
            self.star_mag_doublespinbox.setValue(float(self.star_detail.mag()))
        except:
            self.star_mag_doublespinbox.clear()
        self.star_type_combobox.setCurrentText(self.database.type_dictionary[self.star_detail.type()])
        if self.star_detail.b_v() == " " or not self.star_detail.b_v():
            self.star_b_v_doublespinbox.clear()
        else:
            try:
                self.star_b_v_doublespinbox.setValue(float(self.star_detail.b_v()))
            except:
                self.star_b_v_doublespinbox.clear()
        if self.star_detail.j_k() == " " or not self.star_detail.j_k():
            self.star_j_k_doublespinbox.clear()
        else:
            try:
                self.star_j_k_doublespinbox.setValue(float(self.star_detail.j_k()))
            except:
                self.star_j_k_doublespinbox.clear()
        self.notes1_textedit.setText(self.star_detail.note1())
        self.notes2_textedit.setText(self.star_detail.note2())
        self.notes3_textedit.setText(self.star_detail.note3())
        self.pair_comp0_checkbox.setText(str(self.star_detail.comp0()))
        self.pair_comp1_checkbox.setText(str(self.star_detail.comp1()))
        self.pair_comp2_checkbox.setText(str(self.star_detail.comp2()))
        self.pair_comp3_checkbox.setText(str(self.star_detail.comp3()))
        self.pair_comp4_checkbox.setText(str(self.star_detail.comp4()))
        self.pair_comp5_checkbox.setText(str(self.star_detail.comp5()))
        self.pair_comp6_checkbox.setText(str(self.star_detail.comp6()))
        self.pair_comp7_checkbox.setText(str(self.star_detail.comp7()))
        self.pair_comp8_checkbox.setText(str(self.star_detail.comp8()))
        self.pair_comp9_checkbox.setText(str(self.star_detail.comp9()))
        self.pair_chk1_checkbox.setText(str(self.star_detail.chk1()))

    def fill_variable(self):
        self.lightcurve_period_editline.setText(str(self.variable.period()))
        self.lightcurve_epoch_editline.setText(str(self.variable.epoch()))
        self.lightcurve_type_combobox.setCurrentText(str(self.variable.variability_type()))
        self.lightcurve_amplitude_prim_doulespinbox.setValue(float(self.variable.amplitude_p()))
        self.lightcurve_amplitude_sec_doulespinbox.setValue(float(self.variable.amplitude_s()))
        self.lightcurve_d_big_prim_doulespinbox.setValue(float(self.variable.d_eclipse_prim()))
        self.lightcurve_d_big_sec_doulespinbox.setValue(float(self.variable.d_eclipse_sec()))
        self.lightcurve_d_prim_doulespinbox.setValue(float(self.variable.d_minimum_prim()))
        self.lightcurve_d_sec_doulespinbox.setValue(float(self.variable.d_minimum_sec()))
        self.model_mag0_doulespinbox.setValue(float(self.variable.mag0()))
        self.model_sec_phase_doulespinbox.setValue(float(self.variable.sec_phase()))
        self.model_a_pri_doulespinbox.setValue(float(self.variable.a_pri()))
        self.model_d_pri_doulespinbox.setValue(float(self.variable.d_pri()))
        self.model_g_pri_doulespinbox.setValue(float(self.variable.g_pri()))
        self.model_c_pri_doulespinbox.setValue(float(self.variable.c_pri()))
        self.model_a_sec_doulespinbox.setValue(float(self.variable.a_sec()))
        self.model_d_sec_doulespinbox.setValue(float(self.variable.d_sec()))
        self.model_g_sec_doulespinbox.setValue(float(self.variable.g_sec()))
        self.model_c_sec_doulespinbox.setValue(float(self.variable.c_sec()))
        self.model_sin1_doulespinbox.setValue(float(self.variable.a_sin1()))
        self.model_sin2_doulespinbox.setValue(float(self.variable.a_sin2()))
        self.model_sin3_doulespinbox.setValue(float(self.variable.a_sin3()))
        self.model_cos1_doulespinbox.setValue(float(self.variable.a_cos1()))
        self.model_cos2_doulespinbox.setValue(float(self.variable.a_cos2()))
        self.model_cos3_doulespinbox.setValue(float(self.variable.a_cos3()))
        self.model_apsid_coef_doulespinbox.setValue(float(self.variable.apsidal_movement_correction()))
        self.model_ofset_doulespinbox.setValue(float(self.variable.lc_offset()))

    def pair_was_changed(self):
        if self.current_object_checkbox.isChecked():
            if self.__pair_was_add:
                if self.__pair_was_add == "B" and not self.pair_b_checkbox.isChecked():
                    self.pair_b_checkbox.setEnabled(False)
                elif self.__pair_was_add == "C" and not self.pair_c_checkbox.isChecked():
                    self.pair_c_checkbox.setEnabled(False)
                elif self.__pair_was_add == "D" and not self.pair_d_checkbox.isChecked():
                    self.pair_d_checkbox.setEnabled(False)
                elif self.__pair_was_add == "E" and not self.pair_e_checkbox.isChecked():
                    self.pair_e_checkbox.setEnabled(False)
                elif self.__pair_was_add == "F" and not self.pair_f_checkbox.isChecked():
                    self.pair_f_checkbox.setEnabled(False)
                else:
                    self.import_pair_button.setEnabled(False)
                    return
                self.import_pair_button.setEnabled(True)
                self.change_pair_was_add("")
            pair = self.check_pair()
            self.variable = self.database.variables.find_variable(self.star_detail.name(), pair)
            self.fill_variable()

    def clear_star(self):
        self.star_id_editline.setText("")
        self.star_name_editline.setText("")
        self.star_alternativ_name_editline.setText("")
        self.star_ekvinokcium_combobox.setCurrentText("2000")
        self.star_constilation_combobox.setCurrentText("")
        self.dec_sign.setCurrentText("+")
        self.star_rec_h_spinbox.setValue(0)
        self.star_rec_m_spinbox.setValue(0)
        self.star_rec_s_spinbox.setValue(0)
        self.star_dec_h_spinbox.setValue(0)
        self.star_dec_m_spinbox.setValue(0)
        self.star_dec_s_spinbox.setValue(0)
        self.star_mag_doublespinbox.setValue(0)
        self.star_type_combobox.setCurrentText(self.database.type_dictionary[""])
        self.star_b_v_doublespinbox.setValue(0)
        self.star_j_k_doublespinbox.setValue(0)
        self.notes1_textedit.setText("")
        self.notes2_textedit.setText("")
        self.notes3_textedit.setText("")
        self.cross_type_label.setText("")
        self.cross_number_label.setText("")


        self.star_id_editline.clear()
        self.star_name_editline.clear()
        self.star_alternativ_name_editline.clear()
        self.star_ekvinokcium_combobox.setCurrentText("2000")
        self.star_constilation_combobox.setCurrentText("")
        self.star_rec_h_spinbox.clear()
        self.star_rec_m_spinbox.clear()
        self.star_rec_s_spinbox.clear()
        self.star_dec_h_spinbox.clear()
        self.star_dec_m_spinbox.clear()
        self.star_dec_s_spinbox.clear()
        self.star_mag_doublespinbox.clear()
        self.star_type_combobox.setCurrentText(self.database.type_dictionary[""])
        self.star_b_v_doublespinbox.clear()
        self.star_j_k_doublespinbox.clear()
        self.notes1_textedit.clear()
        self.notes2_textedit.clear()
        self.notes3_textedit.clear()
        self.cross_type_label.clear()
        self.cross_number_label.clear()

    def clear_variable(self):
        self.lightcurve_period_editline.setText("0")
        self.lightcurve_epoch_editline.setText("0")
        self.lightcurve_type_combobox.setCurrentText("")
        self.lightcurve_amplitude_prim_doulespinbox.setValue(0)
        self.lightcurve_amplitude_sec_doulespinbox.setValue(0)
        self.lightcurve_d_big_prim_doulespinbox.setValue(0)
        self.lightcurve_d_big_sec_doulespinbox.setValue(0)
        self.lightcurve_d_prim_doulespinbox.setValue(0)
        self.lightcurve_d_sec_doulespinbox.setValue(0)
        self.model_mag0_doulespinbox.setValue(0)
        self.model_sec_phase_doulespinbox.setValue(0)
        self.model_a_pri_doulespinbox.setValue(0)
        self.model_d_pri_doulespinbox.setValue(0)
        self.model_g_pri_doulespinbox.setValue(0)
        self.model_c_pri_doulespinbox.setValue(0)
        self.model_a_sec_doulespinbox.setValue(0)
        self.model_d_sec_doulespinbox.setValue(0)
        self.model_g_sec_doulespinbox.setValue(0)
        self.model_c_sec_doulespinbox.setValue(0)
        self.model_sin1_doulespinbox.setValue(0)
        self.model_sin2_doulespinbox.setValue(0)
        self.model_sin3_doulespinbox.setValue(0)
        self.model_cos1_doulespinbox.setValue(0)
        self.model_cos2_doulespinbox.setValue(0)
        self.model_cos3_doulespinbox.setValue(0)
        self.model_apsid_coef_doulespinbox.setValue(0)
        self.model_ofset_doulespinbox.setValue(0)
        if self.pair_was_add():
            return
        self.pair_comp0_checkbox.setText("0")
        self.pair_comp1_checkbox.setText("0")
        self.pair_comp2_checkbox.setText("0")
        self.pair_comp3_checkbox.setText("0")
        self.pair_comp4_checkbox.setText("0")
        self.pair_comp5_checkbox.setText("0")
        self.pair_comp6_checkbox.setText("0")
        self.pair_comp7_checkbox.setText("0")
        self.pair_comp8_checkbox.setText("0")
        self.pair_comp9_checkbox.setText("0")
        self.pair_chk1_checkbox.setText("0")

        self.lightcurve_period_editline.clear()
        self.lightcurve_epoch_editline.clear()
        self.lightcurve_type_combobox.setCurrentText("")
        self.lightcurve_amplitude_prim_doulespinbox.clear()
        self.lightcurve_amplitude_sec_doulespinbox.clear()
        self.lightcurve_d_big_prim_doulespinbox.clear()
        self.lightcurve_d_big_sec_doulespinbox.clear()
        self.lightcurve_d_prim_doulespinbox.clear()
        self.lightcurve_d_sec_doulespinbox.clear()
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
        self.model_ofset_doulespinbox.clear()
        if self.pair_was_add():
            return
        self.pair_comp0_checkbox.clear()
        self.pair_comp1_checkbox.clear()
        self.pair_comp2_checkbox.clear()
        self.pair_comp3_checkbox.clear()
        self.pair_comp4_checkbox.clear()
        self.pair_comp5_checkbox.clear()
        self.pair_comp6_checkbox.clear()
        self.pair_comp7_checkbox.clear()
        self.pair_comp8_checkbox.clear()
        self.pair_comp9_checkbox.clear()
        self.pair_chk1_checkbox.clear()

    def get_new_variability_type(self):
        new_var_type, ok = QtWidgets.QInputDialog.getText(self, 'New var.type', 'Enter new type of variability:')
        if ok and new_var_type not in self.database.variability_type:
            self.database.variability_type.append(new_var_type)
            self.lightcurve_type_combobox.addItem(new_var_type)
            self.lightcurve_type_combobox.setCurrentText(new_var_type)

    def save_changes(self):
        name = self.star_name_editline.text().strip().replace(",", "").replace(";", "")
        if not name:
            mistake("Name", "Name is empty")
            return
        if not check_input(name, special_characters=True, plus_minus=True, dot_sign=True):
            mistake("Name", "Forbidden characters")
            return
        alt_name = self.star_alternativ_name_editline.text().strip().replace(",", "").replace(";", "")
        if not check_input(alt_name, special_characters=True, plus_minus=True, dot_sign=True):
            mistake("Alt.name", "Forbidden characters")
            return

        constellation = self.star_constilation_combobox.currentText()
        h_rec = self.star_rec_h_spinbox.value()
        m_rec = self.star_rec_m_spinbox.value()
        s_rec = self.star_rec_s_spinbox.value()
        h_dec = self.star_dec_h_spinbox.value()
        m_dec = self.star_dec_m_spinbox.value()
        s_dec = self.star_dec_s_spinbox.value()
        rektascenze = radians(h_rec*15 + m_rec / 4 + s_rec / 240)
        if self.dec_sign.currentText() == "-":
            sign = True
        else:
            sign = False
        declination = radians(h_dec + m_dec / 60 + s_dec / 3600)
        if sign:
            declination = - declination
        coor_epoch = self.star_ekvinokcium_combobox.currentText()
        coor = Coordinate(rektascenze, declination, epoch=coor_epoch)
        if constellation == "":
            constellation = Coordinate(rektascenze, declination).get_const()
        star_type = list(self.database.type_dictionary.keys())[self.star_type_combobox.currentIndex()]
        magnitude = self.star_mag_doublespinbox.value()
        b_v = str(self.star_b_v_doublespinbox.value())
        j_k = str(self.star_j_k_doublespinbox.value())
        if self.cross_type_label.text() == "UCAC4":
            ucac4 = self.cross_number_label.text()
            catalogue = "UCAC4"
            catalogue_id = ucac4
            usno = ""
        elif self.cross_type_label.text() == "USNO-B1.0":
            ucac4 = ""
            usno = self.cross_number_label.text()
            catalogue = "USNO-B1.0"
            catalogue_id = usno
        else:
            ucac4 = ""
            usno = ""
            catalogue = ""
            catalogue_id = ""
        note1 = self.notes1_textedit.toPlainText().replace(";", " ").replace("\n", " ")
        note2 = self.notes2_textedit.toPlainText().replace(";", " ").replace("\n", " ")
        note3 = self.notes3_textedit.toPlainText().replace(";", " ").replace("\n", " ")
        if self.new_object_checkbox.isChecked():
            near_star_list = self.database.stars.already_exist(name, rektascenze, declination, catalogue=catalogue,
                                                               catalogue_id=catalogue_id)
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
        if self.cmp_checkbox.isChecked():
            if self.new_object_checkbox.isChecked():
                new_cmp = Star(str(self.database.next_star()), name, alt_name, coor, magnitude, constellation, "", "CMP",
                               note1, note2, note3, b_v, j_k, ucac4, usno, "", "", "", "", 0, 0, 0, 0, 0, 0, 0, 0, 0,
                               0, 0, "", "", "", "", "",  variability=False)
                self.database.stars.add_star(new_cmp)
                self.database.increase_next_star()
            else:
                star_id = self.star_id_editline.text()
                for star in self.database.stars.stars:
                    if str(star.id()) == star_id:
                        if not star.variability():
                            star.change_name(name)
                            star.change_alt_name(alt_name)
                            star.change_coordinate(coor)
                            star.change_mag(magnitude)
                            star.change_constellation(constellation)
                            star.change_type("CMP")
                            star.change_note1(note1)
                            star.change_note2(note2)
                            star.change_note3(note3)
                            star.change_b_v(b_v)
                            star.change_j_k(j_k)
                            if ucac4:
                                star.change_ucac4(ucac4)
                            if usno:
                                star.change_usnob1(usno)
                        else:
                            mistake("Input error", "It is not CMP but VAR, I can´t save it")
                            return
        else:
            try:
                comp0 = int(self.pair_comp0_checkbox.text().replace(" ", ""))
            except:
                comp0 = 0
            if not self.database.stars.comperison_star_exist(comp0) and comp0:
                mistake("CMP error", "Comperison star CMP0 does not exist")
                comp0 = 0
            try:
                comp1 = int(self.pair_comp1_checkbox.text().replace(" ", ""))
            except:
                comp1 = 0
            if not self.database.stars.comperison_star_exist(comp1) and comp1:
                mistake("CMP error", "Comperison star CMP1 does not exist")
                comp1 = 0
            try:
                comp2 = int(self.pair_comp2_checkbox.text().replace(" ", ""))
            except:
                comp2 = 0
            if not self.database.stars.comperison_star_exist(comp2) and comp2:
                mistake("CMP error", "Comperison star CMP2 does not exist")
                comp2 = 0
            try:
                comp3 = int(self.pair_comp3_checkbox.text().replace(" ", ""))
            except:
                comp3 = 0
            if not self.database.stars.comperison_star_exist(comp3) and comp3:
                mistake("CMP error", "Comperison star CMP3 does not exist")
                comp3 = 0
            try:
                comp4 = int(self.pair_comp4_checkbox.text().replace(" ", ""))
            except:
                comp4 = 0
            if not self.database.stars.comperison_star_exist(comp4) and comp4:
                mistake("CMP error", "Comperison star CMP4 does not exist")
                comp4 = 0
            try:
                comp5 = int(self.pair_comp5_checkbox.text().replace(" ", ""))
            except:
                comp5 = 0
            if not self.database.stars.comperison_star_exist(comp5) and comp5:
                mistake("CMP error", "Comperison star CMP5 does not exist")
                comp5 = 0
            try:
                comp6 = int(self.pair_comp6_checkbox.text().replace(" ", ""))
            except:
                comp6 = 0
            if not self.database.stars.comperison_star_exist(comp6) and comp6:
                mistake("CMP error", "Comperison star CMP6 does not exist")
                comp6 = 0
            try:
                comp7 = int(self.pair_comp7_checkbox.text().replace(" ", ""))
            except:
                comp7 = 0
            if not self.database.stars.comperison_star_exist(comp7) and comp7:
                mistake("CMP error", "Comperison star CMP7 does not exist")
                comp7 = 0
            try:
                comp8 = int(self.pair_comp8_checkbox.text().replace(" ", ""))
            except:
                comp8 = 0
            if not self.database.stars.comperison_star_exist(comp8) and comp8:
                mistake("CMP error", "Comperison star CMP8 does not exist")
                comp8 = 0
            try:
                comp9 = int(self.pair_comp9_checkbox.text().replace(" ", ""))
            except:
                comp9 = 0
            if not self.database.stars.comperison_star_exist(comp9) and comp9:
                mistake("CMP error", "Comperison star CMP9 does not exist")
                comp9 = 0
            try:
                chk1 = int(self.pair_chk1_checkbox.text().replace(" ", ""))
            except:
                chk1 = 0
            if not self.database.stars.comperison_star_exist(chk1) and chk1:
                mistake("CMP error", "Comperison star CHK1 does not exist")
                chk1 = 0
            try:
                period = float(self.lightcurve_period_editline.text())
            except:
                mistake("Period error", "The period is a necessary input, it must be a number")
                return
            try:
                epoch_0 = float(self.lightcurve_epoch_editline.text())
            except:
                mistake("Epoch error", "The epoch zero is a necessary input, it must be a number")
                return
            variability_type = self.lightcurve_type_combobox.currentText()
            amplitude_prim = self.lightcurve_amplitude_prim_doulespinbox.value()
            amplitude_sec = self.lightcurve_amplitude_sec_doulespinbox.value()
            d_big_prim = self.lightcurve_d_big_prim_doulespinbox.value()
            d_big_sec = self.lightcurve_d_big_sec_doulespinbox.value()
            d_min_prim = self.lightcurve_d_prim_doulespinbox.value()
            d_min_sec = self.lightcurve_d_sec_doulespinbox.value()
            mag0 = self.model_mag0_doulespinbox.value()
            a_pri = self.model_a_pri_doulespinbox.value()
            d_pri = self.model_d_pri_doulespinbox.value()
            g_pri = self.model_g_pri_doulespinbox.value()
            c_pri = self.model_c_pri_doulespinbox.value()
            sin1 = self.model_sin1_doulespinbox.value()
            sin2 = self.model_sin2_doulespinbox.value()
            sin3 = self.model_sin3_doulespinbox.value()
            apsid_coefficient = self.model_apsid_coef_doulespinbox.value()
            sec_phase = self.model_sec_phase_doulespinbox.value()
            a_sec = self.model_a_sec_doulespinbox.value()
            d_sec = self.model_d_sec_doulespinbox.value()
            g_sec = self.model_g_sec_doulespinbox.value()
            c_sec = self.model_c_sec_doulespinbox.value()
            cos1 = self.model_cos1_doulespinbox.value()
            cos2 = self.model_cos2_doulespinbox.value()
            cos3 = self.model_cos3_doulespinbox.value()
            ofset = self.model_ofset_doulespinbox.value()
            if self.new_object_checkbox.isChecked():
                user_list = self.database.user.name()
                place_list = self.database.place.name
                instrument_list = self.database.instrument.id
                new_cmp = Star(str(self.database.next_star()), name, alt_name, coor, magnitude, constellation, "", star_type,
                               note1, note2, note3, b_v, j_k, ucac4, usno, "", "", "", "", comp0, comp1, comp2, comp3,
                               comp4, comp5, comp6, comp7, comp8, comp9, chk1, "", "", "", "", "", user_list=user_list,
                               place_list=place_list, instrument_list=instrument_list, variability=True)
                self.database.stars.add_star(new_cmp)
                new_variable = VariableStar(name, "A", variability_type, period, epoch_0, amplitude_prim, amplitude_sec,
                                            d_big_prim, d_big_sec, d_min_prim, d_min_sec, mag0, a_pri, d_pri, g_pri,
                                            c_pri, sin1, sin2, sin3, apsid_coefficient, sec_phase, a_sec, d_sec, g_sec,
                                            c_sec, cos1, cos2, cos3, ofset, 1)
                self.database.variables.add_variable(new_variable)
                self.database.increase_next_star()
            else:
                if self.pair_a_checkbox.isChecked():
                    pair = "A"
                else:
                    if self.pair_b_checkbox.isChecked():
                        pair = "B"
                    else:
                        if self.pair_c_checkbox.isChecked():
                            pair = "C"
                        else:
                            if self.pair_d_checkbox.isChecked():
                                pair = "D"
                            else:
                                if self.pair_e_checkbox.isChecked():
                                    pair = "E"
                                else:
                                    pair = "F"
                star_id = self.star_id_editline.text()
                for star in self.database.stars.stars:
                    a = str(star.id())
                    if str(star.id()) == star_id:
                        if star.variability():
                            if star.name() != name:
                                a = Popup("Name was changed",
                                          "The name of star was changed, you really want to continue?",
                                          buttons="OK, Exit".split(","))
                                if a.do() == 1:
                                    return
                            star.change_alt_name(alt_name)
                            star.change_coordinate(coor)
                            star.change_mag(magnitude)
                            star.change_constellation(constellation)
                            star.change_type(star_type)
                            star.change_note1(note1)
                            star.change_note2(note2)
                            star.change_note3(note3)
                            star.change_b_v(b_v)
                            star.change_j_k(j_k)
                            if ucac4:
                                star.change_ucac4(ucac4)
                            if usno:
                                star.change_usnob1(usno)
                            star.change_comp0(comp0)
                            star.change_comp1(comp1)
                            star.change_comp2(comp2)
                            star.change_comp3(comp3)
                            star.change_comp4(comp4)
                            star.change_comp5(comp5)
                            star.change_comp6(comp6)
                            star.change_comp7(comp7)
                            star.change_comp8(comp8)
                            star.change_comp9(comp9)
                            star.change_chk1(chk1)
                            if self.__pair_was_add:
                                new_variable = VariableStar(name, pair, variability_type, period, epoch_0,
                                                            amplitude_prim, amplitude_sec, d_big_prim, d_big_sec,
                                                            d_min_prim, d_min_sec, mag0, a_pri, d_pri, g_pri, c_pri,
                                                            sin1, sin2, sin3, apsid_coefficient, sec_phase, a_sec,
                                                            d_sec, g_sec, c_sec, cos1, cos2, cos3, ofset, 1)
                                self.database.variables.add_variable(new_variable)
                            else:
                                for variable in self.database.variables.variables:
                                    if variable.name() == star.name():
                                        self.variable.change_name(name)
                                        if variable.pair() == pair:
                                            self.variable.change_name(name)
                                            self.variable.change_variability_type(variability_type)
                                            self.variable.change_period(period)
                                            self.variable.change_epoch(epoch_0)
                                            self.variable.change_amplitude_p(amplitude_prim)
                                            self.variable.change_amplitude_s(amplitude_sec)
                                            self.variable.change_d_eclipse_prim(d_big_prim)
                                            self.variable.change_d_eclipse_sec(d_big_sec)
                                            self.variable.change_d_minimum_prim(d_min_prim)
                                            self.variable.change_d_minimum_sec(d_min_sec)
                                            self.variable.change_mag0(mag0)
                                            self.variable.change_a_pri(a_pri)
                                            self.variable.change_d_pri(d_pri)
                                            self.variable.change_g_pri(g_pri)
                                            self.variable.change_c_pri(c_pri)
                                            self.variable.change_a_sin1(sin1)
                                            self.variable.change_a_sin2(sin2)
                                            self.variable.change_a_sin3(sin3)
                                            self.variable.change_apsidal_movement_correction(apsid_coefficient)
                                            self.variable.change_sec_phase(sec_phase)
                                            self.variable.change_a_sec(a_sec)
                                            self.variable.change_d_sec(d_sec)
                                            self.variable.change_g_sec(g_sec)
                                            self.variable.change_c_sec(c_sec)
                                            self.variable.change_a_cos1(cos1)
                                            self.variable.change_a_cos2(cos2)
                                            self.variable.change_a_cos3(cos3)
                                            self.variable.change_lc_offset(ofset)
                            star.change_name(name)
                        else:
                            mistake("Input error", "It is not VAR but CMP, I can´t save it")
                            return
        self.step_main_form.fill_table()
        table_item_find = False
        for i, star in enumerate(self.step_main_form.filtered_stars.stars):
            if star.name() == name:
                table_item_find = True
                self.step_main_form.objects_table.setCurrentCell(i, 0)
        if not table_item_find:
            self.step_main_form.objects_table.setCurrentCell(0, 0)
        self.step_main_form.fill_object()
        self.step_main_form.fill_comp()
        self.close()
