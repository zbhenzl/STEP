from PyQt5 import QtWidgets, QtCore, QtGui
from coordinate import *
from astroquery.vizier import Vizier
from astropy.coordinates import Angle
import astropy.coordinates as coord
import astropy.units as u
from PyQt5.QtCore import QUrl
from PyQt5.QtGui import QDesktopServices
from import_star import mistake

class ASASWindow(QtWidgets.QWidget):

    def __init__(self, *args,**kvargs):
        super(ASASWindow, self).__init__(*args, **kvargs)

        self.star = []
        self.setWindowTitle("ASAS-SN Catalogue Information")
        main_layout = QtWidgets.QVBoxLayout()
        self.setLayout(main_layout)
        self.is_it_import = False

        self.ucac4_checkbox = QtWidgets.QCheckBox("ASASSN-V")
        self.ucac4_combobox = QtWidgets.QComboBox()
        self.ucac4_combobox.setFixedWidth(200)

        header_layout = QtWidgets.QHBoxLayout()
        header_layout.addWidget(self.ucac4_checkbox)
        header_layout.addWidget(self.ucac4_combobox)

        self.set_cross_id_button = QtWidgets.QPushButton("Choose cross id.")

        header_layout.addWidget(self.set_cross_id_button)

        delta_r_label = QtWidgets.QLabel("Radius:")

        recno_label = QtWidgets.QLabel("Record number assigned by the VizieR team:")
        id_star_label = QtWidgets.QLabel("Internal identifier:")
        oname_label = QtWidgets.QLabel("Other name˙(meta.id):")
        self.raj2000_checkbox = QtWidgets.QCheckBox("Right ascension in decimal degrees (J2000):")
        self.dej2000_checkbox = QtWidgets.QCheckBox("Declination in decimal degrees (J2000):")
        glon_label = QtWidgets.QLabel("Galactic longitude (l):")
        glat_label = QtWidgets.QLabel("Galactic latitude (b):")
        self.vmag_checkbox = QtWidgets.QCheckBox("Johnson V-band magnitude:")
        self.amp_checkbox = QtWidgets.QCheckBox("Amplitude˙(phot.mag):")
        self.per_checkbox = QtWidgets.QCheckBox("Period˙(time.period):")
        self.type_var_checkbox = QtWidgets.QCheckBox("Variability type:")
        prob_label = QtWidgets.QLabel("Classification probability:")
        lksl_label = QtWidgets.QLabel("LKSL statistic:")
        rfr_label = QtWidgets.QLabel("Random forest (RF) regression value:")
        self.hjd_checkbox = QtWidgets.QCheckBox("Heliocentric Julian Date˙(time.epoch):")
        gaia_label = QtWidgets.QLabel("Gaia DR2 identifier:")
        gmag_label = QtWidgets.QLabel("Gaia G-band magnitude:")
        e_gmag_label = QtWidgets.QLabel("Error on Gmag:")
        bpmag_label = QtWidgets.QLabel("Gaia BP-band magnitude:")
        e_bpmag_label = QtWidgets.QLabel("Error on BPmag:")
        gaia_rpmag_label = QtWidgets.QLabel("Gaia RP-band magnitude:")
        gaia_e_rpmag_label = QtWidgets.QLabel("Error on RPmag:")
        bp_rp_label = QtWidgets.QLabel("BP-RP color index:")
        plx_label = QtWidgets.QLabel(" Gaia DR2 parallax:")
        e_plx_label = QtWidgets.QLabel("Parallax uncertainty:")
        plxerr_label = QtWidgets.QLabel("Parallax over error:")
        pmra_label = QtWidgets.QLabel("Gaia proper motion in right ascension direction:")
        e_pmra_label = QtWidgets.QLabel("Error on pmRA:")
        pmde_label = QtWidgets.QLabel("Gaia proper motion in declination direction:")
        e_pmde_label = QtWidgets.QLabel("Error on pmDE:")
        vt_label = QtWidgets.QLabel("Microturbulent velocity:")
        dist_star_label = QtWidgets.QLabel("Distance:")
        wisea_label = QtWidgets.QLabel("AllWISE identifier:")
        jmag_label = QtWidgets.QLabel("2MASS J-band magnitude:")
        e_jmag_label = QtWidgets.QLabel("Error on the J-band magnitude:")
        hmag_label = QtWidgets.QLabel("2MASS H-band magnitude:")
        e_hmag_label = QtWidgets.QLabel("Error on the H-band magnitude:")
        ksmag_label = QtWidgets.QLabel("2MASS Ks-band magnitude:")
        e_ksmag_label = QtWidgets.QLabel("Error on the Ks-band magnitude:")
        w1mag_label = QtWidgets.QLabel("WISE W1 (3.4um) band magnitude:")
        e_w1mag_label = QtWidgets.QLabel("Error on the W1mag:")
        w2mag_label = QtWidgets.QLabel("WISE W2 (4.6um) band magnitude:")
        e_w2mag_label = QtWidgets.QLabel("Error on W2mag:")
        w3mag_label = QtWidgets.QLabel("WISE W3 (12um) band magnitude:")
        e_w3mag_label = QtWidgets.QLabel("Error on W3mag:")
        w4mag_label = QtWidgets.QLabel("band magnitude:")
        e_w4mag_label = QtWidgets.QLabel("Error on W4mag:")
        self.j_k_checkbox = QtWidgets.QCheckBox("J-K color index:")
        w1_w2_label = QtWidgets.QLabel("W1-W2 color index:")
        w3_w4_label = QtWidgets.QLabel("W3-W4 color index:")
        apass_label = QtWidgets.QLabel("APASS identifier:")
        vmaga_label = QtWidgets.QLabel("APASS Johnson V-band magnitude:")
        e_vmaga_label = QtWidgets.QLabel("Error on VmagA:")
        bmaga_label = QtWidgets.QLabel("APASS Johnson B-band magnitude:")
        e_bmaga_label = QtWidgets.QLabel("Error on BmagA:")
        gpmag_label = QtWidgets.QLabel("APASS g'-band AB magnitude:")
        e_gpmag_label = QtWidgets.QLabel("Error on the g'-band magnitude:")
        rpmag_label = QtWidgets.QLabel("APASS r'-band AB magnitude:")
        e_rpmag_label = QtWidgets.QLabel("Error on the r'-band magnitude:")
        ipmag_label = QtWidgets.QLabel("APASS i'-band AB magnitude:")
        e_ipmag_label = QtWidgets.QLabel("Error on the i'-band magnitude:")
        self.b_v_checkbox = QtWidgets.QCheckBox("B-V color index:")
        e_b_v_label = QtWidgets.QLabel("Reddening E(B-V):")
        ref_label = QtWidgets.QLabel("Reference˙(Note 1):")
        perd_label = QtWidgets.QLabel("Periodic ('false' or 'true'):")
        disc_label = QtWidgets.QLabel("ASAS-SN discovery ('false' or 'true'):")
        url_label = QtWidgets.QLabel("URL:")
        m2_label = QtWidgets.QLabel("Display the 2MASS data:")

        self.delta_r_label = QtWidgets.QLabel("")
        self.recno_label = QtWidgets.QLabel("")
        self.id_star_label = QtWidgets.QLabel("")
        self.oname_label = QtWidgets.QLabel("")
        self.raj2000_label = QtWidgets.QLabel("")
        self.dej2000_label = QtWidgets.QLabel("")
        self.glon_label = QtWidgets.QLabel("")
        self.glat_label = QtWidgets.QLabel("")
        self.vmag_label = QtWidgets.QLabel("")
        self.amp_label = QtWidgets.QLabel("")
        self.per_label = QtWidgets.QLabel("")
        self.type_var_label = QtWidgets.QLabel("")
        self.prob_label = QtWidgets.QLabel("")
        self.lksl_label = QtWidgets.QLabel("")
        self.rfr_label = QtWidgets.QLabel("")
        self.hjd_label = QtWidgets.QLabel("")
        self.gaia_label = QtWidgets.QLabel("")
        self.gmag_label = QtWidgets.QLabel("")
        self.e_gmag_label = QtWidgets.QLabel("")
        self.bpmag_label = QtWidgets.QLabel("")
        self.e_bpmag_label = QtWidgets.QLabel("")
        self.gaia_rpmag_label = QtWidgets.QLabel("")
        self.gaia_e_rpmag_label = QtWidgets.QLabel("")
        self.bp_rp_label = QtWidgets.QLabel("")
        self.plx_label = QtWidgets.QLabel("")
        self.e_plx_label = QtWidgets.QLabel("")
        self.plxerr_label = QtWidgets.QLabel("")
        self.pmra_label = QtWidgets.QLabel("")
        self.e_pmra_label = QtWidgets.QLabel("")
        self.pmde_label = QtWidgets.QLabel("")
        self.e_pmde_label = QtWidgets.QLabel("")
        self.vt_label = QtWidgets.QLabel("")
        self.dist_star_label = QtWidgets.QLabel("")
        self.wisea_label = QtWidgets.QLabel("")
        self.jmag_label = QtWidgets.QLabel("")
        self.e_jmag_label = QtWidgets.QLabel("")
        self.hmag_label = QtWidgets.QLabel("")
        self.e_hmag_label = QtWidgets.QLabel("")
        self.ksmag_label = QtWidgets.QLabel("")
        self.e_ksmag_label = QtWidgets.QLabel("")
        self.w1mag_label = QtWidgets.QLabel("")
        self.e_w1mag_label = QtWidgets.QLabel("")
        self.w2mag_label = QtWidgets.QLabel("")
        self.e_w2mag_label = QtWidgets.QLabel("")
        self.w3mag_label = QtWidgets.QLabel("")
        self.e_w3mag_label = QtWidgets.QLabel("")
        self.w4mag_label = QtWidgets.QLabel("")
        self.e_w4mag_label = QtWidgets.QLabel("")
        self.j_k_label = QtWidgets.QLabel("")
        self.w1_w2_label = QtWidgets.QLabel("")
        self.w3_w4_label = QtWidgets.QLabel("")
        self.apass_label = QtWidgets.QLabel("")
        self.vmaga_label = QtWidgets.QLabel("")
        self.e_vmaga_label = QtWidgets.QLabel("")
        self.bmaga_label = QtWidgets.QLabel("")
        self.e_bmaga_label = QtWidgets.QLabel("")
        self.gpmag_label = QtWidgets.QLabel("")
        self.e_gpmag_label = QtWidgets.QLabel("")
        self.rpmag_label = QtWidgets.QLabel("")
        self.e_rpmag_label = QtWidgets.QLabel("")
        self.ipmag_label = QtWidgets.QLabel("")
        self.e_ipmag_label = QtWidgets.QLabel("")
        self.b_v_label = QtWidgets.QLabel("")
        self.e_b_v_label = QtWidgets.QLabel("")
        self.ref_label = QtWidgets.QLabel("")
        self.perd_label = QtWidgets.QLabel("")
        self.disc_label = QtWidgets.QLabel("")
        self.url_label = QtWidgets.QPushButton("")
        self.url_label.setFixedWidth(280)
        self.m2_label = QtWidgets.QLabel("")

        self.info_groupbox = QtWidgets.QGroupBox("ASAS-SN information")
        info_layout = QtWidgets.QHBoxLayout()
        self.info_groupbox.setLayout(info_layout)

        info1_groupbox = QtWidgets.QGroupBox("column 1")
        info1_layout = QtWidgets.QFormLayout()
        info1_groupbox.setLayout(info1_layout)

        info2_groupbox = QtWidgets.QGroupBox("column 2")
        info2_layout = QtWidgets.QFormLayout()
        info2_groupbox.setLayout(info2_layout)

        info_layout.addWidget(info1_groupbox)
        info_layout.addWidget(info2_groupbox)

        info1_layout.addRow(delta_r_label, self.delta_r_label)
        info1_layout.addRow(recno_label, self.recno_label)
        info1_layout.addRow(id_star_label, self.id_star_label)
        info1_layout.addRow(oname_label, self.oname_label)
        info1_layout.addRow(self.raj2000_checkbox, self.raj2000_label)
        info1_layout.addRow(self.dej2000_checkbox, self.dej2000_label)
        info1_layout.addRow(glon_label, self.glon_label)
        info1_layout.addRow(glat_label, self.glat_label)
        info1_layout.addRow(self.vmag_checkbox, self.vmag_label)
        info1_layout.addRow(self.amp_checkbox, self.amp_label)
        info1_layout.addRow(self.per_checkbox, self.per_label)
        info1_layout.addRow(self.type_var_checkbox, self.type_var_label)
        info1_layout.addRow(prob_label, self.prob_label)
        info1_layout.addRow(lksl_label, self.lksl_label)
        info1_layout.addRow(rfr_label, self.rfr_label)
        info1_layout.addRow(self.hjd_checkbox, self.hjd_label)
        info1_layout.addRow(gaia_label, self.gaia_label)
        info1_layout.addRow(gmag_label, self.gmag_label)
        info1_layout.addRow(e_gmag_label, self.e_gmag_label)
        info1_layout.addRow(bpmag_label, self.bpmag_label)
        info1_layout.addRow(e_bpmag_label, self.e_bpmag_label)
        info1_layout.addRow(gaia_rpmag_label, self.gaia_rpmag_label)
        info1_layout.addRow(gaia_e_rpmag_label, self.gaia_e_rpmag_label)
        info1_layout.addRow(bp_rp_label, self.bp_rp_label)
        info1_layout.addRow(plx_label, self.plx_label)
        info1_layout.addRow(e_plx_label, self.e_plx_label)
        info1_layout.addRow(plxerr_label, self.plxerr_label)
        info1_layout.addRow(pmra_label, self.pmra_label)
        info1_layout.addRow(e_pmra_label, self.e_pmra_label)
        info1_layout.addRow(pmde_label, self.pmde_label)
        info1_layout.addRow(e_pmde_label, self.e_pmde_label)
        info1_layout.addRow(vt_label, self.vt_label)
        info1_layout.addRow(dist_star_label, self.dist_star_label)
        info1_layout.addRow(wisea_label, self.wisea_label)
        info2_layout.addRow(jmag_label, self.jmag_label)
        info2_layout.addRow(e_jmag_label, self.e_jmag_label)
        info2_layout.addRow(hmag_label, self.hmag_label)
        info2_layout.addRow(e_hmag_label, self.e_hmag_label)
        info2_layout.addRow(ksmag_label, self.ksmag_label)
        info2_layout.addRow(e_ksmag_label, self.e_ksmag_label)
        info2_layout.addRow(w1mag_label, self.w1mag_label)
        info2_layout.addRow(e_w1mag_label, self.e_w1mag_label)
        info2_layout.addRow(w2mag_label, self.w2mag_label)
        info2_layout.addRow(e_w2mag_label, self.e_w2mag_label)
        info2_layout.addRow(w3mag_label, self.w3mag_label)
        info2_layout.addRow(e_w3mag_label, self.e_w3mag_label)
        info2_layout.addRow(w4mag_label, self.w4mag_label)
        info2_layout.addRow(e_w4mag_label, self.e_w4mag_label)
        info2_layout.addRow(self.j_k_checkbox, self.j_k_label)
        info2_layout.addRow(w1_w2_label, self.w1_w2_label)
        info2_layout.addRow(w3_w4_label, self.w3_w4_label)
        info2_layout.addRow(apass_label, self.apass_label)
        info2_layout.addRow(vmaga_label, self.vmaga_label)
        info2_layout.addRow(e_vmaga_label, self.e_vmaga_label)
        info2_layout.addRow(bmaga_label, self.bmaga_label)
        info2_layout.addRow(e_bmaga_label, self.e_bmaga_label)
        info2_layout.addRow(gpmag_label, self.gpmag_label)
        info2_layout.addRow(e_gpmag_label, self.e_gpmag_label)
        info2_layout.addRow(rpmag_label, self.rpmag_label)
        info2_layout.addRow(e_rpmag_label, self.e_rpmag_label)
        info2_layout.addRow(ipmag_label, self.ipmag_label)
        info2_layout.addRow(e_ipmag_label, self.e_ipmag_label)
        info2_layout.addRow(self.b_v_checkbox, self.b_v_label)
        info2_layout.addRow(e_b_v_label, self.e_b_v_label)
        info2_layout.addRow(ref_label, self.ref_label)
        info2_layout.addRow(perd_label, self.perd_label)
        info2_layout.addRow(disc_label, self.disc_label)
        info2_layout.addRow(m2_label, self.m2_label)

        header_layout.addStretch()
        header_layout.addWidget(url_label)
        header_layout.addWidget(self.url_label)

        self.import_groupbox = QtWidgets.QGroupBox("Import information - Input coordinates")
        import_layout = QtWidgets.QGridLayout()
        self.import_groupbox.setLayout(import_layout)

        self.sign_combobox = QtWidgets.QComboBox()
        self.sign_combobox.addItems(["+", "-"])

        rec_h_label = QtWidgets.QLabel("h")
        rec_h_label.setFixedWidth(7)
        self.rec_h_spinbox = QtWidgets.QSpinBox()
        self.rec_h_spinbox.setRange(0, 23)

        rec_m_label = QtWidgets.QLabel("m")
        rec_m_label.setFixedWidth(7)
        self.rec_m_spinbox = QtWidgets.QSpinBox()
        self.rec_m_spinbox.setRange(0, 59)

        rec_s_label = QtWidgets.QLabel("s   ")
        rec_s_label.setFixedWidth(20)
        self.rec_s_spinbox = QtWidgets.QDoubleSpinBox()
        self.rec_s_spinbox.setRange(0, 59.99)

        dec_h_label = QtWidgets.QLabel("°")
        dec_h_label.setFixedWidth(7)
        self.dec_h_spinbox = QtWidgets.QSpinBox()
        self.dec_h_spinbox.setRange(-89, 89)

        dec_m_label = QtWidgets.QLabel("m")
        dec_m_label.setFixedWidth(7)
        self.dec_m_spinbox = QtWidgets.QSpinBox()
        self.dec_m_spinbox.setRange(0, 59)

        dec_s_label = QtWidgets.QLabel("s       ")
        dec_s_label.setFixedWidth(25)
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

        import_layout.addWidget(self.check_star_pushbutton, 0, 13)
        import_layout.addWidget(aperture_label, 0, 14)
        import_layout.addWidget(self.aperture_spinbox, 0, 15)

        main_layout.addWidget(self.import_groupbox)
        main_layout.addLayout(header_layout)
        main_layout.addWidget(self.info_groupbox)

        self.import_groupbox.setVisible(False)

    def setup(self):
        from step_application import root
        self.step_main_form = root.step_main_form
        self.ucac4_combobox.currentTextChanged.connect(self.ucac_changed)
        self.set_cross_id_button.clicked.connect(self.set_cross_id)
        self.url_label.clicked.connect(self.call_url)
        self.object_edit_window = root.object_edit_window
        self.check_star_pushbutton.clicked.connect(self.check_star)

    def check_star(self):
        self.info_groupbox.setVisible(True)
        self.url_label.setEnabled(True)
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
        self.url_label.setEnabled(False)
        self.set_cross_id_button.setEnabled(False)
        self.aperture_spinbox.setValue(5)
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
        self.url_label.setEnabled(True)
        self.info_groupbox.setVisible(True)
        self.set_cross_id_button.setEnabled(True)
        self.set_cross_id_button.setText("Choose the correct cross identification")
        self.is_it_import = False

    def download_data_id(self, cross_id: str):
        self.star.clear()
        agn = Vizier(catalog="II/366", columns=["recno", "ID", "ASASSN-V", "OName", "RAJ2000", "DEJ2000", "GLON",
                                                "GLAT", "Vmag", "Amp", "Per", "Type", "Prob", "LKSL", "RFR", "HJD",
                                                "Gaia", "Gmag", "e_Gmag", "BPmag", "e_BPmag", "RPmag", "e_RPmag",
                                                "BP-RP", "Plx", "e_Plx", "PlxErr", "pmRA", "e_pmRA", "pmDE", "e_pmDE",
                                                "Vt", "Dist", "WISEA", "Jmag", "e_Jmag", "Hmag", "e_Hmag", "Ksmag",
                                                "e_Ksmag", "W1mag", "e_W1mag", "W2mag", "e_W2mag", "W3mag", "e_W3mag",
                                                "W4mag", "e_W4mag", "J-K", "W1-W2", "W3-W4", "APASS", "VmagA",
                                                "e_VmagA", "BmagA", "e_BmagA", "gpmag", "e_gpmag", "rpmag", "e_rpmag",
                                                "ipmag", "e_ipmag", "B-V", "E(B-V)", "Ref", "Perd", "Disc", "URL",
                                                "2M"]).query_constraints(ASASSN_V=cross_id)[0]
        for x in agn:
            recno = x["recno"]
            id_star = x["ID"]
            asassn = x["ASASSN-V"]
            oname = x["OName"]
            rec_star = x["RAJ2000"]
            dec_star = x["DEJ2000"]
            rec_txt = coordinate_to_text(radians(float(rec_star)), coordinate_format="hours", delimiters=("h ", "m ", 's'),
                                         decimal_numbers=3)
            dec_txt = coordinate_to_text(radians(float(dec_star)), coordinate_format="degree", delimiters=("° ", "m ", 's'),
                                         decimal_numbers=3)

            glon = x["GLON"]
            glat = x["GLAT"]
            vmag = x["Vmag"]
            amp = x["Amp"]
            per = x["Per"]
            type_var = x["Type"]
            prob = x["Prob"]
            lksl = x["LKSL"]
            rfr = x["RFR"]
            hjd = x["_tab1_15"]
            gaia = x["Gaia"]
            gmag = x["Gmag"]
            e_gmag = x["e_Gmag"]
            bpmag = x["BPmag"]
            e_bpmag = x["e_BPmag"]
            gaia_rpmag = x["RPmag"]
            gaia_e_rpmag = x["e_RPmag"]
            bp_rp = x["BP-RP"]
            plx = x["Plx"]
            e_plx = x["e_Plx"]
            plxerr = x["PlxErr"]
            pmra = x["pmRA"]
            e_pmra = x["e_pmRA"]
            pmde = x["pmDE"]
            e_pmde = x["e_pmDE"]
            vt = x["Vt"]
            dist_star = x["Dist"]
            wisea = x["WISEA"]
            jmag = x["Jmag"]
            e_jmag = x["e_Jmag"]
            hmag = x["Hmag"]
            e_hmag = x["e_Hmag"]
            ksmag = x["Ksmag"]
            e_ksmag = x["e_Ksmag"]
            w1mag = x["W1mag"]
            e_w1mag = x["e_W1mag"]
            w2mag = x["W2mag"]
            e_w2mag = x["e_W2mag"]
            w3mag = x["W3mag"]
            e_w3mag = x["e_W3mag"]
            w4mag = x["W4mag"]
            e_w4mag = x["e_W4mag"]
            j_k = x["J-K"]
            w1_w2 = x["W1-W2"]
            w3_w4 = x["W3-W4"]
            apass = x["APASS"]
            vmaga = x["VmagA"]
            e_vmaga = x["e_VmagA"]
            bmaga = x["BmagA"]
            e_bmaga = x["e_BmagA"]
            gpmag = x["gpmag"]
            e_gpmag = x["e_gpmag"]
            rpmag = x["rpmag"]
            e_rpmag = x["e_rpmag"]
            ipmag = x["ipmag"]
            e_ipmag = x["e_ipmag"]
            b_v = x["B-V"]
            e_b_v = x["E_B-V_"]
            ref = x["Ref"]
            perd = x["Perd"]
            disc = x["Disc"]
            url = x["URL"]
            m2 = x["_2M"]

            self.star = [["", recno, id_star, asassn, oname, rec_txt, dec_txt, glon, glat, vmag, amp, per, type_var,
                          prob, lksl, rfr, hjd, gaia, gmag, e_gmag, bpmag, e_bpmag, gaia_rpmag, gaia_e_rpmag, bp_rp,
                          plx, e_plx, plxerr, pmra, e_pmra, pmde, e_pmde, vt, dist_star, wisea, jmag, e_jmag, hmag,
                          e_hmag, ksmag, e_ksmag, w1mag, e_w1mag, w2mag, e_w2mag, w3mag, e_w3mag, w4mag, e_w4mag, j_k,
                          w1_w2, w3_w4, apass, vmaga, e_vmaga, bmaga, e_bmaga, gpmag, e_gpmag, rpmag, e_rpmag, ipmag,
                          e_ipmag, b_v, e_b_v, ref, perd, disc, url, m2, rec_star, dec_star]]
            self.ucac4_combobox.clear()
            self.ucac4_combobox.addItem(str(asassn))
            self.set_cross_id_button.setEnabled(False)
            self.fill_star(0)

    def download_data_coor(self, coor: Coordinate, radius="10s"):
        self.star.clear()
        rec = degrees(coor.rektascenze())
        dec = degrees(coor.deklinace())
        v = Vizier(columns=["+_r", "recno", "ID", "ASASSN-V", "OName", "RAJ2000", "DEJ2000", "GLON", "GLAT", "Vmag",
                            "Amp", "Per", "Type", "Prob", "LKSL", "RFR", "HJD", "Gaia", "Gmag", "e_Gmag", "BPmag",
                            "e_BPmag", "RPmag", "e_RPmag", "BP-RP", "Plx", "e_Plx", "PlxErr", "pmRA", "e_pmRA",
                            "pmDE", "e_pmDE", "Vt", "Dist", "WISEA", "Jmag", "e_Jmag", "Hmag", "e_Hmag", "Ksmag",
                            "e_Ksmag", "W1mag", "e_W1mag", "W2mag", "e_W2mag", "W3mag", "e_W3mag", "W4mag", "e_W4mag",
                            "J-K", "W1-W2", "W3-W4", "APASS", "VmagA", "e_VmagA", "BmagA", "e_BmagA", "gpmag",
                            "e_gpmag", "rpmag", "e_rpmag", "ipmag", "e_ipmag", "B-V", "E(B-V)", "Ref", "Perd",
                            "Disc", "URL", "2M"], catalog="II/366")
        a = coord.SkyCoord(ra=rec, dec=dec, unit=(u.deg, u.deg))
        result = v.query_region(a, radius=radius)
        name_list = []
        for y in result:
            for x in y:
                r = x["_r"]
                recno = x["recno"]
                id_star = x["ID"]
                asassn = x["ASASSN-V"]
                oname = x["OName"]
                rec_star = x["RAJ2000"]
                dec_star = x["DEJ2000"]
                rec_txt = coordinate_to_text(radians(float(rec_star)), coordinate_format="hours",
                                             delimiters=("h ", "m ", 's'),
                                             decimal_numbers=3)
                dec_txt = coordinate_to_text(radians(float(dec_star)), coordinate_format="degree",
                                             delimiters=("° ", "m ", 's'),
                                             decimal_numbers=3)

                glon = x["GLON"]
                glat = x["GLAT"]
                vmag = x["Vmag"]
                amp = x["Amp"]
                per = x["Per"]
                type_var = x["Type"]
                prob = x["Prob"]
                lksl = x["LKSL"]
                rfr = x["RFR"]
                hjd = x["_tab1_15"]
                gaia = x["Gaia"]
                gmag = x["Gmag"]
                e_gmag = x["e_Gmag"]
                bpmag = x["BPmag"]
                e_bpmag = x["e_BPmag"]
                gaia_rpmag = x["RPmag"]
                gaia_e_rpmag = x["e_RPmag"]
                bp_rp = x["BP-RP"]
                plx = x["Plx"]
                e_plx = x["e_Plx"]
                plxerr = x["PlxErr"]
                pmra = x["pmRA"]
                e_pmra = x["e_pmRA"]
                pmde = x["pmDE"]
                e_pmde = x["e_pmDE"]
                vt = x["Vt"]
                dist_star = x["Dist"]
                wisea = x["WISEA"]
                jmag = x["Jmag"]
                e_jmag = x["e_Jmag"]
                hmag = x["Hmag"]
                e_hmag = x["e_Hmag"]
                ksmag = x["Ksmag"]
                e_ksmag = x["e_Ksmag"]
                w1mag = x["W1mag"]
                e_w1mag = x["e_W1mag"]
                w2mag = x["W2mag"]
                e_w2mag = x["e_W2mag"]
                w3mag = x["W3mag"]
                e_w3mag = x["e_W3mag"]
                w4mag = x["W4mag"]
                e_w4mag = x["e_W4mag"]
                j_k = x["J-K"]
                w1_w2 = x["W1-W2"]
                w3_w4 = x["W3-W4"]
                apass = x["APASS"]
                vmaga = x["VmagA"]
                e_vmaga = x["e_VmagA"]
                bmaga = x["BmagA"]
                e_bmaga = x["e_BmagA"]
                gpmag = x["gpmag"]
                e_gpmag = x["e_gpmag"]
                rpmag = x["rpmag"]
                e_rpmag = x["e_rpmag"]
                ipmag = x["ipmag"]
                e_ipmag = x["e_ipmag"]
                b_v = x["B-V"]
                e_b_v = x["E_B-V_"]
                ref = x["Ref"]
                perd = x["Perd"]
                disc = x["Disc"]
                url = x["URL"]
                m2 = x["_2M"]

                self.star.append([r, recno, id_star, asassn, oname, rec_txt, dec_txt, glon, glat, vmag, amp, per,
                                  type_var, prob, lksl, rfr, hjd, gaia, gmag, e_gmag, bpmag, e_bpmag, gaia_rpmag,
                                  gaia_e_rpmag, bp_rp, plx, e_plx, plxerr, pmra, e_pmra, pmde, e_pmde, vt, dist_star,
                                  wisea, jmag, e_jmag, hmag, e_hmag, ksmag, e_ksmag, w1mag, e_w1mag, w2mag, e_w2mag,
                                  w3mag, e_w3mag, w4mag, e_w4mag, j_k, w1_w2, w3_w4, apass, vmaga, e_vmaga, bmaga,
                                  e_bmaga, gpmag, e_gpmag, rpmag, e_rpmag, ipmag, e_ipmag, b_v, e_b_v, ref, perd, disc,
                                  url, m2, rec_star, dec_star])
                name_list.append(str(asassn))
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
        self.delta_r_label.setText(str(self.star[index][0]))
        self.recno_label.setText(str(self.star[index][1]))
        self.id_star_label.setText(str(self.star[index][2]))

        self.oname_label.setText(str(self.star[index][4]))
        self.raj2000_label.setText(str(self.star[index][5]))
        self.dej2000_label.setText(str(self.star[index][6]))
        self.glon_label.setText(str(self.star[index][7]))
        self.glat_label.setText(str(self.star[index][8]))
        self.vmag_label.setText(str(self.star[index][9]))
        self.amp_label.setText(str(self.star[index][10]))
        self.per_label.setText(str(self.star[index][11]))
        self.type_var_label.setText(str(self.star[index][12]))
        self.prob_label.setText(str(self.star[index][13]))
        self.lksl_label.setText(str(self.star[index][14]))
        self.rfr_label.setText(str(self.star[index][15]))
        self.hjd_label.setText(str(self.star[index][16]))
        self.gaia_label.setText(str(self.star[index][17]))
        self.gmag_label.setText(str(self.star[index][18]))
        self.e_gmag_label.setText(str(self.star[index][19]))
        self.bpmag_label.setText(str(self.star[index][20]))
        self.e_bpmag_label.setText(str(self.star[index][21]))
        self.gaia_rpmag_label.setText(str(self.star[index][22]))
        self.gaia_e_rpmag_label.setText(str(self.star[index][23]))
        self.bp_rp_label.setText(str(self.star[index][24]))
        self.plx_label.setText(str(self.star[index][25]))
        self.e_plx_label.setText(str(self.star[index][26]))
        self.plxerr_label.setText(str(self.star[index][27]))
        self.pmra_label.setText(str(self.star[index][28]))
        self.e_pmra_label.setText(str(self.star[index][29]))
        self.pmde_label.setText(str(self.star[index][30]))
        self.e_pmde_label.setText(str(self.star[index][31]))
        self.vt_label.setText(str(self.star[index][32]))
        self.dist_star_label.setText(str(self.star[index][33]))
        self.wisea_label.setText(str(self.star[index][34]))
        self.jmag_label.setText(str(self.star[index][35]))
        self.e_jmag_label.setText(str(self.star[index][36]))
        self.hmag_label.setText(str(self.star[index][37]))
        self.e_hmag_label.setText(str(self.star[index][38]))
        self.ksmag_label.setText(str(self.star[index][39]))
        self.e_ksmag_label.setText(str(self.star[index][40]))
        self.w1mag_label.setText(str(self.star[index][41]))
        self.e_w1mag_label.setText(str(self.star[index][42]))
        self.w2mag_label.setText(str(self.star[index][43]))
        self.e_w2mag_label.setText(str(self.star[index][44]))
        self.w3mag_label.setText(str(self.star[index][45]))
        self.e_w3mag_label.setText(str(self.star[index][46]))
        self.w4mag_label.setText(str(self.star[index][47]))
        self.e_w4mag_label.setText(str(self.star[index][48]))
        self.j_k_label.setText(str(self.star[index][49]))
        self.w1_w2_label.setText(str(self.star[index][50]))
        self.w3_w4_label.setText(str(self.star[index][51]))
        self.apass_label.setText(str(self.star[index][52]))
        self.vmaga_label.setText(str(self.star[index][53]))
        self.e_vmaga_label.setText(str(self.star[index][54]))
        self.bmaga_label.setText(str(self.star[index][55]))
        self.e_bmaga_label.setText(str(self.star[index][56]))
        self.gpmag_label.setText(str(self.star[index][57]))
        self.e_gpmag_label.setText(str(self.star[index][58]))
        self.rpmag_label.setText(str(self.star[index][59]))
        self.e_rpmag_label.setText(str(self.star[index][60]))
        self.ipmag_label.setText(str(self.star[index][61]))
        self.e_ipmag_label.setText(str(self.star[index][62]))
        self.b_v_label.setText(str(self.star[index][63]))
        self.e_b_v_label.setText(str(self.star[index][64]))
        self.ref_label.setText(str(self.star[index][65]))
        self.perd_label.setText(str(self.star[index][66]))
        self.disc_label.setText(str(self.star[index][67]))
        self.url_label.setText(str(self.star[index][68]))
        self.m2_label.setText(str(self.star[index][69]))

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
                self.object_edit_window.star_alternativ_name_editline.setText(
                    "ASASSN-V " + str(self.star[star_index][3]))

            if self.raj2000_checkbox.isChecked():
                try:
                    rektascenze = float(self.star[star_index][70]) / 15
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
                    declination = float(self.star[star_index][71])

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
            if self.type_var_checkbox.isChecked():
                var_type = self.type_var_label.text().strip()
                if var_type in self.object_edit_window.database.variability_type:
                    self.object_edit_window.lightcurve_type_combobox.setCurrentText(var_type)
                else:
                    self.object_edit_window.get_new_variability_type()

            if self.vmag_checkbox.isChecked():
                try:
                    self.object_edit_window.star_mag_doublespinbox.setValue(float(self.vmag_label.text()))
                except:
                    mistake("Magnitude error", "Magnitude must be a number, uncheck magnitude import")

            if self.amp_checkbox.isChecked():
                try:
                    self.object_edit_window.lightcurve_amplitude_prim_doulespinbox.setValue(float(
                        self.amp_label.text()))
                except:
                    mistake("Amplitude error", "Amplitude must be a number, uncheck amplitude import")

            if self.hjd_checkbox.isChecked():
                try:
                    self.object_edit_window.lightcurve_epoch_editline.setText((self.hjd_label.text()))
                except:
                    mistake("Epoch error", "Epoch must be a number, uncheck epoch import")

            if self.per_checkbox.isChecked():
                try:
                    self.object_edit_window.lightcurve_period_editline.setText(self.per_label.text())
                except:
                    mistake("Period error", "Period must be a number, uncheck period import")
            self.is_it_import = False

            if self.j_k_checkbox.isChecked():
                try:
                    self.object_edit_window.star_j_k_doublespinbox.setValue(float(self.j_k_label.text()))
                except:
                    mistake("J-K error", "J-K must be a number, uncheck J-K import")
            self.is_it_import = False

            if self.b_v_checkbox.isChecked():
                try:
                    self.object_edit_window.star_b_v_doublespinbox.setValue(float(self.b_v_label.text()))
                except:
                    mistake("B-V", "B-V must be a number, uncheck B-V import")
            self.is_it_import = False
            self.close()
        else:
            try:
                new_ucac = str(self.star[star_index][3])
                star_index_in_main_file = self.step_main_form.stars.star_index(self.step_main_form.star_detail.name())
                self.step_main_form.stars.stars[star_index_in_main_file].change_asassn(new_ucac)
                self.step_main_form.asas_button.setText("ASASSN-V " + new_ucac)
                current_row = self.step_main_form.objects_table.currentRow()
                self.step_main_form.objects_table.setItem(current_row, 10,
                                                          QtWidgets.QTableWidgetItem(new_ucac))
                self.step_main_form.star_detail.change_asassn(new_ucac)
                self.step_main_form.filtered_stars.stars[current_row].change_asassn(new_ucac)
            except:
                pass

    def call_url(self):
        caled_url = self.url_label.text()
        QDesktopServices.openUrl(QUrl(caled_url))

    def clear_window(self):
        self.delta_r_label.clear()
        self.recno_label.clear()
        self.id_star_label.clear()
        self.oname_label.clear()
        self.raj2000_label.clear()
        self.dej2000_label.clear()
        self.glon_label.clear()
        self.glat_label.clear()
        self.vmag_label.clear()
        self.amp_label.clear()
        self.per_label.clear()
        self.type_var_label.clear()
        self.prob_label.clear()
        self.lksl_label.clear()
        self.rfr_label.clear()
        self.hjd_label.clear()
        self.gaia_label.clear()
        self.gmag_label.clear()
        self.e_gmag_label.clear()
        self.bpmag_label.clear()
        self.e_bpmag_label.clear()
        self.gaia_rpmag_label.clear()
        self.gaia_e_rpmag_label.clear()
        self.bp_rp_label.clear()
        self.plx_label.clear()
        self.e_plx_label.clear()
        self.plxerr_label.clear()
        self.pmra_label.clear()
        self.e_pmra_label.clear()
        self.pmde_label.clear()
        self.e_pmde_label.clear()
        self.vt_label.clear()
        self.dist_star_label.clear()
        self.wisea_label.clear()
        self.jmag_label.clear()
        self.e_jmag_label.clear()
        self.hmag_label.clear()
        self.e_hmag_label.clear()
        self.ksmag_label.clear()
        self.e_ksmag_label.clear()
        self.w1mag_label.clear()
        self.e_w1mag_label.clear()
        self.w2mag_label.clear()
        self.e_w2mag_label.clear()
        self.w3mag_label.clear()
        self.e_w3mag_label.clear()
        self.w4mag_label.clear()
        self.e_w4mag_label.clear()
        self.j_k_label.clear()
        self.w1_w2_label.clear()
        self.w3_w4_label.clear()
        self.apass_label.clear()
        self.vmaga_label.clear()
        self.e_vmaga_label.clear()
        self.bmaga_label.clear()
        self.e_bmaga_label.clear()
        self.gpmag_label.clear()
        self.e_gpmag_label.clear()
        self.rpmag_label.clear()
        self.e_rpmag_label.clear()
        self.ipmag_label.clear()
        self.e_ipmag_label.clear()
        self.b_v_label.clear()
        self.e_b_v_label.clear()
        self.ref_label.clear()
        self.perd_label.clear()
        self.disc_label.clear()
        self.m2_label.clear()
        self.hjd_label.clear()
        self.url_label.setText("")

    def check_item(self, active):
        self.raj2000_checkbox.setChecked(active)
        self.dej2000_checkbox.setChecked(active)
        self.vmag_checkbox.setChecked(active)
        self.amp_checkbox.setChecked(active)
        self.per_checkbox.setChecked(active)
        self.type_var_checkbox.setChecked(active)
        self.j_k_checkbox.setChecked(active)
        self.b_v_checkbox.setChecked(active)
        self.hjd_checkbox.setChecked(active)

