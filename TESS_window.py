from PyQt5 import QtWidgets, QtCore, QtGui
from coordinate import *
from astroquery.vizier import Vizier
from astropy.coordinates import Angle
import astropy.coordinates as coord
import astropy.units as u
from PyQt5.QtCore import QUrl
from PyQt5.QtGui import QDesktopServices
import lightkurve as lk
import warnings
from astropy.utils.exceptions import AstropyWarning



class TESSWindow(QtWidgets.QWidget):

    def __init__(self, *args,**kvargs):
        super(TESSWindow, self).__init__(*args, **kvargs)

        self.star = []
        self.setWindowTitle("TESS Catalogue Information")
        main_layout = QtWidgets.QVBoxLayout()
        self.setLayout(main_layout)

        ucac4_label = QtWidgets.QLabel("TESS Identifier: TIC")
        self.ucac4_combobox = QtWidgets.QComboBox()

        header_layout = QtWidgets.QHBoxLayout()
        header_layout.addWidget(ucac4_label)
        header_layout.addWidget(self.ucac4_combobox)

        self.set_cross_id_button = QtWidgets.QPushButton("Choose cross id.")

        header_layout.addWidget(self.set_cross_id_button)

        delta_r_label = QtWidgets.QLabel("Radius:")

        #tic_label = QtWidgets.QLabel("TESS Input Catalog identifier:")
        raj2000_label = QtWidgets.QLabel("Right Ascension (J2000):")
        dej2000_label = QtWidgets.QLabel("Declination (J2000):")
        tyc_label = QtWidgets.QLabel("Tycho2 Identifier:")
        ucac4_label = QtWidgets.QLabel("UCAC4 Identifier:")
        mass2_label = QtWidgets.QLabel("2MASS Identifier:")
        gaia_label = QtWidgets.QLabel("GAIA DR2 Identifier:")
        s_g_label = QtWidgets.QLabel("Object Type ('STAR' or 'EXTENDED'):")
        ref_label = QtWidgets.QLabel("The source of the object in the TIC:")
        pmra_label = QtWidgets.QLabel("Proper Motion in Right Ascension:")
        e_pmra_label = QtWidgets.QLabel("Uncertainty in pmRA:")
        pmde_label = QtWidgets.QLabel("Proper Motion in Declination:")
        e_pmde_label = QtWidgets.QLabel("Uncertainty in pmDE:")
        r_pm_label = QtWidgets.QLabel("Source of the Proper Motion:")
        teff_label = QtWidgets.QLabel("Effective Temperature:")
        s_teff_label = QtWidgets.QLabel("Uncertainty in Teff:")
        logg_label = QtWidgets.QLabel("log of the Surface Gravity:")
        s_logg_label = QtWidgets.QLabel("Uncertainty in logg:")
        m_h_label = QtWidgets.QLabel(" Metallicity (M/H):")
        e_m_h_label = QtWidgets.QLabel("Uncertainty in [M/H] (e_M/H):")
        rad_label = QtWidgets.QLabel("Radius(R Sun)")
        s_rad_label = QtWidgets.QLabel("Uncertainty in Rad:")
        mass_label = QtWidgets.QLabel("Mass(M Sun:")
        s_mass_label = QtWidgets.QLabel("Uncertainty in Mass:")
        lclass_label = QtWidgets.QLabel("Luminosity Class:")
        dist_label = QtWidgets.QLabel("Distance:")
        s_dist_label = QtWidgets.QLabel("Uncertainty in Dist:")
        ncont_label = QtWidgets.QLabel('Number of contaminants found within 10":')
        rcont_label = QtWidgets.QLabel("Contamination Ratio:")
        neg_e_mass_label = QtWidgets.QLabel("Negative error for Mass:")
        pos_e_mass_label = QtWidgets.QLabel("Positive error for Mass:")
        neg_e_rad_label = QtWidgets.QLabel("Negative error for Rad:")
        pos_e_rad_label = QtWidgets.QLabel("Positive error for Rad:")
        neg_e_logg_label = QtWidgets.QLabel("Negative error for Surface Gravity:")
        pos_e_logg_label = QtWidgets.QLabel("Positive error for Surface Gravity:")
        neg_e_dist_label = QtWidgets.QLabel("Negative Error for Dist:")
        pos_e_dist_label = QtWidgets.QLabel("Positive Error for Dist:")
        r_dist_label = QtWidgets.QLabel("Source of distance:")
        neg_e_teff_label = QtWidgets.QLabel("Negative error for Teff:")
        pos_e_teff_label = QtWidgets.QLabel("Positive error for Teff:")
        r_teff_label = QtWidgets.QLabel("Source of Teff:")
        e_raj2000_label = QtWidgets.QLabel("Error in RAdeg:")
        e_dej2000_label = QtWidgets.QLabel("Error in DEdeg:")
        raodeg_label = QtWidgets.QLabel("RA from original catalog:")
        deodeg_label = QtWidgets.QLabel("Dec from original catalog:")
        e_raodeg_label = QtWidgets.QLabel("RA error as given in original catalog:")
        e_deodeg_label = QtWidgets.QLabel("DEC error as given in original catalog:")
        sloan_label = QtWidgets.QLabel("Display the SDSS data for this object URL:")

        self.delta_r_label = QtWidgets.QLabel("")
        self.tic_label = QtWidgets.QLabel("")
        self.raj2000_label = QtWidgets.QLabel("")
        self.dej2000_label = QtWidgets.QLabel("")
        self.tyc_label = QtWidgets.QLabel("")
        self.ucac4_label = QtWidgets.QLabel("")
        self.mass2_label = QtWidgets.QLabel("")
        self.gaia_label = QtWidgets.QLabel("")
        self.s_g_label = QtWidgets.QLabel("")
        self.ref_label = QtWidgets.QLabel("")
        self.pmra_label = QtWidgets.QLabel("")
        self.e_pmra_label = QtWidgets.QLabel("")
        self.pmde_label = QtWidgets.QLabel("")
        self.e_pmde_label = QtWidgets.QLabel("")
        self.r_pm_label = QtWidgets.QLabel("")
        self.teff_label = QtWidgets.QLabel("")
        self.s_teff_label = QtWidgets.QLabel("")
        self.logg_label = QtWidgets.QLabel("")
        self.s_logg_label = QtWidgets.QLabel("")
        self.m_h_label = QtWidgets.QLabel("")
        self.e_m_h_label = QtWidgets.QLabel("")
        self.rad_label = QtWidgets.QLabel("")
        self.s_rad_label = QtWidgets.QLabel("")
        self.mass_label = QtWidgets.QLabel("")
        self.s_mass_label = QtWidgets.QLabel("")
        self.lclass_label = QtWidgets.QLabel("")
        self.dist_label = QtWidgets.QLabel("")
        self.s_dist_label = QtWidgets.QLabel("")
        self.ncont_label = QtWidgets.QLabel("")
        self.rcont_label = QtWidgets.QLabel("")
        self.neg_e_mass_label = QtWidgets.QLabel("")
        self.pos_e_mass_label = QtWidgets.QLabel("")
        self.neg_e_rad_label = QtWidgets.QLabel("")
        self.pos_e_rad_label = QtWidgets.QLabel("")
        self.neg_e_logg_label = QtWidgets.QLabel("")
        self.pos_e_logg_label = QtWidgets.QLabel("")
        self.neg_e_dist_label = QtWidgets.QLabel("")
        self.pos_e_dist_label = QtWidgets.QLabel("")
        self.r_dist_label = QtWidgets.QLabel("")
        self.neg_e_teff_label = QtWidgets.QLabel("")
        self.pos_e_teff_label = QtWidgets.QLabel("")
        self.r_teff_label = QtWidgets.QLabel("")
        self.e_raj2000_label = QtWidgets.QLabel("")
        self.e_dej2000_label = QtWidgets.QLabel("")
        self.raodeg_label = QtWidgets.QLabel("")
        self.deodeg_label = QtWidgets.QLabel("")
        self.e_raodeg_label = QtWidgets.QLabel("")
        self.e_deodeg_label = QtWidgets.QLabel("")
        self.sloan_label = QtWidgets.QPushButton("")

        self.tess_sectors_textedit = QtWidgets.QTextEdit("")
        self.tess_sectors_textedit.setFixedHeight(60)
        self.tess_sectors_pushbutton = QtWidgets.QPushButton("Available TESS sectors")



        info_groupbox = QtWidgets.QGroupBox("TESS information")
        info_layout = QtWidgets.QGridLayout()
        info_groupbox.setLayout(info_layout)

        info1_groupbox = QtWidgets.QGroupBox("column 1")
        info1_layout = QtWidgets.QFormLayout()
        info1_groupbox.setLayout(info1_layout)

        info2_groupbox = QtWidgets.QGroupBox("column 2")
        info2_layout = QtWidgets.QFormLayout()
        info2_groupbox.setLayout(info2_layout)

        info3_groupbox = QtWidgets.QGroupBox("TESS sectors")
        info3_layout = QtWidgets.QVBoxLayout()
        info3_groupbox.setLayout(info3_layout)

        info_layout.addWidget(info1_groupbox, 0, 0, 2, 1)
        info_layout.addWidget(info2_groupbox, 0, 1)
        info_layout.addWidget(info3_groupbox, 1, 1)

        info1_layout.addRow(delta_r_label, self.delta_r_label)
        info1_layout.addRow(raj2000_label, self.raj2000_label)
        info1_layout.addRow(dej2000_label, self.dej2000_label)
        info1_layout.addRow(tyc_label, self.tyc_label)
        info1_layout.addRow(ucac4_label, self.ucac4_label)
        info1_layout.addRow(mass2_label, self.mass2_label)
        info1_layout.addRow(gaia_label, self.gaia_label)
        info1_layout.addRow(s_g_label, self.s_g_label)
        info1_layout.addRow(ref_label, self.ref_label)
        info1_layout.addRow(pmra_label, self.pmra_label)
        info1_layout.addRow(e_pmra_label, self.e_pmra_label)
        info1_layout.addRow(pmde_label, self.pmde_label)
        info1_layout.addRow(e_pmde_label, self.e_pmde_label)
        info1_layout.addRow(r_pm_label, self.r_pm_label)
        info1_layout.addRow(teff_label, self.teff_label)
        info1_layout.addRow(s_teff_label, self.s_teff_label)
        info1_layout.addRow(logg_label, self.logg_label)
        info1_layout.addRow(s_logg_label, self.s_logg_label)
        info1_layout.addRow(m_h_label, self.m_h_label)
        info1_layout.addRow(e_m_h_label, self.e_m_h_label)
        info1_layout.addRow(rad_label, self.rad_label)
        info1_layout.addRow(s_rad_label, self.s_rad_label)
        info1_layout.addRow(mass_label, self.mass_label)
        info1_layout.addRow(s_mass_label, self.s_mass_label)
        info1_layout.addRow(lclass_label, self.lclass_label)
        info1_layout.addRow(dist_label, self.dist_label)
        info1_layout.addRow(s_dist_label, self.s_dist_label)
        info2_layout.addRow(ncont_label, self.ncont_label)
        info2_layout.addRow(rcont_label, self.rcont_label)
        info2_layout.addRow(neg_e_mass_label, self.neg_e_mass_label)
        info2_layout.addRow(pos_e_mass_label, self.pos_e_mass_label)
        info2_layout.addRow(neg_e_rad_label, self.neg_e_rad_label)
        info2_layout.addRow(pos_e_rad_label, self.pos_e_rad_label)
        info2_layout.addRow(neg_e_logg_label, self.neg_e_logg_label)
        info2_layout.addRow(pos_e_logg_label, self.pos_e_logg_label)
        info2_layout.addRow(neg_e_dist_label, self.neg_e_dist_label)
        info2_layout.addRow(pos_e_dist_label, self.pos_e_dist_label)
        info2_layout.addRow(r_dist_label, self.r_dist_label)
        info2_layout.addRow(neg_e_teff_label, self.neg_e_teff_label)
        info2_layout.addRow(pos_e_teff_label, self.pos_e_teff_label)
        info2_layout.addRow(r_teff_label, self.r_teff_label)
        info2_layout.addRow(e_raj2000_label, self.e_raj2000_label)
        info2_layout.addRow(e_dej2000_label, self.e_dej2000_label)
        info2_layout.addRow(raodeg_label, self.raodeg_label)
        info2_layout.addRow(deodeg_label, self.deodeg_label)
        info2_layout.addRow(e_raodeg_label, self.e_raodeg_label)
        info2_layout.addRow(e_deodeg_label, self.e_deodeg_label)
        info3_layout.addWidget(self.tess_sectors_pushbutton)
        info3_layout.addWidget(self.tess_sectors_textedit)


        header_layout.addStretch()
        header_layout.addWidget(sloan_label)
        header_layout.addWidget(self.sloan_label)

        main_layout.addLayout(header_layout)
        #main_layout.addWidget(self.url_label)
        main_layout.addWidget(info_groupbox)

    def setup(self):
        from step_application import root
        self.step_main_form = root.step_main_form
        self.ucac4_combobox.currentTextChanged.connect(self.ucac_changed)
        self.set_cross_id_button.clicked.connect(self.set_cross_id)
        #self.sloan_label.clicked.connect(self.call_url)
        self.tess_sectors_pushbutton.clicked.connect(self.give_sectors)

    def give_sectors(self):
        alfa = coordinate_to_text(self.step_main_form.star_detail.coordinate().rektascenze(), coordinate_format="hours")
        delta = coordinate_to_text(self.step_main_form.star_detail.coordinate().deklinace(), coordinate_format="degree")
        search_results = lk.search_tesscut(alfa + " " + delta)
        sectors = []
        for tpfs in search_results:
            sectors.append(str(tpfs.mission[0])[12:14])
        sectors_text = ",".join(sectors)
        self.tess_sectors_textedit.setText(sectors_text)

    def download_data_coor(self, coor):
        self.star.clear()
        self.tess_sectors_textedit.clear()
        rec = degrees(coor.rektascenze())
        dec = degrees(coor.deklinace())
        v = Vizier(columns=["+_r", "*"], catalog="IV/38/tic")
        a = coord.SkyCoord(ra=rec, dec=dec, unit=(u.deg, u.deg))
        warnings.simplefilter("ignore", category=AstropyWarning)
        result = v.query_region(a, radius="10s")
        name_list = []
        for y in result:
            for x in y:
                r = x["_r"]
                tic = x["TIC"]
                rec_star = x["RAJ2000"]
                dec_star = x["DEJ2000"]
                tyc = x["TYC"]
                ucac4 = x["UCAC4"]
                mass2 = x["_2MASS"]
                gaia = x["GAIA"]
                s_g = x["S_G"]
                ref = x["Ref"]
                pmra = x["pmRA"]
                e_pmra = x["e_pmRA"]
                pmde = x["pmDE"]
                e_pmde = x["e_pmDE"]
                r_pm = x["r_pm"]
                teff = x["Teff"]
                s_teff = x["s_Teff"]
                logg = x["logg"]
                s_logg = x["s_logg"]
                m_h = x["__M_H_"]
                e_m_h = x["e__M_H_"]
                rad = x["Rad"]
                s_rad = x["s_Rad"]
                mass = x["Mass"]
                s_mass = x["s_Mass"]
                lclass = x["LClass"]
                dist = x["Dist"]
                s_dist = x["s_Dist"]
                ncont = x["Ncont"]
                rcont = x["Rcont"]
                neg_e_mass = x["e_Mass"]
                pos_e_mass = x["E_Mass"]
                neg_e_rad = x["e_Rad"]
                pos_e_rad = x["E_Rad"]
                neg_e_logg = x["e_logg"]
                pos_e_logg = x["E_logg"]
                neg_e_dist = x["e_Dist"]
                pos_e_dist = x["E_Dist"]
                r_dist = x["r_Dist"]
                neg_e_teff = x["e_Teff"]
                pos_e_teff = x["E_Teff"]
                r_teff = x["r_Teff"]
                e_raj2000 = x["e_RAJ2000"]
                e_dej2000 = x["e_DEJ2000"]
                raodeg = x["RAOdeg"]
                deodeg = x["DEOdeg"]
                e_raodeg = x["e_RAOdeg"]
                e_deodeg = x["e_DEOdeg"]
                sloan = x["Sloan"]
                rec_txt = coordinate_to_text(radians(float(rec_star)), coordinate_format="hours",
                                             delimiters=("h ", "m ", 's'),
                                             decimal_numbers=3)
                dec_txt = coordinate_to_text(radians(float(dec_star)), coordinate_format="degree",
                                             delimiters=("° ", "m ", 's'),
                                             decimal_numbers=3)

                self.star.append([r, tic, rec_txt, dec_txt, tyc, ucac4, mass2, gaia, s_g, ref, pmra, e_pmra, pmde,
                                  e_pmde, r_pm, teff, s_teff, logg, s_logg, m_h, e_m_h, rad, s_rad, mass, s_mass,
                                  lclass, dist, s_dist, ncont, rcont, neg_e_mass, pos_e_mass, neg_e_rad, pos_e_rad,
                                  neg_e_logg, pos_e_logg, neg_e_dist, pos_e_dist, r_dist, neg_e_teff, pos_e_teff,
                                  r_teff, e_raj2000, e_dej2000, raodeg, deodeg, e_raodeg, e_deodeg, sloan, rec_star,
                                  dec_star])
                name_list.append(str(tic))
        if name_list:
            self.ucac4_combobox.clear()
            self.ucac4_combobox.addItems(name_list)
            self.set_cross_id_button.setEnabled(True)
            if ("a" + self.step_main_form.star_detail.tess()).strip() == "a":
                self.fill_star(0)
            else:
                if self.step_main_form.star_detail.tess() in name_list:
                    index_in_name_list = name_list.index(self.step_main_form.star_detail.tess())
                    self.ucac4_combobox.setCurrentIndex(index_in_name_list)
                    self.fill_star(index_in_name_list)

                else:
                    self.fill_star(0)
        else:
            self.ucac4_combobox.clear()
            self.delta_r_label = QtWidgets.QLabel("")
            self.tic_label = QtWidgets.QLabel("")
            self.raj2000_label = QtWidgets.QLabel("")
            self.dej2000_label = QtWidgets.QLabel("")
            self.tyc_label = QtWidgets.QLabel("")
            self.ucac4_label = QtWidgets.QLabel("")
            self.mass2_label = QtWidgets.QLabel("")
            self.gaia_label = QtWidgets.QLabel("")
            self.s_g_label = QtWidgets.QLabel("")
            self.ref_label = QtWidgets.QLabel("")
            self.pmra_label = QtWidgets.QLabel("")
            self.e_pmra_label = QtWidgets.QLabel("")
            self.pmde_label = QtWidgets.QLabel("")
            self.e_pmde_label = QtWidgets.QLabel("")
            self.r_pm_label = QtWidgets.QLabel("")
            self.teff_label = QtWidgets.QLabel("")
            self.s_teff_label = QtWidgets.QLabel("")
            self.logg_label = QtWidgets.QLabel("")
            self.s_logg_label = QtWidgets.QLabel("")
            self.m_h_label = QtWidgets.QLabel("")
            self.e_m_h_label = QtWidgets.QLabel("")
            self.rad_label = QtWidgets.QLabel("")
            self.s_rad_label = QtWidgets.QLabel("")
            self.mass_label = QtWidgets.QLabel("")
            self.s_mass_label = QtWidgets.QLabel("")
            self.lclass_label = QtWidgets.QLabel("")
            self.dist_label = QtWidgets.QLabel("")
            self.s_dist_label = QtWidgets.QLabel("")
            self.ncont_label = QtWidgets.QLabel("")
            self.rcont_label = QtWidgets.QLabel("")
            self.neg_e_mass_label = QtWidgets.QLabel("")
            self.pos_e_mass_label = QtWidgets.QLabel("")
            self.neg_e_rad_label = QtWidgets.QLabel("")
            self.pos_e_rad_label = QtWidgets.QLabel("")
            self.neg_e_logg_label = QtWidgets.QLabel("")
            self.pos_e_logg_label = QtWidgets.QLabel("")
            self.neg_e_dist_label = QtWidgets.QLabel("")
            self.pos_e_dist_label = QtWidgets.QLabel("")
            self.r_dist_label = QtWidgets.QLabel("")
            self.neg_e_teff_label = QtWidgets.QLabel("")
            self.pos_e_teff_label = QtWidgets.QLabel("")
            self.r_teff_label = QtWidgets.QLabel("")
            self.e_raj2000_label = QtWidgets.QLabel("")
            self.e_dej2000_label = QtWidgets.QLabel("")
            self.raodeg_label = QtWidgets.QLabel("")
            self.deodeg_label = QtWidgets.QLabel("")
            self.e_raodeg_label = QtWidgets.QLabel("")
            self.e_deodeg_label = QtWidgets.QLabel("")
            self.sloan_label = QtWidgets.QPushButton("")

    def fill_star(self, index):
        self.delta_r_label.setText((str(self.star[index][0])))
        self.raj2000_label.setText(str(self.star[index][2]))
        self.dej2000_label.setText(str(self.star[index][3]))
        self.tyc_label.setText(str(self.star[index][4]))
        self.ucac4_label.setText(str(self.star[index][5]))
        self.mass2_label.setText(str(self.star[index][6]))
        self.gaia_label.setText(str(self.star[index][7]))
        self.s_g_label.setText(str(self.star[index][8]))
        self.ref_label.setText(str(self.star[index][9]))
        self.pmra_label.setText(str(self.star[index][10]))
        self.e_pmra_label.setText(str(self.star[index][11]))
        self.pmde_label.setText(str(self.star[index][12]))
        self.e_pmde_label.setText(str(self.star[index][13]))
        self.r_pm_label.setText(str(self.star[index][14]))
        self.teff_label.setText(str(self.star[index][15]))
        self.s_teff_label.setText(str(self.star[index][16]))
        self.logg_label.setText(str(self.star[index][17]))
        self.s_logg_label.setText(str(self.star[index][18]))
        self.m_h_label.setText(str(self.star[index][19]))
        self.e_m_h_label.setText(str(self.star[index][20]))
        self.rad_label.setText(str(self.star[index][21]))
        self.s_rad_label.setText(str(self.star[index][22]))
        self.mass_label.setText(str(self.star[index][23]))
        self.s_mass_label.setText(str(self.star[index][24]))
        self.lclass_label.setText(str(self.star[index][25]))
        self.dist_label.setText(str(self.star[index][26]))
        self.s_dist_label.setText(str(self.star[index][27]))
        self.ncont_label.setText(str(self.star[index][28]))
        self.rcont_label.setText(str(self.star[index][29]))
        self.neg_e_mass_label.setText(str(self.star[index][30]))
        self.pos_e_mass_label.setText(str(self.star[index][31]))
        self.neg_e_rad_label.setText(str(self.star[index][32]))
        self.pos_e_rad_label.setText(str(self.star[index][33]))
        self.neg_e_logg_label.setText(str(self.star[index][34]))
        self.pos_e_logg_label.setText(str(self.star[index][35]))
        self.neg_e_dist_label.setText(str(self.star[index][36]))
        self.pos_e_dist_label.setText(str(self.star[index][37]))
        self.r_dist_label.setText(str(self.star[index][38]))
        self.neg_e_teff_label.setText(str(self.star[index][39]))
        self.pos_e_teff_label.setText(str(self.star[index][40]))
        self.r_teff_label.setText(str(self.star[index][41]))
        self.e_raj2000_label.setText(str(self.star[index][42]))
        self.e_dej2000_label.setText(str(self.star[index][43]))
        self.raodeg_label.setText(str(self.star[index][44]))
        self.deodeg_label.setText(str(self.star[index][45]))
        self.e_raodeg_label.setText(str(self.star[index][46]))
        self.e_deodeg_label.setText(str(self.star[index][47]))
        self.sloan_label.setText(str(self.star[index][48]))

    def ucac_changed(self):
        star_index = self.ucac4_combobox.currentIndex()
        self.fill_star(star_index)

    def set_cross_id(self):
        try:
            star_index = self.ucac4_combobox.currentIndex()
            new_ucac = str(self.star[star_index][1])
            star_index_in_main_file = self.step_main_form.stars.star_index(self.step_main_form.star_detail.name())
            self.step_main_form.stars.stars[star_index_in_main_file].change_tess(new_ucac)
            self.step_main_form.tess_object_button.setText("TIC " + new_ucac)
            current_row = self.step_main_form.objects_table.currentRow()
            self.step_main_form.objects_table.setItem(current_row, 11,
                                                      QtWidgets.QTableWidgetItem(new_ucac))
            self.step_main_form.star_detail.change_tess(new_ucac)
            self.step_main_form.filtered_stars.stars[current_row].change_tess(new_ucac)
        except:
            pass

    def call_url(self):
        caled_url = self.sloan_label.text()
        QDesktopServices.openUrl(QUrl(caled_url))
