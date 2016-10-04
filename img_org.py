from wand.image import Image
from wand.display import display
import struct
import imghdr
import shutil
import os

# pretty size
def size_fmt(num, suffix='b'):
    for note in ['','K','M','G','T','P','E','Z']:
        if abs(num) < 1024.0:
            return '{:.1f}{}{}'.format(float(num), note, suffix)
        num /= 1024.0
    return '{:.1f}{}{}'.format(float(num), 'y', suffix)


# return image width and height
def ret_img_size(fname):
    with Image(filename=fname) as img:
        return str(img.size[0]), str(img.size[1]) 


# get img width and height when no wand
def ret_img_size_nowand(fname):	
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

# return dict of images
def ret_img_dict(path):

    dict_of_imgs = []

    for fd in os.scandir(path):
        if fd.name.startswith('.') or fd.is_dir() or fd.is_symlink():
            pass
        else:
            d = fd.path.replace(fd.name,'')
            img_w, img_h = ret_img_size(fd.path)
            img_b_size = fd.stat().st_size

            dict_of_imgs.append(
                {'directory': d,
                 'full_path': fd.path,
                 'width': img_w,
                 'height': img_h,
                 'size': img_b_size, 
                 'file_name': fd.name}
                )

    return dict_of_imgs

# build directory tree and move images into the 
# new dst
def build_img_dir_tree_n_move(dict_of_imgs):
    
    for x in dict_of_imgs:

        if(int(x['width']) == int(x['height']) and int(x['width']) <= 512):

            dir_x = '{}icons_{}x{}'.format(
                x['directory'], str(x['width']), str(x['height']))

            # make directory if it doesnt
            if(os.path.exists(dir_x)):
                pass
            else:
                os.mkdir(dir_x)

            src_image = '{}'.format(x['full_path'])
            dst_image = '{}/{}'.format(dir_x, x['file_name'])

            # move file to new location
            shutil.move(src_image, dst_image)
            print('moved {} {}.'.format(x['full_path'], size_fmt(x['size'])))


        elif(int(x['width']) != int(x['height']) and int(x['width']) < 1920):

            dir_x = '{}images_{}x{}'.format(
                x['directory'], str(x['width']), str(x['height']))

            # make directory if it doesnt
            if(os.path.exists(dir_x)):
                pass
            else:
                os.mkdir(dir_x)

            src_image = '{}'.format(x['full_path'])
            dst_image = '{}/{}'.format(dir_x, x['file_name'])

            # move file to new dst
            shutil.move(src_image, dst_image)
            print('moved {} {}.'.format(x['full_path'], size_fmt(x['size'])))

        elif(int(x['width']) >= 1920):

            dir_x = '{}wallpapers_{}x{}'.format(
                x['directory'], str(x['width']), str(x['height']))

            # make directory if it doesnt
            if(os.path.exists(dir_x)):
                pass
            else:
                os.mkdir(dir_x)

            src_image = '{}'.format(x['full_path'])
            dst_image = '{}/{}'.format(dir_x, x['file_name'])

            # move file to new dst
            shutil.move(src_image, dst_image)
            print('moved {} {}.'.format(x['full_path'], size_fmt(x['size'])))

        else:
            print('File error, this doesn\'t seem to be a image.')
            pass





