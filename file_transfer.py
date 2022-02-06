'''
dependency: at first need to run "compare_hist.py" to generate a text file
Input: a text file containing starting frame numbers of each video clip
output: video clips (i.e. frames) will be transfered
--------------------------------------------------------------------------------------------
This script reads the text file that contains the starting frame numbers of all video clips
in a long video. Based on the frame number it moves the video frames to separated directory
to create separate folders for each video clip.
'''


import numpy as np
import time
import os
import os.path as osp
import shutil
import argparse
import glob
from natsort import natsorted



def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--frames_dir", default="new_frames/vid5/")
    parser.add_argument("--anno_file", default="starting_frames.txt")
    parser.add_argument("--destination_dir", default="trimmed_folder/vid5/")
    args = parser.parse_args()
    return args


def main():
    args = get_args()
    frames_dir = args.frames_dir
    destination_folder = args.destination_dir
    anno_file = args.anno_file

    paths = natsorted(glob.glob(os.path.join(frames_dir, '*.jpg')))
    file_transfer(paths, frames_dir,anno_file,destination_folder)

    return

def file_transfer(paths, frames_dir,anno_file,destination_folder):
    starting_frames = []
    with open(anno_file, 'r') as f: #Read the lines from the text file
        for line in f.readlines():
            starting_frames.append(int(line))
    previous_element = 0
    print('Processing...')
    for element in starting_frames:
        destination =os.path.join(destination_folder,str(element))
        if not os.path.exists(destination):
            os.makedirs(destination)
        for frames in range(previous_element,element):
            filename = paths[frames]
            shutil.move(filename, destination)
        previous_element = element
    return print('finished')

if __name__ == '__main__':
    main()
