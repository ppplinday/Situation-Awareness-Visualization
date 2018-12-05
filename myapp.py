import os
import json
import numpy as np
import pandas as pd
import datetime

import SAVIZ.situation_awareness_visualization as saviz

with open("tempfile.json", 'r') as f:

	json_file = f.readlines()[0]

has_type = True
has_time = False
timeRange = [0, 1]

with open("tempconfig.json", 'r') as f:

	config = f.readlines()[0]
	has_type = json.loads(config)['has_type']
	has_time = json.loads(config)['has_time']

	if has_time == True:
		timeRange[0] = json.loads(config)['time_min']
		timeRange[1] = json.loads(config)['time_max']
		timeRange[0] = datetime.datetime.strptime(timeRange[0], "%Y-%m-%dT%H:%M:%S")
		timeRange[1] = datetime.datetime.strptime(timeRange[1], "%Y-%m-%dT%H:%M:%S")

data = json.loads(json_file)
if "time_value" in data:
	for i in range(len(data["time_value"])):
		data["time_value"][i] = datetime.datetime.strptime(data["time_value"][i], "%Y-%m-%dT%H:%M:%S")

# convert the json to dataframe

pd_data = pd.DataFrame.from_dict(data)
pd_data['time_value'] = pd.to_datetime(pd_data['time_value'])
sav = saviz.saviz_visualization(pd_data, has_type, has_time, timeRange)

# build tooltips
tp = sav.set_tooltips()

sp = sav.build()
	