from database import *
from math import *
import time as tm
from astropy.coordinates import SkyCoord
from astropy import units as u


class Coordinate:

    """
    equatorial coordinate class , provides conversion of coordinates between different formats and also conversion to
    the Horizon type or the time at which a given coordinate will pass through the meridian at a given location and the
    position of the coordinates at a defined height above the horizon
    """
    def __init__(self, rektascenze, deklinace, epoch="2000"):
        self.__rektascenze = rektascenze
        self.__deklinace = deklinace
        self.__epoch = str(epoch)
        self.__error_report = None
        if self.__epoch == "1950":
            self.__epoch_jd = 2433282.5
        elif self.__epoch == "1975":
            self.__epoch_jd = 2442413.5
        elif self.__epoch == "2000":
            self.__epoch_jd = 2451544.5
        elif self.__epoch == "now":
            self.__epoch_jd = floor((tm.time() - 946728000) / 86400 + 2451545)
        else:
            self.__error_report = "Unidentified epoch"
        self.__formats = ("hours", "degrees", "deg_dec", "rad_dec")
        self.__delimiters = (" ", ":",)

    @staticmethod
    def ecliptic_inclination(jd):
        return radians(23.4522944444 - 0.00013011111 * (jd - 2415020.5) / 365.242192)

    def rektascenze(self):  # always return epoch 2000
        if 2451544.5 == self.__epoch_jd:
            return self.__rektascenze
        else:
            return self.rektascenze_now(2451544.5)

    def deklinace(self):  # always return epoch 2000
        if 2451544.5 == self.__epoch_jd:
            return self.__deklinace
        else:
            return self.deklinace_now(2451544.5)

    def rektascenze_now(self, jd):  # is is working only with epoch 2000 now
        n_precese_deklinace = 0.0002442055 * sin(self.ecliptic_inclination(jd))
        m_precese_rektascenze = 0.0002442055 * cos(self.ecliptic_inclination(jd))-0.0000006060171
        if self.__rektascenze:
            return (jd - self.__epoch_jd)/365.25*(m_precese_rektascenze + n_precese_deklinace *
                                                  tan(self.__deklinace)*sin(self.__rektascenze)) + self.__rektascenze
        else:
            return self.__rektascenze

    def deklinace_now(self, jd):
        n_precese_deklinace = 0.0002442055 * sin(self.ecliptic_inclination(jd))
        if self.__deklinace:
            return (jd - self.__epoch_jd) / 365.25 * (n_precese_deklinace * cos(self.__rektascenze)) + self.__deklinace
        else:
            return self.__deklinace

    def coordinate_error_report(self):
        return self.__error_report

    def epoch(self):
        return self.__epoch

    def get_const(self):
        c = SkyCoord(self.__rektascenze * u.rad, self.__deklinace * u.rad, frame="icrs")
        const = c.get_constellation(short_name=True, constellation_list='iau')
        return const


def coordinate_to_text(coordinate, coordinate_format="degree", delimiters=(" ", " ", " "), decimal_numbers=2):
    accepted_delimiters_set = ((" ", " ", " "), ("° ", "' ", '"'), ("deg ", "min ", 'sec'), ("h ", "m ", 's'),
                               ("° ", "m ", 's'), ("h ", "' ", '"'), (":", ":", ""))
    accepted_format_set = ("degree", "hours")
    if not (delimiters in accepted_delimiters_set):
        delimiters = (" ", " ", " ")
    if not (coordinate_format in accepted_format_set):
        coordinate_format = "degree"
    if coordinate_format == "hours":
        coordinate = coordinate / 15
    if coordinate < 0:
        positive_negative_sign = "-"
    else:
        positive_negative_sign = "+"
    coordinate = fabs(degrees(coordinate))
    degree = floor(coordinate)
    minute = floor((coordinate - degree)*60)
    second = round(((coordinate - degree)*60 - minute) * 60, decimal_numbers)
    if degree < 10:
        degree = "0" + str(degree)
    else:
        degree = str(degree)
    if minute < 10:
        minute = "0" + str(minute)
    else:
        minute = str(minute)
    if second < 10:
        second = "0" + str(second)
    else:
        second = str(second)
    return positive_negative_sign + degree + delimiters[0] + minute + delimiters[1] + second + delimiters[2]


def read_coordinate(coordinate: str, coor_format="rektascenze_hours", delimiter=None):
    formats = ("rektascenze_hours", "rektascenze_degrees", "declination_degrees")
    if coor_format not in formats:
        return ["", "", "", "", coor_format, "Unknown coordinate format"]
    if not delimiter:
        if ":" in coordinate:
            delimiter = ":"
        else:
            delimiter = " "
    h_m_s = coordinate.split(delimiter)
    if len(h_m_s) == 3:
        try:
            h = int(h_m_s[0])
            m = int(h_m_s[1])
            s = float(h_m_s[2])
        except:
            return ["", "", "", "", coor_format,
                    "Coordinate don´t return number after split {0}. It returns {1},{2},{3}"
                    .format(delimiter, h_m_s[0], h_m_s[1], h_m_s[2])]
        if coor_format == "rektascenze_hours" and (h < 0 or h > 23):
            return ["", "", "", "", coor_format, "Hours are out of range"]
        elif coor_format == "rektascenze_degrees" and (h < 0 or h > 359):
            return ["", "", "", "", coor_format, "Degrees are out of range"]
        elif coor_format == "declination_degrees" and (h < -89 or h > 89):
            return ["", "", "", "", coor_format, "Degrees are out of range"]
        elif m < 0 or m > 59:
            return ["", "", "", "", coor_format, "Minutes are out of range"]
        elif s < 0 or s >= 60:
            return ["", "", "", "", coor_format, "Seconds are out of range"]
        else:
            pass

        if h_m_s[0][0] == "-" and coor_format == "declination_degrees":
            h = -h
            coor_decimal = h + m / 60 + s / 3600
            coor_decimal = -coor_decimal
        else:
            coor_decimal = h + m / 60 + s / 3600
        if coor_format == "rektascenze_hours":
            coor_decimal = coor_decimal * 15
        coor_rad = radians(coor_decimal)
        return [h_m_s[0], h_m_s[1], h_m_s[2], coor_rad, coor_format, ""]
    else:
        return ["", "", "", "", coor_format, "separator error: {0}".format(delimiter)]
