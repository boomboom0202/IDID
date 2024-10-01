# IDID

## Описание
Проект IDID предназначен для выполнения задач детекций дефектов инсуляторов

## Шаги запуска программы
Следуйте инструкциям ниже, чтобы запустить программу на вашем компьютере:

1. **Клонируйте репозиторий:**
   ```bash
   git clone https://github.com/boomboom0202/IDID.git
   cd IDID
2. **Скачайте датасет:**
   ```bash
   https://drive.google.com/file/d/1WUmkx7HFu6ecRcGCK1OVC_uUtwt3pISL/view?usp=drive_link
4. **Создайте виртуальное окружение:**
   ```bash
   python -m venv env
5. **Активируйте виртуальное окружение**
   ```bash
   ./env/Scripts/activate(Windows)
   source env/bin/activate(Linux)
6. **Выберите kernel вашего виртуального окружения в вашей IDE.**
7. **Установите необходимую библиотеку:**
   ```bash
   pip install ultralytics
8. **Укажите путь к вашему датасету: В файле C:\Users\abyla\AppData\Roaming\Ultralytics\settings укажите путь к вашему датасету**
   ```bash
   "C:/Users/abyla/OneDrive/Рабочий стол/project/dataset"
9. **Настройте файл data.yaml: В файле data.yaml указать путь для train, val , test.**
   ```bash
   train: C:\Users\abyla\OneDrive\Рабочий стол\project\dataset\images\train
   val: C:\Users\abyla\OneDrive\Рабочий стол\project\dataset\images\val
   test: C:\Users\abyla\OneDrive\Рабочий стол\project\dataset\images\test
10 **Установить cuda для вашей видеокарты Например(для rtx 3060)**
   ```bash
   pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
Для других видеокарт можете посмотреть по ссылке
   https://pytorch.org/get-started/locally/
11 **Структура проекта**
### Описание структуры
- **project/**: Корневая директория вашего проекта.
  - **dataset/**: Директория, содержащая данные для обучения, тестирования и валидации.
    - **images/**: Директория с изображениями.
      - **train/**: Подкаталог с изображениями для обучения.
      - **test/**: Подкаталог с изображениями для тестирования.
      - **val/**: Подкаталог с изображениями для валидации.
    - **labels/**: Директория с метками для изображений.
      - **train/**: Подкаталог с метками для изображений, используемых в обучении.
      - **test/**: Подкаталог с метками для изображений, используемых в тестировании.
      - **val/**: Подкаталог с метками для изображений, используемых в валидации.
  - **data.yaml**: Файл конфигурации с параметрами для датасета.
  - **yolo.ipynb**: Jupyter-ноутбук, в котором реализованы алгоритмы YOLO.
