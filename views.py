from wsgi_framework.templater import render


# Обработчики запросов (вьюшки)
class Index:
    def __call__(self, request):
        return '200 OK', render('index.html', date=request.get('date', None))


class News:
    def __call__(self, request):
        return '200 OK', render('news.html', date=request.get('date', None))


class Blog:
    def __call__(self, request):
        return '200 OK', render('blog.html', date=request.get('date', None))


class Courses:
    def __call__(self, request):
        return '200 OK', render('courses.html', date=request.get('date', None))


class Contacts:
    def __call__(self, request):
        return '200 OK', render('contacts.html', date=request.get('date', None))