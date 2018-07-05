import time


class MyTimer:

	base_time = time.time()
	timestamps = []

	def __init__(self,enabled = True):
		self.enabled = enabled

	def tag(self,tag):
		if self.enabled:
			self.timestamps.append({'tag':tag,'timestamp':(time.time()-self.base_time)})

	def to_string(self):
		st = ''
		for inst in self.timestamps:
			st+=str(inst['timestamp'])+' - '+inst['tag']+'\n'
		return st

	def print(self):
		print(self.to_string())
