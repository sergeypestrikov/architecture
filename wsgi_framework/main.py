class PageNotFound:
    def __call__(self, request):
        return '404 Page not found'


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
        # Паттерн Page Controller. Находим нужный контроллер
        if path in self.routes_list:
            view = self.routes_list[path]
        else:
            view = PageNotFound()
        request = {}
        # Паттерн Front Controller
        # Наполняем словарь request элементами - получает все контроллеры
        for front_controller in self.fronts_list:
            front_controller(request)
        # Запуск контроллера с передачей объекта request
        code, body = view(request)
        start_response(code, [('Content type', 'text/html')])
        return [body.encode('UTF-8')]