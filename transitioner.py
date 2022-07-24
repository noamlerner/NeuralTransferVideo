import os
import numpy as np
import glob
import shutil
import cv2
from trippyvid.consts import st_output_dir

class StyleTransition:
    def __init__(self, from_style, from_frame, to_frame, perform_file_operations=True):
        '''
        StyleTransition transitions some amount of frames from one style to another style smoothly
        Args:
            from_style: The beginning style
            from_frame: the first frame of the transition
            to_frame: the last frame of the transition
            perform_file_operations:
        '''
        self.from_style = "{}".format(from_style)
        self.to_style = None
        self.weight = 0.0
        self.num_frames = to_frame - from_frame
        self.from_frame = from_frame
        self.to_frame = to_frame
        self.perform_file_operations = perform_file_operations

    def transition(self, img_num):
        imgs = glob.glob("{}}/{}_*".format(st_output_dir, img_num))
        if len(imgs) != 2:
            raise Exception("Incorrect number of images")
        return self.transition_paths(imgs, img_num)

    def transition_paths(self, imgs, img_num=None):
        if self.from_style in imgs[0]:
            from_style_img_path = imgs[0]
            to_style_img_path = imgs[1]
        else:
            from_style_img_path = imgs[1]
            to_style_img_path = imgs[0]

        if self.to_style is None:
            self.to_style = to_style_img_path.split("/")[-1].split("_")[2].split(".")[0]

        to_style_img = cv2.imread(to_style_img_path)
        from_style_img = cv2.imread(from_style_img_path)

        img = self.dissolve(to_style_img, from_style_img)
        self.weight += 1 / self.num_frames
        return img.astype(np.uint8)

    def dissolve(self, to_style_img, from_style_img):
        img = self.weight * to_style_img
        img = img + (1 - self.weight) * (from_style_img)
        return img
