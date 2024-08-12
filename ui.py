from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QApplication,
    QWidget, 
    QVBoxLayout,
    QHeaderView,
    QPushButton,
    QLineEdit,
    QLabel,
    QListWidget,
    QHBoxLayout,
    QMessageBox,
    QTableWidget,
    QAbstractItemView,
    QTableWidgetItem,
    QMessageBox
)
from core import Database,DATA

class Button(QPushButton):
    def __init__(self, text):
        super().__init__(text)
        self.setFixedSize(575, 50)
        self.setStyleSheet(f"""
            QPushButton {{
                background-color: #3B4BFF;
                font-size: 25px;
                padding: 8px;
                font-weight: bold;
                border-radius: 16px;
                border: none;
                color: white;
            }}
            QPushButton:hover {{
                background-color: white;
                font-size: 25px;
                border: 2px solid #3B4BFF;
                color: #3B4BFF;
            }}
        """)


class Sing_up(QWidget):
    def __init__(self):
        super().__init__()
        self.core = Database()
        self.setStyleSheet("font-size: 30px")
        self.v_box = QVBoxLayout()

        self.info_display = QLabel()
        self.display = QLabel("if you have account")

        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Enter email")

        self.pwd_input = QLineEdit()
        self.pwd_input.setPlaceholderText("Password")

        self.sing_in_btn = Button('Sing in')
        self.sing_up_btn = Button("Sing up")

        self.sing_in_btn.clicked.connect(self.open_menu)
        self.sing_up_btn.clicked.connect(self.Sing_in_page)

        self.v_box.addWidget(self.email_input)
        self.v_box.addWidget(self.pwd_input)
        self.v_box.addWidget(self.info_display)
        self.v_box.addWidget(self.sing_in_btn)
        self.v_box.addWidget(self.display)
        self.v_box.addWidget(self.sing_up_btn)

        self.setLayout(self.v_box)
        self.show()
    
    def Sing_in_page(self):
        self.close()
        self.page = Sing_in()
    
    def open_menu(self):
        login = self.email_input.text()
        pwd = self.pwd_input.text()

        if not login:
            self.email_input.setPlaceholderText("Is empty")
        if not pwd:
            self.pwd_input.setPlaceholderText("Is empty")
        st = ""
        for i in pwd:
            st += chr(ord(i)+2)

        if login and pwd:
            user = {
                'email': login,
                'password' : st
            }
            # print(st)
            _id = self.core.is_user(user)
            # print(_id)
            if _id:
                admin = self.core.is_admin(_id)
                # print(admin)
                if admin:
                    self.close()
                    self.admin = AdminPage(_id)
                    self.admin.show()
                else:
                    self.close()
                    self.user = User(_id)
                    self.user.show()
            else:
                self.info_display.setText('login or password error ❌')

class AdminPage(QWidget):
    def __init__(self,id):
        super().__init__()
        self.id = id

        self.v_box = QVBoxLayout()

        self.list_btn = Button('LICT 🪪')
        self.back_btn = Button('Back ❌')
        self.list_btn.clicked.connect(self.List_page)
        self.back_btn.clicked.connect(self.back_page)

        self.v_box.addWidget(self.list_btn)
        self.v_box.addWidget(self.back_btn)

        self.setLayout(self.v_box)

    def List_page(self):
        self.close()
        self.lst = AdminSearch()
        self.lst.show()

    def back_page(self):
        self.close()
        self.page = Sing_up()

