class tooltips:

	def __init__ (self, attr):

		self.tips = dict()
		self.ori_attr = attr
		for i in attr:
			self.tips[i] = True

	def set_attr(self, attr):

		for i in self.tips:
			self.tips[i] = False
		for i in attr:
			if i in self.tips:
				self.tips[i] = True

	def build_tooptips(self):

		res = []
		for i in self.ori_attr:
			if self.tips[i] == True:
				res.append((i, "@" + i))
		return res
