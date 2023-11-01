from coordinate import *
from astroquery.vizier import Vizier
import astropy.coordinates as coord
import astropy.units as u
import csv
from PyQt5 import QtWidgets, QtGui
from tess_menu_window import find_path_to_file
from step_main_form import Popup


class KnownVariableWindow(QtWidgets.QWidget):

    def __init__(self, *args, **kvargs):
        super(KnownVariableWindow, self).__init__(*args, **kvargs)

        self.setWindowTitle("Is it known variable star?")
        self.setWindowIcon(QtGui.QIcon("magnifier.png"))
        main_layout = QtWidgets.QGridLayout()
        self.setLayout(main_layout)
        self.star_list = []
        self.vsx_results_list = []
        self.asas_results_list = []
        self.gaia_results_list = []
        self.gaia_photometry_list = []

        self.input_radiobutton = QtWidgets.QRadioButton("Input catalog number")
        self.file_radiobutton = QtWidgets.QRadioButton("Read from file")
        self.input_editline = QtWidgets.QLineEdit()
        self.check_input_button = QtWidgets.QPushButton("Check")
        self.cataloque_id_combobox = QtWidgets.QComboBox()
        self.asas_list = QtWidgets.QListWidget()
        self.asas_list.setMaximumHeight(60)
        self.vsx_list = QtWidgets.QListWidget()
        self.vsx_list.setMaximumHeight(60)
        self.gaia_list = QtWidgets.QComboBox()
        self.gaia_variability_text_edit = QtWidgets.QTextEdit()
        self.aperture_asas_spinbox = QtWidgets.QSpinBox()
        self.aperture_vsx_spinbox = QtWidgets.QSpinBox()
        self.aperture_gaia_spinbox = QtWidgets.QSpinBox()
        self.clear_button = QtWidgets.QPushButton("Clear all")
        self.description_radiobutton = QtWidgets.QRadioButton("Read from field description")

        self.star_list_widget = QtWidgets.QListWidget()

        self.notes_label = QtWidgets.QLabel("")

        main_layout.addWidget(self.input_editline, 0, 0)
        main_layout.addWidget(self.input_radiobutton, 0, 1)
        main_layout.addWidget(self.check_input_button, 0, 2)
        main_layout.addWidget(self.file_radiobutton, 0, 3)
        main_layout.addWidget(self.description_radiobutton, 0, 4)

        main_layout.addWidget(self.notes_label, 1, 0, 1, 5)

        main_layout.addWidget(self.cataloque_id_combobox, 2, 0, 1, 4)
        main_layout.addWidget(self.clear_button, 2, 4)
        main_layout.addWidget(QtWidgets.QLabel("ASAS-SN:"), 3, 0)
        main_layout.addWidget(QtWidgets.QLabel("  Aperture(s):"), 3, 3)
        main_layout.addWidget(self.aperture_asas_spinbox, 3, 4)
        main_layout.addWidget(self.asas_list, 4, 0, 2, 5)
        main_layout.addWidget(QtWidgets.QLabel("VSX:"), 6, 0)
        main_layout.addWidget(QtWidgets.QLabel("  Aperture(s):"), 6, 3)
        main_layout.addWidget(self.aperture_vsx_spinbox, 6, 4)
        main_layout.addWidget(self.vsx_list, 7, 0, 2, 5)
        main_layout.addWidget(QtWidgets.QLabel("GAIA:"), 9, 0)
        main_layout.addWidget(QtWidgets.QLabel("  Aperture(s):"), 9, 3)
        main_layout.addWidget(self.aperture_gaia_spinbox, 9, 4)
        main_layout.addWidget(self.gaia_list, 10, 0, 1, 5)
        main_layout.addWidget(QtWidgets.QLabel("GAIA variability catalogs:"), 11, 0)
        main_layout.addWidget(self.gaia_variability_text_edit, 12, 0, 8, 5)

    def setup(self):
        from step_application import root
        self.step_main_form_window = root.step_main_form

        self.input_editline.setEnabled(False)
        self.file_radiobutton.setChecked(True)
        self.aperture_asas_spinbox.setValue(5)
        self.aperture_vsx_spinbox.setValue(5)
        self.aperture_gaia_spinbox.setValue(2)
        self.file_radiobutton.clicked.connect(self.radiobuttons_was_clicked)
        self.input_radiobutton.clicked.connect(self.radiobuttons_was_clicked)
        self.description_radiobutton.clicked.connect(self.radiobuttons_was_clicked)
        self.check_input_button.clicked.connect(self.check_button_was_checked)
        self.clear_button.clicked.connect(self.clear_button_was_clicked)
        self.cataloque_id_combobox.currentTextChanged.connect(self.catalogue_id_combobox_was_changed)
        self.gaia_list.currentTextChanged.connect(self.gaia_combobox_was_changed)

    def __combobox_connect(self, connection):
        if connection:
            self.cataloque_id_combobox.currentTextChanged.connect(self.catalogue_id_combobox_was_changed)
            self.gaia_list.currentTextChanged.connect(self.gaia_combobox_was_changed)
        else:
            self.cataloque_id_combobox.disconnect()
            self.gaia_list.disconnect()

    def clear_button_was_clicked(self):
        self.cataloque_id_combobox.clear()
        self.gaia_variability_text_edit.clear()
        self.gaia_list.clear()
        self.vsx_list.clear()
        self.asas_list.clear()
        self.asas_results_list = []
        self.vsx_results_list = []
        self.gaia_results_list = []
        self.gaia_photometry_list = []
        self.star_list = []

    def catalogue_id_combobox_was_changed(self):
        star_index = self.cataloque_id_combobox.currentIndex()
        self.asas_list.clear()
        self.vsx_list.clear()
        self.gaia_list.clear()
        self.gaia_variability_text_edit.clear()
        if self.star_list[star_index][0] != "UNKNOWN":
            for star in self.vsx_results_list[star_index]:
                vsx_info_text = star[1] + ", Δr:" + str(star[0]) + "s, " + star[4] + " " + star[5] + ", mag:" \
                               + str(star[6]) + " period:" + str(star[7]) + " epoch:" + str(star[8])
                item = QtWidgets.QListWidgetItem(vsx_info_text)
                self.vsx_list.addItem(item)
            for star in self.asas_results_list[star_index]:
                asas_info_text = "ASAS-SN " + star[1] + ", Δr:" + str(star[0]) + "s, " + star[4] + " " + star[5] \
                                 + ", mag:" + str(star[6]) + " period:" + str(star[8]) + " amplitude:" + str(star[7])
                item = QtWidgets.QListWidgetItem(asas_info_text)
                self.asas_list.addItem(item)
            for star in self.gaia_results_list[star_index]:
                gaia_info_text = "GAIA " + str(star[1]) + ", Δr:" + str(star[0]) + "s,  " + star[4] + " " \
                                 + star[5] + ", mag:" + str(star[6])
                self.gaia_list.addItem(gaia_info_text)
            self.gaia_combobox_was_changed()

    def gaia_combobox_was_changed(self):
        star_index = self.cataloque_id_combobox.currentIndex()
        gaia_text_list = self.gaia_photometry_list[star_index]
        gaia_index = self.gaia_list.currentIndex()
        if gaia_index >= 0:
            full_text = ""
            for catalogue_text in gaia_text_list[gaia_index]:
                full_text = full_text + catalogue_text
            if "TableList with 2 tables:" in full_text and "TableList with 2 tables:" in full_text and "TableList with 2 tables:" in full_text:
                full_text = "UNKNOWN VARIABLE"
            self.gaia_variability_text_edit.setText(full_text)
        else:
            self.gaia_variability_text_edit.clear()

    def read_input_file(self, data_path):
        try:
            with open(data_path) as data_file:
                read_file = csv.reader(data_file, delimiter=";")
                stars = [row for row in read_file]
        except:
            r = Popup("File error", "File access denied or path not specified", buttons="OK".split(","))
            r.do()
            return []
        variable_list = []
        star_list = []
        if self.description_radiobutton.isChecked():
            if data_path[len(data_path)-3:len(data_path)] != "sfd":
                r = Popup("Not description file", "File isn´t description file", buttons="OK".split(","))
                r.do()
                return []
            while "[Stars]" not in stars[0] and len(stars) > 1:
                del (stars[0])
            del (stars[0])
            while "[Variables]" not in stars[0] and len(stars) > 1:
                star = []
                if stars[0] and stars[0][2] not in ["", " "]:
                    star_first_item = stars[0][0].split(sep="=")
                    star.append(star_first_item[0].strip())
                    star.append((stars[0][2].strip()))
                    star_list.append(star)
                del (stars[0])
            del (stars[0])
            while len(stars) > 0:
                if stars[0]:
                    variable_first_item = stars[0][0].split(sep="=")
                    variable = variable_first_item[0].strip()
                    for item_star in star_list:
                        if variable == item_star[0]:
                            variable_list.append([item_star[1],item_star[0]])
                del (stars[0])
        else:
            for star in stars:
                if star:
                    variable_list.append([star[0],""])
        return variable_list

    def radiobuttons_was_clicked(self):
        if self.file_radiobutton.isChecked() or self.description_radiobutton.isChecked():
            self.input_editline.setEnabled(False)
        if self.input_radiobutton.isChecked():
            self.input_editline.setEnabled(True)

    def fill_star(self, star_id_info, star_name=""):
        if star_id_info[0] == "UNKNOWN":
            if star_name:
                item_text = star_id_info[1] + " (" + star_name + ") UNKNOWN"
            else:
                item_text = star_id_info[1] + "UNKNOWN"
            self.cataloque_id_combobox.addItem(item_text)
            self.cataloque_id_combobox.setCurrentText(item_text)
            self.asas_list.clear()
            self.vsx_list.clear()
            self.gaia_list.clear()
            self.gaia_variability_text_edit.clear()
            self.vsx_results_list.append(star_id_info)
            self.asas_results_list.append(star_id_info)
            self.gaia_results_list.append(star_id_info)
            self.gaia_photometry_list.append([""])
        else:
            if star_name:
                item_text = star_id_info[0] + " " + star_id_info[1] + " (" + star_name + "), " + star_id_info[4] \
                            + " " + star_id_info[5] + ", mag:" + str(star_id_info[6])
            else:
                item_text = star_id_info[0] + " " + star_id_info[1] + "," + star_id_info[4] + " " + star_id_info[5] \
                            + ", mag:" + str(star_id_info[6])
            self.cataloque_id_combobox.addItem(item_text)
            self.cataloque_id_combobox.setCurrentText(item_text)
            self.notes_label.setText("loading: star " + star_id_info[0] + " " + star_id_info[1] + " - VSX")
            QtWidgets.QApplication.processEvents()
            vsx_info_list = self.vsx_star_in_aperture(star_id_info[2], star_id_info[3])
            self.notes_label.setText("loading: star " + star_id_info[0] + " "  + star_id_info[1] + " - ASAS-SN")
            QtWidgets.QApplication.processEvents()
            asas_info_list = self.assa_sn_star_in_aperture(star_id_info[2], star_id_info[3])
            self.notes_label.setText("loading: star " + star_id_info[0] + " "  + star_id_info[1] + " - GAIA")
            QtWidgets.QApplication.processEvents()
            gaia_info_list = self.gaia_star_in_aperture(star_id_info[2], star_id_info[3])
            self.vsx_results_list.append(vsx_info_list)
            self.gaia_results_list.append(gaia_info_list)
            self.asas_results_list.append(asas_info_list)
            self.asas_list.clear()
            self.vsx_list.clear()
            self.gaia_list.clear()
            self.gaia_variability_text_edit.clear()
            gaia_variability_info_list = []
            for star in vsx_info_list:
                vsx_info_text = star[1] + ", Δr:" + str(star[0]) + "s, " + star[4] + " " + star[5] \
                                + ", mag:" + str(star[6]) + " period:" + str(star[7]) + " epoch:" + str(star[8])
                item = QtWidgets.QListWidgetItem(vsx_info_text)
                self.vsx_list.addItem(item)
            for star in gaia_info_list:
                gaia_info_text = "GAIA " + str(star[1]) + ", Δr:" + str(star[0]) + "s,  " + star[4] + " " \
                                 + star[5] + ", mag:" + str(star[6])
                self.gaia_list.addItem(gaia_info_text)
                self.notes_label.setText("loading: star " + star_id_info[0] + " " + star_id_info[1] + " - GAIA "
                                         + str(star[1]))
                QtWidgets.QApplication.processEvents()

                gaia_variability_info_list.append(self.check_gaia_photometry(star[1]))
            self.gaia_photometry_list.append(gaia_variability_info_list)
            if len(gaia_variability_info_list) > 0:
                full_text = ""
                for catalogue_text in gaia_variability_info_list[0]:
                    full_text = full_text + catalogue_text
                if "TableList with 2 tables:" in full_text and "TableList with 2 tables:" in full_text and "TableList with 2 tables:" in full_text:
                    full_text = "UNKNOWN VARIABLE"
                self.gaia_variability_text_edit.setText(full_text)
            else:
                self.gaia_variability_text_edit.clear()
            for star in asas_info_list:
                asas_info_text = "ASAS-SN " + star[1] + ", Δr:" + str(star[0]) + "s, " + star[4] + " " + star[5] \
                                 + ", mag:" + str(star[6]) + " period:" + str(star[8]) + " amplitude:" \
                                 + str(star[7])
                item = QtWidgets.QListWidgetItem(asas_info_text)
                self.asas_list.addItem(item)
        self.star_list.append(star_id_info)
        self.notes_label.setText("")

    def check_button_was_checked(self):
        self.__combobox_connect(False)
        self.check_input_button.setText("READING")
        QtWidgets.QApplication.processEvents()
        if self.input_radiobutton.isChecked():
            star_id_info = self.star_information(self.input_editline.text())
            self.fill_star(star_id_info)
            self.check_input_button.setText("Check")
        elif self.file_radiobutton.isChecked() or self.description_radiobutton.isChecked():
            if self.file_radiobutton.isChecked():
                data_path = find_path_to_file(current_path="", window_table="Select the file", mask="*.txt",
                                              path_to_file=True)
            else:
                data_path = find_path_to_file(current_path="", window_table="Select the file", mask="*.sfd",
                                              path_to_file=True)
            star_list = self.read_input_file(data_path[0])
            stars_quantity = len(star_list)
            for i, star in enumerate(star_list):
                self.check_input_button.setText("UPLOADING: " + str(int((i+1) / stars_quantity * 100)) + "%")
                QtWidgets.QApplication.processEvents()
                star_id_info = self.star_information(star[0])
                self.fill_star(star_id_info, star_name=star[1])
        else:
            pass

        self.check_input_button.setText("Check")
        self.__combobox_connect(True)

    def check_catalogue(self, catalogue_number):
        catalogue_number = catalogue_number.strip()
        if len(catalogue_number) == 10:
                if catalogue_number[3] == "-" and catalogue_number[0:3].isdigit() and catalogue_number[4:10].isdigit():
                    return "UCAC4"
                else:
                    return ["UNKNOWN"]
        elif len(catalogue_number) == 12:
            if catalogue_number[4] == "-" and catalogue_number[0:4].isdigit() and catalogue_number[5:12].isdigit():
                return "USNO-B1.0"
            else:
                return ["UNKNOWN"]
        else:
            return ["UNKNOWN"]

    def star_information(self, id_number):
        if self.check_catalogue(id_number) == "UCAC4":
            self.notes_label.setText("loading: star UCAC4 " + id_number)
            QtWidgets.QApplication.processEvents()
            try:
                agn = Vizier(catalog="I/322A", columns=["*"]).query_constraints(UCAC4=id_number.strip())[0]
                for x in agn:
                    rec_star = x["RAJ2000"]
                    dec_star = x["DEJ2000"]
                    rec_txt = coordinate_to_text(radians(float(rec_star)), coordinate_format="hours",
                                                 delimiters=("h ", "m ", 's'),
                                                 decimal_numbers=3)
                    dec_txt = coordinate_to_text(radians(float(dec_star)), coordinate_format="degree",
                                                 delimiters=("° ", "m ", 's'),
                                                 decimal_numbers=3)
                    fmag = x["f.mag"]
                    star_info = ["UCAC4", id_number, rec_star, dec_star, rec_txt, dec_txt, fmag, ""]
                    return(star_info)
            except:
                return ["UNKNOWN", id_number]
        elif self.check_catalogue(id_number) == "USNO-B1.0":
            self.notes_label.setText("loading: star USNO-B1.0 " + id_number)
            QtWidgets.QApplication.processEvents()
            try:
                agn = Vizier(catalog="I/284", columns=["*"]).query_constraints(USNO_B1_0=id_number.strip())[0]
                for x in agn:
                    rec_star = x["RAJ2000"]
                    dec_star = x["DEJ2000"]
                    rec_txt = coordinate_to_text(radians(float(rec_star)), coordinate_format="hours",
                                                 delimiters=("h ", "m ", 's'),
                                                 decimal_numbers=3)
                    dec_txt = coordinate_to_text(radians(float(dec_star)), coordinate_format="degree",
                                                 delimiters=("° ", "m ", 's'),
                                                 decimal_numbers=3)
                    r1mag = x["R1mag"]
                    star_info = ["USNO-B1.0", id_number, rec_star, dec_star, rec_txt, dec_txt, r1mag, ""]
                    return(star_info)
            except:
                return ["UNKNOWN", id_number]
        else:
            return ["UNKNOWN", id_number]


    def gaia_star_in_aperture(self, rec_star, dec_star, aperture="1s"):
        if self.aperture_gaia_spinbox.value() > 0:
            aperture = str(self.aperture_gaia_spinbox.value()) + "s"
        near_star_list = []
        v = Vizier(columns=["*", "+_r", "BP-G", "G-RP"], catalog="I/355/gaiadr3")
        a = coord.SkyCoord(ra=rec_star, dec=dec_star, unit=(u.deg, u.deg))
        result = v.query_region(a, radius=aperture)
        for y in result:
            for x in y:
                id_star = x["Source"]
                delta_r = x["_r"]
                ra_icrs = x["RA_ICRS"]
                de_icrs = x["DE_ICRS"]
                ra_icrs_txt = coordinate_to_text(radians(float(ra_icrs)), coordinate_format="hours",
                                                 delimiters=("h ", "m ", 's'),
                                                 decimal_numbers=3)
                de_icrs_txt = coordinate_to_text(radians(float(de_icrs)), coordinate_format="degree",
                                                 delimiters=("° ", "m ", 's'),
                                                 decimal_numbers=3)
                rpmag = x["RPmag"]
                raj2000 = x["RAJ2000"]
                dej2000 = x["DEJ2000"]
                raj2000_txt = coordinate_to_text(radians(float(raj2000)), coordinate_format="hours",
                                                 delimiters=("h ", "m ", 's'),
                                                 decimal_numbers=3)
                dej2000_txt = coordinate_to_text(radians(float(dej2000)), coordinate_format="degree",
                                                 delimiters=("° ", "m ", 's'),
                                                 decimal_numbers=3)

                near_star_list.append([delta_r, id_star, ra_icrs, de_icrs, ra_icrs_txt, de_icrs_txt, rpmag, raj2000,
                                       dej2000, raj2000_txt, dej2000_txt])
        return near_star_list

    def assa_sn_star_in_aperture(self, rec_star, dec_star, aperture="1s"):
        near_star_list = []
        if self.aperture_asas_spinbox.value() > 0:
            aperture = str(self.aperture_asas_spinbox.value()) + "s"
        v = Vizier(columns=["+_r", "ASASSN-V", "RAJ2000", "DEJ2000", "Vmag", "Amp", "Per"], catalog="II/366")
        a = coord.SkyCoord(ra=rec_star, dec=dec_star, unit=(u.deg, u.deg))
        result = v.query_region(a, radius=aperture)
        for y in result:
            for x in y:
                delta_r = x["_r"]
                asassn = x["ASASSN-V"]
                rec_star = x["RAJ2000"]
                dec_star = x["DEJ2000"]
                rec_txt = coordinate_to_text(radians(float(rec_star)), coordinate_format="hours",
                                             delimiters=("h ", "m ", 's'),
                                             decimal_numbers=3)
                dec_txt = coordinate_to_text(radians(float(dec_star)), coordinate_format="degree",
                                             delimiters=("° ", "m ", 's'),
                                             decimal_numbers=3)

                vmag = x["Vmag"]
                amp = x["Amp"]
                per = x["Per"]

                near_star_list.append([delta_r, asassn, rec_star, dec_star, rec_txt, dec_txt, vmag, amp, per])
        return near_star_list

    def vsx_star_in_aperture(self, rec_star, dec_star, aperture="1s"):
        near_star_list = []
        if self.aperture_vsx_spinbox.value() > 0:
            aperture = str(self.aperture_vsx_spinbox.value()) + "s"

        v = Vizier(columns=["*", "+_r", "Epoch", "u_Epoch"], catalog="B/vsx")
        a = coord.SkyCoord(ra=rec_star, dec=dec_star, unit=(u.deg, u.deg))
        result = v.query_region(a, radius=aperture)
        for y in result:
            for x in y:
                delta_r = x["_r"]
                id_star = x["Name"]
                rec_star = x["RAJ2000"]
                dec_star = x["DEJ2000"]
                rec_txt = coordinate_to_text(radians(float(rec_star)), coordinate_format="hours",
                                             delimiters=("h ", "m ", 's'),
                                             decimal_numbers=3)
                dec_txt = coordinate_to_text(radians(float(dec_star)), coordinate_format="degree",
                                             delimiters=("° ", "m ", 's'),
                                             decimal_numbers=3)
                max_mag = x["max"]
                period = x["Period"]
                epoch = x["_tab1_15"]

                near_star_list.append([delta_r, id_star, rec_star, dec_star, rec_txt, dec_txt, max_mag,
                                       period, epoch])
        return near_star_list

    def check_gaia_photometry(self, gaia_number):
        gaia_info_list = []
        try:
            agn = Vizier(catalog="I/358", columns=["*"]).query_constraints(Source=gaia_number)
        except:
            gaia_info_list.append("download error\n\n\n")
            return gaia_info_list
        catalogue_list = str(agn).split("\n")
        for i, catalogue in enumerate(catalogue_list):
            try:
                if "I/358/varisum" in catalogue:
                    for x in agn[i-1]:
                        star_source = x["Source"]
                        ra_icrs = x["RA_ICRS"]
                        de_icrs = x["DE_ICRS"]
                        vcr = x["VCR"]
                        vrrlyr = x["VRRLyr"]
                        vcep = x["VCep"]
                        vpn = x["VPN"]
                        vst = x["VST"]
                        vlpv = x["VLPV"]
                        veb = x["VEB"]
                        vrm = x["VRM"]
                        vmso = x["VMSO"]
                        vagn = x["VAGN"]
                        vmicro = x["Vmicro"]
                        vcc = x["VCC"]
                    all_line = catalogue + "\nSource: " + str(star_source) + "\nRA_ICRS: " + str(ra_icrs) \
                               + "deg\nDE_ICRS: " + str(de_icrs) + "deg\nVCR: " + str(vcr) + "\tVRRLyr: " \
                               + str(vrrlyr) + "\tVCep: " + str(vcep) + "\tVPN: " + str(vpn) + "\tVST:" + str(vst) \
                               + "\tVLPV " + str(vlpv) + "\nVEB " + str(veb) + "\tVRM " + str(vrm) + "\tVMSO " \
                               + str(vmso) + "\tVAGN " + str(vagn) + "\tVmicro " + str(vmicro) + "\tVCC " + str(vcc) \
                               + "\n\n\n"
                    gaia_info_list.insert(0, all_line)
            except:
                gaia_info_list.insert(0, "I/358/varisum - ERROR\n\n\n")
            try:
                if "I/358/vagn" in catalogue:
                    for x in agn[i-1]:
                        fvarg =x["fvarG"]
                        sfindex = x["SFIndex"]
                    all_line = catalogue + "\nfvarG: " + str(fvarg) + "\nSFIndex: " + str(sfindex) + "\n\n\n"
                    gaia_info_list.append(all_line)
            except:
                gaia_info_list.append("I/358/vagn - ERROR\n\n\n")
            try:
                if "I/358/vclassre" in catalogue:
                    for x in agn[i-1]:
                        classifier =x["Classifier"]
                        star_class = x["Class"]
                    all_line = catalogue + "\nClassifier: " + str(classifier) + "\nClass: " + str(star_class) + "\n\n\n"
                    gaia_info_list.append(all_line)
            except:
                gaia_info_list.append("I/358/vclassre - ERROR\n\n\n")
            try:
                if "I/358/vcep" in catalogue and "I/358/vceph" not in catalogue:
                    for x in agn[i-1]:
                        pf =x["PF"]
                        p10 = x["P1O"]
                        gmagavg = x["Gmagavg"]
                        bpmagavg = x["BPmagavg"]
                        rpmagavg = x["RPmagavg"]
                        star_class = x["Class"]
                        subclass = x["SubClass"]
                        modeclass = x["ModeClass"]
                        mulmodeclass = x["MulModeClass"]
                    all_line = catalogue + "\nPF: " + str(pf) + "d\nP1O: " + str(p10) + "d\nGmagavg: " + str(gmagavg) \
                               + "mag\nBPmagavg: " + str(bpmagavg) + "mag\nRPmagavg: " + str(rpmagavg) \
                               + "mag\nClass: " + str(star_class) + "\nSubClass: " + str(subclass) + "\nModeClass:" \
                               + str(modeclass) + "\nMulModeClas " + str(mulmodeclass) + "\n\n\n"
                    gaia_info_list.append(all_line)
            except:
                gaia_info_list.append("I/358/vcep - ERROR\n\n\n")
            try:
                if "I/358/vceph" in catalogue:
                    for x in agn[i-1]:
                        ampfund =x["AmpFundFreq1G"]
                        phasefund = x["PhaseFundFreq1G"]
                    all_line = catalogue + "\nAmpFundFreq1G: " + str(ampfund) + "mag\nPhaseFundFreq1G: " \
                               + str(phasefund) + "rad\n\n\n"
                    gaia_info_list.append(all_line)
            except:
                gaia_info_list.append("I/358/vceph - ERROR\n\n\n")
            try:
                if "I/358/vcc" in catalogue and "I/358/vcclassd" not in catalogue:
                    for x in agn[i-1]:
                        per = x["Per"]
                        epoch = x["T0G"]
                    all_line = catalogue + "\nPer: " + str(per) + "d\nT0G: " + str(epoch) + "d\n\n\n"
                    gaia_info_list.append(all_line)
            except:
                gaia_info_list.append("I/358/vcc - ERROR\n\n\n")
            try:
                if "I/358/veb" in catalogue:
                    for x in agn[i - 1]:
                        ttime = x["_tab10_4"]
                        freg = x["Freq"]
                        magmod = x["magModRef"]
                        phase = x["PhaseGauss1"]
                        depth1 = x["DepthE1"]
                        depth2 = x["DepthE2"]

                    all_line = catalogue + "\nTimeRef: " + str(ttime) + "d\nFreq: " + str(freg) + "d-1\nmagModRef: " \
                               + str(magmod) + "mag\nPhaseGauss1: " + str(phase) + "\nDepthE1: " + str(depth1) \
                               + "mag\nDepthE2: " + str(depth2) + "mag\n\n\n"
                    gaia_info_list.append(all_line)
            except:
                gaia_info_list.append("I/358/veb - ERROR\n\n\n")
            try:
                if "I/358/veprv" in catalogue:
                    for x in agn[i-1]:
                        timerv =x["TimeRV"]
                        rv = x["RV"]
                        e_rv = x["e_RV"]
                    all_line = catalogue + "\nTimeRV: " + str(timerv) + "d\nRV: " + str(rv) + "km/s\ne_RV: " \
                               + str(e_rv) + "km/s\n\n\n"
                    gaia_info_list.append(all_line)
            except:
                gaia_info_list.append("I/358/veprv - ERROR\n\n\n")
            try:
                if "I/358/vlpv" in catalogue:
                    for x in agn[i - 1]:
                        freq = x["Freq"]
                        amp = x["Amp"]
                    all_line = catalogue + "\nFreq: " + str(freq) + "1/d\nAmp: " + str(amp) + "mag\n\n\n"
                    gaia_info_list.append(all_line)
            except:
                gaia_info_list.append("I/358/vlpv - ERROR\n\n\n")
            try:
                if "I/358/vmicro" in catalogue:
                    #for x in agn[i - 1]:
                    #    freq = x["Freq"]
                    #    amp = x["Amp"]
                    all_line = catalogue + "\nAsk the author of this program to add specific characteristics from " \
                                           "the GAIA source table\n\n\n"
                    gaia_info_list.append(all_line)
            except:
                gaia_info_list.append("I/358/vmicro - ERROR\n\n\n")
            try:
                if "I/358/vmsosc" in catalogue:
                    #for x in agn[i - 1]:
                    #    freq = x["Freq"]
                    #    amp = x["Amp"]
                    all_line = catalogue + "\nAsk the author of this program to add specific characteristics from " \
                                           "the GAIA source table\n\n\n"
                    gaia_info_list.append(all_line)
            except:
                gaia_info_list.append("I/358/vmsosc - ERROR\n\n\n")
            try:
                if "I/358/vrm" in catalogue and "I/358/vrmo" not in catalogue and "I/358/vrmos" not in catalogue:
                    for x in agn[i - 1]:
                        prot = x["Prot"]
                        gunsp = x["Gunsp"]
                    all_line = catalogue + "\nProt: " + str(prot) + "d\nGunsp: " + str(gunsp) + "mag\n\n\n"
                    gaia_info_list.append(all_line)
            except:
                gaia_info_list.append("I/358/vrm - ERROR\n\n\n")
            try:
                if "I/358/vrmo" in catalogue:
                    #for x in agn[i - 1]:
                    #    freq = x["Freq"]
                    #    amp = x["Amp"]
                    all_line = catalogue + "\nAsk the author of this program to add specific characteristics from " \
                                           "the GAIA source table\n\n\n"
                    gaia_info_list.append(all_line)
            except:
                gaia_info_list.append("I/358/vrmo - ERROR\n\n\n")
            try:
                if "I/358/vrms" in catalogue:
                    #for x in agn[i - 1]:
                    #    freq = x["Freq"]
                    #    amp = x["Amp"]
                    all_line = catalogue + "\nAsk the author of this program to add specific characteristics from " \
                                           "the GAIA source table\n\n\n"
                    gaia_info_list.append(all_line)
            except:
                gaia_info_list.append("I/358/vrms - ERROR\n\n\n")
            try:
                if "I/358/vpltrans" in catalogue:
                    for x in agn[i - 1]:
                        timereftrans = x["TimeRefTrans"]
                        pertrans = x["PerTrans"]
                        depthtrans = x["DepthTrans"]
                        durtrans = x["DurTrans"]
                        nintransit = x["Nintransit"]
                    all_line = catalogue + "\nTimeRefTrans: " + str(timereftrans) + "d\nPerTrans: " + str(pertrans) \
                               + "d\nDepthTrans: " + str(depthtrans) + "mmag\nDurTrans: " + str(durtrans) + "d\nNintransit: " + str(nintransit) + "\n\n\n"
                    gaia_info_list.append(all_line)
            except:
                gaia_info_list.append("I/358/vpltrans - ERROR\n\n\n")
            try:
                if "I/358/vrrlyr" in catalogue and "I/358/vrrlyrh" not in catalogue:
                    for x in agn[i - 1]:
                        pf = x["PF"]
                        epochg = x["EpochG"]
                    all_line = catalogue + "\nPF: " + str(pf) + "d\nEpochG: " + str(epochg) + "d\n\n\n"
                    gaia_info_list.append(all_line)
            except:
                gaia_info_list.append("I/358/vrrlyr - ERROR\n\n\n")
            try:
                if "I/358/vrrlyrh" in catalogue:
                    #for x in agn[i - 1]:
                    #    freq = x["Freq"]
                    #    amp = x["Amp"]
                    all_line = catalogue + "\nAsk the author of this program to add specific characteristics from " \
                                           "the GAIA source table\n\n\n"
                    gaia_info_list.append(all_line)
            except:
                gaia_info_list.append("I/358/vrrlyrh - ERROR\n\n\n")
            try:
                if "I/358/vst" in catalogue:
                    for x in agn[i - 1]:
                        ampl = x["Ampl"]
                        nfo = x["NfoVTrans"]
                    all_line = catalogue + "\nAmpl: " + str(ampl) + "mag\nNfoVTrans: " + str(nfo) + "\n\n\n"
                    gaia_info_list.append(all_line)
            except:
                gaia_info_list.append("I/358/vst - ERROR\n\n\n")
        catalogue_text = ""
        for catalogue in catalogue_list:
            catalogue_text = catalogue_text + "\n" + catalogue
        all_line = "List of catalogues with relevant information:\n" + catalogue_text
        gaia_info_list.append(all_line)
        return gaia_info_list




