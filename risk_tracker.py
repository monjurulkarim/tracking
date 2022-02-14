import csv
import os
import re
import sys
import copy
import time
import argparse

import cv2 as cv
import logging


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--video_dir", default="../sample_movie/")
    parser.add_argument("--direction", type=str, default="forward", choices= ["forward","backward"], help='video direction forward or backward, default: forward')
    parser.add_argument("--files", default="michael_rain.csv")
    parser.add_argument("--destination_dir", default = 'tracking_results')
    parser.add_argument("--width", help='cap width', type=int, default=1080)
    parser.add_argument("--height", help='cap height', type=int, default=720)
    args = parser.parse_args()
    return args


def log_information(video_id):
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    file_handler = logging.FileHandler('completion_log.log')
    formatter = logging.Formatter('%(asctime)s:%(levelname)s:%(message)s')

    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    logger.info(f"---------{video_id}.mp4--Completed")
    return

class Tracking():
    def __init__(self, cap_width,cap_height, destination_dir, direction):
        self.color_list = [
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
        self.cap_width = cap_width
        self.cap_height = cap_height
        self.destination_dir = destination_dir
        self.direction = direction

    def isint(self, s):
        p = '[-+]?\d+'
        return True if re.fullmatch(p, s) else False

    def initialize_tracker(self, window_name, image):
        params = cv.TrackerDaSiamRPN_Params()
        params.model = "model/DaSiamRPN/dasiamrpn_model.onnx"
        params.kernel_r1 = "model/DaSiamRPN/dasiamrpn_kernel_r1.onnx"
        params.kernel_cls1 = "model/DaSiamRPN/dasiamrpn_kernel_cls1.onnx"
        tracker = cv.TrackerDaSiamRPN_create(params)

        # target selection
        while True:
            bbox = cv.selectROI(window_name, image)

            try:
                tracker.init(image, bbox)
            except Exception as e:
                print(e)
                continue

            return tracker

    def manner_collision(self,accident_type):
        if accident_type == '':
            print('===========================================================')
            print('What type of accident it was?')
            print('Please select an option from the below list:')
            print('1. Front to rear, 2. Front to front, 3. Angle, 4. Sideswipe same direction, 5. N/A , 6. Bad quality/Not usable')
            print('+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
            options= ['Front to rear', 'Front to front','Angle','Sideswipe same direction', 'N/A', 'Not usable']
            while True:
                try:
                    inp = int(input("Enter the number corresponding to the accident type : "))
                    if inp in range(len(options)+1):
                        value = options[inp-1]
                    else:
                        print('Wrong input type. You have to select a number between 1 to 6. Please try again.')
                        continue
                except ValueError:
                    print('Wrong input type. You have to select a number between 1 to 6. Please try again.')
                    continue
                else:
                    print('You have selected : ', value)
                    print('===========================================================')
                    break
        else:
            value = accident_type
        return value

    def unselection_logging(self,frame_num, object,window_name):
        #creating the header for the csv file
        # destination_dir = 'tracking_results/unselection_log/'
        destination_dir = self.destination_dir + '/'+'unselection_log/'
        if not os.path.exists(destination_dir):
            os.makedirs(destination_dir)
        unselection_csv_file = f"{destination_dir}/{window_name.split('.')[0]}.csv"
        with open(unselection_csv_file, 'a', newline= '') as f:
            writer = csv.writer(f)
            # writer.writerow(['frame','unselected object'])
            writer.writerow([frame_num, object])

        return print(f"Unselected objects list is saved at -{unselection_csv_file}")

    def tracking_object(self,video_file, destination_dir,accident_type):
        if self.isint(video_file):
            video_file = int(video_file)
        cap = cv.VideoCapture(video_file)
        cap.set(cv.CAP_PROP_FRAME_WIDTH, self.cap_width)
        cap.set(cv.CAP_PROP_FRAME_HEIGHT, self.cap_height)

        # Tracker initialize ############################################################
        window_name = video_file.split('/')[-1]
        cv.namedWindow(window_name)

        #creating the header for the csv file
        tracking_csv_file = f"{destination_dir}/{window_name.split('.')[0]}.csv"
        with open(tracking_csv_file, 'w', newline= '') as f:
            writer = csv.writer(f)
            writer.writerow(['frame','Risk_1', 'Risk_2', 'Risk3', 'Risk4'])
        f.close()

        count = 1

        while True:
            ret, image = cap.read()

            if not ret:
                try:
                    break
                except:
                    sys.exit("Can't read first frame")
            # cv.namedWindow(window_name)
            if self.direction == "forward":
                cv.putText(
                    image,
                    'Frame # ' + str(count),
                    (10, 25), cv.FONT_HERSHEY_SIMPLEX, 0.7, self.color_list[1], 2,
                    cv.LINE_AA)
            elif self.direction == "backward":
                cv.putText(
                    image,
                    'Frame # ' + str(100 -count),
                    (10, 25), cv.FONT_HERSHEY_SIMPLEX, 0.7, self.color_list[1], 2,
                    cv.LINE_AA)
            else:
                raise ValueError('please select direction from forward and backward')


            cv.imshow(window_name,image)


            #pause at the beginning of each video clip

            if count == 1:
                cv.waitKey()
            key = cv.waitKey(200) & 0xFF

            if key== ord('p'):
                cv.waitKey()



            if key == 32:

                tracker = self.initialize_tracker(window_name, image)

                #for the 2nd risky object if any
                tracker2 = None
                ok2 = None
                bbox2 = None

                #for the 3rd risky object if any
                tracker3 = None
                ok3 = None
                bbox3 = None

                #for the 4th risky object if any
                tracker4 = None
                ok4 = None
                bbox4 = None

                frame_num = 0

                while cap.isOpened():
                    tracked_frame = frame_num +  count
                    ret, image = cap.read()
                    if not ret:
                        break
                    debug_image = copy.deepcopy(image)

                    # Tracking update

                    start_time = time.time()
                    # ley = cv.waitKey(100)
                    k = cv.waitKey(100)

                    if tracker != None:
                        ok, bbox = tracker.update(image)
                        if k == ord('v'):
                            ok, bbox, tracker = None, None, None
                            self.unselection_logging(tracked_frame, 'risk1', window_name)

                    if tracker2 != None:
                        ok2,bbox2 = tracker2.update(image)

                        if k == ord('z'):
                            ok2,bbox2, tracker2 = None, None, None
                            self.unselection_logging(tracked_frame, 'risk2', window_name)

                    if tracker3 != None:
                        ok3,bbox3 = tracker3.update(image)
                        if k == ord('x'):
                            ok3, bbox3, tracker3 = None, None, None
                            self.unselection_logging(tracked_frame, 'risk3', window_name)

                    if tracker4 != None:
                        ok4,bbox4 = tracker4.update(image)
                        if k == ord('c'):
                            ok4, bbox4, tracker4 = None, None, None
                            self.unselection_logging(tracked_frame, 'risk4', window_name)


                    elapsed_time = time.time() - start_time
                    if ok:
                        # Bounding box drawing after tracking
                        cv.rectangle(debug_image, bbox, self.color_list[0], thickness=2)
                        with open(tracking_csv_file, 'a+',newline='') as tracking_box:
                            writer = csv.writer(tracking_box)
                            writer.writerow([tracked_frame,bbox, bbox2, bbox3,bbox4])
                    elif ok2:
                        with open(tracking_csv_file, 'a+',newline='') as tracking_box:
                            writer = csv.writer(tracking_box)
                            writer.writerow([tracked_frame,bbox, bbox2, bbox3,bbox4])
                    elif ok3:
                        with open(tracking_csv_file, 'a+',newline='') as tracking_box:
                            writer = csv.writer(tracking_box)
                            writer.writerow([tracked_frame,bbox, bbox2, bbox3,bbox4])
                    else:
                        with open(tracking_csv_file, 'a+',newline='') as tracking_box:
                            writer = csv.writer(tracking_box)
                            writer.writerow([tracked_frame,bbox, bbox2, bbox3,bbox4])

                    if ok2:
                        cv.rectangle(debug_image, bbox2, self.color_list[1], thickness=2)

                    if ok3:
                        cv.rectangle(debug_image, bbox3, self.color_list[2], thickness=2)
                    if ok4:
                        cv.rectangle(debug_image, bbox4, self.color_list[3], thickness=2)


                    # Processing time
                    if self.direction == "forward":
                        cv.putText(
                            debug_image,
                            'Frame # ' + str(tracked_frame),
                            (10, 25), cv.FONT_HERSHEY_SIMPLEX, 0.7, self.color_list[1], 2,
                            cv.LINE_AA)
                        cv.putText(
                            debug_image,
                            'DaSiamRPN' + " : " + '{:.1f}'.format(elapsed_time * 1000) + "ms",
                            (10, 50), cv.FONT_HERSHEY_SIMPLEX, 0.7, self.color_list[0], 2,
                            cv.LINE_AA)
                    elif self.direction == "backward":
                        cv.putText(
                            debug_image,
                            'Frame # ' + str(100-tracked_frame),
                            (10, 25), cv.FONT_HERSHEY_SIMPLEX, 0.7, self.color_list[1], 2,
                            cv.LINE_AA)
                    else:
                        print('Something is wrong')

                    # if tracked_frame == 99:
                    #     cv.waitKey()

                    cv.imshow(window_name, debug_image)

                    frame_num +=1


                    # k = cv.waitKey(100)
                    if k == 32:  # SPACE
                        # redesignation
                        tracker = self.initialize_tracker(window_name, image)
                    if k == ord('a'): # a

                        tracker2 = self.initialize_tracker(window_name, image)
                    if k == ord('s'): # s
                        tracker3 = self.initialize_tracker(window_name, image)
                    if k == ord('d'): # s
                        tracker4 = self.initialize_tracker(window_name, image)
                    if k == ord('p'): # Pause button
                        cv.waitKey()

                    if k == 27:  # ESC
                        self.unselection_logging(tracked_frame, 'all', window_name)
                        break

            try:
                count = tracked_frame
                count +=1
                tracked_frame = count

            except:
                count+=1

        cv.destroyAllWindows()
        value = self.manner_collision(accident_type)
        return value


def main():
    args = get_args()
    cap_width = args.width
    cap_height = args.height
    input_file = args.files
    if not os.path.exists(input_file):
        raise FileNotFoundError('Please check your input csv file name')
    tmp_file = f"{input_file}.tmp"


    video_dir = args.video_dir
    if not os.path.exists(video_dir):
        raise FileNotFoundError('Please check your input video folder name')
    direction = args.direction

    destination_dir1 = args.destination_dir
    destination_dir = os.path.join(destination_dir1,input_file.split('.')[0])
    if not os.path.exists(destination_dir):
        os.makedirs(destination_dir)

    track = Tracking(cap_width, cap_height,destination_dir,direction)

    with open(input_file, 'r', newline='') as csvfile, open(tmp_file, 'w+', newline='') as csvtempfile:
        writer = csv.writer(csvtempfile, delimiter=',')
        reader = csv.reader(csvfile, delimiter=',')
        for row in reader:
            video_id,frame_1,accident_frame,last_frame,accident_type,status= row

            if status == 'status':
                writer.writerow(row)
            elif status != 'Done':
                if video_id != 'video_id':
                    video_file = f"{video_dir}{video_id}.mp4"
                    assert os.path.exists(video_file)== True, f"video id -{video_id} from the csv file is not found in the input video directory. Please check again."
                    print('Reading :', video_file)
                    try:
                        accident_type = track.tracking_object(video_file, destination_dir,accident_type)
                    except KeyboardInterrupt:
                        window_name = video_file.split('/')[-1]
                        tracking_csv_file = f"{destination_dir}/{window_name.split('.')[0]}.csv"
                        print(f"interruptedupted at {video_id}")
                        os.remove(tracking_csv_file)
                        print('Removed -- ', tracking_csv_file)
                        unselected_log_dir = destination_dir + '/'+'unselection_log/'
                        unselection_csv_file = f"{unselected_log_dir}/{window_name.split('.')[0]}.csv"
                        if os.path.exists(input_file):
                            os.remove(unselection_csv_file)
                            print('Removed unselection log from-- ', unselection_csv_file)
                        sys.exit(0)
                    writer.writerow([video_id,frame_1,accident_frame,last_frame, accident_type, 'Done'])
                    log_information(video_id)
                else:
                    continue
            else:
                writer.writerow(row)
    os.remove(input_file)
    os.rename(tmp_file,input_file)

if __name__ == '__main__':
    main()
