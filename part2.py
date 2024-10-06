import requests, json
from datetime import timedelta
from collections import namedtuple
from contextlib import closing
import sqlite3
from table import table

from prefect import Flow, task
from prefect.schedules import IntervalSchedule
from prefect.tasks.database.sqlite import SQLiteScript

DB_NAME = "todo.db"

create_table = SQLiteScript(
    db=DB_NAME,
    script='CREATE TABLE IF NOT EXISTS todo (userId INTEGER, id INTEGER, title TEXT, completed INTEGER)'
)

# setup
@task
def get_todo_data():
    r = requests.get("https://jsonplaceholder.cypress.io/todos/", params={"size":16})
    response_json = json.loads(r.text)
    return response_json

# extract
@task
def parse_todo_data(raw):
    todos = []
    Todo = namedtuple("Todo", ['USERID', 'ID', 'TITLE', 'COMPLETED'])
    for row in raw:
        
        this_todo = Todo(
            userId=row.get('userId'),
            id=row.get('id'),
            title=row.get('title'),
            completed=row.get('completed'),
        )
        todos.append(this_todo)
    return todos

# load
@task
def store_todos(parsed):
    insert_cmd = "INSERT INTO todo VALUES (?, ?, ?, ?)"

    with closing(sqlite3.connect(DB_NAME)) as conn:
        with closing(conn.cursor()) as cursor:
            cursor.executemany(insert_cmd, parsed)
            conn.commit()

@task
# show a table of todos in format: userId | id | title | completed
def show_todos(todo: list):
    todo.insert(0, ("userId", "id", "title", "completed"))
    table(todo)
    # print(todo)
    # for task in todo:
    #     print(f"{task[0]} | {task[1]} | {task[2]} | {task[3]}")

# Show first five user todos
@task
def first_five_user_todos(userId : int = 1):
    with closing(sqlite3.connect(DB_NAME)) as conn:
        with closing(conn.cursor()) as cursor:
            cursor.execute(f"SELECT * FROM todo WHERE userId = {userId} LIMIT 5")
            return cursor.fetchall()

# show uncompleted user todos
@task
def uncompleted_user_todos(userId : int = 1):
    with closing(sqlite3.connect(DB_NAME)) as conn:
        with closing(conn.cursor()) as cursor:
            cursor.execute(f"SELECT * FROM todo WHERE userId = {userId} and completed = 0 LIMIT 5")
            return cursor.fetchall()

schedule = IntervalSchedule(interval=timedelta(minutes=1))

with Flow("my etl flow", schedule) as f:
    db_table = create_table()
    raw = get_todo_data()
    parsed = parse_todo_data(raw)
    populated_table = store_todos(parsed)
    populated_table.set_upstream(db_table)
    todos = first_five_user_todos()
    # table(todos)
    show_todos(todos)
    todos = uncompleted_user_todos()
    # table(todos)
    show_todos(todos)

f.run()