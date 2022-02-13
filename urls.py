from datetime import date
from views import Index, About, Podcasts, Contact

def date_front(request):
    request['date'] = date.today()

fronts_list = [date_front]

routes_list = {
    '/': Index(),
    '/about/': About(),
    '/podcasts/': Podcasts(),
    '/contact/': Contact(),
}

