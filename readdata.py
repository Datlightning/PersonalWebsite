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
def get_exercise(exercise_type):
  filename = directory.joinpath("exercises.txt")
  lines = []
  with open(filename.resolve(), "r") as file:
    lines = file.read().split("\n")
  if exercise_type == "chest":
    return eval(lines[0])
  elif exercise_type == "back":
    return eval(lines[1])
  elif exercise_type == "legs":
    return eval(lines[2])
  else:
    return eval(lines[3])

def add_exercise(data):
  filename = directory.joinpath('current-workout.txt')
  with open(filename.resolve(), "a+") as file:
    file.write("\n" + str(data))

def add_new_exercise(data):

  filename = directory.joinpath('exercises.txt')
  lines = []
  with open(filename.resolve(), "r+") as file:
    lines = file.read().split("\n")
    print(lines)
    for i in range(len(lines)):
      print(i)
      lines[i] = eval(lines[i])
    file.close()
  with open(filename.resolve(), "w") as file:
    file.close()
  if data[0] == "chest":
    lines[0].append(data[1])
  if data[0] == "back":
    lines[1].append(data[1])
  if data[0] == "legs":
    lines[2].append(data[1])
  if data[0] == "misc":
    lines[3].append(data[1])
  for i in range(len(lines)):
    lines[i]=sorted(lines[i])
  with open(filename.resolve(), "a+") as file:
    for line in lines[:-1]:
      file.write(str(line) + "\n")
    file.write(str(lines[3]))
  add_exercise(data)
def read_current_exercises():
  output = []
  filename = directory.joinpath("current-workout.txt")
  with open(filename.resolve(), "r") as file:
    lines = file.read().split("\n")
    for line in lines[1:]:
      try:
        output.append(eval(line))
      except:
        return ""
    file.close()
  return output
def change_exercise(text):
  chest = get_exercise("chest")
  back = get_exercise("back")
  legs = get_exercise("legs")
  misc = get_exercise("misc")
  exercises_dict = {
     "chest":chest,
    "back":back,
    "legs":legs,
    "misc":misc
  }

  current_exercises = eval(text)
  exercise_type = ""
  max_count = 0
  count = {
    "chest":0,
    "back":0,
    "legs":0,
    "misc":0
  }
  exercises = []
  for var in current_exercises[1:]:
    count[var[0]] += 1
    if count[var[0]] > max_count:
      exercise_type = var[0]
      max_count = count[var[0]]
    exercises.append(var[1])
  exercises_dict[exercise_type] = set(exercises_dict[exercise_type]).union(set(exercises))
  print(exercises_dict[exercise_type])
  options = ["chest", "back", "legs"]
  if exercise_type == "misc":
    return
  options.remove(exercise_type)
  for option in options:
    print(option)
    exercises_dict[option] = set(exercises_dict[option]).difference(set(exercises))
  filename = directory.joinpath("exercises.txt")
  with open(filename.resolve(), "w") as file:
    file.close()
  with open(filename.resolve(), "a+") as file:
    file.write(str(sorted(list(exercises_dict["chest"]))) + "\n")
    file.write(str(sorted(list(exercises_dict["back"]))) + "\n")
    file.write(str(sorted(list(exercises_dict["legs"]))) + "\n")
    file.write(str(sorted(list(exercises_dict["misc"]))) + "\n")
    
  
def log_current_workout():
  filename = directory.joinpath("current-workout.txt")
  text = f'["{time.localtime().tm_mon}.{time.localtime().tm_mday}.{time.localtime().tm_year}"'

  with open(filename.resolve(), "r") as file:
    for line in file.read().split('\n'):
      text += line + ","
  text = text[:-1]
  text += "]"
  with open(filename.resolve(), "w") as file:
    file.close()
  filename = directory.joinpath("workouts.txt")
  with open(filename.resolve(), "a+") as file:
    file.write("\n")
    file.write(text)
  change_exercise(text)
def generate_string(number,workout_list):
  output = f"{number}. {workout_list[1]} for {workout_list[2]}x{workout_list[3]}x {workout_list[4]}. {workout_list[5]}"
  return output
def get_all_workouts():
  filename = directory.joinpath("workouts.txt")
  text = []
  lines = []
  with open(filename.resolve(), "r") as file:
    lines = file.read().split("\n")
  for i in range(len(lines)):
    lines[i] = eval(lines[i])
    values = [0,0,0]
    title = ""

    text.append([])
    index = 1
    for item in lines[i][1:]:

      if item[0] == "back":
        values[1] += 1
      elif item[0] == "chest":
        values[0] += 1
      elif item[0] == "legs":
        values[2] += 1
      text[i].append(generate_string(index, item))
      index += 1
    if (max(values) == values[0]):
      title = "Chest"
    if (max(values) == values[1]):
      title = "Back"
    if (max(values) == values[2]):
      title = "Legs"
    text[i].insert(0,title)
    text[i].insert(0,lines[i][0])
  
  return text[::-1]
