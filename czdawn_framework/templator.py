'''
This module implement logic of templator jinja2 work.
'''

from os.path import join
from jinja2 import FileSystemLoader, Environment


def render(template_name, folder='templates', static_url='/static/', **kwargs):
    env = Environment()
    env.loader = FileSystemLoader(folder)
    env.globals['static'] = static_url
    template = env.get_template(template_name)
    return template.render(**kwargs)
