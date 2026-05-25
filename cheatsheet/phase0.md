# 🎓 ПОЛНАЯ ШПАРГАЛКА ФАЗЫ 0: AI Engineering from Scratch

> *"От копипаста до инженерного мышления. Всё, что нужно знать AI-инженеру для старта."*

---

## 🎯 МИССИЯ ФАЗЫ 0

Построить **профессиональную инфраструктуру** для разработки AI-приложений. После этой фазы ты:
- ✅ Не боишься терминала и Linux-серверов
- ✅ Умеешь изолировать проекты (venv, Docker)
- ✅ Версионируешь код (Git) и данные (HF Hub)
- ✅ Отлаживаешь "молчаливые" баги нейросетей
- ✅ Упаковываешь AI-стек в контейнеры

---

## 🗺 КАРТА ИНСТРУМЕНТОВ

| Инструмент | Для чего | Когда использовать |
|-----------|----------|-------------------|
| **Git + GitHub** | Версионирование кода | Всегда |
| **uv** | Пакетный менеджер Python | Установка библиотек |
| **pyproject.toml + uv.lock** | Рецепт среды | Для воспроизводимости |
| **VS Code + Pylance** | Редактор кода | Написание кода |
| **JupyterLab** | Эксперименты | Прототипирование |
| **Docker + Compose** | Изоляция стека | GPU-тренировки, деплой |
| **Hugging Face `datasets`** | Загрузка данных | Работа с датасетами |
| **PyTorch** | Нейросети | Фаза 1+ |
| **Linux (WSL2)** | Серверная среда | Облачные GPU |

---

## 📚 СВОДКА ПО УРОКАМ

### 🟢 УРОК 1: Dev Environment
**Проблема:** Нужна система контроля версий.  
**Решение:** Git + GitHub.  
**Команды:**
```bash
git clone <url>
git status
git add .
git commit -m "message"
git push origin main
```
**Артефакт:** Репозиторий на GitHub.

---

### 🟢 УРОК 2: First API Call
**Проблема:** Нужно работать с LLM (OpenRouter).  
**Решение:** `requests` + `.env` для секретов.  
**Код:**
```python
import os
from dotenv import load_dotenv
import requests

load_dotenv()
API_KEY = os.getenv("OPENROUTER_API_KEY")
```
**Артефакт:** `.env` (в `.gitignore`!), `lesson4_api_test.py`.

---

### 🟢 УРОК 3: Git in Practice
**Проблема:** Случайные и системные файлы засоряют репозиторий.  
**Решение:** `.gitignore` + атомарные коммиты.  
**Правило:** *Один коммит = одно логическое изменение.*

---

### 🟢 УРОК 4: Python Environments (uv)
**Проблема:** Dependency Hell (конфликт версий библиотек).  
**Решение:** `uv` + `pyproject.toml` + `uv.lock`.  
**Команды:**
```powershell
uv venv
.\.venv\Scripts\activate
uv add torch numpy
uv sync  # восстановить среду из lock-файла
```
**Артефакты:** `pyproject.toml`, `uv.lock`, `.python-version`.

---

### 🟢 УРОК 5: Jupyter Notebooks
**Проблема:** Для экспериментов нужен интерактивный формат.  
**Решение:** JupyterLab + `uv add jupyterlab`.  
**Запуск:** `jupyter lab` → `http://localhost:8888`.

---

### 🟢 УРОК 6: Prompt Engineering
**Проблема:** Как правильно общаться с LLM.  
**Решение:** Markdown-структура промптов (Context, Role, Task).  
**Артефакты:** `outputs/prompt-*.md`.

---

### 🟢 УРОК 7: Docker for AI 🐳 (БОСС ФАЗЫ)
**Проблема:** *"У меня на машине работает"*, конфликт CUDA.  
**Решение:** Docker-контейнеры с GPU passthrough.

**Ключевые концепции:**
- **Image** = рецепт (застывший)
- **Container** = запущенный процесс
- **Volume** = "дырка в стене" (сохраняет данные)
- **Dockerfile** = инструкции для сборки

