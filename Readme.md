# Neural Transfer Video

This whole repo is a hack.

This is the code I used to make https://www.youtube.com/watch?v=TjGolWLh8ZM

## Usage

This was written in a directory that lived alongside a cloned version of
the [Magenta repo](https://github.com/magenta/magenta).

In order to get this to work, there are some edits I made to magenta after cloning.

Those changes can be found in the `arbitrary_image_stylization` folder. and should be copied into the folder with the
matching name in the `magenta` repo.

You'll also need to follow the instructions in that repo toset up magenta.

You can use any other library and edit the `run.py` to use that. I found magenta didn't have the best results, but it
was the fastest. When you're working on thousands of frames, that's super important.