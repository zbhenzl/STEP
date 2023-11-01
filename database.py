from csv import *
from coordinate import Coordinate
from object import Star
from time_period import *
from stars import *
from user import *
from instrument import *
from variables import *
from observer import *
from observations import *
from datetime import *
from prediction_form_2 import *
import os
import shutil


def check_input(string, digits=True, capital_letters=True, lower_case_letters=True, space=True,
                special_characters=False, semicolon=False, comma=False, plus_minus=False, dot_sign=False):
    permitted_characters = []
    if digits:
        permitted_characters = permitted_characters + ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
    if capital_letters:
        permitted_characters = permitted_characters + ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L",
                                                       "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X",
                                                       "Y", "Z"]
    if lower_case_letters:
        permitted_characters = permitted_characters + ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l",
                                                       "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x",
                                                       "y", "z"]
    if space:
        permitted_characters = permitted_characters + [" "]
    if semicolon:
        permitted_characters = permitted_characters + [";"]
    if comma:
        permitted_characters = permitted_characters + [","]
    if dot_sign:
        permitted_characters = permitted_characters + ["."]
    if plus_minus:
        permitted_characters = permitted_characters + ["+", "-"]
    if special_characters:
        permitted_characters = permitted_characters + ["/", "{", "}", "[", "]", "|", "<", ">", "%", "_", "'"]
    for one_sign in string:
        if one_sign not in permitted_characters:
            return False
    return True