**Команды:**
```powershell
docker build -t my-env .
docker run --rm --gpus all -v ${PWD}:/workspace my-env
docker compose up -d
docker compose down
docker ps
docker images
```

**Структура `docker-compose.yml`:**
```yaml
services:
  ai-dev:
    build: .
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: all
              capabilities: [gpu]
    volumes:
      - ./:/workspace
    ports: ["8888:8888"]
  
  qdrant:
    image: qdrant/qdrant:v1.12.5
    ports: ["6333:6333"]
```

**Артефакты:** `Dockerfile`, `docker-compose.yml`, `.dockerignore`.

---

### 🟢 УРОК 8: Editor Setup
**Проблема:** Редактор не помогает писать код.  
**Решение:** VS Code + расширения + workspace settings.

**Главные расширения:**
- `ms-python.python` — база
- `ms-python.vscode-pylance` — автодополнение, проверка типов
- `ms-toolsai.jupyter` — блокноты
- `charliermarsh.ruff` — быстрый линтер
- `eamodio.gitlens` — история Git в коде
- `ms-vscode-remote.remote-ssh` — подключение к серверам

**`settings.json` (мастхев):**
```json
{
    "python.analysis.typeCheckingMode": "basic",
    "editor.formatOnSave": true,
    "editor.rulers": [88, 120],
    "notebook.output.scrolling": true,
    "files.autoSave": "afterDelay"
}
```

**Артефакты:** `.vscode/settings.json`, `.vscode/extensions.json`.

---

### 🟢 УРОК 9: Data Management
**Проблема:** Гигабайты датасетов убивают Git и диск.  
**Решение:** Hugging Face `datasets` + `.gitignore` для AI.

**Код:**
```python
from datasets import load_dataset

# Загрузка (с кэшем в ~/.cache/huggingface/)
ds = load_dataset("namespace/name", split="train")

# Стриминг (для больших датасетов)
ds = load_dataset("big/data", streaming=True)

# Конвертация
ds.to_parquet("data.parquet")  # ⭐ Золотой стандарт!
```

**Форматы данных:**
| Формат | Размер | Скорость | Когда |
|--------|--------|----------|-------|
| CSV | Большой | Медленно | Для людей |
| JSON | Большой | Медленно | Для API |
| **Parquet** | Маленький | Быстро | **Для AI** ⭐ |
| Arrow | — | Мгновенно | В памяти |

**Артефакты:** Обновленный `.gitignore`, `data_utils.py`, `prompt-data-helper.md`.

---

### 🟢 УРОК 10: Terminal & Shell
**Проблема:** Нужно работать на Linux-серверах.  
**Решение:** Bash + tmux + SSH.

**Топ команд:**
```bash
cat log.txt | grep "error" | wc -l    # Pipe
python train.py > out.log 2>&1        # Redirect
nohup python train.py &               # Background
tmux new -s train                     # Persistent session
# Ctrl+B, D — detach
tmux attach -t train                  # Reattach

# SSH port forwarding (Jupyter на сервере → локально)
ssh -L 8888:localhost:8888 user@server
```

**Артефакт:** `prompt-terminal-helper.md`.

---

### 🟢 УРОК 11: Linux for AI
**Проблема:** Все GPU-сервера на Linux.  
**Решение:** Базовые команды + WSL2.

**Survival Kit:**
```bash
# Навигация
pwd, ls -la, cd ~, cd ..

# Файлы
mkdir -p a/b/c, cp -r src/ backup/
rm -rf dir/, find . -name "*.pt"

# Права
chmod +x script.sh
sudo apt install -y htop

# Мониторинг
htop, nvidia-smi, df -h, du -sh *
```

**Артефакт:** `prompt-linux-helper.md`.

---

### 🟢 УРОК 12: Debugging & Profiling 🔥
**Проблема:** AI-код падает молча (NaN, shape mismatch).  
**Решение:** debug_print, breakpoint, TensorBoard.

**4 главных врага:**
1. **Shape Mismatch** — тензор не той формы
2. **NaN Loss** — взрыв градиентов
3. **Data Leakage** — 99% accuracy = баг
4. **Wrong Device** — тензор на CPU вместо GPU

