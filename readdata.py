from pathlib import Path
import time
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
  print(elem[1])
  print('bv')
  return elem[1]
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
print('09/15/2023' < '06/09/2024')