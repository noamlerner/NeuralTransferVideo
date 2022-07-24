import cv2

'''
This script will open a video file and output every frame as a jpg to the output_folder
'''
video_file = "og.mp4"
output_folder = "trippiedog/"
vc = cv2.VideoCapture(video_file)
c = 1

if vc.isOpened():
    rval, frame = vc.read()
else:
    rval = False

while rval:
    rval, frame = vc.read()
    cv2.imwrite("{}/{}.jpg".format(output_folder, c), frame)
    c = c + 1
    cv2.waitKey(1)
    if c % 100 == 0:
        print("On frame {}".format(c))
vc.release()
