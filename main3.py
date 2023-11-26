import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QTableWidget, QWidget, QLineEdit, \
    QPushButton, QMessageBox, QComboBox
from PyQt5.QtGui import QPixmap, QFont
import sqlite3


class LibraryCatalog(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Каталог библиотеки')
        self.setGeometry(300, 100, 500, 599)

        self.init_ui()

    def init_ui(self):
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.table = QTableWidget(self)
        self.table.setColumnCount(1)

        self.table.setHorizontalHeaderLabels([''])
        self.table.move(10, 10)
        self.table.resize(450, 500)

        self.author_search = QLineEdit(self)
        self.author_search.setGeometry(58, 559, 200, 20)

        self.search_button = QPushButton(self)
        self.search_button.setText("Искать")
        self.search_button.setGeometry(290, 520, 50, 50)
        self.search_button.clicked.connect(self.search_book)

        self.book_info = QLabel(self)

        self.init_database()
        self.search_type = QComboBox(self)
        self.search_type.setGeometry(58, 520, 90, 20)
        self.search_type.addItems(['по автору', 'по названию'])

    def init_database(self):
        self.connection = sqlite3.connect('library.db')
        self.cursor = self.connection.cursor()
        self.cursor.execute(
            'CREATE TABLE IF NOT EXISTS books (id INTEGER PRIMARY KEY, title TEXT, author TEXT, year INTEGER, genre TEXT, image_path TEXT)')

    def search_book(self):
        search_text = self.author_search.text()
        search_type = self.search_type.currentText()

        if search_type == 'по автору':
            self.cursor.execute('SELECT * FROM books WHERE author LIKE ?', (f'%{search_text}%',))
        elif search_type == 'по названию':
            self.cursor.execute('SELECT * FROM books WHERE title LIKE ?', (f'%{search_text}%',))
        else:
            QMessageBox.warning(self, 'Ошибка', 'Выберите тип поиска')
            return

        books = self.cursor.fetchall()

        self.table.setRowCount(0)
        for book in books:
            row_position = self.table.rowCount()
            self.table.insertRow(row_position)
            title_button = QPushButton(book[1])
            title_button.clicked.connect(lambda _, book=book: self.show_book_info(book))
            self.table.setCellWidget(row_position, 0, title_button)

        self.table.setColumnWidth(0, 420)
        self.connection.commit()

    def show_book_info(self, book):
        global book_
        book_ = book
        self.informationWindow = InfWindow()
        self.informationWindow.show()

    def closeEvent(self, event):
        self.connection.close()
        event.accept()


class InfWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Каталог библиотеки')
        self.setGeometry(500, 500, 350, 350)

        self.init_ui()

    def init_ui(self):
        self.book_info = QLabel(self)
        self.book_info.setGeometry(10, 10, 400, 100)

        global book_
        self.info = f'''
        Название: {book_[1]}
        Автор: {book_[2]}
        Год издания: {book_[3]}
        Жанр: {book_[4]}\n'''

        font = QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)

        self.book_info.setFont(font)

        image_path = book_[5]
        if image_path:
            self.label = QLabel(self)
            pixmap = QPixmap(image_path)
            self.label.setPixmap(pixmap)

        else:
            self.label = QLabel(self)
            pixmap = QPixmap("defolt.png")
            self.label.setPixmap(pixmap)
        self.label.move(10, 120)
        self.book_info.setText(self.info)


app = QApplication(sys.argv)
window = LibraryCatalog()
window.show()
sys.exit(app.exec_())
