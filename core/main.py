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

    import os
    if not os.getenv("WEEEK_TOKEN"):
        print("КРИТИЧЕСКАЯ ОШИБКА: Нет токена WEEEK_TOKEN", file=sys.stderr)
        sys.exit(1)
    
    print("Токен найден, сервер готов к работе", file=sys.stderr)
    
    while True:
        try:
            line = sys.stdin.readline()
            if not line:
                print("Получен EOF, завершаем работу", file=sys.stderr)
                break
                
            line = line.strip()
            if not line:
                continue
                
            print(f"Получен запрос: {line}", file=sys.stderr)
            
            try:
                request = json.loads(line)
            except json.JSONDecodeError as e:
                print(f"Ошибка парсинга JSON: {e}", file=sys.stderr)
                continue
            
            response = handle_request(request)
            response_str = json.dumps(response, ensure_ascii=False)
            print(f"Отправляем ответ: {response_str}", file=sys.stderr)
            
            print(response_str)
            sys.stdout.flush()
            
        except KeyboardInterrupt:
            print("Получен сигнал прерывания", file=sys.stderr)
            break
        except Exception as e:
            print(f"Ошибка обработки запроса: {e}", file=sys.stderr)
            import traceback
            traceback.print_exc(file=sys.stderr)
            
            error_response = {
                "jsonrpc": "2.0",
                "id": 1,
                "error": {
                    "code": -32603,
                    "message": f"Внутренняя ошибка сервера: {str(e)}"
                }
            }
            print(json.dumps(error_response, ensure_ascii=False))
            sys.stdout.flush()

if __name__ == "__main__":
    main()