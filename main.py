import sys
import os
from PyQt6 import uic, QtGui, QtCore
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QButtonGroup,
    QDialog,
)
from random import randint, uniform

list_of_symbols_16 = [
    "A",
    "B",
    "C",
    "D",
    "E",
    "F",
    "1",
    "2",
    "3",
    "4",
    "5",
    "6",
    "7",
    "8",
    "9",
    "0",
    ".",
    ",",
]
list_of_symbols = [
    "1",
    "2",
    "3",
    "4",
    "5",
    "6",
    "7",
    "8",
    "9",
    "0",
    ".",
    ",",
]


class Num_Translate(QMainWindow):
    def __init__(self):
        super().__init__()

        uic.loadUi(
            os.path.abspath("design/NumTranslator.ui"), self
        )  # ПОДГРУЗКА ИНТЕРФЕЙСА

        self.create_test_button.clicked.connect(self.create_test)  # СОЗДАТЬ ТЕСТ
        # Из какой сс
        self.from_ss = QButtonGroup(self)
        self.from_ss.addButton(self.ss16)
        self.from_ss.addButton(self.ss10)
        self.from_ss.addButton(self.ss8)
        self.from_ss.addButton(self.ss4)
        self.from_ss.addButton(self.ss2)
        self.from_ss.buttonClicked.connect(self.fromss)

        # В какую сс
        self.in_ss = QButtonGroup(self)
        self.in_ss.addButton(self.iss16)
        self.in_ss.addButton(self.iss10)
        self.in_ss.addButton(self.iss8)
        self.in_ss.addButton(self.iss4)
        self.in_ss.addButton(self.iss2)
        self.in_ss.buttonClicked.connect(self.inss)

        # Изначальное положение кнопок
        self.in_system = 2
        self.from_system = 2

        dict_with_error_codes = {
            0: ["Same system", "Выберите различные\nсистемы счисления"],
            1: [
                "Unknown symbol",
                f"Используйте только:\n'{''.join(list_of_symbols_16 if self.in_system == 16 else list_of_symbols)}'",
            ],
            2: ["No answer", "Сначала введите\nответ"],
            3: [
                "A large number of examples",
                "Введите меньшее\nколичество тестов\n(<=15)",
            ],
            4: ["Not a digit", "Используйте положительное\nцелое число"],
        }

    # Изменение сс при нажатии
    def inss(self, button):
        self.in_system = int(button.text())

    def fromss(self, button):
        self.from_system = int(button.text())

    # СОЗДАНИЕ ТЕСТА
    def create_test(self):

        self.test = []
        self.correct_answers = []
        self.user_answers = []
        self.test_number = 1
        self.incorrect_answers = 0

        if self.in_system == self.from_system:
            self.show_error()
            return

        if self.count_number.text().isdigit() and int(self.count_number.text()) > 15:
            self.show_error()
            return

        if self.count_number.text().isdigit() and int(self.count_number.text()) <= 15:

            self.count = int(self.count_number.text())
            # Целые числа
            if not self.fractional_num.isChecked():
                for i in range(self.count):
                    num = randint(0, 999)
                    # Создание числа для примера
                    self.test.append(self.decimal_to_base(num, self.from_system))

                    # Правильный ответ
                    self.correct_answers.append(
                        self.decimal_to_base(num, self.in_system)
                    )
            # Вещественные числа
            else:

                for i in range(self.count):
                    num = round(uniform(0, 999), randint(1, 4))
                    # Создание числа для примера
                    self.test.append(self.decimal_to_base(num, self.from_system))

                    # Правильный ответ
                    self.correct_answers.append(
                        self.decimal_to_base(num, self.in_system)
                    )
        elif not self.count_number.text().isdigit():
            self.show_error()

        # НАЧАЛО ТЕСТА
        if self.count_number.text().isdigit():
            self.show_test()
            self.check_answ()

    # ПЕРЕВОД ЧИСЕЛ
    def decimal_to_base(self, num, base):
        if num == 0:
            return "0"

        # Разделяем целую и дробную части
        integer_part = int(num)
        fractional_part = num - integer_part

        # Переводим целую часть
        digits = "0123456789ABCDEF"
        integer_result = ""

        # Обработка целой части
        while integer_part > 0:
            integer_result = digits[integer_part % base] + integer_result
            integer_part //= base

        # Переводим дробную часть
        fractional_result = ""
        while fractional_part > 0 and len(fractional_result) < 3:
            fractional_part *= base
            digit = int(fractional_part)
            fractional_result += digits[digit]
            fractional_part -= digit

        # Результат
        if fractional_result:
            return integer_result + "." + fractional_result
        else:
            return integer_result

    # ПРОВЕРКА ОТВЕТА НА СИМВОЛЫ
    def check_symbol(self, text):
        self.count_of_incorrect_sym = 0
        if self.in_system == 16:
            for symbol in list(text):
                if symbol not in list_of_symbols_16:
                    self.count_of_incorrect_sym += 1
        else:
            for symbol in list(text):
                if symbol not in list_of_symbols:
                    self.count_of_incorrect_sym += 1

    # Вызов диалога с ошибкой + определение типа ошибки
    def show_error(self, extra_code=0):
        # Одинаковая сс
        if self.in_system == self.from_system:
            error_code = 0
        # Кол-во примеров не число
        if not self.count_number.text().isdigit():
            error_code = 1
        # Ответ не число
        if extra_code == 1:
            error_code = 1
        # Пустой ответ
        if extra_code == 2:
            error_code = 2
        # Большое кол-во тестов
        if self.count_number.text().isdigit() and int(self.count_number.text()) > 15:
            error_code = 3
        if not self.count_number.text().isdigit():
            error_code = 4

        rd = Error(error_code, self.in_system)
        rd.show()
        rd.exec()

    # Вызов диалога с оценкой
    def show_mark(self):
        md = Mark_dialog(self.mark)
        md.show()
        md.exec()

    # Прохождение теста
    def show_test(self):
        for n in range(int(self.count_number.text())):
            if self.fractional_num.isChecked():
                td = Test_dialog(
                    n, self.test[n], self.from_system, self.in_system, fract=True
                )
            else:
                td = Test_dialog(n, self.test[n], self.from_system, self.in_system)
            td.show()
            td.exec()
            # Цикл для повторного введения ответа, если до этого ничего не ввели
            text = ""
            while text == "" or self.count_of_incorrect_sym != 0:
                text = answer
                self.check_symbol(text)
                if text != "":
                    if self.in_system == 16:
                        for symbol in list(text):
                            if symbol not in list_of_symbols_16:
                                self.show_error(extra_code=1)
                                td = Test_dialog(
                                    n, self.test[n], self.from_system, self.in_system
                                )
                                td.show()
                                td.exec()
                                break
                    else:
                        for symbol in list(text):
                            if symbol not in list_of_symbols:
                                self.show_error(extra_code=1)
                                td = Test_dialog(
                                    n, self.test[n], self.from_system, self.in_system
                                )
                                td.show()
                                td.exec()
                                break
                    # Вывести ошибку
                elif text == "":
                    self.show_error(extra_code=2)
                    td = Test_dialog(n, self.test[n], self.from_system, self.in_system)
                    td.show()
                    td.exec()
            self.user_answers.append(
                text.replace(",", ".")
            )  # Сохранение ответа + приведение к общему виду

    def check_answ(self):
        if len(self.user_answers) > 0:
            for i in range(len(self.correct_answers)):
                if self.correct_answers[i] != self.user_answers[i]:
                    self.incorrect_answers += 1
            self.proportion_of_correct_answers = (
                len(self.user_answers) - self.incorrect_answers
            ) / len(self.user_answers)
            if self.proportion_of_correct_answers >= 0.85:
                self.mark = 5
            elif self.proportion_of_correct_answers >= 0.70:
                self.mark = 4
            elif self.proportion_of_correct_answers >= 0.50:
                self.mark = 3
            elif self.proportion_of_correct_answers < 0.50:
                self.mark = 2
            self.show_mark()


