import cv2

video1 = cv2.VideoCapture('samples/sample1.mp4')
video2 = cv2.VideoCapture('samples/sample2.mp4')
save_name = "output.mp4"
fps = video1.get(cv2.CAP_PROP_FPS)
width = 690
height = 360
output_size = ((width * 2), height)

fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter(save_name, fourcc, fps, output_size)


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
        frame = cv2.resize(frame, output_size, interpolation=cv2.INTER_AREA)

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
