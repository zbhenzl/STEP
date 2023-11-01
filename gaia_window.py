from coordinate import *
from astroquery.vizier import Vizier
import astropy.coordinates as coord
import astropy.units as u
from PyQt5 import QtWidgets, QtCore, QtGui
from astropy.coordinates import Angle


class GaiaWindow(QtWidgets.QWidget):

    def __init__(self, *args,**kvargs):
        super(GaiaWindow, self).__init__(*args, **kvargs)

        self.star = []
        self.setWindowTitle("GAIA DDR3 Catalogue Information")
        main_layout = QtWidgets.QGridLayout()
        self.setLayout(main_layout)

        ucac4_label = QtWidgets.QLabel("GAIA DDR3 identifier: ")
        self.ucac4_combobox = QtWidgets.QComboBox()

        header_layout = QtWidgets.QHBoxLayout()
        header_layout.addWidget(ucac4_label)
        header_layout.addWidget(self.ucac4_combobox)

        self.set_cross_id_button = QtWidgets.QPushButton("Choose the correct cross identification")
        delta_r_label = QtWidgets.QLabel("Radius:")
        ra_icrs_label = QtWidgets.QLabel("Right ascension (ICRS) at Ep=2016.0:")
        de_icrs_label = QtWidgets.QLabel("Declination (ICRS) at Ep=2016.0 (dec):")
        e_ra_icrs_label = QtWidgets.QLabel("Standard error of right ascension (ra_error) (mas):")
        e_de_icrs_label = QtWidgets.QLabel("Standard error of declination (dec_error) (mas):")
        plx_label = QtWidgets.QLabel("Parallax(mas) :")
        e_plx_label = QtWidgets.QLabel("Standard error of parallax(mas):")
        pm_label = QtWidgets.QLabel("Total proper motion (mas/yr)")
        pmra_label = QtWidgets.QLabel("Proper motion in right ascension direction(mas/yr):")
        e_pmra_label = QtWidgets.QLabel("Standard error of proper motion in right ascension direction(mas/yr):")
        pmde_label = QtWidgets.QLabel("Proper motion in declination direction(mas/yr):")
        e_pmde_label = QtWidgets.QLabel("Standard error of proper motion in declination direction(mas/yr):")
        ruwe_label = QtWidgets.QLabel("Renormalised unit weight error:")
        fg_label = QtWidgets.QLabel("G-band mean flux(e-/s):")
        e_fg_label = QtWidgets.QLabel("Error on G-band mean flux(e-/s):")
        gmag_label = QtWidgets.QLabel("G-band mean magnitude(mag):")
        fbp_label = QtWidgets.QLabel("Integrated BP mean flux(e-/s):")
        e_fbp_label = QtWidgets.QLabel("Error on the integrated BP mean flux(e-/s):")
        bpmag_label = QtWidgets.QLabel("Integrated BP mean magnitude(mag):")
        frp_label = QtWidgets.QLabel("Integrated RP mean flux:")
        e_frp_label = QtWidgets.QLabel("Error on the integrated RP mean flux")
        rpmag_label = QtWidgets.QLabel("Integrated RP mean magnitude(mag):")
        bp_rp_label = QtWidgets.QLabel("BP-RP colour(mag):")
        bp_g_label = QtWidgets.QLabel("BP-G colour(mag):")
        g_rp_label = QtWidgets.QLabel("G-RP colour(mag):")
        rv_label = QtWidgets.QLabel("Radial velocity(km/s):")
        e_rv_label = QtWidgets.QLabel("Radial velocity error(km/s):")
        vbroad_label = QtWidgets.QLabel("Spectral line broadening parameter(km/s):")
        grvsmag_label = QtWidgets.QLabel("Integrated Grvs magnitude(mag):")
        qsu_label = QtWidgets.QLabel("information in the QSO candidates table:")
        gal_label = QtWidgets.QLabel("information in the galaxy candidates table:")
        nss_label = QtWidgets.QLabel("information in the various Non-Single Star tables:")
        xpcont_label = QtWidgets.QLabel("mean BP/RP spectrum in continuous representation:")
        xpsamp_label = QtWidgets.QLabel("mean BP/RP spectrum in sampled form:")
        rvs_label = QtWidgets.QLabel("mean RVS spectrum for this source:")
        epochph_label = QtWidgets.QLabel("epoch photometry for this source:")
        epochrv_label = QtWidgets.QLabel("epoch radial velocity for this source:")
        mcmcgsp_label = QtWidgets.QLabel("GSP-Phot MCMC samples for this source:")
        mcmcmsc_label = QtWidgets.QLabel("MSC MCMC samples for this source:")
        and_label = QtWidgets.QLabel("present in the Gaia Andromeda Photometric Survey:")
        teff_label = QtWidgets.QLabel("Effective temperature from GSP(K):")
        logg_label = QtWidgets.QLabel("Surface gravity from GSP(cm/s2):")
        fe_h__label = QtWidgets.QLabel("Iron abundance from GSP:")
        dist_label = QtWidgets.QLabel("Distance from GSP(pc):")
        a0_label = QtWidgets.QLabel("Monochromatic extinction A_0 at 547.7nm(mag):")
        hip_label = QtWidgets.QLabel("HIP cross-id number:")
        ps1_label = QtWidgets.QLabel("PS1 cross-id name:")
        sdss13_label = QtWidgets.QLabel("SDSS name:")
        skym2_label = QtWidgets.QLabel("SkyMapperDR2 cross-id name:")
        tyc2_label = QtWidgets.QLabel("Tycho-2 cross-id name:")
        urat1_label = QtWidgets.QLabel("URAT1 name, Zacharias et al.:")
        allwise_label = QtWidgets.QLabel("ALLWISE cross-id name:")
        apass9_label = QtWidgets.QLabel("APASS9 identification:")
        gsc23_label = QtWidgets.QLabel("GSC2.3 cross-id name:")
        rave5_label = QtWidgets.QLabel("RAVE DR5 cross-id name:")
        two_mass_label = QtWidgets.QLabel("2MASS cross-id name:")
        rave6_label = QtWidgets.QLabel("RAVE DR6 cross-id name:")
        raj2000_label = QtWidgets.QLabel("Barycentric right ascension (ICRS) at Ep=2000.0:")
        dej2000_label = QtWidgets.QLabel("Barycentric declination (ICRS) at Ep=2000.0:")

        self.delta_r_label = QtWidgets.QLabel("")
        self.ra_icrs_label = QtWidgets.QLabel("")
        self.de_icrs_label = QtWidgets.QLabel("")
        self.e_ra_icrs_label = QtWidgets.QLabel("")
        self.e_de_icrs_label = QtWidgets.QLabel("")
        self.plx_label = QtWidgets.QLabel("")
        self.e_plx_label = QtWidgets.QLabel("")
        self.pm_label = QtWidgets.QLabel("")
        self.pmra_label = QtWidgets.QLabel("")
        self.e_pmra_label = QtWidgets.QLabel("")
        self.pmde_label = QtWidgets.QLabel("")
        self.e_pmde_label = QtWidgets.QLabel("")
        self.ruwe_label = QtWidgets.QLabel("")
        self.fg_label = QtWidgets.QLabel("")
        self.e_fg_label = QtWidgets.QLabel("")
        self.gmag_label = QtWidgets.QLabel("")
        self.fbp_label = QtWidgets.QLabel("")
        self.e_fbp_label = QtWidgets.QLabel("")
        self.bpmag_label = QtWidgets.QLabel("")
        self.frp_label = QtWidgets.QLabel("")
        self.e_frp_label = QtWidgets.QLabel("")
        self.rpmag_label = QtWidgets.QLabel("")
        self.bp_rp_label = QtWidgets.QLabel("")
        self.bp_g_label = QtWidgets.QLabel("")
        self.g_rp_label = QtWidgets.QLabel("")
        self.rv_label = QtWidgets.QLabel("")
        self.e_rv_label = QtWidgets.QLabel("")
        self.vbroad_label = QtWidgets.QLabel("")
        self.grvsmag_label = QtWidgets.QLabel("")
        #self.qsu_label = QtWidgets.QPushButton("")
        #self.gal_label = QtWidgets.QPushButton("")
        self.nss_label = QtWidgets.QPushButton("")
        self.xpcont_label = QtWidgets.QPushButton("")
        self.xpsamp_label = QtWidgets.QPushButton("")
        self.rvs_label = QtWidgets.QPushButton("")
        self.epochph_label = QtWidgets.QPushButton("")
        self.epochrv_label = QtWidgets.QPushButton("")
        self.mcmcgsp_label = QtWidgets.QPushButton("")
        self.mcmcmsc_label = QtWidgets.QPushButton("")
        #self.and_label = QtWidgets.QLabel("")
        self.teff_label = QtWidgets.QLabel("")
        self.logg_label = QtWidgets.QLabel("")
        self.fe_h__label = QtWidgets.QLabel("")
        self.dist_label = QtWidgets.QLabel("")
        self.a0_label = QtWidgets.QLabel("")
        self.hip_label = QtWidgets.QLabel("")
        self.ps1_label = QtWidgets.QLabel("")
        self.sdss13_label = QtWidgets.QLabel("")
        self.skym2_label = QtWidgets.QLabel("")
        self.tyc2_label = QtWidgets.QLabel("")
        self.urat1_label = QtWidgets.QLabel("")
        self.allwise_label = QtWidgets.QLabel("")
        self.apass9_label = QtWidgets.QLabel("")
        self.gsc23_label = QtWidgets.QLabel("")
        self.rave5_label = QtWidgets.QLabel("")
        self.two_mass_label = QtWidgets.QLabel("")
        self.rave6_label = QtWidgets.QLabel("")
        self.raj2000_label = QtWidgets.QLabel("")
        self.dej2000_label = QtWidgets.QLabel("")

        info_groupbox = QtWidgets.QGroupBox("GAIA DDR3 information")
        info_layout = QtWidgets.QGridLayout()
        info_groupbox.setLayout(info_layout)

        coor_groupbox = QtWidgets.QGroupBox("Coordinate information")
        coor_layout = QtWidgets.QFormLayout()
        coor_groupbox.setLayout(coor_layout)

        parallax_groupbox = QtWidgets.QGroupBox("Parallax information")
        parallax_layout = QtWidgets.QFormLayout()
        parallax_groupbox.setLayout(parallax_layout)

        flux_groupbox = QtWidgets.QGroupBox("Flux and magnitude information")
        flux_layout = QtWidgets.QFormLayout()
        flux_groupbox.setLayout(flux_layout)

        phys_groupbox = QtWidgets.QGroupBox("Physical parameters and information")
        phys_layout = QtWidgets.QFormLayout()
        phys_groupbox.setLayout(phys_layout)

        flag_groupbox = QtWidgets.QGroupBox("Flag indicating the availability")
        flag_layout = QtWidgets.QFormLayout()
        flag_groupbox.setLayout(flag_layout)

        cross_groupbox = QtWidgets.QGroupBox("cross identification")
        cross_layout = QtWidgets.QFormLayout()
        cross_groupbox.setLayout(cross_layout)

        coor_layout.addRow(delta_r_label, self.delta_r_label)
        coor_layout.addRow(ra_icrs_label, self.ra_icrs_label)
        coor_layout.addRow(de_icrs_label, self.de_icrs_label)
        coor_layout.addRow(e_ra_icrs_label, self.e_ra_icrs_label)
        coor_layout.addRow(e_de_icrs_label, self.e_de_icrs_label)
        coor_layout.addRow(raj2000_label, self.raj2000_label)
        coor_layout.addRow(dej2000_label, self.dej2000_label)

        parallax_layout.addRow(plx_label, self.plx_label)
        parallax_layout.addRow(e_plx_label, self.e_plx_label)
        parallax_layout.addRow(pm_label, self.pm_label)
        parallax_layout.addRow(pmra_label, self.pmra_label)
        parallax_layout.addRow(e_pmra_label, self.e_pmra_label)
        parallax_layout.addRow(pmde_label, self.pmde_label)
        parallax_layout.addRow(e_pmde_label, self.e_pmde_label)

        flux_layout.addRow(fg_label, self.fg_label)
        flux_layout.addRow(e_fg_label, self.e_fg_label)
        flux_layout.addRow(gmag_label, self.gmag_label)
        flux_layout.addRow(fbp_label, self.fbp_label)
        flux_layout.addRow(e_fbp_label, self.e_fbp_label)
        flux_layout.addRow(bpmag_label, self.bpmag_label)
        flux_layout.addRow(frp_label, self.frp_label)
        flux_layout.addRow(e_frp_label, self.e_frp_label)
        flux_layout.addRow(rpmag_label, self.rpmag_label)
        flux_layout.addRow(grvsmag_label, self.grvsmag_label)
        flux_layout.addRow(a0_label, self.a0_label)

        phys_layout.addRow(ruwe_label, self.ruwe_label)
        phys_layout.addRow(rv_label, self.rv_label)
        phys_layout.addRow(e_rv_label, self.e_rv_label)
        phys_layout.addRow(vbroad_label, self.vbroad_label)
        phys_layout.addRow(teff_label, self.teff_label)
        phys_layout.addRow(logg_label, self.logg_label)
        phys_layout.addRow(fe_h__label, self.fe_h__label)
        phys_layout.addRow(dist_label, self.dist_label)
        phys_layout.addRow(bp_rp_label, self.bp_rp_label)
        phys_layout.addRow(bp_g_label, self.bp_g_label)
        phys_layout.addRow(g_rp_label, self.g_rp_label)


        #flag_layout.addRow(qsu_label, self.qsu_label)
        #flag_layout.addRow(gal_label, self.gal_label)
        flag_layout.addRow(nss_label, self.nss_label)
        flag_layout.addRow(xpcont_label, self.xpcont_label)
        flag_layout.addRow(xpsamp_label, self.xpsamp_label)
        flag_layout.addRow(rvs_label, self.rvs_label)
        flag_layout.addRow(epochph_label, self.epochph_label)
        flag_layout.addRow(epochrv_label, self.epochrv_label)
        flag_layout.addRow(mcmcgsp_label, self.mcmcgsp_label)
        flag_layout.addRow(mcmcmsc_label, self.mcmcmsc_label)
        #flag_layout.addRow(and_label, self.and_label)

        cross_layout.addRow(hip_label, self.hip_label)
        cross_layout.addRow(ps1_label, self.ps1_label)
        cross_layout.addRow(sdss13_label, self.sdss13_label)
        cross_layout.addRow(skym2_label, self.skym2_label)
        cross_layout.addRow(tyc2_label, self.tyc2_label)
        cross_layout.addRow(urat1_label, self.urat1_label)
        cross_layout.addRow(allwise_label, self.allwise_label)
        cross_layout.addRow(apass9_label, self.apass9_label)
        cross_layout.addRow(gsc23_label, self.gsc23_label)
        cross_layout.addRow(rave5_label, self.rave5_label)
        cross_layout.addRow(two_mass_label, self.two_mass_label)
        cross_layout.addRow(rave6_label, self.rave6_label)

        info_layout.addWidget(coor_groupbox, 0, 0)
        info_layout.addWidget(parallax_groupbox, 0, 1)
        info_layout.addWidget(flux_groupbox, 1, 0)
        info_layout.addWidget(phys_groupbox, 1, 1)
        info_layout.addWidget(flag_groupbox, 2, 1)
        info_layout.addWidget(cross_groupbox, 2, 0)

        main_layout.addLayout(header_layout, 0, 0)
        main_layout.addWidget(self.set_cross_id_button, 0, 1)
        main_layout.addWidget(info_groupbox, 1, 0, 20, 2)



    def setup(self):
        from step_application import root
        self.step_main_form = root.step_main_form
        self.ucac4_combobox.currentTextChanged.connect(self.ucac_changed)
        self.set_cross_id_button.clicked.connect(self.set_cross_id)

    def download_data_id(self, cross_id: str):
        self.star.clear()
        agn = Vizier(catalog="I/355/gaiadr3", columns=["*", "BP-G", "G-RP"]).query_constraints(Source=cross_id)[0]
        for x in agn:
            id_star = x["Source"]
            delta_r = x["_r"]
            ra_icrs = x["RA_ICRS"]
            de_icrs = x["DE_ICRS"]
            ra_icrs_txt = coordinate_to_text(radians(float(ra_icrs)), coordinate_format="hours", delimiters=("h ", "m ", 's'),
                                         decimal_numbers=3)
            de_icrs_txt = coordinate_to_text(radians(float(de_icrs)), coordinate_format="degree", delimiters=("° ", "m ", 's'),
                                         decimal_numbers=3)
            e_ra_icrs = x["e_RA_ICRS"]
            e_de_icrs = x["e_DE_ICRS"]
            plx = x["Plx"]
            e_plx = x["e_Plx"]
            pm = x["PM"]
            pmra = x["pmRA"]
            e_pmra = x["e_pmRA"]
            pmde = x["pmDE"]
            e_pmde = x["e_pmDE"]
            ruwe = x["RUWE"]
            fg = x["FG"]
            e_fg = x["e_FG"]
            gmag = x["Gmag"]
            fbp = x["FBP"]
            e_fbp = x["e_FBP"]
            bpmag = x["BPmag"]
            frp = x["FRP"]
            e_frp = x["e_FRP"]
            rpmag = x["RPmag"]
            bp_rp = x["BP-RP"]
            bp_g = x["BP-G"]
            g_rp = x["G-RP"]
            rv = x["RV"]
            e_rv = x["e_RV"]
            vbroad = x["Vbroad"]
            grvsmag = x["GRVSmag"]
            qsu = x["QSO"]
            gal = x["Gal"]
            nss = x["NSS"]
            xpcont = x["XPcont"]
            xpsamp = x["XPsamp"]
            rvs = x["RVS"]
            epochph = x["EpochPh"]
            epochrv = x["EpochRV"]
            mcmcgsp = x["MCMCGSP"]
            mcmcmsc = x["MCMCMSC"]
            and_ = x["And"]
            teff = x["Teff"]
            logg = x["logg"]
            fe_h_ = x["__Fe_H_"]
            dist = x["Dist"]
            a0 = x["A0"]
            hip = x["HIP"]
            ps1 = x["PS1"]
            sdss13 = x["SDSS13"]
            skym2 = x["SKYM2"]
            tyc2 = x["TYC2"]
            urat1 = x["URAT1"]
            allwise = x["AllWISE"]
            apass9 = x["APASS9"]
            gsc23 = x["GSC23"]
            rave5 = x["RAVE5"]
            two_mass = x["_2MASS"]
            rave6 = x["RAVE6"]
            raj2000 = x["RAJ2000"]
            dej2000 = x["DEJ2000"]
            raj2000_txt = coordinate_to_text(radians(float(raj2000)), coordinate_format="hours", delimiters=("h ", "m ", 's'),
                                         decimal_numbers=3)
            dej2000_txt = coordinate_to_text(radians(float(dej2000)), coordinate_format="degree", delimiters=("° ", "m ", 's'),
                                         decimal_numbers=3)



            self.star = [["", ra_icrs_txt, de_icrs_txt, e_ra_icrs, e_de_icrs, plx, e_plx, pm, pmra, e_pmra, pmde,
                          e_pmde, ruwe, fg, e_fg, gmag, fbp, e_fbp, bpmag, frp, e_frp, rpmag, bp_rp, bp_g, g_rp, rv,
                          e_rv, vbroad, grvsmag, qsu, gal, nss, xpcont, xpsamp, rvs, epochph, epochrv, mcmcgsp, mcmcmsc,
                          and_, teff, logg, fe_h_, dist, a0, hip, ps1, sdss13, skym2, tyc2, urat1, allwise, apass9,
                          gsc23, rave5, two_mass, rave6, raj2000_txt, dej2000_txt, ra_icrs, de_icrs, raj2000, dej2000]]

            self.ucac4_combobox.clear()
            self.ucac4_combobox.addItem(str(id_star))
            self.set_cross_id_button.setEnabled(False)
            self.fill_star(0)

    def download_data_coor(self, coor: Coordinate):
        self.star.clear()
        rec = degrees(coor.rektascenze())
        dec = degrees(coor.deklinace())
        v = Vizier(columns=["*", "+_r", "BP-G", "G-RP"], catalog="I/355/gaiadr3")
        a = coord.SkyCoord(ra=rec, dec=dec, unit=(u.deg, u.deg))
        result = v.query_region(a, radius="10s")
        name_list = []
        for y in result:
            for x in y:
                r = x["_r"]
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
                e_ra_icrs = x["e_RA_ICRS"]
                e_de_icrs = x["e_DE_ICRS"]
                plx = x["Plx"]
                e_plx = x["e_Plx"]
                pm = x["PM"]
                pmra = x["pmRA"]
                e_pmra = x["e_pmRA"]
                pmde = x["pmDE"]
                e_pmde = x["e_pmDE"]
                ruwe = x["RUWE"]
                fg = x["FG"]
                e_fg = x["e_FG"]
                gmag = x["Gmag"]
                fbp = x["FBP"]
                e_fbp = x["e_FBP"]
                bpmag = x["BPmag"]
                frp = x["FRP"]
                e_frp = x["e_FRP"]
                rpmag = x["RPmag"]
                bp_rp = x["BP-RP"]
                bp_g = x["BP-G"]
                g_rp = x["G-RP"]
                rv = x["RV"]
                e_rv = x["e_RV"]
                vbroad = x["Vbroad"]
                grvsmag = x["GRVSmag"]
                qsu = x["QSO"]
                gal = x["Gal"]
                nss = x["NSS"]
                xpcont = x["XPcont"]
                xpsamp = x["XPsamp"]
                rvs = x["RVS"]
                epochph = x["EpochPh"]
                epochrv = x["EpochRV"]
                mcmcgsp = x["MCMCGSP"]
                mcmcmsc = x["MCMCMSC"]
                and_ = x["And"]
                teff = x["Teff"]
                logg = x["logg"]
                fe_h_ = x["__Fe_H_"]
                dist = x["Dist"]
                a0 = x["A0"]
                hip = x["HIP"]
                ps1 = x["PS1"]
                sdss13 = x["SDSS13"]
                skym2 = x["SKYM2"]
                tyc2 = x["TYC2"]
                urat1 = x["URAT1"]
                allwise = x["AllWISE"]
                apass9 = x["APASS9"]
                gsc23 = x["GSC23"]
                rave5 = x["RAVE5"]
                two_mass = x["_2MASS"]
                rave6 = x["RAVE6"]
                raj2000 = x["RAJ2000"]
                dej2000 = x["DEJ2000"]
                raj2000_txt = coordinate_to_text(radians(float(raj2000)), coordinate_format="hours",
                                                 delimiters=("h ", "m ", 's'),
                                                 decimal_numbers=3)
                dej2000_txt = coordinate_to_text(radians(float(dej2000)), coordinate_format="degree",
                                                 delimiters=("° ", "m ", 's'),
                                                 decimal_numbers=3)

                self.star.append([r, ra_icrs_txt, de_icrs_txt, e_ra_icrs, e_de_icrs, plx, e_plx, pm, pmra, e_pmra,
                                  pmde, e_pmde, ruwe, fg, e_fg, gmag, fbp, e_fbp, bpmag, frp, e_frp, rpmag, bp_rp, bp_g,
                                  g_rp, rv, e_rv, vbroad, grvsmag, qsu, gal, nss, xpcont, xpsamp, rvs, epochph, epochrv,
                                  mcmcgsp, mcmcmsc, and_, teff, logg, fe_h_, dist, a0, hip, ps1, sdss13, skym2, tyc2,
                                  urat1, allwise, apass9, gsc23, rave5, two_mass, rave6, raj2000_txt, dej2000_txt,
                                  id_star, ra_icrs, de_icrs, raj2000, dej2000])

                name_list.append(str(id_star))
        self.ucac4_combobox.clear()
        self.ucac4_combobox.addItems(name_list)
        self.set_cross_id_button.setEnabled(True)
        self.fill_star(0)

    def fill_star(self, index):
        self.delta_r_label.setText(str(self.star[index][0]))
        self.ra_icrs_label.setText(str(self.star[index][1]))
        self.de_icrs_label.setText(str(self.star[index][2]))
        self.e_ra_icrs_label.setText(str(self.star[index][3]))
        self.e_de_icrs_label.setText(str(self.star[index][4]))
        self.plx_label.setText(str(self.star[index][5]))
        self.e_plx_label.setText(str(self.star[index][6]))
        self.pm_label.setText(str(self.star[index][7]))
        self.pmra_label.setText(str(self.star[index][8]))
        self.e_pmra_label.setText(str(self.star[index][9]))
        self.pmde_label.setText(str(self.star[index][10]))
        self.e_pmde_label.setText(str(self.star[index][11]))
        self.ruwe_label.setText(str(self.star[index][12]))
        self.fg_label.setText(str(self.star[index][13]))
        self.e_fg_label.setText(str(self.star[index][14]))
        self.gmag_label.setText(str(self.star[index][15]))
        self.fbp_label.setText(str(self.star[index][16]))
        self.e_fbp_label.setText(str(self.star[index][17]))
        self.bpmag_label.setText(str(self.star[index][18]))
        self.frp_label.setText(str(self.star[index][19]))
        self.e_frp_label.setText(str(self.star[index][20]))
        self.rpmag_label.setText(str(self.star[index][21]))
        self.bp_rp_label.setText(str(self.star[index][22]))
        self.bp_g_label.setText(str(self.star[index][23]))
        self.g_rp_label.setText(str(self.star[index][24]))
        self.rv_label.setText(str(self.star[index][25]))
        self.e_rv_label.setText(str(self.star[index][26]))
        self.vbroad_label.setText(str(self.star[index][27]))
        self.grvsmag_label.setText(str(self.star[index][28]))
        #self.qsu_label.setText(str(self.star[index][29]))
        #self.gal_label.setText(str(self.star[index][30]))
        self.nss_label.setText(str(self.star[index][31]))
        self.xpcont_label.setText(str(self.star[index][32]))
        self.xpsamp_label.setText(str(self.star[index][33]))
        self.rvs_label.setText(str(self.star[index][34]))
        self.epochph_label.setText(str(self.star[index][35]))
        self.epochrv_label.setText(str(self.star[index][36]))
        self.mcmcgsp_label.setText(str(self.star[index][37]))
        self.mcmcmsc_label.setText(str(self.star[index][38]))
        #self.and_label.setText(str(self.star[index][39]))
        self.teff_label.setText(str(self.star[index][40]))
        self.logg_label.setText(str(self.star[index][41]))
        self.fe_h__label.setText(str(self.star[index][42]))
        self.dist_label.setText(str(self.star[index][43]))
        self.a0_label.setText(str(self.star[index][44]))
        self.hip_label.setText(str(self.star[index][45]))
        self.ps1_label.setText(str(self.star[index][46]))
        self.sdss13_label.setText(str(self.star[index][47]))
        self.skym2_label.setText(str(self.star[index][48]))
        self.tyc2_label.setText(str(self.star[index][49]))
        self.urat1_label.setText(str(self.star[index][50]))
        self.allwise_label.setText(str(self.star[index][51]))
        self.apass9_label.setText(str(self.star[index][52]))
        self.gsc23_label.setText(str(self.star[index][53]))
        self.rave5_label.setText(str(self.star[index][54]))
        self.two_mass_label.setText(str(self.star[index][55]))
        self.rave6_label.setText(str(self.star[index][56]))
        self.raj2000_label.setText(str(self.star[index][57]))
        self.dej2000_label.setText(str(self.star[index][58]))

        #if self.qsu_label.text() == "0":
        #    self.qsu_label.setEnabled(False)
        #else:
        #    self.qsu_label.setEnabled(True)
