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

from collections import deque
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
    pts1 = deque(maxlen=36)
    pts2 = deque(maxlen=36)
    pts3 = deque(maxlen=36)
    pts4 = deque(maxlen=36)
    center1 = None
    center2 = None
    center3 = None
    center4 = None
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

            centroid_center_r1 = 0
            centroid_center_r2 = 0
            centroid_center_r3 = 0
            centroid_center_r4 = 0
            for i in range(100):
                img = cv2.imread(os.path.join(image_folder, images[i]))
                if i< int(value[0]):
                    video.write(img)
                elif i == int(value[0]):
                    risk1 = value[1]
                    risk1 = re.sub("[()]","", risk1)
                    risk1 = [int(i) for i in risk1.split(',')]
                    center1 = (int((risk1[0]+risk1[2]/2)),int((risk1[1]+risk1[3]/2)))
                    cv2.rectangle(img, risk1, color_list[0], thickness=2)
                    cv2.circle(img,center1,5,color_list[0],-1)
                    pts1.appendleft(center1)
                    centroid_center_r1+=1

                    # if centroid_center_r1 > 2:
                    try:
                        pts_r1=[item for item in pts1]
                        pts_r1 = np.array(pts_r1)
                        thickness =  int(np.sqrt(36 / float(centroid_center_r1 + 1)) * 2.5)
                        cc = 0
                        for point1, point2 in zip(pts_r1,pts_r1[1:]):
                            if cc < 5:
                                cv2.line(img, point1,point2, color_list[0], thickness=7)
                                cc+=1
                            else:
                                cv2.line(img, point1,point2, color_list[0], thickness)
                                cc+=1
                        # cv2.line(img, pts[centroid_center_r1 - 2], pts[centroid_center_r1-1], color_list[0], thickness)
                        # cv2.line(img, pts_r1, color_list[0], thickness)
                    except:
                        print('skipped from 1st object')
                    if value[2] != '':
                        risk2 = value[2]
                        risk2 = re.sub("[()]","", risk2)
                        risk2 = [int(i) for i in risk2.split(',')]
                        center2 = (int((risk2[0]+risk2[2]/2)),int((risk2[1]+risk2[3]/2)))
                        cv2.rectangle(img, risk2, color_list[1], thickness=2)
                        cv2.circle(img,center2,5,color_list[1],-1)
                        pts2.appendleft(center2)
                        centroid_center_r2 +=1
                        # if centroid_center_r1 > 2:
                        try:
                            pts_r2=[item for item in pts2]
                            pts_r2 = np.array(pts_r2)
                            thickness =  int(np.sqrt(36 / float(centroid_center_r2 + 1)) * 2.5)
                            dd = 0
                            for point1, point2 in zip(pts_r2,pts_r2[1:]):
                                if dd < 5:
                                    cv2.line(img, point1,point2, color_list[1], thickness=7)
                                    dd+=1
                                else:
                                    cv2.line(img, point1,point2, color_list[1], thickness)
                                    dd+=1
                            # cv2.line(img, pts[centroid_center_r1 - 2], pts[centroid_center_r1-1], color_list[0], thickness)
                            # cv2.line(img, pts1, color_list[0], thickness)
                        except:
                            print('skipped from 2nd object')

                    if value[3] != '':
                        risk3 = value[3]
                        risk3 = re.sub("[()]","", risk3)
                        risk3 = [int(i) for i in risk3.split(',')]
                        center3 = (int((risk3[0]+risk3[2]/2)),int((risk3[1]+risk3[3]/2)))
                        cv2.rectangle(img, risk3, color_list[2], thickness=2)
                        cv2.circle(img,center3,5,color_list[2],-1)
                        pts3.appendleft(center3)
                        centroid_center_r3 +=1
                        try:
                            pts_r3=[item for item in pts3]
                            pts_r3 = np.array(pts_r3)
                            thickness =  int(np.sqrt(36 / float(centroid_center_r3 + 1)) * 2.5)
                            ee = 0
                            for point1, point2 in zip(pts_r3,pts_r3[1:]):
                                if ee < 5:
                                    cv2.line(img, point1,point2, color_list[2], thickness=7)
                                    ee+=1
                                else:
                                    cv2.line(img, point1,point2, color_list[2], thickness)
                                    ee+=1
                        except:
                            print('skipped from 3rd object')
                    if value[4] != '':
                        risk4 = value[4]
                        risk4 = re.sub("[()]","", risk4)
                        risk4 = [int(i) for i in risk4.split(',')]
                        center4 = (int((risk4[0]+risk4[2]/2)),int((risk4[1]+risk4[3]/2)))
                        cv2.rectangle(img, risk4, color_list[3], thickness=2)
                        cv2.circle(img,center4,5,color_list[3],-1)
                        pts4.appendleft(center4)
                        centroid_center_r4 +=1
                        try:
                            pts_r4=[item for item in pts4]
                            pts_r4 = np.array(pts_r4)
                            thickness =  int(np.sqrt(36 / float(centroid_center_r4 + 1)) * 2.5)
                            ff = 0
                            for point1, point2 in zip(pts_r4,pts_r4[1:]):
                                if ff < 5:
                                    cv2.line(img, point1,point2, color_list[3], thickness=7)
                                    ff+=1
                                else:
                                    cv2.line(img, point1,point2, color_list[3], thickness)
                                    ff+=1
                        except:
                            print('skipped from 4th object')
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



if __name__ == '__main__':
    main()
