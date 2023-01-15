# Используем шаблонизатор jinja2

from jinja2 import FileSystemLoader
from jinja2.environment import Environment


def render(template_name, folder='templates', **kwargs):
    '''
    :param template_name: имя шаблона
    :param kwargs: параметры для передачи в шаблон
    :return:
    '''
    # Создаем объект окружения
    env = Environment()
    # Указываем папку для поиска шаблонов
    env.loader = FileSystemLoader(folder)
    # Находим шаблон
    template = env.get_template(template_name)
    return template.render(**kwargs)