from pathlib import Path
import time
import datetime
from assignment import assignment

directory = Path(__file__).parent.joinpath('data')
def read_cred():
    filename = directory.joinpath('login_credentials.txt')
    with open(filename.resolve(), 'r') as file:
        return eval(file.read().split("\n")[0])

def read_assignments():
  filename = directory.joinpath("assignments.txt")
  with open(filename.resolve(), 'r') as file:
    output = []
    for line in file.read().split("\n"):
      try:
        output.append(eval(line))
      except Exception as e:
        pass
    file.close()
  return output

def add_assignment(hw):
  filename = directory.joinpath('assignments.txt')
  with open(filename.resolve(), 'a+') as file:
    file.write(hw.generateString() + "\n")
  return
def second(elem):

  reference_date = datetime.date(2000,1,1)
  current_date = datetime.date(int(elem[1].split("/")[2]), int(elem[1].split("/")[0]), int(elem[1].split("/")[1]))
  return current_date - reference_date
def write_assignments(assignments):
  assignments = sorted(assignments, key = second)
  filename = directory.joinpath("assignments.txt")
  with open(filename.resolve(), "w+") as file:
    string = ""
    for line in assignments:
      string += str(line) + "\n"
    file.write(string)
    file.close()
  return
def get_api_key():
  filename = directory.joinpath('api.txt')
  with open(filename.resolve(), 'r') as file:
    return file.read().split('\n')[0]
