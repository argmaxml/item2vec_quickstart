# Item2vec quickstart

A cookie cutter project for item2vec based experiments.
# Directory Strcture
1. `src` - This is where your python code is
1. `data` - This is where your data is stored or intermediate steps are saved
1. `notebooks` - For experiments, excluded from Docker

# Docker cheat sheet

## Create image
  docker build -t tag_name .
## Run it
  docker run -it -p5000:5000 tag_name
## Image
  docker image list
## Deleting an image
  docker image rm -f <image_id>
