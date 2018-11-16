import os
import json
import numpy as np
import pandas as pd

import SAVIZ.situation_awareness_visualization as saviz

with open("tempfile.json", 'r') as f:

	json_file = f.readlines()[0]

has_type = True

with open("tempconfig.json", 'r') as f:

	config = f.readlines()[0]
	has_type = json.loads(config)['has_type']

data = json.loads(json_file)

# convert the json to dataframe

pd_data = pd.DataFrame.from_dict(data)
sav = saviz.saviz_visualization(pd_data, has_type)

# build tooltips
tp = sav.set_tooltips()

sp = sav.build()
	