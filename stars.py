from object import Star
from observer import Observer
from step_main_form import *
from object import *
from observer import *
from time_period import *
from user import *
from instrument import *
from astropy.coordinates import angular_separation


class Stars:
    def __init__(self, stars, stars_key):
        self.__stars = stars
        self.__stars_key = stars_key

    @property
    def key(self):
        return self.__stars_key

    @property
    def stars(self):
        return self.__stars

    def filter(self, user_now: User, place_now: Observer, instrument_now: Instrument, name: str, alt_name: str,
               rec_start: float, rec_end: float, dec_start: float, dec_end: float, type1: str, type2: str, type3: str,
               type4: str, mag_max: float, mag_min: float, note1: str, note2: str, note_log_info: bool,
               by_variability=True, by_user=True, by_place=True, by_instrument=True, by_name=False, by_rec=False,
               by_dec=False, by_type=True, by_mag=True, by_note=True, by_constilation=True, constilation=""):
        sorted_stars = []
        type_list = []
        if type1 != "":
            type_list.append(type1)
        if type2 != "":
            type_list.append(type2)
        if type3 != "":
            type_list.append(type3)
        if type4 != "":
            type_list.append(type4)

        for star in self.__stars:
            note_all = star.note1() + star.note2() + star.note3()
            if by_variability and not star.variability():
                pass
            elif by_user and not user_now.name() in star.user_list():
                pass
            elif by_place and place_now.name not in star.place_list():
                pass
            elif by_instrument and instrument_now.id not in star.instrument_list():
                pass
            elif by_name and name not in star.name():
                pass
            elif by_name and alt_name not in star.alt_name():
                pass
            elif by_rec and not(rec_start < star.coordinate().rektascenze() < rec_end
                                or rec_end < rec_start < star.coordinate().rektascenze()
                                or star.coordinate().rektascenze() < rec_end < rec_start):
                pass
            elif by_dec and not dec_start < star.coordinate().deklinace() < dec_end:
                pass
            elif by_mag and not mag_max <= star.mag() <= mag_min:
                pass
            elif by_type and not((star.type() in type_list) or not type_list):
                pass
            elif by_note and not((not note1 and not note2)
                                 or (not note1 and note2 and note2 in note_all)
                                 or (not note2 and note1 and note1 in note_all)
                                 or (note1 and note2 and note_log_info and note1 in note_all and note2 in note_all)
                                 or (note1 and note2 and not note_log_info and (note1 in note_all or note2 in note_all)
                                     )):
                pass
            elif by_constilation and not star.constellation() == constilation:
                pass
            else:
                sorted_stars.append(star)
        return sorted_stars

    def sort_by(self, sort_by):
        for i in range(len(self.stars) - 1):
            for j in range(i+1, len(self.stars)):
                if sort_by == "Name":
                    if self.stars[i].name() > self.stars[j].name():
                        new_max = self.stars.pop(j)
                        self.stars.insert(i, new_max)
                if sort_by == "Alt_name":
                    if self.stars[i].alt_name() > self.stars[j].alt_name():
                        new_max = self.stars.pop(j)
                        self.stars.insert(i, new_max)
                if sort_by == "Rec":
                    if self.stars[i].rektascenze() > self.stars[j].rektascenze():
                        new_max = self.stars.pop(j)
                        self.stars.insert(i, new_max)
                if sort_by == "Dec":
                    if self.stars[i].declination() > self.stars[j].declination():
                        new_max = self.stars.pop(j)
                        self.stars.insert(i, new_max)
                if sort_by == "Type":
                    if self.stars[i].type() > self.stars[j].type():
                        new_max = self.stars.pop(j)
                        self.stars.insert(i, new_max)
                if sort_by == "Mag":
                    if self.stars[i].mag() > self.stars[j].mag():
                        new_max = self.stars.pop(j)
                        self.stars.insert(i, new_max)

    def add_star(self, star: Star):
        self.__stars.append(star)

    def delete_star(self, delete_star: Star):
        if delete_star.variability():
            from step_application import root
            variable_list = []
            for i, variable in enumerate(root.database.variables.variables):
                if variable.name() == delete_star.name():
                    variable_list.append(i)
            while variable_list:
                delete_index = variable_list.pop()
                del root.database.variables.variables[delete_index]
        for i, star in enumerate(self.__stars):
            if star.id() == delete_star.id():
                del self.__stars[i]
                return

    def change_stars_set(self, new_set):
        self.__stars = new_set

    def change_key_set(self, new_set):
        self.__stars_key = new_set

    def check_aperture(self, aperture):
        pass

    def star_index(self, name):
        for i, star in enumerate(self.__stars):
            if star.name() == name:
                return i

    def star_id_index(self, star_id):
        for i, star in enumerate(self.__stars):
            if int(star.id()) == int(star_id):
                return i

    def comperison_star_exist(self, id_star):
        try:
            id_star = int(id_star)
        except:
            return False
        for star in self.__stars:
            if int(star.id()) == id_star and not star.variability():
                return True
        return False

    def edit_star(self, new_star):
        for i, star in enumerate(self.__stars):
            if star.name() == new_star.name:
                self.__stars[i] = new_star
                return

    def edit_star_id(self, new_star):
        for i, star in enumerate(self.__stars):
            if star.name() == new_star.name:
                self.__stars[i] = new_star
                return

    def change_user_in_user_list(self, new_user, last_user):
        for star in self.__stars:
            if last_user in star.user_list():
                user_list = star.user_list()
                for i in range(len(user_list)):
                    if user_list[i] == last_user:
                        user_list[i] = new_user
                star.change_user_list(user_list)

    def change_place_in_place_list(self, new_place, last_place):
        for star in self.__stars:
            if last_place in star.place_list():
                place_list = star.place_list()
                for i in range(len(place_list)):
                    if place_list[i] == last_place:
                        place_list[i] = new_place
                star.change_place_list(place_list)


    # variables: Variables, sun: Sun, moon: Moon, observation_place: Observer, epoch: TimePeriod,
    def prediction(self, visibility_sun, visibility_horizon, visibility_moon, moon_max_phase=100, moon_min_distance=0):
        from step_application import root
        variables = root.database.variables
        user_name = root.database.user.name()
        sun = root.database.sun
        moon = root.database.moon
        observation_place = root.database.place
        place_name = observation_place.name
        epoch = root.database.time_period
        important_predictions = root.database.important_predictions
        important_predictions.delete_old_prediction(float(root.step_main_form.local_jd_now_label.text()))
        predictions = []
        for star in self.__stars:
            for variable in variables.variables:
                if star.name() == variable.name():
                    predicts = variable.prediction(star, sun, moon, observation_place, epoch.jd_start(),
                                                   epoch.jd_end(), visibility_sun, visibility_horizon, visibility_moon,
                                                   moon_max_phase=moon_max_phase, moon_min_distance=moon_min_distance)
                    if predicts:
                        for predict in predicts:
                            prediction = [str(star.id()), star.name(), variable.pair(), predict.minimum_p_s(),
                                          star.alt_name(), star.constellation(), star.type(),
                                          coordinate_to_text(star.rektascenze(), coordinate_format="hours",
                                                             delimiters=("h ", "' ", '"')),
                                          coordinate_to_text(star.declination(), coordinate_format="degree",
                                                             delimiters=("° ", "' ", '"')), str(star.mag()),
                                          star.ucac4(), star.usnob1()]
                            meridian = jd_to_date(star.meridian(predict.minimum_jd(), observation_place.longitude))
                            starrise = jd_to_date(star.sunrise_h(observation_place.minimum_h, predict.minimum_jd(),
                                                                 observation_place.longitude,
                                                                 observation_place.latitude))
                            starset = jd_to_date(star.sunset_h(observation_place.minimum_h, predict.minimum_jd(),
                                                               observation_place.longitude, observation_place.latitude))
                            if predict.minimum_type():
                                big_d_entry = jd_to_date(predict.minimum_jd() -
                                                         variable.d_minimum_prim()/48)
                                big_d_out = jd_to_date(predict.minimum_jd() +
                                                       variable.d_minimum_prim()/48)
                                d_entry = jd_to_date(predict.minimum_jd() -
                                                     variable.d_eclipse_prim()/48)
                                d_out = jd_to_date(predict.minimum_jd() -
                                                   variable.d_eclipse_prim()/48)
                                amp = variable.amplitude_p()
                            else:
                                big_d_entry = jd_to_date(predict.minimum_jd() -
                                                         variable.d_minimum_sec()/48)
                                big_d_out = jd_to_date(predict.minimum_jd() +
                                                       variable.d_minimum_sec()/48)
                                d_entry = jd_to_date(predict.minimum_jd() -
                                                     variable.d_eclipse_sec()/48)
                                d_out = jd_to_date(predict.minimum_jd() -
                                                   variable.d_eclipse_sec()/48)
                                amp = variable.amplitude_s()
                            prediction.append(meridian.strftime("%d.%m.%Y %H:%M"))
                            prediction.append(starrise.strftime("%d.%m.%Y %H:%M"))
                            prediction.append(starset.strftime("%d.%m.%Y %H:%M"))
                            prediction.append(big_d_entry.strftime("%d.%m.%Y %H:%M"))
                            prediction.append(big_d_out.strftime("%d.%m.%Y %H:%M"))
                            prediction.append(d_entry.strftime("%d.%m.%Y %H:%M"))
                            prediction.append(d_out.strftime("%d.%m.%Y %H:%M"))
                            minimum_jd = str(predict.minimum_jd())
                            prediction.append(minimum_jd)
                            prediction.append(jd_to_date(predict.minimum_jd()).strftime("%d.%m.%Y %H:%M"))
                            h_star = degrees(star.horizon_coordinates_h(predict.minimum_jd(),
                                                                        observation_place.longitude,
                                                                        observation_place.latitude))
                            prediction.append(str(ceil(h_star)))
                            moon_coor = moon.coordinates(predict.minimum_jd())
                            moon_rec = moon_coor[0]
                            moon_dec = moon_coor[1]
                            moon_h = moon.h(predict.minimum_jd(),
                                            observation_place.latitude,
                                            observation_place.longitude)
                            if moon_h > 0:
                                distance_num = angular_separation(star.coordinate().rektascenze(),
                                                                  star.coordinate().deklinace(),
                                                                  moon_rec, moon_dec)
                                distance = str(round(degrees(distance_num), 2))
                            else:
                                distance = ""
                            prediction.append(distance)
                            prediction.append(str(amp))
                            prediction.append(str(variable.sec_phase()))
                            prediction.append(str(variable.epoch()))
                            prediction.append(str(variable.period()))
                            prediction.append(star.note1())
                            prediction.append(star.note2())
                            prediction.append(star.note3())
                            prediction.append(str(variable.mag0()))
                            prediction.append(str(variable.a_pri()))
                            prediction.append(str(variable.d_pri()))
                            prediction.append(str(variable.g_pri()))
                            prediction.append(str(variable.c_pri()))
                            prediction.append(str(variable.a_sin1()))
                            prediction.append(str(variable.a_sin2()))
                            prediction.append(str(variable.a_sin3()))
                            prediction.append(str(variable.apsidal_movement_correction()))
                            prediction.append(str(variable.sec_phase()))
                            prediction.append(str(variable.a_sec()))
                            prediction.append(str(variable.d_sec()))
                            prediction.append(str(variable.g_sec()))
                            prediction.append(str(variable.c_sec()))
                            prediction.append(str(variable.a_cos1()))
                            prediction.append(str(variable.a_cos2()))
                            prediction.append(str(variable.a_cos3()))
                            prediction.append(str(variable.lc_offset()))
                            try:
                                prediction.append(float(star.mag()))
                            except:
                                prediction.append(0)
                            prediction.append(starrise)
                            prediction.append(starset)
                            prediction.append(big_d_entry)
                            prediction.append(big_d_out)
                            prediction.append(float(predict.minimum_jd()))
                            prediction.append(h_star)
                            if distance:
                                prediction.append(float(distance))
                            else:
                                prediction.append(181)
                            try:
                                prediction.append(float(amp))
                            except:
                                prediction.append(0)
                            prediction.append(float(variable.period()))
                            prediction.append(important_predictions.confirm_prediction(user_name,
                                                                                       place_name,
                                                                                       star.name(), minimum_jd))
                            predictions.append(prediction)

        return predictions

    def already_exist(self, new_name, new_rec, new_dec, aperture=0.00005, catalogue="", catalogue_id=""):
        near_stars = []
        catalogue_id_test = catalogue_id.replace(" ", "")
        if not catalogue_id_test:
            catalogue_id = ""
        for star in self.__stars:
            if new_name == star.name():
                return [[star.id()], "Name error:\nThis star name already exist in your database id:{0}".format(str(star.id()))]
            if fabs(star.coordinate().deklinace() - new_dec) < aperture:
                if fabs(star.coordinate().rektascenze() - new_rec) * cos(new_dec) < aperture:
                    near_stars.append(star.id())
                    near_stars.append(star.name())
            if catalogue == "UCAC4":
                if catalogue_id == star.ucac4() and catalogue_id:
                    return [[star.name()], "UCAC4 error:\nThis star cross id. "
                                           "already exist in your database id:{0}".format(str(star.id()))]
            elif catalogue == "USNO-B1.0":
                if catalogue_id == star.usnob1() and catalogue_id:
                    return [[star.name()], "USNO B1.0 error:\nThis star cross id. "
                                           "already exist in your database id:{0}".format(str(star.id()))]
            elif catalogue == "GAIA":
                if catalogue_id == star.gaia() and catalogue_id:
                    return [[star.name()], "GAIA error:\nThis star cross id. "
                                           "already exist in your database id:{0}".format(str(star.id()))]
            elif catalogue == "VSX":
                if catalogue_id == star.vsx() and catalogue_id:
                    return [[star.name()], "VSX error:\nThis star cross id. "
                                           "already exist in your database id:{0}".format(str(star.id()))]
            elif catalogue == "ASAS-SN" and catalogue_id:
                if catalogue_id == star.asassn():
                    return [[star.name()], "ASAS-SN error:\nThis star cross id. "
                                           "already exist in your database id:{0}".format(str(star.id()))]
            elif not catalogue or not catalogue_id:
                pass
            else:
                return [["-1"], "catalogue error:\nUnknown catalogue type"]
        if near_stars:
            return [near_stars, "list"]
        else:
            return ["", ""]
