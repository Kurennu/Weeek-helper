# test_server.py
import subprocess
import json
import time

def test_server():
    proc = subprocess.Popen(['python', 'main.py'], 
                           stdin=subprocess.PIPE, 
                           stdout=subprocess.PIPE, 
                           stderr=subprocess.PIPE,
                           text=True)
    
    init_request = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "initialize",
        "params": {
            "protocolVersion": "2024-11-05",
            "capabilities": {},
            "clientInfo": {"name": "test", "version": "1.0.0"}
        }
    }
    
    proc.stdin.write(json.dumps(init_request) + '\n')
    proc.stdin.flush()
    
    response = proc.stdout.readline()
    print(f"Initialize response: {response}")
    
    proc.terminate()

if __name__ == "__main__":
    test_server()