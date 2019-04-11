# Standard library imports...
from urllib.parse import urljoin

# Third-party imports...
import requests

TODOS_URL = urljoin('http://jsonplaceholder.typicode.com', 'todos')


def get_todos():
    response = requests.get(TODOS_URL)
    if response.ok:
        return response
    else:
        return None


def get_uncompleted_todos():
    response = get_todos()
    if response is None:
        return []
    else:
        todos = response.json()
        return [todo for todo in todos if todo.get('completed') == False]
