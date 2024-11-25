import sys
import re
import json
import logging

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ConfigParser:
    def __init__(self, filepath):
        self.filepath = filepath
        self.data = []
        self.constants = {}  # Хранилище констант

    def parse(self):
        with open(self.filepath, 'r', encoding="utf-8") as file:
            content = file.read()

        # Убираем многострочные комментарии
        content = re.sub(r'/#.*?#/', '', content, flags=re.DOTALL)

        # Приводим все многострочные конструкции к однострочным
        lines = self.join_multiline_constructions(content.splitlines())

        for line in lines:
            line = line.strip()
            if not line:
                continue  # Пропуск пустых строк

            self.process_line(line)

    def join_multiline_constructions(self, lines):
        """Объединяет многострочные конструкции в одну строку."""
        joined_lines = []
        buffer = ""
        open_brackets = 0

        for line in lines:
            stripped = line.strip()
            if not stripped:
                continue  # Пропуск пустых строк

            # Считаем открывающие и закрывающие скобки
            open_brackets += stripped.count('(') + stripped.count('{')
            open_brackets -= stripped.count(')') + stripped.count('}')

            if buffer:
                buffer += " " + stripped
            else:
                buffer = stripped

            # Если все скобки закрыты, добавляем в итоговый список
            if open_brackets == 0:
                joined_lines.append(buffer)
                buffer = ""

        # Если остался незакрытый буфер, это ошибка синтаксиса
        if buffer:
            logger.error(f"Ошибка синтаксиса: Незавершённая конструкция: {buffer}")
        return joined_lines

    def process_line(self, line):
        # Обработка одиночных конструкций
        if line.startswith('(define'):
            self.handle_define(line)
        elif line.startswith('@('):
            self.handle_calculation(line)
        elif line.startswith('({'):
            self.handle_array(line)
        else:
            logger.error(f"Ошибка синтаксиса: Неизвестная конструкция: {line}")

    def handle_define(self, line):
        match = re.match(r'\(define (\w+) (.+)\);', line)
        if match:
            name, value = match.groups()
            # Сохраняем константу
            self.constants[name] = int(value)
            self.data.append({'define': {'name': name, 'value': value}})
        else:
            logger.error(f"Ошибка синтаксиса: Некорректное определение константы: {line}")

    def handle_calculation(self, line):
        match = re.match(r'@\((.+)\)', line)
        if match:
            expression = match.group(1).strip()
            try:
                # Подставляем значения констант
                expression = self.substitute_constants(expression)
                result = self.evaluate_expression(expression)
                self.data.append({'calculate': {'expression': expression, 'result': result}})
            except Exception as e:
                logger.error(f"Ошибка вычисления: {expression} ({e})")
        else:
            logger.error(f"Ошибка синтаксиса: Некорректное вычисление: {line}")

    def substitute_constants(self, expression):
        tokens = expression.split()
        result_tokens = []
        for token in tokens:
            if token in self.constants:
                result_tokens.append(str(self.constants[token]))
            else:
                result_tokens.append(token)
        return " ".join(result_tokens)

    def evaluate_expression(self, expression):
        tokens = expression.split()
        stack = []
        for token in tokens:
            if self.is_number(token):  # Число (включая отрицательные)
                stack.append(int(token))
            elif token == '+':  # Операция сложения
                b, a = stack.pop(), stack.pop()
                stack.append(a + b)
            elif token == 'abs':  # Функция abs
                a = stack.pop()
                stack.append(abs(a))
            else:  # Неизвестный токен
                raise ValueError(f"Неизвестный токен: {token}")
        if len(stack) != 1:
            raise ValueError("Некорректное выражение")
        return stack[0]

    def is_number(self, token):
        try:
            int(token)  # Пытаемся преобразовать в целое число
            return True
        except ValueError:
            return False

    def handle_array(self, line):
        match = re.match(r'\(\{(.+)\}\)', line)
        if match:
            values = match.group(1).split(',')
            values = [v.strip() for v in values]
            # Если это массив с константами, заменяем их значениями
            resolved_values = [self.constants.get(v, v) for v in values]
            self.data.append({'array': resolved_values})
        else:
            logger.error(f"Ошибка синтаксиса: Некорректный массив: {line}")

    def save_to_json(self, output_filepath):
        with open(output_filepath, 'w') as outfile:
            json.dump(self.data, outfile, indent=4)

    def get_json(self):
        return json.dumps(self.data, indent=4)


def main():
    if len(sys.argv) < 2:
        sys.exit(1)

    filepath = sys.argv[1]
    parser = ConfigParser(filepath)
    parser.parse()

    print(parser.get_json())


if __name__ == "__main__":
    main()

