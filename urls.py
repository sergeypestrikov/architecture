from datetime import date
from views import Index, News, Courses, Contacts, Blog, GenerateCategory, CoursesCopy, CategoryList, GenerateCourse, Program


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
    '/program/': Program(),
    '/courses/': Courses(),
    '/contacts/': Contacts(),
    '/category_list/': CategoryList(),
    '/generate_category/': GenerateCategory(),
    '/generate_course/': GenerateCourse()
}