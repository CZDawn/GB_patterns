from jsonpickle import dumps, loads
from czdawn_framework.templator import render


class AbstractObserver:

    def update(self, subject):
        pass


class AbstractSubject:

    def __init__(self):
        self.observers = []

    def notify(self):
        for observer in self.observers:
            observer.update(self)


class PushNotifier(AbstractObserver):

    def update(self, subject):
        print(('PUSH->', 'к нам присоединился', subject.listeners[-1].name))


class TemplateView:
    template_name = 'base_template.html'

    def get_template_context_data(self):
        return {}

    def get_template_name(self):
        return self.template_name

    def render_template_with_context_data(self):
        template_name = self.get_template_name()
        template_context = self.get_template_context_data()
        return '200 OK', render(template_name, **template_context)

    def __call__(self, request):
        return self.render_template_with_context_data()


class ListView(TemplateView):
    queryset = []
    template_name = 'list.html'
    context_object_name = 'objects_list'

    def get_queryset(self):
        print(self.queryset)
        return self.queryset

    def get_context_object_name(self):
        return self.context_object_name

    def get_template_context_data(self):
        queryset = self.get_queryset()
        context_object_name = self.get_context_object_name()
        context = {context_object_name: queryset}
        return context


class CreateView(TemplateView):
    template_name = 'create.html'

    @staticmethod
    def get_request_data(request):
        return request['data']

    def create_object(sef, data):
        pass

    def __call__(self, request):
        if request['method']  == 'POST':
            data = self.get_request_data(request)
            self.create_object(data)
            return self.render_template_with_context_data()
        else:
            return super().__call__(request)


class BaseSerializer:

    def __init__(self, obj):
        self.obj = obj

    def save(self):
        return dumps(self.obj)

    @staticmethod
    def load(data):
        return loads(data)


class ConsoleWriter:

    def write(self, text):
        print(text)


class FileWriter:

    def __init__(self):
        self.file_name = 'log'

    def write(self, text):
        with open(self.file_name, 'a', encoding='utf-8') as f:
            f.write(f'{text}\n')

