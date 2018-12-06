import os
import sys
import json
import datetime
import collections

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

# base year is 2018
def cal_time_value(time_):
	time_ = str(time_)
	
	t = ["", "", "", "", ""]
	index = 0
	
	for i in range(len(time_)):
		
		if time_[i] >= '0' and time_[i] <= '9':
			t[index]= t[index] + time_[i]
		else:
			if len(t[index]) != 0:
				index = index + 1
			if index == 5:
				break

	res = []
	for i in range(5):
		res.append(int(t[i]))
		
	return res

def preprocessing(data):
    keys, values = zip(*data.items())
    return [{k:v for k, v in zip(keys, vs)} for vs in zip(*values)]

def postprocessing(n):
    res = collections.defaultdict(list)
    for nn in n:
        for k, v in nn.items():
            res[k].append(v)
    return res

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

		# # store in a tempconfig file
		# tempconfig.write(json.dumps(config_dict) + '\n')

		attr_name.append(config_dict['x'])
		name_dict[config_dict['x']] = 'x'
		attr_name.append(config_dict['y'])
		name_dict[config_dict['y']] = 'y'
		if config_dict['has_type'] == True:
			attr_name.append(config_dict['type'])
			name_dict[config_dict['type']] = 'type'
		if config_dict['has_time'] == True:
			attr_name.append(config_dict['time'])
			attr_name.append('time_value')
			name_dict['time_value'] = 'time_value'
			name_dict[config_dict['time']] = 'time'
		attr_name.append(config_dict['body'])
		name_dict[config_dict['body']] = 'body'


	# add some information about the size of json and the size after process

	with open(file_name, 'r') as f:

		res = dict()
		for i in range(len(attr_name)):
			res[name_dict[attr_name[i]]] = [];

		if config_dict['has_time'] == True:
			time_min = datetime.datetime(3000,1,1).isoformat()
			time_max = datetime.datetime(1001,1,1).isoformat()

		# read json lines
		data = f.readlines()
		total_size = len(data)
		for line in data:
			line_json = json.loads(line)
			temp_arr = dict()
			for i in range(len(attr_name)):

				temp = findvalue(line_json, attr_name[i])
				
				if attr_name[i] == 'time_value':
					continue
				if temp == None and attr_name[i] != 'time_value':
					break
				if name_dict[attr_name[i]] == 'x' or name_dict[attr_name[i]] == 'y':
					temp = float(temp)
				elif name_dict[attr_name[i]] == 'time':
					t = cal_time_value(temp)
					tempV = datetime.datetime(t[0],t[1],t[2],t[3],t[4]).isoformat()
					time_min = min(time_min, tempV)
					time_max = max(time_max, tempV)
					temp_arr['time_value'] = tempV
					temp = str(t[0]) + "-" + str(t[1]) + "-" + str(t[2]) + " " + str(t[3]) + ":" + str(t[4])

				temp_arr[attr_name[i]] = temp
			
			if len(temp_arr) != len(attr_name):
				continue

			for i in range(len(attr_name)):
				res[name_dict[attr_name[i]]].append(temp_arr[attr_name[i]])

		# tempfile.write(json.dumps(res) + '\n')


	final_res = {}
	if config_dict['has_time'] == True:
		config_dict['time_min'] = time_min
		config_dict['time_max'] = time_max

		begin_num = config_dict['begin_point_baseOfTime']
		total_num = config_dict['number_point_baseOfTime']
		if begin_num is not None and total_num is not None:
			
			n = preprocessing(res)
			n.sort(key=lambda x: x["time_value"])
			n = postprocessing(n)
			

			for key in n:
				final_res[key] = []
			
			for i in range(total_size):
				if (i >= begin_num and i < begin_num + total_num):
					for key in n:
						final_res[key].append(n[key][i])

			config_dict['time_min'] = datetime.datetime(3000,1,1).isoformat()
			config_dict['time_max'] = datetime.datetime(1001,1,1).isoformat()
			for i in range(len(final_res["time_value"])):
				config_dict['time_min'] = min(config_dict['time_min'], final_res["time_value"][i])
				config_dict['time_max'] = max(config_dict['time_max'], final_res["time_value"][i])
				# print(final_res["time_value"][i], config_dict['time_min'], config_dict['time_max'])
			tempfile.write(json.dumps(final_res) + '\n')
	else:
		tempfile.write(json.dumps(res) + '\n')
		

	# store in a tempconfig file
	tempconfig.write(json.dumps(config_dict) + '\n')


	tempfile.close()
	tempconfig.close()

