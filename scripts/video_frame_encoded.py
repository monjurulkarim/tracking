'''
Input: video frames directory
Output: mp4 video with frame number encoded on it
'''
import cv2
import os
from natsort import natsorted
import argparse
import sys
import csv
# import pandas as pd

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--frames_dir", default="output/videos/")
    parser.add_argument("--destination_dir", default = 'v04feb22/')
    args = parser.parse_args()
    return args




def video_generation(image_folder,video_name):
    images = natsorted([img for img in os.listdir(image_folder) if img.endswith(".jpg")])
    # sample_img = cv2.imread(images[0])
    sample_img = cv2.imread(os.path.join(image_folder, images[0]))

    # print(sample_img.shape)
    # for img in images:
    #     print(img)
    # images = images[frame_1:]
    # while len(images)<100:
    #     images.append(images[-1])
    # images = images[:100]
    #
    height, width, c = sample_img.shape
    #
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    video = cv2.VideoWriter(video_name, fourcc, 20, (width, height),True)
    print('======================')
    print(f"{video_name}...")
    #
    x,y,w,h = 0,0,60,35
    count = 0
    for i in images:
        img = cv2.imread(os.path.join(image_folder, i))
        # cv2.rectangle(img, (x, x), (x + w, y + h), (0,0,0), -1)
        cv2.rectangle(img, (x, y), (x + w, y + h), (0,0,0), -1)
        cv2.putText(
                    img,
                    str(count),
                    (x + int(w/10),y + int(h/2)), cv2.FONT_HERSHEY_SIMPLEX, 0.7, [255,255,255], 2,
                    cv2.LINE_AA)
        video.write(img)
        count += 1
    #
    cv2.destroyAllWindows()
    video.release()
    return

def main():
    args = get_args()
    frames_dir = args.frames_dir
    destination_dir = args.destination_dir
    if not os.path.exists(destination_dir):
        os.makedirs(destination_dir)

    folder_lists = os.listdir(frames_dir)
    for folder in folder_lists:
        frame_dir = os.path.join(frames_dir, folder)
        video_name = f"{destination_dir}{folder}.mp4"
        video_generation(frame_dir,video_name)

    return print('===========finished=============')





if __name__ == '__main__':
    main()
