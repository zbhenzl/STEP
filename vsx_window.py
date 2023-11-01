from PyQt5 import QtWidgets, QtCore, QtGui
from coordinate import *
from astroquery.vizier import Vizier
from astropy.coordinates import Angle
import astropy.coordinates as coord
import astropy.units as u
from import_star import mistake


class VSXWindow(QtWidgets.QWidget):

    def __init__(self, *args,**kvargs):
        super(VSXWindow, self).__init__(*args, **kvargs)

        self.star = []
        self.is_it_import = False
        self.setWindowTitle("VSX Catalogue Information")
        main_layout = QtWidgets.QVBoxLayout()
        self.setLayout(main_layout)
        main_layout.setSpacing(10)


        self.ucac4_checkbox = QtWidgets.QCheckBox("VSX identifier:")
        self.ucac4_combobox = QtWidgets.QComboBox()

        header_layout = QtWidgets.QHBoxLayout()
        header_layout.addWidget(self.ucac4_checkbox)
        header_layout.addWidget(self.ucac4_combobox)

        self.set_cross_id_button = QtWidgets.QPushButton("Choose the correct cross identification")
        delta_r_label = QtWidgets.QLabel("Radius:")
        self.raj2000_checkbox = QtWidgets.QCheckBox("RA eq.2000:")
        self.dej2000_checkbox = QtWidgets.QCheckBox("DE eq.2000:")
        oid_label = QtWidgets.QLabel("Internal identifier:")
        n_oid_label = QtWidgets.QLabel("indicates bibliography:")
        v_label = QtWidgets.QLabel("Variability flag:")
        self.type_checkbox = QtWidgets.QCheckBox("Variability type:")
        l_max_label =QtWidgets.QLabel("Limit flag on max:")
        self.max_checkbox = QtWidgets.QCheckBox(" Magnitude at maximum:")
        u_max_label =QtWidgets.QLabel("Uncertainty flag on max:")
        n_max_label = QtWidgets.QLabel("Passband on max magnitude:")
        f_min_label = QtWidgets.QLabel("Flag to indicate an amplitude:")
        l_min_label = QtWidgets.QLabel("Limit flag on min:")
        self.min_checkbox = QtWidgets.QCheckBox("Magnitude at minimum")
        u_min_label = QtWidgets.QLabel("Uncertainty flag on min:")
        n_min_label = QtWidgets.QLabel("Passband on min magnitude:")
        self.epoch_checkbox = QtWidgets.QCheckBox("Epoch of max.or min.(HJD):")
        u_epoch_label = QtWidgets.QLabel("Uncertainty flag on epoch:")
        l_period_label = QtWidgets.QLabel("Limit flag on period:")
        self.period_checkbox = QtWidgets.QCheckBox("Period in days:")
        u_period_label = QtWidgets.QLabel("Uncertainty flag on Period:")
        sp_label = QtWidgets.QLabel("Spectral type:")

        self.delta_r_label1 = QtWidgets.QLabel("")
        self.raj2000_editline = QtWidgets.QLineEdit("")
        self.dej2000_editline = QtWidgets.QLineEdit("")
        self.oid_label1 = QtWidgets.QLabel("")
        self.n_oid_label1 = QtWidgets.QLabel("")
        self.v_label1 = QtWidgets.QLabel("")
        self.type_editline = QtWidgets.QLineEdit("")
        self.l_max_label1 =QtWidgets.QLabel("")
        self.max_editline = QtWidgets.QLineEdit("")
        self.u_max_label1 =QtWidgets.QLabel("")
        self.n_max_label1 = QtWidgets.QLabel("")
        self.f_min_label1 = QtWidgets.QLabel("")
        self.l_min_label1 = QtWidgets.QLabel("")
        self.min_editline = QtWidgets.QLineEdit("")

        self.u_min_label1 = QtWidgets.QLabel("")
        self.n_min_label1 = QtWidgets.QLabel("")
        self.epoch_editline = QtWidgets.QLineEdit("")
        self.u_epoch_label1 = QtWidgets.QLabel("")
        self.l_period_label1 = QtWidgets.QLabel("")
        self.period_editline = QtWidgets.QLineEdit("")
        self.u_period_label1 = QtWidgets.QLabel("")
        self.sp_label1 = QtWidgets.QLabel("")

        self.info_groupbox = QtWidgets.QGroupBox("VSX information")
        info_layout = QtWidgets.QFormLayout()
        self.info_groupbox.setLayout(info_layout)

        info_layout.addRow(delta_r_label, self.delta_r_label1)
        info_layout.addRow(self.raj2000_checkbox, self.raj2000_editline)
        info_layout.addRow(self.dej2000_checkbox, self.dej2000_editline)
        info_layout.addRow(oid_label, self.oid_label1)
        info_layout.addRow(n_oid_label, self.n_oid_label1)
        info_layout.addRow(v_label, self.v_label1)
        info_layout.addRow(self.type_checkbox, self.type_editline)
        info_layout.addRow(l_max_label, self.l_max_label1)
        info_layout.addRow(self.max_checkbox, self.max_editline)
        info_layout.addRow(u_max_label, self.u_max_label1)
        info_layout.addRow(n_max_label, self.n_max_label1)
        info_layout.addRow(f_min_label, self.f_min_label1)
        info_layout.addRow(l_min_label, self.l_min_label1)
        info_layout.addRow(self.min_checkbox, self.min_editline)
        info_layout.addRow(u_min_label, self.u_min_label1)
        info_layout.addRow(n_min_label, self.n_min_label1)
        info_layout.addRow(self.epoch_checkbox, self.epoch_editline)
        info_layout.addRow(u_epoch_label, self.u_epoch_label1)
        info_layout.addRow(l_period_label, self.l_period_label1)
        info_layout.addRow(self.period_checkbox, self.period_editline)
        info_layout.addRow(u_period_label, self.u_period_label1)
        info_layout.addRow(sp_label, self.sp_label1)

        self.import_groupbox = QtWidgets.QGroupBox("Import information - Input coordinates")
        import_layout = QtWidgets.QGridLayout()
        self.import_groupbox.setLayout(import_layout)

        self.sign_combobox = QtWidgets.QComboBox()
        self.sign_combobox.addItems(["+", "-"])

        rec_h_label = QtWidgets.QLabel("h")
        rec_h_label.setFixedWidth(5)
        self.rec_h_spinbox = QtWidgets.QSpinBox()
        self.rec_h_spinbox.setRange(0, 23)

        rec_m_label = QtWidgets.QLabel("m")
        rec_m_label.setFixedWidth(5)
        self.rec_m_spinbox = QtWidgets.QSpinBox()
        self.rec_m_spinbox.setRange(0, 59)

        rec_s_label = QtWidgets.QLabel("s   ")
        rec_s_label.setFixedWidth(5)
        self.rec_s_spinbox = QtWidgets.QDoubleSpinBox()
        self.rec_s_spinbox.setRange(0, 59.99)

        dec_h_label = QtWidgets.QLabel("°")
        self.dec_h_spinbox = QtWidgets.QSpinBox()
        self.dec_h_spinbox.setRange(-89, 89)

        dec_m_label = QtWidgets.QLabel("m")
        self.dec_m_spinbox = QtWidgets.QSpinBox()
        self.dec_m_spinbox.setRange(0, 59)

        dec_s_label = QtWidgets.QLabel("s")
        self.dec_s_spinbox = QtWidgets.QDoubleSpinBox()
        self.dec_s_spinbox.setRange(0, 59.99)

        self.check_star_pushbutton = QtWidgets.QPushButton("Check for stars")
        aperture_label = QtWidgets.QLabel("Radius(m)")
        self.aperture_spinbox = QtWidgets.QSpinBox()
        self.aperture_spinbox.setRange(0, 99)


        import_layout.addWidget(self.rec_h_spinbox, 0, 0)
        import_layout.addWidget(rec_h_label, 0, 1)
        import_layout.addWidget(self.rec_m_spinbox, 0, 2)
        import_layout.addWidget(rec_m_label, 0, 3)
        import_layout.addWidget(self.rec_s_spinbox, 0, 4)
        import_layout.addWidget(rec_s_label, 0, 5)


        import_layout.addWidget(self.sign_combobox, 0, 6)
        import_layout.addWidget(self.dec_h_spinbox, 0, 7)
        import_layout.addWidget(dec_h_label, 0, 8)
        import_layout.addWidget(self.dec_m_spinbox, 0, 9)
        import_layout.addWidget(dec_m_label, 0, 10)
        import_layout.addWidget(self.dec_s_spinbox, 0, 11)
        import_layout.addWidget(dec_s_label, 0, 12)

        import_layout.addWidget(self.check_star_pushbutton, 1, 0, 1, 5)
        import_layout.addWidget(aperture_label, 1, 7, 1, 4)
        import_layout.addWidget(self.aperture_spinbox, 1, 11, 1, 2)

        main_layout.addWidget(self.import_groupbox)
        main_layout.addLayout(header_layout)
        main_layout.addWidget(self.set_cross_id_button)
        main_layout.addWidget(self.info_groupbox)

        self.raj2000_editline.setReadOnly(True)
        self.dej2000_editline.setReadOnly(True)
        self.type_editline.setReadOnly(True)
        self.max_editline.setReadOnly(True)
        self.min_editline.setReadOnly(True)
        self.period_editline.setReadOnly(True)
        self.epoch_editline.setReadOnly(True)

        self.import_groupbox.setVisible(False)

    def setup(self):
        from step_application import root
        self.step_main_form = root.step_main_form
        self.ucac4_combobox.currentTextChanged.connect(self.ucac_changed)
        self.set_cross_id_button.clicked.connect(self.set_cross_id)
        self.object_edit_window = root.object_edit_window
        self.check_star_pushbutton.clicked.connect(self.check_star)

    def check_star(self):
        self.info_groupbox.setVisible(True)
        self.set_cross_id_button.setEnabled(True)
        rec_h = self.rec_h_spinbox.value()
        rec_m = self.rec_m_spinbox.value()
        rec_s = self.rec_s_spinbox.value()
        dec_h = self.dec_h_spinbox.value()
        dec_m = self.dec_m_spinbox.value()
        dec_s = self.dec_s_spinbox.value()
        aperture = str(self.aperture_spinbox.value() * 60) + "s"
        rec = rec_h * 15 + rec_m / 4 + rec_s / 240
        dec = dec_h + dec_m / 60 + dec_s / 3600
        if self.sign_combobox.currentIndex() == 1:
            dec = -dec
        coor = Coordinate(radians(rec), radians(dec))
        self.download_data_coor(coor, radius=aperture)

    def import_star(self):
        self.close()
        self.import_groupbox.setVisible(True)
        self.info_groupbox.setVisible(False)
        self.set_cross_id_button.setEnabled(False)
        self.aperture_spinbox.setValue(10)
        self.set_cross_id_button.setText("Import star")
        self.ucac4_combobox.clear()
        self.sign_combobox.setCurrentText(self.object_edit_window.dec_sign.currentText())
        self.rec_h_spinbox.setValue(self.object_edit_window.star_rec_h_spinbox.value())
        self.rec_m_spinbox.setValue(self.object_edit_window.star_rec_m_spinbox.value())
        self.rec_s_spinbox.setValue(self.object_edit_window.star_rec_s_spinbox.value())
        self.dec_h_spinbox.setValue(self.object_edit_window.star_dec_h_spinbox.value())
        self.dec_m_spinbox.setValue(self.object_edit_window.star_dec_m_spinbox.value())
        self.dec_s_spinbox.setValue(self.object_edit_window.star_dec_s_spinbox.value())
        self.is_it_import = True

    def looking_for_cross_id(self):
        self.import_groupbox.setVisible(False)
        self.info_groupbox.setVisible(True)
        self.set_cross_id_button.setEnabled(True)
        self.set_cross_id_button.setText("Choose the correct cross identification")
        self. is_it_import = False

    def download_data_id(self, cross_id: str):
        self.star.clear()
        agn = Vizier(catalog="B/vsx", columns=["*", "Epoch", "u_Epoch"]).query_constraints(Name=cross_id)[0]
        for x in agn:
            oid = x["OID"]
            noid = x["n_OID"]
            id_star = x["Name"]
            rec_star = x["RAJ2000"]
            dec_star = x["DEJ2000"]
            rec_txt = coordinate_to_text(radians(float(rec_star)), coordinate_format="hours", delimiters=("h ", "m ", 's'),
                                         decimal_numbers=3)
            dec_txt = coordinate_to_text(radians(float(dec_star)), coordinate_format="degree", delimiters=("° ", "m ", 's'),
                                         decimal_numbers=3)
            v = x["V"]
            type_var = x["Type"]
            lmax = x["l_max"]
            max_mag = x["max"]
            umax = x["u_max"]
            nmax = x["n_max"]
            fmin = x["f_min"]
            lmin = x["l_min"]
            min_mag = x["min"]
            nmin = x["n_min"]
            lperiod = x["l_Period"]
            period = x["Period"]
            uperiod = x["u_Period"]
            sp = x["Sp"]
            epoch = x["_tab1_15"]
            uepoch = x["u_Epoch"]

            self.star = [["", oid, noid, id_star, rec_txt, dec_txt, v, type_var, lmax, max_mag, umax, nmax, fmin, lmin,
                          min_mag, nmin, lperiod, period, uperiod, sp, epoch, uepoch, rec_star, dec_star]]
            self.ucac4_combobox.clear()
            self.ucac4_combobox.addItem(str(id_star))
            self.set_cross_id_button.setEnabled(False)
            self.fill_star(0)

    def download_data_coor(self, coor: Coordinate, radius="10s"):
        self.star.clear()
        rec = degrees(coor.rektascenze())
        dec = degrees(coor.deklinace())
        v = Vizier(columns=["*", "+_r", "Epoch", "u_Epoch"], catalog="B/vsx")
        a = coord.SkyCoord(ra=rec, dec=dec, unit=(u.deg, u.deg))
        result = v.query_region(a, radius=radius)
        name_list = []
        for y in result:
            for x in y:
                r = x["_r"]
                oid = x["OID"]
                noid = x["n_OID"]
                id_star = x["Name"]
                rec_star = x["RAJ2000"]
                dec_star = x["DEJ2000"]
                rec_txt = coordinate_to_text(radians(float(rec_star)), coordinate_format="hours",
                                             delimiters=("h ", "m ", 's'),
                                             decimal_numbers=3)
                dec_txt = coordinate_to_text(radians(float(dec_star)), coordinate_format="degree",
                                             delimiters=("° ", "m ", 's'),
                                             decimal_numbers=3)
                v = x["V"]
                type_var = x["Type"]
                lmax = x["l_max"]
                max_mag = x["max"]
                umax = x["u_max"]
                nmax = x["n_max"]
                fmin = x["f_min"]
                lmin = x["l_min"]
                min_mag = x["min"]
                nmin = x["n_min"]
                lperiod = x["l_Period"]
                period = x["Period"]
                uperiod = x["u_Period"]
                sp = x["Sp"]
                epoch = x["_tab1_15"]
                uepoch = x["u_Epoch"]

                self.star.append([r, oid, noid, id_star, rec_txt, dec_txt, v, type_var, lmax, max_mag, umax, nmax, fmin,
                                 lmin, min_mag, nmin, lperiod, period, uperiod, sp, epoch, uepoch, rec_star, dec_star])
                name_list.append(str(id_star))
        self.ucac4_combobox.clear()
        self.ucac4_combobox.addItems(name_list)
        self.set_cross_id_button.setEnabled(True)
        if name_list:
            self.fill_star(0)
            if self.is_it_import:
                self.check_item(True)
            else:
                self.check_item(False)
        else:
            self.clear_window()
            self.check_item(False)

    def fill_star(self, index):
        self.delta_r_label1.setText(str(self.star[index][0]))
        self.raj2000_editline.setText(str(self.star[index][4]))
        self.dej2000_editline.setText(str(self.star[index][5]))
        self.oid_label1.setText(str(self.star[index][1]))
        self.n_oid_label1.setText(str(self.star[index][2]))
        self.v_label1.setText(str(self.star[index][6]))
        self.type_editline.setText(str(self.star[index][7]))
        self.l_max_label1.setText(str(self.star[index][8]))
        self.max_editline.setText(str(self.star[index][9]))
        self.u_max_label1.setText(str(self.star[index][10]))
        self.n_max_label1.setText(str(self.star[index][11]))
        self.f_min_label1.setText(str(self.star[index][12]))
        self.l_min_label1.setText(str(self.star[index][13]))
        self.min_editline.setText(str(self.star[index][14]))
        self.n_min_label1.setText(str(self.star[index][15]))
        self.l_period_label1.setText(str(self.star[index][16]))
        self.period_editline.setText(str(self.star[index][17]))
        self.u_period_label1.setText(str(self.star[index][18]))
        self.sp_label1.setText(str(self.star[index][19]))
        self.epoch_editline.setText(str(self.star[index][20]))
        self.u_epoch_label1.setText(str(self.star[index][21]))

    def ucac_changed(self):
        star_index = self.ucac4_combobox.currentIndex()
        if star_index < 0:
            self.clear_window()
            self.check_item(False)
        else:
            self.fill_star(star_index)
            if self.is_it_import:
                self.check_item(True)
            else:
                self.check_item(False)

    def set_cross_id(self):
        star_index = self.ucac4_combobox.currentIndex()
        if star_index < 0:
            return
        if self.is_it_import:
            if self.ucac4_checkbox.isChecked():
                self.object_edit_window.star_alternativ_name_editline.setText(str(self.star[star_index][3]).strip())

            if self.raj2000_checkbox.isChecked():
                try:
                    rektascenze = float(self.star[star_index][22]) / 15
                    rec_h = floor(rektascenze)
                    rec_m = floor((rektascenze - rec_h) * 60)
                    rec_s = round((((rektascenze - rec_h) * 60) - rec_m) * 60, 3)
                    self.object_edit_window.star_rec_h_spinbox.setValue(rec_h)
                    self.object_edit_window.star_rec_m_spinbox.setValue(rec_m)
                    self.object_edit_window.star_rec_s_spinbox.setValue(rec_s)
                except:
                    mistake("Rektascenze error", "Rektascenze must be a number, uncheck rektascenze import")
                self.object_edit_window.star_ekvinokcium_combobox.setCurrentText("2000")

            if self.dej2000_checkbox.isChecked():
                try:
                    declination = float(self.star[star_index][23])
                    if declination < 0:
                        self.object_edit_window.dec_sign.setCurrentIndex(1)
                        declination = fabs(declination)
                        print(declination)
                    else:
                        self.object_edit_window.dec_sign.setCurrentIndex(0)
                    dec_h = floor(declination)
                    dec_m = floor((declination - dec_h) * 60)
                    dec_s = round((((declination - dec_h) * 60) - dec_m) * 60, 3)
                    self.object_edit_window.star_dec_h_spinbox.setValue(dec_h)
                    self.object_edit_window.star_dec_m_spinbox.setValue(dec_m)
                    self.object_edit_window.star_dec_s_spinbox.setValue(dec_s)
                except:
                    mistake("Declination error", "Declination must be a number, uncheck declination import")
                self.object_edit_window.star_ekvinokcium_combobox.setCurrentText("2000")

            if self.type_checkbox.isChecked():
                var_type = self.type_editline.text().strip()
                if var_type in self.object_edit_window.database.variability_type:
                    self.object_edit_window.lightcurve_type_combobox.setCurrentText(var_type)
                else:
                    self.object_edit_window.get_new_variability_type()

            if self.max_checkbox.isChecked():
                try:
                    self.object_edit_window.star_mag_doublespinbox.setValue(float(self.star[star_index][9]))
                except:
                    mistake("Magnitude error", "Magnitude must be a number, uncheck magnitude import")

            if self.min_checkbox.isChecked():
                try:
                    self.object_edit_window.lightcurve_amplitude_prim_doulespinbox.setValue(float(
                        self.star[star_index][14]))
                except:
                    mistake("Amplitude error", "Amplitude must be a number, uncheck amplitude import")

            if self.epoch_checkbox.isChecked():
                try:
                    self.object_edit_window.lightcurve_epoch_editline.setText((str(self.star[star_index][20])))
                except:
                    mistake("Epoch error", "Epoch must be a number, uncheck epoch import")

            if self.period_checkbox.isChecked():
                try:
                    self.object_edit_window.lightcurve_period_editline.setText(str(self.star[star_index][17]))
                except:
                    mistake("Period error", "Period must be a number, uncheck period import")
            self.is_it_import = False
            self.close()
        else:
            try:
                new_ucac = str(self.star[star_index][3])
                star_index_in_main_file = self.step_main_form.stars.star_index(self.step_main_form.star_detail.name())
                self.step_main_form.stars.stars[star_index_in_main_file].change_vsx(new_ucac)
                self.step_main_form.vsx_button.setText("VSX " + new_ucac)
                current_row = self.step_main_form.objects_table.currentRow()
                self.step_main_form.objects_table.setItem(current_row, 9,
                                                          QtWidgets.QTableWidgetItem(new_ucac))
                self.step_main_form.star_detail.change_vsx(new_ucac)
                self.step_main_form.filtered_stars.stars[current_row].change_vsx(new_ucac)
            except:
                pass

    def clear_window(self):
        self.delta_r_label1.clear()
        self.raj2000_editline.clear()
        self.dej2000_editline.clear()
        self.oid_label1.clear()
        self.n_oid_label1.clear()
        self.v_label1.clear()
        self.type_editline.clear()
        self.l_max_label1.clear()
        self.max_editline.clear()
        self.u_max_label1.clear()
        self.n_max_label1.clear()
        self.f_min_label1.clear()
        self.l_min_label1.clear()
        self.min_editline.clear()
        self.n_min_label1.clear()
        self.l_period_label1.clear()
        self.period_editline.clear()
        self.u_period_label1.clear()
        self.sp_label1.clear()
        self.epoch_editline.clear()
        self.u_epoch_label1.clear()

    def check_item(self, active):
        self.raj2000_checkbox.setChecked(active)
        self.dej2000_checkbox.setChecked(active)
        self.type_checkbox.setChecked(active)
        self.max_checkbox.setChecked(active)
        self.min_checkbox.setChecked(active)
        self.period_checkbox.setChecked(active)
        self.epoch_checkbox.setChecked(active)
        self.ucac4_checkbox.setChecked(active)



