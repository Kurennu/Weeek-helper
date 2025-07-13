import sys
import io
import json
from dotenv import load_dotenv
from rpc import handle_request

load_dotenv()
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

def main():
    print("Запуск MCP сервера", file=sys.stderr)
    while True:
        try:
            line = sys.stdin.readline()
            if not line:
                break
            print(f"Получен запрос: {line.strip()}", file=sys.stderr)
            request = json.loads(line.strip())
            response = handle_request(request)
            response_str = json.dumps(response, ensure_ascii=False)
            print(f"Отправляем ответ: {response_str}", file=sys.stderr)
            print(response_str)
            sys.stdout.flush()
        except Exception as e:
            print(f"Ошибка обработки запроса: {e}", file=sys.stderr)
            continue

if __name__ == "__main__":
    main()