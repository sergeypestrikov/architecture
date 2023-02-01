from quopri import decodestring
from wsgi_framework.requester import GetRequest, PostRequest


class PageNotFound:
    def __call__(self, request):
        return '404 What', '404 Page not found'


class Framework:
    '''Это основа нашего фреймворка'''
    def __init__(self, routes, fronts):
        self.routes_list = routes
        self.fronts_list = fronts

    def __call__(self, environ, start_response):
        # Получаем адрес по которому выполнен переход
        path = environ['PATH_INFO']
        # Добавляем косую черту в путь
        if not path.endswith('/'):
            path = f'{path}/'

        request = {}
        # Получаем все данные запроса
        method = environ['REQUEST_METHOD']
        request['method'] = method

        if method == 'POST':
            data = PostRequest().get_req_params(environ)
            request['data'] = Framework.decode_value(data)
            print(f'Пришел POST запрос: {Framework.decode_value(data)}')
        if method == 'GET':
            req_params = GetRequest().get_req_params(environ)
            request['req_params'] = Framework.decode_value(req_params)
            print(f'Пришли GET параметры: {Framework.decode_value(req_params)}')

        # Паттерн Page Controller. Находим нужный контроллер
        if path in self.routes_list:
            view = self.routes_list[path]
        else:
            view = PageNotFound()
        # Паттерн Front Controller
        # Наполняем словарь request элементами - получает все контроллеры
        for front in self.fronts_list:
            front(request)
        # Запуск контроллера с передачей объекта request
        code, body = view(request)
        start_response(code, [('Content-Type', 'text/html')])
        return [body.encode('UTF-8')]

    @staticmethod
    def decode_value(data):
        # Решение проблемы с кодировкой (что бы данные на кириллице корректно отображались)
        new_data = {}
        for k, v in data.items():
            value = bytes(v.replace('%', '=').replace('+', ' '), 'UTF-8')
            value_decode = decodestring(value).decode('UTF-8')
            new_data[k] = value_decode
        return new_data


# Новый вид WSGI App
# Первый - логирующий (для каждого запроса выводит инфу в консоль)
class LogApp(Framework):
    def __init__(self, routes, fronts):
        self.application = Framework(routes, fronts)
        super().__init__(routes, fronts)

    def __call__(self, env, start_response):
        print('LOGER MODE')
        print(env)
        return self.application(env, start_response)


# Новый вид WSGI App
# Второй - фейковый (на все запросы отвечает 200 ОК, Fake
class FakeApp(Framework):
    def __init__(self, routes, fronts):
        self.application = Framework(routes, fronts)
        super().__init__(routes, fronts)

    def __call__(self, env, start_response):
        start_response('200 OK', [('Content-Type', 'text/html')])
        return [b'Its Fake']