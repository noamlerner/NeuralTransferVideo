import os
import numpy as np
import glob
from PIL import Image
import shutil
from trippyvid.consts import st_image_size

base_dir = "/Users/nlerner/Snapchat/Dev/magenta/magenta/magenta/models/arbitrary_image_stylization/"
styles = glob.glob(
    "/Users/nlerner/Snapchat/Dev/Neural-Style-Transfer/images/inputs/style/*")
style_sizes = [128, 128, 128, 256, 256, 256, 512, 512, 1024]


class StyleOpts:
    def __init__(self,
                 content_paths,
                 num_frames,
                 i_size=st_image_size
                 ):
        '''
        A StyleOpt is a contiguous list of frames that will all have one style.
        This describes one section of a video with one style. It is initialized with a set of filenames it will write to.
        It knows how many frames it has and  the output image size. It will select a random style to use for
        all these frames.
        Args:
            content_paths: what are the output files that will written?
            num_frames: How many frames this will cover
            i_size: Size of output image
        '''
        self.i_size = i_size
        self.content_paths = content_paths
        self.num_frames = num_frames

        self.roll_style()
        self.style_frame_change = 150
        self.frames_since_transition = 0
        self.transition = None

        self.style_size = np.random.randint(0, len(style_sizes))
        self.interpolation_weight = 1.0

    def get_style(self):
        if self.transition is None:
            return self.style_path
        else:
            return "{}*".format(transition_dir_path)

    def get_interpolation_weight(self):
        return self.interpolation_weight

    def get_style_size(self):
        return style_sizes[self.style_size]

    def get_content_path(self):
        return ",".join(self.content_paths)

    def roll_style(self):
        self.style_path = np.random.choice(styles)


transition_dir_path = "/Users/nlerner/Snapchat/Dev/magenta/magenta/trippyvid/style_transition/"
