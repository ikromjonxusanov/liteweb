# LiteWeb

LiteWeb is a lightweight web framework for building web applications in Python. It supports common HTTP methods and allows for easy routing and middleware integration.

## Features

- Supports GET, POST, PUT, PATCH, DELETE methods
- Middleware support for global and route-specific middlewares
- Simple routing mechanism
- Template rendering

## Usage

### Creating a LiteWeb Application

```python
from main import LiteWeb

# Define global middleware
def global_middleware(environ):
    print('Global middleware')

# Create an instance of LiteWeb
lite = LiteWeb(middlewares=[global_middleware])

# Define routes
@lite.get('/users/{pk}', middlewares=[])
def get_users(req, res, pk):
    res.send(['Ikromjon', 'Zohid'][int(pk)])

@lite.post('/users')
def post_users(req, res):
    res.send('User created!', '201 Created')

@lite.route('/', middlewares=[])
class User:
    def __init__(self):
        pass

    def get(req, res):
        res.render('example.html', {'name': 'Ikromjon', 'message': 'Hello, World!'})

    def post(req, res):
        res.send('User created!', '201 Created')

    def put(req, res):
        res.send('User updated!', '200 OK')

    def delete(req, res):
        res.send('User deleted!', '200 OK')