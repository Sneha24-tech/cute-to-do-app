from flask import Flask, render_template, request, redirect
from datetime import datetime
import random

app = Flask(__name__)

# ✅ Add this RIGHT HERE
@app.template_filter('datetimeformat')
def datetimeformat(value):
    try:
        date_obj = datetime.strptime(value, '%Y-%m-%d')
        return date_obj.strftime('%d/%m/%Y')
    except:
        return value


# 🌸 Your cute task basket!
tasks = []

quotes = [
        "You are stronger than you think.",
        "One task at a time — you’ve got this!",
        "Every great journey starts with a single step.",
        "Believe in yourself and keep going.",
        "Today is your day to shine!"
        ]

@app.route("/splash")
def splash():
    return render_template("splash.html")


# 🏡 Home page - displays the to-do list
@app.route("/")
def index():
    today = datetime.now().strftime("%A, %d %B %Y")
    daily_quote = random.choice(quotes)
    return render_template("index.html", tasks=tasks, today=today, quote=daily_quote)

# ➕ Route to handle adding new tasks
@app.route("/add", methods=["POST"])
def add_task():
    task_text = request.form["task"]
    task_date = request.form["task_date"]
    task_priority = request.form["task_priority"]
    formatted_date = datetime.strptime(task_date, "%Y-%m-%d").strftime("%d/%m/%Y")
    if task_text:  # Prevent empty tasks
        tasks.append({"text":task_text, "date":formatted_date, "priority":task_priority, "completed":False})
    return redirect("/")

# ✅ Route to checklist a task
@app.route("/toggle/<int:task_id>")
def toggle_task(task_id):
    if 0 <= task_id < len(tasks):
        tasks[task_id]["completed"] = not tasks[task_id]["completed"]
    return redirect("/")

# 🗑️ Route to handle deleting tasks
@app.route("/delete/<int:task_id>",methods=["POST"])
def delete(task_id):
    if 0 <=task_id < len(tasks):
       tasks.pop(task_id)
    return redirect("/")

# 🚀 Run the app
if __name__ == "__main__":
    app.run(debug=True)
