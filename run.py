from wsgiref.simple_server import make_server
from czdawn_framework.main import CzdawnFramework
from urls import routes_list, fronts_list

with make_server('', 8080, CzdawnFramework(routes_list, fronts_list)) as httpd:
    print('Serving on port 8080...')
    httpd.serve_forever()

