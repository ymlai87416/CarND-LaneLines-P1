import traceback
from string import Template
from app.setting import Setting
import os
import logging
import sys

from app.process import process_video

def parseListTuple3(sInput):
    tokens = sInput.split(';')
    return list(map(lambda x: parseTupleI3(x.strip()), tokens))

def parseListOfPoint(sInput):
    tokens = sInput.split(';')
    return list(map(lambda x: parseTupleI2(x.strip()), tokens))

def parseTupleI3(sInput):
    tokens = sInput.split(',')
    return int(tokens[0]), int(tokens[1]), int(tokens[2])

def parseTupleI2(sInput):
    tokens = sInput.split(',')
    return int(tokens[0]), int(tokens[1])

def formatListTuple(lstInput):
    result = []
    for tuple in lstInput:
        tempstr = list(map(lambda x: str(x), tuple))
        temp = ", ".join(tempstr)
        result.append(temp)
    return "; ".join(result)

class Application:
    instance = None

    def __new__(cls):  # __new__ always a classmethod
        if not Application.instance:
            Application.instance = Application.__ApplicationInner()
        return Application.instance

    def __getattr__(self, name):
        return getattr(self.instance, name)

    def __setattr__(self, name):
        return setattr(self.instance, name)

    class __ApplicationInner:
        outputDir = r'test_videos_output/'

        configFile = r'setting.conf'

        template = '''; color filtering
; color_filter is either 'off' or 'hsv'
; color_filter_hsv_low and color_filter_hsv_high can take multiple filter and add them with or operation

color_filter = $str_color_filter
color_filter_hsv_low = $str_color_filter_hsv_low
color_filter_hsv_high = $str_color_filter_hsv_high

; gray scale
; gray_scale is either 'gray' or 'yuv'

gray_scale = $str_gray_scale

; Guassian
; guassian_kernel_size = odd number

guassian_kernel_size = $str_guassian_kernel_size

; Canny
; canny is either 'canny' or 'canny-ostu'
; canny_low_threshold is between 0 to 255
; canny_high_threshold is between 0 to 255
; canny_ostu_threshold is between 0 to 1

canny = $str_canny
canny_low_threshold = $str_canny_low_threshold
canny_high_threshold = $str_canny_high_threshold
canny_ostu_threshold = $str_canny_ostu_threshold

; Hough
; hough_rho: any integer
; hough_theta: any integer
; hough_vote_threshold: any integer
; hough_min_line: any integer
; hough_line_gap: any integer

hough_rho = $str_hough_rho
hough_theta = $str_hough_theta
hough_vote_threshold = $str_hough_vote_threshold
hough_min_line = $str_hough_min_line
hough_line_gap = $str_hough_line_gap

; region of interest
; a list of point from 0 - 100 of width or height
region_of_interest = $str_region_of_interest

; averaging line and smoothing
unwanted_slope = $str_unwanted_slope
prev_frame_weight = $str_prev_frame_weight

; final_output
; final_output can be either 'normal', 'color_filter', 'gray_scale', 'canny', 'hough', 'average'
final_output = $str_final_output'''

        def __init__(self):
            self.setting = Setting()
            settingToBe = self.readConfig()
            if settingToBe != None:
                self.setting = settingToBe

            self.logger = logging.getLogger("CarND-LaneLines-P1")
            self.logger.setLevel(logging.INFO)
            handler = logging.FileHandler('application.log')
            handler.setLevel(logging.INFO)
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)

            # redirect stdout
            sys.stdout = open('stdout.log', 'w')
            sys.stderr = open('stderr.log', 'w')

        @property
        def logger(self):
            return self.__logger

        @logger.setter
        def logger(self, logger):
            self.__logger = logger

        @property
        def setting(self):
            return self.__setting

        @setting.setter
        def setting(self, setting):
            if not (type(setting) is Setting):
                raise ValueError("must provide a Setting object")
            self.__setting = setting

        def readConfig(self):
            setting = Setting()
            file = open(self.configFile, "r")
            for line in file:
                if line.startswith(";"):
                    continue
                tokens = line.split("=");

                if(len(tokens) != 2):
                    continue;
                key, value = tokens
                key = key.strip()
                value = value.strip()

                try:
                    if key == 'color_filter':
                        setting.color_filter = value.lower()
                    elif key == 'color_filter':
                        setting.color_filter_hsv_low = parseListTuple3(value)
                    elif key == 'color_filter_hsv_high':
                        setting.color_filter_hsv_high = parseListTuple3(value)
                    elif key == 'gray_scale':
                        setting.gray_scale = value.lower()
                    elif key == 'guassian_kernel_size':
                        setting.guassian_kernel_size = int(value)
                    elif key == 'canny':
                        setting.canny = value.lower()
                    elif key == 'canny_low_threshold':
                        setting.canny_low_threshold = int(value)
                    elif key == 'canny_high_threshold':
                        setting.canny_high_threshold = int(value)
                    elif key == 'canny_ostu_threshold':
                        setting.canny_ostu_threshold = float(value)
                    elif key == 'hough_rho':
                        setting.hough_rho = int(value)
                    elif key == 'hough_theta':
                        setting.hough_theta = int(value)
                    elif key == 'hough_vote_threshold':
                        setting.hough_vote_threshold = int(value)
                    elif key == 'hough_min_line':
                        setting.hough_min_line_length = int(value)
                    elif key == 'hough_line_gap':
                        setting.hough_max_line_gap = int(value)
                    elif key == 'region_of_interest':
                        setting.region_of_interest = parseListOfPoint(value)
                    elif key == 'unwanted_slope':
                        setting.unwanted_slope = float(value)
                    elif key == 'prev_frame_weight':
                        setting.prev_frame_weight = float(value)
                    elif key == 'final_output':
                        setting.final_output = value.lower()
                except Exception as ex:
                    print("Error occurred", ex)
                    traceback.print_exc()
                    self.logger.error("Error occurred when parsing configuration file", exc_info=True)
                    return None

            file.close()
            return setting

        def writeConfig(self):
            s = Template(self.template)
            output = s.substitute(str_color_filter = self.setting.color_filter, str_color_filter_hsv_low = formatListTuple(self.setting.color_filter_hsv_low),
                         str_color_filter_hsv_high = formatListTuple(self.setting.color_filter_hsv_high), str_canny = self.setting.canny,
                         str_gray_scale = self.setting.gray_scale, str_guassian_kernel_size = str(self.setting.guassian_kernel_size),
                         str_canny_low_threshold = str(self.setting.canny_low_threshold), str_canny_high_threshold = str(self.setting.canny_high_threshold),
                         str_canny_ostu_threshold = '%.1f' % self.setting.canny_ostu_threshold,
                         str_hough_rho = str(self.setting.hough_rho), str_hough_theta = str(self.setting.hough_theta),
                         str_hough_vote_threshold = str(self.setting.hough_vote_threshold), str_hough_min_line = str(self.setting.hough_min_line_length),
                         str_hough_line_gap = str(self.setting.hough_max_line_gap),
                         str_region_of_interest = formatListTuple(self.setting.region_of_interest),
                         str_unwanted_slope = '%.1f' % self.setting.unwanted_slope, str_prev_frame_weight = '%.1f' % self.setting.prev_frame_weight,
                         str_final_output = self.setting.final_output)

            file = open(self.configFile, "w")
            file.write(output)
            file.close()

        def processVideo(self, filename):
            try:
                process_video(self.outputDir, filename, self.setting, self.logger)
                base = os.path.basename(filename)
                return self.outputDir+base
            except Exception as ex:
                print("Error occurred", ex)
                traceback.print_exc()
                self.logger.error("Error occurred when processing video", exc_info=True)

