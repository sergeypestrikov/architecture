from jsonpickle import dumps, loads
from wsgi_framework.templater import render


# Курс
# Наблюдатель - the pattern
# Тот кто следит
class Observer:
    def update(self, subject):
        pass


# Тот за кем следят (предок курса)
class Subject:
    def __init__(self):
        self.observers = []

    def notify(self):
        for item in self.observers:
            item.update(self)


class SMSNotifier(Observer):
    def update(self, subject):
        print('SMS', 'в нашей школе новый студент', subject.students[-1].name)


class EmailNotifier(Observer):
    def update(self, subject):
        print('e-mail', 'в нашей школе новый студент', subject.students[-1].name)


class Serializer:
    def __init__(self, obj):
        self.obj = obj

    def dump(self):
        return dumps(self.obj)

    @staticmethod
    def load(data):
        return loads(data)


# Шаблонный метод
class TemplateView:
    # Простейший рендеринг шаблона с передачей контекста
    template_name = 'template.html'

    def get_context_data(self):
        return {}

    def get_template(self):
        return self.template_name

    # Алгоритм
    def render_template_context(self):
        template_name = self.get_template()
        context = self.get_context_data()
        return '200 OK', render(template_name, **context)

    def __call__(self, request):
        return self.render_template_context()


# Тоже рендеринг
class ListView(TemplateView):
    queryset = []
    template_name = 'list.html'
    context_obj_name = 'objects.list'

    # Действие
    def get_queryset(self):
        print(self.queryset)
        return self.queryset

    def get_context_obj_name(self):
        return self.context_obj_name

    # Алгоритм
    def get_context_data(self):
        queryset = self.get_queryset()
        context_obj_name = self.get_context_obj_name()
        context = {context_obj_name: queryset}
        return context


class CreateView(TemplateView):
    template_name = 'create.html'

    # Получение данных из запроса
    @staticmethod
    def get_request_data(request):
        return request['data']

    def create_object(self, data):
        pass

    def __call__(self, request):
        if request['method'] == 'POST':
            data = self.get_request_data(request)
            self.create_object(data)

            return self.render_template_context()
        else:
            return super().__call__(request)


# Стратегия the pattern
class ConsoleLog:
    def write(self, text):
        print(text)


class FileLog:
    def __init__(self):
        self.file_name = 'log'

    def write(self, text):
        with open(self.file_name, 'a', encoding='UTF-8') as f:
            f.write(f'{text}\n')