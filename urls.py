from datetime import date

def date_front(request):
    request['date'] = date.today()

fronts_list = [date_front]

