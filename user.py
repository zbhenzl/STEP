

class User:

    def __init__(self,
                 id: int,
                 name: str,
                 authorizations="User",
                 prediction_select_column_setup=["1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1"],
                 prediction_sort_column_setup="Name",
                 prediction_visibility_setup=["1", "1", "0"],
                 prediction_lightcurve_setup=["1", "1", "1", "1", "1", "1"],
                 object_filtered_by_setup=["1", "0", "0", "0", "0", "0", "0", "0", "0", "0"],
                 coordinate_setup=["0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0"],
                 object_sort_by_setup=["1", "0", "0", "0", "0", "0"],
                 time_extension_setup=["1", "1"],
                 texts_filter_setup_name_key1="",
                 texts_filter_setup_name_key2="",
                 texts_filter_setup_type_key1="",
                 texts_filter_setup_type_key2="",
                 texts_filter_setup_type_key3="",
                 texts_filter_setup_type_key4="",
                 texts_filter_setup_mag_start="0",
                 texts_filter_setup_mag_end="0",
                 texts_filter_setup_note_key1="",
                 texts_filter_setup_note_key2="",
                 texts_filter_setup_note_key3="and",
                 photometry_setting=["", "", "", "0", "0", "0.1", "", "18", "1", "default", "0", "1", "1", "0", "0",
                                     "0", True, True, False, False, False, True, True, True, True, True, True, True,
                                     True, False, True, False, False, False, False, True, True, True, True, True, True,
                                     True],
                 silicups_file_path="",
                 model_path=""):
        self.__id = id
        self.__name = name
        self.__authorizations = authorizations
        self.__posibble_authorization = ["User", "Administrator"]
        self.__prediction_select_column_setup = prediction_select_column_setup
        self.__prediction_sort_column_setup = prediction_sort_column_setup
        self.__prediction_visibility_setup = prediction_visibility_setup
        self.__prediction_lightcurve_setup = prediction_lightcurve_setup
        self.__object_filtered_by_setup = object_filtered_by_setup
        self.__coordinate_setup = coordinate_setup
        self.__object_sort_by_setup = object_sort_by_setup
        self.__time_extension_setup = time_extension_setup
        self.__texts_filter_setup_name_key1 = texts_filter_setup_name_key1
        self.__texts_filter_setup_name_key2 = texts_filter_setup_name_key2
        self.__texts_filter_setup_type_key1 = texts_filter_setup_type_key1
        self.__texts_filter_setup_type_key2 = texts_filter_setup_type_key2
        self.__texts_filter_setup_type_key3 = texts_filter_setup_type_key3
        self.__texts_filter_setup_type_key4 = texts_filter_setup_type_key4
        self.__texts_filter_setup_mag_start = texts_filter_setup_mag_start
        self.__texts_filter_setup_mag_end = texts_filter_setup_mag_end
        self.__texts_filter_setup_note_key1 = texts_filter_setup_note_key1
        self.__texts_filter_setup_note_key2 = texts_filter_setup_note_key2
        self.__texts_filter_setup_note_key3 = texts_filter_setup_note_key3
        self.__photometry_setting = photometry_setting
        self.__silicups_file_path = silicups_file_path
        self.__model_path = model_path

    def model_path(self):
        return self.__model_path

    def change_model_path(self, new):
        self.__model_path = new

    def silicups_file_path(self):
        return self.__silicups_file_path

    def change_silicups_file_path(self,new):
        self.__silicups_file_path = new

    def __str__(self):
        return self.__name

    @property
    def id(self):
        return self.__id

    def edit_authorizations(self, new_authorizations):
        if new_authorizations in self.__posibble_authorization:
            self.__authorizations = new_authorizations
        else:
            self.__authorizations = "User"

    @property
    def authorizations(self):
        return self.__authorizations

    def name(self):
        return self.__name

    def photometry_setting(self):
        return self.__photometry_setting

    def change_photometry_setting(self, new):
        self.__photometry_setting = new

    def edit_name(self, name):
        self.__name = name

    def edit_id(self, new_id):
        self.__id = new_id

    def __basic_environment_setting(self):
        self.__prediction_select_column_setup = ["1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1",
                                                 "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1", "1"]
        self.__prediction_sort_column_setup = "Name"
        self.__prediction_visibility_setup = ["1", "1", "0"]
        self.__prediction_lightcurve_setup = []
        self.__object_filtered_by_setup = ["1", "0", "0", "0", "0", "0", "0", "0", "0", "0"]
        self.__coordinate_setup = ["0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0"]
        self.__object_sort_by_setup = ["1", "0", "0", "0", "0", "0"]
        self.__time_extension_setup = ["1", "1"]
        self.__texts_filter_setup_name_key1 = ""
        self.__texts_filter_setup_name_key2 = ""
        self.__texts_filter_setup_type_key1 = ""
        self.__texts_filter_setup_type_key2 = ""
        self.__texts_filter_setup_type_key3 = ""
        self.__texts_filter_setup_type_key4 = ""
        self.__texts_filter_setup_mag_start = "0"
        self.__texts_filter_setup_mag_end = "0"
        self.__texts_filter_setup_note_key1 = ""
        self.__texts_filter_setup_note_key2 = ""
        self.__texts_filter_setup_note_key3 = "and"
        self.__photometry_setting = ["", "", "", "0", "0", "0.1", "", "18", "1", "default", "0", "1", "1", "0",
                                     "0", "0", "1", "1", "0", "0", "0", "1", "1", "1", "1", "1", "1", "1", "1",
                                     "0", "1", "0", "0", "0", "0", "1", "1", "1", "1", "1", "1", "1"]
        self.__silicups_file_path = ""
        self.__model_path = ""

    def edit_all(self, key_value, value, users):
        if users.users():
            row = users.return_row(key_value, value)
            if row:
                self.edit_name(row[1])
                self.edit_id(row[0])
                self.edit_authorizations(row[2])
                try:
                    self.__prediction_select_column_setup = row[3].strip().split(",")
                    self.__prediction_sort_column_setup = row[4]
                    self.__prediction_visibility_setup = row[5].strip().split(",")
                    self.__prediction_lightcurve_setup = row[6].strip().split(",")
                    self.__object_filtered_by_setup = row[7].strip().split(",")
                    self.__coordinate_setup = row[8].strip().split(",")
                    self.__object_sort_by_setup = row[9].strip().split(",")
                    self.__time_extension_setup = row[10].strip().split(",")
                    self.__texts_filter_setup_name_key1 = row[11]
                    self.__texts_filter_setup_name_key2 = row[12]
                    self.__texts_filter_setup_type_key1 = row[13]
                    self.__texts_filter_setup_type_key2 = row[14]
                    self.__texts_filter_setup_type_key3 = row[15]
                    self.__texts_filter_setup_type_key4 = row[16]
                    self.__texts_filter_setup_mag_start = row[17]
                    self.__texts_filter_setup_mag_end = row[18]
                    self.__texts_filter_setup_note_key1 = row[19]
                    self.__texts_filter_setup_note_key2 = row[20]
                    self.__texts_filter_setup_note_key3 = row[21]
                    self.__photometry_setting = row[22].split(",")
                    self.__silicups_file_path = row[23]
                    self.__model_path = row[24]
                except:
                    self.__basic_environment_setting()

            else:
                self.edit_name(0)
                self.edit_id("add user")
                self.edit_authorizations("User")

        else:
            self.edit_name(0)
            self.edit_id("add user")
            self.edit_authorizations("User")
            self.__basic_environment_setting()

    def texts_filter_setup_name_key1(self):
        return self.__texts_filter_setup_name_key1

    def texts_filter_setup_name_key2(self):
        return self.__texts_filter_setup_name_key2
    def texts_filter_setup_type_key1(self):
        return self.__texts_filter_setup_type_key1

    def texts_filter_setup_type_key2(self):
        return self.__texts_filter_setup_type_key2

    def texts_filter_setup_type_key3(self):
        return self.__texts_filter_setup_type_key3

    def texts_filter_setup_type_key4(self):
        return self.__texts_filter_setup_type_key4

    def texts_filter_setup_mag_start(self):
        return self.__texts_filter_setup_mag_start

    def texts_filter_setup_mag_end(self):
        return self.__texts_filter_setup_mag_end

    def texts_filter_setup_note_key1(self):
        return self.__texts_filter_setup_note_key1

    def texts_filter_setup_note_key2(self):
        return self.__texts_filter_setup_note_key2

    def texts_filter_setup_note_key3(self):
        return self.__texts_filter_setup_note_key3

    def prediction_select_column_setup(self):
        return self.__prediction_select_column_setup

    def prediction_sort_column_setup(self):
        return self.__prediction_sort_column_setup

    def prediction_visibility_setup(self):
        return self.__prediction_visibility_setup

    def prediction_lightcurve_setup(self):
        return self.__prediction_lightcurve_setup

    def object_filtered_by_setup(self):
        return self.__object_filtered_by_setup

    def coordinate_setup(self):
        return self.__coordinate_setup

    def object_sort_by_setup(self):
        return self.__object_sort_by_setup

    def time_extension_setup(self):
        return self.__time_extension_setup

    def edit_environment(self,
                         prediction_select_column_setup,
                         prediction_sort_column_setup,
                         prediction_visibility_setup,
                         object_filtered_by_setup,
                         coordinate_setup,
                         object_sort_by_setup,
                         time_extension_setup,
                         texts_filter_setup_name_key1,
                         texts_filter_setup_name_key2,
                         texts_filter_setup_type_key1,
                         texts_filter_setup_type_key2,
                         texts_filter_setup_type_key3,
                         texts_filter_setup_type_key4,
                         texts_filter_setup_mag_start,
                         texts_filter_setup_mag_end,
                         texts_filter_setup_note_key1,
                         texts_filter_setup_note_key2,
                         texts_filter_setup_note_key3
                         ):
        if prediction_select_column_setup:
            self.__prediction_select_column_setup = prediction_select_column_setup
        if prediction_sort_column_setup:
            self.__prediction_sort_column_setup = prediction_sort_column_setup
        if prediction_visibility_setup:
            self.__prediction_visibility_setup = prediction_visibility_setup
        if object_filtered_by_setup:
            self.__object_filtered_by_setup = object_filtered_by_setup
        if coordinate_setup:
            self.__coordinate_setup = coordinate_setup
        if object_sort_by_setup:
            self.__object_sort_by_setup = object_sort_by_setup
        if time_extension_setup:
            self.__time_extension_setup = time_extension_setup
        self.__texts_filter_setup_name_key1 = texts_filter_setup_name_key1
        self.__texts_filter_setup_name_key2 = texts_filter_setup_name_key2
        self.__texts_filter_setup_type_key1 = texts_filter_setup_type_key1
        self.__texts_filter_setup_type_key2 = texts_filter_setup_type_key2
        self.__texts_filter_setup_type_key3 = texts_filter_setup_type_key3
        self.__texts_filter_setup_type_key4 = texts_filter_setup_type_key4
        self.__texts_filter_setup_mag_start = texts_filter_setup_mag_start
        self.__texts_filter_setup_mag_end = texts_filter_setup_mag_end
        self.__texts_filter_setup_note_key1 = texts_filter_setup_note_key1
        self.__texts_filter_setup_note_key2 = texts_filter_setup_note_key2
        self.__texts_filter_setup_note_key3 = texts_filter_setup_note_key3


