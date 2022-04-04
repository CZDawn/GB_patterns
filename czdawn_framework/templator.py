'''
This module implement logic of templator jinja2 work.
'''

from jinja2 import Template, FileSystemLoader
from jinja2.environment import Environment



def render(template_name, folder='templates', static_url='/static/', **kwargs):
    print(template_name)
    env = Environment()
    env.loader = FileSystemLoader(folder)
    env.globals['static'] = static_url
    template = env.get_template(template_name)
    return template.render(**kwargs)
