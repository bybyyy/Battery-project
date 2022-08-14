import math
import random

#beta = pi*sqrt(diffusionCoefficient)/length #0.574
beta = 0.574
unused = 0

class task:
	def __init__(self, ID, startTime, voltage, duration):
		self.ID = ID
		self.startTime = startTime
		self.voltage = voltage
		self.duration = duration

tasks = []

for x in range(1, 5):
	if x == 1:
		startTime = 0
	else:
		startTime = tasks[x-2].startTime + tasks[x-2].duration
	voltage = random.randint(100,999)
	duration = random.randint(1,60)
	tasks.append(task(x, startTime, voltage, duration))

for obj in tasks:
	print( obj.ID, obj.startTime, obj.voltage, obj.duration )

def F (x, y, z, b):
	sum = 0
	for m in range(1,10):
		n1 = math.exp(-(b**2)*(m**2)*(x-z))
		n2 = math.exp(-(b**2)*(m**2)*(x-y))
		d1 = (b**2)*(m**2)
		sigma = round((n1 - n2)/d1 , 3)
		sum = sum + sigma

	return z - y + 2* sum

def Capacity():
	sum = 0
	for k in range(0, failTaskNO):
		sigma = tasks[k].voltage * F(failTime, tasks[k].startTime, tasks[k].startTime + tasks[k].duration, beta)
		sum = sum + sigma

	return sum
	# return round(sum, 3) + currentU * F(failTime, failTaskStartTime, failTime, beta)

def wasted (x, y, z, b):
	unused = 0
	for m in range(1,10):
		n1 = math.exp(-(b**2)*(m**2)*(x-z))
		n2 = math.exp(-(b**2)*(m**2)*(x-y))
		d1 = (b**2)*(m**2)
		sigma = round((n1 - n2)/d1 , 3)
		unused = unused + sigma

	# m.x = var(i, within=binary)
	# @m.Objective(sense=maximize)
	# sum(x[i] * b[i] for i in I)

	return 2 * unused

def totalUnsed():
	sum = 0
	for k in range(0, failTaskNO):
		sigma = tasks[k].voltage * wasted(failTime, tasks[k].startTime, tasks[k].startTime + tasks[k].duration, beta)
		sum = sum + sigma

	return round(sum , 3)

def totalCharge(total, wasted):
	return total - wasted

failTime = tasks[len(tasks)-1].startTime + tasks[len(tasks)-1].duration
failTaskNO = len(tasks)
# failTaskStartTime = 35
# currentU = 912


print("total,", Capacity())
print("unused,", totalUnsed())
print("used," , totalCharge(Capacity(), totalUnsed()))