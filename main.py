from flask import Flask, render_template, request
from bson.objectid import ObjectId
from pymongo import MongoClient

title = "TODO list"

app = Flask(__name__)

# подключение бд
client = MongoClient(
    "mongodb+srv://admin:admin@cluster0.1cqv7.mongodb.net/todo_db?retryWrites=true&w=majority")

db = client.db
tasks = db.tasks

initial_tasks = [
    {"message": "Подготовить презентацию", "completed": True},
    {"message": "Сделать доклад", "completed": False},
    {"message": "Отрепетировать", "completed": False},
    {"message": "Выпить чаю", "completed": False}
]

# раскомментировать чтоб добавить заданий
# tasks.insert_many(initial_tasks)

unfinished_tasks = []
finished_tasks = []


@app.route('/')
def main_page():
    unfinished_tasks = tasks.find({"completed": False})
    finished_tasks = tasks.find({"completed": True})
    return render_template("index.html", title=title, unfinished=unfinished_tasks, finished=finished_tasks)


@app.route('/add', methods=["POST"])
def add():
    message = request.form["message"]
    tasks.insert_one({"message": message, "completed": False})
    finished_tasks = tasks.find({"completed": True})
    unfinished_tasks = tasks.find({"completed": False})
    return render_template("index.html", title=title, unfinished=unfinished_tasks, finished=finished_tasks)


@app.route('/delete')
def deleteAll():
    tasks.drop()
    return render_template("index.html", title=title, unfinished=unfinished_tasks, finished=finished_tasks)


@app.route('/complete/<id>')
def complete(id):
    tasks.find_one_and_update({"_id": ObjectId(id)}, {
                              "$set": {"completed": True}})
    finished_tasks = tasks.find({"completed": True})
    unfinished_tasks = tasks.find({"completed": False})
    return render_template("index.html", title=title, unfinished=unfinished_tasks, finished=finished_tasks)


if __name__ == '__main__':
    app.run()
