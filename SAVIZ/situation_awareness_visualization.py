'''

This is situation awareness visualization(SAVIZ) version 1

'''

import os
import numpy as np
import pandas as pd
from datetime import datetime

from bokeh.layouts import row, column, widgetbox
from bokeh.models import CustomJS, ColumnDataSource
from bokeh.plotting import figure, show, curdoc
from bokeh.models.widgets import DataTable, DateFormatter, TableColumn, Select, CheckboxGroup, RangeSlider, DateRangeSlider

from SAVIZ.selection_table import selection_table
from SAVIZ.tooltips import tooltips

class saviz_visualization:

	def __init__(self, pd_data, has_type=True, has_time=False, timeRange=[0,1]):
		
		self.has_type = has_type
		self.original_data = pd_data
		self.has_time = has_time
		self.timeRange = timeRange

		# init colors
		self.colors = ["red", "green", "blue", "pink", "orange", "tan", "black", "teal", "darkviolet", "cyan", "gold", "peru"]
		self.attr_name = self.original_data.columns.values.tolist()
		self.num = len(self.original_data)
		
		self.attr_name[0] = 'x'
		self.attr_name[1] = 'y'
		self.color = "blue"

		# init color col in the original data
		self.tooltip = []
		self.original_data['color'] = "blue"
		self.attr_name.append('color')


		
		# if has label, we need to add a color col
		if self.has_type == True:
			self.color = "color"
			
			self.attr_name[2] = 'type'
			#self.tooltip.append(("label", "@label"))
			
			# extract the label
			self.label_size = 0
			self.label2index = {}
			self.index2label = {}
			self.labels = []
			for i in range(self.num):
				temp_label = self.original_data.ix[i, 2]
				
				if temp_label not in self.label2index:
					self.index2label[self.label_size] = temp_label
					self.label2index[temp_label] = self.label_size
					self.labels.append(temp_label)
					self.label_size = self.label_size + 1
				
				self.original_data.loc[i, 'color'] = self.colors[self.label2index[temp_label]]

		# add index col
		self.attr_name.append('index')
		for i in range(self.num):
			self.original_data.loc[i, 'index'] = i

		# can be chosed in the future
		self.tools = ["pan, tap, lasso_select, box_select, wheel_zoom, zoom_in, zoom_out, reset"]

		# init tooltip
		self.tp = tooltips(self.attr_name[:-1])

	def add_tooltip(self):
		r = 1

	def select_data(self):
		
		data = self.original_data
		
		if self.has_time == True:
			vtime = self.time_rangeslider.value_as_datetime
			selected = data[
				(data['x'] >= self.x_rangeslider.value[0]) &
				(data['x'] <= self.x_rangeslider.value[1]) &
				(data['y'] >= self.y_rangeslider.value[0]) &
				(data['y'] <= self.y_rangeslider.value[1]) &
				(data['time_value'] >= vtime[0]) &
				(data['time_value'] <= vtime[1])
			]
		else:
			selected = data[
				(data['x'] >= self.x_rangeslider.value[0]) &
				(data['x'] <= self.x_rangeslider.value[1]) &
				(data['y'] >= self.y_rangeslider.value[0]) &
				(data['y'] <= self.y_rangeslider.value[1])
			]
		

		if self.has_type == True:
			dic = {}
			for i in self.label_checkbox.active:
				dic[self.labels[i]] = 0
			bool_list = []
			for i in selected['type']:
				if i in dic:
					bool_list.append(True)
				else:
					bool_list.append(False)
			selected = selected[bool_list]
		
		return selected

	# callback function for update data
	def update(self):
		
		df = self.select_data()

		temp_dict = dict()
		if len(df) == 0:
			for name in self.attr_name:
				temp_dict[name] = []
		else:
			for name in self.attr_name:
				temp_dict[name] = df[name]

		self.source_scatter.data = temp_dict
		self.scatter_plot.title.text = "situation awareness visualization: %d points displayed in the figure!" % len(temp_dict[self.attr_name[0]])


	def build(self):

		# init widget
		if self.has_type == True:
			active = [i for i in range(len(self.labels))]
			labels = [self.labels[i] + " (" + self.colors[i] + ")" for i in range(len(self.labels))]
			self.label_checkbox = CheckboxGroup(labels=labels, active=active)

		self.x_rangeslider = RangeSlider(value=[-100, 150], start=-100, end=150, step=1, title="x")
		self.y_rangeslider = RangeSlider(value=[-100, 100], start=-100, end=100, step=1, title="y")

		if self.has_time == True:
			self.time_rangeslider = DateRangeSlider(format="%Y-%b-%d %H:%M", value=[self.timeRange[0], self.timeRange[1]], start=self.timeRange[0], end=self.timeRange[1], step=10, title="time")

		controls = []
		if self.has_type == True:
			controls.append(self.label_checkbox)
		controls.append(self.x_rangeslider)
		controls.append(self.y_rangeslider)
		if self.has_time == True:
			controls.append(self.time_rangeslider)
		widgets = widgetbox(controls, width=700, height=700)

		# if self.has_type == True:
		# 	widgets = widgetbox(self.label_checkbox, self.x_rangeslider, self.y_rangeslider, width=700, height=700)
		# 	controls = [self.label_checkbox, self.x_rangeslider, self.y_rangeslider]
		# else:
		# 	widgets = widgetbox(self.x_rangeslider, self.y_rangeslider, width=700, height=700)
		# 	controls = [self.x_rangeslider, self.y_rangeslider]

		for control in controls:
			
			if type(control) == CheckboxGroup:
				control.on_change('active', lambda attr, old, new: self.update())
			else:
				control.on_change('value', lambda attr, old, new: self.update())


		# self.source_scatter is variable which figure will display the data from
		self.source_scatter = ColumnDataSource(data=self.original_data)
	
		self.scatter_plot = figure(plot_width=700, plot_height=700, tools=self.tools, tooltips=self.tooltip, toolbar_location="left", title="")
		sp = self.scatter_plot.circle(x='x', y='y', size = 20, color=self.color, source=self.source_scatter)

		table_attr_name = self.attr_name[:-1]
		st_table = selection_table(table_attr_name, sp, self.source_scatter)

		layout = column(row(widgets, self.scatter_plot), st_table.table)
		
		self.update()
		for name in self.attr_name:
			self.source_scatter.data[name] = pd.Series(self.source_scatter.data[name])
		

		curdoc().add_root(layout)

	def set_tooltips(self, arr=None):

		if arr != None:
			self.tp.set_attr(arr)
		self.tooltip = self.tp.build_tooptips()
		print(self.tooltip)
		print("xxx")
