import math
import random
import copy

alpha = 39668
# beta = pi*sqrt(diffusionCoefficient)/length
beta = 0.574
unused = 0
NumberofTasks = 3
tasks = []
finaltasks = []


class task:
    def __init__(self, ID, arrivetime, startTime, amperage, duration, deadline, process):
        self.ID = ID
        self.startTime = startTime
        self.arrivetime = arrivetime
        self.amperage = amperage
        self.duration = duration
        self.deadline = deadline
        self.process = process

    def __repr__(self):
        return str(self.ID) + ' ' + str(self.arrivetime) + ' ' + str(self.startTime) + ' ' + str(self.amperage) + ' ' + str(self.duration) + ' ' + str(self.deadline) + ' ' + str(self.process)

    def __lt__(self, other):
        # if self.arrivetime != 0
        return self.amperage > other.amperage

    # def __lt__(self, other):
    #     return self.amperage < other.amperage


def printalltasks(tasks):
    for obj in tasks:
        print("iD:", obj.ID, " arrive time:", obj.arrivetime, " start time:", obj.startTime, " amperage:", obj.amperage,
              " duration:", obj.duration, " deadline:", obj.deadline, " process:", obj.process)
    print("")


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
    for k in range(0, failtaskindex):
        sigma = arr[k].amperage * F(endtime, arr[k].startTime, arr[k].startTime + arr[k].duration, beta)
        sum = sum + sigma

    return round(sum + arr[failtaskindex].amperage * F(endtime, arr[failtaskindex].startTime, endtime, beta), 3)


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
    for k in range(0, failtaskindex):
        sigma = arr[k].amperage * wasted(endtime, arr[k].startTime, arr[k].startTime + arr[k].duration, beta)
        sum = sum + sigma

    return round(sum + arr[failtaskindex].amperage * wasted(endtime, arr[failtaskindex].startTime, endtime, beta), 3)


def totalCharge(total, wasted):
    return total - wasted


def searchfailtaskindex(tasks, a):
    index = 0
    for i in range(0, len(tasks)):
        tarrary = []
        for j in range(0, i + 1):
            tarrary.append(tasks[j])
        total = Capacity(tarrary, tarrary[len(tarrary) - 1].startTime + tarrary[len(tarrary) - 1].duration, i)
        if total < a:
            index += 1
        else:
            return index
    return -1


def binarySearch(arr, left, right, x):
    if right >= left:
        middle = left + (right - left) // 2
        # print("middle: ", middle)

        totalt = Capacity(arr, middle, failtaskindex)
        # print("total: ", totalt)
        # print("dif: \n", totalt - x)
        if abs(totalt - x) <= 15:
            return round(middle, 3)
        elif totalt > x:
            return binarySearch(arr, left, middle - 0.1, x)
        else:
            return binarySearch(arr, middle + 0.1, right, x)

    else:
        return -1


def splitarray(arr, i, f):
    newarr = []

    for a in range(i, f + 1):
        newarr.append(arr[a])
    return newarr


def findobjectbyID(list, value):
    for x in list:
        if x.ID == value:
            return x
    return -1


def firstoptimizationfordeadline():
    finaltasks.append(tasks[0])
    tasks[1].startTime = max(tasks[1].arrivetime, tasks[0].startTime + tasks[0].duration)
    finaltasks.append(tasks[1])
    # printalltasks(tasks)
    for x in range(2, len(tasks)):
        tasks[x].startTime = max(tasks[x].arrivetime, tasks[x - 1].startTime + tasks[x - 1].duration)
        if tasks[x].startTime + tasks[x].duration > tasks[x].deadline:
            c = copy.copy(tasks[x])  # current task
            p = copy.copy(finaltasks[-1])  # previous task
            originalsum = (c.startTime + c.duration - c.deadline) + (p.startTime + p.duration - p.deadline)
            # hypothetical switch
            c.startTime = max(c.arrivetime, p.startTime)
            p.startTime = c.startTime + c.duration
            switchedsum = (c.startTime + c.duration - c.deadline) + (p.startTime + p.duration - p.deadline)
            # print("o", originalsum)
            # print("s", switchedsum)
            if switchedsum <= originalsum:  # do switch, but then check if it meets the deadline
                finaltasks.pop(-1)
                # check current and add it
                if c.startTime + c.duration - c.deadline <= 0:
                    finaltasks.append(c)
                else:
                    c.amperage *= voltagescaling
                    c.duration /= voltagescaling
                    if c.startTime + c.duration - c.deadline <= 0:
                        finaltasks.append(c)
                        p.startTime = max(p.arrivetime, c.startTime + c.duration)

                # check previous and add it
                if p.startTime + p.duration - p.deadline <= 0:
                    finaltasks.append(p)
                else:
                    p.amperage *= voltagescaling
                    p.duration /= voltagescaling
                    # if it works, add the previous
                    if p.startTime + p.duration - p.deadline <= 0:
                        finaltasks.append(p)
        else:
            finaltasks.append(tasks[x])


def secondoptimizationforamperage(finaltasks):
    for x in reversed(range(2, len(finaltasks))):
        if finaltasks[x].amperage > finaltasks[x - 1].amperage:
            min = finaltasks[x].deadline - finaltasks[x].duration - finaltasks[x].startTime
            for y in range(x + 2, len(finaltasks)):
                currentdiff = finaltasks[y].deadline - finaltasks[y].duration - finaltasks[y].startTime
                if currentdiff < min:
                    min = currentdiff
            if min > 0:
                total = finaltasks[x].amperage * finaltasks[x].duration
                finaltasks[x].duration += min
                finaltasks[x].amperage = total / finaltasks[x].duration


