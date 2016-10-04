import magic
import sys
import os
import re
import shutil
import img_org
from pathlib import Path
from pathlib import PurePath


# return a dict of all files in location
def  get_files_dict(dir):
	the_files = os.scandir(dir)
	return the_files

# slashes for underlines
def fix_dir_name(string):
	new_string = string.replace('/', '_')
	return new_string


# slashes for none
def rm_forward_slash(string):
	new_string = string.replace('/', '')
	return new_string


# make directory via; regex chomp 
def makedir_for_mv(dir_name, entry):

	regex = r'^(.*/)?(?:$|(.+?)(?:(\.[^.]*$)|$))'

	d = re.match(regex, entry).group(1)

	current = ''.join(d)

	new_dir = current+dir_name

	if(os.path.exists(new_dir)):
		return
	else:
		os.mkdir(new_dir)

# move list of like files to dir
def move_files(files_to_move, where):

	regex = r'^(.*/)?(?:$|(.+?)(?:(\.[^.]*$)|$))'

	for entry in files_to_move:
		n = re.match(regex, entry).group(2,3)

		try:
			filename = ''.join(n)
		except TypeError:
			print('type error')
			filename = n[0]

		d = re.match(regex, entry).group(1)

		dst = ''.join(d)

		backup = '{}{}{}{}'.format(dst,where,'/',filename)

		shutil.move(entry, backup)
		print('moving:',entry,' to ',backup)

	print('Done.')

# find others like types of provided type and return list of them
def find_others(type, p, location):

	other_likes = []

	for entry in p.iterdir():
		if (entry.is_dir() or entry.is_symlink()):
			pass
		else:
			magick = PurePath(os.getcwd()+'/'+location,entry.name)
			if (magic.from_file(str(magick), mime=True) == type):
				other_likes.append(str(magick))
			else:
				pass

	return other_likes

# <------------------main----------------->

def main():
	if __name__ == '__main__':
		print('Location:',sys.argv[1])
		if (sys.argv[1] == None):
			print('Usage: python organize.py location\n')
			print('e.g. : $ python organize.py $HOME')
			print('e.g. : $ python organize.py .')
			print('e.g. : $ python organize.py /mnt/backup/download')
			quit()
		else:
			location = sys.argv[1]

	found = get_files_dict(location)

	p = Path(location)

	image_directories = []

	for entry in p.iterdir():

		try:
			if(entry.is_dir() or entry.is_symlink()):
				pass
			else:
				magick = PurePath(os.getcwd()+'/'+location,entry.name)

				file_type = magic.from_file(str(magick), mime=True)

				dir_name = fix_dir_name(file_type)

				if(dir_name == 'image_png' or
					dir_name == 'image_jpeg' or
					dir_name == 'image_gif'):
					image_directories.append(os.getcwd()+'/'+location+'/'+dir_name)

				makedir_for_mv(dir_name, str(magick))

				to_move = find_others(file_type, p, location)

				move_files(to_move, dir_name)
				
		except FileNotFoundError:
			continue


	for img_dir in image_directories:
		dic = img_org.ret_img_dict(img_dir)
		img_org.build_img_dir_tree_n_move(dic)
	
main()

