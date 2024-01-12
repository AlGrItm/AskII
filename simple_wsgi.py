def application(environ, start_response):
    # Получаем метод запроса
    request_method = environ['REQUEST_METHOD']

    # Получаем и анализируем параметры GET
    query_string = environ.get('QUERY_STRING', '')
    get_params = dict(pair.split('=') for pair in query_string.split('&') if pair)

    # Получаем и анализируем параметры POST (если метод запроса POST)
    if request_method == 'POST':
        content_length = int(environ.get('CONTENT_LENGTH', 0))
        post_data = environ['wsgi.input'].read(content_length)
        post_params = dict(pair.split('=') for pair in post_data.decode('utf-8').split('&') if pair)
    else:
        post_params = {}

    # Список всех параметров (GET + POST)
    all_params = {**get_params, **post_params}

    # Формируем ответ
    status = '200 OK'
    response_headers = [('Content-type', 'text/plain')]
    response_body = f"Request Method: {request_method}\nParameters: {all_params}"

    # Отправляем ответ
    start_response(status, response_headers)
    return [response_body.encode('utf-8')]

if __name__ == '__main__':
    from gunicorn.app.wsgiapp import run
    run()
