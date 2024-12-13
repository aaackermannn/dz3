import argparse
import argparse
import re
import sys
import toml


class ConfigProcessor:
    def __init__(self):
        self.constants = {}

    def parse_value(self, value):
        # Определяем тип значения
        if re.match(r'^-?\d+(\.\d+)?$', value):
            return float(value) if '.' in value else int(value)

        # Строки
        elif re.match(r'^".*"$', value):
            return value.strip('"')

        # Массивы
        elif value.startswith('(') and value.endswith(')'):
            # Разделяем элементы по запятой или пробелу, игнорируя пустые строки
            items = re.split(r'[\s,]+', value[1:-1].strip())
            return [self.parse_value(item) for item in items]

        # Словари
        elif value.startswith('{') and value.endswith('}'):
            # Убираем фигурные скобки и разделяем по запятой
            items = value[1:-1].strip().split(',')
            result = {}
            for item in items:
                # Разделяем на ключ и значение по первому двоеточию
                if ':' not in item:
                    raise ValueError(f"Invalid dictionary entry: {item}")
                key, val = item.split(':', 1)
                result[key.strip()] = self.parse_value(val.strip())
            return result

        # Константы
        elif value.startswith('![') and value.endswith(']'):
            constant_name = value[2:-1]
            if constant_name not in self.constants:
                raise ValueError(f"Undefined constant: {constant_name}")
            return self.constants[constant_name]

        # Строки, которые не являются массивами или словарями
        else:
            return value




    def process_line(self, line):
        if '->' in line:  # Объявление константы
            name, value = line.split('->')
            name = name.strip().strip(';')
            value = value.strip(";")
            self.constants[name] = self.parse_value(value)
        else:
            raise ValueError(f"Invalid syntax: {line}")

    def parse(self, lines):
        result = {}
        # Сначала собираем все константы
        for line in lines:
            line = line.strip()
            if not line or line.startswith('#'):  # Пропускаем пустые строки и комментарии
                continue
            if '->' in line:  # Обработка объявлений констант
                self.process_line(line)

        # Теперь, когда константы собраны, можно обрабатывать остальные строки
        for line in lines:
            line = line.strip()
            if not line or line.startswith('#'):  # Пропускаем пустые строки и комментарии
                continue
            if '->' not in line:  # Все строки после определения констант
                if ':' in line:  # Обработка словарей или структур
                    key, value = line.split(':', 1)
                    result[key.strip()] = self.parse_value(value.strip())
                else:
                    raise ValueError(f"Invalid line format: {line}")
        return result


def main():
    parser = argparse.ArgumentParser(description="Transform config to TOML.")
    parser.add_argument('config_file', help="Path to the input config file.")
    args = parser.parse_args()

    try:
        with open(args.config_file, 'r', encoding='utf-8') as file:
            lines = file.readlines()

        processor = ConfigProcessor()
        data = processor.parse(lines)

        # Выводим результат в формате TOML
        toml_output = toml.dumps(data)
        print(toml_output)

    except FileNotFoundError:
        print(f"Error: File '{args.config_file}' not found.")
        sys.exit(1)
    except ValueError as e:
        print(f"Syntax error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()






