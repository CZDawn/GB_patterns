from datetime import date
from views import Index, About, Contact, CreateCategory, CategoriesList, \
                  CreateTheme, ThemesList, CreatePodcast, PodcastsList


def date_front(request):
    request['date'] = date.today()

fronts_list = [date_front]

routes_list = {
    '/': Index(),
    '/about/': About(),
    '/podcasts/': CategoriesList(),
    '/contact/': Contact(),
    '/create_category/': CreateCategory(),
    '/create_theme/': CreateTheme(),
    '/themes_list/': ThemesList(),
    '/create_podcast/': CreatePodcast(),
    '/podcasts_list/': PodcastsList()
}

