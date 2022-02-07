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
    parser.add_argument("--input_video", default="./tracking_results/a2")
    parser.add_argument("--bbox_dir", default="./tracking_results/file_list/")
    args = parser.parse_args()
    return args


def video_generation(input_video,video_name,frame,risk1,risk2,risk3,risk4):
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
        [0, 128, 128],  # olive
        [0, 255, 255],  # yellow
    ]
    # images = natsorted([img for img in os.listdir(input_video) if img.endswith(".jpg")])
    # height, width = 720, 1080
    #
    # fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    # video = cv2.VideoWriter(video_name, fourcc, 20, (width, height))
    # print('======================')
    # print(f"{video_name}...")

    # for i in images:





    return

def main():
    args = get_args()
    input_video = args.input_video
    bbox_dir = args.bbox_dir
    folder_name = input_video.split('/')[-1]
    video_name = f"{folder_name}.mp4"
    bbox_csv = f"{bbox_dir}{folder_name}.csv"
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
        [0, 128, 128],  # olive
        [0, 255, 255],  # yellow
    ]

    images = natsorted([img for img in os.listdir(input_video) if img.endswith(".jpg")])
    height, width = 720, 1080

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    video = cv2.VideoWriter(video_name, fourcc, 20, (width, height))
    print('======================')
    print(f"{video_name}...")

    # data = np.zeros((100,5))


    with open(bbox_csv,'r', newline = '') as csvfile:
        reader = csv.reader(csvfile,delimiter=',')
        heading = next(reader)
        value = next(reader)
        # frame = int(value[0])
        # risk1 = value[1]
        # risk1 = re.sub("[()]","", risk1)
        # risk1 = [int(i) for i in risk1.split(',')]


        for i in range(100):
            img = cv2.imread(os.path.join(input_video, images[i]))
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
                    cv2.rectangle(img, risk2, color_list[1], thickness=2)
                if value[3] != '':
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


        # print(int(value[0]))
    #     data = 0
    #     for row in reader:
    #         frame, risk1, risk2,risk3,risk4 = row
    #         # for ind in range(len(images)):
    #         #     if ind < int(frame):
    #         #         print('before tracking :',ind)
    #         #     elif ind == int(frame):
    #         #         print('tracking :',ind)
    #         #     else:
    #         #         print('no-tracking :',ind)
    #
    #
    #             # risk1 = re.sub("[()]","", risk1)
    #             # # risk1 = [int(i) for i in risk1.split(',')]
    #             # risk2 = re.sub("[()]","", risk2)
    #             # risk3 = re.sub("[()]","", risk3)
    #             # risk4 = re.sub("[()]","", risk4)
    #             data.append([frame,risk1,risk2,risk3,risk4])
    #
    # print(data[0])
    # video_generation(input_video,video_name,frame,risk1,risk2,risk3,risk4)
                # # print(int(risk1))
                # print(risk2.split(','))



if __name__ == '__main__':
    main()
