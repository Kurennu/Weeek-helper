import requests
import os
import sys

WEEEK_TOKEN = os.getenv("WEEEK_TOKEN")

def get_weeek_tasks(project_id):
    if not WEEEK_TOKEN:
        return []

    headers = {'Authorization': f'Bearer {WEEEK_TOKEN}'}
    params = {'projectId': project_id}
    url = 'https://api.weeek.net/public/v1/tm/tasks'

    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        return []

def get_weeek_task_by_id(task_id):
    if not WEEEK_TOKEN:
        print("Нет токена", file=sys.stderr)
        return None

    headers = {'Authorization': f'Bearer {WEEEK_TOKEN}'}
    url = f'https://api.weeek.net/public/v1/tm/tasks/{task_id}'

    try:
        print(f"Запрос задачи {task_id} из {url}", file=sys.stderr)
        response = requests.get(url, headers=headers)
        print(f"Статус ответа: {response.status_code}", file=sys.stderr)
        response.raise_for_status()
        result = response.json()
        print(f"Получен ответ: {result}", file=sys.stderr)

        if result.get('success') and 'task' in result:
            task = result['task']
            print(f"Извлечена задача: {task}", file=sys.stderr)
            return task
        else:
            print(f"Неожиданный формат ответа: {result}", file=sys.stderr)
            return None

    except requests.exceptions.HTTPError as e:
        print(f"HTTP ошибка при получении задачи {task_id}: {e}", file=sys.stderr)
        return None
    except Exception as e:
        print(f"Общая ошибка при получении задачи {task_id}: {e}", file=sys.stderr)
        return None
