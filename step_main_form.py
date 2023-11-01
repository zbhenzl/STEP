from PyQt5 import QtWidgets, QtCore, QtGui
import sys
from datetime import *
import os
import threading
from database import *
from coordinate import *
from time_period import jd_to_date
from variables import *
from astropy.coordinates import angular_separation


class StepMainForm(QtWidgets.QMainWindow):

    def __init__(self, **kvargs):
        super(StepMainForm, self).__init__(**kvargs)

        self.__author = "Zbynek Henzl"
        self.__version = "2.6"
        self.setWindowTitle("STEP - STellar Eclipse Predicting and lightcurve modeling system")

        # Main Widget a layout
        main_page = QtWidgets.QWidget()
        self.main_page_layout = QtWidgets.QGridLayout()
        self.main_page_layout.setSpacing(10)
        self.main_page_layout.setContentsMargins(10, 10, 10, 10)
        main_page.setLayout(self.main_page_layout)
        self.setCentralWidget(main_page)
        self.setWindowIcon(QtGui.QIcon("stairs.png"))


        self.__menu()
        self.__build()

    def __menu(self):
        menu = self.menuBar()
        user_menu = menu.addMenu("&User")
        period_menu = menu.addMenu("&Time range")
        star_menu = menu.addMenu("&Object")
        action_menu = menu.addMenu("&Action")
        program_menu = menu.addMenu("&Exit")


        # User menu
        self.user_add_action = QtWidgets.QAction(QtGui.QIcon("user--plus.png"), "Add &User", self)
        self.user_add_action.setStatusTip("Define and add another user")
        self.user_add_action.triggered.connect(self.add_user)

        self.user_delete_action = QtWidgets.QAction(QtGui.QIcon("user--minus.png"), "Delete User", self)
        self.user_delete_action.setStatusTip("Delete user from user list. The user cannot have a defined observation place "
                                        "and instruments")
        self.user_delete_action.triggered.connect(self.delete_user)

        self.user_rename_action = QtWidgets.QAction(QtGui.QIcon("user-share.png"), "Rename User", self)
        self.user_rename_action.setStatusTip("Change current user name")
        self.user_rename_action.triggered.connect(self.rename_user)

        self.place_add_action = QtWidgets.QAction(QtGui.QIcon("store--plus.png"), "Add new place", self)
        self.place_add_action.setStatusTip("Define and add another observation site")
        self.place_add_action.triggered.connect(self.add_observer)

        self.place_delete_action = QtWidgets.QAction(QtGui.QIcon("store--minus.png"), "Delete Place", self)
        self.place_delete_action.setStatusTip("Delete place from place list. The place cannot have a defined instruments")
        self.place_delete_action.triggered.connect(self.delete_place)

        self.place_rename_action = QtWidgets.QAction(QtGui.QIcon("store-open.png"), "Edit Place", self)
        self.place_rename_action.setStatusTip("Change current place name or coordinates")
        self.place_rename_action.triggered.connect(self.set_place)

        self.place_horizon_action = QtWidgets.QAction(QtGui.QIcon("eye--pencil.png"), "Set &Horizon", self)
        self.place_horizon_action.setStatusTip("Defines the horizon at the point of observation")
        self.place_horizon_action.setShortcut(QtGui.QKeySequence(QtCore.Qt.ALT + QtCore.Qt.Key_H))
        self.place_horizon_action.triggered.connect(self.set_horizon)

        self.instrument_add_action = QtWidgets.QAction(QtGui.QIcon("binocular--plus.png"), "Add Instrument", self)
        self.instrument_add_action.setStatusTip("Define and add new instrument set")
        self.instrument_add_action.triggered.connect(self.add_instrument)

        self.instrument_delete_action = QtWidgets.QAction(QtGui.QIcon("binocular--minus.png"), "Delete Instrument", self)
        self.instrument_delete_action.setStatusTip("Delete instrument from instrument list")
        self.instrument_delete_action.triggered.connect(self.delete_instrument)

        self.instrument_edit_action = QtWidgets.QAction(QtGui.QIcon("binocular--pencil.png"), "Edit Instrument", self)
        self.instrument_edit_action.setStatusTip("Change the current settings of the device. The instrument settings will "
                                           "also change for past observations")
        self.instrument_edit_action.triggered.connect(self.set_instrument)

        # action menu
        self.save_action = QtWidgets.QAction(QtGui.QIcon("computer--pencil.png"), "&Save All", self)
        self.save_action.setStatusTip("Save all data and seting")
        self.save_action.setShortcut(QtGui.QKeySequence(QtCore.Qt.CTRL + QtCore.Qt.Key_S))
        self.save_action.triggered.connect(self.save)

        self.photometry_action = QtWidgets.QAction(QtGui.QIcon("star-small.png"), "&Tess Photometry", self)
        self.photometry_action.setStatusTip("Tess photometry window")
        self.photometry_action.setShortcut(QtGui.QKeySequence(QtCore.Qt.CTRL + QtCore.Qt.Key_T))
        self.photometry_action.triggered.connect(self.tess_menu_window_start)

        self.prediction_action = QtWidgets.QAction(QtGui.QIcon("chart-up.png"), "Show P&rediction", self)
        self.prediction_action.setStatusTip("Show prediction of all selected stars in selected time area")
        self.prediction_action.setShortcut(QtGui.QKeySequence(QtCore.Qt.CTRL + QtCore.Qt.Key_R))
        self.prediction_action.triggered.connect(self.show_prediction_click)

        self.observation_action = QtWidgets.QAction(QtGui.QIcon("binocular--exclamation.png"), "Show &Observation", self)
        self.observation_action.setStatusTip("Shows information about the observations made")
        self.observation_action.setShortcut(QtGui.QKeySequence(QtCore.Qt.CTRL + QtCore.Qt.Key_O))
        self.observation_action.triggered.connect(self.show_observation)

        self.import_action = QtWidgets.QAction(QtGui.QIcon("application-import.png"), "&Import Objects", self)
        self.import_action.setStatusTip("Import objects from STEP Import file")
        self.import_action.triggered.connect(self.import_stars)

        self.export_action = QtWidgets.QAction(QtGui.QIcon("application-export.png"), "&Export Objects", self)
        self.export_action.setStatusTip("Export objects to STEP Import file")
        self.export_action.triggered.connect(self.export)

        self.lightcurve_action = QtWidgets.QAction(QtGui.QIcon("chart-down-color.png"), "Show_&Light Curve", self)
        self.lightcurve_action.setStatusTip("Displays the light curve of the object")
        self.lightcurve_action.setShortcut(QtGui.QKeySequence(QtCore.Qt.CTRL + QtCore.Qt.Key_L))
        self.lightcurve_action.triggered.connect(self.show_lightcurve)

        self.check_variability_action = QtWidgets.QAction(QtGui.QIcon("magnifier.png"), "Check Variability", self)
        self.check_variability_action.setStatusTip("You can check if star in known variable")
        self.check_variability_action.setShortcut(QtGui.QKeySequence(QtCore.Qt.CTRL + QtCore.Qt.Key_B))
        self.check_variability_action.triggered.connect(self.check_variability)

        self.tess_setting_action = QtWidgets.QAction(QtGui.QIcon("star--arrow.png"), "TESS photometry setting", self)
        self.tess_setting_action.setStatusTip("You can change parameters of TESS photometry")
        self.tess_setting_action.setShortcut(QtGui.QKeySequence(QtCore.Qt.CTRL + QtCore.Qt.Key_K))
        self.tess_setting_action.triggered.connect(self.photometry_setting)


        # star menu
        self.star_new_action = QtWidgets.QAction(QtGui.QIcon("star--plus.png"), "&New object", self)
        self.star_new_action.setStatusTip("Add new object")
        self.star_new_action.setShortcut(QtGui.QKeySequence(QtCore.Qt.CTRL + QtCore.Qt.Key_N))
        self.star_new_action.triggered.connect(self.new_object)


        self.star_edit_action = QtWidgets.QAction(QtGui.QIcon("star--pencil.png"), "&Edit object", self)
        self.star_edit_action.setStatusTip("Edit object and pair parameters, import data from external "
                                      "databases and programs, etc....Object must be selected")
        self.star_edit_action.setShortcut(QtGui.QKeySequence(QtCore.Qt.CTRL + QtCore.Qt.Key_E))
        self.star_edit_action.triggered.connect(self.edit_object)

        self.star_delete_pair_action = QtWidgets.QAction(QtGui.QIcon("star-half.png"), "&Delete pair", self)
        self.star_delete_pair_action.setStatusTip("Delete current selected pair from current selected object. "
                                             "Object must be selected")
        self.star_delete_pair_action.triggered.connect(self.delete_pair)

        self.star_add_model_file_action = QtWidgets.QAction(QtGui.QIcon("star--pencil.png"), "&Import model from file", self)
        self.star_add_model_file_action.setStatusTip("Import model from file (Silicups model file). Object must be selected")
        self.star_add_model_file_action.setShortcut(QtGui.QKeySequence(QtCore.Qt.CTRL + QtCore.Qt.Key_M))
        self.star_add_model_file_action.triggered.connect(self.add_model_quickly)

        self.star_delete_action = QtWidgets.QAction(QtGui.QIcon("star--minus.png"), "&Delete Star", self)
        self.star_delete_action.setStatusTip("Delete current selected object. Object must be selected")
        self.star_delete_action.triggered.connect(self.delete_star)

        # program menu

        self.program_version_action = QtWidgets.QAction(QtGui.QIcon("information-shield.png"), "&Program Info", self)
        self.program_version_action.setStatusTip("Show program a version information")
        self.program_version_action.triggered.connect(self.version)

        self.quit_action = QtWidgets.QAction(QtGui.QIcon("door-open-out.png"), "&Exit", self)
        self.quit_action.setShortcut(QtGui.QKeySequence(QtCore.Qt.CTRL + QtCore.Qt.Key_Q))
        self.quit_action.setStatusTip("Exit STEP")
        self.quit_action.triggered.connect(self.closeEvent)

        # period menu

        self.start_action = QtWidgets.QAction(QtGui.QIcon("alarm-clock--plus.png"), "Time range &start", self)
        self.start_action.setShortcut(QtGui.QKeySequence(QtCore.Qt.ALT + QtCore.Qt.Key_S))
        self.start_action.setStatusTip("Setting the start of the observation interval")
        self.start_action.triggered.connect(self.calendar_start_add_form)

        self.end_action = QtWidgets.QAction(QtGui.QIcon("alarm-clock--minus.png"), "Time range e&nd", self)
        self.end_action.setShortcut(QtGui.QKeySequence(QtCore.Qt.ALT + QtCore.Qt.Key_N))
        self.end_action.setStatusTip("Setting the end of the observation interval")
        self.end_action.triggered.connect(self.calendar_end_add_form)



        user_menu.addAction(self.user_add_action)
        user_menu.addAction(self.user_delete_action)
        user_menu.addAction(self.user_rename_action)
        user_menu.addSeparator()
        user_menu.addAction(self.place_add_action)
        user_menu.addAction(self.place_delete_action)
        user_menu.addAction(self.place_rename_action)
        user_menu.addAction(self.place_horizon_action)
        user_menu.addSeparator()
        user_menu.addAction(self.instrument_add_action)
        user_menu.addAction(self.instrument_delete_action)
        user_menu.addAction(self.instrument_edit_action)

        action_menu.addAction(self.save_action)
        action_menu.addSeparator()
        action_menu.addAction(self.photometry_action)
        action_menu.addAction(self.tess_setting_action)
        action_menu.addAction(self.prediction_action)
        action_menu.addAction(self.observation_action)
        action_menu.addAction(self.lightcurve_action)
        action_menu.addAction(self.check_variability_action)


        star_menu.addAction(self.star_new_action)
        star_menu.addAction(self.star_edit_action)
        star_menu.addAction(self.star_delete_action)
        star_menu.addSeparator()
        star_menu.addAction(self.star_add_model_file_action)
        star_menu.addAction(self.star_delete_pair_action)
        star_menu.addSeparator()
        star_menu.addAction(self.import_action)
        star_menu.addAction(self.export_action)

        period_menu.addAction(self.start_action)
        period_menu.addAction(self.end_action)

        program_menu.addAction(self.program_version_action)
        program_menu.addAction(self.quit_action)

        self.setStatusBar(QtWidgets.QStatusBar(self))

    def setup(self):
        from step_application import root
        self.database = root.database
        self.calendar_add_widget = root.calendar_add_widget
        self.horizon_set_window = root.horizon_set_window
        self.time_period = self.database.time_period
        self.sun = self.database.sun
        self.moon = self.database.moon
        self.users = self.database.users
        self.horizons = self.database.horizons
        self.places = self.database.places
        self.instruments = self.database.instruments
        self.user = self.database.user
        self.place = self.database.place
        self.instrument = self.database.instrument
        self.horizon = self.place.horizon()
        self.add_user_window = root.add_user_window
        self.add_place_window = root.add_place_window
        self.add_instrument_window = root.add_instrument_window
        self.stars = root.database.stars
        self.filtered_stars = root.database.filtered_stars
        self.variable = root.database.variables
        self.actual_variable = self.database.actual_variable
        self.object_edit_window = root.object_edit_window
        self.ucac4_window = root.ucac4_window
        self.usno_window = root.usno_window
        self.vsx_window = root.vsx_window
        self.gaia_window = root.gaia_window
        self.asas_window = root.asas_window
        self.tess_window = root.tess_window
        self.tess_menu_window = root.tess_menu_window
        self.prediction2 = root.prediction2
        self.rename_user_window = root.rename_user_window
        self.edit_place_window = root.edit_place_window
        self.edit_instrument_window = root.edit_instrument_window
        self.observation_log_window = root.observation_log_window
        self.export_window = root.export_window
        self.import_window = root.import_window
        self.known_variable_window = root.known_variable_window
        self.tess_menu_window_setting = root.tess_menu_window_setting
        self.show()

        # filling
        self.constilation_combobox.addItems(self.database.const_abbrs)
        self.period_start_dateedit.setDate(jd_to_date(self.time_period.jd_start()).date())
        self.period_start_timeedit.setTime(jd_to_date(self.time_period.jd_start()).time())
        self.period_end_dateedit.setDate(jd_to_date(self.time_period.jd_end()))
        self.period_end_timeedit.setTime(jd_to_date(self.time_period.jd_end()).time())
        self.julian_date_start_label.setText(str(round(self.time_period.jd_start(), 5)))
        self.julian_date_end_label.setText(str(round(self.time_period.jd_end(), 5)))
        self.fill_user()
        self.user_combobox.setCurrentText(str(self.user))
        self.edit_user()
        self.observer_combobox.setCurrentText(str(self.place))
        self.edit_place()
        self.fill_type_boxes()
        self.fill_table()
        self.update()

        # connecting

        # user
        self.user_combobox.currentTextChanged.connect(self.edit_user)

       # observer
        self.observer_combobox.currentTextChanged.connect(self.edit_place)

        # instruments
        self.instrument_combobox.currentTextChanged.connect(self.edit_instrument)

        # don´disturb
        self.catalog_show_button.clicked.connect(self.show_catalog)
        self.catalog_combobox.currentTextChanged.connect(self.show_catalog_number)

        # period
        self.period_start_dateedit.dateChanged.connect(self.time_period_start_change)
        self.period_start_timeedit.timeChanged.connect(self.time_period_start_change)
        self.period_end_dateedit.dateChanged.connect(self.time_period_end_change)
        self.period_end_timeedit.timeChanged.connect(self.time_period_end_change)

        # flat
        self.sun_h_set_spinbox.valueChanged.connect(self.fill_sun_moon)
        self.flat_h_spinbox.valueChanged.connect(self.fill_sun_moon)
        self.flat_a_spinbox_sunrise.valueChanged.connect(self.fill_sun_moon)
        self.flat_h_spinbox_sunrise.valueChanged.connect(self.fill_sun_moon)
        self.flat_a_spinbox_sunset.valueChanged.connect(self.fill_sun_moon)
        self.flat_h_spinbox_sunset.valueChanged.connect(self.fill_sun_moon)
        self.group_checkbox.buttonClicked.connect(self.fill_sun_moon)
        self.sun_settime_dateedit.dateChanged.connect(self.fill_sun_moon)

        # table
        self.sort_by_combobox.currentTextChanged.connect(self.fill_table)
        self.filter_by_var_checkbox.clicked.connect(self.fill_table)
        self.filter_by_user_checkbox.clicked.connect(self.fill_table)
        self.filter_by_place_checkbox.clicked.connect(self.fill_table)
        self.filter_by_instrument_checkbox.clicked.connect(self.fill_table)
        self.filter_by_name_checkbox.clicked.connect(self.fill_table)
        self.filter_by_rec_checkbox.clicked.connect(self.fill_table)
        self.filter_by_dec_checkbox.clicked.connect(self.fill_table)
        self.filter_by_type_checkbox.clicked.connect(self.fill_table)
        self.filter_by_mag_checkbox.clicked.connect(self.fill_table)
        self.filter_by_note_checkbox.clicked.connect(self.fill_table)
        self.filter_name_key1.textChanged.connect(self.fill_table)
        self.filter_name_key2.textChanged.connect(self.fill_table)
        self.filter_note_key1.textChanged.connect(self.fill_table)
        self.filter_note_key2.textChanged.connect(self.fill_table)
        self.filter_rec_h_start.valueChanged.connect(self.fill_table)
        self.filter_rec_m_start.valueChanged.connect(self.fill_table)
        self.filter_rec_s_start.valueChanged.connect(self.fill_table)
        self.filter_rec_h_end.valueChanged.connect(self.fill_table)
        self.filter_rec_m_end.valueChanged.connect(self.fill_table)
        self.filter_rec_s_end.valueChanged.connect(self.fill_table)
        self.filter_dec_h_start.valueChanged.connect(self.fill_table)
        self.filter_dec_m_start.valueChanged.connect(self.fill_table)
        self.filter_dec_s_start.valueChanged.connect(self.fill_table)
        self.filter_dec_h_end.valueChanged.connect(self.fill_table)
        self.filter_dec_m_end.valueChanged.connect(self.fill_table)
        self.filter_dec_s_end.valueChanged.connect(self.fill_table)
        self.filter_mag_start.valueChanged.connect(self.fill_table)
        self.filter_mag_end.valueChanged.connect(self.fill_table)
        self.constilation_combobox.currentTextChanged.connect(self.fill_table)
        self.constilation_checkbox.clicked.connect(self.fill_table)
        self.filter_type_key1.currentTextChanged.connect(self.fill_table)
        self.filter_type_key2.currentTextChanged.connect(self.fill_table)
        self.filter_type_key3.currentTextChanged.connect(self.fill_table)
        self.filter_type_key4.currentTextChanged.connect(self.fill_table)
        self.filter_note_bool.currentTextChanged.connect(self.fill_table)
        self.objects_table.itemSelectionChanged.connect(self.fill_object)
        self.show_lightcurve_checkbox.clicked.connect(self.show_lightcurve)

        # objekt
        self.pair_a_checkbox.clicked.connect(self.fill_object)
        self.pair_b_checkbox.clicked.connect(self.fill_object)
        self.pair_c_checkbox.clicked.connect(self.fill_object)
        self.pair_d_checkbox.clicked.connect(self.fill_object)
        self.pair_e_checkbox.clicked.connect(self.fill_object)
        self.pair_f_checkbox.clicked.connect(self.fill_object)

        # comp
        self.comperison_combobox.currentTextChanged.connect(self.fill_comp)

        self.object_show_detail_checkbox.clicked.connect(self.show_prediction)

        self.object_clear_filter_button.clicked.connect(self.clear_filter)
        self.h_spinbox.valueChanged.connect(self.h_changed)
        self.select_user_checkbox.clicked.connect(self.add_user_to_list)
        self.select_place_checkbox.clicked.connect(self.add_place_to_list)
        self.select_instrument_checkbox.clicked.connect(self.add_instrument_to_list)
        self.in_prediction_checkbox.clicked.connect(self.in_prediction_changed)

    def version(self):
        a = Popup("Program Info", "Version {0}\nPowered by Python\nAuthor: {1}".format(self.__version, self.__author))
        a.do()

    def show_lightcurve(self):
        self.show_lightcurve_checkbox.setChecked(True)
        self.prediction2.lightcurve_window.time_home()
        self.prediction2.show_lightcurve()

    def rename_user(self):
        if self.user_combobox.currentText() == "add user":
            return
        else:
            self.setEnabled(False)
            self.rename_user_window.show()


    def set_place(self):
        if self.observer_combobox.currentText() in ["add user", "add place"]:
            return
        else:
            self.edit_place_window.fill_place()
            self.edit_place_window.show()

    def set_instrument(self):
        if self.instrument_combobox.currentText() in ["add instrument", "add place", "Add telescope"]:
            return
        else:
            self.edit_instrument_window.fill_instrument()
            self.edit_instrument_window.show()

    def show_observation(self):
        self.observation_log_window.show()

    def check_variability(self):
        self.known_variable_window.show()

    def photometry_setting(self):
        self.tess_menu_window_setting.show()

    def show_catalog_number(self):
        if self.catalog_combobox.currentIndex() == 0:
            self.catalog_number_label.setText(self.star_detail.ucac4())
        elif self.catalog_combobox.currentIndex() == 1:
            self.catalog_number_label.setText(self.star_detail.usnob1())
        elif self.catalog_combobox.currentIndex() == 2:
            self.catalog_number_label.setText(self.star_detail.gaia())
        elif self.catalog_combobox.currentIndex() == 3:
            self.catalog_number_label.setText(self.star_detail.vsx())
        elif self.catalog_combobox.currentIndex() == 4:
            self.catalog_number_label.setText(self.star_detail.asassn())
        elif self.catalog_combobox.currentIndex() == 5:
            self.catalog_number_label.setText(self.star_detail.tess())
        else:
            pass

    def show_catalog(self):
        if self.catalog_combobox.currentIndex() == 0:
            self.ucac4_cross_info()
        elif self.catalog_combobox.currentIndex() == 1:
            self.usno_cross_info()
        elif self.catalog_combobox.currentIndex() == 2:
            self.gaia_cross_info()
        elif self.catalog_combobox.currentIndex() == 3:
            self.vsx_cross_info()
        elif self.catalog_combobox.currentIndex() == 4:
            self.asas_cross_info()
        elif self.catalog_combobox.currentIndex() == 5:
            self.tess_cross_info()
        else:
            pass

    def tess_menu_window_start(self):
        self.tess_menu_window.show()

    def delete_star(self):
        if self.star_id_editline.text():
            id_star = str(self.star_detail.id())
            star = self.star_detail.name()
            a = Popup("Delete star",
                      "You really want to DELETE\nStar id: {0}\nName: {1}\n ".format(id_star, star),
                      buttons="Delete,Exit".split(","))
            if a.do() == 1:
                return
            self.object_edit_window.close()
            self.ucac4_window.close()
            self.usno_window.close()
            self.gaia_window.close()
            self.vsx_window.close()
            self.asas_window.close()
            self.tess_window.close()
            self.prediction2.close()
            self.stars.delete_star(self.star_detail)
            delete_comperison_list = []
            for i, star in enumerate(self.stars.stars):
                if str(star.comp0()) == id_star:
                    self.stars.stars[i].change_comp0(0)
                    delete_comperison_list.append(star.name())
                if str(star.comp1()) == id_star:
                    self.stars.stars[i].change_comp1(0)
                    delete_comperison_list.append(star.name())
                if str(star.comp2()) == id_star:
                    self.stars.stars[i].change_comp2(0)
                    delete_comperison_list.append(star.name())
                if str(star.comp3()) == id_star:
                    self.stars.stars[i].change_comp3(0)
                    delete_comperison_list.append(star.name())
                if str(star.comp4()) == id_star:
                    self.stars.stars[i].change_comp4(0)
                    delete_comperison_list.append(star.name())
                if str(star.comp5()) == id_star:
                    self.stars.stars[i].change_comp5(0)
                    delete_comperison_list.append(star.name())
                if str(star.comp6()) == id_star:
                    self.stars.stars[i].change_comp6(0)
                    delete_comperison_list.append(star.name())
                if str(star.comp7()) == id_star:
                    self.stars.stars[i].change_comp7(0)
                    delete_comperison_list.append(star.name())
                if str(star.comp8()) == id_star:
                    self.stars.stars[i].change_comp8(0)
                    delete_comperison_list.append(star.name())
                if str(star.comp9()) == id_star:
                    self.stars.stars[i].change_comp9(0)
                    delete_comperison_list.append(star.name())
                if str(star.chk1()) == id_star:
                    self.stars.stars[i].change_chk1(0)
                    delete_comperison_list.append(star.name())
            if delete_comperison_list:
                a = Popup("Comperison stars deleted",
                          "The removed star was listed as a comparison for the following objects\n"
                          + "\n".join(delete_comperison_list))
                a.do()
            self.fill_table()
            self.fill_object()
            self.pair_a_checkbox.setChecked(True)
            self.fill_comp()
        else:
            return

    def delete_pair(self):
        if self.star_id_editline.text():
            if not self.star_detail.variability():
                a = Popup("No pairs", "It is a comparison star, there is no pair")
                a.do()
                return
            id_star = self.star_detail.id()
            table_index = self.objects_table.currentRow()
            star = self.star_detail.name()
            pair = self.actual_variable.pair()
            all_star_variables = []
            for variable in self.variable.variables:
                if variable.name() == star:
                    all_star_variables.append(variable)
            if len(all_star_variables) < 2:
                a = Popup("No pairs", "There's only one pair, remove the whole object")
                a.do()
                return
            a = Popup("Delete pair",
                      "You really want to DELETE\nPair {2}\nStar id: {0}\nName: {1}\n ".format(id_star, star, pair),
                      buttons="Delete,Exit".split(","))
            if a.do() == 1:
                return
            self.object_edit_window.close()
            self.ucac4_window.close()
            self.usno_window.close()
            self.gaia_window.close()
            self.vsx_window.close()
            self.asas_window.close()
            self.tess_window.close()
            self.prediction2.close()
            self.variable.delete_variable(self.actual_variable)
            self.fill_table()
            self.fill_object()
            self.pair_a_checkbox.setChecked(True)
            self.fill_comp()
        else:
            return

    def in_prediction_changed(self):
        self.actual_variable.change_in_prediction(self.in_prediction_checkbox.isChecked())
        # self.fill_table()

    def show_prediction_click(self):
        self.object_show_detail_checkbox.setChecked(True)
        self.show_prediction()


    def add_model_quickly(self):
        if self.objects_table.currentRow() > -1:
            self.object_edit_window.setWindowIcon(QtGui.QIcon("star--pencil.png"))
            self.object_edit_window.fill_form()
            self.object_edit_window.show()
            self.object_edit_window.import_model(import_defined="file")

    def edit_object(self):
        if self.objects_table.currentRow() == -1:
            self.new_object()
        else:
            self.object_edit_window.setWindowIcon(QtGui.QIcon("star--pencil.png"))
            self.object_edit_window.fill_form()
            self.object_edit_window.show()

    def new_object(self):
        self.object_edit_window.setWindowIcon(QtGui.QIcon("star--plus.png"))
        self.object_edit_window.new_object_checkbox.setChecked(True)
        self.object_edit_window.new_button()
        self.object_edit_window.show()

    def __build(self):
        # USER widgets and layouts
        observer_group_box = QtWidgets.QGroupBox("User and Observation site")
        observer_group_layout = QtWidgets.QGridLayout()
        observer_group_box.setLayout(observer_group_layout)
        self.user_combobox = QtWidgets.QComboBox()
        self.user_combobox.setMinimumWidth(100)
        user_label = QtWidgets.QLabel("User/Place:")

        self.observer_combobox = QtWidgets.QComboBox()
        instrument_label = QtWidgets.QLabel("Instrument set: ")
        self.instrument_combobox = QtWidgets.QComboBox()
        self.latitude_label = QtWidgets.QLabel("00h 00m 00s")
        self.longitude_label = QtWidgets.QLabel("00h 00m 00s")

        h_label = QtWidgets.QLabel("star h(min):")

        self.h_spinbox = QtWidgets.QDoubleSpinBox()
        self.h_spinbox.setRange(0, 80)

        sun_h_set_label = QtWidgets.QLabel("Sun - max h(°):")
        self.sun_h_set_spinbox = QtWidgets.QDoubleSpinBox()
        self.sun_h_set_spinbox.setRange(-40, 50)
        self.sun_h_set_spinbox.setValue(-12.00)

        observer_group_layout.addWidget(user_label, 0, 0)
        observer_group_layout.addWidget(self.user_combobox, 0, 1, 1, 2)
        observer_group_layout.addWidget(self.observer_combobox, 0, 3, 1, 2)
        observer_group_layout.addWidget(self.latitude_label, 1, 4)
        observer_group_layout.addWidget(self.longitude_label, 1, 3)
        observer_group_layout.addWidget(h_label, 2, 0)
        observer_group_layout.addWidget(self.h_spinbox, 2, 1)
        observer_group_layout.addWidget(instrument_label, 1, 0)
        observer_group_layout.addWidget(self.instrument_combobox, 1, 1, 1, 2)
        observer_group_layout.addWidget(sun_h_set_label, 2, 2, 1, 2)
        observer_group_layout.addWidget(self.sun_h_set_spinbox, 2, 4, 1, 1)
        self.main_page_layout.addWidget(observer_group_box, 0, 0, 5, 3)


        # PERIOD START Widgets and Layout
        period_group_box = QtWidgets.QGroupBox("Observation time range")
        period_group_layout = QtWidgets.QGridLayout()
        period_group_box.setLayout(period_group_layout)
        self.period_start_dateedit = QtWidgets.QDateEdit()
        self.period_start_timeedit = QtWidgets.QTimeEdit()
        self.period_start_timeedit.setTime(time(hour=17))

        period_group_layout.addWidget(QtWidgets.QLabel("Start:"), 0, 0, 1, 1, QtCore.Qt.AlignRight)
        period_group_layout.addWidget(self.period_start_dateedit, 0, 1, 1, 1, QtCore.Qt.AlignRight)
        period_group_layout.addWidget(self.period_start_timeedit, 0, 2, 1, 1, QtCore.Qt.AlignRight)
        period_group_layout.addWidget(QtWidgets.QLabel("End:"), 0, 3, 1, 1, QtCore.Qt.AlignRight)

        # PERIOD START Widgets and Layout
        self.period_end_dateedit = QtWidgets.QDateEdit()
        self.period_end_timeedit = QtWidgets.QTimeEdit(time(hour=17))
        local_star_time_label = QtWidgets.QLabel("LST now:")
        local_jd_now_label = QtWidgets.QLabel("Local JD now:")
        julian_date_label = QtWidgets.QLabel("JD:")
        self.local_star_time_label = QtWidgets.QLabel("")
        self.julian_date_start_label = QtWidgets.QLabel("")
        self.julian_date_start_label.setWhatsThis("julian day")
        self.local_jd_now_label = QtWidgets.QLabel("")
        self.julian_date_end_label = QtWidgets.QLabel("")

        period_group_layout.addWidget(self.period_end_dateedit, 0, 4, 1, 1, QtCore.Qt.AlignRight)
        period_group_layout.addWidget(self.period_end_timeedit, 0, 5, 1, 1, QtCore.Qt.AlignRight)
        period_group_layout.addWidget(julian_date_label, 1, 0, 1, 1, QtCore.Qt.AlignRight)
        period_group_layout.addWidget(self.julian_date_start_label, 1, 1, 1, 2, QtCore.Qt.AlignRight)
        period_group_layout.addWidget(self.julian_date_end_label, 1, 4, 1, 2, QtCore.Qt.AlignRight)
        period_group_layout.addWidget(local_star_time_label, 2, 0, 1, 1, QtCore.Qt.AlignRight)
        period_group_layout.addWidget(local_jd_now_label, 2, 2, 1, 2, QtCore.Qt.AlignRight)
        period_group_layout.addWidget(self.local_star_time_label, 2, 1, 1, 1, QtCore.Qt.AlignRight)
        period_group_layout.addWidget(self.local_jd_now_label, 2, 4, 1, 2, QtCore.Qt.AlignRight)

        self.main_page_layout.addWidget(period_group_box, 0, 4, 5, 4)


        # FLAT Widgets and Layout
        flat_group_box = QtWidgets.QGroupBox("Flat Information")
        flat_group_layout = QtWidgets.QGridLayout()
        flat_group_box.setLayout(flat_group_layout)
        flat_sunset_label = QtWidgets.QLabel("S.set")
        flat_sunrise_label = QtWidgets.QLabel("S.rise")
        label_texts_flat = ("Sun position:", "Sunset:", "Sunrise:")
        for i, text in enumerate(label_texts_flat):
            text_label = QtWidgets.QLabel(text)
            flat_group_layout.addWidget(text_label, i, 0, 1, 1, QtCore.Qt.AlignRight)

        self.flat_h_spinbox = QtWidgets.QDoubleSpinBox()
        self.flat_h_spinbox.setRange(-18, 50)
        self.flat_h_spinbox.setValue(-7)
        self.flat_a_spinbox_sunset = QtWidgets.QSpinBox()
        self.flat_a_spinbox_sunset.setRange(0, 360)
        self.flat_a_spinbox_sunset.setValue(90)
        self.flat_h_spinbox_sunset = QtWidgets.QSpinBox()
        self.flat_h_spinbox_sunset.setRange(10, 90)
        self.flat_h_spinbox_sunset.setValue(55)
        self.flat_a_spinbox_sunrise = QtWidgets.QSpinBox()
        self.flat_a_spinbox_sunrise.setRange(0, 360)
        self.flat_a_spinbox_sunrise.setValue(270)
        self.flat_h_spinbox_sunrise = QtWidgets.QSpinBox()
        self.flat_h_spinbox_sunrise.setRange(0, 90)
        self.flat_h_spinbox_sunrise.setValue(55)

        self.flat_time_sunset_label = QtWidgets.QLabel()
        self.flat_time_sunrise_label = QtWidgets.QLabel()
        self.flat_rec_sunset_label = QtWidgets.QLabel()
        self.flat_rec_sunrise_label = QtWidgets.QLabel()
        self.flat_dec_sunset_label = QtWidgets.QLabel()
        self.flat_dec_sunrise_label = QtWidgets.QLabel()

        flat_group_layout.addWidget(self.flat_h_spinbox, 0, 1)
        flat_group_layout.addWidget(flat_sunset_label, 0, 2, 1, 1, QtCore.Qt.AlignCenter)
        flat_group_layout.addWidget(self.flat_a_spinbox_sunset, 0, 3)
        flat_group_layout.addWidget(self.flat_h_spinbox_sunset, 0, 4)
        flat_group_layout.addWidget(flat_sunrise_label, 0, 5, 1, 1, QtCore.Qt.AlignCenter)
        flat_group_layout.addWidget(self.flat_a_spinbox_sunrise, 0, 6)
        flat_group_layout.addWidget(self.flat_h_spinbox_sunrise, 0, 7)
        flat_group_layout.addWidget(self.flat_rec_sunset_label, 1, 1, 1, 2)
        flat_group_layout.addWidget(self.flat_dec_sunset_label, 1, 3, 1, 2)
        flat_group_layout.addWidget(self.flat_time_sunset_label, 1, 5, 1, 2)
        flat_group_layout.addWidget(self.flat_rec_sunrise_label, 2, 1, 1, 2)
        flat_group_layout.addWidget(self.flat_dec_sunrise_label, 2, 3, 1, 2)
        flat_group_layout.addWidget(self.flat_time_sunrise_label, 2, 5, 1, 2)

        self.main_page_layout.addWidget(flat_group_box, 0, 8, 5, 5)

        # SUN / MOON Info Widgets and Layout
        sun_group_box = QtWidgets.QGroupBox("Sun and Moon information")
        sun_group_layout = QtWidgets.QGridLayout()
        sun_group_box.setLayout(sun_group_layout)

        self.sun_start_checkbox = QtWidgets.QRadioButton("Start")
        self.sun_start_checkbox.setChecked(True)
        self.sun_end_checkbox = QtWidgets.QRadioButton("End")
        self.sun_settime_checkbox = QtWidgets.QRadioButton("Set Date")
        self.sun_settime_dateedit = QtWidgets.QDateEdit(datetime.now())
        self.group_checkbox = QtWidgets.QButtonGroup()
        self.group_checkbox.addButton(self.sun_start_checkbox, 1)
        self.group_checkbox.addButton(self.sun_end_checkbox, 1)
        self.group_checkbox.addButton(self.sun_settime_checkbox, 1)

        sun_group_layout.addWidget(self.sun_start_checkbox, 0, 0, 1, 1)
        sun_group_layout.addWidget(self.sun_end_checkbox, 0, 1, 1, 1)
        sun_group_layout.addWidget(self.sun_settime_checkbox, 1, 0, 1, 1)
        sun_group_layout.addWidget(self.sun_settime_dateedit, 1, 1, 1, 1)

        label_texts = ("sunset(0°):",  "naut.dusk(-12°):", "ast.dusk(-18°)", "", "", "ast.dawn(-18°):",
                       "naut.dawn(-12°):", "sunrise(0°):", "MOON ", "Moonrise: ", "Moonset: ", "Moon phase:")
        for i, text in enumerate(label_texts):
            text_label = QtWidgets.QLabel(text)
            sun_group_layout.addWidget(text_label, i + 2, 0, 1, 1, QtCore.Qt.AlignRight)

        self.set_dust_label = QtWidgets.QLabel("set h dusk({0}°):".format(str(int(self.sun_h_set_spinbox.value()))))
        self.set_dawn_label = QtWidgets.QLabel("set h dawn({0}°):".format(str(int(self.sun_h_set_spinbox.value()))))
        sun_group_layout.addWidget(self.set_dust_label, 5, 0, 1, 1, QtCore.Qt.AlignRight)
        sun_group_layout.addWidget(self.set_dawn_label, 6, 0, 1, 1, QtCore.Qt.AlignRight)

        self.sun_sunset_label = QtWidgets.QLabel()
        self.sun_nautdusk_label = QtWidgets.QLabel()
        self.sun_astdusk_label = QtWidgets.QLabel()
        self.sun_sethdusk_label = QtWidgets.QLabel()
        self.sun_sethdawn_label = QtWidgets.QLabel()
        self.sun_astdawn_label = QtWidgets.QLabel()
        self.sun_nautdawn_label = QtWidgets.QLabel()
        self.sun_sunrise_label = QtWidgets.QLabel()
        self.sun_moonrise_label = QtWidgets.QLabel()
        self.sun_moonset_label = QtWidgets.QLabel()
        self.sun_moonfase_label = QtWidgets.QLabel()

        sun_group_layout.addWidget(self.sun_sunset_label, 2, 1, 1, 1, QtCore.Qt.AlignCenter)
        sun_group_layout.addWidget(self.sun_nautdusk_label, 3, 1, 1, 1, QtCore.Qt.AlignCenter)
        sun_group_layout.addWidget(self.sun_astdusk_label, 4, 1, 1, 1, QtCore.Qt.AlignCenter)
        sun_group_layout.addWidget(self.sun_sethdusk_label, 5, 1, 1, 1, QtCore.Qt.AlignCenter)
        sun_group_layout.addWidget(self.sun_sethdawn_label, 6, 1, 1, 1, QtCore.Qt.AlignCenter)
        sun_group_layout.addWidget(self.sun_astdawn_label, 7, 1, 1, 1, QtCore.Qt.AlignCenter)
        sun_group_layout.addWidget(self.sun_nautdawn_label, 8, 1, 1, 1, QtCore.Qt.AlignCenter)
        sun_group_layout.addWidget(self.sun_sunrise_label, 9, 1, 1, 1, QtCore.Qt.AlignCenter)
        sun_group_layout.addWidget(self.sun_moonrise_label, 11, 1, 1, 1, QtCore.Qt.AlignCenter)
        sun_group_layout.addWidget(self.sun_moonset_label, 12, 1, 1, 1, QtCore.Qt.AlignCenter)
        sun_group_layout.addWidget(self.sun_moonfase_label, 13, 1, 1, 1, QtCore.Qt.AlignCenter)

        self.main_page_layout.addWidget(sun_group_box, 0, 13, 17, 2)

        # OBJECT
        self.object_group_box = QtWidgets.QGroupBox(
            "OBSERVED OBJECT - choice, add, delete, import, sort or see detail of observed object")
        object_group_layout = QtWidgets.QGridLayout()
        self.object_group_box.setLayout(object_group_layout)

        self.objects_table = QtWidgets.QTableWidget()

        self.object_show_detail_checkbox = QtWidgets.QCheckBox("Show Prediction")
        self.show_lightcurve_checkbox = QtWidgets.QCheckBox("Show Lightcurve")
        self.object_clear_filter_button = QtWidgets.QPushButton("Clear Filter")

        self.sort_by_combobox = QtWidgets.QComboBox()
        self.sort_by_combobox.addItems(["Name", "Alt.name", "RA", "DE", "Type", "Mag"])
        self.sort_by_combobox.setCurrentIndex(0)

        filter_by_group_box = QtWidgets.QGroupBox("Filtred by")
        filter_by_group_layout = QtWidgets.QVBoxLayout()
        filter_by_user_layout = QtWidgets.QHBoxLayout()
        filter_by_id_layout = QtWidgets.QHBoxLayout()
        filter_by_rec_layout = QtWidgets.QHBoxLayout()
        filter_by_dec_layout = QtWidgets.QHBoxLayout()
        filter_by_type_layout = QtWidgets.QHBoxLayout()
        filter_by_mag_layout = QtWidgets.QHBoxLayout()
        filter_by_note_layout = QtWidgets.QHBoxLayout()

        filter_by_group_box.setLayout(filter_by_group_layout)
        self.filter_by_var_checkbox = QtWidgets.QCheckBox("Variable")
        self.filter_by_var_checkbox.setChecked(True)
        self.filter_by_user_checkbox = QtWidgets.QCheckBox("User marked")
        self.filter_by_user_checkbox.setChecked(False)
        self.filter_by_place_checkbox = QtWidgets.QCheckBox("Place marked")
        self.filter_by_place_checkbox.setChecked(False)
        self.filter_by_instrument_checkbox = QtWidgets.QCheckBox("Instrument marked")
        self.filter_by_instrument_checkbox.setChecked(False)
        self.filter_by_name_checkbox = QtWidgets.QCheckBox("Name")
        filter_by_user_layout.addWidget(self.filter_by_var_checkbox)
        filter_by_user_layout.addWidget(self.filter_by_user_checkbox)
        filter_by_user_layout.addWidget(self.filter_by_place_checkbox)
        filter_by_user_layout.addWidget(self.filter_by_instrument_checkbox)

        self.filter_name_key1 = QtWidgets.QLineEdit()
        self.filter_name_key2 = QtWidgets.QLineEdit()
        filter_alt_name_label = QtWidgets.QLabel("Alt.name: ")
        filter_by_id_layout.addWidget(self.filter_by_name_checkbox)
        filter_by_id_layout.addWidget(self.filter_name_key1)
        filter_by_id_layout.addWidget(filter_alt_name_label)
        filter_by_id_layout.addWidget(self.filter_name_key2)

        self.filter_by_rec_checkbox = QtWidgets.QCheckBox("RA")
        self.filter_rec_h_start = QtWidgets.QSpinBox()
        self.filter_rec_h_start.setRange(0, 23)
        filter_rec_start_h_label = QtWidgets.QLabel("h")
        self.filter_rec_m_start = QtWidgets.QSpinBox()
        self.filter_rec_m_start.setRange(0, 59)
        filter_rec_start_m_label = QtWidgets.QLabel("m")
        self.filter_rec_s_start = QtWidgets.QSpinBox()
        self.filter_rec_s_start.setRange(0, 59)
        filter_rec_start_s_label = QtWidgets.QLabel("s ")
        self.filter_rec_h_end = QtWidgets.QSpinBox()
        self.filter_rec_h_end.setRange(0, 23)
        filter_rec_end_h_label = QtWidgets.QLabel("h")
        self.filter_rec_m_end = QtWidgets.QSpinBox()
        self.filter_rec_m_end.setRange(0, 59)
        filter_rec_end_m_label = QtWidgets.QLabel("m")
        self.filter_rec_s_end = QtWidgets.QSpinBox()
        self.filter_rec_s_end.setRange(0, 59)
        filter_rec_end_s_label = QtWidgets.QLabel("s")
        filter_by_rec_layout.addWidget(self.filter_by_rec_checkbox)
        filter_by_rec_layout.addWidget(self.filter_rec_h_start)
        filter_by_rec_layout.addWidget(filter_rec_start_h_label)
        filter_by_rec_layout.addWidget(self.filter_rec_m_start)
        filter_by_rec_layout.addWidget(filter_rec_start_m_label)
        filter_by_rec_layout.addWidget(self.filter_rec_s_start)
        filter_by_rec_layout.addWidget(filter_rec_start_s_label)
        filter_by_rec_layout.addWidget(self.filter_rec_h_end)
        filter_by_rec_layout.addWidget(filter_rec_end_h_label)
        filter_by_rec_layout.addWidget(self.filter_rec_m_end)
        filter_by_rec_layout.addWidget(filter_rec_end_m_label)
        filter_by_rec_layout.addWidget(self.filter_rec_s_end)
        filter_by_rec_layout.addWidget(filter_rec_end_s_label)

        self.filter_by_dec_checkbox = QtWidgets.QCheckBox("DE")
        self.filter_dec_h_start = QtWidgets.QSpinBox()
        self.filter_dec_h_start.setRange(-89, 89)
        filter_dec_start_h_label = QtWidgets.QLabel("°")
        self.filter_dec_m_start = QtWidgets.QSpinBox()
        self.filter_dec_m_start.setRange(0, 59)
        filter_dec_start_m_label = QtWidgets.QLabel("'")
        self.filter_dec_s_start = QtWidgets.QSpinBox()
        self.filter_dec_s_start.setRange(0, 59)
        filter_dec_start_s_label = QtWidgets.QLabel('"')
        self.filter_dec_h_end = QtWidgets.QSpinBox()
        self.filter_dec_h_end.setRange(-89, 89)
        filter_dec_end_h_label = QtWidgets.QLabel("°")
        self.filter_dec_m_end = QtWidgets.QSpinBox()
        self.filter_dec_m_end.setRange(0, 59)
        filter_dec_end_m_label = QtWidgets.QLabel("'")
        self.filter_dec_s_end = QtWidgets.QSpinBox()
        self.filter_dec_s_end.setRange(0, 59)
        filter_dec_end_s_label = QtWidgets.QLabel('"')
        filter_by_dec_layout.addWidget(self.filter_by_dec_checkbox)
        filter_by_dec_layout.addWidget(self.filter_dec_h_start)
        filter_by_dec_layout.addWidget(filter_dec_start_h_label)
        filter_by_dec_layout.addWidget(self.filter_dec_m_start)
        filter_by_dec_layout.addWidget(filter_dec_start_m_label)
        filter_by_dec_layout.addWidget(self.filter_dec_s_start)
        filter_by_dec_layout.addWidget(filter_dec_start_s_label)
        filter_by_dec_layout.addWidget(self.filter_dec_h_end)
        filter_by_dec_layout.addWidget(filter_dec_end_h_label)
        filter_by_dec_layout.addWidget(self.filter_dec_m_end)
        filter_by_dec_layout.addWidget(filter_dec_end_m_label)
        filter_by_dec_layout.addWidget(self.filter_dec_s_end)
        filter_by_dec_layout.addWidget(filter_dec_end_s_label)

        self.filter_by_type_checkbox = QtWidgets.QCheckBox("Type")
        self.filter_type_key1 = QtWidgets.QComboBox()
        self.filter_type_key2 = QtWidgets.QComboBox()
        self.filter_type_key3 = QtWidgets.QComboBox()
        self.filter_type_key4 = QtWidgets.QComboBox()

        filter_by_type_layout.addWidget(self.filter_by_type_checkbox)
        filter_by_type_layout.addWidget(self.filter_type_key1)
        filter_by_type_layout.addWidget(self.filter_type_key2)
        filter_by_type_layout.addWidget(self.filter_type_key3)
        filter_by_type_layout.addWidget(self.filter_type_key4)

        self.filter_by_mag_checkbox = QtWidgets.QCheckBox("Mag")
        self.filter_mag_start = QtWidgets.QDoubleSpinBox()
        self.filter_mag_start.setRange(-2, 25)
        filter_mag_start_label = QtWidgets.QLabel("mag to ")
        self.filter_mag_end = QtWidgets.QDoubleSpinBox()
        self.filter_mag_end.setRange(-2, 25)
        filter_mag_end_label = QtWidgets.QLabel("mag")
        self.constilation_checkbox = QtWidgets.QCheckBox("Const.")
        self.constilation_combobox = QtWidgets.QComboBox()
        filter_by_mag_layout.addWidget(self.filter_by_mag_checkbox)
        filter_by_mag_layout.addWidget(self.filter_mag_start)
        filter_by_mag_layout.addWidget(filter_mag_start_label)
        filter_by_mag_layout.addWidget(self.filter_mag_end)
        filter_by_mag_layout.addWidget(filter_mag_end_label)
        filter_by_mag_layout.addWidget(self.constilation_checkbox)
        filter_by_mag_layout.addWidget(self.constilation_combobox)

        self.filter_by_note_checkbox = QtWidgets.QCheckBox("Note")
        self.filter_note_key1 = QtWidgets.QLineEdit()
        self.filter_note_key2 = QtWidgets.QLineEdit()
        self.filter_note_bool = QtWidgets.QComboBox()
        self.filter_note_bool.addItem("and")
        self.filter_note_bool.addItem("or")
        filter_by_note_layout.addWidget(self.filter_by_note_checkbox)
        filter_by_note_layout.addWidget(self.filter_note_key1)
        filter_by_note_layout.addWidget(self.filter_note_bool)
        filter_by_note_layout.addWidget(self.filter_note_key2)

        filter_by_group_layout.addLayout(filter_by_user_layout)
        filter_by_group_layout.addLayout(filter_by_id_layout)
        filter_by_group_layout.addLayout(filter_by_rec_layout)
        filter_by_group_layout.addLayout(filter_by_dec_layout)
        filter_by_group_layout.addLayout(filter_by_type_layout)
        filter_by_group_layout.addLayout(filter_by_mag_layout)
        filter_by_group_layout.addLayout(filter_by_note_layout)

        object_group_layout.addWidget(self.objects_table, 0, 0, 7, 10)
        object_group_layout.addWidget(self.object_show_detail_checkbox, 0, 10, 1, 1)
        object_group_layout.addWidget(self.show_lightcurve_checkbox, 0, 11, 1, 1)
        object_group_layout.addWidget(self.object_clear_filter_button, 0, 12, 1, 1)
        object_group_layout.addWidget(QtWidgets.QLabel("Sort by:"), 0, 13, 1, 1)
        object_group_layout.addWidget(self.sort_by_combobox, 0, 14, 1, 1)

        object_group_layout.addWidget(filter_by_group_box, 1, 10, 6, 6)

        self.main_page_layout.addWidget(self.object_group_box, 5, 0, 12, 13)

        # OBJECT DETAIL Widgets and Layout

        # pair
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

        # pair in prediction
        self.in_prediction_checkgroup = QtWidgets.QGroupBox("Prediction yes/no")
        in_prediction_layout = QtWidgets.QHBoxLayout()
        self.in_prediction_checkgroup.setLayout(in_prediction_layout)

        self.in_prediction_checkbox = QtWidgets.QCheckBox("Show in prediction")
        in_prediction_layout.addWidget(self.in_prediction_checkbox)

        self.comp_checkgroup = QtWidgets.QGroupBox("Choice comparison star")
        comp1_layout = QtWidgets.QHBoxLayout()
        self.comp_checkgroup.setLayout(comp1_layout)

        self.comperison_combobox = QtWidgets.QComboBox()

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

        comp1_layout.addWidget(self.comperison_combobox)

        # choice objects for user, place or instrument
        self.select_checkgroup = QtWidgets.QGroupBox("Mark stars")
        select_layout = QtWidgets.QHBoxLayout()
        self.select_checkgroup.setLayout(select_layout)

        self.select_user_checkbox = QtWidgets.QCheckBox("User")
        self.select_user_checkbox.setChecked(True)
        self.select_place_checkbox = QtWidgets.QCheckBox("Place")
        self.select_place_checkbox.setChecked(True)
        self.select_instrument_checkbox = QtWidgets.QCheckBox("Instrument")
        self.select_instrument_checkbox.setChecked(True)

        select_layout.addWidget(self.select_user_checkbox)
        select_layout.addWidget(self.select_place_checkbox)
        select_layout.addWidget(self.select_instrument_checkbox)

        # star parametrs
        star_groupbox = QtWidgets.QGroupBox("Star parameters")
        star_layout = QtWidgets.QVBoxLayout()
        star_groupbox.setLayout(star_layout)
        self.star_id_editline = QtWidgets.QLineEdit()
        self.star_name_editline = QtWidgets.QLineEdit()
        self.star_alternativ_name_editline = QtWidgets.QLineEdit()
        self.star_ekvinokcium_editline = QtWidgets.QLineEdit()
        self.star_constilation_editline = QtWidgets.QLineEdit()
        self.star_rec_editline = QtWidgets.QLineEdit()
        self.star_dec_editline = QtWidgets.QLineEdit()
        self.star_rec_now_editline = QtWidgets.QLineEdit()
        self.star_dec_now_editline = QtWidgets.QLineEdit()
        self.star_mag_editline = QtWidgets.QLineEdit()
        self.star_type_editline = QtWidgets.QLineEdit()
        self.star_b_v_editline = QtWidgets.QLineEdit()
        self.star_j_k_editline = QtWidgets.QLineEdit()

        self.star_id_editline.setAlignment(QtCore.Qt.AlignRight)
        self.star_name_editline.setAlignment(QtCore.Qt.AlignRight)
        self.star_alternativ_name_editline.setAlignment(QtCore.Qt.AlignRight)
        self.star_ekvinokcium_editline.setAlignment(QtCore.Qt.AlignRight)
        self.star_constilation_editline.setAlignment(QtCore.Qt.AlignRight)
        self.star_rec_editline.setAlignment(QtCore.Qt.AlignRight)
        self.star_dec_editline.setAlignment(QtCore.Qt.AlignRight)
        self.star_rec_now_editline.setAlignment(QtCore.Qt.AlignRight)
        self.star_dec_now_editline.setAlignment(QtCore.Qt.AlignRight)
        self.star_mag_editline.setAlignment(QtCore.Qt.AlignRight)
        self.star_b_v_editline.setAlignment(QtCore.Qt.AlignRight)
        self.star_j_k_editline.setAlignment(QtCore.Qt.AlignRight)

        self.star_id_editline.setReadOnly(True)
        self.star_name_editline.setReadOnly(True)
        self.star_alternativ_name_editline.setReadOnly(True)
        self.star_ekvinokcium_editline.setReadOnly(True)
        self.star_constilation_editline.setReadOnly(True)
        self.star_rec_editline.setReadOnly(True)
        self.star_dec_editline.setReadOnly(True)
        self.star_rec_now_editline.setReadOnly(True)
        self.star_dec_now_editline.setReadOnly(True)
        self.star_mag_editline.setReadOnly(True)
        self.star_b_v_editline.setReadOnly(True)
        self.star_j_k_editline.setReadOnly(True)

        star_id_label = QtWidgets.QLabel("Star Id:")
        star_name_label = QtWidgets.QLabel("Name:")
        star_alternativ_name_label = QtWidgets.QLabel("Alt.name:")
        star_ekvinokcium_label = QtWidgets.QLabel("eq.:")
        star_constilation_label = QtWidgets.QLabel("Const:")
        star_rec_label = QtWidgets.QLabel("RA/DE eq:")
        star_rec_now_label = QtWidgets.QLabel("RA/DE now:")
        star_mag_label = QtWidgets.QLabel("Mag:")
        star_type_label = QtWidgets.QLabel("Type:")
        star_b_v_label = QtWidgets.QLabel("B-V:")
        star_j_k_label = QtWidgets.QLabel("J-K:")

        self.star_rec_editline.setFixedWidth(83)
        self.star_dec_editline.setFixedWidth(80)
        self.star_rec_now_editline.setFixedWidth(83)
        self.star_dec_now_editline.setFixedWidth(80)
        self.star_mag_editline.setFixedWidth(55)

        star_id_layout = QtWidgets.QHBoxLayout()
        star_id_layout.addWidget(star_id_label)
        star_id_layout.addWidget(self.star_id_editline)
        star_id_layout.addWidget(star_constilation_label)
        star_id_layout.addWidget(self.star_constilation_editline)

        star_name_layout = QtWidgets.QHBoxLayout()
        star_name_layout.addWidget(star_name_label)
        star_name_layout.addWidget(self.star_name_editline)

        star_alt_name_layout = QtWidgets.QHBoxLayout()
        star_alt_name_layout.addWidget(star_alternativ_name_label)
        star_alt_name_layout.addWidget(self.star_alternativ_name_editline)

        star_coor_layout = QtWidgets.QHBoxLayout()
        star_coor_layout.addWidget(star_rec_label)
        star_coor_layout.addWidget(self.star_rec_editline)
        star_coor_layout.addWidget(self.star_dec_editline)

        star_coor_now_layout = QtWidgets.QHBoxLayout()
        star_coor_now_layout.addWidget(star_rec_now_label)
        star_coor_now_layout.addWidget(self.star_rec_now_editline)
        star_coor_now_layout.addWidget(self.star_dec_now_editline)

        star_mag_layout = QtWidgets.QHBoxLayout()
        star_mag_layout.addWidget(star_mag_label)
        star_mag_layout.addWidget(self.star_mag_editline)
        star_mag_layout.addWidget(star_ekvinokcium_label)
        star_mag_layout.addWidget(self.star_ekvinokcium_editline)

        star_type_layout = QtWidgets.QHBoxLayout()
        star_type_layout.addWidget(star_type_label)
        star_type_layout.addWidget(self.star_type_editline)

        star_b_v_layout = QtWidgets.QHBoxLayout()
        star_b_v_layout.addWidget(star_b_v_label)
        star_b_v_layout.addWidget(self.star_b_v_editline)
        star_b_v_layout.addWidget(star_j_k_label)
        star_b_v_layout.addWidget(self.star_j_k_editline)

        star_layout.addLayout(star_id_layout)
        star_layout.addLayout(star_name_layout)
        star_layout.addLayout(star_alt_name_layout)
        star_layout.addLayout(star_coor_layout)
        star_layout.addLayout(star_coor_now_layout)
        star_layout.addLayout(star_mag_layout)
        star_layout.addLayout(star_type_layout)
        star_layout.addLayout(star_b_v_layout)

        # lightcurve parameters
        lightkurve_groupbox = QtWidgets.QGroupBox("lightcurve parameters")
        lightkurve_layout = QtWidgets.QFormLayout()
        lightkurve_groupbox.setLayout(lightkurve_layout)
        self.lightcurve_period_editline = QtWidgets.QLineEdit()
        self.lightcurve_epoch_editline = QtWidgets.QLineEdit()
        self.lightcurve_type_editline = QtWidgets.QLineEdit()
        self.lightcurve_amplitude_prim_editline = QtWidgets.QLineEdit()
        self.lightcurve_amplitude_sec_editline = QtWidgets.QLineEdit()
        self.lightcurve_d_big_prim_editline = QtWidgets.QLineEdit()
        self.lightcurve_d_big_sec_editline = QtWidgets.QLineEdit()
        self.lightcurve_d_prim_editline = QtWidgets.QLineEdit()
        self.lightcurve_d_sec_editline = QtWidgets.QLineEdit()

        self.lightcurve_period_editline.setAlignment(QtCore.Qt.AlignRight)
        self.lightcurve_epoch_editline.setAlignment(QtCore.Qt.AlignRight)
        self.lightcurve_type_editline.setAlignment(QtCore.Qt.AlignRight)
        self.lightcurve_amplitude_prim_editline.setAlignment(QtCore.Qt.AlignRight)
        self.lightcurve_amplitude_sec_editline.setAlignment(QtCore.Qt.AlignRight)

        self.lightcurve_period_editline.setReadOnly(True)
        self.lightcurve_epoch_editline.setReadOnly(True)
        self.lightcurve_type_editline.setReadOnly(True)
        self.lightcurve_amplitude_prim_editline.setReadOnly(True)
        self.lightcurve_amplitude_sec_editline.setReadOnly(True)
        self.lightcurve_d_big_prim_editline.setReadOnly(True)
        self.lightcurve_d_big_sec_editline.setReadOnly(True)
        self.lightcurve_d_prim_editline.setReadOnly(True)
        self.lightcurve_d_sec_editline.setReadOnly(True)

        lightkurve_layout.addRow(QtWidgets.QLabel("Period: "), self.lightcurve_period_editline)
        lightkurve_layout.addRow(QtWidgets.QLabel("Epoch: "), self.lightcurve_epoch_editline)
        lightkurve_layout.addRow(QtWidgets.QLabel("Var.type: "), self.lightcurve_type_editline)
        lightkurve_layout.addRow(QtWidgets.QLabel("Amp.prim.: "), self.lightcurve_amplitude_prim_editline)
        lightkurve_layout.addRow(QtWidgets.QLabel("Amp.sec.: "), self.lightcurve_amplitude_sec_editline)
        lightkurve_layout.addRow(QtWidgets.QLabel("D prim.(h): "), self.lightcurve_d_big_prim_editline)
        lightkurve_layout.addRow(QtWidgets.QLabel("D sec.(h): "), self.lightcurve_d_big_sec_editline)
        lightkurve_layout.addRow(QtWidgets.QLabel("d prim.(h): "), self.lightcurve_d_prim_editline)
        lightkurve_layout.addRow(QtWidgets.QLabel("d sec.(h): "), self.lightcurve_d_sec_editline)

        # model
        model_groupbox = QtWidgets.QGroupBox("phenomenological model")
        model_layout = QtWidgets.QHBoxLayout()
        model_part1_layout = QtWidgets.QFormLayout()
        model_part2_layout = QtWidgets.QFormLayout()
        model_groupbox.setLayout(model_layout)
        model_layout.addLayout(model_part1_layout)
        model_layout.addLayout(model_part2_layout)
        self.model_mag0_editline = QtWidgets.QLineEdit()
        self.model_sec_phase_editline = QtWidgets.QLineEdit()
        self.model_a_pri_editline = QtWidgets.QLineEdit()
        self.model_d_pri_editline = QtWidgets.QLineEdit()
        self.model_g_pri_editline = QtWidgets.QLineEdit()
        self.model_c_pri_editline = QtWidgets.QLineEdit()
        self.model_a_sec_editline = QtWidgets.QLineEdit()
        self.model_d_sec_editline = QtWidgets.QLineEdit()
        self.model_g_sec_editline = QtWidgets.QLineEdit()
        self.model_c_sec_editline = QtWidgets.QLineEdit()
        self.model_sin1_editline = QtWidgets.QLineEdit()
        self.model_sin2_editline = QtWidgets.QLineEdit()
        self.model_sin3_editline = QtWidgets.QLineEdit()
        self.model_cos1_editline = QtWidgets.QLineEdit()
        self.model_cos2_editline = QtWidgets.QLineEdit()
        self.model_cos3_editline = QtWidgets.QLineEdit()
        self.model_apsid_coef_editline = QtWidgets.QLineEdit()
        self.model_ofset_editline = QtWidgets.QLineEdit()

        self.model_mag0_editline.setReadOnly(True)
        self.model_sec_phase_editline.setReadOnly(True)
        self.model_a_pri_editline.setReadOnly(True)
        self.model_d_pri_editline.setReadOnly(True)
        self.model_g_pri_editline.setReadOnly(True)
        self.model_c_pri_editline.setReadOnly(True)
        self.model_a_sec_editline.setReadOnly(True)
        self.model_d_sec_editline.setReadOnly(True)
        self.model_g_sec_editline.setReadOnly(True)
        self.model_c_sec_editline.setReadOnly(True)
        self.model_sin1_editline.setReadOnly(True)
        self.model_sin2_editline.setReadOnly(True)
        self.model_sin3_editline.setReadOnly(True)
        self.model_cos1_editline.setReadOnly(True)
        self.model_cos2_editline.setReadOnly(True)
        self.model_cos3_editline.setReadOnly(True)
        self.model_apsid_coef_editline.setReadOnly(True)
        self.model_ofset_editline.setReadOnly(True)

        model_part1_layout.addRow(QtWidgets.QLabel("mag0: "), self.model_mag0_editline)
        model_part1_layout.addRow(QtWidgets.QLabel("a_pri: "), self.model_a_pri_editline)
        model_part1_layout.addRow(QtWidgets.QLabel("d_pri: "), self.model_d_pri_editline)
        model_part1_layout.addRow(QtWidgets.QLabel("g_pri: "), self.model_g_pri_editline)
        model_part1_layout.addRow(QtWidgets.QLabel("c_pri: "), self.model_c_pri_editline)
        model_part1_layout.addRow(QtWidgets.QLabel("sin1: "), self.model_sin1_editline)
        model_part1_layout.addRow(QtWidgets.QLabel("sin2: "), self.model_sin2_editline)
        model_part1_layout.addRow(QtWidgets.QLabel("sin3: "), self.model_sin3_editline)
        model_part1_layout.addRow(QtWidgets.QLabel("coef.apsid: "), self.model_apsid_coef_editline)

        model_part2_layout.addRow(QtWidgets.QLabel("sec_phase: "), self.model_sec_phase_editline)
        model_part2_layout.addRow(QtWidgets.QLabel("a_sec: "), self.model_a_sec_editline)
        model_part2_layout.addRow(QtWidgets.QLabel("d_sec: "), self.model_d_sec_editline)
        model_part2_layout.addRow(QtWidgets.QLabel("g_sec: "), self.model_g_sec_editline)
        model_part2_layout.addRow(QtWidgets.QLabel("c_sec: "), self.model_c_sec_editline)
        model_part2_layout.addRow(QtWidgets.QLabel("cos1: "), self.model_cos1_editline)
        model_part2_layout.addRow(QtWidgets.QLabel("cos2: "), self.model_cos2_editline)
        model_part2_layout.addRow(QtWidgets.QLabel("cos3: "), self.model_cos3_editline)
        model_part2_layout.addRow(QtWidgets.QLabel("ofset: "), self.model_ofset_editline)

        # notes
        notes_groupbox = QtWidgets.QGroupBox("Notes")
        notes_layout = QtWidgets.QVBoxLayout()
        self.notes1_textedit = QtWidgets.QTextEdit()
        self.notes2_textedit = QtWidgets.QTextEdit()
        self.notes3_textedit = QtWidgets.QTextEdit()


        notes_groupbox.setLayout(notes_layout)
        notes_layout.addWidget(self.notes1_textedit)
        notes_layout.addWidget(self.notes2_textedit)
        notes_layout.addWidget(self.notes3_textedit)

        self.notes1_textedit.setReadOnly(True)
        self.notes2_textedit.setReadOnly(True)
        self.notes3_textedit.setReadOnly(True)

        # comp parameters
        comp_groupbox = QtWidgets.QGroupBox("Comparison star parameters")
        comp_layout = QtWidgets.QVBoxLayout()
        comp_groupbox.setLayout(comp_layout)
        self.comp_id_editline = QtWidgets.QLineEdit()
        self.comp_name_editline = QtWidgets.QLineEdit()
        self.comp_alternativ_name_editline = QtWidgets.QLineEdit()
        self.comp_ekvinokcium_editline = QtWidgets.QLineEdit()
        self.comp_constilation_editline = QtWidgets.QLineEdit()
        self.comp_rec_editline = QtWidgets.QLineEdit()
        self.comp_dec_editline = QtWidgets.QLineEdit()
        self.comp_rec_now_editline = QtWidgets.QLineEdit()
        self.comp_dec_now_editline = QtWidgets.QLineEdit()
        self.comp_mag_editline = QtWidgets.QLineEdit()
        self.comp_b_v_editline = QtWidgets.QLineEdit()
        self.comp_j_k_editline = QtWidgets.QLineEdit()

        self.comp_id_editline.setReadOnly(True)
        self.comp_name_editline.setReadOnly(True)
        self.comp_alternativ_name_editline.setReadOnly(True)
        self.comp_ekvinokcium_editline.setReadOnly(True)
        self.comp_constilation_editline.setReadOnly(True)
        self.comp_rec_editline.setReadOnly(True)
        self.comp_dec_editline.setReadOnly(True)
        self.comp_rec_now_editline.setReadOnly(True)
        self.comp_dec_now_editline.setReadOnly(True)
        self.comp_mag_editline.setReadOnly(True)
        self.comp_b_v_editline.setReadOnly(True)
        self.comp_j_k_editline.setReadOnly(True)

        self.comp_id_editline.setAlignment(QtCore.Qt.AlignRight)
        self.comp_name_editline.setAlignment(QtCore.Qt.AlignRight)
        self.comp_alternativ_name_editline.setAlignment(QtCore.Qt.AlignRight)
        self.comp_ekvinokcium_editline.setAlignment(QtCore.Qt.AlignRight)
        self.comp_constilation_editline.setAlignment(QtCore.Qt.AlignRight)
        self.comp_rec_editline.setAlignment(QtCore.Qt.AlignRight)
        self.comp_dec_editline.setAlignment(QtCore.Qt.AlignRight)
        self.comp_rec_now_editline.setAlignment(QtCore.Qt.AlignRight)
        self.comp_dec_now_editline.setAlignment(QtCore.Qt.AlignRight)
        self.comp_mag_editline.setAlignment(QtCore.Qt.AlignRight)
        self.comp_b_v_editline.setAlignment(QtCore.Qt.AlignRight)
        self.comp_j_k_editline.setAlignment(QtCore.Qt.AlignRight)

        comp_id_label = QtWidgets.QLabel("Star Id:")
        comp_name_label = QtWidgets.QLabel("Name:")
        comp_alternativ_name_label = QtWidgets.QLabel("Alt.name:")
        comp_ekvinokcium_label = QtWidgets.QLabel("eq.:")
        comp_constilation_label = QtWidgets.QLabel("Const:")
        comp_rec_label = QtWidgets.QLabel("RA/DE.eq:")
        comp_rec_now_label = QtWidgets.QLabel("RA/DE.now:")
        comp_mag_label = QtWidgets.QLabel("Mag:")
        comp_b_v_label = QtWidgets.QLabel("B-V:")
        comp_j_k_label = QtWidgets.QLabel("J-K:")

        self.comp_rec_editline.setFixedWidth(83)
        self.comp_dec_editline.setFixedWidth(80)
        self.comp_rec_now_editline.setFixedWidth(83)
        self.comp_dec_now_editline.setFixedWidth(80)
        self.comp_mag_editline.setFixedWidth(60)

        comp_id_layout = QtWidgets.QHBoxLayout()
        comp_id_layout.addWidget(comp_id_label)
        comp_id_layout.addWidget(self.comp_id_editline)
        comp_id_layout.addWidget(comp_constilation_label)
        comp_id_layout.addWidget(self.comp_constilation_editline)

        comp_name_layout = QtWidgets.QHBoxLayout()
        comp_name_layout.addWidget(comp_name_label)
        comp_name_layout.addWidget(self.comp_name_editline)

        comp_alt_name_layout = QtWidgets.QHBoxLayout()
        comp_alt_name_layout.addWidget(comp_alternativ_name_label)
        comp_alt_name_layout.addWidget(self.comp_alternativ_name_editline)

        comp_coor_layout = QtWidgets.QHBoxLayout()
        comp_coor_layout.addWidget(comp_rec_label)
        comp_coor_layout.addWidget(self.comp_rec_editline)
        comp_coor_layout.addWidget(self.comp_dec_editline)

        comp_coor_now_layout = QtWidgets.QHBoxLayout()
        comp_coor_now_layout.addWidget(comp_rec_now_label)
        comp_coor_now_layout.addWidget(self.comp_rec_now_editline)
        comp_coor_now_layout.addWidget(self.comp_dec_now_editline)

        comp_mag_layout = QtWidgets.QHBoxLayout()
        comp_mag_layout.addWidget(comp_mag_label)
        comp_mag_layout.addWidget(self.comp_mag_editline)
        comp_mag_layout.addWidget(comp_ekvinokcium_label)
        comp_mag_layout.addWidget(self.comp_ekvinokcium_editline)

        comp_bv_layout = QtWidgets.QHBoxLayout()
        comp_bv_layout.addWidget(comp_b_v_label)
        comp_bv_layout.addWidget(self.comp_b_v_editline)
        comp_bv_layout.addWidget(comp_j_k_label)
        comp_bv_layout.addWidget(self.comp_j_k_editline)

        comp_layout.addLayout(comp_id_layout)
        comp_layout.addLayout(comp_name_layout)
        comp_layout.addLayout(comp_alt_name_layout)
        comp_layout.addLayout(comp_coor_layout)
        comp_layout.addLayout(comp_coor_now_layout)
        comp_layout.addLayout(comp_mag_layout)
        comp_layout.addLayout(comp_bv_layout)

        # cross identification
        crossid_groupbox = QtWidgets.QGroupBox("Cross Identification")
        crossid_layout = QtWidgets.QHBoxLayout()
        crossid_groupbox.setLayout(crossid_layout)

        self.catalog_combobox = QtWidgets.QComboBox()
        self.catalog_combobox.addItems(["UCAC4", "USNOB1", "GAIA", "VSX", "ASAS-SN", "TESS"])
        self.catalog_number_label = QtWidgets.QLabel("")
        self.catalog_show_button = QtWidgets.QPushButton("Show detail")

        crossid_layout.addWidget(self.catalog_combobox)
        crossid_layout.addWidget(self.catalog_number_label)
        crossid_layout.addWidget(self.catalog_show_button)

        # near star
        self.near_groupbox = QtWidgets.QGroupBox("Nearby stars (diagonal of your field or 100')")
        near_layout = QtWidgets.QHBoxLayout()
        self.near_groupbox.setLayout(near_layout)
        self.near_combobox = QtWidgets.QComboBox()
        near_layout.addWidget(self.near_combobox)

        # SETUP
        self.object_detail_box = QtWidgets.QGroupBox("OBJECT DETAIL")
        object_detail_layout = QtWidgets.QGridLayout()
        self.object_detail_box.setLayout(object_detail_layout)

        object_detail_layout.addWidget(self.select_checkgroup, 0, 0, 1, 2)
        object_detail_layout.addWidget(self.pair_checkgroup, 0, 2, 1, 4)
        object_detail_layout.addWidget(self.in_prediction_checkgroup, 0, 6, 1, 1)
        object_detail_layout.addWidget(self.comp_checkgroup, 0, 7, 1, 1)
        object_detail_layout.addWidget(crossid_groupbox, 0, 8, 1, 3)
        object_detail_layout.addWidget(self.near_groupbox, 0, 11, 1, 2)
        object_detail_layout.addWidget(star_groupbox, 1, 0, 9, 3)
        object_detail_layout.addWidget(lightkurve_groupbox, 1, 3, 9, 3)
        object_detail_layout.addWidget(model_groupbox, 1, 6, 9, 3)
        object_detail_layout.addWidget(notes_groupbox, 1, 9, 9, 2)
        object_detail_layout.addWidget(comp_groupbox, 1, 11, 9, 2)


        self.main_page_layout.addWidget(self.object_detail_box, 17, 0, 10, 15)

    def __test_sunrise(self, jd, h, is_sunrise, sun_moon):
        date_h = sun_moon.sunrise_h(h, jd, self.place.longitude, self.place.latitude, is_sunrise=is_sunrise)
        if date_h != "No sunrise" and date_h != "No sunset":
            date_h = datetime.strftime(jd_to_date(date_h), "%d.%m.%Y %H:%M")
        return date_h

    def add_instrument(self):
        self.setEnabled(False)
        self.add_instrument_window.show()

    def add_user_to_list(self):
        if self.objects_table.currentRow() != -1:
            star_row = self.stars.star_index(self.star_name_editline.text())
            if self.select_user_checkbox.isChecked():
                self.stars.stars[star_row].user_list().append(self.user.name())
            else:
                if self.user.name() in self.stars.stars[star_row].user_list():
                    index = self.stars.stars[star_row].user_list().index(self.user.name())
                    self.stars.stars[star_row].user_list_del_item(index)
            self.fill_table()

    def add_place_to_list(self):
        if self.objects_table.currentRow() != -1:
            star_row = self.stars.star_index(self.star_name_editline.text())
            if self.select_place_checkbox.isChecked():
                self.stars.stars[star_row].place_list().append(self.place.name)
            else:
                if self.place.name in self.stars.stars[star_row].place_list():
                    index = self.stars.stars[star_row].place_list().index(self.place.name)
                    self.stars.stars[star_row].place_list_del_item(index)
            self.fill_table()

    def add_instrument_to_list(self):
        if self.objects_table.currentRow() != -1:
            star_row = self.stars.star_index(self.star_name_editline.text())
            if self.select_instrument_checkbox.isChecked():
                self.stars.stars[star_row].instrument_list().append(str(self.instrument.id))
            else:
                if self.instrument.id in self.stars.stars[star_row].instrument_list():
                    index = self.stars.stars[star_row].instrument_list().index(self.instrument.id)
                    self.stars.stars[star_row].instrument_list_del_item(index)
            self.fill_table()

    def add_observer(self):
        self.setEnabled(False)
        self.add_place_window.show()

    def add_user(self):
        self.save_user_environment()
        if self.user.authorizations == "Administrator":
            self.add_user_window.add_authorization_combobox.setEnabled(True)
        else:
            self.add_user_window.add_authorization_combobox.setEnabled(False)
        self.setEnabled(False)
        self.add_user_window.show()

    def calendar_start_add_form(self):
        self.setEnabled(False)
        self.calendar_add_start = True
        self.calendar_add_widget.setWindowIcon(QtGui.QIcon("alarm-clock--plus.png"))
        self.calendar_add_widget.show()

    def calendar_end_add_form(self):
        self.setEnabled(False)
        self.calendar_add_start = False
        self.calendar_add_widget.setWindowIcon(QtGui.QIcon("alarm-clock--minus.png"))
        self.calendar_add_widget.show()

    def clear_filter(self):
        self.filter_by_name_checkbox.setChecked(False)
        self.filter_name_key1.clear()
        self.filter_name_key2.clear()
        self.filter_by_rec_checkbox.setChecked(False)
        self.filter_rec_h_start.setValue(0)
        self.filter_rec_m_start.setValue(0)
        self.filter_rec_s_start.setValue(0)
        self.filter_rec_h_end.setValue(0)
        self.filter_rec_m_end.setValue(0)
        self.filter_rec_s_end.setValue(0)
        self.filter_by_dec_checkbox.setChecked(False)
        self.filter_dec_h_start.setValue(0)
        self.filter_dec_m_start.setValue(0)
        self.filter_dec_s_start.setValue(0)
        self.filter_dec_h_end.setValue(0)
        self.filter_dec_m_end.setValue(0)
        self.filter_dec_s_end.setValue(0)
        self.filter_by_type_checkbox.setChecked(False)
        self.filter_type_key1.setCurrentText("")
        self.filter_type_key2.setCurrentText("")
        self.filter_type_key3.setCurrentText("")
        self.filter_type_key4.setCurrentText("")
        self.filter_by_mag_checkbox.setChecked(False)
        self.filter_mag_start.setValue(0)
        self.filter_mag_end.setValue(0)
        self.filter_by_note_checkbox.setChecked(False)
        self.filter_note_key1.clear()
        self.filter_note_bool.setCurrentText("and")
        self.filter_note_key2.clear()

    def clear_comp_editlines(self):
        self.comp_id_editline.clear()
        self.comp_name_editline.clear()
        self.comp_alternativ_name_editline.clear()
        self.comp_constilation_editline.clear()
        self.comp_rec_editline.clear()
        self.comp_dec_editline.clear()
        self.comp_rec_now_editline.clear()
        self.comp_dec_now_editline.clear()
        self.comp_ekvinokcium_editline.clear()
        self.comp_mag_editline.clear()
        self.comp_b_v_editline.clear()
        self.comp_j_k_editline.clear()

    def clear_variable_editlines(self):
        self.lightcurve_period_editline.clear()
        self.lightcurve_epoch_editline.clear()
        self.lightcurve_type_editline.clear()
        self.lightcurve_amplitude_prim_editline.clear()
        self.lightcurve_amplitude_sec_editline.clear()
        self.lightcurve_d_big_prim_editline.clear()
        self.lightcurve_d_big_sec_editline.clear()
        self.lightcurve_d_prim_editline.clear()
        self.lightcurve_d_sec_editline.clear()
        self.model_mag0_editline.clear()
        self.model_a_pri_editline.clear()
        self.model_d_pri_editline.clear()
        self.model_g_pri_editline.clear()
        self.model_c_pri_editline.clear()
        self.model_sin1_editline.clear()
        self.model_sin2_editline.clear()
        self.model_sin3_editline.clear()
        self.model_apsid_coef_editline.clear()
        self.model_sec_phase_editline.clear()
        self.model_a_sec_editline.clear()
        self.model_d_sec_editline.clear()
        self.model_c_sec_editline.clear()
        self.model_g_sec_editline.clear()
        self.model_cos1_editline.clear()
        self.model_cos2_editline.clear()
        self.model_cos3_editline.clear()
        self.model_ofset_editline.clear()

    def ucac4_cross_info(self):
        try:
            if ("a" + self.star_detail.ucac4()).strip() == "a":
                self.ucac4_window.download_data_coor(self.star_detail.coordinate())
            else:
                self.ucac4_window.download_data_id(self.star_detail.ucac4())
            self.ucac4_window.show()
        except:
            pass

    def usno_cross_info(self):
        try:
            if ("a" + self.star_detail.usnob1()).strip() == "a":
                self.usno_window.download_data_coor(self.star_detail.coordinate())
            else:
                self.usno_window.download_data_id(self.star_detail.usnob1())
            self.usno_window.show()
        except:
            pass

    def vsx_cross_info(self):
        try:
            if ("a" + self.star_detail.vsx()).strip() == "a":
                self.vsx_window.download_data_coor(self.star_detail.coordinate())
            else:
                self.vsx_window.download_data_id(self.star_detail.vsx())
            self.vsx_window.looking_for_cross_id()
            self.vsx_window.show()
        except:
            pass

    def gaia_cross_info(self):
        try:
            if ("a" + self.star_detail.gaia()).strip() == "a":
                self.gaia_window.download_data_coor(self.star_detail.coordinate())
            else:
                self.gaia_window.download_data_id(self.star_detail.gaia())
            self.gaia_window.show()
        except:
            pass

    def asas_cross_info(self):
        try:
            if ("a" + self.star_detail.asassn()).strip() == "a":
                self.asas_window.download_data_coor(self.star_detail.coordinate())
            else:
                self.asas_window.download_data_id(self.star_detail.asassn())
            self.asas_window.looking_for_cross_id()
            self.asas_window.show()
        except:
            pass

    def tess_cross_info(self):
        try:
            self.tess_window.download_data_coor(self.star_detail.coordinate())
            self.tess_window.show()
        except:
            pass

    def closeEvent(self, event):
        save_window = Popup("Save changes", "Do you want to save all changes and close application?", buttons="Save changes, Exit without save, Back to STEP".split(","))
        response = save_window.do()
        if response == 0:
            self.database.save_setup()
            self.save(info_window=True)
            self.horizon_set_window.close()
            self.calendar_add_widget.close()
            self.add_user_window.close()
            self.add_instrument_window.close()
            self.add_place_window.close()
            os._exit(0)
        elif response == 1:
            self.horizon_set_window.close()
            self.calendar_add_widget.close()
            self.add_user_window.close()
            self.add_instrument_window.close()
            self.add_place_window.close()
            os._exit(0)
        else:
            try:
                event.ignore()
            except:
                pass
            return

    def delete_instrument(self):
        if self.instrument_combobox.currentText() in ["add instrument", "add place", "Add telescope"]:
            return
        else:
            r = Popup("Remove the observation set",
                      "You really want to remove the instrument set?", buttons="OK,Back".split(","))
            if r.do() == 0:
                self.instruments.delete_instrument(str(self.instrument.id))
                self.fill_instruments()

    def delete_place(self):
        if self.observer_combobox.currentText() == "add place":
            return
        else:
            if self.instrument_combobox.currentText() in ["add instrument", "add place", "Add telescope"]:
                r = Popup("Remove place", "You really want to remove this observation site?", buttons="OK,Back".split(","))
                if r.do() == 0:
                    self.places.delete_observer(str(self.place.name))
                    self.horizons.delete_horizon(str(self.place.horizon_id))
                    self.fill_place()
                    self.edit_place()
            else:
                r = Popup("Remove place", "Firstly delete all instruments set.", buttons="OK".split(","))
                r.do()

    def delete_user(self):
        if self.user_combobox.currentText() == "add user":
            return
        else:
            if self.observer_combobox.currentText() == "add place" and \
                    self.instrument_combobox.currentText() == "add place":
                r = Popup("Remove user", "You really want to remove this user?", buttons="OK,Back".split(","))
                if r.do() == 0:
                    self.users.delete_user(str(self.user.name()))
                    self.user_combobox.clear()
                    self.fill_user()
                    self.edit_user()
            else:
                r = Popup("Remove user", "Firstly delete observation site and instruments", buttons="OK".split(","))
                r.do()

    def edit_instrument(self):
        if self.instrument_combobox.currentText() == "add place" or \
                self.instrument_combobox.currentText() == "add instrument":
            self.instrument.edit_all("id", 0, self.instruments)
            self.select_instrument_checkbox.setEnabled(False)
        else:
            self.select_instrument_checkbox.setEnabled(True)
            instruments_list_id = self.database.return_list_by_key("id", "instruments", filter_key="observer_id",
                                                                   filter_value=self.place.id)
            if instruments_list_id:
                current_instrument_id = instruments_list_id[self.instrument_combobox.currentIndex()]
                self.instrument.edit_all("id", current_instrument_id, self.instruments)
                self.fill_table()

    def edit_place(self):
        if self.observer_combobox.currentText() != self.place.name:
            self.place.edit_all("name", self.observer_combobox.currentText(), self.places, self.horizons)
            self.latitude_label.setText(self.place.latitude_text())
            self.longitude_label.setText(self.place.longitude_text())
            self.sun_h_set_spinbox.setValue(degrees(self.place.min_sunset))
            self.h_spinbox.setValue(degrees(self.place.minimum_h))
            self.fill_sun_moon()
            self.fill_table()
        if self.observer_combobox.currentText() == "add place":
            self.instrument_combobox.setEnabled(False)
            self.object_group_box.setEnabled(False)
            if self.filtered_stars.stars:
                self.object_detail_box.setEnabled(False)

        else:
            self.instrument_combobox.setEnabled(True)
            self.object_group_box.setEnabled(True)
            self.object_detail_box.setEnabled(True)
        self.fill_instruments()

    def save(self, info_window=False):
        self.save_user_environment()
        self.database.save_database()
        self.database.save_setup()
        if not info_window:
            info_label = QtWidgets.QMessageBox()
            info_label.setText("Databases a Environment were saved")
            info_label.setWindowIcon(QtGui.QIcon("information-italic.png"))
            info_label.setWindowTitle("Saved")
            info_label.exec()


    def edit_user(self):
        if self.user_combobox.currentText() == "add user":
            self.instrument_combobox.setEnabled(False)
            self.object_group_box.setEnabled(False)
            if self.filtered_stars.stars:
                self.object_detail_box.setEnabled(False)
        else:
            try:
                self.save_user_environment()
            except:
                pass
            self.instrument_combobox.setEnabled(True)
            self.object_group_box.setEnabled(True)
            self.object_detail_box.setEnabled(True)
        if self.user_combobox.currentText() != self.user.name() or self.observer_combobox.count() == 0:
            self.user.edit_all("name", self.user_combobox.currentText(), self.users)
            self.fill_place()
            self.latitude_label.setText(self.place.latitude_text())
            self.longitude_label.setText(self.place.longitude_text())
            self.sun_h_set_spinbox.setValue(degrees(self.place.min_sunset))
            self.h_spinbox.setValue(degrees(self.place.minimum_h))
            self.fill_sun_moon()
            try:
                self.prediction2.fill_form()
                self.prediction2.lightcurve_window.lc_time_start_doublespinbox.setValue(
                    float(self.user.time_extension_setup()[0]))
                self.prediction2.lightcurve_window.lc_time_end_doublespinbox.setValue(
                    float(self.user.time_extension_setup()[1]))
            except:
                pass

            objects_sort_by_index = int(self.user.object_sort_by_setup()[0])
            self.sort_by_combobox.setCurrentIndex(objects_sort_by_index)
            objects_filter = self.user.object_filtered_by_setup()
            for i, object_filter in enumerate(objects_filter):
                if object_filter == "1":
                    if i == 0:
                        self.filter_by_var_checkbox.setChecked(True)
                    elif i == 1:
                        self.filter_by_user_checkbox.setChecked(True)
                    elif i == 2:
                        self.filter_by_place_checkbox.setChecked(True)
                    elif i == 3:
                        self.filter_by_instrument_checkbox.setChecked(True)
                    elif i == 4:
                        self.filter_by_name_checkbox.setChecked(True)
                    elif i == 5:
                        self.filter_by_rec_checkbox.setChecked(True)
                    elif i == 6:
                        self.filter_by_dec_checkbox.setChecked(True)
                    elif i == 7:
                        self.filter_by_type_checkbox.setChecked(True)
                    elif i == 8:
                        self.filter_by_mag_checkbox.setChecked(True)
                    else:
                        self.filter_by_note_checkbox.setChecked(True)
                else:
                    if i == 0:
                        self.filter_by_var_checkbox.setChecked(False)
                    elif i == 1:
                        self.filter_by_user_checkbox.setChecked(False)
                    elif i == 2:
                        self.filter_by_place_checkbox.setChecked(False)
                    elif i == 3:
                        self.filter_by_instrument_checkbox.setChecked(False)
                    elif i == 4:
                        self.filter_by_name_checkbox.setChecked(False)
                    elif i == 5:
                        self.filter_by_rec_checkbox.setChecked(False)
                    elif i == 6:
                        self.filter_by_dec_checkbox.setChecked(False)
                    elif i == 7:
                        self.filter_by_type_checkbox.setChecked(False)
                    elif i == 8:
                        self.filter_by_mag_checkbox.setChecked(False)
                    else:
                        self.filter_by_note_checkbox.setChecked(False)
            self.filter_rec_h_start.setValue(int(self.user.coordinate_setup()[0]))
            self.filter_rec_m_start.setValue(int(self.user.coordinate_setup()[1]))
            self.filter_rec_s_start.setValue(int(self.user.coordinate_setup()[2]))
            self.filter_rec_h_end.setValue(int(self.user.coordinate_setup()[3]))
            self.filter_rec_m_end.setValue(int(self.user.coordinate_setup()[4]))
            self.filter_rec_s_end.setValue(int(self.user.coordinate_setup()[5]))
            self.filter_dec_h_start.setValue(int(self.user.coordinate_setup()[6]))
            self.filter_dec_m_start.setValue(int(self.user.coordinate_setup()[7]))
            self.filter_dec_s_start.setValue(int(self.user.coordinate_setup()[8]))
            self.filter_dec_h_end.setValue(int(self.user.coordinate_setup()[9]))
            self.filter_dec_m_end.setValue(int(self.user.coordinate_setup()[10]))
            self.filter_dec_s_end.setValue(int(self.user.coordinate_setup()[11]))
            self.filter_name_key1.setText(self.user.texts_filter_setup_name_key1())
            self.filter_name_key2.setText(self.user.texts_filter_setup_name_key2())
            self.filter_type_key1.setCurrentText(self.user.texts_filter_setup_type_key1())
            self.filter_type_key2.setCurrentText(self.user.texts_filter_setup_type_key2())
            self.filter_type_key3.setCurrentText(self.user.texts_filter_setup_type_key3())
            self.filter_type_key4.setCurrentText(self.user.texts_filter_setup_type_key4())
            self.filter_mag_start.setValue(float(self.user.texts_filter_setup_mag_start()))
            self.filter_mag_end.setValue(float(self.user.texts_filter_setup_mag_end()))
            self.filter_note_key1.setText(self.user.texts_filter_setup_note_key1())
            self.filter_note_key2.setText(self.user.texts_filter_setup_note_key2())
            self.filter_note_bool.setCurrentText(self.user.texts_filter_setup_note_key3())
            self.fill_table()

    def fill_flat(self, jd, h, is_sunrise):
        date_h = self.sun.sunrise_h(h, jd, self.place.longitude, self.place.latitude, is_sunrise=is_sunrise)
        if date_h != "No sunrise" and date_h != "No sunset":
            if is_sunrise:
                a_sunrise = radians(self.flat_a_spinbox_sunrise.value()) - pi
                h_sunrise = radians(self.flat_h_spinbox_sunrise.value())
                coor = self.place.horizontal_to_eqatoreal(date_h, a_sunrise, h_sunrise)
                rec_text = coordinate_to_text(coor.rektascenze(), coordinate_format="hours", decimal_numbers=0)
                dec_text = coordinate_to_text(coor.deklinace(), decimal_numbers=0)
                self.flat_rec_sunrise_label.setText(rec_text)
                self.flat_dec_sunrise_label.setText(dec_text)
            else:
                a_sunset = radians(self.flat_a_spinbox_sunset.value()) - pi
                h_sunset = radians(self.flat_h_spinbox_sunset.value())
                coor = self.place.horizontal_to_eqatoreal(date_h, a_sunset, h_sunset)
                rec_text = coordinate_to_text(coor.rektascenze(), coordinate_format="hours", decimal_numbers=0)
                dec_text = coordinate_to_text(coor.deklinace(), decimal_numbers=0)
                self.flat_rec_sunset_label.setText(rec_text)
                self.flat_dec_sunset_label.setText(dec_text)
        else:
            self.flat_rec_sunset_label.setText("")
            self.flat_rec_sunrise_label.setText("")
            self.flat_dec_sunset_label.setText("")
            self.flat_dec_sunrise_label.setText("")

    def fill_instruments(self):
        if self.observer_combobox.currentText() == "add place":
            self.instrument_combobox.clear()
            self.instrument_combobox.addItem("add place")
            self.instrument.edit_all("id", 0, self.instruments)
        else:
            instruments_list_telescope = self.database.return_list_by_key("telescope",
                                                                          "instruments",
                                                                          filter_key="observer_id",
                                                                          filter_value=self.place.id)
            instruments_list_mount = self.database.return_list_by_key("mount", "instruments",
                                                                      filter_key="observer_id",
                                                                      filter_value=self.place.id)
            instruments_list_camera = self.database.return_list_by_key("camera", "instruments",
                                                                       filter_key="observer_id",
                                                                       filter_value=self.place.id)
            instruments_list_id = self.database.return_list_by_key("id", "instruments",
                                                                   filter_key="observer_id",
                                                                   filter_value=self.place.id)
            self.instrument_combobox.clear()
            if instruments_list_telescope:
                # self.instrument_delete.setEnabled(True)
                self.instrument_combobox.setEnabled(True)
                for i in range(len(instruments_list_telescope)):
                    self.instrument_combobox.addItem(instruments_list_telescope[i] + " + " + instruments_list_mount[i]
                                                     + " + " + instruments_list_camera[i])
                self.instrument.edit_all("id", instruments_list_id[0], self.instruments)
            else:
                self.instrument_combobox.addItem("add instrument")
                # self.instrument_delete.setEnabled(False)
                self.instrument_combobox.setEnabled(False)
                self.instrument.edit_all("id", 0, self.instruments)
            self.fill_table()

    def fill_comp(self):
        if self.objects_table.currentRow() > -1:
            self.object_detail_box.setEnabled(True)
            if self.comperison_combobox.currentText() == "comp0":
                comp_id = self.star_detail.comp0()
            elif self.comperison_combobox.currentText() == "comp1":
                comp_id = self.star_detail.comp1()
            elif self.comperison_combobox.currentText() == "comp2":
                comp_id = self.star_detail.comp2()
            elif self.comperison_combobox.currentText() == "comp3":
                comp_id = self.star_detail.comp3()
            elif self.comperison_combobox.currentText() == "comp4":
                comp_id = self.star_detail.comp4()
            elif self.comperison_combobox.currentText() == "comp5":
                comp_id = self.star_detail.comp5()
            elif self.comperison_combobox.currentText() == "comp6":
                comp_id = self.star_detail.comp6()
            elif self.comperison_combobox.currentText() == "comp7":
                comp_id = self.star_detail.comp7()
            elif self.comperison_combobox.currentText() == "comp8":
                comp_id = self.star_detail.comp8()
            elif self.comperison_combobox.currentText() == "comp9":
                comp_id = self.star_detail.comp9()
            elif self.comperison_combobox.currentText() == "chk1":
                comp_id = self.star_detail.chk1()
            else:
                comp_id = 0

            if comp_id:
                comp_row = self.stars.star_id_index(comp_id)
                self.comp_detail = self.stars.stars[comp_row]
                self.comp_id_editline.setText(self.comp_detail.id())
                self.comp_name_editline.setText(self.comp_detail.name())
                self.comp_alternativ_name_editline.setText(self.comp_detail.alt_name())
                self.comp_constilation_editline.setText(self.comp_detail.constellation())
                rec_text = coordinate_to_text(self.comp_detail.rektascenze(), coordinate_format="hours",
                                              delimiters=("h ", "' ", '"'))
                dec_text = coordinate_to_text(self.comp_detail.declination(), delimiters=("° ", "' ", '"'))
                self.comp_rec_editline.setText(rec_text)
                self.comp_dec_editline.setText(dec_text)
                self.comp_rec_now_editline.setText(
                    coordinate_to_text(
                        self.comp_detail.coordinate().rektascenze_now(float(self.local_jd_now_label.text())),
                        coordinate_format="hours", delimiters=("h ", "' ", '"')))
                self.comp_dec_now_editline.setText(
                    coordinate_to_text(
                        self.comp_detail.coordinate().deklinace_now(float(self.local_jd_now_label.text())),
                        delimiters=("° ", "' ", '"')))
                self.comp_ekvinokcium_editline.setText(self.comp_detail.coordinate().epoch())
                self.comp_mag_editline.setText((str(round(float(self.comp_detail.mag()), 2))))
                if self.comp_detail.b_v():
                    self.comp_b_v_editline.setText(str(self.comp_detail.b_v()))
                else:
                    self.comp_b_v_editline.clear()
                if self.comp_detail.j_k():
                    self.comp_j_k_editline.setText(str(self.comp_detail.j_k()))
                else:
                    self.comp_j_k_editline.clear()
        else:
            if self.filtered_stars.stars:
                self.object_detail_box.setEnabled(False)

    def fill_object(self):
        self.object_edit_window.close()
        self.asas_window.close()
        self.vsx_window.close()
        self.tess_window.close()
        self.usno_window.close()
        self.ucac4_window.close()
        self.gaia_window.close()
        self.clear_comp_editlines()
        if self.objects_table.currentRow() > -1:
            self.object_detail_box.setEnabled(True)
            star_row = self.objects_table.currentRow()
            self.star_detail = self.filtered_stars.stars[star_row]
            if self.observation_log_window.by_prediction_checkbox.isChecked():
                self.observation_log_window.find_variable_lineedit.setText(self.star_detail.name())
            else:
                pass
            if self.prediction2.prediction_table and not self.prediction2.isHidden():
                prediction_star_name = ""
                if self.prediction2.prediction_table_widget.currentRow() > -1:
                    row = self.prediction2.prediction_table_widget.currentRow()
                    prediction_star_name = self.prediction2.prediction_table[row][1]
                if self.star_detail.name() != prediction_star_name:
                    try:
                        is_set = False
                        for i, row in enumerate(self.prediction2.prediction_table):
                            if not is_set and row[1] == self.star_detail.name():
                                self.prediction2.prediction_table_widget.selectRow(i)
                                is_set = True
                    except:
                        pass
            else:
                if self.show_lightcurve_checkbox.isChecked():
                    self.prediction2.lightcurve_window.time_home()
                    self.prediction2.show_lightcurve()
                else:
                    self.prediction2.close()



            try:
                self.horizon_set_window.update()
            except:
                pass

            self.star_id_editline.setText(self.star_detail.id())
            self.star_name_editline.setText(self.star_detail.name())
            self.star_alternativ_name_editline.setText(self.star_detail.alt_name())
            self.star_constilation_editline.setText(self.star_detail.constellation())
            rec_text = coordinate_to_text(self.star_detail.rektascenze(), coordinate_format="hours",
                                          delimiters=("h ", "' ", '"'))
            dec_text = coordinate_to_text(self.star_detail.declination(), delimiters=("° ", "' ", '"'))
            dec = int(dec_text[0:3])
            self.horizon_set_window.dec_spinbox.setValue(dec)
            self.star_rec_editline.setText(rec_text)
            self.star_dec_editline.setText(dec_text)
            self.star_rec_now_editline.setText(coordinate_to_text(self.star_detail.coordinate().
                                                                  rektascenze_now(
                float(self.local_jd_now_label.text())),
                                                                  coordinate_format="hours",
                                                                  delimiters=("h ", "' ", '"')))
            self.star_dec_now_editline.setText(coordinate_to_text(self.star_detail.coordinate().
                                                                  deklinace_now(float(self.local_jd_now_label.text())),
                                                                  delimiters=("° ", "' ", '"')))
            self.star_ekvinokcium_editline.setText(self.star_detail.coordinate().epoch())
            self.star_mag_editline.setText(str(self.star_detail.mag()))
            self.star_type_editline.setText(self.database.type_dictionary[self.star_detail.type()])
            self.star_b_v_editline.setText(str(self.star_detail.b_v()))
            self.star_j_k_editline.setText(str(self.star_detail.j_k()))
            self.notes1_textedit.setText(self.star_detail.note1())
            self.notes2_textedit.setText(self.star_detail.note2())
            self.notes3_textedit.setText(self.star_detail.note3())
            self.show_catalog_number()

            if self.user.name() in self.star_detail.user_list():
                self.select_user_checkbox.setChecked(True)
            else:
                self.select_user_checkbox.setChecked(False)
            if self.place.name in self.star_detail.place_list():
                self.select_place_checkbox.setChecked(True)
            else:
                self.select_place_checkbox.setChecked(False)
            if self.instrument.id in self.star_detail.instrument_list():
                self.select_instrument_checkbox.setChecked(True)
            else:
                self.select_instrument_checkbox.setChecked(False)
            active = self.star_detail.variability()
            self.lightcurve_period_editline.setEnabled(active)
            self.lightcurve_epoch_editline.setEnabled(active)
            self.lightcurve_type_editline.setEnabled(active)
            self.lightcurve_amplitude_prim_editline.setEnabled(active)
            self.lightcurve_amplitude_sec_editline.setEnabled(active)
            self.lightcurve_d_big_prim_editline.setEnabled(active)
            self.lightcurve_d_big_sec_editline.setEnabled(active)
            self.lightcurve_d_prim_editline.setEnabled(active)
            self.lightcurve_d_sec_editline.setEnabled(active)
            self.model_mag0_editline.setEnabled(active)
            self.model_a_pri_editline.setEnabled(active)
            self.model_d_pri_editline.setEnabled(active)
            self.model_g_pri_editline.setEnabled(active)
            self.model_c_pri_editline.setEnabled(active)
            self.model_sin1_editline.setEnabled(active)
            self.model_sin2_editline.setEnabled(active)
            self.model_sin3_editline.setEnabled(active)
            self.model_apsid_coef_editline.setEnabled(active)
            self.model_sec_phase_editline.setEnabled(active)
            self.model_a_sec_editline.setEnabled(active)
            self.model_d_sec_editline.setEnabled(active)
            self.model_c_sec_editline.setEnabled(active)
            self.model_g_sec_editline.setEnabled(active)
            self.model_cos1_editline.setEnabled(active)
            self.model_cos2_editline.setEnabled(active)
            self.model_cos3_editline.setEnabled(active)
            self.model_ofset_editline.setEnabled(active)

            star_variability = self.variable.choice_by_name(self.star_detail.name())

            if "A" in star_variability[1] or self.star_detail.variability() != "VAR":
                self.pair_a_checkbox.setEnabled(True)
            else:
                self.pair_a_checkbox.setEnabled(False)
            if "B" in star_variability[1]:
                self.pair_b_checkbox.setEnabled(True)
            else:
                self.pair_b_checkbox.setEnabled(False)
            if "C" in star_variability[1]:
                self.pair_c_checkbox.setEnabled(True)
            else:
                self.pair_c_checkbox.setEnabled(False)
            if "D" in star_variability[1]:
                self.pair_d_checkbox.setEnabled(True)
            else:
                self.pair_d_checkbox.setEnabled(False)
            if "E" in star_variability[1]:
                self.pair_e_checkbox.setEnabled(True)
            else:
                self.pair_e_checkbox.setEnabled(False)
            if "F" in star_variability[1]:
                self.pair_f_checkbox.setEnabled(True)
            else:
                self.pair_f_checkbox.setEnabled(False)
            self.comperison_combobox.clear()
            if self.star_detail.comp0() != 0:
                self.comperison_combobox.addItem("comp0")
            if self.star_detail.comp1() != 0:
                self.comperison_combobox.addItem("comp1")
            if self.star_detail.comp2() != 0:
                self.comperison_combobox.addItem("comp2")
            if self.star_detail.comp3() != 0:
                self.comperison_combobox.addItem("comp3")
            if self.star_detail.comp4() != 0:
                self.comperison_combobox.addItem("comp4")
            if self.star_detail.comp5() != 0:
                self.comperison_combobox.addItem("comp5")
            if self.star_detail.comp6() != 0:
                self.comperison_combobox.addItem("comp6")
            if self.star_detail.comp7() != 0:
                self.comperison_combobox.addItem("comp7")
            if self.star_detail.comp8() != 0:
                self.comperison_combobox.addItem("comp8")
            if self.star_detail.comp9() != 0:
                self.comperison_combobox.addItem("comp9")
            if self.star_detail.chk1() != 0:
                self.comperison_combobox.addItem("chk1")

            if "A" in star_variability[1] and self.pair_a_checkbox.isChecked():
                variable_index = star_variability[1].index("A")
            elif "B" in star_variability[1] and self.pair_b_checkbox.isChecked():
                variable_index = star_variability[1].index("B")
            elif "C" in star_variability[1] and self.pair_c_checkbox.isChecked():
                variable_index = star_variability[1].index("C")
            elif "D" in star_variability[1] and self.pair_d_checkbox.isChecked():
                variable_index = star_variability[1].index("D")
            elif "E" in star_variability[1] and self.pair_e_checkbox.isChecked():
                variable_index = star_variability[1].index("E")
            elif "F" in star_variability[1] and self.pair_f_checkbox.isChecked():
                variable_index = star_variability[1].index("F")
            else:
                variable_index = -1

            if variable_index < 0:
                self.clear_variable_editlines()
            else:
                self.actual_variable: VariableStar = star_variability[0][variable_index]
                self.lightcurve_period_editline.setText(str(self.actual_variable.period()))
                self.lightcurve_epoch_editline.setText(str(self.actual_variable.epoch()))
                self.lightcurve_type_editline.setText(self.actual_variable.variability_type())
                self.lightcurve_amplitude_prim_editline.setText(str(self.actual_variable.amplitude_p()))
                self.lightcurve_amplitude_sec_editline.setText(str(self.actual_variable.amplitude_s()))
                self.lightcurve_d_big_prim_editline.setText(str(self.actual_variable.d_eclipse_prim()))
                self.lightcurve_d_big_sec_editline.setText(str(self.actual_variable.d_eclipse_sec()))
                self.lightcurve_d_prim_editline.setText(str(self.actual_variable.d_minimum_prim()))
                self.lightcurve_d_sec_editline.setText(str(self.actual_variable.d_minimum_sec()))
                self.model_mag0_editline.setText(str(self.actual_variable.mag0()))
                self.model_a_pri_editline.setText(str(self.actual_variable.a_pri()))
                self.model_d_pri_editline.setText(str(self.actual_variable.d_pri()))
                self.model_g_pri_editline.setText(str(self.actual_variable.g_pri()))
                self.model_c_pri_editline.setText(str(self.actual_variable.c_pri()))
                self.model_sin1_editline.setText(str(self.actual_variable.a_sin1()))
                self.model_sin2_editline.setText(str(self.actual_variable.a_sin2()))
                self.model_sin3_editline.setText(str(self.actual_variable.a_sin3()))
                self.model_apsid_coef_editline.setText(str(self.actual_variable.apsidal_movement_correction()))
                self.model_sec_phase_editline.setText(str(self.actual_variable.sec_phase()))
                self.model_a_sec_editline.setText(str(self.actual_variable.a_sec()))
                self.model_d_sec_editline.setText(str(self.actual_variable.d_sec()))
                self.model_c_sec_editline.setText(str(self.actual_variable.c_sec()))
                self.model_g_sec_editline.setText(str(self.actual_variable.g_sec()))
                self.model_cos1_editline.setText(str(self.actual_variable.a_cos1()))
                self.model_cos2_editline.setText(str(self.actual_variable.a_cos2()))
                self.model_cos3_editline.setText(str(self.actual_variable.a_cos3()))
                self.model_ofset_editline.setText(str(self.actual_variable.lc_offset()))
                self.in_prediction_checkbox.setChecked(self.actual_variable.in_prediction())
            self.fill_comp()
            self.near_combobox.clear()
            near_star_list = []
            try:
                max_distance = (3437.71680736 ** 2 * float(self.instrument.sensor_h()) *
                                float(self.instrument.sensor_w()) / float(self.instrument.focus()) ** 2) ** 0.5
                self.near_groupbox.setTitle("Nearby stars: " + str(int(max_distance))+ "'")
            except:
                max_distance = 100
                self.near_groupbox.setTitle("Nearby stars(100' - set camera and telescope parameters)")

            if self.star_detail.variability():
                for star in self.stars.stars:
                    if star.variability() and star.name() != self.star_detail.name():
                        angle_distance = angular_separation(star.rektascenze(), star.declination(),
                                                            self.star_detail.rektascenze(), self.star_detail.declination())
                        angle_distance_min = angle_distance * 10800 / pi
                        if angle_distance_min < max_distance:
                            angle_distance_int = round(angle_distance_min, 1)
                            if angle_distance_int < 10:
                                angle_distance_text = "0"+str(angle_distance_int)
                            else:
                                angle_distance_text = str(angle_distance_int)
                            near_star_list.append(angle_distance_text + "': " + star.name())
                if near_star_list:
                    near_star_list.sort()
                    self.near_combobox.addItems(near_star_list)
                else:
                    self.near_combobox.addItem("Any near star")
        else:
            if self.filtered_stars.stars:
                self.object_detail_box.setEnabled(False)

    def fill_place(self):
        observer_list = self.database.return_list_by_key("name", "places", filter_key="user_id",
                                                         filter_value=self.user_combobox.currentText())
        self.observer_combobox.clear()
        if observer_list:
            # self.observer_delete.setEnabled(True)
            self.observer_combobox.setEnabled(True)
            # self.horizon_button.setEnabled(True)
            self.h_spinbox.setEnabled(True)
            for observer in observer_list:
                self.observer_combobox.addItem(observer)
        else:
            self.observer_combobox.addItem("add place")
            # self.observer_delete.setEnabled(False)
            self.observer_combobox.setEnabled(False)
            # self.horizon_button.setEnabled(False)
            self.h_spinbox.setEnabled(False)

    def fill_sun_moon(self):
        self.place.set_min_sunset(radians(self.sun_h_set_spinbox.value()))
        self.places.edit_h(self.place.name, radians(self.h_spinbox.value()), radians(self.sun_h_set_spinbox.value()))
        if self.sun_start_checkbox.isChecked():
            jd = self.time_period.jd_start()
        elif self.sun_end_checkbox.isChecked():
            jd = self.time_period.jd_end()
        else:
            a = self.sun_settime_dateedit.date()
            jd = (date_to_jd(datetime(year=a.year(), month=a.month(), day=a.day(), hour=17, minute=0,
                                      tzinfo=timezone.utc)))
        self.sun_sunset_label.setText(self.__test_sunrise(jd, 0, False, self.sun))
        self.sun_nautdusk_label.setText(self.__test_sunrise(jd, radians(-12), False, self.sun))
        self.sun_astdusk_label.setText(self.__test_sunrise(jd, radians(-18), False, self.sun))
        self.sun_sethdusk_label.setText(self.__test_sunrise(jd, radians(self.sun_h_set_spinbox.value()),
                                                            False, self.sun))
        self.sun_sethdawn_label.setText(self.__test_sunrise(jd, radians(self.sun_h_set_spinbox.value()), True,
                                                            self.sun))
        self.sun_astdawn_label.setText(self.__test_sunrise(jd, radians(-18), True, self.sun))
        self.sun_nautdawn_label.setText(self.__test_sunrise(jd, radians(-12), True, self.sun))
        self.sun_sunrise_label.setText(self.__test_sunrise(jd, 0, True, self.sun))
        self.sun_moonrise_label.setText(self.__test_sunrise(jd, 0, True, self.moon))
        self.sun_moonset_label.setText(self.__test_sunrise(jd, 0, False, self.moon))
        moon_faze = degrees(self.moon.moon_phase(jd))
        if moon_faze < 180:
            faze_percentages = str(int(moon_faze / 1.8))
        else:
            faze_percentages = str(200 - int(moon_faze / 1.8))
        self.sun_moonfase_label.setText(str(round(moon_faze, 1)) + "° - (" + faze_percentages + "%)")
        h_flat = radians(self.flat_h_spinbox.value())
        self.flat_time_sunset_label.setText(self.__test_sunrise(jd, h_flat, False, self.sun))
        self.flat_time_sunrise_label.setText(self.__test_sunrise(jd, h_flat, True, self.sun))
        self.fill_flat(jd, h_flat, True)
        self.fill_flat(jd, h_flat, False)
        self.set_dust_label.setText("set h dusk({0}°):".format(str(int(self.sun_h_set_spinbox.value()))))
        self.set_dawn_label.setText("set h dawn({0}°):".format(str(int(self.sun_h_set_spinbox.value()))))

    def fill_table(self):
        current_set_name = self.star_name_editline.text()
        self.object_edit_window.close()
        name = self.filter_name_key1.text()
        alt_name = self.filter_name_key2.text()
        rec_start = radians(self.filter_rec_h_start.value() * 15 + self.filter_rec_m_start.value() / 4
                            + self.filter_rec_s_start.value() / 240)
        rec_end = radians(self.filter_rec_h_end.value() * 15 + self.filter_rec_m_end.value() / 4
                          + self.filter_rec_s_end.value() / 240)
        dec_start = radians(self.filter_dec_h_start.value() + self.filter_dec_m_start.value() / 60
                            + self.filter_dec_s_start.value() / 3600)
        dec_end = radians(self.filter_dec_h_end.value() + self.filter_dec_m_end.value() / 60
                          + self.filter_dec_s_end.value() / 3600)
        type1 = self.filter_type_key1.currentText()
        type2 = self.filter_type_key2.currentText()
        type3 = self.filter_type_key3.currentText()
        type4 = self.filter_type_key4.currentText()
        mag_max = self.filter_mag_start.value()
        mag_min = self.filter_mag_end.value()
        note1 = self.filter_note_key1.text()
        note2 = self.filter_note_key2.text()
        if self.filter_note_bool.currentText() == "and":
            note_log_info = True
        else:
            note_log_info = False
        by_variability = self.filter_by_var_checkbox.isChecked()
        by_user = self.filter_by_user_checkbox.isChecked()
        by_place = self.filter_by_place_checkbox.isChecked()
        by_instrument = self.filter_by_instrument_checkbox.isChecked()
        by_name = self.filter_by_name_checkbox.isChecked()
        by_rec = self.filter_by_rec_checkbox.isChecked()
        by_dec = self.filter_by_dec_checkbox.isChecked()
        by_type = self.filter_by_type_checkbox.isChecked()
        by_mag = self.filter_by_mag_checkbox.isChecked()
        by_note = self.filter_by_note_checkbox.isChecked()
        by_constilation = self.constilation_checkbox.isChecked()
        constilation = self.constilation_combobox.currentText()
        if rec_start == rec_end:
            by_rec = False
        if dec_start == dec_end:
            by_dec = False
        if mag_min == mag_max:
            by_mag = False

        sorted_star = self.stars.filter(self.user, self.place, self.instrument, name, alt_name, rec_start, rec_end,
                                        dec_start, dec_end, type1, type2, type3, type4, mag_max, mag_min, note1, note2,
                                        note_log_info, by_variability, by_user, by_place, by_instrument, by_name,
                                        by_rec, by_dec, by_type, by_mag, by_note, by_constilation, constilation)
        self.objects_table.clear()
        self.filtered_stars.change_stars_set(sorted_star)
        self.filtered_stars.change_key_set(self.stars.key)

        if self.sort_by_combobox.currentIndex() == 0:
            sort_by = "Name"
        elif self.sort_by_combobox.currentIndex() == 1:
            sort_by = "Alt_name"
        elif self.sort_by_combobox.currentIndex() == 2:
            sort_by = "Rec"
        elif self.sort_by_combobox.currentIndex() == 3:
            sort_by = "Dec"
        elif self.sort_by_combobox.currentIndex() == 4:
            sort_by = "Type"
        elif self.sort_by_combobox.currentIndex() == 5:
            sort_by = "Mag"
        else:
            sort_by = "Name"

        self.filtered_stars.sort_by(sort_by)

        keys = self.filtered_stars.key
        table_key = [keys[1], keys[2], keys[3], keys[4], keys[6], keys[9], keys[15], keys[16], keys[17], keys[18],
                     keys[19], keys[20], keys[37], keys[38], keys[39], keys[40]]
        self.objects_table.setRowCount(len(self.filtered_stars.stars))
        self.objects_table.setColumnCount(len(table_key))
        self.objects_table.setHorizontalHeaderLabels(table_key)
        current_star_index = -1
        for i, star in enumerate(self.filtered_stars.stars):
            if star.name() == current_set_name:
                current_star_index = i
            item = QtWidgets.QTableWidgetItem(star.name())
            item.setFlags(QtCore.Qt.ItemIsEnabled)
            self.objects_table.setItem(i, 0, item)

            item = QtWidgets.QTableWidgetItem(star.alt_name())
            item.setFlags(QtCore.Qt.ItemIsEnabled)
            item.setFlags(QtCore.Qt.ItemIsSelectable)
            self.objects_table.setItem(i, 1, item)

            item = QtWidgets.QTableWidgetItem(coordinate_to_text(star.rektascenze(), coordinate_format="hours"))
            item.setFlags(QtCore.Qt.ItemIsEnabled)
            item.setFlags(QtCore.Qt.ItemIsSelectable)
            self.objects_table.setItem(i, 2, item)

            item = QtWidgets.QTableWidgetItem(coordinate_to_text(star.declination()))
            item.setFlags(QtCore.Qt.ItemIsEnabled)
            item.setFlags(QtCore.Qt.ItemIsSelectable)
            self.objects_table.setItem(i, 3, item)

            item = QtWidgets.QTableWidgetItem(str(star.mag()))
            item.setFlags(QtCore.Qt.ItemIsEnabled)
            item.setFlags(QtCore.Qt.ItemIsSelectable)
            self.objects_table.setItem(i, 4, item)

            item = QtWidgets.QTableWidgetItem(star.type())
            item.setFlags(QtCore.Qt.ItemIsEnabled)
            item.setFlags(QtCore.Qt.ItemIsSelectable)
            self.objects_table.setItem(i, 5, item)

            item = QtWidgets.QTableWidgetItem(star.ucac4())
            item.setFlags(QtCore.Qt.ItemIsEnabled)
            item.setFlags(QtCore.Qt.ItemIsSelectable)
            self.objects_table.setItem(i, 6, item)

            item = QtWidgets.QTableWidgetItem(star.usnob1())
            item.setFlags(QtCore.Qt.ItemIsEnabled)
            item.setFlags(QtCore.Qt.ItemIsSelectable)
            self.objects_table.setItem(i, 7, item)

            item = QtWidgets.QTableWidgetItem(star.gaia())
            item.setFlags(QtCore.Qt.ItemIsEnabled)
            item.setFlags(QtCore.Qt.ItemIsSelectable)
            self.objects_table.setItem(i, 8, item)

            item = QtWidgets.QTableWidgetItem(star.vsx())
            item.setFlags(QtCore.Qt.ItemIsEnabled)
            item.setFlags(QtCore.Qt.ItemIsSelectable)
            self.objects_table.setItem(i, 9, item)

            item = QtWidgets.QTableWidgetItem(star.asassn())
            item.setFlags(QtCore.Qt.ItemIsEnabled)
            item.setFlags(QtCore.Qt.ItemIsSelectable)
            self.objects_table.setItem(i, 10, item)

            item = QtWidgets.QTableWidgetItem(star.tess())
            item.setFlags(QtCore.Qt.ItemIsEnabled)
            item.setFlags(QtCore.Qt.ItemIsSelectable)
            self.objects_table.setItem(i, 11, item)

            item = QtWidgets.QTableWidgetItem(",".join(star.user_list()))
            item.setFlags(QtCore.Qt.ItemIsEnabled)
            item.setFlags(QtCore.Qt.ItemIsSelectable)
            self.objects_table.setItem(i, 12, item)

            item = QtWidgets.QTableWidgetItem(",".join(star.place_list()))
            item.setFlags(QtCore.Qt.ItemIsEnabled)
            item.setFlags(QtCore.Qt.ItemIsSelectable)
            self.objects_table.setItem(i, 13, item)

            item = QtWidgets.QTableWidgetItem(",".join(star.instrument_list()))
            item.setFlags(QtCore.Qt.ItemIsEnabled)
            item.setFlags(QtCore.Qt.ItemIsSelectable)
            self.objects_table.setItem(i, 14, item)
            if star.variability():
                variability = "VAR"
            else:
                variability = "CMP"

            item = QtWidgets.QTableWidgetItem(variability)
            item.setFlags(QtCore.Qt.ItemIsEnabled)
            item.setFlags(QtCore.Qt.ItemIsSelectable)
            self.objects_table.setItem(i, 15, item)

        self.objects_table.resizeColumnsToContents()
        if self.filtered_stars.stars:
            if current_star_index > -1:
                self.objects_table.selectRow(current_star_index)
            else:
                self.object_detail_box.setEnabled(False)

        if self.object_show_detail_checkbox.isChecked():
            self.show_prediction()

    def fill_user(self):
        user_list = self.database.return_list_by_key("name", "users")

        if user_list:
            # self.user_delete.setEnabled(True)
            for user in user_list:
                self.user_combobox.addItem(user)
        else:
            self.user_combobox.addItem("add user")
            # self.user_delete.setEnabled(False)

    def fill_type_boxes(self):
        self.filter_type_key1.clear()
        self.filter_type_key2.clear()
        self.filter_type_key3.clear()
        self.filter_type_key3.clear()
        star_types = [""]
        for star in self.stars.stars:
            if not star.type() in star_types:
                star_types.append(star.type())
        star_types.sort()
        for star_type in star_types:
            self.filter_type_key1.addItem(star_type)
            self.filter_type_key2.addItem(star_type)
            self.filter_type_key3.addItem(star_type)
            self.filter_type_key4.addItem(star_type)
        self.filter_type_key1.setCurrentText("")
        self.filter_type_key2.setCurrentText("")
        self.filter_type_key3.setCurrentText("")
        self.filter_type_key3.setCurrentText("")

    def h_changed(self):
        self.place.set_minimum_h(radians(self.h_spinbox.value()))
        self.places.edit_h(self.place.name, radians(self.h_spinbox.value()), radians(self.sun_h_set_spinbox.value()))
        try:
            self.horizon_set_window.change_h(str(self.h_spinbox.value()))
            self.horizon_set_window.update()
        except:
            pass
        try:
            current_star = self.filtered_stars.stars[self.objects_table.currentRow()].name()
        except:
            return
        self.fill_object()
        self.show_prediction()
        self.objects_table.selectRow(self.filtered_stars.star_index(current_star))

    def save_user_environment(self):
        prediction_select_column_setup = self.prediction2.columns_setup
        try:
            prediction_sort_column_setup = self.prediction2.sort_by_combobox.currentText()
        except:
            prediction_sort_column_setup = ""
            # prediction_sort_column_setup = ["1", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0",
            #                                "0", "0", "0", "0", "0", "0"]
        prediction_visibility_setup = []
        try:
            if self.prediction2.visibility_sun_checkbox.isChecked():
                prediction_visibility_setup.append("1")
            else:
                prediction_visibility_setup.append("0")
            if self.prediction2.visibility_horizon_checkbox.isChecked():
                prediction_visibility_setup.append("1")
            else:
                prediction_visibility_setup.append("0")
            if self.prediction2.visibility_moon_checkbox.isChecked():
                prediction_visibility_setup.append("1")
            else:
                prediction_visibility_setup.append("0")
        except:
            pass
            # prediction_visibility_setup = ["1", "1", "0"]
        time_extension_setup = []
        try:
            time_extension_setup.append(str(self.prediction2.lightcurve_window.
                                            lc_time_start_doublespinbox.value()))
            time_extension_setup.append(str(self.prediction2.lightcurve_window.lc_time_end_doublespinbox.value()))
        except:
            pass
            # time_extension_setup = ["1", "1"]

        object_sort_by_setup = [str(self.sort_by_combobox.currentIndex())]

        object_filtered_by_setup = []
        if self.filter_by_var_checkbox.isChecked():
            object_filtered_by_setup.append("1")
        else:
            object_filtered_by_setup.append("0")
        if self.filter_by_user_checkbox.isChecked():
            object_filtered_by_setup.append("1")
        else:
            object_filtered_by_setup.append("0")
        if self.filter_by_place_checkbox.isChecked():
            object_filtered_by_setup.append("1")
        else:
            object_filtered_by_setup.append("0")
        if self.filter_by_instrument_checkbox.isChecked():
            object_filtered_by_setup.append("1")
        else:
            object_filtered_by_setup.append("0")
        if self.filter_by_name_checkbox.isChecked():
            object_filtered_by_setup.append("1")
        else:
            object_filtered_by_setup.append("0")
        if self.filter_by_rec_checkbox.isChecked():
            object_filtered_by_setup.append("1")
        else:
            object_filtered_by_setup.append("0")
        if self.filter_by_dec_checkbox.isChecked():
            object_filtered_by_setup.append("1")
        else:
            object_filtered_by_setup.append("0")
        if self.filter_by_type_checkbox.isChecked():
            object_filtered_by_setup.append("1")
        else:
            object_filtered_by_setup.append("0")
        if self.filter_by_mag_checkbox.isChecked():
            object_filtered_by_setup.append("1")
        else:
            object_filtered_by_setup.append("0")
        if self.filter_by_note_checkbox.isChecked():
            object_filtered_by_setup.append("1")
        else:
            object_filtered_by_setup.append("0")

        coordinate_setup = []
        coordinate_setup.append(str(self.filter_rec_h_start.value()))
        coordinate_setup.append(str(self.filter_rec_m_start.value()))
        coordinate_setup.append(str(self.filter_rec_s_start.value()))
        coordinate_setup.append(str(self.filter_rec_h_end.value()))
        coordinate_setup.append(str(self.filter_rec_m_end.value()))
        coordinate_setup.append(str(self.filter_rec_s_end.value()))
        coordinate_setup.append(str(self.filter_dec_h_start.value()))
        coordinate_setup.append(str(self.filter_dec_m_start.value()))
        coordinate_setup.append(str(self.filter_dec_s_start.value()))
        coordinate_setup.append(str(self.filter_dec_h_end.value()))
        coordinate_setup.append(str(self.filter_dec_m_end.value()))
        coordinate_setup.append(str(self.filter_dec_s_end.value()))

        texts_filter_setup_name_key1 = self.filter_name_key1.text()
        texts_filter_setup_name_key2 = self.filter_name_key2.text()
        texts_filter_setup_type_key1 = self.filter_type_key1.currentText()
        texts_filter_setup_type_key2 = self.filter_type_key2.currentText()
        texts_filter_setup_type_key3 = self.filter_type_key3.currentText()
        texts_filter_setup_type_key4 = self.filter_type_key4.currentText()
        texts_filter_setup_mag_start = str(self.filter_mag_start.value())
        texts_filter_setup_mag_end = str(self.filter_mag_end.value())
        texts_filter_setup_note_key1 = self.filter_note_key1.text()
        texts_filter_setup_note_key2 = self.filter_note_key2.text()
        texts_filter_setup_note_key3 = self.filter_note_bool.currentText()
        self.tess_menu_window.save_photometry_setting()

        self.user.edit_environment(prediction_select_column_setup, prediction_sort_column_setup,
                                   prediction_visibility_setup, object_filtered_by_setup,
                                   coordinate_setup, object_sort_by_setup, time_extension_setup,
                                   texts_filter_setup_name_key1, texts_filter_setup_name_key2,
                                   texts_filter_setup_type_key1, texts_filter_setup_type_key2,
                                   texts_filter_setup_type_key3, texts_filter_setup_type_key4,
                                   texts_filter_setup_mag_start, texts_filter_setup_mag_end,
                                   texts_filter_setup_note_key1, texts_filter_setup_note_key2,
                                   texts_filter_setup_note_key3)
        self.users.edit_environments(self.user)

    def LST_now_setting(self):
        jd = date_to_jd(datetime.now(timezone.utc))
        jd_text = str(round(jd, 5))
        while len(jd_text) < 13:
            jd_text = jd_text + "0"
        self.local_jd_now_label.setText(jd_text)
        star_time = (21.9433888888 + degrees(self.database.place.longitude) / 15 + (
                    jd - 2458534) * 24 * 1.0027379093) % 24
        star_time_h = floor(star_time)
        star_time_m = floor((star_time - star_time_h) * 60)
        star_time_s = floor((((star_time - star_time_h) * 60) - star_time_m) * 60)
        if star_time_h < 10:
            h = "0" + str(star_time_h) + "h "
        else:
            h = str(star_time_h) + "h "
        if star_time_m < 10:
            m = "0" + str(star_time_m) + "m "
        else:
            m = str(star_time_m) + "m "
        if star_time_s < 10:
            s = "0" + str(star_time_s) + "s"
        else:
            s = str(star_time_s) + "s"
        lst_text = h + m + s
        self.local_star_time_label.setText(lst_text)

    def set_horizon(self):
        if self.observer_combobox.currentText() in ["add user", "add place"]:
            return
        else:
            self.horizon_set_window.horizon = self.database.place.horizon()
            self.horizon_set_window.azimuth = self.horizon_set_window.horizon.azimuth()
            self.h_altitude = self.horizon_set_window.horizon.h_altitude()
            self.horizon_set_window.show()

    def show_prediction(self):
        if self.filtered_stars.stars:
            stars_quantity = len(self.filtered_stars.stars)
            days_quantity = int(self.time_period.jd_end() - self.time_period.jd_start()) + 1
            if stars_quantity * days_quantity > 5000:
                a = Popup("Prediction warning", "A long period or a large number of stars. It may take longer.",
                          buttons="OK, Exit".split(","))
                if a.do() == 1:
                    self.object_show_detail_checkbox.setChecked(False)
                    return
            if self.object_show_detail_checkbox.isChecked():
                self.prediction2.fill_prediction()
                self.prediction2.show()
            else:
                self.prediction2.close()

        else:
            self.prediction2.close()

    def time_period_end_change(self):
        a = self.period_end_dateedit.date()
        b = self.period_end_timeedit.time()
        jd = (date_to_jd(datetime(year=a.year(), month=a.month(), day=a.day(), hour=b.hour(), minute=b.minute(),
                                  tzinfo=timezone.utc)))
        self.time_period.set_jd_end(jd)
        if self.time_period.jd_end() <= self.time_period.jd_start():
            self.time_period.set_jd_start(self.time_period.jd_end() - 1)
            self.period_start_dateedit.setDate(jd_to_date(self.time_period.jd_start()))
        self.fill_sun_moon()
        self.julian_date_end_label.setText(str(round(self.time_period.jd_end(), 5)))

    def time_period_start_change(self):
        a = self.period_start_dateedit.date()
        b = self.period_start_timeedit.time()
        jd = (date_to_jd(datetime(year=a.year(), month=a.month(), day=a.day(), hour=b.hour(), minute=b.minute(),
                                  tzinfo=timezone.utc)))
        self.time_period.set_jd_start(jd)
        if self.time_period.jd_end() <= self.time_period.jd_start():
            self.time_period.set_jd_end(self.time_period.jd_start() + 1)
            self.period_end_dateedit.setDate(jd_to_date(self.time_period.jd_end()))
        self.fill_sun_moon()
        self.julian_date_start_label.setText(str(round(self.time_period.jd_start(), 5)))

    def update(self):
        self.LST_now_setting()
        t = threading.Timer(1, self.update)
        t.start()

    def export(self):
        self.export_window.clear_window()
        self.export_window.show()
        export_file_stars = []  # exported stars
        export_file_var = []  # variability
        export_file_var_name = []  # exported stars names
        export_file_comparison_stars = []  # comparison stars
        missing_comperison_star_id = []
        comparison_star_in_filtered_star_id = []
        for star in self.filtered_stars.stars:
            if not star.variability():
                comparison_star_in_filtered_star_id.append(str(star.id()))
        for star in self.filtered_stars.stars:
            if star.variability():
                if not str(star.comp0()) in comparison_star_in_filtered_star_id and not str(star.comp0()) in missing_comperison_star_id:
                    missing_comperison_star_id.append(str(star.comp0()))
                if not str(star.comp1()) in comparison_star_in_filtered_star_id and not str(star.comp1()) in missing_comperison_star_id:
                    missing_comperison_star_id.append(str(star.comp1()))
                if not str(star.comp2()) in comparison_star_in_filtered_star_id and not str(star.comp2()) in missing_comperison_star_id:
                    missing_comperison_star_id.append(str(star.comp2()))
                if not str(star.comp3()) in comparison_star_in_filtered_star_id and not str(star.comp3()) in missing_comperison_star_id:
                    missing_comperison_star_id.append(str(star.comp3()))
                if not str(star.comp4()) in comparison_star_in_filtered_star_id and not str(star.comp4()) in missing_comperison_star_id:
                    missing_comperison_star_id.append(str(star.comp4()))
                if not str(star.comp5()) in comparison_star_in_filtered_star_id and not str(star.comp5()) in missing_comperison_star_id:
                    missing_comperison_star_id.append(str(star.comp5()))
                if not str(star.comp6()) in comparison_star_in_filtered_star_id and not str(star.comp6()) in missing_comperison_star_id:
                    missing_comperison_star_id.append(str(star.comp6()))
                if not str(star.comp7()) in comparison_star_in_filtered_star_id and not str(star.comp7()) in missing_comperison_star_id:
                    missing_comperison_star_id.append(str(star.comp7()))
                if not str(star.comp8()) in comparison_star_in_filtered_star_id and not str(star.comp8()) in missing_comperison_star_id:
                    missing_comperison_star_id.append(str(star.comp8()))
                if not str(star.comp9()) in comparison_star_in_filtered_star_id and not str(star.comp9()) in missing_comperison_star_id:
                    missing_comperison_star_id.append(str(star.comp9()))
                if not str(star.chk1()) in comparison_star_in_filtered_star_id and not str(star.chk1()) in missing_comperison_star_id:
                    missing_comperison_star_id.append(str(star.chk1()))
                if not star.name() in export_file_var_name:
                    export_file_var_name.append(star.name())
            export_file_stars.append(star)
        # fill stars in export window
        table_key = self.filtered_stars.key
        extend_table_key = table_key + ["", ""]
        stars_info_table = []
        for star in export_file_stars:
            star_info_table_row = [str(star.id()), star.name(), star.alt_name(), str(star.rektascenze()),
                                   str(star.declination()), str(star.eq()), str(star.mag()), star.constellation(),
                                   star.tess_sectors(), star.type(), star.note1(), star.note2(), star.note3(),
                                   str(star.b_v()), str(star.j_k()), star.ucac4(), star.usnob1(), star.gaia(),
                                   star.vsx(), star.asassn(), star.tess(), str(star.comp0()), str(star.comp1()),
                                   str(star.comp2()), str(star.comp3()), str(star.comp4()), str(star.comp5()),
                                   str(star.comp6()), str(star.comp7()), str(star.comp8()), str(star.comp9()),
                                   str(star.chk1()), "", "", "", "", "", "", "", "", str(star.variability()), "", ""]
            stars_info_table.append(star_info_table_row)
        self.export_window.fill_stars(extend_table_key, stars_info_table, True)
        # search for comparison
        comparison_info_table = []
        for star in self.stars.stars:
            if not star.variability() and str(star.id()) in missing_comperison_star_id:
                export_file_comparison_stars.append(star)
                star_info_table_row = [str(star.id()), star.name(), star.alt_name(), str(star.rektascenze()),
                                       str(star.declination()), str(star.eq()), str(star.mag()), star.constellation(),
                                       "", star.type(), star.note1(), star.note2(), star.note3(),
                                       str(star.b_v()), str(star.j_k()), star.ucac4(), star.usnob1(), star.gaia(),
                                       star.vsx(), star.asassn(), star.tess(), "", "", "", "", "", "", "", "", "", "",
                                       "", "", "", "", "", "", "", "", "", str(star.variability()), "", ""]
                comparison_info_table.append(star_info_table_row)
        self.export_window.fill_stars(extend_table_key, comparison_info_table, False)
        # search for variability
        table_key_variable = self.variable.key
        extend_table_key_variable = table_key_variable + [""]
        variable_info_table = []
        for variable in self.variable.variables:
            if variable.name() in export_file_var_name:
                export_file_var.append(variable)
                variable_info_table_row = [variable.name(), variable.pair(), variable.variability_type(),
                                           str(variable.period()), str(variable.epoch()), str(variable.amplitude_p()),
                                           str(variable.amplitude_s()), str(variable.d_eclipse_prim()),
                                           str(variable.d_eclipse_sec()), str(variable.d_minimum_prim()),
                                           str(variable.d_minimum_sec()), str(variable.mag0()), str(variable.a_pri()),
                                           str(variable.d_pri()), str(variable.g_pri()), str(variable.c_pri()),
                                           str(variable.a_sin1()), str(variable.a_sin2()), str(variable.a_sin3()),
                                           str(variable.apsidal_movement_correction()), str(variable.sec_phase()),
                                           str(variable.a_sec()), str(variable.d_sec()), str(variable.g_sec()),
                                           str(variable.c_sec()), str(variable.a_cos1()), str(variable.a_cos2()),
                                           str(variable.a_cos3()), str(variable.lc_offset()),
                                           str(variable.in_prediction()), ""]
                variable_info_table.append(variable_info_table_row)
        self.export_window.fill_variability(extend_table_key_variable, variable_info_table)

    def import_stars(self):
        path_to_file = QtWidgets.QFileDialog.getOpenFileName(caption="Import file", directory=os.getenv("APPDATA"),
                                                             filter="*.ste")
        if path_to_file[0] == "":
            return
        try:
            with open(path_to_file[0], "r", encoding="utf-8") as data:
                rows = reader(data, delimiter=";")
                import_table = [row for row in rows]
        except:
            a = Popup("Import error", "Failed to create file\n{0}\nPlease check your permissions.".format(path_to_file))
            a.do()
            return
        self.import_window.clear_window()
        if import_table[0] == ["&[Stars]"] and ["&[Variables]"] in import_table and ["&[Comparison]"] in import_table \
                and import_table[-1] == ["&[End of export]"]:
            start_variables_index = import_table.index(["&[Variables]"])
            start_comparisons_index = import_table.index(["&[Comparison]"])
            if import_table[1] == self.stars.key and import_table[start_variables_index + 1] == self.variable.key:
                all_stars = []
                star_keys = import_table[1] + ["", ""]
                all_variables = []
                variable_keys = import_table[start_variables_index + 1] + [""]
                all_comparisons = []
                for i in range(2, start_variables_index):
                    all_stars.append(import_table[i] + ["", ""])
                for i in range(start_variables_index + 2, start_comparisons_index):
                    all_variables.append(import_table[i] + [""])
                for i in range(start_comparisons_index + 2, len(import_table)-1):
                    all_comparisons.append(import_table[i] + ["", ""])
                self.import_window.show()
                self.import_window.fill_stars(star_keys, all_stars, True)
                self.import_window.fill_stars(star_keys, all_comparisons, False)
                self.import_window.fill_variability(variable_keys, all_variables)
                self.import_window.data_integrity()
            else:
                a = Popup("Import error", "Stars or variables structure does not match")
                a.do()
                return
        else:
            a = Popup("Import error", "The file structure does not match")
            a.do()
            return