def randomtaskgeneration(NumberofTasks):
    # random generate certain amount of tasks
    for x in range(1, NumberofTasks + 1):
        if x == 1:
            arrivetime = 0
        else:
            arrivetime = random.randint(tasks[x - 2].arrivetime + 1, tasks[x - 2].arrivetime + 6)
        startTime = arrivetime
        amperage = random.randint(10, 900)
        duration = random.randint(1, 40)  # minutes
        deadline = random.randint(arrivetime + 1, 40)
        tasks.append(task(x, arrivetime, startTime, amperage, duration, deadline, 0))


def calculateenergyconsumption(list, failtime, failtask):
    sortCapacity = Capacity(list, failtime, failtask)
    sortUnused = totalUnsed(list, failtime, failtask)
    sortConsumption = totalCharge(sortCapacity, sortUnused)
    printall(sortCapacity, sortUnused, sortConsumption)

randomtaskgeneration(NumberofTasks)

# printalltasks(tasks)

# tasks = sorted(tasks)  # arrange them in descending order of their amperage
# for x in range(1, NumberofTasks + 1):  # recalculate the start time for all tasks in the new arrangement
#     if x == 1:
#         startTime = 0
#     else:
#         startTime = tasks[x - 2].startTime + tasks[x - 2].duration
#     tasks[x - 1].startTime = startTime

tasks = [task(1, 0, 0, 300, 10, 20, 0),
         task(2, 6, 6, 200, 8, 19, 0),
         task(3, 7, 7, 400, 8, 15, 0),
         task(4, 9, 9, 500, 2, 20, 0)]

printalltasks(tasks)
voltagescaling = 2

firstoptimizationfordeadline()
# for x in range(0, len(tasks)):
#     if tasks[x].deadline == -1:  # if no deadline, then just add it
#         finaltasks.append(tasks[x])
#     else:
#         if x != 0 and tasks[x - 1].startTime + tasks[x - 1].duration > tasks[x].arrivetime:
#             tasks[x].startTime = tasks[x - 1].startTime + tasks[x - 1].duration
#         if tasks[x].startTime + tasks[x].duration < tasks[x].deadline:
#             finaltasks.append(tasks[x])
#         else:
#             tasks[x].amperage = tasks[x].amperage * voltagescaling
#             tasks[x].duration = tasks[x].duration / voltagescaling
#             if tasks[x].startTime + tasks[x].duration - tasks[x].deadline <= 0:
#                 finaltasks.append(tasks[x])
#             else:
#                 index = x
#                 while index >= 2:
#                     #  switch with the one before it and see if it works
#                     print("here")
#                     print(repr(tasks[index]))
#                     print(repr(tasks[index - 1]))
#                     subject = tasks[index]
#                     friend = tasks[index-1]
#                     subject.startTime = max(subject.arrivetime, friend.startTime)
#                     friend.startTime = subject.startTime + subject.duration
#                     print("updated")
#                     print(repr(subject))
#                     print(repr(friend))
#                     #  if it works, then update to the new order
#                     if subject.startTime + subject.duration <= subject.deadline and \
#                             friend.startTime + friend.duration <= friend.deadline:
#                         print("nice")
#                         obj = findobjectbyID(tasks, friend.ID)
#                         print(obj)
#                         finaltasks.remove(obj)
#                         finaltasks.append(subject)
#                         finaltasks.append(friend)
#                         index = -1
#                         print("now")
#                         printalltasks(finaltasks)
#                     index -= 1

            #     print("here")
            #     stop = 0
            #     a = x
            #     b = len(finaltasks) - 1  # last index of the final list
            #     while stop == 0 and a > 0:
            #         print("takssssssss")
            #         print("a:", a)
            #         print("b", b)
            #         printalltasks(tasks)
            #         printalltasks(finaltasks)
            #         if tasks[a].startTime + tasks[a].duration > tasks[a].deadline and finaltasks[b].startTime + \
            #                 tasks[a].duration + finaltasks[b].duration < finaltasks[b].deadline:
            #             print("here")
            #             print("before,", tasks[a].ID)
            #             # tasks[a], tasks[a - 1] = tasks[a - 1], tasks[a]
            #             print("after,", tasks[a].ID)
            #             finaltasks.insert(b - 1, tasks[a])
            #             stop = 1
            #         a -= 1
print("first round")
printalltasks(finaltasks)

secondoptimizationforamperage(finaltasks)
print("second round")
printalltasks(finaltasks)

failtaskindex = searchfailtaskindex(tasks, alpha)
print(failtaskindex + 1)
actualendtime = binarySearch(tasks, tasks[failtaskindex].startTime,
                             tasks[failtaskindex].startTime + tasks[failtaskindex].duration, alpha)
print(actualendtime)
#
endTime = finaltasks[len(finaltasks) - 1].startTime + finaltasks[len(finaltasks) - 1].duration
failTaskIn = len(finaltasks) - 1

print("\nbefore sorted")
calculateenergyconsumption(finaltasks,endTime,failTaskIn)

# arrange tasks in descending order of their amperage
tasks = sorted(tasks)
for x in range(1, len(tasks) + 1):  # recalculate the start time for all tasks in the new arrangement
    if x == 1:
        startTime = 0
    else:
        startTime = tasks[x - 2].startTime + tasks[x - 2].duration
    tasks[x - 1].startTime = startTime

print("after sorted")
calculateenergyconsumption(finaltasks, actualendtime, failtaskindex)

# print("alpha - energy consumption = ", round(alpha - sortCapacity, 3))

for obj in tasks:
    print(obj.ID, obj.startTime, obj.amperage, obj.duration)

