'''

This is selection table class for the SAVIZ

'''

from bokeh.layouts import row, column, widgetbox
from bokeh.models import CustomJS, ColumnDataSource
from bokeh.plotting import figure, show, curdoc
from bokeh.models.widgets import DataTable, DateFormatter, TableColumn, Select, CheckboxGroup, RangeSlider

class selection_table:

	def __init__(self, attr_name, figure, source_scatter):

		self.select_index = None
		self.attr_name = attr_name

		self.source_scatter = source_scatter

		empty_dic = self.create_empty_dic()

		self.source_table = ColumnDataSource(data=empty_dic)

		# create columns
		columns = []
		for i in range(len(attr_name)):
			columns.append(TableColumn(field=attr_name[i], title=attr_name[i]))
		
		self.table = DataTable(source=self.source_table, columns=columns, width=1400, height=700)
		figure.data_source.on_change('selected', self.selection_change)


	# callback function when select the data
	def create_empty_dic(self):

		empty_dic = {}
		for i in range(len(self.attr_name)):
			empty_dic[self.attr_name[i]] = []
		return empty_dic

	def selection_change(self, attr, old, new):

		inds = new['1d']['indices']
		temp = self.create_empty_dic()

		for i in inds:
			
			index = self.source_scatter.data['x']._index[i]
			
			for name in self.attr_name:
				temp[name].append(self.source_scatter.data[name][index])

		self.source_table.data = temp