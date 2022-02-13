'''
This method contains common functions for other project packages,
for not to copy the code (DRY).
'''

from os import path
from quopri import decodestring
from components.content_types import CONTENT_TYPES_MAP


def parse_input_data(data: str) -> dict:
    result = {}
    if data:
        params = data.split('&')
        for param in params:
            key, value = param.split('=')
            result[key] = value
    return result

def parse_wsgi_input_data(data: bytes) -> dict:
    if data:
        data_to_str = data.decode(encoding='utf-8')
    return parse_input_data(data_to_str)

def get_wsgi_input_data(environ) -> bytes:
    content_length = environ.get('CONTENT_LENGTH')
    content_length = int(content_length) if content_length else 0

    data = environ['wsgi.input'].read(content_length) \
            if content_length > 0 else b''
    return data

def decode_value(data):
    new_data = {}
    for key, value in data.items():
        value = bytes(value.replace('%', '=').replace('+', ' '), 'UTF-8')
        decode_value_to_str = decodestring(value).decode('UTF-8')
        new_data[key] = decode_value_to_str
    return new_data

def get_content_type(file_path, content_types_map=CONTENT_TYPES_MAP):
    file_name = path.basename(file_path).lower()
    extension = path.splitext(file_name)[1]
    return content_types_map.get(extension, "text/html")

def get_static(static_dir, file_path):
    path_to_file = path.join(static_dir, file_path)
    with open(path_to_file, 'rb') as file:
        file_content = file.read()
    status_code = '200 OK'
    return status_code, file_content

