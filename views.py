from datetime import date

from wsgi_framework.templater import render
from patterns.generative import Engine, Logger

site = Engine()
logger = Logger('main')

# Обработчики запросов (вьюшки)


# Контроллер - главная страница
class Index:
    def __call__(self, request):
        return '200 OK', render('index.html', objects_list=site.categories)


# Контроллер - новости
class News:
    def __call__(self, request):
        return '200 OK', render('news.html', date=date.today())


# Контроллер - блог
class Blog:
    def __call__(self, request):
        return '200 OK', render('blog.html')


# Контроллер - контакты
class Contacts:
    def __call__(self, request):
        return '200 OK', render('contacts.html')


# Контроллер - программа обучения
class Program:
    def __call__(self, request):
        return '200 OK', render('program.html', date=date.today())


# Контроллер 404
class NotFound404:
    def __call__(self, request):
        return '404 WHAT', '404 PAGE Not Found'


# Контроллер - курсы
class Courses:
    def __call__(self, request):
        logger.log('Список курсов')
        try:
            category = site.find_category_by_id(int(request['request_params']['id']))
            return '200 OK', render('courses.html', objects_list=category.courses, name=category.name, id=category.id)

        except KeyError:
            return '200 OK', 'There is no such course yet'


# Контроллер - создание курса
class GenerateCourse:
    category_id = -1

    def __call__(self, request):
        if request['method'] == 'POST':
            # Метод пост
            data = request['data']
            name = data['name']
            name = site.decode_value(name)

            category = None
            if self.category_id != -1:
                category = site.find_category_by_id(int(self.category_id))

                course = site.generate_course('online', name, category)
                site.courses.append(course)

            return '200 OK', render('courses.html', objects_list=category.courses, name=category.name, id=category.id)
        else:
            try:
                self.category_id = int(request['request_params']['id'])
                category = site.find_category_by_id(int(self.category_id))

                return '200 OK', render('generate_course.html', name=category.name, id=category.id)

            except KeyError:
                return '200 OK', 'There is no such category yet'


# Контроллер - создание категории
class GenerateCategory:
    def __call__(self, request):

        if request['method'] == 'POST':
            # Метод пост
            data = request['data']
            name = data['name']
            name = site.decode_value(name)

            category_id = data.get('category_id')

            category = None
            if category_id:
                category = site.find_category_by_id(int(category_id))

            new_category = site.generate_category(name, category)

            site.categories.append(new_category)
            return '200 OK', render('index.html', objects_list=site.categories)
        else:
            categories = site.categories
            return '200 OK', render('generate_category.html', categories=categories)


# Контроллер - список категорий
class CategoryList:
    def __call__(self, request):
        logger.log('Список категорий')
        return '200 OK', render('category_list.html', objects_list=site.categories)


# Контроллер - копир курса
class CoursesCopy:
    def __call__(self, request):
        request_params = request['request_params']

        try:
            name = request_params['name']

            current_course = site.get_course(name)
            if current_course:
                new_name = f'copy_{name}'
                new_course = current_course.replica()
                new_course.name = new_name
                site.courses.append(new_course)
            return '200 OK', render('courses.html', objects_list=site.courses, name=new_course.category.name)

        except KeyError:
            return '200 OK', 'There is no such course yet'