class Popup(QtWidgets.QMessageBox):
    def __init__(self, title, text, buttons=["Ok"]):
        super(Popup, self).__init__()

        self.setWindowTitle(title)
        self.setText(text)
        self.setWindowIcon(QtGui.QIcon("exclamation-shield-frame.png"))
        self.buttons = buttons

        for txt in self.buttons:
            b = QtWidgets.QPushButton(txt)
            self.addButton(b, QtWidgets.QMessageBox.NoRole)

    def do(self):
        answer = self.exec_()
        return answer

class ExportWindow(QtWidgets.QWidget):

    def __init__(self, *args, **kvargs):
        super(ExportWindow, self).__init__(*args, **kvargs)

        self.setWindowTitle("Export (stars)")
        self.window_layout = QtWidgets.QGridLayout()
        self.setLayout(self.window_layout)
        self.setWindowIcon(QtGui.QIcon("application-export.png"))
        self.info_text = ""
        self.stars = []
        self.star_key = []
        self.comparisons = []
        self.variable_key = []
        self.variables = []
        self.__line = "______________________________\n"


        self.choice_star_checkbox = QtWidgets.QCheckBox("discard/reinstate selected star")
        self.star_without_comparison_checkbox = QtWidgets.QCheckBox("with/wo comparison stars (selected star)")
        self.export_without_comparison_checkbox = QtWidgets.QCheckBox("Export with/wo comparison stars (all stars)")
        self.star_table_widget = QtWidgets.QTableWidget()
        self.comparison_table_widget = QtWidgets.QTableWidget()
        self.variability_table_widget = QtWidgets.QTableWidget()
        self.export_information_text_edit = QtWidgets.QTextEdit()
        self.continue_button = QtWidgets.QPushButton("SAVE FILE(*.ste)")
        self.exit_button = QtWidgets.QPushButton("Close without save")
        self.__build()

    def __build(self):
        self.window_layout.addWidget(QtWidgets.QLabel("exported stars"), 0, 0)
        self.window_layout.addWidget(self.star_table_widget, 1, 0, 10, 10)
        self.window_layout.addWidget(QtWidgets.QLabel("variability of exported stars"), 11, 0)
        self.window_layout.addWidget(self.variability_table_widget, 12, 0, 10, 10)
        self.window_layout.addWidget(QtWidgets.QLabel("the necessary comparison stars"), 22, 0)
        self.window_layout.addWidget(self.comparison_table_widget, 23, 0, 5, 10)
        self.window_layout.addWidget(QtWidgets.QLabel("Info panel:"), 28, 0)
        self.window_layout.addWidget(self.export_information_text_edit, 28, 3, 6, 7)
        self.window_layout.addWidget(self.choice_star_checkbox, 29, 0, 1, 3)
        self.window_layout.addWidget(self.star_without_comparison_checkbox, 30, 0, 1, 3)
        self.window_layout.addWidget(self.export_without_comparison_checkbox, 31, 0, 1, 3)
        self.window_layout.addWidget(self.continue_button, 32, 0, 1, 3)
        self.window_layout.addWidget(self.exit_button, 33, 0, 1, 3)

    def setup(self):
        from step_application import root
        self.step_main_form = root.step_main_form

        self.choice_star_checkbox.clicked.connect(self.choice_star_checkbox_was_checked)
        self.star_table_widget.itemSelectionChanged.connect(self.__star_was_changed)
        self.star_without_comparison_checkbox.clicked.connect(self.__with_comparison_was_clicked)
        self.export_without_comparison_checkbox.clicked.connect(self.__export_without_comparison_was_clicked)
        self.continue_button.clicked.connect(self.save_export_file)
        self.exit_button.clicked.connect(self.close_window)

    def clear_window(self):
        self.info_text = ""
        self.choice_star_checkbox.setChecked(False)
        self.star_without_comparison_checkbox.setChecked(False)
        self.export_without_comparison_checkbox.setChecked(False)
        self.choice_star_checkbox.setEnabled(True)
        self.star_without_comparison_checkbox.setEnabled(True)
        self.star_table_widget.clear()
        self.comparison_table_widget.clear()
        self.variability_table_widget.clear()
        self.export_information_text_edit.setText("")
        self.stars = []
        self.comparisons = []
        self.variables = []

    def __set_item_background(self, table_id, row, column, r=255, g=0, b=0, alfa=60):
        if column == "all":
            if table_id == "star":
                for i in range(0, 43):
                    self.star_table_widget.item(row, i).setBackground(QtGui.QBrush(QtGui.QColor(r, g, b, alfa)))
            elif table_id == "comp":
                for i in range(0, 43):
                    self.comparison_table_widget.item(row, i).setBackground(QtGui.QBrush(QtGui.QColor(r, g, b, alfa)))
            elif table_id == "var":
                for i in range(0, 31):
                    self.variability_table_widget.item(row, i).setBackground(QtGui.QBrush(QtGui.QColor(r, g, b, alfa)))
            else:
                pass
        else:
            if table_id == "star":
                self.star_table_widget.item(row, column).setBackground(QtGui.QBrush(QtGui.QColor(r, g, b, alfa)))
            elif table_id == "comp":
                self.comparison_table_widget.item(row, column).setBackground(QtGui.QBrush(QtGui.QColor(r, g, b, alfa)))
            elif table_id == "var":
                self.variability_table_widget.item(row, column).setBackground(QtGui.QBrush(QtGui.QColor(r, g, b, alfa)))
            else:
                pass

    def fill_stars(self, table_key, stars, variability):
        self.star_key = table_key
        if variability:
            table_widget = self.star_table_widget
            self.stars = stars
        else:
            table_widget = self.comparison_table_widget
            self.comparisons = stars
        table_widget.setRowCount(len(stars))
        table_widget.setColumnCount(len(table_key))
        table_widget.setHorizontalHeaderLabels(table_key)
        for i in range(len(stars)):
            for j in range(len(stars[0])):
                item = QtWidgets.QTableWidgetItem(stars[i][j])
                item.setFlags(QtCore.Qt.ItemIsEnabled)
                if variability:
                    item.setFlags(QtCore.Qt.ItemIsSelectable)
                table_widget.setItem(i, j, item)
        table_widget.resizeColumnsToContents()
        if variability:
            self.info_text = "Exported stars have been found a filled\n" + self.__line + self.info_text
        else:
            self.info_text = "Related comparison stars have been found a filled\n" + self.info_text
        self.export_information_text_edit.setText(self.info_text)
        QtWidgets.QApplication.processEvents()

    def fill_variability(self, table_key, variability):
        self.variable_key = table_key
        self.variables = variability
        self.variability_table_widget.setRowCount(len(variability))
        self.variability_table_widget.setColumnCount(len(table_key))
        self.variability_table_widget.setHorizontalHeaderLabels(table_key)
        for i in range(len(variability)):
            for j in range(len(variability[0])):
                item = QtWidgets.QTableWidgetItem(variability[i][j])
                item.setFlags(QtCore.Qt.ItemIsEnabled)
                self.variability_table_widget.setItem(i, j, item)
        self.variability_table_widget.resizeColumnsToContents()
        self.info_text = "Variability for exported stars has been found a filled\n" + self.info_text
        self.export_information_text_edit.setText(self.info_text)
        QtWidgets.QApplication.processEvents()

    def choice_star_checkbox_was_checked(self):
        row = self.star_table_widget.currentRow()
        if row > -1:
            if self.choice_star_checkbox.isChecked():
                self.stars[row][41] = "discarded"
                self.star_without_comparison_checkbox.setEnabled(False)
                self.star_table_widget.setItem(row, 41, QtWidgets.QTableWidgetItem("discarded"))
                self.__set_item_background("star", row, "all")
                self.info_text = "The star {0} has been discarded from export file\n".format(self.stars[row][1]) + self.info_text
                self.export_information_text_edit.setText(self.info_text)
                for i, variability in enumerate(self.variables):
                    if variability[0] == self.stars[row][1]:
                        variability[30] = "discarded"
                        self.variability_table_widget.setItem(i, 30, QtWidgets.QTableWidgetItem("discarded"))
                        self.__set_item_background("var", i, "all")
                        self.info_text = "The star {0} variability {1} has been discarded from export file\n".format(
                            variability[0], variability[1]) + self.info_text
                        self.export_information_text_edit.setText(self.info_text)
            else:
                self.stars[row][41] = ""
                self.star_table_widget.setItem(row, 41, QtWidgets.QTableWidgetItem(""))
                self.__set_item_background("star", row, "all", r=0, alfa=0)
                self.star_without_comparison_checkbox.setEnabled(True)
                self.info_text = "The star {0} has been reinstated to the export file\n".format(self.stars[row][1]) + self.info_text
                self.export_information_text_edit.setText(self.info_text)
                for i, variability in enumerate(self.variables):
                    if variability[0] == self.stars[row][1]:
                        variability[30] = ""
                        self.__set_item_background("var", i, "all", r=0, alfa=0)
                        self.variability_table_widget.setItem(i, 30, QtWidgets.QTableWidgetItem(""))
                        self.info_text = "The star {0} variability {1} has been reinstated to the export file\n".format(
                            variability[0], variability[1]) + self.info_text
                        self.export_information_text_edit.setText(self.info_text)

            comparison_id_list = self.__check_comparison_star()
            for k, comparison in enumerate(self.comparisons):
                if comparison[0] in comparison_id_list:
                    if comparison[41] == "discarded":
                        comparison[41] = ""
                        self.comparison_table_widget.setItem(row, 41, QtWidgets.QTableWidgetItem(""))
                        self.info_text = "The comparison star {0} id: {1} has been reinstated to export file\n".format(
                            comparison[1], comparison[0]) + self.info_text
                        self.export_information_text_edit.setText(self.info_text)
                        if not self.export_without_comparison_checkbox.isChecked():
                            self.__set_item_background("comp", k, "all", r=0, alfa=0)
                else:
                    if comparison[41] == "":
                        comparison[41] = "discarded"
                        self.comparison_table_widget.setItem(row, 41, QtWidgets.QTableWidgetItem("discarded"))
                        self.info_text = "The comparison star {0} id: {1} has been discarded from export file\n".format(
                            comparison[1], comparison[0]) + self.info_text
                        self.export_information_text_edit.setText(self.info_text)
                        self.__set_item_background("comp", k, "all")
        else:
            self.info_text = "No star is marked, it cannot be discarded\n" + self.info_text
            self.export_information_text_edit.setText(self.info_text)
            self.choice_star_checkbox.setChecked(False)

    def __star_was_changed(self):
        row = self.star_table_widget.currentRow()
        if row > -1:
            if self.stars[row][41] == "":
                self.star_without_comparison_checkbox.setEnabled(True)
                self.choice_star_checkbox.setChecked(False)
            else:
                self.star_without_comparison_checkbox.setEnabled(False)
                self.choice_star_checkbox.setChecked(True)
            if self.stars[row][42] == "":
                self.choice_star_checkbox.setEnabled(True)
                self.star_without_comparison_checkbox.setChecked(False)
            else:
                self.choice_star_checkbox.setEnabled(False)
                self.star_without_comparison_checkbox.setChecked(True)
        else:
            self.choice_star_checkbox.setChecked(False)
            self.star_without_comparison_checkbox.setChecked(False)
            self.choice_star_checkbox.setEnabled(True)
            self.star_without_comparison_checkbox.setEnabled(True)


    def __with_comparison_was_clicked(self):
        row = self.star_table_widget.currentRow()
        if row > -1:
            if self.star_without_comparison_checkbox.isChecked():
                self.choice_star_checkbox.setEnabled(False)
                self.stars[row][42] = "discarded"
                self.star_table_widget.setItem(row, 42, QtWidgets.QTableWidgetItem("discarded"))
                self.info_text = "The star {0} will be exported without comparison star\n".format(
                    self.stars[row][1]) + self.info_text
                self.export_information_text_edit.setText(self.info_text)
            else:
                self.choice_star_checkbox.setEnabled(True)
                self.stars[row][42] = ""
                self.star_table_widget.setItem(row, 42, QtWidgets.QTableWidgetItem(""))
                self.info_text = "The star {0} will be exported with comparison star\n".format(
                    self.stars[row][1]) + self.info_text
                self.export_information_text_edit.setText(self.info_text)

            comparison_id_list = self.__check_comparison_star()
            for k, comparison in enumerate(self.comparisons):
                if comparison[0] in comparison_id_list:
                    if comparison[41] == "discarded":
                        comparison[41] = ""
                        self.comparison_table_widget.setItem(row, 41, QtWidgets.QTableWidgetItem(""))
                        self.info_text = "The comparison star {0} id: {1} has been reinstated to export file\n".format(
                            comparison[1], comparison[0]) + self.info_text
                        self.export_information_text_edit.setText(self.info_text)
                        if not self.export_without_comparison_checkbox.isChecked():
                            self.__set_item_background("comp", k, "all", r=0, alfa=0)
                else:
                    if comparison[41] == "":
                        comparison[41] = "discarded"
                        self.comparison_table_widget.setItem(row, 41, QtWidgets.QTableWidgetItem("discarded"))
                        self.info_text = "The comparison star {0} id: {1} has been discarded from export file\n".format(
                            comparison[1], comparison[0]) + self.info_text
                        self.export_information_text_edit.setText(self.info_text)
                        self.__set_item_background("comp", k, "all")
        else:
            self.info_text = "No star is marked, it cannot be discarded\n" + self.info_text
            self.export_information_text_edit.setText(self.info_text)
            self.star_without_comparison_checkbox.setChecked(False)

    def __export_without_comparison_was_clicked(self):
        if self.export_without_comparison_checkbox.isChecked():
            for i in range(len(self.comparisons)):
                self.__set_item_background("comp", i, "all")
            self.info_text = "Information about comparison stars will be deletes." \
                             "All comparison stars have been discarded from export file\n" + self.info_text
            self.export_information_text_edit.setText(self.info_text)
        else:
            for i in range(len(self.comparisons)):
                if self.comparisons[i][41] == "":
                    self.__set_item_background("comp", i, "all", r=0, alfa=0)
            self.info_text = "All eligible comparison stars have been added\n" + self.info_text
            self.export_information_text_edit.setText(self.info_text)


    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        self.clear_window()

    def close_window(self):
        self.close()

    def __check_comparison_star(self):
        # str(star.id())0, star.name()1, star.alt_name()2, str(star.rektascenze())3,
        # str(star.declination())4, str(star.eq())5, str(star.mag())6, star.constellation()7,
        # star.tess_sectors()8, star.type()9, star.note1()10, star.note2()11, star.note3()12,
        # str(star.b_v())13, str(star.j_k())14, star.ucac4()15, star.usnob1()16, star.gaia()17,
        # star.vsx()18, star.asassn()19, star.tess()20, str(star.comp0())21, str(star.comp1())22,
        # str(star.comp2())23, str(star.comp3())24, str(star.comp4())25, str(star.comp5())26,
        # str(star.comp6())27, str(star.comp7())28, str(star.comp8())29, str(star.comp9())30,
        # str(star.chk1())31, ""32, ""33, ""34, ""35, ""36, ""37, ""38, ""39, str(star.variability())40, ""41, ""42

        comparison_star_in_stars_id = []
        for star in self.stars:
            if not star[40] and star[41] == "":
                comparison_star_in_stars_id.append(star[0])
        missing_comparison_star_id = []
        for star in self.stars:
            if star[41] == "" and star[42] == "":
                if not star[21] in comparison_star_in_stars_id and not star[21] in missing_comparison_star_id:
                    missing_comparison_star_id.append(star[21])
                if not star[22] in comparison_star_in_stars_id and not star[22] in missing_comparison_star_id:
                    missing_comparison_star_id.append(star[22])
                if not star[23] in comparison_star_in_stars_id and not star[23] in missing_comparison_star_id:
                    missing_comparison_star_id.append(star[23])
                if not star[24] in comparison_star_in_stars_id and not star[24] in missing_comparison_star_id:
                    missing_comparison_star_id.append(star[24])
                if not star[25] in comparison_star_in_stars_id and not star[25] in missing_comparison_star_id:
                    missing_comparison_star_id.append(star[25])
                if not star[26] in comparison_star_in_stars_id and not star[26] in missing_comparison_star_id:
                    missing_comparison_star_id.append(star[26])
                if not star[27] in comparison_star_in_stars_id and not star[27] in missing_comparison_star_id:
                    missing_comparison_star_id.append(star[27])
                if not star[28] in comparison_star_in_stars_id and not star[28] in missing_comparison_star_id:
                    missing_comparison_star_id.append(star[28])
                if not star[29] in comparison_star_in_stars_id and not star[29] in missing_comparison_star_id:
                    missing_comparison_star_id.append(star[29])
                if not star[30] in comparison_star_in_stars_id and not star[30] in missing_comparison_star_id:
                    missing_comparison_star_id.append(star[30])
                if not star[31] in comparison_star_in_stars_id and not star[31] in missing_comparison_star_id:
                    missing_comparison_star_id.append(star[31])
        return missing_comparison_star_id

    def save_export_file(self):
        for star in self.stars:
            if star[42] == "discarded":
                star[21], star[22], star[23], star[24], star[25], star[26], star[27] = "0", "0", "0", "0", "0", "0", "0"
                star[28], star[29], star[30], star[31] = "0", "0", "0", "0"
        export_csv = []
        export_csv.append(["&[Stars]"])
        export_csv.append(self.star_key[0:41])
        for star in self.stars:
            if not star[41]:
                export_csv.append(star[0:41])
        export_csv.append(["&[Variables]"])
        export_csv.append(self.variable_key[0:30])
        for variable in self.variables:
            if not variable[30]:
                export_csv.append(variable[0:30])
        export_csv.append(["&[Comparison]"])
        export_csv.append(self.star_key[0:41])
        if not self.export_without_comparison_checkbox.isChecked():
            for comparison in self.comparisons:
                if not comparison[41]:
                    export_csv.append(comparison[0:41])
        export_csv.append(["&[End of export]"])
        path_to_file = QtWidgets.QFileDialog.getSaveFileName(caption="Save export file", directory=os.getenv("APPDATA"),
                                                             filter="*.ste")
        try:
            if path_to_file[0]:
                with open(path_to_file[0], "w", encoding="utf-8") as f:
                    for u in export_csv:
                        radek = ";".join(u)
                        f.write(radek + "\n")
        except:
            a = Popup("Export error",
                      "Failed to create file\n{0}\nPlease check your permissions.".format(path_to_file[0]))
            a.do()

