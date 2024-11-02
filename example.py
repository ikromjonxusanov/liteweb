from main import LiteWeb

def global_middleware(environ):
    print('Global middleware')

lite = LiteWeb()


@lite.get('/users/{pk}', middlewares=[global_middleware])
def get_users(req, res, pk):
    res.send(['Ikromjon', 'Zohid'][int(pk)])


@lite.post('/users')
def post_users(req, res):
    res.send('User created!', '201 Created')
    

@lite.route('/', middlewares=[global_middleware])
class User:
    def __init__(self):
        pass

    def get(req, res):
        res.send('User list')
    
    def post(req, res):
        res.send('User created!', '201 Created')
    
    def put(req, res):
        res.send('User updated!', '200 OK')
    
    def delete(req, res):
        res.send('User deleted!', '200 OK')
