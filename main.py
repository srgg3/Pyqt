import sys
import sqlite3
from random import randint
from PIL import Image

from PyQt6 import uic
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (QApplication, QWidget, QMainWindow)
from PyQt6.QtWidgets import (QLabel, QLineEdit, QTableWidgetItem)


class Register(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('registration form.ui', self)

        self.setWindowTitle('Вход')

        self.regist.clicked.connect(self.run_regist)
        self.enter_in.clicked.connect(self.run_inter_in)
        self.flag = False

        self.con = sqlite3.connect('users.sqlite')
        self.cur = self.con.cursor()
        result = self.cur.execute(f"""SELECT login, password FROM user
                WHERE login == '{self.Login.text()} AND password == '{self.Password.text()}''""").fetchone()
        spisok = []
        if result != None:
            for elem in result:
                spisok.append(elem)

        if bool(spisok):
            self.flag = True

        if not bool(spisok):
            self.flag = False

    def run_regist(self):
        if self.flag:
            self.label.setText('Аккаунт уже создан')
        else:
            psw = self.Password.text()
            nums = '0123456789'

            sp = []
            for i in psw:
                if i in nums:
                    sp.append(True)
                else:
                    sp.append(False)

            sp2 = []
            for i in psw:
                if i.isupper():
                    sp2.append(True)
                else:
                    sp2.append(False)

            repeats = set()
            for i in psw:
                repeats.add(i)

            if len(psw) < 6:
                self.label.setText('Пароль должен содержать хотя бы 6 символов')
            elif self.cur.execute(f"""SELECT id FROM user
                WHERE login == '{self.Login.text()}'""").fetchone():
                self.label.setText('Аккаунт уже создан')
            elif not any(sp):
                self.label.setText('В пароле должна быть хотя бы одна цифра')
            elif not any(sp2):
                self.label.setText('В пароле должна быть хотя бы заглавная буква')
            elif len(psw) != len(repeats):
                self.label.setText('В пароле не должно быть повторяющихся символов')
            elif '123' in psw or '234' in psw or \
                    '345' in psw or '456' in psw or '567' in psw \
                    or '678' in psw or '789' in psw or 'qwe' in psw:
                self.label.setText('Пароль слабый, придумайте новый')
            elif self.Login.text() == '':
                self.label.setText('Введите логин')
            else:
                self.cur.execute(f"INSERT INTO user(id, login, password) VALUES ({randint(1, 1000000)}, '{self.Login.text()}', '{self.Password.text()}')")
                self.con.commit()
                self.label.setText('Аккаунт создан')
                self.flag = not self.flag

    def run_inter_in(self):
        result = self.cur.execute(f"""SELECT login, password FROM user
                        WHERE login == '{self.Login.text()}'""").fetchone()
        if result == None:
            self.label.setText('Аккаунт не создан')
        elif self.Password.text() == '':
            self.label.setText('Введите пароль')
        elif result[1] != self.Password.text():
            self.label.setText('Пароль неправильный')
        else:
            self.label.setText('Добро пожаловать!')
            self.name = self.Login.text()
            self.window = General(f'{self.Login.text()}', f'{self.Password.text()}')
            self.hide()
            self.window.show()


class General(QWidget):
    def __init__(self, *args):
        super().__init__()
        self.initUI(args)

    def initUI(self, args):
        self.setGeometry(300, 300, 300, 300)
        self.setWindowTitle('Главное меню')
        self.loginName = args[-2]
        self.pswName = args[-1]
        uic.loadUi('Main_windows.ui', self)
        self.name_login.setText(f'Имя: {self.loginName}              Пароль: {self.pswName}')
        self.name_login.setVisible(False)
        self.change_the_psw.setVisible(False)
        self.hide.setVisible(False)
        self.new_psw.setVisible(False)
        self.confirm.setVisible(False)
        self.pswError.setVisible(False)
        self.exit_go.setVisible(False)
        self.tableWidget.setVisible(False)
        self.name.clicked.connect(self.show_name)
        self.change_the_psw.clicked.connect(self.run_change_the_psw)
        self.hide.clicked.connect(self.run_hide)
        self.confirm.clicked.connect(self.run_new_psw)
        self.results.clicked.connect(self.run_result)
        self.new_option.clicked.connect(self.create_a_new_option)
        self.exit_go.clicked.connect(self.run_exit)
        self.open_option.clicked.connect(self.run_open_definite_option)
        self.Variant = ''
        for i in range(12):
            self.Variant += str(randint(1, 5))
        self.count = 0
        self.con = sqlite3.connect('users.sqlite')
        self.con.commit()


    def create_a_new_option(self):
        self.tableWidget.setVisible(False)
        self.exit_go.setVisible(False)
        self.window2 = Create_a_new_option(f'{self.loginName}', f'{self.Variant}')
        self.window2.show()

    def run_result(self):
        self.ifError.setVisible(False)
        self.text_open_option.setVisible(False)
        self.name_login.setVisible(False)
        self.change_the_psw.setVisible(False)
        self.hide.setVisible(False)
        self.new_psw.setVisible(False)
        self.confirm.setVisible(False)
        self.pswError.setVisible(False)
        self.exit_go.setVisible(False)
        self.tableWidget.setVisible(True)
        res = self.con.cursor().execute(f"SELECT * from result WHERE Имя = '{self.loginName}'").fetchall()
        self.tableWidget.setColumnCount(16)
        self.tableWidget.setRowCount(0)
        for i, row in enumerate(res):
            self.tableWidget.setRowCount(
                self.tableWidget.rowCount() + 1)
            for j, elem in enumerate(row):
                self.tableWidget.setItem(
                    i, j, QTableWidgetItem(str(elem)))

    def run_open_definite_option(self):
        self.text_open_option.setVisible(True)
        self.tableWidget.setVisible(False)
        self.exit_go.setVisible(False)
        if len(self.text_open_option.text()) == 12:
            itog = 0
            for i in self.text_open_option.text():
                if i == '1' or i == '2' or i == '3' or i == '4' or i == '5':
                    itog += 1
            if itog == 12:
                self.window2 = Create_a_new_option(f'{self.loginName}', self.text_open_option.text())
                self.window2.show()
            else:
                self.ifError.setText('Вариант не существует')
        else:
            self.ifError.setText('Вариант не существует')

    def run_change_the_psw(self):
        self.text_open_option.setVisible(True)
        self.tableWidget.setVisible(False)
        self.new_psw.setVisible(True)
        self.confirm.setVisible(True)
        self.exit_go.setVisible(True)
        self.new_name_psw = self.new_psw.text()
        self.pswName = self.new_name_psw

    def run_new_psw(self):
        self.text_open_option.setVisible(True)
        self.tableWidget.setVisible(False)
        self.pswError.setVisible(True)
        nums = '0123456789'
        psw = self.new_psw.text()
        sp = []
        for i in psw:
            if i in nums:
                sp.append(True)
            else:
                sp.append(False)

        sp2 = []
        for i in psw:
            if i.isupper():
                sp2.append(True)
            else:
                sp2.append(False)

        repeats = set()
        for i in psw:
            repeats.add(i)

        con = sqlite3.connect('users.sqlite')
        cur = con.cursor()
        if len(psw) < 6:
            self.pswError.setText('Пароль должен содержать хотя бы 6 символов')

        elif not any(sp):
            self.pswError.setText('В пароле должна быть хотя бы одна цифра')

        elif not any(sp2):
            self.pswError.setText('В пароле должна быть хотя бы заглавная буква')

        elif len(psw) != len(repeats):
            self.pswError.setText('В пароле не должно быть повторяющихся символов')

        elif '123' in psw or '234' in psw or \
                '345' in psw or '456' in psw or '567' in psw \
                or '678' in psw or '789' in psw or 'qwe' in psw:
            self.pswError.setText('Пароль слабый, придумайте новый')
        else:
            self.pswError.setText('')
            result = cur.execute(f"UPDATE user "
                                 f"SET password = '{self.new_psw.text()}' "
                                 f"WHERE login = '{self.loginName}'")
            self.name_login.setText(f'Имя: {self.loginName}              Пароль: {self.new_psw.text()}')
            con.commit()

    def run_exit(self):
        self.wind_exit = Register()
        self.close()
        self.wind_exit.show()

    def keyPressEvent(self, event):
        if event.modifiers() == (Qt.KeyboardModifier.AltModifier | Qt.KeyboardModifier.ShiftModifier):
            if event.key() == Qt.Key.Key_P:
                self.wind_exit = Register()
                self.close()
                self.wind_exit.show()

    def run_hide(self):
        self.text_open_option.setVisible(True)
        self.tableWidget.setVisible(False)
        self.name_login.setVisible(False)
        self.change_the_psw.setVisible(False)
        self.hide.setVisible(False)
        self.new_psw.setVisible(False)
        self.confirm.setVisible(False)
        self.exit_go.setVisible(False)

    def show_name(self):
        self.text_open_option.setVisible(True)
        self.exit_go.setVisible(True)
        self.tableWidget.setVisible(False)
        self.name_login.setVisible(True)
        self.change_the_psw.setVisible(True)
        self.hide.setVisible(True)


class Create_a_new_option(QWidget):
    def __init__(self, *args):
        super().__init__()
        self.initUI(args)

    def initUI(self, args):
        self.setWindowTitle('Новый вариант')

        self.loginName = args[-2]
        self.num_opt = args[-1]

        uic.loadUi('CANO.ui', self)
        self.lgName.setText(self.loginName)
        self.Option.setText(self.num_opt)

        self.pushButton.clicked.connect(self.run_number_one)
        self.pushButton_2.clicked.connect(self.run_number_two)
        self.pushButton_3.clicked.connect(self.run_number_three)
        self.pushButton_4.clicked.connect(self.run_number_four)
        self.pushButton_5.clicked.connect(self.run_number_five)
        self.pushButton_6.clicked.connect(self.run_number_six)
        self.pushButton_8.clicked.connect(self.run_number_seven)
        self.pushButton_7.clicked.connect(self.run_number_eight)
        self.pushButton_9.clicked.connect(self.run_number_nine)
        self.pushButton_10.clicked.connect(self.run_number_ten)
        self.pushButton_11.clicked.connect(self.run_number_eleven)
        self.pushButton_12.clicked.connect(self.run_number_tvelve)
        self.pushButton_13.clicked.connect(self.checked)

        self.num1 = QLabel(self)
        self.num1.move(20, 160)
        self.num1.setText(f'Задание 1')
        self.pixmap1 = QPixmap(f'tasks\\1\\{self.num_opt[0]}.png')
        self.image1 = QLabel(self)
        self.image1.move(20, 190)
        self.image1.setPixmap(self.pixmap1)
        im = Image.open(f'tasks\\1\\{self.num_opt[0]}.png')
        x, y = im.size
        self.lineEdit1 = QLineEdit(self)
        self.lineEdit1.move(20, 190 + y + 20)
        self.num1.setVisible(False)
        self.image1.setVisible(False)
        self.lineEdit1.setVisible(False)

        self.num2 = QLabel(self)
        self.num2.move(20, 160)
        self.num2.setText(f'Задание 2')
        self.pixmap2 = QPixmap(f'tasks\\2\\{self.num_opt[1]}.png')
        self.image2 = QLabel(self)
        self.image2.move(20, 190)
        self.image2.setPixmap(self.pixmap2)
        im = Image.open(f'tasks\\2\\{self.num_opt[1]}.png')
        x, y = im.size
        self.lineEdit2 = QLineEdit(self)
        self.lineEdit2.move(20, 190 + y + 20)
        self.num2.setVisible(False)
        self.image2.setVisible(False)
        self.lineEdit2.setVisible(False)

        self.num3 = QLabel(self)
        self.num3.move(20, 160)
        self.num3.setText(f'Задание 3')
        self.pixmap3 = QPixmap(f'tasks\\3\\{self.num_opt[2]}.png')
        self.image3 = QLabel(self)
        self.image3.move(20, 190)
        self.image3.setPixmap(self.pixmap3)
        im = Image.open(f'tasks\\3\\{self.num_opt[2]}.png')
        x, y = im.size
        self.lineEdit3 = QLineEdit(self)
        self.lineEdit3.move(20, 190 + y + 20)
        self.num3.setVisible(False)
        self.image3.setVisible(False)
        self.lineEdit3.setVisible(False)

        self.num4 = QLabel(self)
        self.num4.move(20, 160)
        self.num4.setText(f'Задание 4')
        self.pixmap4 = QPixmap(f'tasks\\4\\{self.num_opt[3]}.png')
        self.image4 = QLabel(self)
        self.image4.move(20, 190)
        self.image4.setPixmap(self.pixmap4)
        im = Image.open(f'tasks\\4\\{self.num_opt[3]}.png')
        x, y = im.size
        self.lineEdit4 = QLineEdit(self)
        self.lineEdit4.move(20, 190 + y + 20)
        self.num4.setVisible(False)
        self.image4.setVisible(False)
        self.lineEdit4.setVisible(False)

        self.num5 = QLabel(self)
        self.num5.move(20, 160)
        self.num5.setText(f'Задание 5')
        self.pixmap5 = QPixmap(f'tasks\\5\\{self.num_opt[4]}.png')
        self.image5 = QLabel(self)
        self.image5.move(20, 190)
        self.image5.setPixmap(self.pixmap5)
        im = Image.open(f'tasks\\5\\{self.num_opt[4]}.png')
        x, y = im.size
        self.lineEdit5 = QLineEdit(self)
        self.lineEdit5.move(20, 190 + y + 20)
        self.num5.setVisible(False)
        self.image5.setVisible(False)
        self.lineEdit5.setVisible(False)

        self.num6 = QLabel(self)
        self.num6.move(20, 160)
        self.num6.setText(f'Задание 6')
        self.pixmap6 = QPixmap(f'tasks\\6\\{self.num_opt[5]}.png')
        self.image6 = QLabel(self)
        self.image6.move(20, 190)
        self.image6.setPixmap(self.pixmap6)
        im = Image.open(f'tasks\\6\\{self.num_opt[5]}.png')
        x, y = im.size
        self.lineEdit6 = QLineEdit(self)
        self.lineEdit6.move(20, 190 + y + 20)
        self.num6.setVisible(False)
        self.image6.setVisible(False)
        self.lineEdit6.setVisible(False)

        self.num7 = QLabel(self)
        self.num7.move(20, 160)
        self.num7.setText(f'Задание 7')
        self.pixmap7 = QPixmap(f'tasks\\7\\{self.num_opt[6]}.png')
        self.image7 = QLabel(self)
        self.image7.move(20, 190)
        self.image7.setPixmap(self.pixmap7)
        im = Image.open(f'tasks\\7\\{self.num_opt[6]}.png')
        x, y = im.size
        self.lineEdit7 = QLineEdit(self)
        self.lineEdit7.move(20, 190 + y + 20)
        self.num7.setVisible(False)
        self.image7.setVisible(False)
        self.lineEdit7.setVisible(False)

        self.num8 = QLabel(self)
        self.num8.move(20, 160)
        self.num8.setText(f'Задание 8')
        self.pixmap8 = QPixmap(f'tasks\\8\\{self.num_opt[7]}.png')
        self.image8 = QLabel(self)
        self.image8.move(20, 190)
        self.image8.setPixmap(self.pixmap8)
        im = Image.open(f'tasks\\8\\{self.num_opt[7]}.png')
        x, y = im.size
        self.lineEdit8 = QLineEdit(self)
        self.lineEdit8.move(20, 190 + y + 20)
        self.num8.setVisible(False)
        self.image8.setVisible(False)
        self.lineEdit8.setVisible(False)

        self.num9 = QLabel(self)
        self.num9.move(20, 160)
        self.num9.setText(f'Задание 9')
        self.pixmap9 = QPixmap(f'tasks\\9\\{self.num_opt[8]}.png')
        self.image9 = QLabel(self)
        self.image9.move(20, 190)
        self.image9.setPixmap(self.pixmap9)
        im = Image.open(f'tasks\\9\\{self.num_opt[8]}.png')
        x, y = im.size
        self.lineEdit9 = QLineEdit(self)
        self.lineEdit9.move(20, 190 + y + 20)
        self.num9.setVisible(False)
        self.image9.setVisible(False)
        self.lineEdit9.setVisible(False)

        self.num10 = QLabel(self)
        self.num10.move(20, 160)
        self.num10.setText(f'Задание 10')
        self.pixmap10 = QPixmap(f'tasks\\10\\{self.num_opt[9]}.png')
        self.image10 = QLabel(self)
        self.image10.move(20, 190)
        self.image10.setPixmap(self.pixmap10)
        im = Image.open(f'tasks\\10\\{self.num_opt[9]}.png')
        x, y = im.size
        self.lineEdit10 = QLineEdit(self)
        self.lineEdit10.move(20, 190 + y + 20)
        self.num10.setVisible(False)
        self.image10.setVisible(False)
        self.lineEdit10.setVisible(False)

        self.num11 = QLabel(self)
        self.num11.move(20, 160)
        self.num11.setText(f'Задание 11')
        self.pixmap11 = QPixmap(f'tasks\\11\\{self.num_opt[10]}.png')
        self.image11 = QLabel(self)
        self.image11.move(20, 190)
        self.image11.setPixmap(self.pixmap11)
        im = Image.open(f'tasks\\11\\{self.num_opt[10]}.png')
        x, y = im.size
        self.lineEdit11 = QLineEdit(self)
        self.lineEdit11.move(20, 190 + y + 20)
        self.num11.setVisible(False)
        self.image11.setVisible(False)
        self.lineEdit11.setVisible(False)

        self.num12 = QLabel(self)
        self.num12.move(20, 160)
        self.num12.setText(f'Задание 12')
        self.pixmap12 = QPixmap(f'tasks\\12\\{self.num_opt[11]}.png')
        self.image12 = QLabel(self)
        self.image12.move(20, 190)
        self.image12.setPixmap(self.pixmap12)
        im = Image.open(f'tasks\\12\\{self.num_opt[11]}.png')
        x, y = im.size
        self.lineEdit12 = QLineEdit(self)
        self.lineEdit12.move(20, 190 + y + 20)
        self.num12.setVisible(False)
        self.image12.setVisible(False)
        self.lineEdit12.setVisible(False)

    def run_number_one(self):
        self.num1.setVisible(True)
        self.image1.setVisible(True)
        self.lineEdit1.setVisible(True)

        self.num2.setVisible(False)
        self.image2.setVisible(False)
        self.lineEdit2.setVisible(False)

        self.num3.setVisible(False)
        self.image3.setVisible(False)
        self.lineEdit3.setVisible(False)

        self.num4.setVisible(False)
        self.image4.setVisible(False)
        self.lineEdit4.setVisible(False)

        self.num5.setVisible(False)
        self.image5.setVisible(False)
        self.lineEdit5.setVisible(False)

        self.num6.setVisible(False)
        self.image6.setVisible(False)
        self.lineEdit6.setVisible(False)

        self.num7.setVisible(False)
        self.image7.setVisible(False)
        self.lineEdit7.setVisible(False)

        self.num8.setVisible(False)
        self.image8.setVisible(False)
        self.lineEdit8.setVisible(False)

        self.num9.setVisible(False)
        self.image9.setVisible(False)
        self.lineEdit9.setVisible(False)

        self.num10.setVisible(False)
        self.image10.setVisible(False)
        self.lineEdit10.setVisible(False)

        self.num11.setVisible(False)
        self.image11.setVisible(False)
        self.lineEdit11.setVisible(False)

        self.num12.setVisible(False)
        self.image12.setVisible(False)
        self.lineEdit12.setVisible(False)

    def run_number_two(self):
        self.num1.setVisible(False)
        self.image1.setVisible(False)
        self.lineEdit1.setVisible(False)

        self.num2.setVisible(True)
        self.image2.setVisible(True)
        self.lineEdit2.setVisible(True)

        self.num3.setVisible(False)
        self.image3.setVisible(False)
        self.lineEdit3.setVisible(False)

        self.num4.setVisible(False)
        self.image4.setVisible(False)
        self.lineEdit4.setVisible(False)

        self.num5.setVisible(False)
        self.image5.setVisible(False)
        self.lineEdit5.setVisible(False)

        self.num6.setVisible(False)
        self.image6.setVisible(False)
        self.lineEdit6.setVisible(False)

        self.num7.setVisible(False)
        self.image7.setVisible(False)
        self.lineEdit7.setVisible(False)

        self.num8.setVisible(False)
        self.image8.setVisible(False)
        self.lineEdit8.setVisible(False)

        self.num9.setVisible(False)
        self.image9.setVisible(False)
        self.lineEdit9.setVisible(False)

        self.num10.setVisible(False)
        self.image10.setVisible(False)
        self.lineEdit10.setVisible(False)

        self.num11.setVisible(False)
        self.image11.setVisible(False)
        self.lineEdit11.setVisible(False)

        self.num12.setVisible(False)
        self.image12.setVisible(False)
        self.lineEdit12.setVisible(False)

    def run_number_three(self):
        self.num1.setVisible(False)
        self.image1.setVisible(False)
        self.lineEdit1.setVisible(False)

        self.num2.setVisible(False)
        self.image2.setVisible(False)
        self.lineEdit2.setVisible(False)

        self.num3.setVisible(True)
        self.image3.setVisible(True)
        self.lineEdit3.setVisible(True)

        self.num4.setVisible(False)
        self.image4.setVisible(False)
        self.lineEdit4.setVisible(False)

        self.num5.setVisible(False)
        self.image5.setVisible(False)
        self.lineEdit5.setVisible(False)

        self.num6.setVisible(False)
        self.image6.setVisible(False)
        self.lineEdit6.setVisible(False)

        self.num7.setVisible(False)
        self.image7.setVisible(False)
        self.lineEdit7.setVisible(False)

        self.num8.setVisible(False)
        self.image8.setVisible(False)
        self.lineEdit8.setVisible(False)

        self.num9.setVisible(False)
        self.image9.setVisible(False)
        self.lineEdit9.setVisible(False)

        self.num10.setVisible(False)
        self.image10.setVisible(False)
        self.lineEdit10.setVisible(False)

        self.num11.setVisible(False)
        self.image11.setVisible(False)
        self.lineEdit11.setVisible(False)

        self.num12.setVisible(False)
        self.image12.setVisible(False)
        self.lineEdit12.setVisible(False)

    def run_number_four(self):
        self.num1.setVisible(False)
        self.image1.setVisible(False)
        self.lineEdit1.setVisible(False)

        self.num2.setVisible(False)
        self.image2.setVisible(False)
        self.lineEdit2.setVisible(False)

        self.num3.setVisible(False)
        self.image3.setVisible(False)
        self.lineEdit3.setVisible(False)

        self.num4.setVisible(True)
        self.image4.setVisible(True)
        self.lineEdit4.setVisible(True)

        self.num5.setVisible(False)
        self.image5.setVisible(False)
        self.lineEdit5.setVisible(False)

        self.num6.setVisible(False)
        self.image6.setVisible(False)
        self.lineEdit6.setVisible(False)

        self.num7.setVisible(False)
        self.image7.setVisible(False)
        self.lineEdit7.setVisible(False)

        self.num8.setVisible(False)
        self.image8.setVisible(False)
        self.lineEdit8.setVisible(False)

        self.num9.setVisible(False)
        self.image9.setVisible(False)
        self.lineEdit9.setVisible(False)

        self.num10.setVisible(False)
        self.image10.setVisible(False)
        self.lineEdit10.setVisible(False)

        self.num11.setVisible(False)
        self.image11.setVisible(False)
        self.lineEdit11.setVisible(False)

        self.num12.setVisible(False)
        self.image12.setVisible(False)
        self.lineEdit12.setVisible(False)

    def run_number_five(self):
        self.num1.setVisible(False)
        self.image1.setVisible(False)
        self.lineEdit1.setVisible(False)

        self.num2.setVisible(False)
        self.image2.setVisible(False)
        self.lineEdit2.setVisible(False)

        self.num3.setVisible(False)
        self.image3.setVisible(False)
        self.lineEdit3.setVisible(False)

        self.num4.setVisible(False)
        self.image4.setVisible(False)
        self.lineEdit4.setVisible(False)

        self.num5.setVisible(True)
        self.image5.setVisible(True)
        self.lineEdit5.setVisible(True)

        self.num6.setVisible(False)
        self.image6.setVisible(False)
        self.lineEdit6.setVisible(False)

        self.num7.setVisible(False)
        self.image7.setVisible(False)
        self.lineEdit7.setVisible(False)

        self.num8.setVisible(False)
        self.image8.setVisible(False)
        self.lineEdit8.setVisible(False)

        self.num9.setVisible(False)
        self.image9.setVisible(False)
        self.lineEdit9.setVisible(False)

        self.num10.setVisible(False)
        self.image10.setVisible(False)
        self.lineEdit10.setVisible(False)

        self.num11.setVisible(False)
        self.image11.setVisible(False)
        self.lineEdit11.setVisible(False)

        self.num12.setVisible(False)
        self.image12.setVisible(False)
        self.lineEdit12.setVisible(False)

    def run_number_six(self):
        self.num1.setVisible(False)
        self.image1.setVisible(False)
        self.lineEdit1.setVisible(False)

        self.num2.setVisible(False)
        self.image2.setVisible(False)
        self.lineEdit2.setVisible(False)

        self.num3.setVisible(False)
        self.image3.setVisible(False)
        self.lineEdit3.setVisible(False)

        self.num4.setVisible(False)
        self.image4.setVisible(False)
        self.lineEdit4.setVisible(False)

        self.num5.setVisible(False)
        self.image5.setVisible(False)
        self.lineEdit5.setVisible(False)

        self.num6.setVisible(True)
        self.image6.setVisible(True)
        self.lineEdit6.setVisible(True)

        self.num7.setVisible(False)
        self.image7.setVisible(False)
        self.lineEdit7.setVisible(False)

        self.num8.setVisible(False)
        self.image8.setVisible(False)
        self.lineEdit8.setVisible(False)

        self.num9.setVisible(False)
        self.image9.setVisible(False)
        self.lineEdit9.setVisible(False)

        self.num10.setVisible(False)
        self.image10.setVisible(False)
        self.lineEdit10.setVisible(False)

        self.num11.setVisible(False)
        self.image11.setVisible(False)
        self.lineEdit11.setVisible(False)

        self.num12.setVisible(False)
        self.image12.setVisible(False)
        self.lineEdit12.setVisible(False)

    def run_number_seven(self):
        self.num1.setVisible(False)
        self.image1.setVisible(False)
        self.lineEdit1.setVisible(False)

        self.num2.setVisible(False)
        self.image2.setVisible(False)
        self.lineEdit2.setVisible(False)

        self.num3.setVisible(False)
        self.image3.setVisible(False)
        self.lineEdit3.setVisible(False)

        self.num4.setVisible(False)
        self.image4.setVisible(False)
        self.lineEdit4.setVisible(False)

        self.num5.setVisible(False)
        self.image5.setVisible(False)
        self.lineEdit5.setVisible(False)

        self.num6.setVisible(False)
        self.image6.setVisible(False)
        self.lineEdit6.setVisible(False)

        self.num7.setVisible(True)
        self.image7.setVisible(True)
        self.lineEdit7.setVisible(True)

        self.num8.setVisible(False)
        self.image8.setVisible(False)
        self.lineEdit8.setVisible(False)

        self.num9.setVisible(False)
        self.image9.setVisible(False)
        self.lineEdit9.setVisible(False)

        self.num10.setVisible(False)
        self.image10.setVisible(False)
        self.lineEdit10.setVisible(False)

        self.num11.setVisible(False)
        self.image11.setVisible(False)
        self.lineEdit11.setVisible(False)

        self.num12.setVisible(False)
        self.image12.setVisible(False)
        self.lineEdit12.setVisible(False)

    def run_number_eight(self):
        self.num1.setVisible(False)
        self.image1.setVisible(False)
        self.lineEdit1.setVisible(False)

        self.num2.setVisible(False)
        self.image2.setVisible(False)
        self.lineEdit2.setVisible(False)

        self.num3.setVisible(False)
        self.image3.setVisible(False)
        self.lineEdit3.setVisible(False)

        self.num4.setVisible(False)
        self.image4.setVisible(False)
        self.lineEdit4.setVisible(False)

        self.num5.setVisible(False)
        self.image5.setVisible(False)
        self.lineEdit5.setVisible(False)

        self.num6.setVisible(False)
        self.image6.setVisible(False)
        self.lineEdit6.setVisible(False)

        self.num7.setVisible(False)
        self.image7.setVisible(False)
        self.lineEdit7.setVisible(False)

        self.num8.setVisible(True)
        self.image8.setVisible(True)
        self.lineEdit8.setVisible(True)

        self.num9.setVisible(False)
        self.image9.setVisible(False)
        self.lineEdit9.setVisible(False)

        self.num10.setVisible(False)
        self.image10.setVisible(False)
        self.lineEdit10.setVisible(False)

        self.num11.setVisible(False)
        self.image11.setVisible(False)
        self.lineEdit11.setVisible(False)

        self.num12.setVisible(False)
        self.image12.setVisible(False)
        self.lineEdit12.setVisible(False)

    def run_number_nine(self):
        self.num1.setVisible(False)
        self.image1.setVisible(False)
        self.lineEdit1.setVisible(False)

        self.num2.setVisible(False)
        self.image2.setVisible(False)
        self.lineEdit2.setVisible(False)

        self.num3.setVisible(False)
        self.image3.setVisible(False)
        self.lineEdit3.setVisible(False)

        self.num4.setVisible(False)
        self.image4.setVisible(False)
        self.lineEdit4.setVisible(False)

        self.num5.setVisible(False)
        self.image5.setVisible(False)
        self.lineEdit5.setVisible(False)

        self.num6.setVisible(False)
        self.image6.setVisible(False)
        self.lineEdit6.setVisible(False)

        self.num7.setVisible(False)
        self.image7.setVisible(False)
        self.lineEdit7.setVisible(False)

        self.num8.setVisible(False)
        self.image8.setVisible(False)
        self.lineEdit8.setVisible(False)

        self.num9.setVisible(True)
        self.image9.setVisible(True)
        self.lineEdit9.setVisible(True)

        self.num10.setVisible(False)
        self.image10.setVisible(False)
        self.lineEdit10.setVisible(False)

        self.num11.setVisible(False)
        self.image11.setVisible(False)
        self.lineEdit11.setVisible(False)

        self.num12.setVisible(False)
        self.image12.setVisible(False)
        self.lineEdit12.setVisible(False)

    def run_number_ten(self):
        self.num1.setVisible(False)
        self.image1.setVisible(False)
        self.lineEdit1.setVisible(False)

        self.num2.setVisible(False)
        self.image2.setVisible(False)
        self.lineEdit2.setVisible(False)

        self.num3.setVisible(False)
        self.image3.setVisible(False)
        self.lineEdit3.setVisible(False)

        self.num4.setVisible(False)
        self.image4.setVisible(False)
        self.lineEdit4.setVisible(False)

        self.num5.setVisible(False)
        self.image5.setVisible(False)
        self.lineEdit5.setVisible(False)

        self.num6.setVisible(False)
        self.image6.setVisible(False)
        self.lineEdit6.setVisible(False)

        self.num7.setVisible(False)
        self.image7.setVisible(False)
        self.lineEdit7.setVisible(False)

        self.num8.setVisible(False)
        self.image8.setVisible(False)
        self.lineEdit8.setVisible(False)

        self.num9.setVisible(False)
        self.image9.setVisible(False)
        self.lineEdit9.setVisible(False)

        self.num10.setVisible(True)
        self.image10.setVisible(True)
        self.lineEdit10.setVisible(True)

        self.num11.setVisible(False)
        self.image11.setVisible(False)
        self.lineEdit11.setVisible(False)

        self.num12.setVisible(False)
        self.image12.setVisible(False)
        self.lineEdit12.setVisible(False)

    def run_number_eleven(self):
        self.num1.setVisible(False)
        self.image1.setVisible(False)
        self.lineEdit1.setVisible(False)

        self.num2.setVisible(False)
        self.image2.setVisible(False)
        self.lineEdit2.setVisible(False)

        self.num3.setVisible(False)
        self.image3.setVisible(False)
        self.lineEdit3.setVisible(False)

        self.num4.setVisible(False)
        self.image4.setVisible(False)
        self.lineEdit4.setVisible(False)

        self.num5.setVisible(False)
        self.image5.setVisible(False)
        self.lineEdit5.setVisible(False)

        self.num6.setVisible(False)
        self.image6.setVisible(False)
        self.lineEdit6.setVisible(False)

        self.num7.setVisible(False)
        self.image7.setVisible(False)
        self.lineEdit7.setVisible(False)

        self.num8.setVisible(False)
        self.image8.setVisible(False)
        self.lineEdit8.setVisible(False)

        self.num9.setVisible(False)
        self.image9.setVisible(False)
        self.lineEdit9.setVisible(False)

        self.num10.setVisible(False)
        self.image10.setVisible(False)
        self.lineEdit10.setVisible(False)

        self.num11.setVisible(True)
        self.image11.setVisible(True)
        self.lineEdit11.setVisible(True)

        self.num12.setVisible(False)
        self.image12.setVisible(False)
        self.lineEdit12.setVisible(False)

    def run_number_tvelve(self):
        self.num1.setVisible(False)
        self.image1.setVisible(False)
        self.lineEdit1.setVisible(False)

        self.num2.setVisible(False)
        self.image2.setVisible(False)
        self.lineEdit2.setVisible(False)

        self.num3.setVisible(False)
        self.image3.setVisible(False)
        self.lineEdit3.setVisible(False)

        self.num4.setVisible(False)
        self.image4.setVisible(False)
        self.lineEdit4.setVisible(False)

        self.num5.setVisible(False)
        self.image5.setVisible(False)
        self.lineEdit5.setVisible(False)

        self.num6.setVisible(False)
        self.image6.setVisible(False)
        self.lineEdit6.setVisible(False)

        self.num7.setVisible(False)
        self.image7.setVisible(False)
        self.lineEdit7.setVisible(False)

        self.num8.setVisible(False)
        self.image8.setVisible(False)
        self.lineEdit8.setVisible(False)

        self.num9.setVisible(False)
        self.image9.setVisible(False)
        self.lineEdit9.setVisible(False)

        self.num10.setVisible(False)
        self.image10.setVisible(False)
        self.lineEdit10.setVisible(False)

        self.num11.setVisible(False)
        self.image11.setVisible(False)
        self.lineEdit11.setVisible(False)

        self.num12.setVisible(True)
        self.image12.setVisible(True)
        self.lineEdit12.setVisible(True)

    def checked(self):
        self.con = sqlite3.connect('users.sqlite')
        self.cur = self.con.cursor()

        sp = []
        result = self.cur.execute("""SELECT * FROM ответы""").fetchall()

        for item in result:
            sp.append(item)

        chek = []

        ans = [self.lineEdit1.text(), self.lineEdit2.text(), self.lineEdit3.text(), self.lineEdit4.text(),\
               self.lineEdit5.text(), self.lineEdit6.text(), self.lineEdit7.text(), self.lineEdit5.text(),\
               self.lineEdit9.text(), self.lineEdit10.text(), self.lineEdit11.text(), self.lineEdit12.text()]

        for i in range(12):
            if sp[int(self.num_opt[i]) - 1][i] == ans[i]:
                chek.append(1)
            else:
                chek.append(0)

        self.cur.execute(f"INSERT INTO result(Имя, Вариант, '№ 1', '№ 2', '№ 3', '№ 4', '№ 5', '№ 6', '№ 7', '№ 8', '№ 9', '№ 10', '№ 11', '№ 12', итого, 'количество правильного в %') VALUES ('{self.loginName}', '{self.num_opt}', {chek[0]}, {chek[1]}, {chek[2]}, {chek[3]}, {chek[4]}, {chek[5]}, {chek[6]}, {chek[7]}, {chek[8]}, {chek[9]}, {chek[10]}, {chek[11]}, {sum(chek)}, {sum(chek) * 100 // 12})")
        self.con.commit()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Register()
    ex.show()
    sys.exit(app.exec())

