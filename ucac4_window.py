from PyQt5 import QtWidgets            # QtCore, QtGui
from coordinate import *
from astroquery.vizier import Vizier
# from astropy.coordinates import Angle
import astropy.coordinates as coord
import astropy.units as u


class UCAC4Window(QtWidgets.QWidget):

    def __init__(self, *args,**kvargs):
        super(UCAC4Window, self).__init__(*args, **kvargs)

        self.star = []
        self.setWindowTitle("UCAC4 Catalogue Information")
        main_layout = QtWidgets.QVBoxLayout()
        self.setLayout(main_layout)

        ucac4_label = QtWidgets.QLabel("UCAC4 identifier: ")
        self.ucac4_combobox = QtWidgets.QComboBox()

        header_layout = QtWidgets.QHBoxLayout()
        header_layout.addWidget(ucac4_label)
        header_layout.addWidget(self.ucac4_combobox)

        self.set_cross_id_button = QtWidgets.QPushButton("Choose the correct cross identification")
        delta_r_label = QtWidgets.QLabel("Radius:")
        self.raj2000_checkbox = QtWidgets.QCheckBox("RA eq.2000:")
        self.dej2000_checkbox = QtWidgets.QCheckBox("DE eq.2000:")
        position_error_label = QtWidgets.QLabel("Position err (mas):")
        self.fmag_checkbox = QtWidgets.QCheckBox("UCAC4 mag:")
        of_label = QtWidgets.QLabel("Object classification flag")
        db_label = QtWidgets.QLabel("Double star flag")
        pm_ra_label = QtWidgets.QLabel("Proper motion in RA")
        pm_de_label = QtWidgets.QLabel("Proper motion in DE")
        j_mag_label = QtWidgets.QLabel("J magnitude:")
        k_mag_label = QtWidgets.QLabel("K magnitude:")
        b_mag_label = QtWidgets.QLabel("B magnitude:")
        v_mag_label = QtWidgets.QLabel("V magnitude:")
        r_mag_label = QtWidgets.QLabel("r magnitude:")
        i_mag_label = QtWidgets.QLabel("i magnitude:")

        self.delta_r_label1 = QtWidgets.QLabel("")
        self.raj2000_editline = QtWidgets.QLineEdit("")
        self.dej2000_editline = QtWidgets.QLineEdit("")
        self.position_error_label1 = QtWidgets.QLabel("")
        self.fmag_editline = QtWidgets.QLineEdit("")
        self.of_label1 = QtWidgets.QLabel("")
        self.db_label1 = QtWidgets.QLabel("")
        self.pm_ra_label1 = QtWidgets.QLabel("")
        self.pm_de_label1 = QtWidgets.QLabel("")
        self.j_mag_label1 = QtWidgets.QLabel("")
        self.k_mag_label1 = QtWidgets.QLabel("")
        self.b_mag_label1 = QtWidgets.QLabel("")
        self.v_mag_label1 = QtWidgets.QLabel("")
        self.r_mag_label1 = QtWidgets.QLabel("")
        self.i_mag_label1 = QtWidgets.QLabel("")

        info_groupbox = QtWidgets.QGroupBox("UCAC4 information")
        info_layout = QtWidgets.QFormLayout()
        info_groupbox.setLayout(info_layout)

        info_layout.addRow(delta_r_label, self.delta_r_label1)
        info_layout.addRow(self.raj2000_checkbox, self.raj2000_editline)
        info_layout.addRow(self.dej2000_checkbox, self.dej2000_editline)
        info_layout.addRow(position_error_label, self.position_error_label1)
        info_layout.addRow(self.fmag_checkbox, self.fmag_editline)
        info_layout.addRow(of_label, self.of_label1)
        info_layout.addRow(db_label, self.db_label1)
        info_layout.addRow(pm_ra_label, self.pm_ra_label1)
        info_layout.addRow(pm_de_label, self.pm_de_label1)
        info_layout.addRow(j_mag_label, self.j_mag_label1)
        info_layout.addRow(k_mag_label, self.k_mag_label1)
        info_layout.addRow(b_mag_label,self.b_mag_label1)
        info_layout.addRow(v_mag_label, self.v_mag_label1)
        info_layout.addRow(r_mag_label, self.r_mag_label1)
        info_layout.addRow(i_mag_label, self.i_mag_label1)

        main_layout.addLayout(header_layout)
        main_layout.addWidget(self.set_cross_id_button)
        main_layout.addWidget(info_groupbox)

    def setup(self):
        from step_application import root
        self.step_main_form = root.step_main_form
        self.ucac4_combobox.currentTextChanged.connect(self.ucac_changed)
        self.set_cross_id_button.clicked.connect(self.set_cross_id)

    def download_data_id(self, cross_id: str):
        self.star.clear()
        agn = Vizier(catalog="I/322A", columns=["*"]).query_constraints(UCAC4=cross_id)[0]
        for x in agn:
            id_star = x["UCAC4"]
            rec_star = x["RAJ2000"]
            dec_star = x["DEJ2000"]
            rec_txt = coordinate_to_text(radians(float(rec_star)), coordinate_format="hours", delimiters=("h ", "m ", 's'),
                                         decimal_numbers=3)
            dec_txt = coordinate_to_text(radians(float(dec_star)), coordinate_format="degree", delimiters=("° ", "m ", 's'),
                                         decimal_numbers=3)
            epos = x["ePos"]
            fmag = x["f.mag"]
            of = x["of"]
            db = x["db"]
            pmra = x["pmRA"]
            pmde = x["pmDE"]
            jmag = x["Jmag"]
            kmag = x["Kmag"]
            vmag = x["Vmag"]
            bmag = x["Bmag"]
            rmag = x["rmag"]
            imag = x["imag"]

            self.star = [["", id_star, rec_txt, dec_txt, epos, fmag, of, db, pmra, pmde, jmag, kmag, vmag, bmag, rmag,
                          imag, rec_star, dec_star]]
            self.ucac4_combobox.clear()
            self.ucac4_combobox.addItem(str(id_star))
            self.set_cross_id_button.setEnabled(False)
            self.fill_star(0)




    def download_data_coor(self, coor: Coordinate):
        self.star.clear()
        rec = degrees(coor.rektascenze())
        dec = degrees(coor.deklinace())
        v = Vizier(columns=["*", "+_r"], catalog="I/322A")
        a = coord.SkyCoord(ra=rec, dec=dec, unit=(u.deg, u.deg))
        result = v.query_region(a, radius="10s")
        name_list = []
        for y in result:
            for x in y:
                r = x["_r"]
                id_star = x["UCAC4"]
                rec_star = x["RAJ2000"]
                dec_star = x["DEJ2000"]
                rec_txt = coordinate_to_text(radians(float(rec_star)), coordinate_format="hours",
                                             delimiters=("h ", "m ", 's'),
                                             decimal_numbers=3)
                dec_txt = coordinate_to_text(radians(float(dec_star)), coordinate_format="degree",
                                             delimiters=("° ", "m ", 's'),
                                             decimal_numbers=3)
                epos = x["ePos"]
                fmag = x["f.mag"]
                of = x["of"]
                db = x["db"]
                pmra = x["pmRA"]
                pmde = x["pmDE"]
                jmag = x["Jmag"]
                kmag = x["Kmag"]
                vmag = x["Vmag"]
                bmag = x["Bmag"]
                rmag = x["rmag"]
                imag = x["imag"]

                self.star.append([r, id_star, rec_txt, dec_txt, epos, fmag, of, db, pmra, pmde, jmag, kmag, vmag,
                                  bmag, rmag, imag, rec_star, dec_star])
                name_list.append(str(id_star))
        self.ucac4_combobox.clear()
        self.ucac4_combobox.addItems(name_list)
        self.set_cross_id_button.setEnabled(True)
        self.fill_star(0)

    def fill_star(self, index):
        self.delta_r_label1.setText(str(self.star[index][0]))
        self.raj2000_editline.setText(str(self.star[index][2]))
        self.dej2000_editline.setText(str(self.star[index][3]))
        self.position_error_label1.setText(str(self.star[index][4]))
        self.fmag_editline.setText(str(self.star[index][5]))
        self.of_label1.setText(str(self.star[index][6]))
        self.db_label1.setText(str(self.star[index][7]))
        self.pm_ra_label1.setText(str(self.star[index][8]))
        self.pm_de_label1.setText(str(self.star[index][9]))
        self.j_mag_label1.setText(str(self.star[index][10]))
        self.k_mag_label1.setText(str(self.star[index][11]))
        self.b_mag_label1.setText(str(self.star[index][12]))
        self.v_mag_label1.setText(str(self.star[index][13]))
        self.r_mag_label1.setText(str(self.star[index][14]))
        self.i_mag_label1.setText(str(self.star[index][15]))

    def ucac_changed(self):
        star_index = self.ucac4_combobox.currentIndex()
        self.fill_star(star_index)

    def set_cross_id(self):
        try:
            star_index = self.ucac4_combobox.currentIndex()
            new_ucac = str(self.star[star_index][1])
            star_index_in_main_file = self.step_main_form.stars.star_index(self.step_main_form.star_detail.name())
            self.step_main_form.stars.stars[star_index_in_main_file].change_ucac4(new_ucac)
            self.step_main_form.ucac4_button.setText("UCAC4 " + new_ucac)
            current_row = self.step_main_form.objects_table.currentRow()
            self.step_main_form.objects_table.setItem(current_row, 6,
                                                      QtWidgets.QTableWidgetItem(new_ucac))
            self.step_main_form.star_detail.change_ucac4(new_ucac)
            self.step_main_form.filtered_stars.stars[current_row].change_ucac4(new_ucac)
        except:
            pass