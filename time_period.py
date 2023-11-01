from slunce_mesic import *
from observer import Observer
from object import *
from datetime import *
from slunce_mesic import Sun


class TimePeriod:

    def __init__(self, jd_start: float, jd_end: float):
        self.__jd_start = jd_start
        self.__jd_end = jd_end

    def set_jd_start(self, jd):
        self.__jd_start = jd

    def set_jd_end(self, jd):
        self.__jd_end = jd

    def jd_start(self):
        return self.__jd_start

    def jd_end(self):
        return self.__jd_end

    def inside(self, jd, extend_time_start=0, extend_time_end=0):
        return self.__jd_start - extend_time_start <= jd <= self.__jd_end + extend_time_end

    def interact_sun(self, sun: Sun, observer: Observer, extend_time_start=0, extend_time_end=0):
        time_period_sun_interact: list[float] = []
        midnight_jd = self.__jd_start - extend_time_start
        while midnight_jd < self.__jd_end + extend_time_end + 2:
            meridian_jd = sun.meridian(midnight_jd, observer.longitude)
            midnight_jd = meridian_jd - 0.5
            sunset_jd = sun.sunrise_h(observer.min_sunset, midnight_jd, observer.longitude, observer.latitude, False)
            sunrise_jd = sun.sunrise_h(observer.min_sunset, midnight_jd, observer.longitude, observer.latitude, True)
            if sunset_jd == "No sunrise" or sunrise_jd == "No sunrise":
                midnight_jd = midnight_jd + 1.1
                if meridian_jd > self.__jd_end + extend_time_end:
                    return time_period_sun_interact
            elif sunset_jd == "No sunset" or sunrise_jd == "No sunset":
                midnight_jd = midnight_jd + 1.1
                time_period_sun_interact.append(self.__jd_start - extend_time_start)
                if meridian_jd > self.__jd_end + extend_time_end:
                    time_period_sun_interact.append(self.__jd_end + extend_time_end)
                    return time_period_sun_interact
            else:
                if sunset_jd >= self.__jd_end + extend_time_end:
                    return time_period_sun_interact
                elif self.__jd_start - extend_time_start <= sunset_jd < self.__jd_end + extend_time_end:
                    time_period_sun_interact.append(sunset_jd)
                    if sunrise_jd <= self.__jd_end + extend_time_end:
                        time_period_sun_interact.append(sunrise_jd)
                        midnight_jd = midnight_jd + 1.1
                    else:
                        time_period_sun_interact.append(self.__jd_end + extend_time_end)
                        return time_period_sun_interact
                else:
                    time_period_sun_interact.append(self.__jd_start - extend_time_start)
                    if sunrise_jd <= self.__jd_end + extend_time_end:
                        time_period_sun_interact.append(sunrise_jd)
                        midnight_jd = midnight_jd + 1.1
                    else:
                        time_period_sun_interact.append(self.__jd_end + extend_time_end)
                        return time_period_sun_interact

    def __check_start_of_period(self, jd_visibles, extend_time_start=0, extend_time_end=0):
        if len(jd_visibles) % 2 == 1:
            jd_visibles.append(self.__jd_end + extend_time_end)
        while jd_visibles[0] < self.__jd_start - extend_time_start:
            del (jd_visibles[0])
            if not jd_visibles:
                return None
        if len(jd_visibles) % 2 == 1:
            jd_visibles.insert(0, self.__jd_start - extend_time_start)
        return jd_visibles

    def interact_horizon(self, observer: Observer, star, jd_step=0.0007, extend_time_start=0, extend_time_end=0):
        visible = False
        azimuth_set = observer.show_horizon()[0]
        h_latitude_set = observer.show_horizon()[1]
        h = degrees(observer.minimum_h)
        jd_visibles: list[float] = []
        latitude = observer.latitude
        longitude = observer.longitude
        meridian_time = star.meridian(self.__jd_start - extend_time_start, observer.longitude)
        if len(azimuth_set) < 2:
            if len(azimuth_set) == 1:
                if h_latitude_set[0] > h:
                    h = h_latitude_set[0]
            half_arc = star.daily_half_arc(radians(h), self.__jd_start - extend_time_start, latitude)
            if half_arc == 0:
                return None
            half_arc_time = half_arc * 0.99726956637
            jd_visibles.append(meridian_time - half_arc_time)
            jd_visibles.append(meridian_time + half_arc_time)
        else:
            half_arc = star.daily_half_arc(radians(h), self.__jd_start - extend_time_start, latitude)
            half_arc_time = half_arc * 0.99726956637
            if half_arc == 0:
                return None
            if 0 not in azimuth_set:
                h_latitude_0 = int((h_latitude_set[0] - h_latitude_set[-1]) / (azimuth_set[0] - azimuth_set[-1] + 360) *
                                   (360 - azimuth_set[-1]) + h_latitude_set[-1])
                azimuth_set = [0] + azimuth_set
                h_latitude_set = [h_latitude_0] + h_latitude_set
            azimuth_set = azimuth_set + [360]
            h_latitude_set = h_latitude_set + [h_latitude_set[0]]
            inspected_jd = meridian_time - half_arc_time
            while inspected_jd < meridian_time + half_arc_time:
                h_star = degrees(star.horizon_coordinates_h(inspected_jd, longitude, latitude))
                a_star = degrees(star.horizon_coordinates_a(inspected_jd, longitude, latitude))
                azimuth_set_index = 0
                while azimuth_set[azimuth_set_index] <= a_star:
                    azimuth_set_index = azimuth_set_index + 1
                if azimuth_set_index == 0:
                    horizon_h = h_latitude_set[0]
                else:
                    a_before = azimuth_set[azimuth_set_index - 1]
                    a_next = azimuth_set[azimuth_set_index]
                    h_before = h_latitude_set[azimuth_set_index - 1]
                    h_next = h_latitude_set[azimuth_set_index]
                    horizon_h = (h_next - h_before) / (a_next - a_before) * (a_star - a_before) + h_before
                    if horizon_h < h:
                        horizon_h = h
                if horizon_h < h_star and not visible:
                    jd_visibles.append(inspected_jd)
                    visible = True
                if horizon_h >= h_star and visible:
                    jd_visibles.append(inspected_jd)
                    visible = False
                inspected_jd = inspected_jd + jd_step
            if visible:
                jd_visibles.append(meridian_time + half_arc)
            if not jd_visibles:
                return None
        x = jd_visibles[0] - (meridian_time - half_arc_time)
        za = jd_visibles[-1] - (meridian_time + half_arc_time)
        if half_arc == 0.5 and jd_visibles[0] == meridian_time - half_arc_time and jd_visibles[-1] == meridian_time + half_arc_time:
            if len(jd_visibles) == 2:
                jd_visibles[0] = self.__jd_start - extend_time_start
                jd_visibles[1] = self.__jd_end + extend_time_end
                return jd_visibles
            else:
                del(jd_visibles[-1])
                if jd_visibles[-1] > self.__jd_end + extend_time_end:
                    while jd_visibles[-1] > self.__jd_end + extend_time_end:
                        del(jd_visibles[-1])
                        if not jd_visibles:
                            return None
                    return self.__check_start_of_period(jd_visibles, extend_time_start=extend_time_start,
                                                        extend_time_end=extend_time_end)
                else:
                    jd_visibles_length_for_copy = len(jd_visibles) - 1
                    while jd_visibles[-jd_visibles_length_for_copy] + 0.99726956637 < self.__jd_end + extend_time_end:
                        jd_visibles.append(jd_visibles[-jd_visibles_length_for_copy] + 0.99726956637)
                    return self.__check_start_of_period(jd_visibles, extend_time_start=extend_time_start,
                                                        extend_time_end=extend_time_end)
        else:
            if jd_visibles[-1] > self.__jd_end + extend_time_end:
                while jd_visibles[-1] > self.__jd_end + extend_time_end:
                    del(jd_visibles[-1])
                    if not jd_visibles:
                        return None
                return self.__check_start_of_period(jd_visibles, extend_time_start=extend_time_start,
                                                    extend_time_end=extend_time_end)
            else:
                jd_visibles_length_for_copy = len(jd_visibles)
                while jd_visibles[-jd_visibles_length_for_copy] + 0.99726956637 < self.__jd_end + extend_time_end:
                    jd_visibles.append(jd_visibles[-jd_visibles_length_for_copy] + 0.99726956637)
                jd_visibles = self.__check_start_of_period(jd_visibles, extend_time_start=extend_time_start,
                                                           extend_time_end=extend_time_end)
                return jd_visibles

    def visibility_point(self, observer: Observer, star, sun, sun_visibility=True,
                         horizon_visibility=True, moon_visibility=False, step=1500, extend_time_start=0,
                         extend_time_end=0):
        sun_visibility_jd = [self.__jd_start - extend_time_start, self.__jd_end + extend_time_end]
        moon_visibility_jd = [self.__jd_start - extend_time_start, self.__jd_end + extend_time_end]
        horizon_visibility_jd = [self.__jd_start - extend_time_start, self.__jd_end + extend_time_end]

        if sun_visibility:
            sun_visibility_jd = self.interact_sun(sun, observer, extend_time_start=extend_time_start,
                                                  extend_time_end=extend_time_end)
        if moon_visibility:
            pass
        if horizon_visibility:
            horizon_visibility_jd = self.interact_horizon(observer, star, extend_time_start=extend_time_start,
                                                          extend_time_end=extend_time_end)

        sun_visibility_point = []
        moon_visibility_point = []
        horizon_visibility_point = []
        time_aria = self.__jd_end - self.__jd_start + extend_time_start + extend_time_end
        for i in range(step):
            jd = self.__jd_start - extend_time_start + time_aria / step * i
            if sun_visibility_jd:
                if jd >= sun_visibility_jd[0]:
                    a = sun_visibility_jd.pop(0)
                if len(sun_visibility_jd) % 2 == 0:
                    sun_visibility_point.append(False)
                else:
                    sun_visibility_point.append(True)
            else:
                sun_visibility_point.append(False)

            if moon_visibility_jd:
                if jd >= moon_visibility_jd[0]:
                    a = moon_visibility_jd.pop(0)
                if len(moon_visibility_jd) % 2 == 0:
                    moon_visibility_point.append(False)
                else:
                    moon_visibility_point.append(True)
            else:
                moon_visibility_point.append(False)

            if horizon_visibility_jd:
                if jd >= horizon_visibility_jd[0]:
                    a = horizon_visibility_jd.pop(0)
                if len(horizon_visibility_jd) % 2 == 0:
                    horizon_visibility_point.append(False)
                else:
                    horizon_visibility_point.append(True)
            else:
                horizon_visibility_point.append(False)

        visibility = []
        for i in range(len(sun_visibility_point)):
            if horizon_visibility_point[i] and sun_visibility_point[i] and moon_visibility_point[i]:
                visibility.append(True)
            else:
                visibility.append(False)
        return visibility

def jd_to_date(jd: float):
    delta_sec = int((jd - 2458534)*86400)
    return timedelta(seconds=delta_sec) + datetime(2019, 2, 19, 12, 0, tzinfo=timezone.utc)

def date_to_jd(today_date):
    return (today_date - datetime(2019, 2, 19, 12, 0, tzinfo=timezone.utc)).total_seconds()/86400 + 2458534



