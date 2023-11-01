from PyQt5 import QtWidgets                        # , QtCore, QtGui
from coordinate import *
from astroquery.vizier import Vizier
                                                  # from astropy.coordinates import Angle
import astropy.coordinates as coord
import astropy.units as u


class USNOWindow(QtWidgets.QWidget):

    def __init__(self, *args,**kvargs):
        super(USNOWindow, self).__init__(*args, **kvargs)

        self.star = []
        self.setWindowTitle("USNO B1.0 Catalogue Information")
        main_layout = QtWidgets.QVBoxLayout()
        self.setLayout(main_layout)

        ucac4_label = QtWidgets.QLabel("USNO B1.0 identifier: ")
        self.ucac4_combobox = QtWidgets.QComboBox()

        header_layout = QtWidgets.QHBoxLayout()
        header_layout.addWidget(ucac4_label)
        header_layout.addWidget(self.ucac4_combobox)

        self.set_cross_id_button = QtWidgets.QPushButton("Choose the correct cross identification")
        delta_r_label = QtWidgets.QLabel("Radius:")
        raj2000_label = QtWidgets.QLabel("RA eq.2000:")
        dej2000_label = QtWidgets.QLabel("DE eq.2000:")
        position_rec_error_label = QtWidgets.QLabel("RA pos.err(mas):")
        position_dec_error_label = QtWidgets.QLabel("DE pos.err(mas):")
        epoch_label = QtWidgets.QLabel("Epoch (yr):")
        pm_ra_label = QtWidgets.QLabel("Proper motion in RA")
        pm_de_label = QtWidgets.QLabel("Proper motion in DE")
        b1_mag_label = QtWidgets.QLabel("B1 magnitude:")
        r1_mag_label = QtWidgets.QLabel("R1 magnitude:")
        b2_mag_label = QtWidgets.QLabel("B2 magnitude:")
        r2_mag_label = QtWidgets.QLabel("R2 magnitude:")
        i_mag_label = QtWidgets.QLabel("I magnitude:")

        self.delta_r_label1 = QtWidgets.QLabel("")
        self.raj2000_label1 = QtWidgets.QLabel("")
        self.dej2000_label1 = QtWidgets.QLabel("")
        self.position_rec_error_label1 = QtWidgets.QLabel("")
        self.position_dec_error_label1 = QtWidgets.QLabel("")
        self.epoch_label1 = QtWidgets.QLabel("")
        self.pm_ra_label1 = QtWidgets.QLabel("")
        self.pm_de_label1 = QtWidgets.QLabel("")
        self.b1_mag_label1 = QtWidgets.QLabel("")
        self.r1_mag_label1 = QtWidgets.QLabel("")
        self.b2_mag_label1 = QtWidgets.QLabel("")
        self.r2_mag_label1 = QtWidgets.QLabel("")
        self.i_mag_label1 = QtWidgets.QLabel("")

        info_groupbox = QtWidgets.QGroupBox("USNO B1.0 information")
        info_layout = QtWidgets.QFormLayout()
        info_groupbox.setLayout(info_layout)

        info_layout.addRow(delta_r_label, self.delta_r_label1)
        info_layout.addRow(raj2000_label, self.raj2000_label1)
        info_layout.addRow(dej2000_label, self.dej2000_label1)
        info_layout.addRow(position_rec_error_label, self.position_rec_error_label1)
        info_layout.addRow(position_dec_error_label, self.position_dec_error_label1)
        info_layout.addRow(epoch_label, self.epoch_label1)
        info_layout.addRow(pm_ra_label, self.pm_ra_label1)
        info_layout.addRow(pm_de_label, self.pm_de_label1)
        info_layout.addRow(b1_mag_label, self.b1_mag_label1)
        info_layout.addRow(r1_mag_label, self.r1_mag_label1)
        info_layout.addRow(b2_mag_label,self.b2_mag_label1)
        info_layout.addRow(r2_mag_label, self.r2_mag_label1)
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
        agn = Vizier(catalog="I/284", columns=["*"]).query_constraints(USNO_B1_0=cross_id)[0]
        for x in agn:
            id_star = x["USNO-B1.0"]
            rec_star = x["RAJ2000"]
            dec_star = x["DEJ2000"]
            rec_txt = coordinate_to_text(radians(float(rec_star)), coordinate_format="hours", delimiters=("h ", "m ", 's'),
                                         decimal_numbers=3)
            dec_txt = coordinate_to_text(radians(float(dec_star)), coordinate_format="degree", delimiters=("° ", "m ", 's'),
                                         decimal_numbers=3)
            eraj2000 = x["e_RAJ2000"]
            edej2000 = x["e_DEJ2000"]
            epoch = x["Epoch"]
            pmra = x["pmRA"]
            pmde = x["pmDE"]
            b1mag = x["B1mag"]
            r1mag = x["R1mag"]
            b2mag = x["B2mag"]
            r2mag = x["R2mag"]
            imag = x["Imag"]

            self.star = [["", id_star, rec_txt, dec_txt, eraj2000, edej2000, epoch, pmra, pmde, b1mag, r1mag, b2mag,
                          r2mag, imag, rec_star, dec_star]]
            self.ucac4_combobox.clear()
            self.ucac4_combobox.addItem(str(id_star))
            self.set_cross_id_button.setEnabled(False)
            self.fill_star(0)

    def download_data_coor(self, coor):
        self.star.clear()
        rec = degrees(coor.rektascenze())
        dec = degrees(coor.deklinace())
        v = Vizier(columns=["*", "+_r"], catalog="I/284")
        a = coord.SkyCoord(ra=rec, dec=dec, unit=(u.deg, u.deg))
        result = v.query_region(a, radius="10s")
        name_list = []
        for y in result:
            for x in y:
                r = x["_r"]
                id_star = x["USNO-B1.0"]
                rec_star = x["RAJ2000"]
                dec_star = x["DEJ2000"]
                rec_txt = coordinate_to_text(radians(float(rec_star)), coordinate_format="hours",
                                             delimiters=("h ", "m ", 's'),
                                             decimal_numbers=3)
                dec_txt = coordinate_to_text(radians(float(dec_star)), coordinate_format="degree",
                                             delimiters=("° ", "m ", 's'),
                                             decimal_numbers=3)
                eraj2000 = x["e_RAJ2000"]
                edej2000 = x["e_DEJ2000"]
                epoch = x["Epoch"]
                pmra = x["pmRA"]
                pmde = x["pmDE"]
                b1mag = x["B1mag"]
                r1mag = x["R1mag"]
                b2mag = x["B2mag"]
                r2mag = x["R2mag"]
                imag = x["Imag"]

                self.star.append([r, id_star, rec_txt, dec_txt, eraj2000, edej2000, epoch, pmra, pmde, b1mag, r1mag,
                                  b2mag, r2mag, imag, rec_star, dec_star])
                name_list.append(str(id_star))
        self.ucac4_combobox.clear()
        self.ucac4_combobox.addItems(name_list)
        self.set_cross_id_button.setEnabled(True)
        self.fill_star(0)

    def fill_star(self, index):
        self.delta_r_label1.setText(str(self.star[index][0]))
        self.raj2000_label1.setText(str(self.star[index][2]))
        self.dej2000_label1.setText(str(self.star[index][3]))
        self.position_rec_error_label1.setText(str(self.star[index][4]))
        self.position_dec_error_label1.setText(str(self.star[index][4]))
        self.epoch_label1.setText(str(self.star[index][6]))
        self.pm_ra_label1.setText(str(self.star[index][8]))
        self.pm_de_label1.setText(str(self.star[index][9]))
        self.b1_mag_label1.setText(str(self.star[index][10]))
        self.r1_mag_label1.setText(str(self.star[index][11]))
        self.b2_mag_label1.setText(str(self.star[index][12]))
        self.r2_mag_label1.setText(str(self.star[index][14]))
        self.i_mag_label1.setText(str(self.star[index][15]))

    def ucac_changed(self):
        star_index = self.ucac4_combobox.currentIndex()
        self.fill_star(star_index)

    def set_cross_id(self):
        try:
            star_index = self.ucac4_combobox.currentIndex()
            new_ucac = str(self.star[star_index][1])
            star_index_in_main_file = self.step_main_form.stars.star_index(self.step_main_form.star_detail.name())
            self.step_main_form.stars.stars[star_index_in_main_file].change_usnob1(new_ucac)
            self.step_main_form.usnob1_button.setText("USBO B1.0 " + new_ucac)
            current_row = self.step_main_form.objects_table.currentRow()
            self.step_main_form.objects_table.setItem(current_row, 7,
                                                      QtWidgets.QTableWidgetItem(new_ucac))
            self.step_main_form.star_detail.change_usnob1(new_ucac)
            self.step_main_form.filtered_stars.stars[current_row].change_usnob1(new_ucac)
        except:
            pass