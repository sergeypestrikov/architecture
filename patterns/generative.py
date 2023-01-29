from copy import deepcopy
from quopri import decodestring
from patterns.behavioral import Subject, FileLog


# Абстрактный класс пользователя
class User:
    def __init__(self, name):
        self.name = name


# Преподаватель
class Teacher(User):
    pass


# Студент
class Student(User):
    def __init__(self, name):
        self.courses = []
        super().__init__(name)


class UserFactory:
    users = {
        'teacher': Teacher,
        'student': Student
    }

    # Фабричный метод the pattern
    @classmethod
    def generate(cls, type_, name):
        return cls.users[type_](name)


# Прототип the pattern
class CoursesProto:
    # Прототип обучающих курсов
    def replica(self):
        return deepcopy(self)


class Course(CoursesProto, Subject):
    def __init__(self, name, category):
        self.name = name
        self.category = category
        self.category.courses.append(self)
        self.students = []
        super().__init__()

    def __getitem__(self, item):
        return self.students[item]

    def add_student(self, student: Student):
        self.students.append(student)
        student.courses.append(self)
        self.notify()


# Очные курсы
class OfflineCourses(Course):
    pass


# Онлайн курсы
class OnlineCourses(Course):
    pass


# Каталог (категории)
class Category:
    category_id = 0

    def __init__(self, name, category):
        self.id = Category.category_id
        Category.category_id += 1
        self.name = name
        self.category = category
        self.courses = []

    def courses_counter(self):
        result = len(self.courses)
        if self.category:
            result += self.category.courses_counter()
        return result


class CoursesFactory:
    types = {
        'offline': OfflineCourses,
        'online': OnlineCourses
    }

    # Фабричный метод the pattern
    @classmethod
    def generate(cls, type_, name, category):
        return cls.types[type_](name, category)


# Основной интерфейс
class Engine:
    def __init__(self):
        self.teachers = []
        self.students = []
        self.courses = []
        self.categories = []

    @staticmethod
    def generate_user(type_, name):
        return UserFactory.generate(type_, name)

    @staticmethod
    def generate_category(name, category=None):
        return Category(name, category)

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

    def get_student(self, name) -> Student:
        for item in self.students:
            if item.name == name:
                return item

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
    def __init__(self, name, writer=FileLog()):
        self.name = name
        self.writer = writer

    def log(self, text):
        text = f'loger says: {text}, '
        self.writer.write(text)