from wsgi_framework.templater import render


# Обработчики запросов (вьюшки)
class Index:
    def __call__(self, request):
        return '200 OK', render('index.html', date=request.get('date', None))


class About:
    def __call__(self, request):
        return '200 OK', 'about'


class Blog:
    def __call__(self, request):
        return '200 OK', 'blog'


class Courses:
    def __call__(self, request):
        return '200 OK', 'courses'


class Contacts:
    def __call__(self, request):
        return '200 OK', 'contacts'