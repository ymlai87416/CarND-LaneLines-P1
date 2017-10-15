#importing some useful packages
#import matplotlib.pyplot as plt
#import matplotlib.image as mpimg
import numpy as np
import cv2
import uuid
import traceback
import os
# Import everything needed to edit/save/watch video clips
from moviepy.video.io.VideoFileClip import VideoFileClip
import math
from app.setting import Setting
from functools import partial

previous_lanes = None

def removeNonYellowAndWhite(img):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    lower_yellow = np.array([75, 0, 0])
    upper_yellow = np.array([115, 255, 255])
    lower_white = np.array([0, 0, 230], dtype=np.uint8)
    upper_white = np.array([180, 25, 255], dtype=np.uint8)

    kernel = np.ones((9, 9), np.uint8)

    # Threshold the HSV image to get only yellow colors
    mask_yellow = cv2.inRange(hsv, lower_yellow, upper_yellow)
    mask_white = cv2.inRange(hsv, lower_white, upper_white)

    mask = cv2.bitwise_or(mask_yellow, mask_white)
    mask = cv2.dilate(mask, kernel, iterations=1)

    res = cv2.bitwise_and(img, img, mask=mask)

    return res

def color_filtering(img, color_filter_hsv_low, color_filter_hsv_high):
    kernel = np.ones((9, 9), np.uint8)
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    mask = None

    minLength = min(len(color_filter_hsv_low), len(color_filter_hsv_high))

    for i in range(minLength):
        mask_temp  = cv2.inRange(hsv, color_filter_hsv_low[i], color_filter_hsv_high[i])
        if mask == None:
            mask = mask_temp
        else:
            mask = cv2.bitwise_or(mask_temp, mask)

    mask = cv2.dilate(mask, kernel, iterations=1)

    res = cv2.bitwise_and(img, img, mask=mask)

    return res

def grayscale(img):
    """Applies the Grayscale transform
    This will return an image with only one color channel
    but NOTE: to see the returned image as grayscale
    (assuming your grayscaled image is called 'gray')
    you should call plt.imshow(gray, cmap='gray')"""
    return cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    # Or use BGR2GRAY if you read an image with cv2.imread()
    # return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)


def canny(img, low_threshold, high_threshold):
    """Applies the Canny transform"""
    return cv2.Canny(img, low_threshold, high_threshold)


def adoptive_canny(img, threshold):
    ret, thresh1 = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU);
    cannyThresh = threshold * ret;
    return cv2.Canny(img, cannyThresh, ret);


def gaussian_blur(img, kernel_size):
    """Applies a Gaussian Noise kernel"""
    return cv2.GaussianBlur(img, (kernel_size, kernel_size), 0)


def region_of_interest(img, vertices):
    """
    Applies an image mask.

    Only keeps the region of the image defined by the polygon
    formed from `vertices`. The rest of the image is set to black.
    """
    # defining a blank mask to start with
    mask = np.zeros_like(img)

    # defining a 3 channel or 1 channel color to fill the mask with depending on the input image
    if len(img.shape) > 2:
        channel_count = img.shape[2]  # i.e. 3 or 4 depending on your image
        ignore_mask_color = (255,) * channel_count
    else:
        ignore_mask_color = 255

    # filling pixels inside the polygon defined by "vertices" with the fill color
    cv2.fillPoly(mask, vertices, ignore_mask_color)

    # returning the image only where mask pixels are nonzero
    masked_image = cv2.bitwise_and(img, mask)
    return masked_image


def draw_lines(img, lines, color=[255, 0, 0], thickness=2):
    """
    NOTE: this is the function you might want to use as a starting point once you want to 
    average/extrapolate the line segments you detect to map out the full
    extent of the lane (going from the result shown in raw-lines-example.mp4
    to that shown in P1_example.mp4).  

    Think about things like separating line segments by their 
    slope ((y2-y1)/(x2-x1)) to decide which segments are part of the left
    line vs. the right line.  Then, you can average the position of each of 
    the lines and extrapolate to the top and bottom of the lane.

    This function draws `lines` with `color` and `thickness`.    
    Lines are drawn on the image inplace (mutates the image).
    If you want to make the lines semi-transparent, think about combining
    this function with the weighted_img() function below
    """
    for line in lines:
        for x1, y1, x2, y2 in line:
            cv2.line(img, (x1, y1), (x2, y2), color, thickness)


