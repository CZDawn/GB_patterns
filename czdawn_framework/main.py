'''
This is the core module of framework, that contains its main logic.
'''

from .errors import PageNotFound404
from .requests import GetRequests, PostRequests
from .services import decode_value, get_content_type, get_static


class CzdawnFramework:
    '''This class managing framework functionality.'''

    def __init__(self, settings, routes, fronts):
        self.routes_list = routes
        self.fronts_list = fronts
        self.settings = settings

    def __call__(self, environ, start_response):
        path = environ['PATH_INFO']

        if not path.endswith('/'):
            path = f'{path}/'

        request = {}
        method = environ['REQUEST_METHOD']
        request['method'] = method

        if method == 'POST':
            data = PostRequests().get_request_params(environ)
            request['data'] = decode_value(data)
        if method == 'GET':
            params = GetRequests().get_request_params(environ)
            request['request_params'] = decode_value(params)

        if path in self.routes_list:
            view = self.routes_list[path]
            content_type = get_content_type(path)
            code, body = view(request)
            body = body.encode('utf-8')
        elif path.startswith(self.settings.STATIC_URL):
            file_path = path[len(self.settings.STATIC_URL):len(path)-1]
            content_type = get_content_type(file_path)
            code, body = get_static(self.settings.STATIC_FILES_DIR, file_path)
        else:
            view = PageNotFound404()
            content_type = get_content_type(path)
            code, body = view(request)
            body = body.encode('utf-8')

        if path in self.routes_list and self.fronts_list:
            view = self.routes_list[path]
            for front in self.fronts_list:
                front(request)
            code, body = view(request)
            body = body.encode('utf-8')

        start_response(code, [('Content-Type', content_type)])
        return [body]

