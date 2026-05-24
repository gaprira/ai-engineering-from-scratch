# 1. Базовый образ (легкий Linux с Python 3.12)
FROM python:3.12-slim

# 2. Устанавливаем рабочую папку
WORKDIR /workspace

# 3. Устанавливаем JupyterLab и наши любимые библиотеки прямо в системный Python контейнера
# (Внутри Docker это безопасная и стандартная практика!)
RUN pip install --no-cache-dir \
    jupyterlab \
    numpy \
    matplotlib \
    requests \
    openai \
    python-dotenv

# 4. Открываем порт 8888, чтобы мы могли зайти в Jupyter из браузера Windows
EXPOSE 8888

# 5. Команда по умолчанию (запускаем JupyterLab без пароля для удобства локальной разработки)
CMD ["jupyter", "lab", "--ip=0.0.0.0", "--port=8888", "--no-browser", "--allow-root", "--NotebookApp.token=''"]