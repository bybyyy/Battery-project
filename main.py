import math

#beta = pi*sqrt(diffusionCoefficient)/length #0.574
beta = 0.574
unused = 0

def F (x, y, z, b):
	sum = 0
	for m in range(1,10):
		n1 = math.exp(-(b**2)*(m**2)*(x-z))
		#print((b**2)*(m**2)*(x-z))
		n2 = math.exp(-(b**2)*(m**2)*(x-y))
		d1 = (b**2)*(m**2)
		sigma = round((n1 - n2)/d1 , 3)
		sum = sum + sigma
	unused = sum

	return z - y + 2* sum

def Capacity():
	sum = 0
	for k in range(0, failTaskNO):
		sigma = current[k] * F(failTime, startTime[k], startTime[k] + duration[k], beta)
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

	return unused

def totalUnsed():
	sum = 0
	for k in range(0, failTaskNO):
		sigma = current[k] * wasted(failTime, startTime[k], startTime[k] + duration[k], beta)
		sum = sum + sigma

	return sum

def totalCharge(total, wasted):
	return total - wasted

current = [912, 912]
startTime = [0, 35]
duration = [25, 9.2]
failTime = 44.2
failTaskNO = 2
failTaskStartTime = 35
currentU = 912


print("total,", Capacity())
print("unused,", totalUnsed())
print("used," , totalCharge(Capacity(), totalUnsed()))