from __future__ import division

import os
import PIL
import dlib
import numpy as np
from tqdm import tqdm
from skimage import io

from crop_tool.utils.file_utils import get_img_paths_in_dir
from crop_tool.settings import MODEL_PATH


def get_bounding_boxes(dets):
    """returns a list of dictionaries containing
    the bounding vertices of each detection."""
    bounding_boxes = []
    for box in dets:
        bounding_box = {'top_left_x': box.left(),
                        'top_left_y': box.top(),
                        'bottom_right_x': box.right(),
                        'bottom_right_y': box.bottom()}
        bounding_boxes.append(bounding_box)
    return bounding_boxes

def crop_frame(frame, crop_region):
    """returns cropped frame using the values specified by
     'crop_region'."""
    tl_x = crop_region['top_left_x'] 
    tl_y = crop_region['top_left_y']
    br_x = crop_region['bottom_right_x']
    br_y = crop_region['bottom_right_y']
    return frame[tl_y:br_y, tl_x:br_x]

def find_square_box(box):
    """returns the smallest possible square box containing
    within it the rectangle defined by box."""
    width = box['bottom_right_x'] - box['top_left_x']
    height = box['bottom_right_y'] - box['top_left_y']
    if width <= height:
        offset = int((width - height) / 2)
        box['top_left_x'] = box['top_left_x'] - offset
        box['bottom_right_x'] = box['bottom_right_x'] + offset
    else:
        offset = int((height - width) / 2)
        box['top_left_y'] = box['top_left_y'] - offset
        box['bottom_right_y'] = box['bottom_right_y'] + offset
    return box

def is_valid(box, img):
    """returns true if the given box is contained within
    the dimensions of the image."""
    valid_width = box['top_left_x'] > 0 and box['bottom_right_x'] < img.shape[1]
    valid_height = box['top_left_y'] > 0 and box['bottom_right_y'] < img.shape[0]
    return valid_width and valid_height                                                                  

def get_subdirs(src_dir):
    """returns the subfolers in the given directory."""
    img_dirs = sorted(next(os.walk(src_dir))[1])
    subdirs = [src_dir + img_dir for img_dir in img_dirs]
    return subdirs
    
def convert_dataset(src_dir, dest_dir, idx):
    """converts the dataset of colour face images to 
    54 x 54 greyscale crops of the faces."""
    subdirs = get_subdirs(src_dir)
    detector = dlib.simple_object_detector(MODEL_PATH)
    for img_dir in tqdm(subdirs[idx[0]:idx[1]]):
	print(img_dir)
        jpegs = get_img_paths_in_dir(img_dir)
        target_dir = dest_dir + img_dir.split('/')[-1]
        if not os.path.exists(target_dir):
            os.makedirs(target_dir)
        for src_path in jpegs:
            target_path = target_dir + '/' + src_path.split('/')[-1]
            img = io.imread(src_path)
            dets = detector(img)
            bounding_boxes = get_bounding_boxes(dets)
            if bounding_boxes:
                square_box = find_square_box(bounding_boxes[0])
                if is_valid(square_box, img):
                    box = bounding_boxes[0]
                    square_box = find_square_box(box)
                    cropped_img = crop_frame(img, square_box)
                    PIL_img = PIL.Image.fromarray(cropped_img)
                    resized_img = PIL_img.resize((54,54), PIL.Image.BILINEAR)
		    resized_img.save(target_path)
                    # grey_img = resized_img.convert('L')
                    # grey_img.save(target_path)

    
