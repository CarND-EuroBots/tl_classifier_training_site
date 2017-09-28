#!/usr/bin/env python
from __future__ import print_function
import os
import argparse
import cv2
import  yaml
from PIL import Image

def parse_arguments():
    """ Parses the arguments sent from command line
        Returns: a struct with the value of the arguments
    """
    parser = argparse.ArgumentParser()

    parser.add_argument('-s', '--src', dest='src_path')
    parser.add_argument('-y', '--yaml', dest='yaml_filename')
    parser.add_argument('-d', '--dest', dest='dest_path')
    parser.add_argument('-f', '--force', dest='force')

    return parser.parse_args()

def move_file(args, path, category):
    if not os.path.exists(os.path.join(args.dest_path, category)):
        return
    filename = os.path.basename(path)
    if args.force:
        src_path = os.path.join(args.force, filename)
    else:
        src_path = os.path.join(args.src_path, path)
    filename_jpg = os.path.splitext(filename)[0] + '.jpg'
    dest_path = os.path.join(args.dest_path, category, filename_jpg)
    if os.path.exists(src_path):
        im = Image.open(src_path)
        im.save(dest_path)
        os.remove(src_path)


def main():
    """ Main function """
    # Parse arguments
    args = parse_arguments()

    if not os.path.exists(args.dest_path):
        os.mkdir(args.dest_path)
    if not os.path.exists(os.path.join(args.dest_path, "red")):
        os.mkdir(os.path.join(args.dest_path, "red"))
    if not os.path.exists(os.path.join(args.dest_path, "green")):
        os.mkdir(os.path.join(args.dest_path, "green"))
    if not os.path.exists(os.path.join(args.dest_path, "none")):
        os.mkdir(os.path.join(args.dest_path, "none"))
    if not os.path.exists(os.path.join(args.dest_path, "yellow")):
        os.mkdir(os.path.join(args.dest_path, "yellow"))

    file_path = os.path.join(args.src_path, args.yaml_filename)
    with open(file_path, 'r') as stream:
        try:
            annotations = yaml.load(stream)
            for annotation in annotations:
                boxes = annotation['boxes']
                path = annotation['path']
                if (len(boxes) == 0):
                    move_file(args, path, "none")
                else:
                    common_label  = boxes[0]['label']
                    skip_it = False
                    large_enough = False
                    for box in boxes:
                        label = box['label']
                        occluded = box['occluded']
                        if occluded or label != common_label:
                            skip_it = True
                            break;
                        x_diff = box['x_max'] - box['x_min']
                        y_diff = box['y_max'] - box['y_min']
                        if x_diff > 15 and y_diff > 30:
                            large_enough = True
                    if not skip_it and large_enough:
                       move_file(args, path, common_label.lower())

        except yaml.YAMLError as exc:
            print(exc)

    return 0

if __name__ == "__main__":
    exit(main())
