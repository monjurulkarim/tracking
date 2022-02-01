import cv2
import os
from natsort import natsorted
import argparse
import sys
import csv
# import pandas as pd

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--frames_dir", default="../files_frames")
    parser.add_argument("--csv_file", default="file_list.csv")
    parser.add_argument("--destination_dir", default = '../sample_movie/')
    args = parser.parse_args()
    return args



def video_generation(image_folder, video_name, frame_1):
    images = natsorted([img for img in os.listdir(image_folder) if img.endswith(".jpg")])
    images = images[frame_1:]
    while len(images)<100:
        images.append(images[-1])
    images = images[:100]

    height, width = 720, 1080

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    video = cv2.VideoWriter(video_name, fourcc, 20, (width, height))
    print('======================')
    print(f"{video_name}...")

    for i in images:
        # print(i)
        img = cv2.imread(os.path.join(image_folder, i))
        video.write(img)

    cv2.destroyAllWindows()
    video.release()
    return

def main():
    args = get_args()
    input_file = args.csv_file
    frames_dir = args.frames_dir
    destination_dir = args.destination_dir
    if not os.path.exists(destination_dir):
        os.makedirs(destination_dir)

    # data = pd.read_csv(input_file, header=None)
    # print(data)


    with open(input_file, 'r', newline='') as csv_file:
        reader =csv.reader(csv_file,delimiter=',')
        heading = next(reader)
        for row in reader:
            video_id,frame_1,accident_frame,last_frame,status,accident_type = row
            image_folder = os.path.join(frames_dir,video_id)
            # print(image_folder)
            video_name = f"{destination_dir}{video_id}.mp4"
            video_generation(image_folder,video_name, int(frame_1))

    return print('----Finished----')




if __name__ == '__main__':
    main()
