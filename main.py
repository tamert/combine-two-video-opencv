import cv2
# import numpy as np
# import subprocess
import multiprocessing as mp
from collections import deque
from multiprocessing.pool import ThreadPool

video1 = cv2.VideoCapture('samples/sample1.mp4')
video2 = cv2.VideoCapture('samples/sample2.mp4')

# video2 = cv2.VideoCapture(0)
# if not (video2.isOpened()):
#      print("Could not open video device")


bar = cv2.imread('samples/bg.jpg')
logo = cv2.imread('samples/logo.jpeg')
save_name = "output.mp4"
fps = video2.get(cv2.CAP_PROP_FPS)
width = 690
height = 360
output_size = ((width * 2), height)

fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter(save_name, fourcc, fps, output_size)


def connect_frame(left_frame, right_frame, box_width, box_height):
    right_frame = cv2.resize(right_frame, (int(box_width), int(box_height)), interpolation=cv2.INTER_AREA)
    cover = cv2.resize(left_frame, (int(box_width + box_width), int(box_height)), interpolation=cv2.INTER_AREA)
    cover[0:int(box_height), 0:int(box_width)] = left_frame
    cover[0:int(box_height), int(box_width):int(box_width + width)] = right_frame
    return cover


def render_template(main_frame, logo_image, bar_image, border_size=20):
    main_frame = cv2.copyMakeBorder(main_frame, border_size, border_size, border_size, border_size,
                                    cv2.BORDER_CONSTANT, value=[255, 255, 255])

    frame_height, frame_width, _ = main_frame.shape

    y = 0
    x = 0
    x_bar = bar_image[x:frame_height, y:border_size]
    # added left bar
    img_height, img_width, _ = x_bar.shape
    main_frame[x:x + img_height, y:y + img_width] = x_bar

    y = frame_width - border_size
    x = 0
    x_bar = bar_image[x:frame_height, y:y + border_size]
    # added right bar
    img_height, img_width, _ = x_bar.shape
    main_frame[x:x + img_height, y:y + img_width] = x_bar

    y = 0
    x = 0
    y_bar = bar_image[x:border_size, y:frame_width]
    # added top bar
    img_height, img_width, _ = y_bar.shape
    main_frame[x:x + img_height, y:y + img_width] = y_bar

    y = 0
    x = frame_height - border_size
    y_bar = bar_image[x:x + border_size, y:frame_width]
    # added bottom bar
    img_height, img_width, _ = y_bar.shape
    main_frame[x:x + img_height, y:y + img_width] = y_bar

    logo = cv2.resize(logo_image, (int(100), int(100)), interpolation=cv2.INTER_AREA)
    img_height, img_width, _ = logo.shape
    x = border_size
    y = border_size
    main_frame[x:x + img_width, y:y + img_height] = logo

    return main_frame


if __name__ == '__main__':
    mp.freeze_support()
    pool = ThreadPool(processes=mp.cpu_count())
    pending_task = deque()

    while True:
        # print(len(pending_task))

        while len(pending_task) > 0 and pending_task[0].ready():
            res = pending_task.popleft().get()
            # cv2.imshow('threaded video', res) ıf you want to see ın guı
            out.write(cv2.resize(res, output_size))

        if len(pending_task) < mp.cpu_count():

            ret1, frame_1 = video1.read()
            ret2, frame_2 = video2.read()

            if ret1 is not False and ret2 is not False:
                frame = connect_frame(frame_1, frame_2, width, height)
                task = pool.apply_async(render_template, (frame.copy(), logo.copy(), bar.copy(),))
                pending_task.append(task)

                key = cv2.waitKey(1)
                if key != ord('q'):
                    continue
                break
            else:
                print("video is not found")
            break
    out.release()
    cv2.destroyAllWindows()
