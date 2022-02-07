'''
Extract video frames
Input: folder containing videos
Output: extracted video frames
'''

from src.frame_extract import FrameExtract


input_dir = './input/' #Directory that contains the videos, you
                        #want to extract frames
destination_dir = './output/' #destination directory where extracted frames
                                # will be stored. For each video it will create
                                # separate subfolder by each video's name
# dim = (1080,720) #optional

# FrameExtract(input_dir,destination_dir,dim)
FrameExtract(input_dir,destination_dir)
