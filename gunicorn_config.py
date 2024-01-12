bind = "127.0.0.1:8000"  # Замените 8000 на порт, который вы хотите использовать
workers = 2
worker_class = "sync"
module = "djangoProject.wsgi"