def line_averaging(lines, len_x, len_y):
    line_left_neg_slope = []
    line_right_pos_slope = []
    left_x = []
    left_y = []
    right_x = []
    right_y = []

    ttl_dst_right = 0.
    ttl_dst_left = 0.
    for line in lines:
        for x1, y1, x2, y2 in line:
            slope = ((y2 - y1) / (x2 - x1))
            b = y1 - slope * x1
            dist = int(math.sqrt((x2 - x1) * (x2 - x1) + (y2 - y1) * (y2 - y1)))
            minx = min(x1, x2)
            maxx = max(x1, x2)
            if (slope > 0 and x1 > len_x // 2 and x2 > len_x // 2 and np.isfinite(slope)):
                line_right_pos_slope.append(line)
                # right_x.append(slope * dist)
                # right_y.append(b * dist)
                # ttl_dst_right = ttl_dst_right + dist
                for w in range(1, dist, 10):
                    right_x.append(slope)
                    right_y.append(b)
            elif (slope < 0 and x1 < len_x // 2 and x2 < len_x // 2 and np.isfinite(slope)):
                line_left_neg_slope.append(line)
                # left_x.append(slope * dist)
                # left_y.append(b * dist)
                # ttl_dst_left = ttl_dst_left + dist
                for w in range(1, dist, 10):
                    left_x.append(slope)
                    left_y.append(b)

    result = []

    if (len(left_x) > 0):
        left_fit = (np.median(left_x), np.median(left_y))
        # left_fit = (np.sum(left_x) /ttl_dst_left, np.sum(left_y)/ttl_dst_left )
        left_x1, left_x2, left_y1, left_y2 = 0, len_x, int(left_fit[1]), int(left_fit[0] * len_x + left_fit[1])
        result.append([(left_x1, left_y1, left_x2, left_y2)])
    else:
        result.append([])

    if (len(right_x) > 0):
        right_fit = (np.median(right_x), np.median(right_y))
        # right_fit = (np.sum(right_x) /ttl_dst_right, np.sum(right_y)/ttl_dst_right )
        right_x1, right_x2, right_y1, right_y2 = 0, len_x, int(right_fit[1]), int(right_fit[0] * len_x + right_fit[1])
        result.append([(right_x1, right_y1, right_x2, right_y2)])
    else:
        result.append([])

    return result


def filter_non_lane_lines(lines, len_x, len_y, threshold=0.2):
    result = []

    for line in lines:
        for x1, y1, x2, y2 in line:
            slope = ((y2 - y1) / (x2 - x1))
            if (slope > threshold or slope < -threshold):
                if (slope > 0 and x1 > len_x // 2 and x2 > len_x // 2):
                    result.append(line)
                elif (slope < 0 and x1 < len_x // 2 and x2 < len_x // 2):
                    result.append(line)

    return result


def hough_lines(img, rho, theta, threshold, min_line_len, max_line_gap):
    """
    `img` should be the output of a Canny transform.

    Returns an image with hough lines drawn.
    """
    lines = cv2.HoughLinesP(img, rho, theta, threshold, np.array([]), minLineLength=min_line_len,
                            maxLineGap=max_line_gap)
    return lines


def draw_lane(img, lines, color, thickness):
    line_img = np.zeros((img.shape[0], img.shape[1], 3), dtype=np.uint8)
    draw_lines(line_img, lines, color, thickness)
    return line_img


# Python 3 has support for cool math symbols.

def weighted_img(img, initial_img, α=0.8, β=1., λ=0.):
    """
    `img` is the output of the hough_lines(), An image with lines drawn on it.
    Should be a blank image (all black) with lines drawn on it.

    `initial_img` should be the image before any processing.

    The result image is computed as follows:

    initial_img * α + img * β + λ
    NOTE: initial_img and img must be the same shape!
    """
    return cv2.addWeighted(initial_img, α, img, β, λ)


def smooth_lane(current_lane, previous_lane, weight):
    result = []
    if (previous_lane != None):
        for i in range(0, 2):
            if (len(current_lane[i]) == 0):
                # current_lane[i].extends(previous_lane[i])
                result.append(previous_lane[i])
            else:
                if (len(previous_lane[i]) > 0):
                    x1, y1, x2, y2 = current_lane[i][0]
                    px1, py1, px2, py2 = previous_lane[i][0]
                    line = (int(weight * x1) + int((1 - weight) * px1), int(weight * y1 + (1 - weight) * py1), \
                            int(weight * x2 + (1 - weight) * px2), int(weight * y2) + int((1 - weight) * py2))
                    result.append([line])
                else:
                    result.append(current_lane[i])
    else:
        result = current_lane

    # print('debug', current_lane, previous_lane, result)
    return result


# TODO: Build your pipeline that will draw lane lines on the test_images
# then save them to the test_images directory.
def remove_alpha_channel(img):
    if (img.shape[2] == 4):
        # print("alpha channel exists")
        img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
    return img


def gray_to_color(img):
    result = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)
    return result


def equalizeIntensity(img):
    if (img.shape[2] >= 3):
        ycrcb = cv2.cvtColor(img, cv2.COLOR_BGR2YCrCb);

        channels = cv2.split(ycrcb)
        clahe = cv2.createCLAHE(clipLimit=4.0, tileGridSize=(8, 8))
        channels[0] = clahe.apply(channels[0])

        ycrcb = cv2.merge(channels);

        result = cv2.cvtColor(ycrcb, cv2.COLOR_YCrCb2BGR);

        return result;
    return img


def prob(img, cmap, save=False):
    plt.figure()
    plt.imshow(img, cmap=cmap)
    if (save):
        plt.imsave("prob_images/" + str(uuid.uuid4()) + '.png', img)


def pipeline(img,
             color_filter, color_filter_hsv_low, color_filter_hsv_high,
             gray_scale,
             guassian_kernel_size,
             canny, canny_low_threshold, canny_high_threshold, canny_ostu_threshold,
             region_of_interest_,
             hough_rho, hough_theta, hough_threshold, hough_min_line_len, hough_max_line_gap,
             unwanted_slop, prev_frame_weight,
             final_output,
             previous_lanes, logger):
    try:
        output_img = None

        img = remove_alpha_channel(img)

        # color filtering
        if (color_filter == 'hsv'):
            img_alt = color_filtering(img, color_filter_hsv_low, color_filter_hsv_high)
        else:
            img_alt = img

        if (final_output == 'color_filter'):
            output_img = img_alt

        # gray scale
        if(gray_scale == 'gray'):
            img_alt = grayscale(img_alt)
        elif(gray_scale == 'yuv'):
            img_alt = grayscale(img_alt)
        else:
            raise ValueError("Unknown gray scale algorithm.")

        if (final_output == 'gray_scale'):
            output_img = gray_to_color(img_alt)

        # guassian blur
        imshape = img_alt.shape
        img_alt = gaussian_blur(img_alt, guassian_kernel_size)

        if (final_output == 'guassian'):
            output_img = gray_to_color(img_alt)

        # canny edge detection algorithm
        if canny == 'canny':
            img_alt = canny(img_alt, canny_low_threshold, canny_high_threshold)
        elif canny == 'canny-ostu':
            img_alt = adoptive_canny(img_alt, canny_ostu_threshold)
        else:
            raise ValueError("Unknown edge detection algorithm.")

        # hough algorithm
        roi = list(map(lambda x: (int(imshape[1]*x[0]/100), int(imshape[0]*x[1]/100)), region_of_interest_))
        roi = [roi]
        vertices = np.array(roi, dtype=np.int32)
        masked_image = region_of_interest(img_alt, vertices)

        if (final_output == 'canny'):
            output_img = gray_to_color(masked_image)

        lines = hough_lines(masked_image, hough_rho, hough_theta, hough_threshold, hough_min_line_len,
                            hough_max_line_gap)
        lines = filter_non_lane_lines(lines, imshape[1], imshape[0], unwanted_slop)
        img_line_detect = draw_lane(masked_image, lines, [0, 0, 255], 2)

        lines = line_averaging(lines, imshape[1], imshape[0])
        lines = smooth_lane(lines, previous_lanes, 1-prev_frame_weight)
        img_line_main = draw_lane(masked_image, lines, [255, 0, 0], 5)

        if final_output == 'hough':
            img_line = weighted_img(img_line_detect, img_line_main, 0., 1., 0.)
            # clip the lane lines
            img_line = region_of_interest(img_line, vertices)
            img_final = weighted_img(img_line, img, 0.8, 1., 0.)
            output_img = img_final
        elif final_output == 'average':
            img_line = weighted_img(img_line_detect, img_line_main, .5, .5, 0.)
            # clip the lane lines
            img_line = region_of_interest(img_line, vertices)
            img_final = weighted_img(img_line, img, 0.8, 1., 0.)
            output_img = img_final
        elif final_output == 'normal':
            img_line = weighted_img(img_line_detect, img_line_main, 1., 0., 0.)
            # clip the lane lines
            img_line = region_of_interest(img_line, vertices)
            img_final = weighted_img(img_line, img, 0.8, 1., 0.)
            output_img = img_final

        return output_img, lines
    except Exception as ex:
        print("Error occurred", ex)
        traceback.print_exc()
        logger.error("Error occurred when processing video frame.", exc_info=True)
        return None

def process_image(image, setting: Setting, logger):
    # NOTE: The output you return should be a color image (3 channel) for processing video below
    # TODO: put your pipeline here,
    # you should return the final output (image where lines are drawn on lanes)

    global previous_lanes
    try:
        result, lanes = pipeline(image,
                                 setting.color_filter, setting.color_filter_hsv_low, setting.color_filter_hsv_high,
                                 setting.gray_scale,
                                 setting.guassian_kernel_size,
                                 setting.canny, setting.canny_low_threshold, setting.canny_high_threshold, setting.canny_ostu_threshold,
                                 setting.region_of_interest,
                                 setting.hough_rho, setting.hough_theta*np.pi/180, setting.hough_vote_threshold, setting.hough_min_line_length, setting.hough_max_line_gap,
                                 setting.unwanted_slope, setting.prev_frame_weight,
                                 setting.final_output,
                                 previous_lanes, logger)

        previous_lanes = lanes
    except Exception as ex:
        img_out = remove_alpha_channel(image)
        #mpimg.imsave("test_images/error.jpg", img_out)
        traceback.print_exc()
        logger.error("Error occurred when processing video frame.", exc_info=True)

    return result

def process_video(outputDir, video, setting, logger):
    if not (os.path.isdir(outputDir)):
        os.mkdir(outputDir)

    base = os.path.basename(video)
    outputPath = outputDir + base
    ## To speed up the testing process you may want to try your pipeline on a shorter subclip of the video
    ## To do so add .subclip(start_second,end_second) to the end of the line below
    ## Where start_second and end_second are integer values representing the start and end of the subclip
    ## You may also uncomment the following line for a subclip of the first 5 seconds
    ##clip1 = VideoFileClip("test_videos/solidWhiteRight.mp4").subclip(0,5)
    clip1 = VideoFileClip(video)
    previous_lane = None
    white_clip = clip1.fl_image(partial(process_image, setting=setting, logger=logger))  # NOTE: this function expects color images!!
    white_clip.write_videofile(outputPath, audio=False, progress_bar=False)