import math

#beta = pi*sqrt(diffusionCoefficient)/length #0.574
beta = 0.574

def F (x, y, z, b):
	sum = 0
	for m in range(1,1000):
		n1 = round(math.exp(-(b**2)*(m**2)*(x-z)) , 4)
		#print((b**2)*(m**2)*(x-z))
		n2 = round(math.exp(-(b**2)*(m**2)*(x-y)) , 4)
		d1 = round((b**2)*(m**2) , 4)
		sigma = round((n1 - n2)/d1 , 3)
		sum = sum + sigma
		# print(sum)

	return (z - y + 2 * sum)

def alpha():
	sum = 0
	for k in range(1, failTaskNO):
		sigma = current[k] * F(failTime, startTime[k], startTime[k] + duration[k], beta)
		sum = sum + sigma


	return round(sum, 3) + currentU * F(failTime, failTaskStartTime, failTime, beta)

current = [912, 912]
startTime = [0, 35]
duration = [25, 9.2]
failTime = 44.2
failTaskNO = 2
failTaskStartTime = 35
currentU = 912

print(alpha())