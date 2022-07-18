class Person():
  def __init__(self, firstName, lastName):
    self.firstName = firstName
    self.lastName = lastName
  bday = 24
  # bday = input("Your birthday is: ")

  def __repr__(self):
    return(self.firstName + ' ' + self.lastName)

  def getLast(self):
    return(self.lastName)

  def getbday(self):
    return(self.bday)

  def __lt__(self, other):
    return self.lastName < other.lastName
  
class IDsystem():
  def __init__(self,num):
    self.Id = num

  def nextID(self):
    self.Id += 1
    return self.Id

class schoolPerson(Person):
  def __init__(self, firstName, lastName,id):
    super().__init__(firstName, lastName)
    self.ID = id.nextID()
  def __repr__(self):
    return(self.firstName + ' ' + self.lastName + ' ' + str(self.ID))

  def getID (self):
    return(self.ID)
  def nextID(self):
    schoolPerson.id += 1
  
  def __lt__(self, other):
    return self.ID < other.ID

id = IDsystem(0)
p1 = schoolPerson("Brant", "Yang",id)
p2 = schoolPerson("Tait", "Duan",id)
p3 = schoolPerson("David", "Dong",id)

people = [p1,p2,p3]
print(sorted(people))
