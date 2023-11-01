import csv
import lightkurve as lk
import astropy.units as u
import statistics as st
from PyQt5 import QtWidgets, QtCore, QtGui
from coordinate import *
from astroquery.vizier import Vizier
from astropy.coordinates import Angle
import astropy.coordinates as coord
import os
import sys
import matplotlib
from step_main_form import Popup
import warnings
from astropy.utils.exceptions import AstropyWarning


class TessCutInfo:

    def __init__(self, lightcurves, coor, var_id, name, mag, period, epoch, tess_cut_set, sectors, x, y, mx, my, m, n,
                 cut_size, description, pair, name_origin):
        self.__lightcurves = lightcurves
        self.__detrend_parameter_list = [101, 301]
        self.__list_section = [0.05, 0.1, 0.25, 0.5, 1.1, 2, 5, 10, 50]
        self.__set_oversample_factor = 500
        self.__coor = coor
        self.__var_id = var_id
        self.__name = name
        self.__mag = mag
        self.__period = period
        self.__epoch = epoch
        self.__tess_cut_set = tess_cut_set
        self.__sectors = sectors
        self.__x = x
        self.__y = y
        self.__mx = mx
        self.__my = my
        self.__m = m
        self.__n = n
        self.__cut_size = cut_size
        self.__description = description
        self.__error_start = 0
        self.__error_end = 0
        self.__error_center = 0
        self.__data_focus = 1
        self.__delimiter_csv = ","
        self.__find_max_power_period = True
        self.__change_detrend_parameters = True
        self.__change_data_focus_by_period = True
        self.__interact = False
        self.__masks_disintegration = False
        self.__magnitude_limit = 18
        self.__mask = []
        self.__save_data = True
        self.__save_norm_data = True
        self.__save_detrend_data = True
        self.__save_pictures = True
        self.__percentage_of_erroneous_points = 0.1
        self.__show_pictures_data = True
        self.__show_pictures_detrend_data = False
        self.__show_pictures_data_faze = False
        self.__show_pictures_detrend_data_faze = True
        self.__show_all_lc_faze = False
        self.__show_all_lc_faze_detrend = True
        self.__set_detrend_border = 1
        self.__pair = pair
        self.__name_origin = name_origin

    def name_origin(self):
        return self.__name_origin

    def pair(self):
        return self.__pair

    def change_pair(self, new):
        self.__pair = new

    def lightcurves(self):
        return self.__lightcurves

    def change_lightcurves(self, new):
        self.__lightcurves = new

    def error_start(self):
        return self.__error_start

    def error_end(self):
        return self.__error_end

    def error_center(self):
        return self.__error_center

    def coor(self):
        return self.__coor

    def var_id(self):
        return self.__var_id

    def name(self):
        return self.__name

    def mag(self):
        return self.__mag

    def period(self):
        return self.__period

    def epoch(self):
        return self.__epoch

    def tess_cut_set(self):
        return self.__tess_cut_set

    def sectors(self):
        return self.__sectors

    def x(self):
        return self.__x

    def y(self):
        return self.__y

    def mx(self):
        return self.__mx

    def my(self):
        return self.__my

    def m(self):
        return self.__m

    def n(self):
        return self.__n

    def cut_size(self):
        return self.__cut_size

    def description(self):
        return self.__description

    def change_error_start(self, new):
        self.__error_start = new

    def change_error_end(self, new):
        self.__error_end = new

    def change_error_center(self, new):
        self.__error_center = new

    def change_coor(self, new):
        self.__coor = new

    def change_var_id(self, new):
        self.__var_id = new

    def change_name(self, new):
        self.__name = new

    def change_mag(self, new):
        self.__mag = new

    def change_period(self, new):
        self.__period = new

    def change_epoch(self, new):
        self.__epoch = new

    def change_tess_cut_set(self, new):
        self.__tess_cut_set = new

    def del_index_in_tess_cut_set(self, index):
        del(self.__tess_cut_set[index])

    def change_sectors(self, new):
        self.__sectors = new

    def change_x(self, new):
        self.__x = new

    def change_y(self, new):
        self.__y = new

    def change_mx(self, new):
        self.__mx = new

    def change_my(self, new):
        self.__my = new

    def change_m(self, new):
        self.__m = new

    def change_n(self, new):
        self.__n = new

    def change_cut_size(self, new):
        self.__cut_size = new

    def change_description(self, new):
        self.__description = new

    def change_show_pictures_data(self, new):
        self.__show_pictures_data = new

    def change_show_pictures_detrend_data(self, new):
        self.__show_pictures_detrend_data = new

    def change_show_pictures_data_faze(self, new):
        self.__show_pictures_data_faze = new

    def change_show_pictures_detrend_data_faze(self, new):
        self.__show_pictures_detrend_data_faze = new

    def change_show_all_lc_faze(self, new):
        self.__show_all_lc_faze = new

    def change_show_all_lc_faze_detrend(self, new):
        self.__show_all_lc_faze_detrend = new

    def change_set_detrend_border(self, new):
        self.__set_detrend_border = new

    def change_save_data(self, new):
        self.__save_data = new

    def change_save_norm_data(self, new):
        self.__save_norm_data = new

    def change_save_detrend_data(self, new):
        self.__save_detrend_data = new

    def change_save_pictures(self, new):
        self.__save_pictures = new

    def change_percentage_of_erroneous_points(self, new):
        self.__percentage_of_erroneous_points = new

    def change_change_detrend_parameters(self, new):
        self.__change_detrend_parameters = new

    def change_change_data_focus_by_period(self, new):
        self.__change_data_focus_by_period = new

    def change_interact(self, new):
        self.__interact = new

    def change_masks_disintegration(self, new):
        self.__masks_disintegration = new

    def change_magnitude_limit(self, new):
        self.__magnitude_limit = new

    def change_mask(self, new):
        self.__mask = new

    def change_find_max_power_period(self, new):
        self.__find_max_power_period = new

    def change_delimiter_csv(self, new):
        self.__delimiter_csv = new

    def change_data_focus(self, new):
        self.__data_focus = new

    def change_files_path(self, new):
        self.__files_path = new

    def change_graphs_path(self, new):
        self.__graphs_path = new

    def show_pictures_data(self):
        return self.__show_pictures_data

    def show_pictures_detrend_data(self):
        return self.__show_pictures_detrend_data

    def show_pictures_data_faze(self):
        return self.__show_pictures_data_faze

    def show_pictures_detrend_data_faze(self):
        return self.__show_pictures_detrend_data_faze

    def show_all_lc_faze(self):
        return self.__show_all_lc_faze

    def show_all_lc_faze_detrend(self):
        return self.__show_all_lc_faze_detrend

    def set_detrend_border(self):
        return self.__set_detrend_border

    def save_data(self):
        return self.__save_data

    def save_norm_data(self):
        return self.__save_norm_data

    def save_detrend_data(self):
        return self.__save_detrend_data

    def save_pictures(self):
        return self.__save_pictures

    def percentage_of_erroneous_points(self):
        return self.__percentage_of_erroneous_points

    def change_detrend_parameters(self):
        return self.__change_detrend_parameters

    def change_data_focus_by_period(self):
        return self.__change_data_focus_by_period

    def interact(self):
        return self.__interact

    def masks_disintegration(self):
        return self.__masks_disintegration

    def magnitude_limit(self):
        return self.__magnitude_limit

    def mask(self):
        return self.__mask

    def find_max_power_period(self):
        return self.__find_max_power_period

    def delimiter_csv(self):
        return self.__delimiter_csv

    def list_section(self):
        return self.__list_section

    def files_path(self):
        return self.__files_path

    def graphs_path(self):
        return self.__graphs_path

    def data_focus(self):
        return self.__data_focus

    def set_lc_parameters(self):
        from step_application import root
        self.tess_menu_window = root.tess_menu_window
        self.tess_menu_window_setting = root.tess_menu_window_setting
        self.change_show_pictures_data(self.tess_menu_window_setting.show_picture_origin_checkbox.isChecked())
        self.change_show_pictures_detrend_data(self.tess_menu_window_setting.show_picture_detrend_checkbox.isChecked())
        self.change_show_pictures_data_faze(self.tess_menu_window_setting.show_picture_faze_checkbox.isChecked())
        self.change_show_pictures_detrend_data_faze(
            self.tess_menu_window_setting.show_picture_detrend_faze_checkbox.isChecked())
        self.change_show_all_lc_faze(self.tess_menu_window_setting.show_picture_all_faze_checkbox.isChecked())
        self.change_show_all_lc_faze_detrend(self.tess_menu_window_setting.show_picture_all_detrend_faze_checkbox.isChecked())
        self.change_files_path(self.tess_menu_window_setting.folder_files_pushbutton.text())
        self.change_graphs_path(self.tess_menu_window_setting.folder_pictures_pushbutton.text)
        self.change_masks_disintegration(self.tess_menu_window_setting.show_mask_desintegration_checkbox.isChecked())
        self.change_data_focus(self.tess_menu_window_setting.data_focus_spinbox.value())
        self.change_change_data_focus_by_period(self.tess_menu_window_setting.change_focus_by_period.isChecked())
        self.change_find_max_power_period(self.tess_menu_window_setting.find_max_power_period_checkbox.isChecked())
        self.change_change_detrend_parameters(self.tess_menu_window_setting.change_detrend_parameters_by_period_checkbox.
                                              isChecked())

    def __save_converted(self, converted_file, convert_data, metadata=None):
        file1 = converted_file.replace(".csv", ".txt")
        try:
            if metadata:
                convert = open(file1, "w")
                convert.write(metadata + "\n")
                convert.close()
                convert = open(file1, "a")
                for k in range(len(convert_data)):
                    convert.write(
                        convert_data[k][0] + " " + convert_data[k][1] + " " + convert_data[k][2] + "\n")
                convert.close()
            else:
                convert = open(file1, "w")
                convert.write(convert_data[0][0] + " " + convert_data[0][1] + " " + convert_data[0][2] + "\n")
                convert.close()
                convert = open(file1, "a")
                for k in range(len(convert_data) - 1):
                    convert.write(
                        convert_data[k + 1][0] + " " + convert_data[k + 1][1] + " " + convert_data[k + 1][
                            2] + "\n")
                convert.close()
        except:
            mistake = Popup("Saving error",
                            "Failed to data file\nPlease check your permissions",
                            buttons="OK".split(","))
            mistake.do()

    def saving_error(self):
        mistake = Popup("Saving error",
                        "Failed to data file\nPlease check your permissions",
                        buttons="OK".split(","))
        mistake.do()

    def convert(self, converted_file, metadata=None):  # file(path to converted csv) , delimiter
        with open(converted_file) as data:
            file_contains = csv.reader(data, delimiter=self.__delimiter_csv)
            data = [row for row in file_contains]
        file_lens = len(data) - 1
        convert_data = []
        for line_number in range(file_lens):
            line = [data[line_number + 1][0], str(-float(data[line_number + 1][1])), data[line_number + 1][2]]
            convert_data.append(line)
        self.__save_converted(converted_file, convert_data, metadata=metadata)

    def norm(self, converted_file, metadata=None):  # file(path to converted csv) , delimiter
        with open(converted_file) as data:
            file_contains = csv.reader(data, delimiter=self.__delimiter_csv)
            data = [row for row in file_contains]
        flux = []
        for data_line in data:
            try:
                flux.append(float(data_line[1]))
            except:
                pass
        flux.sort(reverse=True)
        number_of_error_points = int(len(flux) * self.__percentage_of_erroneous_points / 100)
        file_lens = len(data) - 1
        convert_data = []
        for line_number in range(file_lens):
            line = [data[line_number + 1][0], str(-float(data[line_number + 1][1]) / flux[number_of_error_points]),
                    str(float(data[line_number + 1][2]) / flux[number_of_error_points])]
            convert_data.append(line)
        self.__save_converted(converted_file, convert_data, metadata=metadata)

    def save_all(self, origin=False, normalized=False, detrended=False, pictures=False, pictures_folder="",
                 file_folder="", graph_origin=False, graph_detrended=False, graph_faze=False, graph_faze_all=False,
                 graph_detrended_faze=False, graph_detrended_faze_all=False, part_info=[], pair_a=True,
                 percentage_of_erroneous_points=0.1, metadata=None, wl=101, p=2, b=5, n=3, s=3, saved_sector="all"):
        self.change_percentage_of_erroneous_points(percentage_of_erroneous_points)
        main_lc = self.__lightcurves[0][0]
        if wl == -1:
            w_test = 1
        else:
            w_test = 0
        for i, lightcurve in enumerate(self.__lightcurves):
            sector_number = lightcurve[3]
            if saved_sector == "all" or str(sector_number) == saved_sector:
                jd_start = lightcurve[1]
                jd_end = lightcurve[2]
                if w_test == 1:
                    wl = lightcurve[6]
                else:
                    from step_application import root
                    wl = int(root.tess_menu_window.window_length_combobox1.currentText())
                period = lightcurve[4]
                try:
                    epoch = float(self.__epoch) - 2457000
                except:
                    epoch = 2459000

                if origin and pair_a:
                    if metadata:
                        final_metadata = " HJD flux flux_err" + "\n" + metadata
                    else:
                        pass
                        final_metadata = ""  # HJD flux flux_err"
                    new_data_file = file_folder + "\\" + self.__name + "_" + str(sector_number) + "_TESS.csv"
                    lightcurve[0].to_csv(new_data_file, overwrite=True)
                    self.convert(new_data_file, metadata=final_metadata)

                if detrended and pair_a:
                    if metadata:
                        final_metadata = " HJD flux_detrended flux_err" + "\n" + metadata
                    else:
                        final_metadata = "" # HJD flux_detrended flux_err"
                    new_data_file = file_folder + "\\" + self.__name + "_" + str(sector_number) + "_TESS_flat.csv"
                    lightcurve[0].flatten(window_length=wl, polyorder=p, break_tolerance=b, niters=n, sigma=s).to_csv(
                        new_data_file, overwrite=True)
                    self.convert(new_data_file, metadata=final_metadata)

                if normalized and pair_a:
                    if metadata:
                        final_metadata = " HJD flux_normalized flux_err" + "\n" + metadata
                    else:
                        final_metadata = "" # HJD flux_normalized flux_err"
                    new_data_file = file_folder + "\\" + self.__name + "_" + str(sector_number) + "_TESS_NORM.csv"
                    lightcurve[0].to_csv(new_data_file, overwrite=True)
                    self.norm(new_data_file, metadata=final_metadata)

                if pictures:
                    if len(part_info) < 2 or len(lightcurve[0]) == 0:
                        lc_part_set = [lightcurve[0]]
                    else:
                        lc_part_set = []
                        lc_part_length = int(len(lightcurve[0]) / len(part_info))
                        if lc_part_length < 100:
                            lc_part_length = 100
                        start_of_part = 0
                        part = 1
                        while start_of_part < len(lightcurve[0]):
                            end_of_part = start_of_part + lc_part_length
                            if end_of_part + len(part_info) * 20 > len(lightcurve[0]):
                                end_of_part = len(lightcurve[0])
                            part_lc = lightcurve[0][start_of_part:end_of_part]
                            lc_part_set.append(part_lc)
                            start_of_part = end_of_part
                            part = part + 1
                    for j, part_lc in enumerate(lc_part_set):
                        if graph_origin and pair_a:
                            ax = part_lc.plot(ylabel=self.__coor + "\nJD:" + str(jd_start) + "-" + str(jd_end),
                                              xlabel="Data sector " + str(sector_number) + "_" + str(j+1) + "/" +
                                                     str(len(lc_part_set)))
                            ax.set_title(self.__description)
                            file_picture = pictures_folder + "\\" + self.__name + "_" + str(
                                sector_number) + "_" + str(j) + ".png"
                            try:
                                ax.figure.savefig(file_picture)
                            except:
                                self.saving_error()
                            matplotlib.pyplot.close()
                        if graph_detrended and pair_a:
                            ax1 = part_lc.flatten(window_length=wl, polyorder=p, break_tolerance=b, niters=n, sigma=s).\
                                plot(ylabel=self.__coor + "\nJD:" + str(jd_start) + "-" + str(jd_end),
                                     xlabel="Detrended data sector " + str(
                                         sector_number) + "_" + str(j+1) + "/" + str(len(lc_part_set)))
                            ax1.set_title(self.__description)
                            file_picture = pictures_folder + "\\" + self.__name + "_" + str(
                                sector_number) + "_" + str(j) + "_flat.png"
                            try:
                                ax1.figure.savefig(file_picture)
                            except:
                                self.saving_error()
                            matplotlib.pyplot.close()
                    if graph_faze and period:
                        ax2 = lightcurve[0].fold(period, epoch_time=epoch - 2457000, normalize_phase=True).scatter(
                            xlabel="Phased data sector " + str(sector_number))
                        ax2.set_title(self.__description + " pair " + self.__pair)
                        file_picture = pictures_folder + "\\" + self.__name + "_" + self.__pair + "_" + str(
                            sector_number) + "_" + str(i) + "_faze.png"
                        try:
                            ax2.figure.savefig(file_picture)
                        except:
                            self.saving_error()
                        matplotlib.pyplot.close()
                    if graph_detrended_faze and period:
                        ax3 = lightcurve[0].flatten(window_length=wl, polyorder=p, break_tolerance=b, niters=n, sigma=s).fold(
                            period, epoch_time=epoch - 2457000, normalize_phase=True).scatter(
                            xlabel="Phased and detrended data sector " + str(sector_number))
                        ax3.set_title(self.__description + " pair " + self.__pair)
                        file_picture = pictures_folder + "\\" + self.__name + "_" + self.__pair + "_" + str(
                            sector_number) + "_" + str(i) + "_flat_faze.png"
                        try:
                            ax3.figure.savefig(file_picture)
                        except:
                            self.saving_error()
                        matplotlib.pyplot.close()
                matplotlib.pyplot.close(1)
                if i > 0:
                    main_lc = main_lc.append(lightcurve[0])
        if graph_faze_all and saved_sector == "all":
            ax4 = main_lc.fold(self.__lightcurves[0][4],
                               epoch_time=epoch - 2457000,
                               normalize_phase=True).scatter(xlabel="Fazed data all sectors pair " + self.__pair)
            file_picture = pictures_folder + "\\" + self.__name + "_" + self.__pair + "_all_sectors.png"
            ax4.set_title(self.__description + " pair " + self.__pair)
            try:
                ax4.figure.savefig(file_picture)
            except:
                self.saving_error()
            matplotlib.pyplot.close()
        if graph_detrended_faze_all and saved_sector == "all":
            ax5 = main_lc.flatten(
                window_length=wl, polyorder=p, break_tolerance=b, niters=n, sigma=s).fold(self.__lightcurves[0][4],
                                                             epoch_time=epoch - 2457000, normalize_phase=True).scatter(
                xlabel="Fazed detrended data all sectors pair " + self.__pair)
            file_picture = pictures_folder + "\\" + self.__name + "_" + self.__pair + "_all_detrended sectors.png"
            ax5.set_title(self.__description + " pair " + self.__pair)
            try:
                ax5.figure.savefig(file_picture)
            except:
                self.saving_error()
            matplotlib.pyplot.close()

    def find_period(self, light_curve):
        pg = light_curve.flatten(window_length=self.__detrend_parameter_list[0]).to_periodogram(
            minimum_period=self.__list_section[0] * u.day, maximum_period=self.__list_section[1] * u.day,
            oversample_factor=self.__set_oversample_factor)
        for section_number in range(1, len(self.__list_section) - 1):
            new_pg = light_curve.flatten(window_length=self.__detrend_parameter_list[0]).to_periodogram(
                minimum_period=self.__list_section[section_number] * u.day,
                maximum_period=self.__list_section[section_number + 1] * u.day,
                oversample_factor=self.__set_oversample_factor)
            if max(pg.power) < max(new_pg.power):
                pg = new_pg
        local_period = pg.period_at_max_power
        return local_period

    def delete_error(self, changed_lc):
        length = len(changed_lc)
        start = int(length * self.__error_start / 100)
        end = int(length * self.__error_end / 100)
        center = int(length * self.__error_center / 100)
        try:
            del (changed_lc[0:start])
            length = len(changed_lc)
            del (changed_lc[length - end:length])
            length = len(changed_lc)
            str_min = int(length / 2 - center / 2)
            str_max = int(length / 2 + center / 2)
            del (changed_lc[str_min:str_max])
        except:
            pass
        return changed_lc

    def set_detrend_parameter(self, local_period):
        if local_period < self.__set_detrend_border:
            detrend_parameter = self.__detrend_parameter_list[0]
        else:
            detrend_parameter = self.__detrend_parameter_list[1]
        return detrend_parameter

    def give_lightcurve(self, sector_order, lightcurve_type="standard", pixel_x=None, pixel_y=None, mask=[]):
        jd_start = int((self.__tess_cut_set[sector_order].meta["BJDREFI"] +
                        self.__tess_cut_set[sector_order].meta["TSTART"]) * 100) / 100
        jd_end = int((self.__tess_cut_set[sector_order].meta["BJDREFI"] +
                      self.__tess_cut_set[sector_order].meta["TSTOP"]) * 100) / 100
        sector_number = self.__tess_cut_set[sector_order].meta["SECTOR"]
        target_mask = self.__tess_cut_set[sector_order].create_threshold_mask(threshold=150, reference_pixel='center')
        bg_mask = ~self.__tess_cut_set[sector_order].create_threshold_mask(threshold=0.001, reference_pixel=None)
        target_mask[0:self.__cut_size, 0:self.__cut_size] = 0
        if lightcurve_type == "standard":
            if not mask:
                target_mask[self.__x:self.__x + self.__mx, self.__y:self.__y + self.__my] = 1
            else:
                for mask_point in mask:
                    target_mask[mask_point[0], mask_point[1]] = 1
        else:
            target_mask[pixel_x, pixel_y] = 1
        corr_lc_with_err = self.__tess_cut_set[sector_order].to_lightcurve(
            aperture_mask=target_mask) - ((self.__tess_cut_set[sector_order].to_lightcurve(aperture_mask=bg_mask) /
                                           bg_mask.sum()) * target_mask.sum())
        corr_lc = corr_lc_with_err.remove_nans()
        if len(corr_lc) > 0:
            corr_lc = self.delete_error(corr_lc)
            corr_lc.time = corr_lc.time + self.__tess_cut_set[sector_order].get_keyword(
                'BJDREFI') * u.day + self.__tess_cut_set[sector_order].get_keyword('BJDREFF') * u.day
            if lightcurve_type == "standard":
                if self.__period:
                    try:
                        period = float(self.__period)
                    except:
                        period = self.find_period(corr_lc).value
                else:
                    period = self.find_period(corr_lc).value
                if self.__change_detrend_parameters and period:
                    w = self.set_detrend_parameter(period)
                else:
                    w = self.__detrend_parameter_list[0]
                return [corr_lc, jd_start, jd_end, sector_number, period, target_mask, w]
            else:
                return corr_lc
        else:
            return None

    def flux_to_mag(self, jd_star, jd_end, sector_index, third_light, offset, detrend=False, window_length=101,
                    polyorder=2, return_trend=False, break_tolerance=5, niters=3, sigma=3, mask=None,
                    forbidden_time_list=[], quick_display_point=None):
        lightcurve = self.__lightcurves[sector_index][0].remove_nans()
        lightcurve_time_with_errors = lightcurve.time.value
        if detrend:
            lightcurve_detrend_trend_list = lightcurve.flatten(window_length=window_length, polyorder=polyorder,
                                                               return_trend=return_trend,
                                                               break_tolerance=break_tolerance,
                                                               niters=niters, sigma=sigma, mask=mask)
            lightcurve_flux_with_errors = lightcurve_detrend_trend_list[0].flux.value
            lightcurve_flux_err_with_errors = lightcurve_detrend_trend_list[0].flux_err.value
            lightcurve_trend_with_errors = lightcurve_detrend_trend_list[1].flux.value
        else:
            third_light = third_light * 1000
            lightcurve_flux_with_errors = lightcurve.flux.value
            lightcurve_flux_err_with_errors = lightcurve.flux_err.value
            lightcurve_trend_with_errors = [0] * len(lightcurve_flux_with_errors)

        lightcurve_time = []
        lightcurve_flux = []
        lightcurve_flux_err = []
        lightcurve_trend = []
        if quick_display_point:
            quick_display_coefficient = ceil(len(lightcurve_time_with_errors) / quick_display_point)
        else:
            quick_display_coefficient = 1
        for i in range(0, len(lightcurve_time_with_errors), quick_display_coefficient):
            point_jd = lightcurve_time_with_errors[i]
            add_point = True
            if point_jd < jd_star or point_jd > jd_end:
                add_point = False
            else:
                for j in range(0, len(forbidden_time_list), 2):
                    if forbidden_time_list[j] < point_jd < forbidden_time_list[j+1]:
                        add_point = False
            if add_point:
                lightcurve_time.append(point_jd)
                lightcurve_flux.append(lightcurve_flux_with_errors[i])
                lightcurve_trend.append(lightcurve_trend_with_errors[i])
                lightcurve_flux_err.append(lightcurve_flux_err_with_errors[i])
        if lightcurve_flux:
            max_flux = max(lightcurve_flux)
            min_flux = min(lightcurve_flux)
            if min_flux < -third_light/1000:
                third_light = -min_flux + 1/1000
        lightcurve_mag = []
        lightcurve_err_mag = []
        lightcurve_trend_mag = []
        for i, flux in enumerate(lightcurve_flux):
            if flux + third_light/1000 <= 0:
                third_light = - flux * 1000 + 0.00001
            mag = -2.5 * log((flux + third_light/1000) / (max_flux + third_light/1000), 10) + offset
            lightcurve_mag.append(mag)
            err = lightcurve_flux_err[i] / (max_flux + third_light/1000)
            lightcurve_err_mag.append(err)
            if detrend:
                trend_min = min(lightcurve_trend)
                trend_max = max(lightcurve_trend)
                if trend_min < 0:
                    for trend in lightcurve_trend:
                        trend = trend - trend_min + (trend_max - trend_min) / 10
                trend_max = max(lightcurve_trend)
                trend = lightcurve_trend[i] / trend_max
            else:
                trend = 0
            lightcurve_trend_mag.append(trend)
        return [lightcurve_time, lightcurve_mag, lightcurve_err_mag, lightcurve_trend_mag]

    def delete_point(self, sector_number, lightcurve_time, lightcurve_mag,  jd_start, mag_min, jd_end, mag_max):
        if str(sector_number) in self.__sectors:
            sector_index = self.__sectors.index(str(sector_number))
        else:
            sector_index = None
        if sector_index:
            for i, point_time in enumerate(lightcurve_time):
                if jd_start <= point_time <= jd_end and mag_min <= lightcurve_mag[i] <= mag_max:
                    row = self.__lightcurves[sector_index][0][i]
                    del(self.__lightcurves[sector_index][0][i])

    def give_system_models(self, variables):
        return variables.choice_by_name(self.__name_origin)