# Диалог с тестом
class Test_dialog(QDialog):
    def __init__(self, n, num, fss, iss, fract=False):
        super().__init__()
        uic.loadUi(os.path.abspath("design/test_dialog.ui"), self)
        self.setWindowTitle(f"Пример №{n + 1}")
        if fract:
            self.num_text.setText(
                f"Переведите {num} из {fss} в {iss} сс\n(3 знака после запятой)"
            )
        else:
            self.num_text.setText(f"Переведите {num} из {fss} в {iss} сс")
        self.next_ex.clicked.connect(self.next_example)  # ПЕРЕЙТИ К СЛЕД ЧИСЛУ
        # Фикс пропуска примера и вывода ошибки путем закрытия окна с ответом
        global answer
        answer = ""

    def next_example(self):
        global answer
        answer = self.answer.text().upper()
        self.close()
        return


# Дилог с выводом оценки
class Mark_dialog(QDialog):
    def __init__(self, mark):
        super().__init__()
        uic.loadUi(os.path.abspath("design/mark_dialog.ui"), self)
        self.mark_text.setText(f"Ваша оценка:{mark}")
        self.again.clicked.connect(self.exit_to_menu)  # КНОПКА ЗАНОВО -> ВЫЙТИ В НАЧАЛО

    def exit_to_menu(self):
        self.close()


# Диалог с ошибкой об одинакого выбранных сс
class Error(QDialog):
    def __init__(self, error_code, in_system=2):
        super().__init__()
        uic.loadUi(os.path.abspath("design/ss_error_dialog.ui"), self)

        dict_with_error_codes = {
            0: ["Same system", "Выберите различные\nсистемы счисления"],
            1: [
                "Unknown symbol",
                f"Используйте только:\n'{''.join(list_of_symbols_16 if in_system == 16 else list_of_symbols)}'",
            ],
            2: ["No answer", "Сначала введите\nответ"],
            3: [
                "A large number of examples",
                "Введите меньшее\nколичество тестов\n(<=15)",
            ],
            4: ["Not a digit", "Используйте положительное\nцелое число"],
        }

        self.ok.clicked.connect(self.try_again)
        self.error_text.setText(dict_with_error_codes[error_code][1])

    def try_again(self):
        self.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)

    nt = Num_Translate()
    nt.show()
    sys.exit(app.exec())
