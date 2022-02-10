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
    parser.add_argument("--data_dir", default="../../../../tracking/")
    parser.add_argument("--direction", type=str, default="forward", choices= ["forward","backward"], help='video direction forward or backward, default: forward')
    parser.add_argument("--frames_dir", default="demo/")
    parser.add_argument("--destination_dir", default = 'regular/')
    args = parser.parse_args()
    return args




def video_generation(image_folder,video_name):
    if direction == "forward":
        images = natsorted([img for img in os.listdir(image_folder) if img.endswith(".jpg")])
    elif direction == "backward":
        images = [ele for ele in reversed(images)] #for reversed video
    else:
        print("something is not right")
    sample_img = cv2.imread(os.path.join(image_folder, images[0]))

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
        if direction == "forward":
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
    data_dir = args.data_dir
    frames_folder = data_dir +args.frames_dir
    direction = args.direction
    frames_dir = os.path.abspath(os.path.join(__file__ ,frames_folder))
    destination_folder = data_dir + args.destination_dir + '/'
    destination_dir = os.path.abspath(os.path.join(__file__ ,destination_folder))

    if not os.path.exists(destination_dir):
        os.makedirs(destination_dir)

    folder_lists = os.listdir(frames_dir)
    for folder in folder_lists:
        frame_dir = os.path.join(frames_dir, folder)
        video_name = f"{destination_dir}{folder}.mp4"
        video_generation(frame_dir,video_name,direction)

    return print('===========finished=============')





if __name__ == '__main__':
    main()
