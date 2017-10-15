
class Setting:
    # color filter
    def __init__(self):
        self.__color_filter = 'hsv'
        self.__color_filter_hsv_low = [(75,0,0), (0,0,230)]
        self.__color_filter_hsv_high = [(115,255,255), (180,25,255)]
        self.__gray_scale = 'gray'
        self.__guassian_kernel_size = 7
        self.__canny = 'canny-ostu'
        self.__canny_low_threshold = 100
        self.__canny_high_threshold = 200
        self.__canny_ostu_threshold = 0.1
        self.__hough_rho = 2
        self.__hough_theta = 1
        self.__hough_vote_threshold = 15
        self.__hough_min_line = 40
        self.__hough_line_gap = 30
        self.__region_of_interest = [(0, 100), (46, 60), (54, 60), (100, 100)]
        self.__unwanted_slope = 0.3
        self.__prev_frame_weight = 0.3
        self.__final_output = 'normal'

    @property
    def color_filter(self):
        return self.__color_filter

    @color_filter.setter
    def color_filter(self, color_filter):
        if not (type(color_filter) is str):
            raise ValueError("color_filter must be a string")
        self.__color_filter = color_filter

    @property
    def color_filter_hsv_low(self):
        return self.__color_filter_hsv_low

    @color_filter_hsv_low.setter
    def color_filter_hsv_low(self, color_filter_hsv_low):
        if not type(color_filter_hsv_low) == type(list()):
            raise ValueError("color_filter_hsv_low is a list of tuple of 3 integers")
        for tuple in color_filter_hsv_low:
            h, s, v = tuple
            if not (type(h) is int and type(s) is int and type(v) is int):
                raise ValueError("color_filter_hsv_low is a list of tuple of 3 integers")
        self.__color_filter_hsv_low = color_filter_hsv_low

    @property
    def color_filter_hsv_high(self):
        return self.__color_filter_hsv_high

    @color_filter_hsv_high.setter
    def color_filter_hsv_high(self, color_filter_hsv_high):
        if not type(color_filter_hsv_high) == type(list()):
            raise ValueError("color_filter_hsv_high is a list of tuple of 3 integers")
        for tuple in color_filter_hsv_high:
            h, s, v = tuple
            if not (type(h) is int and type(s) is int and type(v) is int):
                raise ValueError("color_filter_hsv_high is a list of tuple of 3 integers")
        self.__color_filter_hsv_high = color_filter_hsv_high

    # gray scale
    @property
    def gray_scale(self):
        return self.__gray_scale

    @gray_scale.setter
    def gray_scale(self, gray_scale):
        if not (type(gray_scale) is str):
            raise ValueError("gray_scale must be a string")
        self.__gray_scale = gray_scale

    # guassian kernel
    @property
    def guassian_kernel_size(self):
        return self.__guassian_kernel_size

    @guassian_kernel_size.setter
    def guassian_kernel_size(self, guassian_kernel_size):
        if not (type(guassian_kernel_size) is int and guassian_kernel_size % 2 == 1):
            raise ValueError("guassian_kernel_size must be an odd integer")
        self.__guassian_kernel_size = guassian_kernel_size

    # canny
    @property
    def canny(self):
        return self.__canny

    @canny.setter
    def canny(self, canny):
        if not (type(canny) is str):
            raise ValueError("canny must be a string")
        self.__canny = canny

    @property
    def canny_low_threshold(self):
        return self.__canny_low_threshold

    @canny_low_threshold.setter
    def canny_low_threshold(self, canny_low_threshold):
        if not (type(canny_low_threshold) is int):
            raise ValueError("canny_low_threshold must be an integer")
        self.__canny_low_threshold = canny_low_threshold

    @property
    def canny_high_threshold(self):
        return self.__canny_high_threshold

    @canny_high_threshold.setter
    def canny_high_threshold(self, canny_high_threshold):
        if not (type(canny_high_threshold) is int):
            raise ValueError("canny_high_threshold must be an integer")
        self.__canny_high_threshold = canny_high_threshold

    @property
    def canny_ostu_threshold(self):
        return self.__canny_ostu_threshold

    @canny_ostu_threshold.setter
    def canny_ostu_threshold(self, canny_ostu_threshold):
        if not (type(canny_ostu_threshold) is float and canny_ostu_threshold >= 0 and canny_ostu_threshold <= 1):
            raise ValueError("canny_ostu_threshold must be a float and between 0 and 1")
        self.__canny_ostu_threshold = canny_ostu_threshold

    # hough
    @property
    def hough_rho(self):
        return self.__hough_rho

    @hough_rho.setter
    def hough_rho(self, hough_rho):
        if not (type(hough_rho) is int):
            raise ValueError("hough_rho must be an integer")
        self.__hough_rho = hough_rho

    @property
    def hough_theta(self):
        return self.__hough_theta

    @hough_theta.setter
    def hough_theta(self, hough_theta):
        if not (type(hough_theta) is int):
            raise ValueError("hough_theta must be an integer")
        self.__hough_theta = hough_theta

    @property
    def hough_vote_threshold(self):
        return self.__hough_vote_threshold

    @hough_vote_threshold.setter
    def hough_vote_threshold(self, hough_vote_threshold):
        if not (type(hough_vote_threshold) is int):
            raise ValueError("hough_threshold must be an integer")
        self.__hough_vote_threshold = hough_vote_threshold

    @property
    def hough_min_line_length(self):
        return self.__hough_min_line_length

    @hough_min_line_length.setter
    def hough_min_line_length(self, hough_min_line_length):
        if not (type(hough_min_line_length) is int):
            raise ValueError("hough_min_line_length must be an integer")
        self.__hough_min_line_length = hough_min_line_length

    @property
    def hough_max_line_gap(self):
        return self.__hough_max_line_gap

    @hough_max_line_gap.setter
    def hough_max_line_gap(self, hough_max_line_gap):
        if not (type(hough_max_line_gap) is int):
            raise ValueError("hough_max_line_gap must be an integer")
        self.__hough_max_line_gap = hough_max_line_gap

    @property
    def region_of_interest(self):
        return self.__region_of_interest

    @region_of_interest.setter
    def region_of_interest(self, region_of_interest):
        if not type(region_of_interest) == type(list()):
            raise ValueError("region_of_interest is a list of points")

        for tuple in region_of_interest:
            x, y = tuple
            if not (type(x) is int and type(y) is int):
                raise ValueError("region_of_interest must be a list of points which are integer values.")
        self.__region_of_interest = region_of_interest

    @property
    def unwanted_slope(self):
        return self.__unwanted_slope

    @unwanted_slope.setter
    def unwanted_slope(self, unwanted_slope):
        if not (type(unwanted_slope) is float):
            raise ValueError("unwanted_slope must be a float")
        self.__unwanted_slope = unwanted_slope

    @property
    def prev_frame_weight(self):
        return self.__prev_frame_weight

    @prev_frame_weight.setter
    def prev_frame_weight(self, prev_frame_weight):
        if not (type(prev_frame_weight) is float):
            raise ValueError("prev_frame_weight must be a float")
        self.__prev_frame_weight = prev_frame_weight

    @property
    def final_output(self):
        return self.__final_output

    @final_output.setter
    def final_output(self, final_output):
        if not (type(final_output) is str):
            raise ValueError("final_output must be a string")
        self.__final_output = final_output