class AdminSearch(QWidget):
    def __init__(self):
        super().__init__()
        self.core = DATA()

        self.initUI()

    def initUI(self):
        vbox = QVBoxLayout()
        hbox = QHBoxLayout()

        self.search_bar = QLineEdit(self)
        hbox.addWidget(self.search_bar)

        self.search_btn = QPushButton('Search 🔍', self)
        self.search_btn.clicked.connect(self.search_data)
        hbox.addWidget(self.search_btn)

        vbox.addLayout(hbox)

        self.table = QTableWidget(self)
        self.table.setColumnCount(8)  
        self.table.setHorizontalHeaderLabels(['ID', 'Username', 'Email', 'Password', 'Card Number', 'Card Password', 'Amount', 'Actions'])
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)

        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)

        self.table.setMinimumWidth(800)
        self.table.setMinimumHeight(100)

        vbox.addWidget(self.table)

        self.setLayout(vbox)
        self.setWindowTitle('PyQt5 Database App')
        self.show()

    def search_data(self):
        query = self.search_bar.text()
        data = {
            'query': query
        }
        results = self.core.search_data(data)
        # print(results)
        self.table.setRowCount(len(results))
        for i, row in enumerate(results):
            for j, value in enumerate(row):
                self.table.setItem(i, j, QTableWidgetItem(str(value)))

            self.v_box = QVBoxLayout()
            action_layout = QHBoxLayout()

            self.back_btn = Button('🔙')
            self.back_btn.clicked.connect(self.back_page)

            update_btn = QPushButton('🖊️')
            update_btn.clicked.connect(lambda _, row=i, id_=row[0]: self.update_data(row, id_))
            action_layout.addWidget(update_btn)

            delete_btn = QPushButton('🗑️')
            delete_btn.clicked.connect(lambda _, id_=row[0]: self.delete_data(id_))
            action_layout.addWidget(delete_btn)

            action_widget = QWidget()
            action_widget.setLayout(action_layout)
            self.v_box.addLayout()

            self.table.setCellWidget(i, 7, action_widget)

    def update_data(self, row, id_):
        new_values = [self.table.item(row, col).text() for col in range(1, 7)]
        self.core.update_data(id_, new_values)
        self.search_data()

    def delete_data(self, id_):
        reply = QMessageBox.question(self, 'Message',
                                     "Are you shure you want to delete this user?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.core.delete_data(id_)
            self.search_data()
        else:
            pass

class User(QWidget):
    def __init__(self,id):
        super().__init__()
        self.id = id

        self.v_box = QVBoxLayout()

        self.back_btn = Button('Back')
        self.back_btn.clicked.connect(self.back_page)

        self.v_box.addWidget(self.back_btn)
        self.setLayout(self.v_box)

    def back_page(self):
        self.close()
        self.page = Sing_up()

class Sing_in(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.core = Database()
        self.setStyleSheet("font-size: 30px")
        self.v_box = QVBoxLayout()

        self.info_display = QLabel()
        self.display = QLabel("Alredy have an account")

        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Username")

        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Email")

        self.pwd_input = QLineEdit()
        self.pwd_input.setPlaceholderText("Password")


        self.card_num_input = QLineEdit()
        self.card_num_input.setPlaceholderText("Card number")

        self.card_pwd_input = QLineEdit()
        self.card_pwd_input.setPlaceholderText("Card Password")

        self.sing_up_btn = Button("Sing up")
        self.sing_in_btn = Button('Sing in')

        self.sing_up_btn.clicked.connect(self.Register)
        self.sing_in_btn.clicked.connect(self.change_sing_up)

        self.v_box.addWidget(self.name_input)
        self.v_box.addWidget(self.email_input)
        self.v_box.addWidget(self.pwd_input)
        self.v_box.addWidget(self.card_num_input)
        self.v_box.addWidget(self.card_pwd_input)
        self.v_box.addWidget(self.info_display)
        self.v_box.addWidget(self.sing_up_btn)
        self.v_box.addWidget(self.display)
        self.v_box.addWidget(self.sing_in_btn)

        self.setLayout(self.v_box)
        self.show()

    def change_sing_up(self):
        self.close()
        self.page = Sing_up()

    def Register(self):
        name = self.name_input.text()
        email = self.email_input.text()
        pwd = self.pwd_input.text()
        card_num = self.card_num_input.text()
        card_pwd = self.card_pwd_input.text()
        pwd2=""
        card_num2=""
        card_pwd2=""
        email = self.email_input.text()
        if name and email and pwd and card_num and card_pwd:
            for i in pwd:
                pwd2 += chr(ord(i)+2)

            for i in card_num:
                card_num2 += chr(ord(i)+2)

            for i in card_pwd:
                card_pwd2 += chr(ord(i)+2)

            user = {
                'username' : name,
                'email' : email,
                'password': pwd2,
                'card_num' : card_num2,
                'card_pwd' : card_pwd2
            }

            err = self.core.insert_user(user)
            if err:
                self.info_display.setText("login exists 🖊️")
            else:
                self.info_display.setText("you have registered successfully ✅")
                self.name_input.clear()
                self.email_input.clear()
                self.pwd_input.clear()
                self.card_num_input.clear()
                self.card_pwd_input.clear()
        else:
            self.info_display.setText("Fill it all out ⚠️")

if __name__ == "__main__":
    app = QApplication([])
    win = Sing_up()
    app.exec_()