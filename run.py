from wsgiref.simple_server import make_server

from views import routes
from urls import fronts_list
from components import settings
from czdawn_framework.main import CzdawnFramework


app = CzdawnFramework(settings, routes, fronts_list)

with make_server('', 8088, app) as httpd:
    print('Serving on port 8080...')
    httpd.serve_forever()

