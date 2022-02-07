import cv2
import os
import os.path as osp

def FrameExtract(input_dir,destination_dir,*args):
    video_list = os.listdir(input_dir)
    assert len(video_list) != 0, "No files in the input directory"

    if not os.path.exists(destination_dir):
        os.makedirs(destination_dir)

    count =0
    for i in range(len(video_list)):
        filename = os.path.join(input_dir,video_list[i])
        video_list[i]
        vname_slice = video_list[i].split('.')
        print(vname_slice[0])

        cap = cv2.VideoCapture(filename)
        fps = round(cap.get(cv2.CAP_PROP_FPS))
        print(fps)
        images =[]


    #     check if capture was successful
        if not cap.isOpened():
            print("Could not open!")
        else:
            print("Video read successful!")
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
