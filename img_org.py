import struct
import imghdr
from wand.image import Image
from wand.display import display
from magic import *
import re
import os

# pretty size
def size_fmt(num, suffix='b'):
    for note in ['','k','m','g','t','p','e','z']:
        if abs(num) < 1024.0:
            return '%3.1f%s%s' % (num, note, suffix)
        num /= 1024.0
    return '%.1f%s%s' % (num, 'y', suffix)


# get img size
def ret_img_size(fname):	
    with open(fname, 'rb') as fd:
        head = fd.read(24)
        if len(head) != 24:
            return
        if imghdr.what(fname) == 'png':
            check = struct.unpack('>i', head[4:8])[0]
            if check != 0x0d0a1a0a:
                return
            width, height = struct.unpack('>ii', head[16:24])
        elif imghdr.what(fname) == 'gif':
            width, height = struct.unpack('<HH', head[6:10])
        elif imghdr.what(fname) == 'jpeg':
            try:
                fd.seek(0) # Read 0xff next
                size = 2
                ftype = 0
                while not 0xc0 <= ftype <= 0xcf:
                    fd.seek(size, 1)
                    byte = fd.read(1)
                    while ord(byte) == 0xff:
                        byte = fd.read(1)
                    ftype = ord(byte)
                    size = struct.unpack('>H', fd.read(2))[0] - 2
                # We are at a SOFn block
                fd.seek(1, 1)  # Skip `precision' byte.
                height, width = struct.unpack('>HH', fd.read(4))
            except Exception: #IGNORE:W0703
                return
        else:
            return
        return width, height


# If get_img_size fails
#def alt_get_img_size(fname):


def get_img_size_in_bytes(img_file):
    statinfo = os.stat(img_file)
    s = size_fmt(statinfo.st_size)
    return s

def ret_img_dict(path):

    dict_of_imgs = {}

    for paths, dirnames, fnames in os.walk(path, topdown=True):

        img_w, img_h = ret_img_size(fnames)
        img_b_size = get_img_size_in_bytes(fnames)

        dict_of_imgs.append(
            {'path_to_file': paths, 'dirs': dirnames,
            'filenames': fnames, 'pic_widths':img_w,
            'pic_heights': img_h, 'pic_sizes':img_b_size})

    return dict_of_imgs

# make dirs for images 

def build_img_dir_tree(dict_of_imgs):
    


# returns True or false
def is_img_sq_or_rect(full_path_img):


# scale image to nearest size
def img_rounder(img):

# main 
def img_org():

# scan build dirt by size "icons, pics, images, photos"
