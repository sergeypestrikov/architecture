# Get request
class GetRequest:

    @staticmethod
    def input_data_parse(data: str):
        result = {}
        if data:
            # Разделяем параметры через &
            params = data.split('&')
            for item in params:
                # Разделяем ключ/значение через =
                k, v = item.split('=')
                result[k] = v
        return result

    @staticmethod
    def get_req_params(environ):
        # Получаем параметры запроса
        query_str = environ['QUERY_STRING']
        # Переводим параметры в словарь
        req_params = GetRequest.input_data_parse(query_str)
        return req_params


# Post request
class PostRequest:

    @staticmethod
    def input_data_parse(data: str):
        result = {}
        if data:
            # Разделяем параметры через &
            params = data.split('&')
            for item in params:
                # Разделяем ключ и значение через =
                k, v = item.split('=')
                result[k] = v
        return result

    @staticmethod
    def wsgi_get_input_data(env) -> bytes:
        # Получаем длину тела
        content_length_data = env.get('CONTENT_LENGTH')
        # Приводим значение к int
        content_length = int(content_length_data) if content_length_data else 0
        print(content_length)
        # Считываем данные (если они есть)
        # Запускаем на чтение
        data = env['wsgi.input'].read(content_length) if content_length > 0 else b''
        return data

    def wsgi_input_data_parse(self, data: bytes) -> dict:
        result = {}
        if data:
            # Декодируем данные
            data_str = data.decode(encoding='UTF-8')
            print(f'Декодированная строка: {data_str}')
            # Добавляем в словарь
            result = self.input_data_parse(data_str)
        return result

    def get_req_params(self, environ):
        # Получаем данные
        data = self.wsgi_get_input_data(environ)
        # Переводим данные в словарь
        data = self.wsgi_input_data_parse(data)
        return data

