import tkinter as tk
from tkinter import ttk
import json
from pathlib import Path

BG_COLOR = "#171B26"
PANEL_COLOR = "#222838"
INPUT_COLOR = "#262D3E"
TEXT_COLOR = "#F4F5FA"
ACCENT_COLOR = "#566CF1"

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
    tasks_listbox.insert(index, task + " (выполнено)")
    tasks_listbox.itemconfig(index, fg="#63D7AD")
    save_tasks()

def clear_selection(event):
    listbox = event.widget

    if not listbox.curselection():
        return
    index = listbox.nearest(event.y)
    bbox = listbox.bbox(index)
    if bbox is None or not (bbox[1] <= event.y < bbox[1] + bbox[3]):
        listbox.selection_clear(0, tk.END)

root = tk.Tk()

root.title("Task Manager")
root.geometry("520x560")
root.minsize(450, 480)
root.configure(bg=BG_COLOR)

title = tk.Label(
    root,
    text="Мои задачи",
    font=("Arial", 20, "bold"),
    bg=BG_COLOR,
    fg=TEXT_COLOR
)
title.pack(pady=20, fill='x', ipady=0)

task_entry = tk.Entry(
    root,
    font=("Arial", 12),
    bg=INPUT_COLOR,
    fg=TEXT_COLOR,
    insertbackground=TEXT_COLOR,
    relief='flat'
)
task_entry.pack(padx=20, fill="x", ipady=9)

add_button = tk.Button(
    root,
    text="+ Добавить задачу",
    command=add_task,
    bg=ACCENT_COLOR,
    fg="#FFFFFF",
    activebackground="#4357CC",
    activeforeground="#FFFFFF",
    font=("Arial", 11, "bold"),
    relief="flat",
    cursor="hand2",
    pady=8
)
add_button.pack(padx=20, pady=10, fill="x")

task_entry.bind('<Return>', lambda event: add_task())

tasks_listbox = tk.Listbox(
    root,
    font=("Arial", 12),
    bg=PANEL_COLOR,
    fg=TEXT_COLOR,
    selectbackground=ACCENT_COLOR,
    selectforeground='#FFFFFF',
    relief='flat',
    borderwidth=0,
    highlightthickness=0
)
tasks_listbox.pack(
    padx=20,
    pady=10,
    fill="both",
    expand=True
)

tasks_listbox.bind("<ButtonRelease-1>", clear_selection)

buttons_frame = tk.Frame(root, bg=BG_COLOR)
buttons_frame.pack(padx=20, pady=15, fill="x")

complete_button = tk.Button(
    buttons_frame,
    text="✓ Выполнено",
    command=complete_task,
    bg="#256D56",
    fg="#FFFFFF",
    font=("Arial", 11),
    relief="flat",
    cursor="hand2",
    pady=8
)
complete_button.pack(side="left", expand=True, fill="x", padx=(0, 5))

delete_button = tk.Button(
    buttons_frame,
    text="Удалить",
    command=delete_task,
    bg="#983D48",
    fg="#FFFFFF",
    font=("Arial", 11),
    relief="flat",
    cursor="hand2",
    pady=8
)
delete_button.pack(side="left", expand=True, fill="x", padx=(5, 0))

for task in load_tasks():
    tasks_listbox.insert(tk.END, task)
    if task.endswith('(выполнено)'):
        tasks_listbox.itemconfig(tk.END, fg='#63D7AD')
root.mainloop()