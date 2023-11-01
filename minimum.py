from observer import Observer
from slunce_mesic import Sun
from time_period import *
from slunce_mesic import *
from astropy.coordinates import angular_separation


class Minimum:

    def __init__(self, minimum_jd: float, minimum_type: bool):
        self.__minimum_jd = minimum_jd
        self.__minimum_type = minimum_type

    def __str__(self):
        if self.__minimum_type:
            return "Minimum:{0} - P".format(str(self.__minimum_jd, ))
        else:
            return "Minimum:{0} - S".format(str(self.__minimum_jd, ))

    def minimum_jd(self):
        return self.__minimum_jd

    def minimum_type(self):
        return self.__minimum_type

    def minimum_p_s(self):
        if self.__minimum_type:
            return "P"
        else:
            return "S"

    def visibility_sun(self, sun: Sun, h_sun_max: int, latitude, longitude):
        h_sun = sun.h(self.__minimum_jd, latitude, longitude)
        if h_sun < h_sun_max:
            return True
        else:
            return False

    def visibility_horizon(self, place_of_obs, star):
        h_star = degrees(star.horizon_coordinates_h(self.__minimum_jd, place_of_obs.longitude, place_of_obs.latitude))
        a_star = degrees(star.horizon_coordinates_a(self.__minimum_jd, place_of_obs.longitude, place_of_obs.latitude))
        azimuth_set = place_of_obs.horizon().azimuth()
        h_altitude_set = place_of_obs.horizon().h_altitude()
        for i, point in enumerate(azimuth_set):
            if point > a_star:
                h_horizon = (h_altitude_set[i] - h_altitude_set[i-1]) / (azimuth_set[i] - azimuth_set[i-1]) * \
                            (a_star - azimuth_set[i-1]) + h_altitude_set[i-1]
                if h_horizon < degrees(place_of_obs.minimum_h):
                    h_horizon = degrees(place_of_obs.minimum_h)
                if h_horizon < h_star:
                    return True
                else:
                    return False

    def visibility_moon(self, moon, star, max_phase: float, min_distance, latitude, longitude):
        moon_coor = moon.coordinates(self.__minimum_jd)
        moon_rec = moon_coor[0]
        moon_dec = moon_coor[1]
        h_moon = moon.h(self.__minimum_jd, latitude, longitude)
        moon_phase = moon.moon_phase(self.__minimum_jd)
        if h_moon <= 0:
            return True
        elif h_moon > 0 and fabs(1 - moon_phase/pi) >= (1 - max_phase / 100):
            return True
        elif angular_separation(star.coordinate().rektascenze(),
                                star.coordinate().deklinace(),
                                moon_rec,
                                moon_dec) > min_distance:
            return True
        else:
            return False

        # h_moon > 0 and fabs(1 - moon_phase/pi) < (1 - max_phase / 100) and



