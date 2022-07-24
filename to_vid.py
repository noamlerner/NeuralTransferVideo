import cv2
import glob
from trippyvid.transitioner import StyleTransition
from trippyvid.consts import st_output_dir

files = glob.glob(st_output_dir + "*.jpg")
'''
This script takes all trippified frames and creates a video
'''
imgs_per_frame = {}
num_frames = 1
last_i = 0
files.sort(key=lambda f: int(f.split("/")[-1].split("_")[0].split(".")[0]))
for f in files:
    if "_" not in f:
        continue
    i = int(f.split("/")[-1].split("_")[0].split(".")[0])
    if i != last_i + 1 and i != last_i:
        raise Exception("Missing frame: {}".format(last_i))
    last_i = i

for f in files:
    if "_" not in f:
        continue
    try:
        i = int(f.split("/")[-1].split("_")[0].split(".")[0])
    except:
        continue
    if i not in imgs_per_frame:
        imgs_per_frame[i] = []
    imgs_per_frame[i].append(f)
    if i > num_frames:
        num_frames = i

on_style = None
transition = None
img_array = []
if num_frames > 9360:
    num_frames = 9360
print("num frames {}".format(num_frames))
for i in range(1, num_frames):
    if i % 100 == 0:
        print("On frame: {} of {}".format(i, num_frames))

    filenames = imgs_per_frame[i]
    if len(filenames) == 1:
        on_style = filenames[0].split("/")[-1].split("_")[2].split(".")[0]
        transition = None
        img = cv2.imread(filenames[0])
    else:
        if transition is None:
            for j in range(i, num_frames):
                if len(imgs_per_frame[j]) == 1:
                    break
            print("transitioning from {} to {}".format(i, j))
            transition = StyleTransition(from_style=on_style, from_frame=i, to_frame=j, perform_file_operations=False)
        img = transition.transition_paths(filenames, img_num=i)

    height, width, layers = img.shape
    size = (width, height)
    img_array.append(img)

print("len array: {}".format(len(img_array)))
outname = st_output_dir.split("/")[-2]
out = cv2.VideoWriter("{}.mp4".format(outname), cv2.VideoWriter_fourcc(*'MP4V'), 30, size)
for i in range(len(img_array)):
    out.write(img_array[i])
    if i % 100 is 0:
        print("written: {} of {}".format(i, num_frames))
out.release()
