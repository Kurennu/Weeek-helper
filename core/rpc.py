from tools import (
    validate_all_project_tasks,
    validate_single_task_title,
    get_and_validate_task_by_id
)

def handle_request(request):
    method = request.get("method")
    request_id = request.get("id", 1)

    if method == "initialize":
        return {
            "jsonrpc": "2.0",
            "id": request_id,
            "result": {
                "protocolVersion": "2024-11-05",
                "capabilities": {"tools": {}},
                "serverInfo": {"name": "weeek-validator", "version": "1.0.0"}
            }
        }

    elif method == "tools/list":
        return {
            "jsonrpc": "2.0",
            "id": request_id,
            "result": {
                "tools": [
                    {
                        "name": "validate_task_titles",
                        "description": "Проверить заголовки всех задач в проекте",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "project_id": {"type": "string", "description": "ID проекта в Weeek"}
                            },
                            "required": ["project_id"]
                        }
                    },
                    {
                        "name": "validate_single_title",
                        "description": "Проверить заголовок задачи",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "title": {"type": "string", "description": "Заголовок задачи"}
                            },
                            "required": ["title"]
                        }
                    },
                    {
                        "name": "get_and_validate_task",
                        "description": "Получить задачу из Weeek и проверить заголовок",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "task_id": {"type": "string", "description": "ID задачи в Weeek"}
                            },
                            "required": ["task_id"]
                        }
                    }
                ]
            }
        }

    elif method == "tools/call":
        params = request.get("params", {})
        tool_name = params.get("name")
        arguments = params.get("arguments", {})

        if tool_name == "validate_task_titles":
            text = validate_all_project_tasks(arguments)
        elif tool_name == "validate_single_title":
            text = validate_single_task_title(arguments)
        elif tool_name == "get_and_validate_task":
            text = get_and_validate_task_by_id(arguments)
        else:
            text = "Неизвестный инструмент"

        return {
            "jsonrpc": "2.0",
            "id": request_id,
            "result": {
                "content": [
                    {"type": "text", "text": text}
                ]
            }
        }

    return {
        "jsonrpc": "2.0",
        "id": request_id,
        "error": {
            "code": -32601,
            "message": "Method not found"
        }
    }
