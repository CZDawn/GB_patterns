'''
This module contains all functions,
classes to show errors which occure in the project.
'''


class PageNotFound404:
    def __call__(self, request):
        return '404', '404 PAGE NOT FOUND'

