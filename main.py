import cv2
import numpy as np

video1 = cv2.VideoCapture('samples/sample1.mp4')
video2 = cv2.VideoCapture('samples/sample2.mp4')
background = cv2.imread('samples/bg.jpeg')
logo = cv2.imread('samples/logo.jpeg')
save_name = "output.mp4"
fps = video1.get(cv2.CAP_PROP_FPS)
width = 690
height = 360
output_size = ((width * 2), height)

fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter(save_name, fourcc, fps, output_size)


def add_bg(bg, video, alpha=1.0, x=0, y=0, scale=1.0):
    (h, w) = bg.shape[:2]
    bg = np.dstack([bg, np.ones((h, w), dtype="uint8") * 255])
    overlay = cv2.resize(video, None, fx=scale, fy=scale)
    (wH, wW) = overlay.shape[:2]
    output = bg.copy()

    try:
        if x < 0: x = w + x
        if y < 0: y = h + y
        if x + wW > w: wW = w - x
        if y + wH > h: wH = h - y
        print(x, y, wW, wH)
        overlay = cv2.addWeighted(output[y:y + wH, x:x + wW], alpha, overlay[:wH, :wW], 1.0, 0)
        output[y:y + wH, x:x + wW] = overlay
    except Exception as e:
        print("Error: Video position is overshooting bg!")
        print(e)
    output = output[:, :, :3]
    return output


def connect_frame(frame1, frame2, width, height):
    frame2 = cv2.resize(frame2, (int(width), int(height)), interpolation=cv2.INTER_AREA)
    bg = cv2.resize(frame1, (int(width + width), int(height)), interpolation=cv2.INTER_AREA)
    bg[0:int(height), 0:int(width)] = frame1
    bg[0:int(height), int(width):int(width + width)] = frame2
    return (bg)


while True:

    ret1, frame1 = video1.read()
    ret2, frame2 = video2.read()
    print(ret1)

    if ret1 is not False and ret2 is not False:

        frame = connect_frame(frame1, frame2, width, height)
        frame = cv2.copyMakeBorder(frame, 20, 20, 20, 20, cv2.BORDER_CONSTANT, value=[255, 255, 255])


        background = cv2.resize(background, (int(20), int(height+40)), interpolation=cv2.INTER_AREA)
        img_height, img_width, _ = background.shape
        x = 0
        y = 0
        frame[x:x+img_height, y:y+img_width] = background

        logo = cv2.resize(logo, (int(100), int(100)), interpolation=cv2.INTER_AREA)
        img_height, img_width, _ = logo.shape
        x = 10
        y = 10
        frame[x:x + img_width, y:y + img_height] = logo

        cv2.imshow('Video frame', frame)  # for video showing window
        out.write(cv2.resize(frame, output_size))

        key = cv2.waitKey(1)
        if key != ord('q'):
            continue
        break
    else:
        print("video is not found")
    break
out.release()
cv2.destroyAllWindows()
