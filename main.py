import json
from pathlib import Path

DATA_FILE = Path(__file__).parent / "tasks.json"

def save_tasks(tasks):
    with open(DATA_FILE, 'w', encoding='utf-8') as file:
        json.dump(tasks, file, ensure_ascii=False, indent=4)

try:
    with open(DATA_FILE, "r", encoding="utf-8") as file:
        tasks = json.load(file)
except FileNotFoundError:
    tasks = []
except json.JSONDecodeError:
    print("Ошибка: Файл tasks.json поврежден. Создан новый пустой список задач.")
    raise SystemExit(1)
while True:
    print('========== TASK MANAGER ==========')
    print('1. Добавить задачу')
    print('2. Просмотреть задачи')
    print('3. Отметить задачу как выполненную')
    print('4. Удалить задачу')
    print('5. Выйти')

    try:
        choice = int(input("Выберите действие: "))
    except ValueError:
        print("Неверный выбор. Попробуйте еще раз.")
        continue

    if choice == 1:
        task = input("Введите задачу: ").strip()
        if not task:
            print("Задача не может быть пустой.")
            continue
        tasks.append(task)
        save_tasks(tasks)
        print("Задача добавлена.")
    elif choice == 2:
        if len(tasks) == 0:
            print("Список задач пуст.")
        else:
            print("Список задач:")
            for i, task in enumerate(tasks):
                print(f"{i + 1}. {task}")
    elif choice == 3:
        if len(tasks) == 0:
            print("Список задач пуст.")
        else:
            try:
                task_number = int(input("Введите номер задачи, которую хотите отметить как выполненную: "))
            except ValueError:
                print("Неверный номер задачи.")
                continue
            if task_number < 1 or task_number > len(tasks):
                print("Неверный номер задачи.")
            else:
                if tasks[task_number - 1].endswith("(выполнено)"):
                    print("Задача уже выполнена.")
                else:
                     tasks[task_number - 1] += " (выполнено)"
                     save_tasks(tasks)
                     print("Задача отмечена как выполненная.")
    elif choice == 4:
        if len(tasks) == 0:
            print('Список задач пуст.')
        else:
            try:
                task_number = int(input("Введите номер задачи, которую хотите удалить: "))
            except ValueError:
                print("Неверный номер задачи.")
                continue
            if task_number < 1 or task_number > len(tasks):
                print("Неверный номер задачи.")
            else:
                tasks.pop(task_number - 1)
                save_tasks(tasks)
                print("Задача удалена.")
    elif choice == 5:
        print("Задачи сохранены, выход из программы.")
        break
    else:
        print("Неверный выбор. Попробуйте еще раз.")