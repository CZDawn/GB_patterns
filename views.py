from czdawn_framework.templator import render
from patterns.creational_patterns import Engine, Logger, MapperRegistry
from patterns.structural_patterns import RouteDecorator, CountTimeForMethodDecorator
from patterns.behavioral_patterns import CreateView, ListView, BaseSerializer, \
                                         PushNotifier, ConsoleWriter
from patterns.architectural_system_pattern_unit_of_work import UnitOfWork


engine_obj = Engine()
logger = Logger('main', ConsoleWriter())
push_notifier = PushNotifier()
UnitOfWork.new_current()
UnitOfWork.get_current().set_mapper_registry(MapperRegistry)

routes = {}

@RouteDecorator(routes=routes, url='/')
class Index:
    @CountTimeForMethodDecorator('Main page')
    def __call__(self, request):
        return '200 OK', render('index.html',
                             date=request.get('date', None))


@RouteDecorator(routes=routes, url='/about/')
class About:
    @CountTimeForMethodDecorator('About')
    def __call__(self, request):
        return '200 OK', render('about.html',
                             date=request.get('date', None))


@RouteDecorator(routes=routes, url='/contact/')
class Contact:
    @CountTimeForMethodDecorator('Contacts')
    def __call__(self, request):
        return '200 OK', render('contact.html',
                             date=request.get('date', None))

"""
@RouteDecorator(routes=routes, url='/create_category/')
class CreateCategory:
    @CountTimeForMethodDecorator('Create category')
    def __call__(self, request):
        if request['method'] == 'POST':
            data = request['data']
            name = data['name']
            name = engine_obj.decode_value(name)

            category = engine_obj.find_category_by_name(name)

            if category:
                return '200 OK', render('categories_list.html',
                                        objects_list=engine_obj.categories)
            else:
                new_category = engine_obj.create_category(name)
                engine_obj.categories.append(new_category)

                return '200 OK', render('categories_list.html',
                                        objects_list=engine_obj.categories)
        else:
            return '200 OK', render('create_category.html')


@RouteDecorator(routes=routes, url='/podcasts/')
class CategoriesList:
    @CountTimeForMethodDecorator('Categories list')
    def __call__(self, request):
        logger.log('Список категорий подкастов')
        return '200 OK', render('categories_list.html',
                                objects_list=engine_obj.categories)
"""

@RouteDecorator(routes=routes, url='/create_category/')
class CreateCategory(CreateView):
    template_name = 'create_category.html'

    def create_object(self, data: dict):
        name = data['name']
        name = engine_obj.decode_value(name)

        new_category = engine_obj.create_category(name)
        engine_obj.categories.append(new_category)
        new_category.mark_new()
        UnitOfWork.get_current().commit()

@RouteDecorator(routes=routes, url='/podcasts/')
class CategoriesList(ListView):
    template_name = 'categories_list.html'

    def get_queryset(self):
        mapper = MapperRegistry.get_current_mapper('category')
        return mapper.all()


@RouteDecorator(routes=routes, url='/create_theme/')
class CreateTheme:
    @CountTimeForMethodDecorator('Create theme')
    def __call__(self, request):
        if request['method'] == 'POST':
            data = request['data']
            name = data['name']
            category_id = data['category_id']
            name = engine_obj.decode_value(name)

            category = engine_obj.find_category_by_id(int(category_id))
            theme = engine_obj.find_theme_by_name(name)

            if theme:
                return '200 OK', render('themes_list.html',
                                        objects_list=engine_obj.themes,
                                        category=category)
            else:
                new_theme = engine_obj.create_theme(name, category)
                engine_obj.themes.append(new_theme)

                return '200 OK', render('themes_list.html',
                                        objects_list=engine_obj.themes,
                                        category=category)
        else:
            category_id = request['request_params']['category_id']
            category = engine_obj.find_category_by_id(int(category_id))

            return '200 OK', render('create_theme.html',
                                    category=category)


@RouteDecorator(routes=routes, url='/themes_list/')
class ThemesList:
    @CountTimeForMethodDecorator('Themes list')
    def __call__(self, request):
        logger.log('Список тем подкастов')
        category_id = request['request_params']['category_id']
        category = engine_obj.find_category_by_id(int(category_id))

        return '200 OK', render('themes_list.html',
                                objects_list=engine_obj.themes,
                                category=category)


