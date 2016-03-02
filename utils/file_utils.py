import os

def get_img_paths_in_dir(image_dir, suffix=".jpg"):
    """returns a list of full paths to files with 
    the given suffix in image_dir."""
    root, frames = get_imgs_in_dir(image_dir, suffix)
    img_paths = [root + '/' + frame for frame in frames]
    return img_paths

def get_imgs_in_dir(image_dir, suffix):
    """returns list of the files in the given
    directory with the given suffix, together 
    with the root path."""
    frames = []
    root = None
    for root, dirs, fnames in os.walk(image_dir):
        for fname in fnames:
            if has_suffix(fname, suffix):
                frames.append(fname)
        root = root
    return root, frames

def has_suffix(fname, suffix):
    """returns true if the file has the given suffix  
    and ignores hidden files sometimes created on ubuntu"""
    return fname.endswith(suffix) and not fname[::-1].endswith('_.')

def get_target_dir(path, selected_time):
    target_dir = path + selected_time + '/'
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)
    return target_dir
