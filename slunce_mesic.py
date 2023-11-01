from numpy import *
from coordinate import *
from math import *
from coordinate import Coordinate


class Sun:

    def __init__(self):
        self._e = 0.016709

    def __str__(self):
        return "Sun"

    @staticmethod
    def _ecliptical_to_equatorial(ecliptic_longitude: float, ecliptic_latitude: float, jd: float):  # convert ecliptic coordinates B,L to equatorial alpha and delta , all radians
        delta = asin(cos(ecliptic_latitude) * sin(ecliptic_longitude) * sin(Coordinate.ecliptic_inclination(jd)) + sin(
            ecliptic_latitude) * cos(Coordinate.ecliptic_inclination(jd)))
        if delta == -pi / 2 or delta == pi / 2:
            alfa = 0
        else:
            alfa_sin = (cos(ecliptic_latitude) * cos(Coordinate.ecliptic_inclination(jd)) * sin(ecliptic_longitude) -
                        sin(ecliptic_latitude) * sin(Coordinate.ecliptic_inclination(jd))) / cos(delta)
            alfa_cos = cos(ecliptic_longitude) * cos(ecliptic_latitude) / cos(delta)
            alfa = (atan2(alfa_sin, alfa_cos)) % (2*pi)
        return [alfa, delta]

    def coordinates(self, jd: float, iteration_kepler=10):  # return L and B for given JD
        d = jd - 2451543.5  # days from 31.12.1999
        omega = radians((d * 0.0000470935 + 102.9404) % 360)  # argument perihelu Earth
        m = radians((356.047 + 0.9856002585 * d) % 360)  # Earth's central anomaly
        e_rad = m + self._e * sin(m)  # eccentric anomaly 1st iteration
        for i in range(iteration_kepler):  # eccentric anomaly iteration of the Kepler equations
            e_rad = m + self._e * sin(e_rad)
        x = cos(e_rad) - self._e  # rectangular coordinate x
        y = sin(e_rad) * sqrt(1 - self._e ** 2)  # rectangular coordinate y
        if atan2(y, x) < 0:  # a true anomaly
            ny = atan2(y, x) + 2*pi
        else:
            ny = atan2(y, x)
        longitude = (ny + omega + pi) % (2*pi)  # ecliptic longitude of the Sun
        return self._ecliptical_to_equatorial(longitude, 0, jd)  # return equatorial coordinates

    @staticmethod
    def _lst(jd, longitude):  # calculates the local star time (days, radians )
        time0 = 21.94338889 + longitude * 12 / pi + (jd - 2458534) * 24 * 1.0027379093
        local_star_time = fmod(time0, 24)
        return local_star_time  # hours

    def hour_angle(self, jd, longitude):
        star_time = (21.9433888888 + degrees(longitude)/15 + (jd - 2458534) * 24 * 1.0027379093) % 24
        rektascenze_now = self.coordinates(jd)[0]
        hour_angle = radians((star_time - degrees(rektascenze_now)/15)*15)  # in rad
        return hour_angle

    def meridian(self, jd, longitude):  # return the nearest next sun passage through a meridian. 1. iteration only
        hour_angle = degrees(self.hour_angle(jd, longitude))/360  # hour angle in days
        if hour_angle < 0:
            return jd - hour_angle * 0.997269566
        else:
            return jd + (1 - hour_angle) * 0.997269566

    def __daily_half_arc(self, h, jd, latitude):  # return daily half-arc in days, if 0 - no sunrise, if 0.5 - no sunset
        deklinace = self.coordinates(jd)[1]
        cos_t0 = (cos(pi / 2 - h)-sin(deklinace) * sin(latitude))/(cos(latitude)*cos(deklinace))
        return cos_t0

    def sunrise_h(self, h, jd, longitude, latitude, is_sunrise=True):  # returns the moment of sunrise/sunset,sunrise = true
        new_jd = self.meridian(jd, longitude)
        daily_half_arc = self.__daily_half_arc(h, new_jd, latitude)
        if daily_half_arc >= 1:
            return "No sunrise"
        elif daily_half_arc <= -1:
            return "No sunset"
        else:
            daily_half_arc = degrees(arccos(daily_half_arc)) / 360
            if is_sunrise:
                if new_jd - daily_half_arc < jd and isinstance(self, Sun):
                    new_jd = new_jd - daily_half_arc + 1
                else:
                    new_jd = new_jd - daily_half_arc
                    for i in range(3):
                        meridian = self.meridian(new_jd, longitude)
                        daily_half_arc = self.__daily_half_arc(h, new_jd, latitude)
                        if daily_half_arc >= 1:
                            return "No sunrise"
                        elif daily_half_arc <= -1:
                            return "No sunset"
                        else:
                            new_jd = meridian - degrees(arccos(daily_half_arc))/360
            else:
                if new_jd - daily_half_arc < jd or isinstance(self, Moon):
                    new_jd = new_jd + daily_half_arc
                else:
                    new_jd = new_jd + daily_half_arc - 1
                    for i in range(3):
                        meridian = self.meridian(new_jd, longitude) - 0.997269566
                        daily_half_arc = self.__daily_half_arc(h, new_jd, latitude)
                        if daily_half_arc >= 1:
                            return "No sunrise"
                        elif daily_half_arc <= -1:
                            return "No sunset"
                        else:
                            new_jd = meridian + degrees(arccos(daily_half_arc))/360
        return new_jd

    def h(self, jd, latitude, longitude):
        equatorial_coordinate = self.coordinates(jd)
        alpha = equatorial_coordinate[0]
        delta = equatorial_coordinate[1]
        lst = (21.9433888888 + degrees(longitude)/15 + (jd - 2458534) * 24 * 1.0027379093) % 24
        t = radians((lst - degrees(alpha)/15)*15)
        z_sun = arccos(sin(latitude) * sin(delta) + cos(latitude) * cos(delta) * cos(t))
        h: float = pi/2 - z_sun
        return h

    def azimuth(self, jd, latitude, longitude):
        equatorial_coordinate = self.coordinates(jd)
        alpha = equatorial_coordinate[0]
        delta = equatorial_coordinate[1]
        lst = (21.9433888888 + degrees(longitude)/15 + (jd - 2458534) * 24 * 1.0027379093) % 24
        t = radians((lst - degrees(alpha)/15)*15)
        z = arccos(sin(latitude) * sin(delta) + cos(latitude) * cos(delta) * cos(t))
        sin_a = cos(delta) * sin(t) / sin(z)
        cos_a = (-cos(latitude) * sin(delta) + sin(latitude) * cos(delta) * cos(t)) / sin(z)
        a = (atan2(sin_a, cos_a) + pi) % (2 * pi)
        return a


