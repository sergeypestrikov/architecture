from datetime import date
from views import Index, News, Courses, Contacts, Blog


# Реализация Front Controller
def front_controller(request):
    request['date'] = date.today()


def other_front(request):
    request['key'] = 'key'


fronts = [front_controller, other_front]

routes = {
    '/': Index(),
    '/news/': News(),
    '/blog/': Blog(),
    '/courses/': Courses(),
    '/contacts/': Contacts(),
}