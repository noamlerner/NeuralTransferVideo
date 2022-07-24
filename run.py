import os
from trippyvid.Planner import Planner
import glob
from trippyvid.consts import st_output_dir, st_image_size
from trippyvid.StyleOpts import StyleOpts


def run_style_transfer(
        opts,
        o_dir=st_output_dir,
):
    '''
    given a StyleOpts, this will run style transfer.
    Args:
        opts:
        o_dir:
    '''
    base_dir = "/Users/nlerner/Snapchat/Dev/magenta/magenta/magenta/models/arbitrary_image_stylization/"
    script_path = base_dir + "arbitrary_image_stylization_with_weights.py"

    checkpoint = " --checkpoint=" + base_dir + "model/model.ckpt"
    output_dir = " --output_dir=" + o_dir
    style_images_paths = " --style_images_paths=" + opts.get_style()
    content_images_paths = " --content_images_paths=" + opts.get_content_path()
    image_size = " --image_size=[{}]".format(opts.i_size)
    content_square_crop = " --content_square_crop=False"
    style_image_size = " --style_image_size=[{}]".format(opts.get_style_size())
    style_square_crop = " --style_square_crop=False"
    interpolation_weights = " --interpolation_weights=[{}]".format(opts.get_interpolation_weight())
    logtostderr = " --logtostderr"

    cmd = "python " + script_path + checkpoint + output_dir + style_images_paths + content_images_paths + image_size + content_square_crop + style_image_size + style_square_crop + interpolation_weights + logtostderr
    print(cmd)
    os.system(cmd)


frames_path = "/Users/nlerner/Snapchat/Dev/magenta/magenta/trippyvid/frames/"
#  Plan out the video
p = Planner(frames_path, i_size=st_image_size)
i = 0
while len(p.opts) < 55:
    # Not enough styles, we will keep randomizing until we have more Opts.
    p = Planner(frames_path, i_size=st_image_size)
    i += 1
    if i % 1000 is 0:
        print("searched through: {} most recent len {}".format(i, len(p.opts)))
print(len(p.opts))

# Run style transfer
for i in range(len(p.opts)):
    print("Running opts for {} frames with style {}".format(p.opts[i].num_frames, p.opts[i].style_path))
    run_style_transfer(p.opts[i])


def test_styles():
    #  use this to test a style and see if it looks nice
    styles = glob.glob(
        "/Users/nlerner/Snapchat/Dev/Neural-Style-Transfer/images/inputs/style/*")
    for s in styles:
        opt = StyleOpts(["/Users/nlerner/Desktop/bass.jpeg"], 1)
        opt.style_path = s
        for size in [1024, 2360]:
            opt.i_size = size
            run_style_transfer(opt)
