import tkinter as tk
from tkinter import ttk
import json
from pathlib import Path

DATA_FILE = Path(__file__).parent / "tasks.json"

def load_tasks():
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        print('Ошибка файл tasks.json поврежден.')
        raise SystemExit(1)


def save_tasks():
    tasks = list(tasks_listbox.get(0, tk.END))

    with open(DATA_FILE, "w", encoding="utf-8") as file:
        json.dump(tasks, file, ensure_ascii=False, indent=4)

def add_task():
    task = task_entry.get().strip()
    if not task:
        return
    tasks_listbox.insert(tk.END, task)
    task_entry.delete(0, tk.END)
    save_tasks()

def delete_task():
    selected = tasks_listbox.curselection()
    if not selected:
        return
    tasks_listbox.delete(selected[0])
    save_tasks()

def complete_task():
    selected = tasks_listbox.curselection()
    if not selected:
        return
    index = selected[0]
    task = tasks_listbox.get(index)
    if task.endswith('(выполнено)'):
        return
    tasks_listbox.delete(index)
    tasks_listbox.insert(index, task + '(выполнено)')
    save_tasks()


root = tk.Tk()

root.title("Task Manager")
root.geometry("500x550")
root.minsize(400, 450)

title = ttk.Label(
    root,
    text="Мои задачи",
    font=("Arial", 18, "bold")
)
title.pack(pady=15)

task_entry = ttk.Entry(root, font=("Arial", 12))
task_entry.pack(padx=20, fill="x")

add_button = ttk.Button(
    root,
    text="Добавить задачу",
    command=add_task
)
add_button.pack(pady=10)

task_entry.bind('<Return>', lambda event: add_task())

tasks_listbox = tk.Listbox(root, font=("Arial", 12))
tasks_listbox.pack(
    padx=20,
    pady=10,
    fill="both",
    expand=True
)

delete_button = ttk.Button(
    root,
    text='Удалить задачу',
    command=delete_task
)
delete_button.pack(pady=5)

complete_button = ttk.Button(
    root,
    text='Выполнить задачу',
    command=complete_task
)
complete_button.pack(pady=5)

for task in load_tasks():
    tasks_listbox.insert(tk.END, task)
root.mainloop()