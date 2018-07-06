import time


class Temporizador:

	base_time = time.time()
	timestamps = []

	def tag(self,tag):
		self.timestamps.append({'tag':tag,'timestamp':(time.time()-self.base_time)})

	def to_string(self):
		st = ''
		for inst in self.timestamps:
			st+=str(inst['timestamp'])+' - '+inst['tag']+'\n'
		return st

	def print(self):
		print(self.to_string())
