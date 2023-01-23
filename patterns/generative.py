from copy import deepcopy
from quopri import decodestring


# Абстрактный класс пользователя
class User:
    pass


# Преподаватель
class Teacher(User):
    pass


# Студент
class Student(User):
    pass


class UserFactory:
    users = {
        'teacher': Teacher,
        'student': Student
    }

    # Фабричный метод the pattern
    @classmethod
    def generate(cls, type_):
        return cls.users[type_]()


# Прототип the pattern
class CoursesProto:
    # Прототип обучающих курсов
    def replica(self):
        return deepcopy(self)


class Courses(CoursesProto):
    def __init__(self, name, category):
        self.name = name
        self.category = category
        self.category.courses.append(self)


# Очные курсы
class OfflineCourses(Courses):
    pass


# Онлайн курсы
class OnlineCourses(Courses):
    pass


class CoursesFactory:
    types = {
        'offline': OfflineCourses,
        'online': OnlineCourses
    }
    # Фабричный метод the pattern
    @classmethod
    def generate(cls, type_, name, category):
        return cls.types[type_](name, category)


# Каталог (категории)
class Catalog:
    category_id = 0

    def __init__(self, name, category):
        self.id = Catalog.category_id
        Catalog.category_id += 1
        self.name = name
        self.category = category
        self.courses = []

    def courses_counter(self):
        result = len(self.courses)
        if self.category:
            result += self.category.courses_counter()
        return result


# Основной интерфейс
class Engine:
    def __init__(self):
        self.teachers = []
        self.students = []
        self.courses = []
        self.categories = []

    @staticmethod
    def generate_user(type_):
        return UserFactory.generate(type_)

    @staticmethod
    def generate_category(name, category=None):
        return Catalog(name, category)

    def find_category_by_id(self, id):
        for item in self.categories:
            print('item', item.id)
            if item.id == id:
                return item
        raise Exception(f'Категории с id {id} не существует')

    @staticmethod
    def generate_course(type_, name, category):
        return CoursesFactory.generate(type_, name, category)

    def get_course(self, name):
        for item in self.courses:
            if item.name == name:
                return item
        return None

    @staticmethod
    def decode_value(val):
        value_bytes = bytes(val.replace('%', '=').replace('+', ' '), 'UTF-8')
        value_decode = decodestring(value_bytes)
        return value_decode.decode('UTF-8')


# Синглтон the pattern
class Singletone(type):
    def __init__(cls, name, bases, attrs, **kwargs):
        super().__init__(name, bases, attrs)
        cls.__instance = {}

    def __call__(cls, *args, **kwargs):
        if args:
            name = args[0]
        if kwargs:
            name = kwargs['name']

        if name in cls.__instance:
            return cls.__instance[name]
        else:
            cls.__instance[name] = super().__call__(*args, **kwargs)
            return cls.__instance[name]


# Логгер
class Logger(metaclass=Singletone):
    def __init__(self, name):
        self.name = name

    @staticmethod
    def log(text):
        print('logger says', text)