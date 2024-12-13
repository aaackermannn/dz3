# Преобразователь конфигурационных файлов в формат TOML

## 1. Общее описание

Этот скрипт предназначен для обработки конфигурационных файлов, представленных в особом формате, и преобразования их в формат TOML. Скрипт поддерживает константы, массивы, словари и стандартные значения. Конфигурации могут включать объявления констант, которые затем используются в других частях файла.

Скрипт предназначен для упрощения работы с конфигурационными данными, позволяя использовать такие возможности, как повторное использование значений и создание сложных структур.

## 2. Описание всех функций и настроек

### Классы и методы

#### `ConfigProcessor`

Класс для обработки конфигурационного файла и преобразования его в структуру данных, которую можно экспортировать в формат TOML.

- **`__init__(self)`**: Инициализация пустого словаря для хранения констант.
  
- **`parse_value(self, value)`**: Метод для анализа и преобразования значения. Он поддерживает следующие типы:
  - Числа (целые и с плавающей точкой).
  - Строки, заключенные в кавычки.
  - Массивы, заключенные в скобки `()`, элементы которых разделяются запятыми или пробелами.
  - Словари, заключенные в фигурные скобки `{}`, с разделением ключ-значение через двоеточие.
  - Константы, которые начинаются с `![<constant>]` и ссылаются на ранее определенные значения.

- **`process_line(self, line)`**: Обрабатывает строку конфигурации. Определяет, является ли строка объявлением константы или нет.

- **`parse(self, lines)`**: Основной метод, который анализирует весь конфигурационный файл, собирает константы и потом обрабатывает остальные строки.

#### Параметры командной строки

- `config_file`: Путь к входному конфигурационному файлу. Это обязательный параметр.

## 3. Описание команд для сборки проекта

### Установка зависимостей

Для работы с файлом в формате TOML используется библиотека `toml`. Чтобы установить все необходимые зависимости, выполните команду:

```bash
pip install toml