class Users:

    def __init__(self, users, users_key):
        self.__users = users
        self.__users_key = users_key

    def users(self):
        return self.__users

    def users_key(self):
        return self.__users_key

    def return_row(self, key_value, value):
        if key_value in self.__users_key:
            key_index = self.__users_key.index(key_value)
            if self.__users:
                for row in self.__users:
                    if row[key_index] == value:
                        return row
        row = self.__users[0]
        return row

    def edit_environments(self, user):
        for i, row in enumerate(self.__users):
            if row[0] == user.id:
                try:
                    self.__users[i][3] = ",".join(user.prediction_select_column_setup())
                except:
                    self.__users[i].append(",".join(user.prediction_select_column_setup()))
                try:
                    self.__users[i][4] = user.prediction_sort_column_setup()
                except:
                    self.__users[i].append(user.prediction_sort_column_setup())
                try:
                    self.__users[i][5] = ",".join(user.prediction_visibility_setup())
                except:
                    self.__users[i].append(",".join(user.prediction_visibility_setup()))
                try:
                    self.__users[i][6] = ",".join(user.prediction_lightcurve_setup())
                except:
                    self.__users[i].append(",".join(user.prediction_lightcurve_setup()))
                try:
                    self.__users[i][7] = ",".join(user.object_filtered_by_setup())
                except:
                    self.__users[i].append(",".join(user.object_filtered_by_setup()))
                try:
                    self.__users[i][8] = ",".join(user.coordinate_setup())
                except:
                    self.__users[i].append(",".join(user.coordinate_setup()))
                try:
                    self.__users[i][9] = ",".join(user.object_sort_by_setup())
                except:
                    self.__users[i].append(",".join(user.object_sort_by_setup()))
                try:
                    self.__users[i][10] = ",".join(user.time_extension_setup())
                except:
                    self.__users[i].append(",".join(user.time_extension_setup()))
                try:
                    self.__users[i][11] = user.texts_filter_setup_name_key1()
                except:
                    self.__users[i].append(user.texts_filter_setup_name_key1())
                try:
                    self.__users[i][12] = user.texts_filter_setup_name_key2()
                except:
                    self.__users[i].append(user.texts_filter_setup_name_key2())
                try:
                    self.__users[i][13] = user.texts_filter_setup_type_key1()
                except:
                    self.__users[i].append(user.texts_filter_setup_type_key1())
                try:
                    self.__users[i][14] = user.texts_filter_setup_type_key2()
                except:
                    self.__users[i].append(user.texts_filter_setup_type_key2())
                try:
                    self.__users[i][15] = user.texts_filter_setup_type_key3()
                except:
                    self.__users[i].append(user.texts_filter_setup_type_key3())
                try:
                    self.__users[i][16] = user.texts_filter_setup_type_key4()
                except:
                    self.__users[i].append(user.texts_filter_setup_type_key4())
                try:
                    self.__users[i][17] = user.texts_filter_setup_mag_start()
                except:
                    self.__users[i].append(user.texts_filter_setup_mag_start())
                try:
                    self.__users[i][18] = user.texts_filter_setup_mag_end()
                except:
                    self.__users[i].append(user.texts_filter_setup_mag_end())
                try:
                    self.__users[i][19] = user.texts_filter_setup_note_key1()
                except:
                    self.__users[i].append(user.texts_filter_setup_note_key1())
                try:
                    self.__users[i][20] = user.texts_filter_setup_note_key2()
                except:
                    self.__users[i].append(user.texts_filter_setup_note_key2())
                try:
                    self.__users[i][21] = user.texts_filter_setup_note_key3()
                except:
                    self.__users[i].append(user.texts_filter_setup_note_key3())
                try:
                    self.__users[i][22] = ",".join(user.photometry_setting())
                except:
                    self.__users[i].append(",".join(user.photometry_setting()))
                try:
                    self.__users[i][23] = user.silicups_file_path()
                except:
                    self.__users[i].append(user.silicups_file_path())
                try:
                    self.__users[i][24] = user.model_path()
                except:
                    self.__users[i].append(user.model_path())

    def delete_user(self, user_name):
        from step_application import root
        for star in root.database.stars.stars:
            if user_name in star.user_list():
                new_list = star.user_list()
                new_list.remove(user_name)
                star.change_user_list(new_list)
        for i, user in enumerate(self.__users):
            if user[1] == user_name:
                del(self.__users[i])
                return

    def add_user(self, user_name, authorization):
        list_id = []
        for user in self.__users:
            list_id.append(int(user[0]))
        if list_id:
            list_id.sort()
            new_id = list_id[-1] + 1
        else:
            new_id = 1
        new_row = [str(new_id), str(user_name), str(authorization)]
        self.__users.append(new_row)

    def rename_user(self, new_name, last_name):
        for user in self.__users:
            if user[1] == last_name:
                user[1] = new_name

    def return_user_list(self):
        user_list = []
        for user in self.__users:
            user_list.append(user[1])
        return user_list
