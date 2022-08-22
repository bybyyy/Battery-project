import math
import random

alpha = 200000
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

    # def __lt__(self, other):
    #     return self.amperage < other.amperage


def printall(total, wasted, consume):
    print("total,", total)
    print("unused,", wasted)
    print("used,", consume)
    print("")


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


def F(x, y, z, b):
    sum = 0
    for m in range(1, 10):
        n1 = math.exp(-(b ** 2) * (m ** 2) * (x - z))
        n2 = math.exp(-(b ** 2) * (m ** 2) * (x - y))
        d1 = (b ** 2) * (m ** 2)
        sigma = round((n1 - n2) / d1, 3)
        sum = sum + sigma

    return z - y + 2 * sum


def Capacity(arr, endtime, failtaskindex):
    sum = 0
    for k in range(0, failtaskindex + 1):
        sigma = arr[k].amperage * F(endtime, arr[k].startTime, arr[k].startTime + arr[k].duration, beta)
        sum = sum + sigma

    # return round(sum, 3) + currentU * F(failTime, failTaskStartTime, failTime, beta)
    return round(sum, 3)


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


def totalUnsed(arr, endtime, failtaskindex):
    sum = 0
    for k in range(0, failtaskindex + 1):
        sigma = arr[k].amperage * wasted(endtime, arr[k].startTime, arr[k].startTime + arr[k].duration, beta)
        sum = sum + sigma

    return round(sum, 3)


def totalCharge(total, wasted):
    return total - wasted


def searchfailtaskindex(tasks, a):
    index = 0
    for i in range(0, len(tasks)):
        tarrary = []
        for j in range(0, i + 1):
            tarrary.append(tasks[j])
        if Capacity(tarrary, tarrary[len(tarrary) - 1].startTime + tarrary[len(tarrary) - 1].duration, i) < a:
            index += 1
        else:
            return index + 1
    return -1


def binarySearch(arr, i, r, x):
    if r >= i:
        m = i + (r - i) // 2

        tendtime = arr[m].startTime + arr[m].duration
        tarr = splitarray(arr, 0, m)
        narr = splitarray(arr, 0, m + 1)

        if Capacity(tarr, tendtime, m) < x and Capacity(narr, tendtime, m + 1) > x:
            return m
        elif Capacity(tarr, tendtime, m) > x:
            return binarySearch(arr, i, m - 1, x)
        else:
            return binarySearch(arr, m + 1, r, x)

    else:
        return -1


def splitarray(arr, i, f):
    newarr = []

    for a in range(i, f + 1):
        newarr.append(arr[a])
    return newarr


for x in range(1, NumberofTasks + 1):  # random generate certain amount of tasks
    amperage = random.randint(10, 900)
    duration = random.randint(1, 10)  # minutes
    tasks.append(task(x, 0, amperage, duration))

# tasks = sorted(tasks)  # arrange them in descending order of their amperage
for x in range(1, NumberofTasks + 1):  # recalculate the start time for all tasks in the new arrangement
    if x == 1:
        startTime = 0
    else:
        startTime = tasks[x - 2].startTime + tasks[x - 2].duration
    tasks[x - 1].startTime = startTime

# tasks = []
# tasks.append(task(1, 0, 912, 25))
# tasks.append(task(2, 35, 912, 9.2))

for obj in tasks:
    print(obj.ID, obj.startTime, obj.amperage, obj.duration)

endTime = tasks[len(tasks) - 1].startTime + tasks[len(tasks) - 1].duration
failTaskIn = len(tasks) - 1

capacity = Capacity(tasks, endTime, failTaskIn)
orgunused = totalUnsed(tasks, endTime, failTaskIn)
consumption = totalCharge(capacity, orgunused)
print("\nbefore sorted")
printall(capacity, orgunused, consumption)

tasks = sorted(tasks)  # arrange them in descending order of their amperage
for x in range(1, NumberofTasks + 1):  # recalculate the start time for all tasks in the new arrangement
    if x == 1:
        startTime = 0
    else:
        startTime = tasks[x - 2].startTime + tasks[x - 2].duration
    tasks[x - 1].startTime = startTime

sortCapacity = Capacity(tasks, endTime, failTaskIn)
sortUnused = totalUnsed(tasks, endTime, failTaskIn)
sortConsumption = totalCharge(sortCapacity, sortUnused)

print("after sorted")
printall(sortCapacity, sortUnused, sortConsumption)

print("alpha - energy consumption = ", round(alpha - sortCapacity, 3))

print(searchfailtaskindex(tasks, alpha) + 1)

# print(binarySearch(tasks, 0, len(tasks) - 1, alpha))
