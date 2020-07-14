from cv2 import cv2 as cv
import argparse
import numpy as np
import time
from utils import choose_run_mode, load_pretrain_model, set_video_writer
from Pose.pose_visualizer import TfPoseVisualizer
from Action.recognizer import load_action_premodel, framewise_recognize

parser = argparse.ArgumentParser(description='Action Recognition by OpenPose')
parser.add_argument('--video', help='Path to video file.')
args = parser.parse_args()

estimator = load_pretrain_model('VGG_origin')
action_classifier = load_action_premodel('Action/framewise_recognition.h5')

realtime_fps = '0.0000'
start_time = time.time()
fps_interval = 1
fps_count = 0
run_timer = 0
frame_count = 0

cap = choose_run_mode(args)
video_writer = set_video_writer(cap, write_fps=int(7.0))

# choosing analysis method
exercises = ["squats", "pushups", "situps"]
choice = ""

while choice not in exercises:
    choice = input("What exercise would you like to do today?\n")
    if choice not in exercises:
        print("That's not a valid option. Current exercises available are:")
        for workout in exercises:
            print(workout)

print(choice)

while cv.waitKey(1) < 0:
    has_frame, show = cap.read()
    if has_frame:
        fps_count += 1
        frame_count += 1

        # pose estimation
        humans = estimator.inference(show)
        # get pose info
        pose = TfPoseVisualizer.draw_pose_rgb(show, humans)  # return frame, joints, bboxes, xcenter
        try:
            # post-processing of info
            if  pose[1][0][4][1] - pose[1][0][2][1] < 200 and pose[1][0][7][1] - pose[1][0][5][1] < 200:
                print("PUSH")
        except:
            pass
        # recognize the action framewise
        show = framewise_recognize(pose, action_classifier)

        height, width = show.shape[:2]

        if (time.time() - start_time) > fps_interval:
            realtime_fps = fps_count / (time.time() - start_time)
            fps_count = 0 
            start_time = time.time()
        fps_label = 'FPS:{0:.2f}'.format(realtime_fps)
        cv.putText(show, fps_label, (width-160, 25), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)

        num_label = "Human: {0}".format(len(humans))
        cv.putText(show, num_label, (5, height-45), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)

        if frame_count == 1:
            run_timer = time.time()
        run_time = time.time() - run_timer
        time_frame_label = '[Time:{0:.2f} | Frame:{1}]'.format(run_time, frame_count)
        cv.putText(show, time_frame_label, (5, height-15), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)

        cv.imshow('Action Recognition based on OpenPose', show)
        video_writer.write(show)

video_writer.release()
cap.release()
