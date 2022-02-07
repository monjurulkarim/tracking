'''
This script trims a video based on the timestamp written in a csv file.
Input: a long video + csv file
Output: splitted video clips.
======csv file should look like below=====
url | timestamps | convert_to_gif | status
-------------------------------------------------
v_1.mp4 | 00:00-03:34;3:39-08:16 | | |
'''

from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
import csv
import os


input_file = 'v_1.csv'
tmp_file = f"{input_file}.tmp"

def converter(url, timestamps):
    print('url : ', url)
    video_dir = url
    video_name = video_dir.split('.')[0]

    timestamps = timestamps.split(';')
    times = []
    for time in timestamps:
        t = time.split('-')
        start_time = int(t[0].split(':')[0])*60+int(t[0].split(':')[1]) #converts to seconds
        end_time = int(t[1].split(':')[0])*60+int(t[1].split(':')[1]) #converts to seconds
        target_name = f"{video_name}_{start_time}.mp4"
        ffmpeg_extract_subclip(url, start_time, end_time, targetname=target_name)
        print('============================')
    return

with open(input_file, 'r', newline='') as csvfile, open(tmp_file, 'w+', newline='') as csvtempfile:
    reader = csv.reader(csvfile, delimiter=',')
    writer = csv.writer(csvtempfile, delimiter=',')
    for row in reader:
        url,timestamps,convert_to_gif,status = row
        if status =='status':
            writer.writerow(row)
        elif status != 'ok':
            converter(url,timestamps)
