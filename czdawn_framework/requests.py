from .services import parse_input_data, parse_wsgi_input_data, \
                      get_wsgi_input_data

class GetRequests:

    @staticmethod
    def get_request_params(environ):
        return parse_input_data(environ['QUERY_STRING'])


class PostRequests:

    @staticmethod
    def get_request_params(environ):
        data = get_wsgi_input_data(environ)
        return parse_wsgi_input_data(data)

