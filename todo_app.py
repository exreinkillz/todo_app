#Simple CLI To-Do App
# Features:
# Add new tasks
# List all tasks
# List completed tasks only
# Toggle task status (done / pending)
# Edit existing tasks
# Delete tasks
# View task statistics (completion rate, pending tasks)
# Persistent storage using JSON

import json

def add_task(tasks):
    task = input("Enter a task: ").strip()

    if task == "":
        print("Invalid task")
        return

    tasks.append({"title":task,"done":False})
    print("Task added")

def show_tasks(tasks):
    if not tasks:
        print("No tasks added")
        return

    i = 1
    for task in tasks:
        status = "[x]" if task["done"] else "[ ]"
        print(f"{i:2}. {status} {task['title']}")
        i += 1

def list_done(tasks):
    done_tasks = [task for task in tasks if task['done']]

    if not done_tasks:
        print("No tasks completed yet")
        return

    print("\n--- Completed tasks ---")
    for i, task in enumerate(done_tasks, 1):
        print(f"{i:2}. [x] {task['title']}")


def select_task(tasks, action):
    if not tasks:
        print(f"No tasks to {action}")
        return None

    show_tasks(tasks)

    choice = input(f"Enter task number to {action}: ").strip()
    if not choice.isdigit():
        print("Invalid input")
        return None

    index = int(choice) - 1
    if index < 0 or index >= len(tasks):
        print("Invalid task number")
        return None

    return index

def toggle_task(tasks):
    index = select_task(tasks, "toggle")
    if index is None:
        return

    tasks[index]["done"] = not tasks[index]["done"]
    print(f"Task {'completed' if tasks[index]['done'] else 'marked as pending'}: {tasks[index]['title']}")

def edit_task(tasks):
    index = select_task(tasks, "edit")
    if index is None:
        return

    old_title = tasks[index]["title"]
    print(f"Current title: {old_title}")

    new_title = input("Enter new title(leave empty to cancel): ").strip()
    if new_title == "":
        print("Edit cancelled")
        return

    tasks[index]["title"] = new_title
    print("Task edited")

def delete_task(tasks):
    index = select_task(tasks, "delete")
    if index is None:
        return

    confirm = input("Are you sure you want to delete the task (y/n): ").strip().lower()
    if confirm != "y":
        print("Delete cancelled!")
        return

    deleted_task = tasks.pop(index)
    print(f"Deleted: {deleted_task['title']}")

def show_stats(tasks):
    if not tasks:
        print("No tasks added")
        return

    total = len(tasks)
    completed = sum(1 for task in tasks if task['done'])
    pending = total - completed
    completion_rate = completed / total * 100

    print("\n--- Task Statistics ---")
    print(f"Total tasks     : {total}")
    print(f"Completed tasks : {completed}")
    print(f"Pending tasks   : {pending}")
    print(f"Completion rate : {completion_rate:.1f}%")

    if pending == 0:
        print("All tasks completed!")
    elif completed == 0:
        print("No progress yet!")
    elif completed > 0 and pending > 0:
        print("Keep going on!")

def save_tasks(tasks):
    with open("tasks.json", "w") as file:
        json.dump(tasks, file, indent=4)

def load_tasks():
    try:
        with open("tasks.json", "r") as file:
            return json.load(file)
    except (FileNotFoundError,json.JSONDecodeError):
        return []

def main():
    tasks = load_tasks()

    while True:
        command = input(
            "Enter a command(add/list/list_done/toggle/edit/delete/stats/exit): "
                        ).strip().lower()

        if command == "exit":
            save_tasks(tasks)
            print("Goodbye!")
            break

        if command not in COMMANDS:
            print("Invalid command")
            continue

        COMMANDS[command]["func"](tasks)

        if COMMANDS[command]["save"]:
            save_tasks(tasks)

COMMANDS = {
    "add": {"func": add_task, "save": True},
    "list": {"func": show_tasks, "save": False},
    "list_done": {"func": list_done, "save": False},
    "toggle": {"func": toggle_task, "save": True},
    "edit": {"func": edit_task, "save": True},
    "delete": {"func": delete_task, "save": True},
    "stats": {"func": show_stats, "save": False},
}

if __name__ == "__main__":
    main()