**Код:**
```python
def debug_print(name, tensor):
    print(f"{name}: shape={tensor.shape}, "
          f"dtype={tensor.dtype}, device={tensor.device}, "
          f"min={tensor.min():.4f}, max={tensor.max():.4f}, "
          f"has_nan={tensor.isnan().any()}")

# Условный breakpoint
if loss.item() > 100 or torch.isnan(loss):
    breakpoint()  # pdb: p tensor.shape, c (continue), q (quit)
```

**Артефакты:** `debug_tools.py`, `prompt-debug-ai-code.md`, установленный PyTorch.

---

## 🔥 ТОП-30 КОМАНД, КОТОРЫЕ НУЖНО ЗНАТЬ

### Git
```bash
1.  git status
2.  git add .
3.  git commit -m "msg"
4.  git push origin main
5.  git log --oneline
```

### uv (Python)
```powershell
6.  uv venv
7.  uv add <package>
8.  uv sync
9.  uv pip list
10. uv run python script.py
```

### Docker
```powershell
11. docker build -t name .
12. docker run --rm -it image
13. docker compose up -d
14. docker compose down
15. docker ps
```

### Linux / Bash
```bash
16. ls -la / cd / pwd
17. mkdir -p / cp -r / rm -rf
18. grep "pattern" file
19. cat | grep | wc -l
20. chmod +x script.sh
21. sudo apt install pkg
22. df -h / du -sh *
```

### Python / Debug
```python
23. breakpoint()
24. import pdb; pdb.set_trace()
25. print(tensor.shape, tensor.device)
26. torch.isnan(tensor).any()
```

### HF Datasets
```python
27. load_dataset("ns/name", split="train")
28. ds.to_parquet("file.parquet")
29. load_dataset(..., streaming=True)
30. hf_hub_download(repo_id, filename)
```

---

## 🚨 ЧАСТЫЕ ОШИБКИ И РЕШЕНИЯ

| Ошибка | Причина | Решение |
|--------|---------|---------|
| `ModuleNotFoundError` | Не активирован venv | `.\.venv\Scripts\activate` |
| `Permission denied` (Linux) | Нет прав | `chmod +x` или `sudo` |
| `CUDA out of memory` | Большой batch | Уменьшить batch_size |
| `NaN loss` | Высокий LR / деление на 0 | Уменьшить learning rate |
| `HfUriError: namespace/name` | Новый формат HF API | Добавить namespace (`author/dataset`) |
| `executable not found` (Docker) | Библиотека не установлена в образ | Добавить `pip install` в Dockerfile |
| `ECONNRESET` (VS Code Marketplace) | Сеть / провайдер | Включить VPN |
| `LF will be replaced by CRLF` | Windows vs Linux line endings | Игнорировать, Git сам разберётся |
| `Import "X" could not be resolved` | VS Code смотрит не в тот Python | `Ctrl+Shift+P` → Select Interpreter → `.venv` |
| `.venv` попал в Git | Нет в `.gitignore` | Добавить `.venv/` в `.gitignore` |
| Symlinks warning (HF on Windows) | Нет Developer Mode | Win+I → Для разработчиков → Включить |

---

## 🏗 АРХИТЕКТУРА ТВОЕГО ПРОЕКТА

```
ai-engineering-from-scratch/
├── .venv/                          # 🔒 Виртуальное окружение (НЕ в Git)
├── .vscode/                        # ✅ Настройки редактора
│   ├── settings.json
│   └── extensions.json
├── .git/                           # 🔒 История Git
├── .gitignore                      # ✅ Чёрный список для Git
├── .dockerignore                   # ✅ Чёрный список для Docker
├── .env                            # 🔒 Секреты (НЕ в Git!)
├── .python-version                 # ✅ Версия Python (3.12)
│
├── pyproject.toml                  # ✅ "Паспорт" проекта
├── uv.lock                         # ✅ Замороженные версии
├── Dockerfile                      # ✅ Рецепт Docker-образа
├── docker-compose.yml              # ✅ Оркестрация сервисов
│
├── phases/
│   └── 00-setup-and-tooling/       # Уроки Фазы 0
│       ├── 01-dev-environment/
│       ├── 07-docker-for-ai/
│       └── 12-debugging-and-profiling/
│
├── outputs/                        # ✅ Артефакты (промпты, отчёты)
│   ├── prompt-data-helper.md
│   ├── prompt-terminal-helper.md
│   ├── prompt-linux-helper.md
│   └── prompt-debug-ai-code.md
│
└── lesson_5_lab.ipynb              # ✅ Твои эксперименты
```

