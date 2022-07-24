from trippyvid.StyleOpts import StyleOpts
from trippyvid.transitioner import StyleTransition
import os
import numpy as np
from trippyvid.consts import st_image_size
import glob

#     This contains all the styles we may use for trippifying an image
style_folder = "/Users/nlerner/Snapchat/Dev/magenta/magenta/trippyvid/styles/*"
styles = glob.glob(
    style_folder)


class Planner:
    def __init__(self, frames_path,
                 i_size=st_image_size,
                 starting_frame=1,
                 transition_length=(30, 90),
                 style_length=(30, 210),
                 ):
        '''
        Planner
            The planner will take a video and section off into different "StyleOpts". A StyleOpt is a contiguous
            list of frames that will all have one style.
            StyleOpts will overlap. An overlap means there is a transition going on.
            This essentially "Plans" what the video will look like.
        Args:
            frames_path: Stylized frames of the video
            i_size:  how large are the output images
            starting_frame: The first frame in frames path to start from. Defaults to 1, but allows you to "contuinue
                where you left off" if you interrupted execution
            transition_length: A range of frames. Transitions between frames will be randomized between these two values
            style_length: A range of frames. The total amount of time for a frame will be randomzied between these two values.
        '''
        self.styles = []
        num_frames = len(os.listdir(frames_path))

        last_frame = starting_frame
        last_transition_length = 30
        opts = []

        while last_frame < num_frames:
            s_length = np.random.randint(style_length[0], style_length[1])
            t_length = np.random.randint(transition_length[0], transition_length[1])
            s_length += last_transition_length

            s_end = last_frame + s_length
            t_end = s_end + t_length

            content_paths = ["'{}{}.jpg'".format(frames_path, i) for i in range(last_frame, t_end)]
            opt = StyleOpts(i_size=i_size, content_paths=content_paths, num_frames=s_length + t_length)
            if self.styles is None or len(self.styles) is 0:
                self.generate_available_styles()
            opt.style_path = self.styles.pop()

            last_frame = s_end
            last_transition_length = t_length
            if len(opts) > 0:
                while opt.style_path == opts[-1].style_path:
                    opt.roll_style()
            opts.append(opt)

        self.opts = opts

    def generate_content_path(self, fn):
        "{}{}.jpg".format(self.frames_path, fn)

    def generate_available_styles(self):
        self.styles = []
        self.styles.extend(styles)
        self.styles.extend(styles)
        self.styles = np.random.permutation(self.styles)
        self.styles = list(self.styles)


frames_path = "/Users/nlerner/Snapchat/Dev/magenta/magenta/trippyvid/frames/"
