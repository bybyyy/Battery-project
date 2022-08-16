import math
import random

alpha = 120000
# beta = pi*sqrt(diffusionCoefficient)/length #0.574
beta = 0.574
unused = 0
NumberofTasks = 100
tasks = []


class task:
    def __init__(self, ID, startTime, amperage, duration):
        self.ID = ID
        self.startTime = startTime
        self.amperage = amperage
        self.duration = duration

    def __repr__(self):
        return str(self.ID) + ' ' + str(self.startTime) + ' ' + str(self.amperage) + ' ' + str(self.duration)

    def __lt__(self, other):
        return self.amperage > other.amperage


for x in range(1, NumberofTasks + 1):  # random generate certain amount of tasks
    amperage = random.randint(10, 900)
    duration = random.randint(1, 5)  # minutes
    tasks.append(task(x, 0, amperage, duration))

tasks = sorted(tasks)  # arrange them in descending order of their amperage
for x in range(1, NumberofTasks + 1):  # recalculate the start time for all tasks in the new arrangement
    if x == 1:
        startTime = 0
    else:
        startTime = tasks[x - 2].startTime + tasks[x - 2].duration
    tasks[x - 1].startTime = startTime


for obj in tasks:
    print(obj.ID, obj.startTime, obj.amperage, obj.duration)

endTime = tasks[len(tasks) - 1].startTime + tasks[len(tasks) - 1].duration
failTaskNO = len(tasks)


def swap(arr, a, b):
    temp = arr[a]
    arr[a] = arr[b]
    arr[b] = temp


def Qsort(array):  # sort the array in descending order
    if len(array) <= 1:
        return array

    pivot = array[len(array) - 1]
    larray = []
    rarray = []
    position = -1
    for i in range(0, len(array) - 1):
        if array[i] > pivot:
            position = position + 1
            swap(array, i, position)
    position += 1
    swap(array, position, len(array) - 1)

    for a in range(0, position):
        larray.append(array[a])
    for b in range(position + 1, len(array)):
        rarray.append(array[b])

    larray = Qsort(larray)
    rarray = Qsort(rarray)

    return [*larray, pivot, *rarray]


# example = [2, 5, 6, 1, 4, 6, 2, 4, 7, 8]
# print(Qsort(example))


def F(x, y, z, b):
    sum = 0
    for m in range(1, 10):
        n1 = math.exp(-(b ** 2) * (m ** 2) * (x - z))
        n2 = math.exp(-(b ** 2) * (m ** 2) * (x - y))
        d1 = (b ** 2) * (m ** 2)
        sigma = round((n1 - n2) / d1, 3)
        sum = sum + sigma

    return z - y + 2 * sum


def Capacity():
    sum = 0
    for k in range(0, failTaskNO):
        sigma = tasks[k].amperage * F(endTime, tasks[k].startTime, tasks[k].startTime + tasks[k].duration, beta)
        sum = sum + sigma

    # return round(sum, 3) + currentU * F(failTime, failTaskStartTime, failTime, beta)
    return sum


def wasted(x, y, z, b):
    unused = 0
    for m in range(1, 10):
        n1 = math.exp(-(b ** 2) * (m ** 2) * (x - z))
        n2 = math.exp(-(b ** 2) * (m ** 2) * (x - y))
        d1 = (b ** 2) * (m ** 2)
        sigma = round((n1 - n2) / d1, 3)
        unused = unused + sigma

    # m.x = var(i, within=binary)
    # @m.Objective(sense=maximize)
    # sum(x[i] * b[i] for i in I)

    return 2 * unused


def totalUnsed():
    sum = 0
    for k in range(0, failTaskNO):
        sigma = tasks[k].amperage * wasted(endTime, tasks[k].startTime, tasks[k].startTime + tasks[k].duration, beta)
        sum = sum + sigma

    return round(sum, 3)


def totalCharge(total, wasted):
    return total - wasted


print("total,", Capacity())
print("unused,", totalUnsed())
print("used,", totalCharge(Capacity(), totalUnsed()))

# tasks = sorted(tasks)  # arrange them in descending order of their amperage
# for x in range(1, NumberofTasks + 1):  # recalculate the start time for all tasks in the new arrangement
#     if x == 1:
#         startTime = 0
#     else:
#         startTime = tasks[x - 2].startTime + tasks[x - 2].duration
#     tasks[x - 1].startTime = startTime
#
# print("total,", Capacity())