**Легенда:**
- ✅ — коммитится в Git
- 🔒 — в `.gitignore`, только локально

---

## 🔄 ВОССТАНОВЛЕНИЕ СРЕДЫ С НУЛЯ

Если ты потерял `.venv` или переехал на другой компьютер:

```powershell
# 1. Клонировать репозиторий
git clone https://github.com/you/ai-engineering-from-scratch.git
cd ai-engineering-from-scratch

# 2. Восстановить Python-среду из lock-файла
uv sync

# 3. Активировать
.\.venv\Scripts\activate

# 4. Запустить Docker-стек (если нужен)
docker compose up -d

# 5. Открыть Jupyter
jupyter lab
```

**Всё. Среда восстановлена побитово идентично.** Это сила `uv.lock` + Docker.

---

## 🎯 ПРИНЦИПЫ ИНЖЕНЕРА (запомни навсегда)

1. **Атомарные коммиты:** 1 коммит = 1 логическое изменение.
2. **Infrastructure as Code:** Настройки (`settings.json`, `Dockerfile`) в Git, не в голове.
3. **Lockfiles:** Всегда коммить `uv.lock` для воспроизводимости.
4. **Изоляция:** Каждый проект — свой venv + свой Docker.
5. **Секреты в `.env`:** Никогда не коммить API-ключи.
6. **Тяжёлые файлы мимо Git:** `.gitignore` для `.safetensors`, `.bin`, `.parquet`.
7. **Читай логи:** 90% багов можно найти, просто прочитав вывод.
8. **Не верь, проверяй:** `debug_print` после каждой подозрительной операции.
9. **Линтер — помощник, не начальник:** `# type: ignore` для сложных случаев.
10. **Код и артефакты — твоя долгосрочная память**, а не голова или чат.

---

## 🚀 ГОТОВНОСТЬ К ФАЗЕ 1: Math Foundations

### Что тебя ждёт:
- 🧮 **Линейная алгебра:** векторы, матрицы, тензоры
- 📈 **Матанализ:** производные, градиенты, chain rule
- 🤖 **Нейросети с нуля:** на чистом NumPy, без PyTorch!
- 🎯 **Backpropagation:** напишешь своими руками

### Что взять с собой:
- ✅ `uv` + `numpy` + `matplotlib` (уже установлены)
- ✅ Навык работы в Jupyter
- ✅ Понимание shape/dtype/device
- ✅ `debug_print` для проверки тензоров

### Что оставить позади:
- Страх "чистого листа" (мы будем писать по строчке)
- Синдром "копипастера" (поймёшь каждую операцию)
- Боязнь математики (объясню простыми словами)

---

## 💎 ФИНАЛЬНАЯ МЫСЛЬ

> *"Разница между слепым копировальщиком и инженером не в том, кто пишет код из головы. А в том, кто умеет читать логи, понимать архитектуру и чинить ошибки."*

Ты больше не `Ctrl+C → Ctrl+V`. Ты **AI-инженер** с:
- 🏭 Заводом (Docker)
- ⛽ Топливом (HF Datasets)
- 🛠 Инструментами (uv, VS Code, PyTorch)
- 📋 Инструкцией (Git-история)

**Фаза 0 закрыта. Добро пожаловать в Фазу 1!** 🎓🚀

---

*📌 Совет: сохрани эту шпаргалку как `outputs/phase0-cheatsheet.md` и возвращайся к ней, когда забудешь команду или концепцию.*