class DataQuadruple:
    def __init__(self):
        self.__path = os.path.join(os.getenv("APPDATA"), "Step")
        self.__database_dict = {"stars": "stars", "users": "users", "places": "observation_places",
                                "instruments": "instruments", "horizons": "horizons", "variable": "variable",
                                "log": "observation_log", "important_prediction": "prediction"}
        self.__file_list = ["stars.csv", "users.csv", "observation_places.csv", "instruments.csv", "horizons.csv",
                            "variable.csv", "setup.csv", "observation_log.csv", "prediction.csv"]
        self.__backuplist = ["backup3", "backup2", "backup1", ""]
        self.__delimiter = ";"
        self.prediction_select_column_setup = "1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1"
        self.prediction_sort_column_setup = "Name"
        self.prediction_visibility_setup = "1,1,0"
        self.prediction_lightcurve_setup = "1,1,1,1,1,1"
        self.object_sort_by_setup = "0"
        self.object_filtered_by_setup = "1,0,0,0"
        self.variability_type = ["", "EA", "EB", "EW", "DSCT", "T", "Puls", "ROT", "DCEP", "VAR"]
        self.const_abbrs = ["", "And", "Ant", "Aps", "Aql", "Aqr", "Ara", "Ari", "Aur", "Boo", "Cae", "Cam", "Cap",
                            "Car", "Cas", "Cen", "Cep", "Cet", "Cha", "Cir", "CMa", "CMi", "Cnc", "Col", "Com", "CrA",
                            "CrB", "Crt", "Cru", "Crv", "CVn", "Cyg", "Del", "Dor", "Dra", "Equ", "Eri", "For", "Gem",
                            "Gru", "Her", "Hor", "Hya", "Hyi", "Ind", "Lac", "Leo", "Lep", "Lib", "LMi", "Lup", "Lyn",
                            "Lyr", "Men", "Mic", "Mon", "Mus", "Nor", "Oct", "Oph", "Ori", "Pav", "Peg", "Per", "Phe",
                            "Pic", "PsA", "Psc", "Pup", "Pyx", "Ret", "Scl", "Sco", "Sct", "Ser", "Sex", "Sge", "Sgr",
                            "Tau", "Tel", "TrA", "Tri", "Tuc", "UMa", "UMi", "Vel", "Vir", "Vol", "Vul"]
        self.possible_epoch = ["2000", "1975", "1950", "now"]

        self.type_dictionary = {"": "Undefined star", "Q": "double eclipsing quadruple", "T": "eclipsing triple",
                                "S": "triple eclipsing sixtuple", "E": "eclipsing binary", "P": "pulsating variable",
                                "R": "Rotation Variable", "Ep": "Exoplanet", "EEA": "Eccentric algolide",
                                "CMP": "Comparison star"}
        self.type_list = list(self.type_dictionary.values())
        self.type_key_list = list(self.type_dictionary.keys())
        self.__next_user = 1
        self.__next_place = 1
        self.__next_instrument = 1
        self.__next_star = 1


    def change_path_data(self, new_path):
        self.__path_data = new_path

    def change_next_user(self, new):
        self.__next_user = new

    def change_next_place(self, new):
        self.__next_place = new

    def change_next_instrument(self, new):
        self.__next_instrument = new

    def next_user(self):
        return self.__next_user

    def next_place(self):
        return self.__next_place

    def next_instrument(self):
        return self.__next_instrument


    def setup(self):
        if os.path.exists(os.path.join(os.getenv("APPDATA"), "Step", "setup.csv")):
            self.__setup = self.__open_table(os.path.join(os.getenv("APPDATA"), "Step", "setup.csv"))
        else:
            self.__setup = ""
        user_setup = 0
        place_setup = 0
        time_delta = 1
        instrument_setup = 0
        instrument_table = self.return_table("instruments")
        places_table = self.return_table("places")
        users_table = self.return_table("users")
        horizons_table = self.return_table("horizons")
        observation_logs = self.return_table("log")
        important_predictions = self.return_table("important_prediction")

        self.instruments = Instruments(instrument_table[0], instrument_table[1])
        self.places = Observers(places_table[0], places_table[1])
        self.users = Users(users_table[0], users_table[1])
        self.horizons = AllHorizons(horizons_table[0], horizons_table[1])
        self.observation_logs = ObservationLogs([], observation_logs[1])
        observation_log_list = []
        for row in observation_logs[0]:
            log = ObservationLog(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9],
                                 row[10], row[11], row[12], row[13], row[14], row[15], row[16], row[17], row[18],
                                 row[19], row[20], row[21], row[22], row[23], row[24], row[25])
            observation_log_list.append(log)
        self.observation_logs.add_logs(observation_log_list)
        important_predictions_list = []
        for row in important_predictions[0]:
            prediction = ImportantPrediction(row[0], row[1], row[2], row[3], row[4], row[5])
            important_predictions_list.append(prediction)
        self.important_predictions = ImportantPredictions(important_predictions_list)


        self.actual_variable = VariableStar("", "", "VAR", 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,  0, 0,
                                            0, 0, 0, 0, 0, 0, 0)
        self.user = User(0, "add_user")
        self.instrument = Instrument(0, 0, "Add telescope", 0, 0, "mount", "camera", 0, 0, 0, 0, "No")
        self.horizon = Horizon(0, [0, 180], [0, 0])
        self.place = Observer(0, "add_place", 0, 0, 0, 0, min_sunset=0, horizon=self.horizon, minimum_object_latitude=0)
        self.filtered_stars = Stars([], [])
        self.sun = Sun()
        self.moon = Moon()
        self.variables = self.open_variable()


        if self.__setup:
            for parameter in self.__setup:
                if parameter[0] == "user":
                    user_setup = parameter[1]
                elif parameter[0] == "place":
                    place_setup = parameter[1]
                elif parameter[0] == "time":
                    try:
                        time_delta = float(parameter[1])
                    except:
                        time_delta = 1
                elif parameter[0] == "instrument":
                    instrument_setup = parameter[1]
                elif parameter[0] == "next_user":
                    self.change_next_user(int(parameter[1]))
                elif parameter[0] == "next_place":
                    self.change_next_place(int(parameter[1]))
                elif parameter[0] == "next_instrument":
                    self.change_next_instrument(int(parameter[1]))
                elif parameter[0] == "next_star":
                    self.change_next_star(int(parameter[1]))
                else:
                    pass
            if self.users.users():
                if user_setup:
                    self.user.edit_all("id", user_setup, self.users)
                    if self.places.observers():
                        if place_setup:
                            self.place.edit_all("id", place_setup, self.places, self.horizons)
                    if self.instruments.instruments():
                        if instrument_setup:
                            self.instrument.edit_all("id", instrument_setup, self.instruments)
                else:
                    self.user.edit_all("id", self.users.users()[0][0], self.users)


        jd_start: float = date_to_jd(datetime.now(timezone.utc))
        jd_end: float = date_to_jd(datetime.now(timezone.utc) + timedelta(time_delta))
        self.time_period = TimePeriod(jd_start, jd_end)
        self.open_stars()


    def change_next_star(self, new_value):
        if self.__next_star < new_value:
            self.__next_star = new_value


    def __open_table(self, table):

        with open(table, "r", encoding="utf-8") as data:
            rows = reader(data, delimiter=self.__delimiter)
            self.__table = [row for row in rows]
        return self.__table

    def return_table(self, database):
        imported_table = []
        imported_keys = []
        if database in self.__database_dict:
            file_path = self.__path + "\\" + self.__database_dict[database] + ".csv"
            if os.path.exists(file_path):
                imported_table = self.__open_table(file_path)
                imported_keys: list = imported_table.pop(0)
            else:
                if database == "users":
                    return [[], ["id", "name", "authorizations", "prediction_select_column_setup",
                                 "prediction_sort_column_setup", "prediction_visibility_setup",
                                 "prediction_lightcurve_setup", "object_filtered_by_setup",
                                 "coordinate_setup", "object_sort_by_setup", "time_extension_setup",
                                 "texts_filter_setup_name_key1", "texts_filter_setup_name_key2",
                                 "texts_filter_setup_type_key1", "texts_filter_setup_type_key",
                                 "texts_filter_setup_type_key", "texts_filter_setup_type_key4",
                                 "texts_filter_setup_mag_start", "texts_filter_setup_mag_end",
                                 "texts_filter_setup_note_key1", "texts_filter_setup_note_key2",
                                 "texts_filter_setup_note_key3", "photometry_setup", "silicups_file_path, model_path"]]
                elif database == "places":
                    return [[], ["id", "name", "user_id", "horizon_id", "instrument_id", "latitude", "longitude",
                                 "min_h", "min_sunset"]]
                elif database == "instruments":
                    return [[], ["id", "observer_id", "telescope", "D", "f", "mount", "camera", "sensor_w", "sensor_h",
                                 "pixel_w", "pixel_h", "filter_set"]]
                elif database == "horizons":
                    return [[], ["id"]]
                elif database == "stars":
                    return [[], ["ID", "name", "Alternativ name", "Rektascenze", "Declination", "eq", "mag",
                                 "Constitution", "sectors_TESS", "type", "Note1", "Note2", "Note3", "B_V", "J_K",
                                 "UCAC4", "USBOB1", "GAIA", "VSX", "ASASSN", "TESS", "Comp0", "Comp1", "Comp2",
                                 "Comp3", "Comp4", "Comp5", "Comp6", "Comp7", "Comp8", "Comp9", "Chk1", "Reserve1",
                                 "Reserve2", "Reserve3", "Reserve4", "Reserve5", "User_list", "Place_list",
                                 "Instrument_list", "Variability"]]
                elif database == "variable":
                    return [[], ["name", "pair", "type", "period", "epoch", "Amp (P)", "Amp (s)", "D(prim)", "D(sec)",
                                 "d(prim)", "d(sec)", "mag0", "a_pri", "d_pri", "g_pri", "c_pri", "a_sin1", "a_sin2",
                                 "a_sin3", "apsid correction", "sec_phase", "a_sec", "d_sec", "g_sec", "c_sec",
                                 "a_cos1", "a_cos2", "a_cos3", "ofsetA", "in_prediction"]]
                elif database == "log":
                    return [[], ["user", "date", "name", "pair", "p_s", "type", "const", "telescope", "mount", "camera",
                                 "filter", "bin", "exposure", "processed", "place", "place_latitude", "place_longitude",
                                 "moon_distance", "moon", "h_at_min", "weather",  "note1", "note2", "note3", "note4",
                                 "note5"]]
                elif database == "important_prediction":
                    return [[], ["user_name", "place_name", "instrument_id", "star_name", "variable_pair",
                                 "minimum_jd"]]
                else:
                    pass
            if database == "stars":
                imported_keys = ["ID", "name", "Alternativ name", "Rektascenze", "Declination", "eq", "mag",
                                 "Constitution", "sectors_TESS", "type", "Note1", "Note2", "Note3", "B_V", "J_K",
                                 "UCAC4", "USBOB1", "GAIA", "VSX", "ASASSN", "TESS", "Comp0", "Comp1", "Comp2",
                                 "Comp3", "Comp4", "Comp5", "Comp6", "Comp7", "Comp8", "Comp9", "Chk1", "Reserve1",
                                 "Reserve2", "Reserve3", "Reserve4", "Reserve5", "User_list", "Place_list",
                                 "Instrument_list", "Variability"]

        return [imported_table, imported_keys]

    def increase_next_star(self):
        self.__next_star += 1

    def open_stars(self):
        all_stars = []
        table_item = self.return_table("stars")
        for star in table_item[0]:
            if star[40] == "VAR":
                variability = True
            else:
                variability = False
            if star[6] == "":
                star[6] = float(0)
            else:
                star[6] = float(star[6])
            for x in range(21, 32):
                if star[x] == "":
                    star[x] = 0
                else:
                    star[x] = int(star[x])
            if int(star[0]) >= self.next_star():
                self.change_next_star(int(star[0]) + 1)
            object_coor = Coordinate(float(star[3]), float(star[4]), epoch=int(star[5]))
            if not star[7]:
                star[7] = object_coor.get_const()

            star_object = Star(star[0], star[1], star[2], object_coor, star[6], star[7], star[8], star[9],
                               star[10], star[11], star[12], star[13], star[14], star[15], star[16],
                               star[17], star[18], star[19], (star[20]), int(star[21]), int(star[22]),
                               int(star[23]), int(star[24]), int(star[25]), int(star[26]), int(star[27]),
                               int(star[28]), int(star[29]), int(star[30]), int(star[31]), star[32], star[33],
                               star[34], star[35], star[36], user_list=star[37], place_list=star[38],
                               instrument_list=star[39], variability=variability)
            all_stars.append(star_object)
        self.stars = Stars(all_stars, table_item[1])

    def open_variable(self):
        all_variable = []
        table_item = self.return_table("variable")
        variable_key = table_item[1]
        variable_stars = table_item[0]

        for variable in variable_stars:
            for i in range(3, 29):
                if variable[i] == "":
                    variable[i] = 0
                else:
                    try:
                        variable[i] = float(variable[i])
                    except:
                        variable[i] = 0
            variable_object = VariableStar(variable[0], variable[1], variable[2], float(variable[3]),
                                           float(variable[4]), float(variable[5]), float(variable[6]),
                                           float(variable[7]), float(variable[8]), float(variable[9]),
                                           float(variable[10]), float(variable[11]), float(variable[12]),
                                           float(variable[13]), float(variable[14]), float(variable[15]),
                                           float(variable[16]), float(variable[17]), float(variable[18]),
                                           float(variable[19]), float(variable[20]), float(variable[21]),
                                           float(variable[22]), float(variable[23]), float(variable[24]),
                                           float(variable[25]), float(variable[26]), float(variable[27]),
                                           float(variable[28]),float(variable[29]))
            if not variable[2].strip() in self.variability_type:
                self.variability_type.append(variable[2].strip())

            all_variable.append(variable_object)
        return Variables(all_variable, variable_key)

    def next_star(self):
        return self.__next_star

    def return_list_by_key(self, list_key, database, filter_key=None, filter_value=None):
        if database == "users":
            table: list[list] = self.users.users()
            keys: list = self.users.users_key()
        elif database == "places":
            table: list[list] = self.places.observers()
            keys: list = self.places.observers_key()
        elif database == "instruments":
            table: list[list] = self.instruments.instruments()
            keys: list = self.instruments.instruments_key()
        else:
            return []
        key_index: int = keys.index(list_key)
        if filter_key and filter_value:
            filter_index: int = keys.index(filter_key)
        list_by_key = []
        if table:
            for table_item in table:
                if filter_value and filter_key:
                    if table_item[filter_index] == str(filter_value):
                        list_by_key.append(table_item[key_index])
                else:
                    list_by_key.append(table_item[key_index])
            return list_by_key
        return list_by_key

    def save_database(self):
        try:
            self.__path_data = os.path.join(os.getenv("APPDATA"), "Step")
            if not os.path.exists(self.__path_data):
                os.mkdir(self.__path_data)
        except:
            mistake = Popup("Saving error",
                            "Failed to create folder\n{0}\nPlease check your permissions.".format(self.__path_data),
                            buttons="EXIT,Try Again".split(","))
            if mistake.do() == 1:
                self.save_database()
            else:
                return
        try:
            for i in range(len(self.__backuplist)-1):
                path_backup = os.path.join(self.__path_data, self.__backuplist[i])
                path_backup_from = os.path.join(self.__path_data, self.__backuplist[i+1])
                if not os.path.exists(path_backup):
                    os.mkdir(path_backup)
                for file in self.__file_list:
                    if os.path.exists(os.path.join(path_backup, file)):
                        os.remove(os.path.join(path_backup, file))
                    if os.path.exists(os.path.join(path_backup_from, file)):
                        shutil.copy(os.path.join(path_backup_from, file), os.path.join(path_backup, file))
        except:
            mistake = Popup("Saving error", "Failed to create buckup. Please check your permissions.")
            mistake.do()
            return
        try:
            with open(os.path.join(self.__path_data, "users.csv"), "w", encoding="utf-8") as f:
                key = self.users.users_key()
                radek = ";".join(key)
                f.write(radek + "\n")
                for u in self.users.users():
                    radek = ";".join(u)
                    f.write(radek + "\n")
        except:
            mistake = Popup("User saving error", "Failed to create file\n{0}\n{1}\nPlease check your permissions.".format(self.__path_data, "users"), buttons="EXIT,Try Again".split(","))
            if mistake.do() == 1:
                self.save_database()
            else:
                return
        try:
            with open(os.path.join(self.__path_data, "observation_places.csv"), "w", encoding="utf-8") as f:
                key = self.places.observers_key()
                radek = ";".join(key)
                f.write(radek+ "\n")
                for u in self.places.observers():
                    radek = ";".join(u)
                    f.write(radek + "\n")
        except:
            mistake = Popup("Place saving error", "Failed to create file\n{0}\n{1}\nPlease check your permissions.".format(self.__path_data, "observation_places"), buttons="EXIT,Try Again".split(","))
            if mistake.do() == 1:
                self.save_database()
            else:
                return
        try:
            with open(os.path.join(self.__path_data, "instruments.csv"), "w", encoding="utf-8") as f:
                key = self.instruments.instruments_key()
                radek = ";".join(key)
                f.write(radek+ "\n")
                for u in self.instruments.instruments():
                    radek = ";".join(u)
                    f.write(radek + "\n")
        except:
            mistake = Popup("Instrument saving error", "Failed to create file\n{0}\n{1}\nPlease check your permissions.".format(self.__path_data, "instruments"), buttons="EXIT,Try Again".split(","))
            if mistake.do() == 1:
                self.save_database()
            else:
                return
        try:
            with open(os.path.join(self.__path_data, "stars.csv"), "w", encoding="utf-8") as f:
                key = self.stars.key
                radek = ";".join(key)
                f.write(radek+ "\n")
                for u in self.stars.stars:
                    star_txt = u.star_to_txt()
                    radek = ";".join(star_txt)
                    f.write(radek + "\n")
        except:
            mistake = Popup("Star saving error", "Failed to create file\n{0}\n{1}\nPlease check your permissions.".format(self.__path_data, "stars"), buttons="EXIT,Try Again".split(","))
            if mistake.do() == 1:
                self.save_database()
            else:
                return
        try:
            with open(os.path.join(self.__path_data, "variable.csv"), "w", encoding="utf-8") as f:
                key = self.variables.key
                radek = ";".join(key)
                f.write(radek + "\n")
                for u in self.variables.variables:
                    variable_txt = u.variable_to_txt()
                    radek = ";".join(variable_txt)
                    f.write(radek + "\n")
        except:
            mistake = Popup("Pair saving error", "Failed to create file\n{0}\n{1}\nPlease check your permissions.".format(self.__path_data, "variable"), buttons="EXIT,Try Again".split(","))
            if mistake.do() == 1:
                self.save_database()
            else:
                return
        try:
            with open(os.path.join(self.__path_data, "horizons.csv"), "w", encoding="utf-8") as f:
                key = self.horizons.horizons_key()
                radek = ";".join(key)
                f.write(radek + "\n")
                for u in self.horizons.horizons():
                    radek = ";".join(u)
                    f.write(radek + "\n")
        except:
            mistake = Popup("Horizon saving error", "Failed to create file\n{0}\n{1}\nPlease check your permissions.".format(self.__path_data, "horizons"), buttons="EXIT,Try Again".split(","))
            if mistake.do() == 1:
                self.save_database()
            else:
                return
        try:
            with open(os.path.join(self.__path_data, "observation_log.csv"), "w", encoding="utf-8") as f:
                key = self.observation_logs.log_keys()
                radek = ";".join(key)
                f.write(radek + "\n")
                for i in range(0, self.observation_logs.total_number()):
                    radek = self.observation_logs.give_observation(i).to_text()
                    f.write(radek + "\n")
        except:
            mistake = Popup("Observations log saving error",
                            "Failed to create file\n{0}\n{1}\nPlease check your permissions.".format(self.__path_data,
                                                                                                     "observation_log"),
                            buttons="EXIT,Try Again".split(","))
            if mistake.do() == 1:
                self.save_database()
            else:
                return
        try:
            with open(os.path.join(self.__path_data, "prediction.csv"), "w", encoding="utf-8") as f:
                dbf_key = ["user_name", "place_name", "instrument_id", "star_name", "variable_pair", "minimum_jd"]
                radek = ";".join(dbf_key)
                f.write(radek + "\n")
                for i in range(self.important_predictions.total_number()):
                    radek = self.important_predictions.give_prediction(i).to_text()
                    radek1 = ";".join(radek)
                    f.write(radek1 + "\n")
        except:
            mistake = Popup("Important prediction saving error",
                            "Failed to create file\n{0}\n{1}\nPlease check your permissions.".format(self.__path_data,
                                                                                                     "prediction"),
                            buttons="EXIT,Try Again".split(","))
            if mistake.do() == 1:
                self.save_database()
            else:
                return




    def save_setup(self):
        setup_file = []
        if self.user.id != "add user":
            setup_file.append(["user", str(self.user.id)])
        if int(self.place.id) > 0:
            setup_file.append(["place", str(self.place.id)])
        setup_file.append(["time", str(self.time_period.jd_end() - self.time_period.jd_start())])
        if int(self.instrument.id) > 0:
            setup_file.append(["instrument", str(self.instrument.id)])
        setup_file.append(["next_user", str(self.next_user())])
        setup_file.append(["next_place", str(self.next_place())])
        setup_file.append(["next_instrument", str(self.next_instrument())])
        setup_file.append(["next_star", str(self.next_star())])
        try:
            with open(os.path.join(os.getenv("APPDATA"), "Step", "setup.csv"), "w", encoding="utf-8") as f:
                for line_u in setup_file:
                    radek = ";".join(line_u)
                    f.write(radek + "\n")
        except:
            mistake = Popup("Setup saving error", "Failed to create and save setup file", buttons="OK".split(","))
            mistake.do()