class Moon(Sun):

    def __init__(self):
        super(Moon, self).__init__()

    def __str__(self):
        return "Moon"

    def coordinates(self, jd, iteration_kepler=10):
        d = jd - 2451543.5  # days from 31.12.1999
        m_big_omega = (125.1228 - 0.0529538083 * d) % 360 / 180 * pi  # Length of the exit node of the Moon's orbit
        m_i = 5.1454 / 180 * pi  # inclination of the orbit to the ecliptic
        m_omega = (d * 0.1643573223 + 318.0634) % 360 / 180 * pi  # the argument of the Moon's perihelion
        m_a = 60.2666  # the great axis of orbit (in Earth radii )
        m_ex = 0.0549  # numerical eccentricity of the Moon's orbit
        m_m = (115.3654 + 13.0649929509 * d) % 360 / 180 * pi  # mean lunar anomaly
        m_e = (m_m + m_ex * sin(m_m))  # iteration (first term) for solving the eccentric anomaly
        for i in range(iteration_kepler):  # iterations (10x) to solve the eccentric anomaly
            m_e = m_m + m_ex * sin(m_e)
        m_x = m_a * (cos(m_e) - m_ex)  # geocentric orthogonal coordinates x
        m_y = m_a * sin(m_e) * sqrt(1 - m_ex * m_ex)  # geocentric orthogonal coordinates y
        if atan2(m_y, m_x) < 0:  # a true anomaly
            m_ny = atan2(m_y, m_x) + 2 * pi
        else:
            m_ny = atan2(m_y, m_x)
        m_r0 = sqrt(m_x * m_x + m_y * m_y)  # preliminary distance
        m_xe = m_r0 * (cos(m_big_omega) * cos(m_ny + m_omega) - sin(m_big_omega) * sin(m_ny + m_omega) * cos(m_i))
        # ecliptic coordinates x
        m_ye = m_r0 * (sin(m_big_omega) * cos(m_ny + m_omega) + cos(m_big_omega) * sin(m_ny + m_omega) * cos(m_i))
        # ecliptic coordinates y
        m_ze = m_r0 * (sin(m_ny + m_omega) * sin(m_i))  # ecliptic coordinates z
        m_l0 = atan2(m_ye, m_xe)  # preliminary ecliptic longitude
        m_b0 = atan2(m_ze, sqrt(m_xe * m_xe + m_ye * m_ye))  # preliminary ecliptic latitude
        s_m = (356.047 + 0.9856002585 * d) % 360 / 180 * pi  # mean solar anomaly
        s_omega = (d * 0.0000470935 + 102.9404) % 360 / 180 * pi  # length of the exit node of the Sun
        sl = (s_omega + s_m + pi)  # mean longitude of the Sun
        ml = (m_m + m_omega + m_big_omega)  # mean lunar longitude
        d = ml - sl  # mean lunar elongation
        f = ml - m_big_omega  # argument of the latitude of the Moon
        # correction for the longitude of the Moon
        lp = -1.274 * sin(m_m - 2 * d) + 0.658 * sin(2 * d) - 0.186 * sin(s_m) - 0.059 * sin(
            2 * m_m - 2 * d) - 0.057 * sin(m_m - 2 * d + s_m) + 0.053 * sin(m_m + 2 * d) + 0.046 * sin(
            2 * d - s_m) + 0.041 * sin(m_m - s_m) - 0.035 * sin(d) - 0.031 * sin(m_m + s_m) - 0.015 * sin(
            2 * f - 2 * d) + 0.011 * sin(m_m - 4 * d)
        # correction for the latitude of the Moon
        bp = -0.173 * sin(f - 2 * d) - 0.055 * sin(m_m - f - 2 * d) - 0.046 * sin(m_m + f - 2 * d) + 0.033 * sin(
            f + 2 * d) + 0.017 * sin(2 * m_m + f)
        m_b = m_b0 + bp / 180 * pi  # ecliptic latitude of the Moon
        m_l = (m_l0 + lp / 180 * pi) % (2*pi)  # ecliptic longitude of the Moon
        return self._ecliptical_to_equatorial(m_l, m_b, jd)  # return equatorial coordinates

    def moon_phase(self, jd):
        return (self.coordinates(jd)[0] - super(Moon, self).coordinates(jd)[0]) % (2*pi)
