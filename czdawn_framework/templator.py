'''
This module implement logic of templator jinja2 work.
'''

from os.path import join
from jinja2 import Environment, FileSystemLoader
# from jinja2 import Template


def render(template_name, folder='templates', static_url='/static/', **kwargs):
    env = Environment()
    env.loader = FileSystemLoader(folder)
    env.globals['static'] = static_url
    template = env.get_template(template_name)
    return template.render(**kwargs)
    # path_to_file = join(folder, template_name)
    # with open(path_to_file, encoding='utf-8') as file:
    #     template = Template(file.read())
    # return template.render(**kwargs)
