import os
import sys

if __name__ == "__main__":

	filename = sys.argv[1]
	config = sys.argv[2]

	# check about the config file

	# conver json file
	converCommend = "python3 format_conversion.py " + filename + " " + config
	print(converCommend)
	os.system(converCommend)

	# run the boken serve
	os.system("bokeh serve --show myapp.py")

	# delete tempfile and delete tempconfig
	os.remove("tempfile.json")
	os.remove("tempconfig.json")