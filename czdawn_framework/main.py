'''
This is the core module of framework, that contains its main logic.
'''

from .errors import PageNotFound404


class CzdawnFramework:
    '''This class managing framework functionality.'''

    def __init__(self, routes, fronts):
        self.routes_list = routes
        self.fronts_list = fronts

    def __call__(self, environ, start_response):
        path = environ['PATH_INFO']

        if not path.endswith('/'):
            path = f'{path}/'

        if path in self.routes_list:
            view = self.routes_list[path]
        else:
            view = PageNotFound404()

        request = {}
        for front in self.fronts_list:
            front(request)
        code, body = view(request)
        start_response(code, [('Content-Type', 'text/html')])
        return [body.encode('utf-8')]

