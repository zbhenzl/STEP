from coordinate import *
from horizon import *
from math import *


class Observer:

    """
    Class of observation points. The basic information is latitude and longitude. It is also possible to add site
    preferences ( horizon shape, minimum height of the object to be observed above the horizon, minimum depth of
    the Sun below the horizon, minimum distance and maximum phase of the Moon ).
    """

    def __init__(self, id_place, name, latitude, longitude, user_id, instrument_id, min_sunset=0.2094395102393195,
                 horizon=Horizon(0, [0], [0]), minimum_object_latitude=0.523599):
        self.__id = id_place
        self.__name = name
        self.__longitude = longitude
        self.__latitude = latitude
        self.__user_id = user_id
        self.__min_sunset = min_sunset
        self.__horizon: Horizon = horizon
        self.__minimum_object_latitude = minimum_object_latitude
        self.__instrument_id = instrument_id


    def __str__(self):
        return self.__name


    def edit_all(self, key_value, value, places, horizons):
        if places.observers():
            row = places.return_row(key_value, value)
            if row:
                self.__id = int(row[0])
                self.__name = row[1]
                self.__user_id = row[2]
                self.__horizon.edit_all("id", row[3], horizons)
                self.__instrument_id = row[4]
                self.__latitude = float(row[5])
                self.__longitude = float(row[6])
                self.__minimum_object_latitude = float(row[7])
                self.__min_sunset = float(row[8])
            else:
                self.__id = 0
                self.__name = "add_place"
                self.__user_id = 0
                self.__horizon.set_id(0)
                self.__horizon.set_azimuths([0, 180])
                self.__horizon.set_h([0, 0])
                self.__instrument_id = 0
                self.__latitude = 0
                self.__longitude = 0
                self.__minimum_object_latitude = 0
                self.__min_sunset = 0

        else:
            self.__id = 0
            self.__name = "add_place"
            self.__user_id = 0
            self.__horizon.set_id(0)
            self.__horizon.set_azimuths([0, 180])
            self.__horizon.set_h([0, 0])
            self.__instrument_id = 0
            self.__latitude = 0
            self.__longitude = 0
            self.__minimum_object_latitude = 0
            self.__min_sunset = 0

    @property
    def longitude(self):
        return self.__longitude

    @property
    def latitude(self):
        return self.__latitude

    @property
    def id(self):
        return self.__id

    @property
    def user_id(self):
        return self.__user_id

    @property
    def name(self):
        return self.__name

    def set_min_sunset(self, min_sunset: float):
        self.__min_sunset = min_sunset

    @property
    def min_sunset(self):
        return self.__min_sunset

    @property
    def instrument_id(self):
        return self.__instrument_id

    @property
    def minimum_h(self):
        return self.__minimum_object_latitude

    def set_minimum_h(self, minimum_object_latitude: float):
        self.__minimum_object_latitude = minimum_object_latitude

    def longitude_text(self):
        return coordinate_to_text(self.__longitude)

    def latitude_text(self):
        return coordinate_to_text(self.__latitude)

    def show_horizon(self):
        return self.__horizon.give_horizon()

    def horizon(self):
        return self.__horizon

    def set_horizon(self, horizon):
        self.__horizon = horizon

    def horizontal_to_eqatoreal(self, jd, a, h):
        z = pi/2 - h
        dec = asin(cos(z) * sin(self.latitude) - sin(z) * cos(self.latitude) * cos(a))
        cos_t = (cos(z) * cos(self.latitude) + sin(z) * sin(self.latitude) * cos(a))/cos(dec)
        sin_t = (sin(z)*sin(a))/cos(dec)
        t = atan2(sin_t, cos_t)
        star_time = radians(((21.9433888888 + degrees(self.longitude)/15 + (jd - 2458534) * 24 * 1.0027379093) % 24)*15)
        rec = star_time - t
        return Coordinate(rec, dec, epoch="now")

    @property
    def horizon_id(self):
        return self.__horizon.id


class Observers:

    def __init__(self, observers, observers_key):
        self.__observers = observers
        self.__observers_key = observers_key

    def observers(self):
        return self.__observers

    def observers_key(self):
        return self.__observers_key

    def return_row(self, key_value, value):
        if key_value in self.__observers_key:
            key_index = self.__observers_key.index(key_value)
            if self.__observers:
                for row in self.__observers:
                    if row[key_index] == value:
                        return row
        row = self.__observers[0]
        return row

    def edit_h(self, name, h, sun_h):
        for i, row in enumerate(self.__observers):
            if row[1] == name:
                self.__observers[i][7] = str(h)
                self.__observers[i][8] = str(sun_h)

    def edit_observers(self, new_observers):
        self.__observers = new_observers

    def edit_place(self, new_name, last_name, longitude, latitude, h, sun_h):
        for place in self.__observers:
            if last_name == place[1]:
                place[1] = str(new_name)
                place[6] = str(longitude)
                place[5] = str(latitude)
                place[7] = str(h)
                place[8] = str(sun_h)

    def place_list(self, user):
        place_list = []
        for place_row in self.__observers:
            if place_row[2] == user:
                place_list.append(place_row[1])
        return place_list

    def delete_observer(self, observer_name):
        from step_application import root
        for star in root.database.stars.stars:
            if observer_name in star.place_list():
                new_list = star.place_list()
                new_list.remove(observer_name)
                star.change_place_list(new_list)
        for i, observer in enumerate(self.__observers):
            if observer[1] == observer_name:
                del(self.__observers[i])
                return

    def add_observer(self, name, latitude, longitude, user_name, sun_h, h):
        all_id = []
        if self.__observers:
            for observer_row in self.__observers:
                all_id.append(observer_row[0])
            all_id.sort()
            new_id = int(all_id[-1]) + 1
        else:
            new_id = 1
        new_row = [str(new_id)]
        new_row.append(name)
        new_row.append(user_name)
        new_row.append(str(0))
        new_row.append(str(0))
        new_row.append(str(latitude))
        new_row.append(str(longitude))
        new_row.append(str(h))
        new_row.append(str(sun_h))
        self.__observers.append(new_row)

    def change_user(self, new_user, last_user):
        for observer_row in self.__observers:
            if observer_row[2] == last_user:
                observer_row[2] = new_user

    def edit_horizon_id(self, index, new_horizon_id):
        self.__observers[index][3] = new_horizon_id


