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

def create_meal(a):
  filename = directory.joinpath('meals.txt')
  name = ""
  meal = ""
  ingredients = []
  instructions = []
  instruction = 1
  for key, item in a.items():
    print(key, item)
    if key == "name":
      name = item
    elif key == "meal_type":
      meal = item
    elif "ingredient" in key:
      ingredients.append(item)
    elif "instruction" in key:
      instructions.append(str(instruction) + ": " + item)
      instruction += 1
  if name == "":
    return
  if len(ingredients) == 0:
    return
  if len(instructions) == 0:
    return
  
  output_array = [name, meal]
  output_array.append(ingredients)
  output_array.append(instructions)
  with open(filename.resolve(), "a+") as file:
    file.write("\n" + str(output_array) )

def read_meals():
  meals = {
    "Breakfast":[],
    "Lunch":[],
    "Dinner":[],
    "Snack":[]
  }
  filename = directory.joinpath("meals.txt")
  with open(filename.resolve(), "r") as file:
    for line in file.read().split("\n"):
      data = eval(line)
      meal_type = data[1]
      name = data[0]
      ingredients = data[2]
      instructions = data[3]
      meal_dictionary = {
        "name":name,
        "ingredients":ingredients,
        "instructions":instructions
      }
      meals[meal_type].append(meal_dictionary)
  return meals