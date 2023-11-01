from coordinate import *
from math import *
from numpy import *
from coordinate import Coordinate


class Star:
    """
    Star class. Each object has a name, equatorial coordinates , luminance.
    The available methods are :
    mag : returns the brightness in mag ( decimal ).
    coor : returns a Coordinate object
    horizon_coordinates_A : input is JD and Observer object , it returns Azimuth (rad)
    horizon_coordinates_h : input is JD and Observer object , it returns height above horizon (h) (rad)
    horizon_coordinate_str : input is A or h horizontal coordinate ( rad ).
                             function returns a string of the form DD MM SS.SS,
    the key parameter format can be changed delimiters = (" "," "," "), ("°","'",'"'), ("deg ","min ",'sec')
    """

    def __init__(self, id_object, name_object: str, alternative_name: str, coordinates: Coordinate,
                 magnitude: float, constellation: str, tess_sectors: str, type_object: str,  note_one: str,
                 note_two: str, note_three: str, b_v: str, j_k: str, ucac4: str, usnob1: str, gaia: str, vsx: str,
                 asassn: str, tess: str, comp0: int, comp1: int, comp2: int, comp3: int, comp4: int, comp5: int,
                 comp6: int, comp7: int, comp8: int, comp9: int, chk1: int, reserve1, reserve2, reserve3, reserve4,
                 reserve5, user_list=[], place_list=[], instrument_list=[], variability=True):
        self.__id = id_object
        self.__name = name_object
        self.__alt_name = alternative_name
        self.__coordinates = coordinates
        self.__mag = magnitude
        self.__constellation = constellation
        self.__tess_sectors = tess_sectors
        self.__type = type_object
        self.__note1 = note_one
        self.__note2 = note_two
        self.__note3 = note_three
        self.__b_v = b_v
        self.__j_k = j_k
        self.__ucac4 = ucac4
        self.__usnob1 = usnob1
        self.__gaia = gaia
        self.__vsx = vsx
        self.__asassn = asassn
        self.__tess = tess
        self.__comp0 = comp0
        self.__comp1 = comp1
        self.__comp2 = comp2
        self.__comp3 = comp3
        self.__comp4 = comp4
        self.__comp5 = comp5
        self.__comp6 = comp6
        self.__comp7 = comp7
        self.__comp8 = comp8
        self.__comp9 = comp9
        self.__chk1 = chk1
        self.__reserve1 = reserve1
        self.__reserve2 = reserve2
        self.__reserve3 = reserve3
        self.__reserve4 = reserve4
        self.__reserve5 = reserve5
        if user_list:
            self.__user_list = user_list.split(",")
        else:
            self.__user_list = []
        if place_list:
            self.__place_list = place_list.split(",")
        else:
            self.__place_list = []
        if instrument_list:
            self.__instrument_list = instrument_list.split(",")
        else:
            self.__instrument_list = []
        self.__variability = variability

    def __str__(self):
        return self.__name

    def change_id(self, new):
        self.__id = new

    def user_list_del_item(self, index):
        del(self.__user_list[index])

    def place_list_del_item(self, index):
        del(self.__place_list[index])

    def instrument_list_del_item(self, index):
        del(self.__instrument_list[index])

    def id(self):
        return self.__id

    def name(self):
        return self.__name

    def alt_name(self):
        return self.__alt_name

    def coordinate(self):
        return self.__coordinates

    def rektascenze(self):
        return self.__coordinates.rektascenze()

    def declination(self):
        return self.__coordinates.deklinace()

    def eq(self):
        return self.__coordinates.epoch()

    def mag(self):
        return self.__mag

    def constellation(self):
        return self.__constellation

    def tess_sectors(self):
        return self.__tess_sectors

    def type(self):
        return self.__type

    def note1(self):
        return self.__note1

    def note2(self):
        return self.__note2

    def note3(self):
        return self.__note3

    def b_v(self):
        return self.__b_v

    def j_k(self):
        return self.__j_k

    def ucac4(self):
        return self.__ucac4

    def usnob1(self):
        return self.__usnob1

    def gaia(self):
        return self.__gaia

    def vsx(self):
        return self.__vsx

    def asassn(self):
        return self.__asassn

    def tess(self):
        return self.__tess

    def comp0(self):
        return self.__comp0

    def comp1(self):
        return self.__comp1

    def comp2(self):
        return self.__comp2

    def comp3(self):
        return self.__comp3

    def comp4(self):
        return self.__comp4

    def comp5(self):
        return self.__comp5

    def comp6(self):
        return self.__comp6

    def comp7(self):
        return self.__comp7

    def comp8(self):
        return self.__comp8

    def comp9(self):
        return self.__comp9

    def chk1(self):
        return self.__chk1

    def user_list(self):
        return self.__user_list

    def place_list(self):
        return self.__place_list

    def instrument_list(self):
        return self.__instrument_list

    def variability(self):
        return self.__variability

    def change_name(self, new):
        self.__name = new

    def change_alt_name(self, new):
        self.__alt_name = new

    def change_coordinate(self, new):
        self.__coordinates = new

    def change_rektascenze(self, new):
        self.__coordinates.rektascenze = new

    def change_declination(self, new):
        self.__coordinates.deklinace = new

    def change_mag(self, new):
        self.__mag = new

    def change_constellation(self, new):
        self.__constellation = new

    def change_tess_sectors(self, new):
        self.__tess_sectors = new

    def change_type(self, new):
        self.__type = new

    def change_note1(self, new):
        self.__note1 = new

    def change_note2(self, new):
        self.__note2 = new

    def change_note3(self, new):
        self.__note3 = new

    def change_b_v(self, new):
        self.__b_v = new

    def change_j_k(self, new):
        self.__j_k = new

    def change_ucac4(self, new):
        self.__ucac4 = new

    def change_usnob1(self, new):
        self.__usnob1 = new

    def change_gaia(self, new):
        self.__gaia = new

    def change_vsx(self, new):
        self.__vsx = new

    def change_asassn(self, new):
        self.__asassn = new

    def change_tess(self, new):
        self.__tess = new

    def change_comp0(self, new):
        self.__comp0 = new

    def change_comp1(self, new):
        self.__comp1 = new

    def change_comp2(self, new):
        self.__comp2 = new

    def change_comp3(self, new):
        self.__comp3 = new

    def change_comp4(self, new):
        self.__comp4 = new

    def change_comp5(self, new):
        self.__comp5 = new

    def change_comp6(self, new):
        self.__comp6 = new

    def change_comp7(self, new):
        self.__comp7 = new

    def change_comp8(self, new):
        self.__comp8 = new

    def change_comp9(self, new):
        self.__comp9 = new

    def change_chk1(self, new):
        self.__chk1 = new

    def change_user_list(self, new):
        self.__user_list = new

    def change_place_list(self, new):
        self.__place_list = new

    def change_instrument_list(self, new):
        self.__instrument_list = new

    def change_variability(self, new):
        self.__variability = new

    def hour_angle(self, jd, longitude):
        star_time = (21.9433888888 + degrees(longitude)/15 + (jd - 2458534) * 24 * 1.0027379093) % 24
        rektascenze_now = self.__coordinates.rektascenze_now(jd)
        hour_angle = radians((star_time - degrees(rektascenze_now)/15)*15)  # in rad
        return hour_angle

    def horizon_coordinates_h(self, jd, longitude, latitude):
        deklinace_now = self.__coordinates.deklinace_now(jd)
        t = self.hour_angle(jd, longitude)
        z = arccos(sin(latitude)*sin(deklinace_now)+cos(latitude)*cos(deklinace_now)*cos(t))
        h = pi/2 - z
        return h

    def horizon_coordinates_a(self, jd, longitude, latitude):
        deklinace_now = self.__coordinates.deklinace_now(jd)
        t = self.hour_angle(jd, longitude)
        return self.__horizon_coordinate_a_from_cos_t(deklinace_now, latitude, t)

    @staticmethod
    def __horizon_coordinate_a_from_cos_t(deklinace_now, latitude, t):
        z = arccos(sin(latitude)*sin(deklinace_now)+cos(latitude)*cos(deklinace_now)*cos(t))
        if sin(z) != 0:
            sin_a = cos(deklinace_now)*sin(t)/sin(z)
            cos_a = (-cos(latitude)*sin(deklinace_now)+sin(latitude)*cos(deklinace_now)*cos(t))/sin(z)
            a = (atan2(sin_a, cos_a) + pi) % (2 * pi)
        else:
            a = pi
        return a

    def meridian(self, jd, longitude):  # return the nearest next star passage of a star through a meridian
        hour_angle = degrees(self.hour_angle(jd, longitude))/360  # hour angle in days
        if hour_angle < 0:
            return jd - hour_angle * 0.997269566
        else:
            return jd + (1 - hour_angle) * 0.997269566

    def daily_half_arc(self, h, jd, latitude):  # return daily half-arc in days, if 0 - no sunrise, if 0.5 - no sunset
        deklinace = self.__coordinates.deklinace_now(jd)
        cos_t0 = (cos(pi / 2 - h)-sin(deklinace) * sin(latitude))/(cos(latitude)*cos(deklinace))
        if cos_t0 >= 1:
            t0 = 0
        elif cos_t0 <= -1:
            t0 = 0.5
        else:
            t0 = degrees(arccos(cos_t0))/360
        return t0

    def sunrise_h(self, h, jd, longitude, latitude):  # return the nearest next star sunrice up h until jd
        meridian_time = self.meridian(jd, longitude)
        daily_half_arc = self.daily_half_arc(h, jd, latitude)
        if jd > meridian_time - daily_half_arc * 0.99726956637:
            return meridian_time - daily_half_arc * 0.99726956637 + 0.99726956637
        else:
            return meridian_time - daily_half_arc * 0.99726956637

    def sunset_h(self, h, jd, longitude, latitude):  # return the nearest next star sunset under h until jd
        meridian_time = self.meridian(jd, longitude)
        daily_half_arc = self.daily_half_arc(h, jd, latitude)
        if jd > meridian_time + daily_half_arc * 0.99726956637 - 0.99726956637:
            return meridian_time + daily_half_arc * 0.99726956637
        else:
            return meridian_time + daily_half_arc * 0.99726956637 - 0.99726956637

    def return_t(self, azimuth, jd_epoch, latitude):  # return cos() of hour angle for given azimuth
        deklinace = self.__coordinates.deklinace_now(jd_epoch)
        c_factor = ((sin(azimuth) ** 2) * (cos(latitude) ** 2) * (sin(deklinace) ** 2)) \
                   - ((cos(deklinace) ** 2) * (cos(azimuth) ** 2))
        b_factor = -2 * cos(latitude) * sin(
            deklinace) * sin(latitude) * cos(deklinace) * (sin(azimuth) ** 2)
        a_factor = ((sin(latitude) ** 2) * (
                cos(deklinace) ** 2) * (sin(azimuth) ** 2)) + ((cos(azimuth) ** 2) * (cos(deklinace) ** 2))
        discriminant = b_factor ** 2 - 4 * a_factor * c_factor
        if discriminant < 0:
            return None
        cos_t1 = (-b_factor + discriminant ** 0.5) / (2 * a_factor)
        cos_t2 = (-b_factor - discriminant ** 0.5) / (2 * a_factor)
        print(cos_t1, cos_t2, degrees(azimuth))
        if azimuth < pi:
            t1 = - arccos(cos_t1)
            t2 = - arccos(cos_t2)
        else:
            t1 = arccos(cos_t1)
            t2 = arccos(cos_t2)
        if -1 <= cos_t1 <= 1:
            test_azimuth_t1 = self.__horizon_coordinate_a_from_cos_t(deklinace, latitude, t1)
            if test_azimuth_t1 - 0.035 < azimuth < test_azimuth_t1 + 0.035:
                return t1
            else:
                return t2

    def star_to_txt(self):
        string = []
        string.append(str(self.__id))
        string.append(str(self.__name))
        string.append(str(self.__alt_name))
        string.append(str(self.__coordinates.rektascenze()))
        string.append(str(self.__coordinates.deklinace()))
        string.append(str(self.__coordinates.epoch()))
        string.append(str(self.__mag))
        string.append(str(self.__constellation))
        string.append(str(self.__tess_sectors))
        string.append(str(self.__type))
        string.append(str(self.__note1))
        string.append(str(self.__note2))
        string.append(str(self.__note3))
        string.append(str(self.__b_v))
        string.append(str(self.__j_k))
        string.append(str(self.__ucac4))
        string.append(str(self.__usnob1))
        string.append(str(self.__gaia))
        string.append(str(self.__vsx))
        string.append(str(self.__asassn))
        string.append(str(self.__tess))
        string.append(str(self.__comp0))
        string.append(str(self.__comp1))
        string.append(str(self.__comp2))
        string.append(str(self.__comp3))
        string.append(str(self.__comp4))
        string.append(str(self.__comp5))
        string.append(str(self.__comp6))
        string.append(str(self.__comp7))
        string.append(str(self.__comp8))
        string.append(str(self.__comp9))
        string.append(str(self.__chk1))
        string.append(str(self.__reserve1))
        string.append(str(self.__reserve2))
        string.append(str(self.__reserve3))
        string.append(str(self.__reserve4))
        string.append(str(self.__reserve5))
        string.append(",".join(self.__user_list))
        string.append(",".join(self.__place_list))
        string.append(",".join(self.__instrument_list))
        if self.__variability:
            string.append("VAR")
        else:
            string.append("CMP")
        return string
