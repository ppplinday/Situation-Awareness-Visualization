import os
import sys
import json

def findvalue(json_line, Key):
	if (type(json_line) != 'dict'):
		if Key in json_line:
			return json_line[Key]
		else:
			return None

	for key in json_line:
		temp = findvalue(json_line[key], Key)
		if temp != None:
			return temp

	return None

if __name__ == "__main__":
	
	file_name = sys.argv[1]
	config = sys.argv[2]
	attr_name = []
	name_dict = {}
	tempfile = open("tempfile.json", 'w')
	tempconfig = open("tempconfig.json", 'w')

	# read config and store in the tempcinfig
	

	with open(config, 'r') as f:

		data = f.readlines()
		temp_str = ""
		for line in data:
			temp_str = temp_str + line.split('\n')[0]
		config_dict = json.loads(temp_str)

		# store in a tempconfig file
		tempconfig.write(json.dumps(config_dict) + '\n')

		attr_name.append(config_dict['x'])
		name_dict[config_dict['x']] = 'x'
		attr_name.append(config_dict['y'])
		name_dict[config_dict['y']] = 'y'
		if config_dict['has_type'] == True:
			attr_name.append(config_dict['type'])
			name_dict[config_dict['type']] = 'type'
		attr_name.append(config_dict['body'])
		name_dict[config_dict['body']] = 'body'


	# add some information about the size of json and the size after process

	with open(file_name, 'r') as f:

		res = dict()
		for i in range(len(attr_name)):
			res[name_dict[attr_name[i]]] = [];
		

		# read json lines
		data = f.readlines()
		for line in data:
			line_json = json.loads(line)
			temp_arr = dict()
			for i in range(len(attr_name)):
				temp = findvalue(line_json, attr_name[i])
				if temp == None:
					break
				if name_dict[attr_name[i]] == 'x' or name_dict[attr_name[i]] == 'y':
					temp = float(temp)
				temp_arr[attr_name[i]] = temp

			if len(temp_arr) != len(attr_name):
				continue

			for i in range(len(attr_name)):
				res[name_dict[attr_name[i]]].append(temp_arr[attr_name[i]])


		tempfile.write(json.dumps(res) + '\n')

	tempfile.close()