@RouteDecorator(routes=routes, url='/create_podcast/')
class CreatePodcast:
    @CountTimeForMethodDecorator('Create podcast')
    def __call__(self, request):
        if request['method'] == 'POST':
            data = request['data']
            type_ = data['type_']
            name = data['name']
            category_id = data['category_id']
            theme_id = data['theme_id']
            author = data['author']
            type_ = engine_obj.decode_value(type_)
            name = engine_obj.decode_value(name)
            author = engine_obj.decode_value(author)

            category = engine_obj.find_category_by_id(int(category_id))
            theme = engine_obj.find_category_by_id(int(theme_id))

            podcast = engine_obj.find_podcast_by_name(name)
            if podcast:
                return '200 OK', render('podcasts_list.html',
                                        objects_list=engine_obj.podcasts,
                                        category=category,
                                        theme=theme)
            else:
                new_podcast = engine_obj.create_podcast(type_, name, category, theme, author)
                engine_obj.podcasts.append(new_podcast)

                return '200 OK', render('podcasts_list.html',
                                        objects_list=engine_obj.podcasts,
                                        category=category,
                                        theme=theme)
        else:
            category_id = request['request_params']['category_id']
            theme_id = request['request_params']['theme_id']
            category = engine_obj.find_category_by_id(int(category_id))
            theme = engine_obj.find_theme_by_id(int(theme_id))

            return '200 OK', render('create_podcast.html',
                                    category=category,
                                    theme=theme)


@RouteDecorator(routes=routes, url='/podcasts_list/')
class PodcastsList:
    @CountTimeForMethodDecorator('Podcasts list')
    def __call__(self, request):
        logger.log('Список подкастов')
        category_id = request['request_params']['category_id']
        theme_id = request['request_params']['theme_id']
        category = engine_obj.find_category_by_id(int(category_id))
        theme = engine_obj.find_theme_by_id(int(theme_id))

        return '200 OK', render('podcasts_list.html',
                                objects_list=engine_obj.podcasts,
                                category=category,
                                theme=theme)


@RouteDecorator(routes=routes, url='/copy_podcast/')
class CopyPodcast:
    @CountTimeForMethodDecorator('Copy podcast')
    def __call__(self, request):
        name = request['request_params']['name']
        old_podcast = engine_obj.find_podcast_by_name(name)
        if old_podcast:
            new_name = f'podcast_{name}_copy'
            new_podcast = old_podcast.clone()
            new_podcast.name = new_name
            engine_obj.podcasts.append(new_podcast)

        return '200 OK', render('podcasts_list.html',
                                objects_list=engine_obj.podcasts,
                                category=new_podcast.category.name)


@RouteDecorator(routes=routes, url='/listeners_list/')
class ListenersListView(ListView):
    template_name = 'listeners_list.html'

    def get_queryset(self):
        mapper = MapperRegistry.get_current_mapper('listener')
        return mapper.all()


@RouteDecorator(routes=routes, url='/create_listener/')
class ListenerCreateView(CreateView):
    template_name = 'create_listener.html'

    def create_object(self, data: dict):
        name = data['listener_name']
        surname = data['listener_surname']
        email = data['email']

        name = engine_obj.decode_value(name)
        surname = engine_obj.decode_value(surname)
        email = engine_obj.decode_value(email)

        new_listener = engine_obj.create_user('listener', name, surname, email)
        engine_obj.listeners.append(new_listener)
        new_listener.mark_new()
        UnitOfWork.get_current().commit()


@RouteDecorator(routes=routes, url='/add_listener/')
class AddListenerByPodcastCreateView(CreateView):
    template_name = 'add_listener.html'

    def get_template_context_data(self):
        context = super().get_template_context_data()
        context['podcasts'] = engine_obj.podcasts
        context['listeners'] = engine_obj.listeners
        return context

    def create_object(self, data: dict):
        podcast_name = data['podcast_name']
        podcast_name = engine_obj.decode_value(podcast_name)
        podcast = engine_obj.find_podcast_by_name(podcast_name)
        listener_name = data['listener_name']
        listener_name = engine_obj.decode_value(listener_name)
        listener = engine_obj.find_listener_by_name(listener_name)
        podcast.add_listener(listener)


@RouteDecorator(routes=routes, url='/api/')
class PodcastApi:
    @CountTimeForMethodDecorator('Podcast Api')
    def __call__(self, request):
        return '200 OK', BaseSerializer(engine_obj.podcasts).save()

