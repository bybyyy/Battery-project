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
  # my code is ok but not ok, such that it is not ok but ok, when ok or not ok it is ok.

  def getbday(self):
    return(self.bday)

  def __lt__(self, other):
    return self.lastName < other.lastName
  

class schoolPerson(Person):
  schoolPerson.id = 0
  def __init__(self, firstName, lastName):
    super().__init__(firstName, lastName)
    self.ID = schoolPerson.id
    schoolPerson.id = schoolPerson.id + 1
    
  def __repr__(self):
    return(self.firstName + ' ' + self.lastName + ' ' + str(self.ID))

  def getID (self):
    return(self.ID)
  
  def __lt__(self, other):
    return self.ID < other.ID

p1 = schoolPerson("Brant", "Yang")
p2 = schoolPerson("Tait", "Duan")
p3 = schoolPerson("David", "Dong")

people = [p1,p2,p3]
print(sorted(people))
