from time import time


# Декоратор the pattern
class MainRoute:
    def __init__(self, routes, url):
        '''
        Сохранение значения переданного параметра
        :param routes:
        :param url:
        '''
        self.routes = routes
        self.url = url

    def __call__(self, cls):
        '''
        Собственно декоратор
        :param cls:
        :return:
        '''
        self.routes[self.url] = cls()


# Декоратор для логирования времени срабатывания того или иного метота
class TimeLog:
    def __init__(self, name):
        self.name = name
    def __call__(self, cls):
        '''
        Собственно декоратор
        :param cls:
        :return:
        '''
        # Доп функция для декора каждого отдельного метода класса
        def right_now(method):
            '''
            Декоратор класса wrapper обертывает в right_now
            каждый метод декорируемого класса
            :param method:
            :return:
            '''
            def period(*args, **kwargs):
                start = time()
                result = method(*args, **kwargs)
                end = time()
                point = end - start

                print(f'{self.name} выполнялся {point:2.2f} ms')
                return result
            return period
        return right_now(cls)