import json
import requests

try :
    users = requests.get('https://json.medrating.org/users')
    users_data = json.loads(users.text)
    todos = requests.get('https://json.medrating.org/todos')
    todo_data = json.loads(todos.text)
except:
    print("Error in converting to json or in API correctness")
