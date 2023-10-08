from flask import Flask, render_template, request, url_for, flash, redirect, session, send_from_directory, abort, jsonify
import os
import hashlib
import readdata as rd
from pathlib import Path
from assignment import assignment
from send import send_data
import time

app = Flask(__name__)
app.config['SECRET_KEY'] = "68c2b6ceb89ed3cd1f1c0e78d5fd79f710bef290bda90a70"


@app.route('/')
def index(): 
  if not 'workout' in session.keys():
    session['workout'] = False
  return render_template('index.html')


@app.route('/gpa')
def gpa():
  return render_template('gpa.html')


@app.route("/member-login", methods=['GET', 'POST'])
def member():

  if request.method == 'POST':
    username = request.form.get('username')
    hash_pass = hashlib.sha256(
        request.form.get('pass').encode('utf-8')).hexdigest()
    cred = rd.read_cred()
    if username.lower() in set(
        cred.keys()) and hash_pass == cred[username.lower()]:
      session['logged_in'] = True
      session['user'] = username
      print('Success')
      return redirect('/')
    else:
      print('failure')
      return render_template('member.html', error=True)
  return render_template('member.html')


@app.route('/logout')
def logout():
  session['logged_in'] = False
  return redirect('/')

@app.route("/meals", methods=['POST',"GET"])
def meals_handler():
  if request.method == 'POST':
    rd.create_meal(request.form)
  return render_template("meals.html")


@app.route("/add-assignment", methods=['GET', 'POST'])
def assigning():
  if not session['logged_in']:
    return redirect("/member-login")
  if request.method == 'POST':
    percentage = 0
    due_date = request.form.get("date")
    temp = due_date.split("-")
    if len(temp) != 3:
      return render_template("add-assignment.html")
    due_date = temp[1] + "/" + temp[2] + "/" + temp[0]
    name = request.form.get("name")
    a = assignment(name=name, completion=percentage, due_date=due_date)
    rd.add_assignment(a)
    rd.write_assignments(rd.read_assignments())
  return render_template("add-assignment.html")

@app.route("/notes", methods=['GET', 'POST'])
def make_notes():
  if not session['logged_in']:
    return redirect("/member-login")
  if request.method == 'POST':
    topic = request.form.get("topic")
    name = request.form.get("class")
    url = send_data(name, topic)
    text = "Link for " + topic + " notes"
    return render_template("notes.html", url=url, text = text)
  return render_template("notes.html")

@app.route('/refresh')
def refresh():
  return redirect("/homework")

@app.route("/homework", methods = ["GET", "POST"])
def homework():
  todays_date = f"{time.localtime().tm_mon}/{time.localtime().tm_mday}/{time.localtime().tm_year}"
  if not session['logged_in']:
    return redirect("/member-login")
  a = rd.read_assignments()
  updates = {}
  for x in a:
    try:
        updates[x[0]] = x[3:]
    except Exception as e:
        print(e)
        updates[x[0]] = []
  refresh = False
  if request.method == 'POST':
    for i in list(range(len(a)))[::-1]:
      completion_percentage = request.form.get("completion")
      if a[i][0] == request.form.get("assignment"):
        if int(completion_percentage) >= 100:
            del a[i]
        else:
            a[i].append(f"{completion_percentage}% - {todays_date}: {request.form.get('update')}")
            a[i][2] == completion_percentage
            updates[a[i][0]] = a[i][3:]

    rd.write_assignments(a)
    # if refresh:
    #   print(" i have arrived")
    #   return redirect("/refresh")
    return jsonify(updates=updates)
  return render_template("homework.html", assignments=a, updates = updates)
@app.route("/cookbook", methods = ["GET", "POST"])
def cookbook():
  if request.method == "POST":
    meals = rd.read_meals()
    
    data = []
    for meal in meals[request.form.get("meal")]:
      data.append([meal['name'], meal['ingredients'], meal['instructions']])
    print(data)
    return jsonify(meals = data)

  return render_template("mealbook.html")

@app.route("/workout", methods=["GET", "POST"])
def workout():
  if request.method == "POST":
    print(request.form.get("arg") == "start")
    if request.form.get("arg") == "start":
      session['workout'] = True
    elif request.form.get("arg") == "end":
      session['workout'] = False
      rd.log_current_workout()
    elif request.form.get("exercise") == "yes":
      return jsonify(data = rd.get_exercise(request.form.get("arg")))
    elif request.form.get("addinfo") == "yes":
      sets = request.form.get("sets")
      reps = request.form.get("reps")
      notes = request.form.get("updates")
      weight = request.form.get("weight")
      name = request.form.get('name')
      muscle = request.form.get('muscle')
      output = [muscle, name, sets, reps, weight, notes]
      rd.add_exercise(output)
      return jsonify(data = rd.get_exercise(muscle))
    elif request.form.get("addinfo") == "new_exercise":
      sets = request.form.get("sets")
      reps = request.form.get("reps")
      notes = request.form.get("updates")
      weight = request.form.get("weight")
      name = request.form.get('name')
      muscle = request.form.get('muscle')
      output = [muscle, name, sets, reps, weight, notes]
      rd.add_new_exercise(output)
      return jsonify(data = rd.get_exercise(muscle))

  workout = session['workout']
  return render_template("workout.html", workout = workout, exercises = rd.read_current_exercises())

@app.route('/workout-history', methods = ["POST", "GET"])
def workout_history():
  if request.method == "POST":
    date = request.form.get("date")
    muscle = request.form.get("muscle")
    rd.remove_workout(date, muscle)
  else:
    pass
  data = rd.get_all_workouts()
  return render_template("workout-history.html", data = data)

if __name__ == '__main__':
    app.run(debug=True)  
