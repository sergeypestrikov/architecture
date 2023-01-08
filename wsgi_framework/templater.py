# Используем шаблонизатор jinja2
from jinja2 import Template
from os.path import join


def render(template_name, folder='templates', **kwargs):
    '''
    :param template_name:
    :param folder:
    :param kwargs:
    :return:
    '''
    file_path = join(folder, template_name)
    # Открываем шаблон по имени
    with open(file_path, encoding='UTF-8') as f:
        # Читаем
        template = Template(f.read())
    # Рендеринг шаблона с параметрами
    return template.render(**kwargs)