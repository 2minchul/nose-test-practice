# Third-party imports...
from nose.tools import assert_true, assert_is_not_none, assert_list_equal, assert_is_none
from unittest.mock import Mock, patch
import requests

from services import get_todos, get_uncompleted_todos


def test_request_response():
    # Send a request to the API server and store the response.
    response = requests.get('http://jsonplaceholder.typicode.com/todos')

    # Confirm that the request-response cycle completed successfully.
    assert_true(response.ok)


def test_get_todos():
    # Call the service, which will send a request to the server.
    response = get_todos()

    # If the request is sent successfully, then I expect a response to be returned.
    assert_is_not_none(response)


# ways to patch

@patch('services.requests.get')
def test_getting_todos_decorator(mock_get):
    # Configure the mock to return a response with an OK status code.
    mock_get.return_value.ok = True

    # Call the service, which will send a request to the server.
    response = get_todos()
    # If the request is sent successfully, then I expect a response to be returned.
    assert_is_not_none(response)


def test_getting_todos_with_context():
    with patch('services.requests.get') as mock_get:
        # Configure the mock to return a response with an OK status code.
        mock_get.return_value.ok = True

        # Call the service, which will send a request to the server.
        response = get_todos()

    # If the request is sent successfully, then I expect a response to be returned.
    assert_is_not_none(response)


def test_getting_todos_use_patcher():
    mock_get_patcher = patch('services.requests.get')

    # Start patching `requests.get`.
    mock_get = mock_get_patcher.start()

    # Configure the mock to return a response with an OK status code.
    mock_get.return_value.ok = True

    # Call the service, which will send a request to the server.
    response = get_todos()

    # Stop patching `requests.get`.
    mock_get_patcher.stop()

    # If the request is sent successfully, then I expect a response to be returned.
    assert_is_not_none(response)


# Mocking the complete service behavior

@patch('services.requests.get')
def test_getting_todos_when_response_is_ok(mock_get):
    todos = [{
        'userId': 1,
        'id': 1,
        'title': 'Make the bed',
        'completed': False
    }]

    # Configure the mock to return a response with an OK status code. Also, the mock should have
    # a `json()` method that returns a list of todos.
    mock_get.return_value = Mock(ok=True)
    mock_get.return_value.json.return_value = todos

    # Call the service, which will send a request to the server.
    response = get_todos()

    # If the request is sent successfully, then I expect a response to be returned.
    assert_list_equal(response.json(), todos)


@patch('services.requests.get')
def test_getting_todos_when_response_is_not_ok(mock_get):
    # Configure the mock to not return a response with an OK status code.
    mock_get.return_value.ok = False

    # Call the service, which will send a request to the server.
    response = get_todos()
    print(response)
    # If the response contains an error, I should get no todos.
    assert_is_none(response)  # response == None


# Mocking integrated functions

@patch('services.get_todos')
def test_getting_uncompleted_todos_when_todos_is_not_none(mock_get_todos):
    todo1 = {
        'userId': 1,
        'id': 1,
        'title': 'Make the bed',
        'completed': False
    }
    todo2 = {
        'userId': 1,
        'id': 2,
        'title': 'Walk the dog',
        'completed': True
    }

    # Configure mock to return a response with a JSON-serialized list of todos.
    mock_get_todos.return_value = Mock()
    mock_get_todos.return_value.json.return_value = [todo1, todo2]

    # Call the service, which will get a list of todos filtered on completed.
    uncompleted_todos = get_uncompleted_todos()

    # Confirm that the mock was called.
    assert_true(mock_get_todos.called)

    # Confirm that the expected filtered list of todos was returned.
    assert_list_equal(uncompleted_todos, [todo1])


@patch('services.get_todos')
def test_getting_uncompleted_todos_when_todos_is_none(mock_get_todos):
    # Configure mock to return None.
    mock_get_todos.return_value = None

    # Call the service, which will return an empty list.
    uncompleted_todos = get_uncompleted_todos()

    # Confirm that the mock was called.
    assert_true(mock_get_todos.called)

    # Confirm that an empty list was returned.
    assert_list_equal(uncompleted_todos, [])


# Refactoring tests to use classes
class TestTodos(object):
    @classmethod
    def setup_class(cls):
        cls.mock_get_patcher = patch('services.requests.get')
        cls.mock_get = cls.mock_get_patcher.start()

    @classmethod
    def teardown_class(cls):
        cls.mock_get_patcher.stop()

    def test_getting_todos_when_response_is_ok(self):
        # Configure the mock to return a response with an OK status code.
        self.mock_get.return_value.ok = True

        todos = [{
            'userId': 1,
            'id': 1,
            'title': 'Make the bed',
            'completed': False
        }]

        self.mock_get.return_value = Mock()
        self.mock_get.return_value.json.return_value = todos

        # Call the service, which will send a request to the server.
        response = get_todos()

        # If the request is sent successfully, then I expect a response to be returned.
        assert_list_equal(response.json(), todos)

    def test_getting_todos_when_response_is_not_ok(self):
        # Configure the mock to not return a response with an OK status code.
        self.mock_get.return_value.ok = False

        # Call the service, which will send a request to the server.
        response = get_todos()

        # If the response contains an error, I should get no todos.
        assert_is_none(response)


class TestUncompletedTodos(object):
    @classmethod
    def setup_class(cls):
        cls.mock_get_todos_patcher = patch('services.get_todos')
        cls.mock_get_todos = cls.mock_get_todos_patcher.start()

    @classmethod
    def teardown_class(cls):
        cls.mock_get_todos_patcher.stop()

    def test_getting_uncompleted_todos_when_todos_is_not_none(self):
        todo1 = {
            'userId': 1,
            'id': 1,
            'title': 'Make the bed',
            'completed': False
        }
        todo2 = {
            'userId': 2,
            'id': 2,
            'title': 'Walk the dog',
            'completed': True
        }

        # Configure mock to return a response with a JSON-serialized list of todos.
        self.mock_get_todos.return_value = Mock()
        self.mock_get_todos.return_value.json.return_value = [todo1, todo2]

        # Call the service, which will get a list of todos filtered on completed.
        uncompleted_todos = get_uncompleted_todos()

        # Confirm that the mock was called.
        assert_true(self.mock_get_todos.called)

        # Confirm that the expected filtered list of todos was returned.
        assert_list_equal(uncompleted_todos, [todo1])

    def test_getting_uncompleted_todos_when_todos_is_none(self):
        # Configure mock to return None.
        self.mock_get_todos.return_value = None

        # Call the service, which will return an empty list.
        uncompleted_todos = get_uncompleted_todos()

        # Confirm that the mock was called.
        assert_true(self.mock_get_todos.called)

        # Confirm that an empty list was returned.
        assert_list_equal(uncompleted_todos, [])
