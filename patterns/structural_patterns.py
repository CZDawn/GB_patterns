from time import time


class RouteDecorator:
    def __init__(self, routes, url):
        self.url = url
        self.routes = routes

    def __call__(self, cls):
        self.routes[self.url] = cls()


class CountTimeForMethodDecorator:
    def __init__(self, name):
        self.name = name

    def __call__(self, cls):
        def count_time_for_method(method):
            def counted(*args, **kw):
                start_time = time()
                method_result = method(*args, **kw)
                end_time = time()
                delta = end_time - start_time

                print(f'debug --> {self.name} выполнялся {delta:2.2f} ms')
                return method_result
            return counted
        return count_time_for_method(cls)