#
        #if self.gal_label.text() == "0":
        #    self.gal_label.setEnabled(False)
        #else:
        #    self.gal_label.setEnabled(True)
        if self.nss_label.text() == "0":
            self.nss_label.setEnabled(False)
        else:
            self.nss_label.setEnabled(True)
        if self.xpcont_label.text() == "0":
            self.xpcont_label.setEnabled(False)
        else:
            self.xpcont_label.setEnabled(True)
        if self.xpsamp_label.text() == "0":
            self.xpsamp_label.setEnabled(False)
        else:
            self.xpsamp_label.setEnabled(True)
        if self.rvs_label.text() == "0":
            self.rvs_label.setEnabled(False)
        else:
            self.rvs_label.setEnabled(True)
        if self.epochph_label.text() == "0":
            self.epochph_label.setEnabled(False)
        else:
            self.epochph_label.setEnabled(True)
        if self.epochrv_label.text() == "0":
            self.epochrv_label.setEnabled(False)
        else:
            self.epochrv_label.setEnabled(True)
        if self.mcmcgsp_label.text() == "0":
            self.mcmcgsp_label.setEnabled(False)
        else:
            self.mcmcgsp_label.setEnabled(True)
        if self.mcmcmsc_label.text() == "0":
            self.mcmcmsc_label.setEnabled(False)
        else:
            self.mcmcmsc_label.setEnabled(True)

    def ucac_changed(self):
        star_index = self.ucac4_combobox.currentIndex()
        self.fill_star(star_index)

    def set_cross_id(self):
        try:
            star_index = self.ucac4_combobox.currentIndex()
            new_ucac = str(self.star[star_index][59])
            star_index_in_main_file = self.step_main_form.stars.star_index(self.step_main_form.star_detail.name())
            self.step_main_form.stars.stars[star_index_in_main_file].change_gaia(new_ucac)
            self.step_main_form.gaia_button.setText("GAIA " + new_ucac)
            current_row = self.step_main_form.objects_table.currentRow()
            self.step_main_form.objects_table.setItem(current_row, 8,
                                                      QtWidgets.QTableWidgetItem(new_ucac))
            self.step_main_form.star_detail.change_gaia(new_ucac)
            self.step_main_form.filtered_stars.stars[current_row].change_gaia(new_ucac)
        except:
            pass