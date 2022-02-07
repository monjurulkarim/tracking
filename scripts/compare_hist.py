'''
Input: long video folder directory
output: A text file containing starting frame numbers
---------------------------------------------------------------------------------------
This script uses opencv compare histogram to compare each video frames with it's previous
frames. When the frame correlation is less than 0.4 then we consider it is a different video clip.
We save this frame number in a text file.
'''

from __future__ import print_function
from __future__ import division
import cv2 as cv
import numpy as np
import argparse
import glob
from natsort import natsorted
import os

def get_args():
    '''
    takes the input video directory as an argument.
    '''
    parser = argparse.ArgumentParser()
    parser = add_argument("--data_dir", default="../../../../data/crash_dataset_monjurul/")
    parser.add_argument("--frames_dir", default="v1/")
    args = parser.parse_args()
    return args


def save_text(starting_frames):
    '''
    loop through a text file to save starting frame numbers.
    '''
    tmp_file = 'starting_frames.txt'
    with open(tmp_file, 'a') as f:
        for item in starting_frames:
            f.write(str(item))
            f.write('\n')
    return

def main():
    args = get_args()
    data_dir = args.data_dir
    folder_dir = data_dir +args.frames_dir
    frames_dir = os.path.abspath(os.path.join(__file__ ,frames_folder))
    paths = natsorted(glob.glob(os.path.join(frames_dir, '*.jpg')))
    starting_frames = compare_hist(paths)
    save_text(starting_frames)
    return



def compare_hist(paths):
    '''
    Uses opencv built-in function to compare each frame with it's previous frame
    '''
    src_base  = cv.imread(paths[0])
    cut_off_frame = []
    for i in range(len(paths)):
        # src_base  = cv.imread(paths[i])
        # src_test1 = cv.imread(paths[i+1])
        if i < len(paths)-1:
            src_test1 = cv.imread(paths[i+1])
            if src_base is None or src_test1 is None:
                print('Could not open or find the images!')
                exit(0)
            hsv_base = cv.cvtColor(src_base, cv.COLOR_BGR2HSV)
            hsv_test1 = cv.cvtColor(src_test1, cv.COLOR_BGR2HSV)
            hsv_half_down = hsv_base[hsv_base.shape[0]//2:,:]
            h_bins = 50
            s_bins = 60
            histSize = [h_bins, s_bins]
            # hue varies from 0 to 179, saturation from 0 to 255
            h_ranges = [0, 180]
            s_ranges = [0, 256]
            ranges = h_ranges + s_ranges # concat lists
            # Use the 0-th and 1-st channels
            channels = [0, 1]
            hist_base = cv.calcHist([hsv_base], channels, None, histSize, ranges, accumulate=False)
            cv.normalize(hist_base, hist_base, alpha=0, beta=1, norm_type=cv.NORM_MINMAX)
            hist_half_down = cv.calcHist([hsv_half_down], channels, None, histSize, ranges, accumulate=False)
            cv.normalize(hist_half_down, hist_half_down, alpha=0, beta=1, norm_type=cv.NORM_MINMAX)
            hist_test1 = cv.calcHist([hsv_test1], channels, None, histSize, ranges, accumulate=False)
            cv.normalize(hist_test1, hist_test1, alpha=0, beta=1, norm_type=cv.NORM_MINMAX)
            base_test1 = cv.compareHist(hist_base, hist_test1, 0) #compare method = 0 (correlation)
            print('test_image:', paths[i+1],'--','base-test1 :',\
                  base_test1)
            if base_test1 < 0.4:
                cut_off_frame.append(i+1)
            print('======================================')
            src_base = src_test1
        else:
            print('--last frame--')
    return cut_off_frame

if __name__ == '__main__':
    main()