class ImportWindow(QtWidgets.QWidget):

    def __init__(self, *args, **kvargs):
        super(ImportWindow, self).__init__(*args, **kvargs)

        self.setWindowTitle("Import stars")
        self.window_layout = QtWidgets.QGridLayout()
        self.setLayout(self.window_layout)
        self.setWindowIcon(QtGui.QIcon("application-import.png"))
        self.info_text = ""
        self.stars = []
        self.star_key = []
        self.comparisons = []
        self.variable_key = []
        self.variables = []
        self.__status = 0
        self.__line = "______________________________\n"

        self.choice_star_checkbox = QtWidgets.QCheckBox("discard/reinstate star")
        self.star_without_comparison_checkbox = QtWidgets.QCheckBox("with/wo comparison star (selected star)")
        self.export_without_comparison_checkbox = QtWidgets.QCheckBox("Export with/wo comparison star")
        self.star_table_widget = QtWidgets.QTableWidget()
        self.comparison_table_widget = QtWidgets.QTableWidget()
        self.variability_table_widget = QtWidgets.QTableWidget()
        self.export_information_text_edit = QtWidgets.QTextEdit()
        self.continue_button = QtWidgets.QPushButton("Continue")
        self.exit_button = QtWidgets.QPushButton("Close w/o save")
        self.__build()

    def __build(self):
        self.window_layout.addWidget(QtWidgets.QLabel("Imported stars"), 0, 0)
        self.window_layout.addWidget(self.star_table_widget, 1, 0, 10, 10)
        self.window_layout.addWidget(QtWidgets.QLabel("variability of imported stars"), 11, 0)
        self.window_layout.addWidget(self.variability_table_widget, 12, 0, 10, 10)
        self.window_layout.addWidget(QtWidgets.QLabel("the necessary comparison stars"), 22, 0)
        self.window_layout.addWidget(self.comparison_table_widget, 23, 0, 5, 10)
        self.window_layout.addWidget(QtWidgets.QLabel("Info panel:"), 28, 0)
        self.window_layout.addWidget(self.export_information_text_edit, 28, 3, 6, 7)
        self.window_layout.addWidget(self.choice_star_checkbox, 29, 0, 1, 3)
        self.window_layout.addWidget(self.star_without_comparison_checkbox, 30, 0, 1, 3)
        self.window_layout.addWidget(self.export_without_comparison_checkbox, 31, 0, 1, 3)
        self.window_layout.addWidget(self.continue_button, 32, 0, 1, 3)
        self.window_layout.addWidget(self.exit_button, 33, 0, 1, 3)

    def setup(self):
        from step_application import root
        self.step_main_form = root.step_main_form
        self.const_abbrs = root.database.const_abbrs
        self.type_key_list = root.database.type_key_list
        self.my_stars = root.database.stars.stars
        self.my_variables = root.database.variables.variables
        self.database = root.database

        self.choice_star_checkbox.clicked.connect(self.choice_star_checkbox_was_checked)
        self.star_table_widget.itemSelectionChanged.connect(self.__star_was_changed)
        self.star_without_comparison_checkbox.clicked.connect(self.__with_comparison_was_clicked)
        self.export_without_comparison_checkbox.clicked.connect(self.__export_without_comparison_was_clicked)
        self.continue_button.clicked.connect(self.process_manager)
        self.exit_button.clicked.connect(self.close_window)


    def __delete_unusefull(self, with_renumber=True):
        delete_index = []
        for i, star in enumerate(self.stars):
            if not star[1] or star[41] == "discarded":
                delete_index.append(i)
                if not star[40] and with_renumber:
                    self.__renumber_comparison_star(star[0], 0)
        delete_index.sort(reverse=True)
        for index in delete_index:
            del(self.stars[index])
        delete_index = []
        for i, star in enumerate(self.comparisons):
            if not star[1] or star[41] == "discarded" or self.export_without_comparison_checkbox.isChecked():
                delete_index.append(i)
                if with_renumber:
                    self.__renumber_comparison_star(star[0], 0)
        delete_index.sort(reverse=True)
        for index in delete_index:
            del(self.comparisons[index])
        delete_index = []
        for i, star in enumerate(self.variables):
            if not star[0] or star[30] == "discarded":
                delete_index.append(i)
        delete_index.sort(reverse=True)
        for index in delete_index:
            del(self.variables[index])
        self.star_table_widget.clear()
        self.comparison_table_widget.clear()
        self.variability_table_widget.clear()
        self.fill_stars(self.star_key, self.stars, True)
        self.fill_stars(self.star_key, self.comparisons, False)
        self.fill_variability(self.variable_key, self.variables)

    def __renumber_comparison_star(self, old_number, new_number):
        for star in self.stars:
            if star[40]:
                for i in range(21, 32):
                    if star[i] == old_number:
                        star[i] = int(new_number)

    def process_manager(self):
        if self.__status == 0:
            self.__delete_unusefull()
            self.choice_star_checkbox.setChecked(False)
            self.star_without_comparison_checkbox.setChecked(False)
            self.export_without_comparison_checkbox.setChecked(False)
            self.choice_star_checkbox.setEnabled(True)
            self.star_without_comparison_checkbox.setEnabled(True)
            self.export_without_comparison_checkbox.setEnabled(True)
            self.__status = 1
            self.info_text = "All tables have been corrected. Now you can restrict the export according to your " \
                             "requirements or go to next step\n" + self.info_text
            self.export_information_text_edit.setText(self.info_text)
            self.__save_import_report()
            # self.continue_button.setText("Save")
        elif self.__status == 1:
            self.__delete_unusefull()
            self.choice_star_checkbox.setChecked(False)
            self.star_without_comparison_checkbox.setChecked(False)
            self.export_without_comparison_checkbox.setChecked(False)
            self.choice_star_checkbox.setEnabled(False)
            self.star_without_comparison_checkbox.setEnabled(False)
            self.export_without_comparison_checkbox.setEnabled(False)
            name_list = []
            rektascenze_list = []
            declination_list = []
            id_list = []
            for star in self.my_stars:
                name_list.append(star.name())
                rektascenze_list.append(star.rektascenze())
                declination_list.append(star.declination())
                id_list.append(star.id())
            all_stars = self.stars + self.comparisons
            for j, star in enumerate(all_stars):
                for i, declination in enumerate(declination_list):
                    if declination + 0.0002 > star[4] > declination - 0.0002 and star[1]:
                        distance_num = angular_separation(rektascenze_list[i], declination, star[3], star[4])
                        if distance_num < 0.0001:
                            if star[1] in name_list: # star already exist ( name and coordinate )
                                self.info_text = "Star {0} already exist (id:{1}) and cannot be imported. " \
                                                 "For comparison stars, the relation to other objects is adjusted " \
                                                 "accordingly.\n".format(star[1], id_list[i]) + self.info_text
                                self.export_information_text_edit.setText(self.info_text)
                                self.__save_import_report()
                                QtWidgets.QApplication.processEvents()
                                if j < len(self.stars):
                                    self.__set_item_background("star", j, "all")
                                else:
                                    self.__set_item_background("comp", j - len(self.stars), "all")
                                if star[40]:
                                    for k, variable in enumerate(self.variables):
                                        if variable[0] == star[1]:
                                            variable[0] = ""
                                            self.__set_item_background("var", k, "all")
                                else:
                                    self.__renumber_comparison_star(star[0], id_list[i])
                                star[1] = ""
                            else:
                                a = Popup("Star identification window",
                                          "The position of star {0} is very similar\nto the position of star {1} in "
                                          "your database.\nIs it the same star?".format(star[1], name_list[i]),
                                          ["The same", "Different star"])
                                if a.do() == 0:
                                    self.info_text = "Star {0} already exist (id:{1}) and cannot be imported. " \
                                                     "For comparison stars, the relation to other objects is adjusted " \
                                                     "accordingly.\n".format(star[1], id_list[i]) + self.info_text
                                    self.export_information_text_edit.setText(self.info_text)
                                    self.__save_import_report()
                                    QtWidgets.QApplication.processEvents()
                                    if j < len(self.stars):
                                        self.__set_item_background("star", j, "all")
                                    else:
                                        self.__set_item_background("comp", j - len(self.stars), "all")
                                    if star[40]:
                                        for k, variable in enumerate(self.variables):
                                            if variable[0] == star[1]:
                                                variable[0] = ""
                                                self.__set_item_background("var", k, "all")
                                    else:
                                        self.__renumber_comparison_star(star[0], id_list[i])
                                    star[1] = ""
            for j, star in enumerate(all_stars):
                if star[1] in name_list: # star name exist ( different coordinate )
                    self.info_text = "Star name {0} already exist (your id:{1}), but coordinate are different" \
                                     " Star cannot be imported. \n".format(star[1], id_list[i]) + \
                                     self.info_text
                    self.export_information_text_edit.setText(self.info_text)
                    self.__save_import_report()
                    QtWidgets.QApplication.processEvents()
                    if i < len(self.stars):
                        self.__set_item_background("star", j, "all")
                    else:
                        self.__set_item_background("comp", j - len(self.stars), "all")
                    if star[40]:
                        for k, variable in enumerate(self.variables):
                            if variable[0] == star[1]:
                                variable[0] = ""
                                self.__set_item_background("var", k, "all")
                    else:
                        self.__renumber_comparison_star(star[0], 0)
                    star[1] = ""
            list_of_comparison_star_id = self.__check_comparison_star()
            if 0 in list_of_comparison_star_id:
                list_of_comparison_star_id.remove(0)
            for k, comparison in enumerate(self.comparisons):
                if comparison[1]:
                    if not comparison[0] in list_of_comparison_star_id:
                        self.info_text = "Comparison id:{0} is not a comparison star for any variable star. It will " \
                                         "not be imported\n".format(comparison[0]) + self.info_text
                        self.__set_item_background("comp", k, "all")
                        self.export_information_text_edit.setText(self.info_text)
                        self.__save_import_report()
                        QtWidgets.QApplication.processEvents()
                        comparison[1] = ""
            self.info_text = "The structural integrity of the data in your database and imported stars was checked. " \
                             "After pressing the Continue key, the table will be adjusted according to the errors " \
                             "found. And stars will be finally imported\n" + self.info_text
            self.export_information_text_edit.setText(self.info_text)
            self.__save_import_report()
            QtWidgets.QApplication.processEvents()
            self.__status = 2
        elif self.__status == 2:
            self.__delete_unusefull(with_renumber=False)
            all_star = self.stars + self.comparisons
            for star in all_star:
                new_id = self.database.next_star()
                if not star[40]:
                    self.__renumber_comparison_star(star[0], new_id)
                star[0] = new_id
                self.database.increase_next_star()
            for star in all_star:
                # user_list = self.database.user.name()
                # place_list = self.database.place.name
                # instrument_list = self.database.instrument.id
                new_coor = Coordinate(star[3], star[4], epoch=int(star[5]))

                # id_object, name_object: str, alternative_name: str, coordinates: Coordinate, magnitude: float, constellation: str, tess_sectors: str
                # , type_object: str, note_one: str, note_two: str, note_three: str, b_v: str, j_k: str, ucac4: str, usnob1: str, gaia: str, vsx: str,
                # asassn: str, tess: str, comp0: int, comp1: int, comp2: int, comp3: int, comp4: int, comp5: int,
                # comp6: int, comp7: int, comp8: int, comp9: int, chk1: int, reserve1, reserve2, reserve3, reserve4,
                # reserve5, user_list = [], place_list = [], instrument_list = [], variability = True

                new_star = Star(str(star[0]), str(star[1]), str(star[2]), new_coor,
                                float(star[6]), str(star[7]), str(star[8]), str(star[9]),
                                str(star[10]), str(star[11]), str(star[12]), str(star[13]),
                                str(star[14]), str(star[15]), str(star[16]), str(star[17]),
                                str(star[18]), str(star[19]), str(star[20]), int(star[21]),
                                int(star[22]), int(star[23]), int(star[24]), int(star[25]),
                                int(star[26]), int(star[27]), int(star[28]), int(star[29]),
                                int(star[30]), int(star[31]), star[32], star[33], star[34],
                                star[35], star[36], variability=bool(star[40]))
                self.database.stars.add_star(new_star)
            for variable in self.variables:
                # name: str, pair: str, variability_type: str, period: float, epoch: float, amplitude_p: float,
                # amplitude_s: float, d_eclipse_prim: float, d_eclipse_sec: float, d_minimum_prim: float,
                # d_minimum_sec: float, mag0: float, a_pri: float, d_pri: float, g_pri: float, c_pri: float,
                # a_sin1: float, a_sin2: float, a_sin3: float, apsidal_movement_correction: float, sec_phase: float,
                # a_sec: float, d_sec: float, g_sec: float, c_sec: float, a_cos1: float, a_cos2: float, a_cos3: float,
                # lc_offset: float, in_prediction: float
                new_variable = VariableStar(variable[0], variable[1], variable[2], float(variable[3]),
                                            float(variable[4]), float(variable[5]), float(variable[6]),
                                            float(variable[7]), float(variable[8]), float(variable[9]),
                                            float(variable[10]), float(variable[11]), float(variable[12]),
                                            float(variable[13]), float(variable[14]), float(variable[15]),
                                            float(variable[16]), float(variable[17]), float(variable[18]),
                                            float(variable[19]), float(variable[20]), float(variable[21]),
                                            float(variable[22]), float(variable[23]), float(variable[24]),
                                            float(variable[25]), float(variable[26]), float(variable[27]),
                                            float(variable[28]), int(variable[29]))
                self.database.variables.add_variable(new_variable)
            self.__delete_unusefull()
            self.info_text = "Stars HAVE BEEN IMPORTED into your database. New ID was set to each imported star. You " \
                             "can check all imported information in table. Then close the window.\n" + self.info_text
            self.export_information_text_edit.setText(self.info_text)
            self.__save_import_report()
            self.continue_button.setEnabled(False)
            QtWidgets.QApplication.processEvents()
            self.step_main_form.fill_table()



    def data_integrity(self):
        self.continue_button.setText("Continue")
        star_id_list = []
        comparison_in_imported_star_list = []
        for k, star in enumerate(self.stars):  # test data lenth and type
            if len(star) == 43 and star[1]:
                # str(star.id())0, star.name()1, star.alt_name()2, str(star.rektascenze())3,
                # str(star.declination())4, str(star.eq())5, str(star.mag())6, star.constellation()7,
                # star.tess_sectors()8, star.type()9, star.note1()10, star.note2()11, star.note3()12,
                # str(star.b_v())13, str(star.j_k())14, star.ucac4()15, star.usnob1()16, star.gaia()17,
                # star.vsx()18, star.asassn()19, star.tess()20, str(star.comp0())21, str(star.comp1())22,
                # str(star.comp2())23, str(star.comp3())24, str(star.comp4())25, str(star.comp5())26,
                # str(star.comp6())27, str(star.comp7())28, str(star.comp8())29, str(star.comp9())30,
                # str(star.chk1())31, ""32, ""33, ""34, ""35, ""36, ""37, ""38, ""39, str(star.variability())40, ""41, ""42
                try:
                    star[0] = int(star[0])
                    star[3] = float(star[3])
                    star[4] = float(star[4])
                    star[5] = int(star[5])
                except:
                    self.info_text = "Star {0}: ID or coordinates aren´t a number. " \
                                     "Star will not be imported\n".format(star[1]) + self.info_text
                    self.export_information_text_edit.setText(self.info_text)
                    self.__save_import_report()
                    self.__set_item_background("star", k, "all")
                    QtWidgets.QApplication.processEvents()
                    star[1] = ""
                if star[1]:
                    if star[3] >= 2 * pi or star[3] < 0 or star[4] <= pi / -2 or star[4] >= pi / 2 or not (star[5] in [1950, 1975, 2000]):
                        self.info_text = "Star {0}: Coordinates are out of range. Star will not be " \
                                         "imported\n".format(star[1]) + self.info_text
                        self.export_information_text_edit.setText(self.info_text)
                        self.__save_import_report()
                        self.__set_item_background("star", k, "all")
                        QtWidgets.QApplication.processEvents()
                        star[1] = ""
                if star[1]:
                    if star[40] == "True":
                        star[40] = True
                    elif star[40] == "False":
                        star[40] = False
                        comparison_in_imported_star_list.append(star[0])
                    else:
                        self.info_text = "Star {0}: Erroneous information indicating whether it is a variable or " \
                                         "comparison star. Star will not be imported\n".format(star[1]) \
                                         + self.info_text
                        self.export_information_text_edit.setText(self.info_text)
                        self.__save_import_report()
                        self.__set_item_background("star", k, "all")
                        QtWidgets.QApplication.processEvents()
                        star[1] = ""
                if star[1]:
                    for i in range(21, 32):
                        try:
                            if star[i]:
                                star[i] = int(star[i])
                            else:
                                star[i] = 0
                        except:
                            self.info_text = "Star {0}: the given ID of the {1} comparison star is not a number. " \
                                             "The information about the comparison star will be " \
                                             "removed".format(star[1], self.star_key[i]) + self.info_text
                            self.export_information_text_edit.setText(self.info_text)
                            self.__save_import_report()
                            self.__set_item_background("star", k, i)
                            QtWidgets.QApplication.processEvents()
                            star[i] = 0
                if star[1]:
                    if not (star[7] in self.const_abbrs):
                        object_coor = Coordinate(float(star[3]), float(star[4]), epoch=int(star[5]))
                        star[7] = object_coor.get_const()
                        self.info_text = "Star {0}: Unknown constellation abbreviation. Constellation will be filled" \
                                         "by coordinates: {1}\n".format(star[1], star[7]) + self.info_text
                        self.export_information_text_edit.setText(self.info_text)
                        self.__save_import_report()
                        self.__set_item_background("star", k, 7)
                        QtWidgets.QApplication.processEvents()
                    try:
                        star[6] = star[6].replace(" ", "")
                        if star[6]:
                            star[6] = float(star[6])
                        else:
                            star[6] = 0
                    except:
                        self.info_text = "Star {0}: Magnitude is not number. Magnitude will not be imported " \
                                         "imported\n".format(star[1]) + self.info_text
                        self.export_information_text_edit.setText(self.info_text)
                        self.__save_import_report()
                        self.__set_item_background("star", k, 6)
                        QtWidgets.QApplication.processEvents()
                        star[6] = 0
                    try:
                        star[13] = star[13].replace(" ", "")
                        if star[13]:
                            star[13] = float(star[13])
                    except:
                        self.info_text = "Star {0}: B-V is not number. B-V will not be imported " \
                                         "imported\n".format(star[1]) + self.info_text
                        self.export_information_text_edit.setText(self.info_text)
                        self.__save_import_report()
                        self.__set_item_background("star", k, 13)
                        QtWidgets.QApplication.processEvents()
                        star[13] = ""
                    try:
                        star[14] = star[14].replace(" ", "")
                        if star[14]:
                            star[14] = float(star[14])
                    except:
                        self.info_text = "Star {0}: J-K is not number. J-K will not be imported " \
                                         "imported\n".format(star[1]) + self.info_text
                        self.export_information_text_edit.setText(self.info_text)
                        self.__save_import_report()
                        self.__set_item_background("star", k, 14)
                        QtWidgets.QApplication.processEvents()
                        star[14] = ""
                    if not (star[9] in self.type_key_list):
                        self.info_text = "Star {0}: Type of object not in the list. It will be imported like " \
                                         "undefined star\n".format(star[1]) + self.info_text
                        self.export_information_text_edit.setText(self.info_text)
                        self.__save_import_report()
                        self.__set_item_background("star", k, 9)
                        QtWidgets.QApplication.processEvents()
                        star[9] = ""
                    star_id_list.append(star[1])
            else:
                self.info_text = "Star {0}: data has an incorrect structure (missing or overflowing) or name missing" \
                                 "Star will not be imported\n".format(star[1]) + self.info_text
                self.export_information_text_edit.setText(self.info_text)
                self.__save_import_report()
                self.__set_item_background("star", k, "all")
                QtWidgets.QApplication.processEvents()
                star[1] = ""
        self.info_text = "The structural integrity of imported stars has been verified. Please check for any error " \
                         "messages\n" + self.info_text
        self.export_information_text_edit.setText(self.info_text)
        self.__save_import_report()
        QtWidgets.QApplication.processEvents()
        comparison_id_list = []
        for k, star in enumerate(self.comparisons):  # test data lenth and type
            if len(star) == 43 and star[1]:
                try:
                    star[0] = int(star[0])
                    star[3] = float(star[3])
                    star[4] = float(star[4])
                    star[5] = int(star[5])
                    star[21], star[22], star[23], star[24], star[25], star[26], star[27], star[28], \
                    star[29], star[30], star[31] = 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
                except:
                    self.info_text = "Comparison {0}: data has an incorrect structure (not number). " \
                                     "Comparison will not be imported\n".format(star[1]) + self.info_text
                    self.export_information_text_edit.setText(self.info_text)
                    self.__save_import_report()
                    self.__set_item_background("comp", k, "all")
                    QtWidgets.QApplication.processEvents()
                    star[1] = ""
                if star[1]:
                    if star[3] >= 2 * pi or star[3] < 0 or star[4] <= pi / -2 or star[4] >= pi / 2 \
                            or not (star[5] in [1950, 1975, 2000]):
                        self.info_text = "Comparison {0}: Coordinates are out of range. Star will not be " \
                                         "imported\n".format(star[1]) + self.info_text
                        self.export_information_text_edit.setText(self.info_text)
                        self.__save_import_report()
                        self.__set_item_background("comp", k, "all")
                        QtWidgets.QApplication.processEvents()
                        star[1] = ""
                star[40] = False
                if star[1]:
                    if not (star[7] in self.const_abbrs):
                        object_coor = Coordinate(float(star[3]), float(star[4]), epoch=int(star[5]))
                        star[7] = object_coor.get_const()
                        self.info_text = "Star {0}: Unknown constellation abbreviation. Constellation will be filled" \
                                         "by coordinates: {1}\n".format(star[1], star[7]) + self.info_text
                        self.export_information_text_edit.setText(self.info_text)
                        self.__save_import_report()
                        self.__set_item_background("comp", k, 7)
                        QtWidgets.QApplication.processEvents()
                    try:
                        star[6] = star[6].replace(" ", "")
                        if star[6]:
                            star[6] = float(star[6])
                        else:
                            star[6] = 0
                    except:
                        self.info_text = "Comparison {0}: Magnitude is not number. Magnitude will not be imported " \
                                         "imported\n".format(star[1]) + self.info_text
                        self.export_information_text_edit.setText(self.info_text)
                        self.__save_import_report()
                        self.__set_item_background("comp", k, 6)
                        QtWidgets.QApplication.processEvents()
                        star[6] = 0
                    try:
                        star[13] = star[13].replace(" ", "")
                        if star[13]:
                            star[13] = float(star[13])
                    except:
                        self.info_text = "Comparison {0}: B-V is not number. B-V will not be imported " \
                                         "imported\n".format(star[1]) + self.info_text
                        self.export_information_text_edit.setText(self.info_text)
                        self.__save_import_report()
                        self.__set_item_background("comp", k, 13)
                        QtWidgets.QApplication.processEvents()
                        star[13] = ""
                    try:
                        star[14] = star[14].replace(" ", "")
                        if star[14]:
                            star[14] = float(star[14])
                    except:
                        self.info_text = "Comparison {0}: J-K is not number. J-K will not be imported " \
                                         "imported\n".format(star[1]) + self.info_text
                        self.export_information_text_edit.setText(self.info_text)
                        self.__save_import_report()
                        self.__set_item_background("comp", k, 14)
                        QtWidgets.QApplication.processEvents()
                        star[14] = ""
                    star[9] = "CMP"
                    comparison_id_list.append(star[0])
            else:
                self.info_text = "Comparison {0}: data has an incorrect structure (missing or overflowing) " \
                                 "or name missing. Comparison will not be imported\n".format(star[1]) + self.info_text
                self.export_information_text_edit.setText(self.info_text)
                self.__save_import_report()
                self.__set_item_background("comp", k, "all")
                QtWidgets.QApplication.processEvents()
                star[1] = ""
        self.info_text = "The structural integrity of comparison stars has been verified. Please check for any error " \
                         "messages\n" + self.info_text
        self.export_information_text_edit.setText(self.info_text)
        self.__save_import_report()
        QtWidgets.QApplication.processEvents()
        for k, star in enumerate(self.variables):  # test data lenth and type
            if len(star) == 31 and star[0]:
                if star[0] in star_id_list and star[1] in ["A", "B", "C", "D", "E", "F"]:
                    for i in range(3, 29):
                        try:
                            star[i] = float(star[i])
                        except:
                            star[i] = 0
                            self.info_text = "Variable {0} pair {1} item {2}: data has an incorrect " \
                                             "structure (not number). A non-numeric entry will be replaced by " \
                                             "zero\n".format(star[0], star[1], self.variable_key[i]) + self.info_text
                            self.export_information_text_edit.setText(self.info_text)
                            self.__save_import_report()
                            self.__set_item_background("var", k, i)
                            QtWidgets.QApplication.processEvents()
                    if star[29] == "False":
                        star[29] = 0
                    else:
                        star[29] = 1
                else:
                    self.info_text = "Variable {0} pair {1}: There is no star for this variability or " \
                                     "variability is out of range\n".format(star[0], star[1]) \
                                     + self.info_text
                    self.__set_item_background("var", k, "all")
                    self.export_information_text_edit.setText(self.info_text)
                    self.__save_import_report()
                    QtWidgets.QApplication.processEvents()
                    star[0] = ""

            else:
                self.info_text = "Variable {0} pair {1}: data has an incorrect structure (missing or overflowing) " \
                                 "or name missing. Variability will not be imported\n".format(star[0], star[1]) \
                                 + self.info_text
                self.export_information_text_edit.setText(self.info_text)
                self.__save_import_report()
                self.__set_item_background("var", k, "all")
                QtWidgets.QApplication.processEvents()
                star[0] = ""

        self.info_text = "The structural integrity of star variability has been verified. Please check for any error " \
                         "messages\n" + self.info_text
        self.export_information_text_edit.setText(self.info_text)
        self.__save_import_report()
        QtWidgets.QApplication.processEvents()
        list_of_comparison_star_id = self.__check_comparison_star()
        if 0 in list_of_comparison_star_id:
            list_of_comparison_star_id.remove(0)
        for k, comparison in enumerate(self.comparisons):
            if comparison[1]:
                if comparison[0] in list_of_comparison_star_id:
                    list_of_comparison_star_id.remove(comparison[0])
                else:
                    self.info_text = "Comparison id:{0} is not a comparison star for any variable star. It will " \
                                     "not be imported\n".format(comparison[0]) + self.info_text
                    self.__set_item_background("comp", k, "all")
                    self.export_information_text_edit.setText(self.info_text)
                    self.__save_import_report()
                    QtWidgets.QApplication.processEvents()
                    comparison[1] = ""
        if list_of_comparison_star_id:
            list_txt = []
            for comp_id in list_of_comparison_star_id:
                list_txt.append(str(comp_id))
            self.info_text = "The following comparison stars were not found Id:{0} Their information will be removed " \
                             "for variable stars\n".format(",".join(list_txt)) + self.info_text
            self.export_information_text_edit.setText(self.info_text)
            self.__save_import_report()
            QtWidgets.QApplication.processEvents()
            for k, star in enumerate(self.stars):
                for i in range(21, 32):
                    if star[i] in list_of_comparison_star_id:
                        star[i] = 0
                        self.__set_item_background("star", k, i)
        self.info_text = "The structural integrity of the data between variable stars, comparison stars and " \
                         "individual variables was checked. After pressing the Continue key, the table will be " \
                         "adjusted according to the errors found.\n" + self.info_text
        self.export_information_text_edit.setText(self.info_text)
        self.__save_import_report()
        QtWidgets.QApplication.processEvents()
        self.choice_star_checkbox.setEnabled(False)
        self.star_without_comparison_checkbox.setEnabled(False)
        self.export_without_comparison_checkbox.setEnabled(False)

    def clear_window(self):
        self.info_text = ""
        self.choice_star_checkbox.setChecked(False)
        self.star_without_comparison_checkbox.setChecked(False)
        self.export_without_comparison_checkbox.setChecked(False)
        self.choice_star_checkbox.setEnabled(True)
        self.star_without_comparison_checkbox.setEnabled(True)
        self.continue_button.setEnabled(True)
        self.star_table_widget.clear()
        self.comparison_table_widget.clear()
        self.variability_table_widget.clear()
        self.export_information_text_edit.setText("")
        self.stars = []
        self.comparisons = []
        self.variables = []
        self.__status = 0

    def __set_item_background(self, table_id, row, column, r=255, g=0, b=0, alfa=60):
        try:
            if column == "all":
                if table_id == "star":
                    for i in range(0, 43):
                        self.star_table_widget.item(row, i).setBackground(QtGui.QBrush(QtGui.QColor(r, g, b, alfa)))
                elif table_id == "comp":
                    for i in range(0, 43):
                        self.comparison_table_widget.item(row, i).setBackground(QtGui.QBrush(QtGui.QColor(r, g, b, alfa)))
                elif table_id == "var":
                    for i in range(0, 31):
                        self.variability_table_widget.item(row, i).setBackground(QtGui.QBrush(QtGui.QColor(r, g, b, alfa)))
                else:
                    pass
            else:
                if table_id == "star":
                    self.star_table_widget.item(row, column).setBackground(QtGui.QBrush(QtGui.QColor(r, g, b, alfa)))
                elif table_id == "comp":
                    self.comparison_table_widget.item(row, column).setBackground(QtGui.QBrush(QtGui.QColor(r, g, b, alfa)))
                elif table_id == "var":
                    self.variability_table_widget.item(row, column).setBackground(QtGui.QBrush(QtGui.QColor(r, g, b, alfa)))
                else:
                    pass
        except:
            pass


    def fill_stars(self, table_key, stars, variability):
        self.star_key = table_key
        if variability:
            table_widget = self.star_table_widget
            self.stars = stars
        else:
            table_widget = self.comparison_table_widget
            self.comparisons = stars
        table_widget.setRowCount(len(stars))
        table_widget.setColumnCount(len(table_key))
        table_widget.setHorizontalHeaderLabels(table_key)
        for i in range(len(stars)):
            for j in range(len(stars[0])):
                item = QtWidgets.QTableWidgetItem(str(stars[i][j]))
                item.setFlags(QtCore.Qt.ItemIsEnabled)
                if variability:
                    item.setFlags(QtCore.Qt.ItemIsSelectable)
                table_widget.setItem(i, j, item)
        table_widget.resizeColumnsToContents()
        if variability:
            self.info_text = "Imported stars have been filled\n" + self.info_text
        else:
            self.info_text = "Related comparison stars have been filled\n" + self.info_text
        self.export_information_text_edit.setText(self.info_text)
        self.__save_import_report()
        QtWidgets.QApplication.processEvents()

    def fill_variability(self, table_key, variability):
        self.variable_key = table_key
        self.variables = variability
        self.variability_table_widget.setRowCount(len(variability))
        self.variability_table_widget.setColumnCount(len(table_key))
        self.variability_table_widget.setHorizontalHeaderLabels(table_key)
        for i in range(len(variability)):
            for j in range(len(variability[0])):
                item = QtWidgets.QTableWidgetItem(str(variability[i][j]))
                item.setFlags(QtCore.Qt.ItemIsEnabled)
                self.variability_table_widget.setItem(i, j, item)
        self.variability_table_widget.resizeColumnsToContents()
        self.info_text = "Variability for imported stars has been filled\n" + self.info_text
        self.export_information_text_edit.setText(self.info_text)
        self.__save_import_report()
        QtWidgets.QApplication.processEvents()

    def choice_star_checkbox_was_checked(self):
        row = self.star_table_widget.currentRow()
        if row > -1:
            if self.choice_star_checkbox.isChecked():
                self.stars[row][41] = "discarded"
                self.__set_item_background("star", row, "all")
                self.star_without_comparison_checkbox.setEnabled(False)
                self.star_table_widget.setItem(row, 41, QtWidgets.QTableWidgetItem("discarded"))
                self.info_text = "The star {0} has been discarded from export file\n".format(self.stars[row][1]) + self.info_text
                self.export_information_text_edit.setText(self.info_text)
                self.__save_import_report()
                for i, variability in enumerate(self.variables):
                    if variability[0] == self.stars[row][1]:
                        variability[30] = "discarded"
                        self.variability_table_widget.setItem(i, 30, QtWidgets.QTableWidgetItem("discarded"))
                        self.info_text = "The star {0} variability {1} has been discarded from export file\n".format(
                            variability[0], variability[1]) + self.info_text
                        self.export_information_text_edit.setText(self.info_text)
                        self.__save_import_report()
                        self.__set_item_background("var", i, "all")
            else:
                self.stars[row][41] = ""
                self.__set_item_background("star", row, "all", r=0, alfa=0)
                self.star_table_widget.setItem(row, 41, QtWidgets.QTableWidgetItem(""))
                self.star_without_comparison_checkbox.setEnabled(True)
                self.info_text = "The star {0} has been reinstated to the export file\n".format(self.stars[row][1]) + self.info_text
                self.export_information_text_edit.setText(self.info_text)
                self.__save_import_report()
                for i, variability in enumerate(self.variables):
                    if variability[0] == self.stars[row][1]:
                        variability[30] = ""
                        self.variability_table_widget.setItem(i, 30, QtWidgets.QTableWidgetItem(""))
                        self.info_text = "The star {0} variability {1} has been reinstated to the export file\n".format(
                            variability[0], variability[1]) + self.info_text
                        self.export_information_text_edit.setText(self.info_text)
                        self.__save_import_report()
                        self.__set_item_background("var", i, "all", r=0, alfa=0)

            comparison_id_list = self.__check_comparison_star()
            for k, comparison in enumerate(self.comparisons):
                if comparison[0] in comparison_id_list:
                    if comparison[41] == "discarded":
                        comparison[41] = ""
                        self.comparison_table_widget.setItem(row, 41, QtWidgets.QTableWidgetItem(""))
                        self.info_text = "The comparison star {0} id: {1} has been reinstated to export file\n".format(
                            comparison[1], comparison[0]) + self.info_text
                        self.export_information_text_edit.setText(self.info_text)
                        self.__save_import_report()
                        if not self.export_without_comparison_checkbox.isChecked():
                            self.__set_item_background("comp", k, "all", r=0, alfa=0)
                else:
                    if comparison[41] == "":
                        comparison[41] = "discarded"
                        self.comparison_table_widget.setItem(row, 41, QtWidgets.QTableWidgetItem("discarded"))
                        self.info_text = "The comparison star {0} id: {1} has been discarded from export file\n".format(
                            comparison[1], comparison[0]) + self.info_text
                        self.export_information_text_edit.setText(self.info_text)
                        self.__save_import_report()
                        self.__set_item_background("comp", k, "all")
        else:
            self.info_text = "No star is marked, it cannot be discarded\n" + self.info_text
            self.export_information_text_edit.setText(self.info_text)
            self.__save_import_report()
            self.choice_star_checkbox.setChecked(False)

    def __star_was_changed(self):
        try:
            row = self.star_table_widget.currentRow()
            if row > -1:
                if self.stars[row][41] == "":
                    self.star_without_comparison_checkbox.setEnabled(True)
                    self.choice_star_checkbox.setChecked(False)
                else:
                    self.star_without_comparison_checkbox.setEnabled(False)
                    self.choice_star_checkbox.setChecked(True)
                if self.stars[row][42] == "":
                    self.choice_star_checkbox.setEnabled(True)
                    self.star_without_comparison_checkbox.setChecked(False)
                else:
                    self.choice_star_checkbox.setEnabled(False)
                    self.star_without_comparison_checkbox.setChecked(True)
            else:
                self.choice_star_checkbox.setChecked(False)
                self.star_without_comparison_checkbox.setChecked(False)
                self.choice_star_checkbox.setEnabled(True)
                self.star_without_comparison_checkbox.setEnabled(True)
        except:
            self.choice_star_checkbox.setChecked(False)
            self.star_without_comparison_checkbox.setChecked(False)
            self.choice_star_checkbox.setEnabled(False)
            self.star_without_comparison_checkbox.setEnabled(False)

    def __with_comparison_was_clicked(self):
        row = self.star_table_widget.currentRow()
        if row > -1:
            if self.star_without_comparison_checkbox.isChecked():
                self.choice_star_checkbox.setEnabled(False)
                self.stars[row][42] = "discarded"
                self.star_table_widget.setItem(row, 42, QtWidgets.QTableWidgetItem("discarded"))
                self.info_text = "The star {0} will be exported without comparison star\n".format(
                    self.stars[row][1]) + self.info_text
                self.export_information_text_edit.setText(self.info_text)
                self.__save_import_report()
            else:
                self.choice_star_checkbox.setEnabled(True)
                self.stars[row][42] = ""
                self.star_table_widget.setItem(row, 42, QtWidgets.QTableWidgetItem(""))
                self.info_text = "The star {0} will be exported with comparison star\n".format(
                    self.stars[row][1]) + self.info_text
                self.export_information_text_edit.setText(self.info_text)
                self.__save_import_report()

            comparison_id_list = self.__check_comparison_star()
            for k, comparison in enumerate(self.comparisons):
                if comparison[0] in comparison_id_list:
                    if comparison[41] == "discarded":
                        comparison[41] = ""
                        self.comparison_table_widget.setItem(row, 41, QtWidgets.QTableWidgetItem(""))
                        self.info_text = "The comparison star {0} id: {1} has been reinstated to export file\n".format(
                            comparison[1], comparison[0]) + self.info_text
                        self.export_information_text_edit.setText(self.info_text)
                        self.__save_import_report()
                        if not self.export_without_comparison_checkbox.isChecked():
                            self.__set_item_background("comp", k, "all", r=0, alfa=0)
                else:
                    if comparison[41] == "":
                        comparison[41] = "discarded"
                        self.comparison_table_widget.setItem(row, 41, QtWidgets.QTableWidgetItem("discarded"))
                        self.info_text = "The comparison star {0} id: {1} has been discarded from export file\n".format(
                            comparison[1], comparison[0]) + self.info_text
                        self.export_information_text_edit.setText(self.info_text)
                        self.__save_import_report()
                        self.__set_item_background("comp", k, "all")
        else:
            self.info_text = "No star is marked, it cannot be discarded\n" + self.info_text
            self.export_information_text_edit.setText(self.info_text)
            self.__save_import_report()
            self.star_without_comparison_checkbox.setChecked(False)

    def __export_without_comparison_was_clicked(self):
        if self.export_without_comparison_checkbox.isChecked():
            for i in range(len(self.comparisons)):
                self.__set_item_background("comp", i, "all")
            self.info_text = "Information about comparison stars will be deletes." \
                             "All comparison stars have been discarded from export file\n" + self.info_text
            self.export_information_text_edit.setText(self.info_text)
            self.__save_import_report()
        else:
            for i in range(len(self.comparisons)):
                if self.comparisons[i][41] == "":
                    self.__set_item_background("comp", i, "all", r=0, alfa=0)
            self.info_text = "All eligible comparison stars have been added\n" + self.info_text
            self.export_information_text_edit.setText(self.info_text)
            self.__save_import_report()


    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        self.clear_window()

    def close_window(self):
        self.close()

    def __check_comparison_star(self):
        # str(star.id())0, star.name()1, star.alt_name()2, str(star.rektascenze())3,
        # str(star.declination())4, str(star.eq())5, str(star.mag())6, star.constellation()7,
        # star.tess_sectors()8, star.type()9, star.note1()10, star.note2()11, star.note3()12,
        # str(star.b_v())13, str(star.j_k())14, star.ucac4()15, star.usnob1()16, star.gaia()17,
        # star.vsx()18, star.asassn()19, star.tess()20, str(star.comp0())21, str(star.comp1())22,
        # str(star.comp2())23, str(star.comp3())24, str(star.comp4())25, str(star.comp5())26,
        # str(star.comp6())27, str(star.comp7())28, str(star.comp8())29, str(star.comp9())30,
        # str(star.chk1())31, ""32, ""33, ""34, ""35, ""36, ""37, ""38, ""39, str(star.variability())40, ""41, ""42

        comparison_star_in_stars_id = []
        for star in self.stars:
            if str(star[40]) == "False" and not star[41] and star[1]:
                comparison_star_in_stars_id.append(star[0])
        missing_comparison_star_id = []
        for star in self.stars:
            if not star[41] and not star[42] and star[1]:
                if not star[21] in comparison_star_in_stars_id and not star[21] in missing_comparison_star_id:
                    missing_comparison_star_id.append(star[21])
                if not star[22] in comparison_star_in_stars_id and not star[22] in missing_comparison_star_id:
                    missing_comparison_star_id.append(star[22])
                if not star[23] in comparison_star_in_stars_id and not star[23] in missing_comparison_star_id:
                    missing_comparison_star_id.append(star[23])
                if not star[24] in comparison_star_in_stars_id and not star[24] in missing_comparison_star_id:
                    missing_comparison_star_id.append(star[24])
                if not star[25] in comparison_star_in_stars_id and not star[25] in missing_comparison_star_id:
                    missing_comparison_star_id.append(star[25])
                if not star[26] in comparison_star_in_stars_id and not star[26] in missing_comparison_star_id:
                    missing_comparison_star_id.append(star[26])
                if not star[27] in comparison_star_in_stars_id and not star[27] in missing_comparison_star_id:
                    missing_comparison_star_id.append(star[27])
                if not star[28] in comparison_star_in_stars_id and not star[28] in missing_comparison_star_id:
                    missing_comparison_star_id.append(star[28])
                if not star[29] in comparison_star_in_stars_id and not star[29] in missing_comparison_star_id:
                    missing_comparison_star_id.append(star[29])
                if not star[30] in comparison_star_in_stars_id and not star[30] in missing_comparison_star_id:
                    missing_comparison_star_id.append(star[30])
                if not star[31] in comparison_star_in_stars_id and not star[31] in missing_comparison_star_id:
                    missing_comparison_star_id.append(star[31])
        return missing_comparison_star_id

    def __save_import_report(self):
        path_data = os.path.join(os.getenv("APPDATA"), "Step")
        try:
            if not os.path.exists(path_data):
                os.mkdir(path_data)
        except:
            mistake = Popup("Saving error",
                            "Failed to create folder\n{0}\nPlease check your permissions.".format(path_data),
                            buttons="EXIT,Try Again".split(","))
            if mistake.do() == 1:
                self.__save_import_report()
            else:
                return
        try:
            with open(os.path.join(path_data, "import_report.csv"), "w", encoding="utf-8") as f:
                f.write(self.info_text)
        except:
            mistake = Popup("Import report saving error", "Failed to create file import_report.csv. Please check your "
                                                          "permissions.", buttons="EXIT,Try Again".split(","))
            if mistake.do() == 1:
                self.__save_import_report()
            else:
                return
