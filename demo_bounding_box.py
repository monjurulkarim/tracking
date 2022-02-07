'''
Input: folders of frames + csv files
Output: tracked .mp4 videos
Input folder structure:
-------------------------
--Demo
    |-26_M
        |-26_M_frame_0.jpg
        |-26_M_frame_1.jpg
        ...
    |-27_M
        |-27_M_frame_0.jpg
        |-27_M_frame_1.jpg
        ...
    ...
    ...
--------------------------

bbox_dir should be as below:
-------------------
--tracking_results/file_list
    |-26_M.csv
    |-27_M.csv
    ...

csv heading:
frame	Risk_1	Risk_2	Risk3	Risk4

'''


import cv2
import os
from natsort import natsorted
import argparse
import sys
import csv
import pandas as pd
import re
import numpy as np

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input_video", default="../demo")
    parser.add_argument("--bbox_dir", default="./tracking_results/file_list/")
    args = parser.parse_args()
    return args


def main():
    color_list = [
        [255, 0, 0],  # blue
        [0, 0, 255], #red
        [0, 255, 0], #lime
        [128, 0, 128],  # purple
        [0, 0, 255],  # red
        [255, 0, 255],  # fuchsia
        [0, 128, 0],  # green
        [128, 128, 0],  # teal
        [0, 0, 128],  # maroon
        [0, 128, 128],  # oliveimage_folder
        [0, 255, 255],  # yellow
    ]
    height, width = 720, 1080
    args = get_args()
    input_video = args.input_video
    input_video_list = os.listdir(input_video)
    bbox_dir = args.bbox_dir
    for folder in input_video_list:
        video_name = f"{folder}.mp4"
        image_folder = os.path.join(input_video,folder)
        images = natsorted([img for img in os.listdir(image_folder) if img.endswith(".jpg")])
        bbox_csv = f"{bbox_dir}{folder}.csv"

        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        video = cv2.VideoWriter(video_name, fourcc, 20, (width, height))
        print('======================')
        print(f"{video_name}...")

        with open(bbox_csv,'r', newline = '') as csvfile:
            reader = csv.reader(csvfile,delimiter=',')
            heading = next(reader)
            value = next(reader)

            for i in range(100):
                img = cv2.imread(os.path.join(image_folder, images[i]))
                if i< int(value[0]):
                    video.write(img)
                elif i == int(value[0]):
                    risk1 = value[1]
                    risk1 = re.sub("[()]","", risk1)
                    risk1 = [int(i) for i in risk1.split(',')]
                    cv2.rectangle(img, risk1, color_list[0], thickness=2)
                    if value[2] != '':
                        risk2 = value[2]
                        risk2 = re.sub("[()]","", risk2)
                        risk2 = [int(i) for i in risk2.split(',')]
                        cv2.rectangle(img, ristructuresk2, color_list[1], thickness=2)
                    if value[3] != '':image_folder
                        risk3 = value[3]
                        risk3 = re.sub("[()]","", risk3)
                        risk3 = [int(i) for i in risk3.split(',')]
                        cv2.rectangle(img, risk3, color_list[2], thickness=2)
                    if value[4] != '':
                        risk4 = value[4]
                        risk4 = re.sub("[()]","", risk4)
                        risk4 = [int(i) for i in risk4.split(',')]
                        cv2.rectangle(img, risk4, color_list[3], thickness=2)
                    try:
                        video.write(img)
                        value = next(reader)
                    except:
                        print('Finished operation')
                else:
                    video.write(img)

            cv2.destroyAllWindows()
            video.release()

    return

# 
# def main_original():
#     args = get_args()
#     input_video = args.input_video
#     bbox_dir = args.bbox_dir
#     folder_name = input_video.split('/')[-1]
#     video_name = f"{folder_name}.mp4"
#     print(video_name)
#     bbox_csv = f"{bbox_dir}{folder_name}.csv"
#     color_list = [
#         [255, 0, 0],  # blue
#         [0, 0, 255], #red
#         [0, 255, 0], #lime
#         [128, 0, 128],  # purple
#         [0, 0, 255],  # red
#         [255, 0, 255],  # fuchsia
#         [0, 128, 0],  # green
#         [128, 128, 0],  # teal
#         [0, 0, 128],  # maroon
#         [0, 128, 128],  # olive
#         [0, 255, 255],  # yellow
#     ]
#
#     images = natsorted([img for img in os.listdir(input_video) if img.endswith(".jpg")])
#     height, width = 720, 1080
#
#     fourcc = cv2.VideoWriter_fourcc(*'mp4v')
#     video = cv2.VideoWriter(video_name, fourcc, 20, (width, height))
#     print('======================')
#     print(f"{video_name}...")
#
#
#
#     with open(bbox_csv,'r', newline = '') as csvfile:
#         reader = csv.reader(csvfile,delimiter=',')
#         heading = next(reader)
#         value = next(reader)
#
#         for i in range(100):
#             img = cv2.imread(os.path.join(input_video, images[i]))
#             if i< int(value[0]):
#                 video.write(img)
#             elif i == int(value[0]):
#                 risk1 = value[1]
#                 risk1 = re.sub("[()]","", risk1)
#                 risk1 = [int(i) for i in risk1.split(',')]
#                 cv2.rectangle(img, risk1, color_list[0], thickness=2)
#                 if value[2] != '':
#                     risk2 = value[2]
#                     risk2 = re.sub("[()]","", risk2)
#                     risk2 = [int(i) for i in risk2.split(',')]
#                     cv2.rectangle(img, risk2, color_list[1], thickness=2)
#                 if value[3] != '':
#                     risk3 = value[3]
#                     risk3 = re.sub("[()]","", risk3)
#                     risk3 = [int(i) for i in risk3.split(',')]
#                     cv2.rectangle(img, risk3, color_list[2], thickness=2)
#                 if value[4] != '':
#                     risk4 = value[4]
#                     risk4 = re.sub("[()]","", risk4)
#                     risk4 = [int(i) for i in risk4.split(',')]
#                     cv2.rectangle(img, risk4, color_list[3], thickness=2)
#                 try:
#                     video.write(img)
#                     value = next(reader)
#                 except:
#                     print('Finished operation')
#             else:
#                 video.write(img)
#
#         cv2.destroyAllWindows()
#         video.release()
#
#     return


if __name__ == '__main__':
    main()
