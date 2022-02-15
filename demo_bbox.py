'''
Input: folders containing videos + csv files
Output: tracked .mp4 videos
Input folder (--input_video) structure:
-------------------------
--Sample_movie
    |-26_M.mp4
    |-27_M.mp4
    ...
    ...
--------------------------

bbox_dir (--bbox_dir) should be as below:
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
from scripts.video_frame_encoded import video_generation
import sys
import os.path as osp
import shutil

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input_video", default="../sample_movie") #frames directory
    parser.add_argument("--bbox_dir", default="./tracking_results/michael_rain/") #csv files directory
    parser.add_argument("--destination_dir", default="demo_results/") # demo video will be saved here
    parser.add_argument("--demo_frame_dir", default="backward_extracted/") # from the demo video converted frames will be saved here
    parser.add_argument("--direction", type=str, default="forward", choices= ["forward","backward"], help='video direction forward or backward, default: forward')
    args = parser.parse_args()
    return args

def FrameExtract(input_dir,destination_dir,*args):
    # video_list = os.listdir(input_dir)
    video_list = natsorted([vid for vid in os.listdir(input_dir) if vid.endswith(".mp4")])

    assert len(video_list) != 0, "No videos in the input directory"

    if not os.path.exists(destination_dir):
        os.makedirs(destination_dir)

    count =0
    for i in range(len(video_list)):
        filename = os.path.join(input_dir,video_list[i])

        video_list[i]
        vname_slice = video_list[i].split('.')
        # print(vname_slice[0])

        cap = cv2.VideoCapture(filename)
        fps = round(cap.get(cv2.CAP_PROP_FPS))
        # print(fps)
        images =[]


    #     check if capture was successful
        if not cap.isOpened():
            print("Could not open!")
        else:
            # print("Video read successful!")
            total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            print('Extracting frames from: ', video_list[i])
            for loop in range(total_frames):
                cap = cv2.VideoCapture(filename)
                cap.set(1,loop)
                success = cap.grab()
                ret, image = cap.retrieve()
                try:
                    if args:
                        for arg in args:
                            image = cv2.resize(image,arg)
                    frame_name = vname_slice[0] +'_frame_%d.jpg' %loop
                    images.append(frame_name)
                    saved_path = '/'+ vname_slice[0]

                    destination_2 = destination_dir + saved_path

                    if not os.path.exists(destination_2):
                        os.makedirs(destination_2)

                    saved_dir = osp.join(destination_2, frame_name)

                    cv2.imwrite(saved_dir,image)
                except:
                    # print('it is here')
                    continue
        count = count + 1
        cap.release()
        cv2.destroyAllWindows()
    print('+++++++++++++++++++++++++++++')
    if args:
        print(f'Extracted frames have been resized to {args[0]}')
    print(f'Total {count} video/s completed.')
    print('+++++++++++++++++++++++++++++')
    return

def frame_extract(input):
    print('---Frame extracting---')
    destination_dir = '../demo_frames'
    if not os.path.exists(destination_dir):
        os.makedirs(destination_dir)
    FrameExtract(input,destination_dir)
    print('--Frame extraction completed---')
    return destination_dir

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
    direction = args.direction
    # input_video_list = os.listdir(input_video)



    input_video = frame_extract(input_video)
    print('-----Demo generation started-----')

    bbox_dir = args.bbox_dir
    input_video_list = natsorted([file for file in os.listdir(input_video)])
    for folder in input_video_list:
        if not os.path.exists(args.destination_dir):
            os.makedirs(args.destination_dir)
        video_name = f"{args.destination_dir}{folder}.mp4"
        # if not os.path.exists(video_name):
        #     os.makedirs(video_name)
        image_folder = os.path.join(input_video,folder)
        # print('image_folder : ', image_folder)
        images = natsorted([img for img in os.listdir(image_folder) if img.endswith(".jpg")])
        if direction=="backward":
            images = [ele for ele in reversed(images)]
        bbox_csv = f"{bbox_dir}{folder}.csv"
        print('bbox_csv ',bbox_csv)

        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        video = cv2.VideoWriter(video_name, fourcc, 20, (width, height))
        print('======================')
        print(f"{video_name}...")

        with open(bbox_csv,'r', newline = '') as csvfile:
            reader = csv.reader(csvfile,delimiter=',')
            heading = next(reader)
            try:
                value = next(reader)
            except:
                print('No tracking information found for ', video_name)
                pass
            for i in range(100):
                img = cv2.imread(os.path.join(image_folder, images[i]))
                if i< int(value[0]):
                    video.write(img)
                elif i == int(value[0]):
                    if value[1] != '':
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
    if direction == 'backward':
        '''
        Will convert video frames from the created demo
        '''
        input_dir =args.destination_dir
        destination_dir = args.demo_frame_dir
        folder_lists = os.listdir(destination_dir)

        '''
        Converted video frames will be joined to create a video and will replace the original backward
        video. Thus as a final video we will get a forward going video.
        '''
        for folder in folder_lists:
            video_name = f"{args.destination_dir}{folder}.mp4"
            frame_dir = os.path.join(destination_dir, folder)
            video_generation(frame_dir, video_name, direction)
    return shutil.rmtree(input_video)



if __name__ == '__main__':
    main()
