class assignment:

  def __init__(self, **kwargs):
    if len(kwargs) == 1:
      self.generateFromString(kwargs['string'])
    else:
      self.name = kwargs['name']
      self.due_date = kwargs['due_date']
      self.completion = kwargs['completion']

  def generateString(self):
    string = f"[\"{self.name}\", \"{self.due_date}\", \"{self.completion}\"]"
    return string

  def generateFromString(self, inputString):
    if inputString == "":
      return

    vars = eval(inputString)
    self.name = vars[0]
    self.due_date = vars[1]
    self.completion = vars[2]

  def toString(self):
    return f"Assignment Name: {self.name}\nDue Date: {self.due_date}\nCompletion: {self.completion}"

  def getData(self):
    output = [self.name, self.due_date, self.completion]
    return output

  def progress(self, percent):
    self.completion = percent
