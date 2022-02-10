from moviepy.editor import *

# loading video dsa gfg intro video and getting only first 5 seconds
clip1 = VideoFileClip("demo_results_forward/GN_1111_1117.mp4")

# rotating clip1 by 90 degree to get the clip2
clip2 = VideoFileClip("demo_results_backward/GN_1111_1117.mp4")


# list of clips
clips = [[clip1, clip2]]


# stacking clips
final = clips_array(clips)
final.write_videofile('combined_GN_1111_1117.mp4')

# showing final clip
# final.ipython_display(width = 480)
