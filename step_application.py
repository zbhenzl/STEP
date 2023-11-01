import sys
from step_main_form import *
from database import *
from time_aria_widget import *
from horizon_formular import *
from add_user_window import *
from add_place_window import *
from add_instrument_window import *
from stars import *
from lightcurve_form import *
from edit_object import *
from ucac4_window import *
from usno_window import *
from vsx_window import *
from gaia_window import *
from asas_window import *
from TESS_window import *
from tess_menu_window import *
from prediction_form_2 import *
from tess_photometry_edit_window import *
from observations import *
from known_variable_window import *


class StepApplication(QtWidgets.QApplication):

    def __init__(self):
        super(StepApplication, self).__init__(sys.argv)

        self.database = DataQuadruple()
        self.step_main_form = StepMainForm()
        self.calendar_add_widget = TimeAreaWindow()
        self.horizon_set_window = SetHorizonWindow()
        self.add_user_window = AddUserWindow()
        self.rename_user_window = RenameUserWindow()
        self.add_place_window = AddPlaceWindow()
        self.add_instrument_window = AddInstrumentWindow()
        self.time_aria_window = TimeAreaWindow()
        self.lightcurve_window = LightCurveWindow()
        self.object_edit_window = EditObjectWindow()
        self.object_import_window = ImportObjectWindow()
        self.ucac4_window = UCAC4Window()
        self.usno_window = USNOWindow()
        self.vsx_window = VSXWindow()
        self.gaia_window = GaiaWindow()
        self.asas_window = ASASWindow()
        self.tess_window = TESSWindow()
        self.tess_menu_window = TESSMenuWindow()
        self.tess_menu_window_setting = TESSMenuWindowSetting()
        self.tess_import = TessImport()
        self.prediction2 = PredictionTwo()
        self.tess_photometry_edit_window = TessPhotometryEditWindow()
        self.observation_log_window = ObservationLogsWindow()
        self.silicups_window = SilicupsFieldWindow()
        self.edit_place_window = EditPlaceWindow()
        self.edit_instrument_window = EditInstrumentWindow()
        self.export_window = ExportWindow()
        self.import_window = ImportWindow()
        self.photometry_star_list_window = TESSListWindow()
        self.known_variable_window = KnownVariableWindow()



    def build(self):
        self.database.setup()
        self.step_main_form.setup()
        self.calendar_add_widget.setup()
        self.horizon_set_window.setup()
        self.add_user_window.setup()
        self.add_place_window.setup()
        self.add_instrument_window.setup()
        self.time_aria_window.setup()
        self.prediction2.setup()
        self.lightcurve_window.setup()
        self.object_edit_window.setup()
        self.tess_import.setup()
        self.object_import_window.setup()
        self.ucac4_window.setup()
        self.usno_window.setup()
        self.vsx_window.setup()
        self.gaia_window.setup()
        self.asas_window.setup()
        self.tess_window.setup()
        self.tess_menu_window.setup()
        self.tess_photometry_edit_window.setup()
        self.tess_menu_window_setting.setup()
        self.observation_log_window.setup()
        self.silicups_window.setup()
        self.rename_user_window.setup()
        self.edit_place_window.setup()
        self.edit_instrument_window.setup()
        self.export_window.setup()
        self.import_window.setup()
        self.photometry_star_list_window.setup()
        self.known_variable_window.setup()

        sys.exit(self.exec())


root = StepApplication()
root.build()
