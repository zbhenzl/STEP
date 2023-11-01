class Instrument:

    def __init__(self, id_instrument, observer_id, telescope, d, f, mount, camera, sensor_w, sensor_h, pixel_w, pixel_h,
                 filter_set):

        self.__id = id_instrument
        self.__observer_id = observer_id
        self.__telescope = telescope
        self.__d = d
        self.__f = f
        self.__mount = mount
        self.__camera = camera
        self.__sensor_width = sensor_w
        self.__sensor_high = sensor_h
        self.__pixel_width = pixel_w
        self.__pixel_high = pixel_h
        self.__filter = filter_set

    def camera(self):
        return self.__camera

    def telescope(self):
        return self.__telescope

    def mount(self):
        return self.__mount

    def diameter(self):
        return self.__d

    def focus(self):
        return self.__f

    def sensor_w(self):
        return self.__sensor_width

    def sensor_h(self):
        return self.__sensor_high

    def pixel_width(self):
        return self.__pixel_width

    def pixel_high(self):
        return self.__pixel_high

    def filter(self):
        return self.__filter


    def change_camera(self, new):
        self.__camera = new

    def change_telescope(self, new):
        self.__telescope = new

    def change_mount(self, new):
        self.__mount = new

    def change_diameter(self, new):
        self.__d = new

    def change_focus(self, new):
        self.__f = new

    def change_sensor_w(self, new):
        self.__sensor_width = new

    def change_sensor_h(self, new):
        self.__sensor_high = new

    def change_pixel_width(self, new):
        self.__pixel_width = new

    def change_pixel_high(self, new):
        self.__pixel_high = new

    def change_filter(self, new):
        self.__filter = new

    def __str__(self):
        return self.__telescope + "+" + self.__mount + "+" + self.__camera + " filter " + self.__filter

    def edit_all(self, key_value, value, instruments):
        if instruments.instruments():
            row = instruments.return_row(key_value, value)
            if row:
                self.__id = row[0]
                self.__observer_id = row[1]
                self.__telescope = row[2]
                self.__d = row[3]
                self.__f = row[4]
                self.__mount = row[5]
                self.__camera = row[6]
                self.__sensor_width = row[7]
                self.__sensor_high = row[8]
                self.__pixel_width = row[9]
                self.__pixel_high = row[10]
                self.__filter = row[11]
            else:
                self.__id = 0
                self.__observer_id = 0
                self.__telescope = "add telescope"
                self.__d = 0
                self.__f = 0
                self.__mount = "mount"
                self.__camera = "camera"
                self.__sensor_width = 0
                self.__sensor_high = 0
                self.__pixel_width = 0
                self.__pixel_high = 0
                self.__filter = "No"
        else:
            self.__id = 0
            self.__observer_id = 0
            self.__telescope = "add telescope"
            self.__d = 0
            self.__f = 0
            self.__mount = "mount"
            self.__camera = "camera"
            self.__sensor_width = 0
            self.__sensor_high = 0
            self.__pixel_width = 0
            self.__pixel_high = 0
            self.__filter = "No"

    @property
    def id(self):
        return self.__id


class Instruments:

    def __init__(self, instruments, instruments_key):
        self.__instruments = instruments
        self.__instruments_key = instruments_key

    def instruments(self):
        return self.__instruments

    def instruments_key(self):
        return self.__instruments_key

    def return_row(self, key_value, value):
        if key_value in self.__instruments_key:
            key_index = self.__instruments_key.index(key_value)
            if self.__instruments:
                for row in self.__instruments:
                    if row[key_index] == value:
                        return row
        row = self.__instruments[0]
        return row

    def delete_instrument(self, instrument_id):
        from step_application import root
        for star in root.database.stars.stars:
            if instrument_id in star.instrument_list():
                new_list = star.instrument_list()
                new_list.remove(instrument_id)
                star.change_instrument_list(new_list)

                star.change_instrument_list(new_list)
        for i, instrument in enumerate(self.__instruments):
            if instrument[0] == instrument_id:
                del(self.__instruments[i])
                return

    def instrument_list(self, observer_id):
        instrument_list = []
        for instrument in self.__instruments:
            if str(observer_id) == str(instrument[1]):
                instrument_list.append(instrument[2] + " + " + instrument[5] + " + " + instrument[6])
        return instrument_list

    def add_instrument(self, observer_id, telescope, d, f, mount, camera, sensor_w, sensor_h, pixel_w, pixel_h,
                       filter_set):
        list_id = []
        for instrument in self.__instruments:
            list_id.append(int(instrument[0]))
        if list_id:
            list_id.sort()
            new_id = list_id[-1] + 1
        else:
            new_id = 1
        new_row = [str(new_id)]
        new_row.append(str(observer_id))
        new_row.append(str(telescope))
        new_row.append(str(d))
        new_row.append(str(f))
        new_row.append(str(mount))
        new_row.append(str(camera))
        new_row.append(str(sensor_w))
        new_row.append(str(sensor_h))
        new_row.append(str(pixel_w))
        new_row.append(str(pixel_h))
        new_row.append(str(filter_set))
        self.__instruments.append(new_row)

    def edit_instrument(self, instrument_id, telescope, d, f, mount, camera, sensor_w, sensor_h, pixel_w, pixel_h,
                       filter_set):
        for instrument in self.__instruments:
            if str(instrument[0]) == str(instrument_id):
                instrument[2] = str(telescope)
                instrument[3] = str(d)
                instrument[4] = str(f)
                instrument[5] = str(mount)
                instrument[6] = str(camera)
                instrument[7] = str(sensor_w)
                instrument[8] = str(sensor_h)
                instrument[9] = str(pixel_w)
                instrument[10] = str(pixel_h)
                instrument[11] = str(filter_set)


