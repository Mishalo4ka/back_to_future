import argparse
import json


def load_tasks():
    try:
        with open("tasks.json", "r") as f:
            tasks = json.load(f)
    except FileNotFoundError:
        tasks = []
    return tasks


def save_tasks(tasks):
    with open("tasks.json", "w") as f:
        json.dump(tasks, f, indent=4)


def new_id():
    tasks = load_tasks()
    if tasks:
        return max(task["id"] for task in tasks) + 1
    else:
        return 0


def add_task(title):
    tasks = load_tasks()
    tasks.append({"id": new_id(), "title": title, "completed": False})
    save_tasks(tasks)


def complete_task(task_id):
    tasks = load_tasks()

    for task in tasks:
        if task["id"] == task_id:
            task["completed"] = True
            break
    else:
        print(f"Task with ID {task_id} not found.")
        return

    save_tasks(tasks)


def list_tasks():
    tasks = load_tasks()

    for task in tasks:
        status = "*" if task["completed"] else " "
        print(f"[{status}] {task['title']} (ID: {task['id']})")


def delete_task(task_id):
    tasks = load_tasks()
    tasks = [task for task in tasks if task["id"] != task_id]
    save_tasks(tasks)


parser = argparse.ArgumentParser(description="Task Manager")
parser.add_argument(
    "command", choices=["add", "do", "list", "delete"], help="Command to execute"
)
parser.add_argument("args", nargs="*", help="Arguments for the command")
args = parser.parse_args()

if args.command == "add":
    if not args.args:
        print("Please provide a title for the task.")
    else:
        add_task(" ".join(args.args))

elif args.command == "do":
    if not args.args:
        print("Please provide the ID of the task to mark as completed.")
    else:
        try:
            task_id = int(args.args[0])
            complete_task(task_id)
        except ValueError:
            print("Task ID must be an integer.")

elif args.command == "list":
    list_tasks()

elif args.command == "delete":
    if not args.args:
        print("Please provide the ID of the task to delete.")
    else:
        try:
            task_id = int(args.args[0])
            delete_task(task_id)
        except ValueError:
            print("Task ID must be an integer.")
