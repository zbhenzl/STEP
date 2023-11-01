from math import *


def half_arc_A_h(latitude, deklination, rektascenze, step):
    a_list = []
    h_list = []
    star_time_list = []
    cos_t0 = -tan(latitude) * tan(deklination)
    if cos_t0 <= -1:
        t0 = pi
    elif cos_t0 >= 1:
        t0 = 0
        return [a_list, h_list, star_time_list]
    else:
        t0 = acos(cos_t0)
    position = -(t0)

    while position <= t0:
        star_time = (rektascenze + position) % (2 * pi)
        z = acos(sin(latitude) * sin(deklination) + cos(latitude) * cos(deklination) * cos(position))
        h = degrees(pi/2-z)
        if sin(z) != 0:
            sin_a = cos(deklination) * sin(position) / sin(z)
            cos_a = (-cos(latitude) * sin(deklination) + sin(latitude) * cos(deklination) * cos(position)) / sin(z)
            a = (atan2(sin_a, cos_a) + pi) % (2 * pi)
            a = degrees(a)
        else:
            a = 180
        if a_list:
            if h == h_list[-1] and a == a_list[-1]:
                pass
            else:
                h_list.append(h)
                a_list.append(a)
                star_time_list.append(star_time)
        else:
            h_list.append(h)
            a_list.append(a)
            star_time_list.append(star_time)

        position = position + t0 / step
    return [a_list, h_list, star_time_list]


class Horizon:

    def __init__(self, id_horizon, azimuth, h_altitude):
        self.__azimuth = azimuth
        self.__h_altitude = h_altitude
        self.__id = id_horizon


    def __str__(self):
        return self.__id

    @property
    def id(self):
        return self.__id

    def set_id(self, new_id):
        self.__id = new_id

    def insert_point(self, azimuth_point, h_latitude_point):
        if isinstance(azimuth_point, int) and isinstance(h_latitude_point, int):
            if 0 <= azimuth_point < 360 and 0 <= h_latitude_point < 90:
                if azimuth_point in self.__azimuth:
                    azimuth_point_index = self.__azimuth.index(azimuth_point)
                    self.__h_altitude[azimuth_point_index] = h_latitude_point
                else:
                    self.__azimuth.append(azimuth_point)
                    self.__azimuth.sort()
                    azimuth_index = self.__azimuth.index(azimuth_point)
                    self.__h_altitude.insert(azimuth_index, h_latitude_point)

    def delete_point(self, azimuth_point):
        if azimuth_point in self.__azimuth:
            del(self.__h_altitude[self.__azimuth.index(azimuth_point)])
            self.__azimuth.remove(azimuth_point)

    def set_azimuths(self, new_azimuth_set):
        self.__azimuth = new_azimuth_set

    def set_h(self, new_h):
        self.__h_altitude = new_h

    def give_horizon(self):
        return [self.__azimuth, self.__h_altitude]

    def horizon_coordinate(self):
        return list(zip(self.__azimuth, self.__h_altitude))

    def azimuth(self):
        if self.__azimuth[0] != 0:
            azimuth_with_0 = [0] + self.__azimuth + [360]
        else:
            azimuth_with_0 = self.__azimuth + [360]
        return azimuth_with_0

    def h_altitude(self):
        if self.__azimuth[0] != 0:
            h0 = self.__h_altitude[0]
            h1 = self.__h_altitude[-1]
            a0 = self.__azimuth[0]
            a1 = self.__azimuth[-1]
            zero_h_altitude = int((h1 - h0) / (a0 - a1 + 360) * a0) + h0
            h_altitudes = [zero_h_altitude] + self.__h_altitude + [zero_h_altitude]
        else:
            h_altitudes = self.__h_altitude + [self.__h_altitude[0]]
        return h_altitudes

    def edit_all(self, key_value, value, horizons):
        if horizons.horizons():
            row = horizons.return_row(key_value, value)
            if row:
                azimuths: list[int] = []
                hights: list[int] = []
                for i in range(1, len(row), 2):
                    if row[i] != "":
                        azimuths.append(int(row[i]))
                        hights.append(int(row[i+1]))
                self.__azimuth = azimuths
                self.__h_altitude = hights
                self.__id = row[0]
            else:
                self.__azimuth = [0, 180]
                self.__h_altitude = [0, 0]
                self.__id = 0
        else:
            self.__azimuth = [0, 180]
            self.__h_altitude = [0, 0]
            self.__id = 0

class AllHorizons:

    def __init__(self, horizons, horizons_key):
        self.__horizons = horizons
        self.__horizons_key = horizons_key


    def horizons(self):
        return self.__horizons

    def horizons_key(self):
        return self.__horizons_key

    def return_row(self, key_value, value):
        if key_value in self.__horizons_key:
            key_index = self.__horizons_key.index(key_value)
            if self.__horizons:
                for row in self.__horizons:
                    if row[key_index] == value:
                        return row
        row = []
        return row

    def edit_horizon(self,new_horizons):
        self.__horizons = new_horizons

    def delete_horizon(self, horizon_id):
        for i, horizon in enumerate(self.__horizons):
            if horizon[0] == horizon_id:
                del(self.__horizons[i])
                return

    def save_horizon(self):
        from step_application import root
        self.database = root.database
        self.places = self.database.places
        self.place = self.database.place
        self.horizon = self.database.horizon  # object import
        horizon = self.horizon.horizon_coordinate()
        row_index = -1
        id_list = []

        for line in self.__horizons:  # index list horizons
            id_list.append(line[0])
        if int(self.horizon.id) < 1:
            if id_list:
                id_list.sort()
                new_row = [str(int(id_list[-1]) + 1)]
            else:
                new_row = ["1"]
            self.horizon.set_id(int(new_row[0]))
            for i, place in enumerate(self.places.observers()):
                if str(place[0]) == str(self.place.id):
                    self.places.edit_horizon_id(i, new_row[0])
        else:
            row_index = id_list.index(str(self.horizon.id))
            new_row = [str(self.horizon.id)]

        for point in horizon:
            new_row.append(str(point[0]))
            new_row.append(str(point[1]))

        if row_index == -1:
            self.__horizons.append(new_row)
        else:
            self.__horizons[row_index] = new_row



