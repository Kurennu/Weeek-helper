import sys
from api import get_weeek_tasks, get_weeek_task_by_id
from validators import validate_title
import os

WEEEK_TOKEN = os.getenv("WEEEK_TOKEN")

def validate_all_project_tasks(arguments):
    project_id = arguments.get("project_id")

    if not WEEEK_TOKEN:
        return "Ошибка: Не установлен токен Weeek"

    tasks = get_weeek_tasks(project_id)
    if not tasks:
        return f"Не удалось получить задачи из проекта {project_id}"

    results = []
    valid_count = 0

    for task in tasks:
        title = task.get('title', '')
        is_valid, message = validate_title(title)
        if is_valid:
            valid_count += 1
            results.append(f"{title}")
        else:
            results.append(f"{title} - {message}")

    text = f"Результаты проверки проекта {project_id}:\n"
    text += f"Всего задач: {len(tasks)}\n"
    text += f"Валидных: {valid_count}\n"
    text += f"Невалидных: {len(tasks) - valid_count}\n\n"
    text += "\n".join(results)
    return text

def validate_single_task_title(arguments):
    title = arguments.get("title", "")
    is_valid, message = validate_title(title)
    if is_valid:
        return f"Заголовок валиден: '{title}'"
    else:
        return f"Заголовок невалиден: '{title}' - {message}"

def get_and_validate_task_by_id(arguments):
    task_id = arguments.get("task_id")
    print(f"Обрабатываем get_and_validate_task для задачи {task_id}", file=sys.stderr)

    if not WEEEK_TOKEN:
        return "Ошибка: Не установлен токен Weeek"

    task = get_weeek_task_by_id(task_id)
    if not task:
        return f"Не удалось получить задачу с ID {task_id}"

    title = task.get('title', '')
    description = task.get('description', '')
    project_id = task.get('projectId', '')
    is_completed = task.get('isCompleted', False)
    created_at = task.get('createdAt', '')

    is_valid, message = validate_title(title)

    text = f"Задача ID {task_id}:\n"
    text += f"Заголовок: '{title}'\n"
    text += f"Описание: '{description[:100]}{'...' if len(description) > 100 else ''}'\n"
    text += f"Проект ID: {project_id}\n"
    text += f"Завершена: {'Да' if is_completed else 'Нет'}\n"
    text += f"Создана: {created_at}\n\n"

    if is_valid:
        text += f"Заголовок валиден"
    else:
        text += f"Заголовок невалиден - {message}"

    return text
