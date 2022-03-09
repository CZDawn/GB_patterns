from czdawn_framework.templator import render
from patterns.creational_patterns import Engine, Logger
from patterns.structural_patterns import RouteDecorator, CountTimeForMethodDecorator


engine_obj = Engine()
logger = Logger('main')
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

