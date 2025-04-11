import os
import datetime
import subprocess

# @owen or whoever, feel free to clean this up, improve, etc. 

DEVICE = "/dev/video1"							# device file path on coral board
RESOLUTION = "250x250"							# img dimensions for fswebcam, default is 640x480
FILE_FORMAT = ".jpg"								# file format for fswebcam, default is .jpg
FILENAME_PREFIX = "sharklink_"			# sharklink_2025_08...
FILENAME_DELIMITER = "_"						# delimiter for filename, make sure to update if change format
DATETIME_FORMAT = "%Y_%m_%d_%H_%M" 	# YEAR_MONTH_DAY_HOUR_MINUTE
DELAY = 0														# amount of fswebcam delay
_VERBOSE_MODE = False								# if True make certain functions print outputs
_TEST_MODULE = False								# set to True to test module

_cur_dir = "."
_full_filename = ""
_dt = datetime.datetime.now()

def setDirectory(path):
	"""Sets the current working directory to store images.

	Params:
		path (str): relative or absolute directory path
	"""
	global _cur_dir 
	_cur_dir = os.path.abspath(path)
	if not os.path.exists(_cur_dir):
		raise OSError("File path '{}' does not exist".format(_cur_dir))
	if _VERBOSE_MODE: print(_cur_dir)
	return 0

def getDirectory():
	"""Gets the current working directory for storing images.

	Returns:
		paths (tuple): relative and absolute paths
	"""
	global _cur_dir
	paths = (_cur_dir, os.path.abspath(_cur_dir))
	return paths

def getDT():
	"""Gets the current datetime object.

	Returns:
		_dt (datetime obj): current private datetime object
	"""
	return _dt

def updateDT():
	"""Automatically updates the private datetime object.

	Returns:
		dt_str (str): datetime in string formatted to const DATETIME_FORMAT
	"""
	global _dt
	_dt = datetime.datetime.now()
	if _VERBOSE_MODE: print(_dt)
	dt_str = _dt.strftime(DATETIME_FORMAT)
	return dt_str

def setFilename():
	"""Creates the full filename with the given directory, FILENAME_PREFIX, datetime, and FILE_FORMAT.

	Returns:
		_full_filename (str): private path and filename string
	"""
	global _full_filename
	# {FILENAME_PREFIX}{updateDT()}{FILE_FORMAT} --> "/home/mendel/ducklink_2025_08_15_10_32.jpg"
	_full_filename = "/home/mendel/shark/camera_image.jpg" # f"{_cur_dir}/{FILENAME_PREFIX}{updateDT()}{FILE_FORMAT}"
	if _VERBOSE_MODE: print(_full_filename)
	return _full_filename

def getFilename():
	"""Gets the _full_filename private string.

	Returns:
		_full_filename (str): private path and filename string
	"""
	return _full_filename

def capture():
	"""Calls fswebcam CLI with DEVICE, DELAY, FILENAME_PREFIX, FILE_FORMAT parameters.

	Returns:
		rc (int): return code of subprocess.call()
	"""
	setFilename()
	if _VERBOSE_MODE: print(f"Capturing {FILE_FORMAT} img with device {DEVICE} at {_cur_dir}")
	if _TEST_MODULE:
		# creates a file to test functionality
		f = open(f"{_cur_dir}/{FILENAME_PREFIX}{updateDT()}.jpg", "w")
		f.close()
		rc = 0
	else:
		rc = subprocess.call(f"fswebcam --device {DEVICE} --delay {DELAY} {_full_filename}", shell=True)
	return rc

def printParameters():
	"""Prints out the module specific parameters.
	
	Returns:
		None
	"""
	param_str = \
f"""Only modify parameters within file.
Module parameters:
- Device path:\t\t{DEVICE}
- Resolution:\t\t{RESOLUTION}
- Delay:\t\t{DELAY}
- File format:\t\t{FILE_FORMAT}
- Prefix:\t\t{FILENAME_PREFIX}
- Datetime format:\t{DATETIME_FORMAT}
- Filename example:\t{setFilename()}
"""
	print(param_str)

if __name__ == "__main__":
	# printParameters()	

	print(_cur_dir)
	setDirectory("./img/")
	print(_cur_dir)

