import math
from math import pow
from math import exp
from math import pi

#beta = pi*sqrt(diffusionCoefficient)/length #0.574
beta = 0.574

def F (x, y, z, b):
	sum = 0
	for m in range(1,1000):
		n1 = math.exp((b**2)*(m**2)*(x-z)) - math.exp(-(b**2)*(m**2)*(x-y))
		d1 = (b**2)*(m**2)
		sigma = n1/d1
		sum = sum + sigma

	return (z - y + 2 * sum)

def alpha():
	sum = 0
	for k in range(0, failTaskNO):
		sigma = current[k] * F(failTime, startTime[k], startTime[k] + duration[k], beta)
		sum = sum + sigma

	return sum + currentU * F(failTime, failTaskStartTime, failTime, beta)

current = [912, 912]
startTime = [0, 35]
duration = [25, 25]
failTime = 43.8
failTaskNO = 2
failTaskStartTime = 35
currentU = 912

print(alpha())