import sys
import fdb  # Import sterownika fdb
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QLineEdit,
                             QPushButton, QVBoxLayout, QHBoxLayout, QMessageBox,
                             QCheckBox, QFormLayout, QGroupBox, QTableView, QComboBox)
from PyQt5.QtGui import QStandardItemModel, QStandardItem, QFont
from PyQt5.QtCore import Qt

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("FireApp")
        self.setFixedSize(1400, 900)

        self.dark_mode = False
        self.db = None

        self.label_font = QFont("Arial", 12)
        self.label_font.setBold(True)

        # Nagłówek
        self.header_label = QLabel("FireApp")
        header_font = QFont("Arial", 16)
        header_font.setBold(True)
        self.header_label.setFont(header_font)
        self.header_label.setAlignment(Qt.AlignCenter)
        self.header_label.setStyleSheet("padding: 1px;")  # Padding dla nagłówka
        self.dark_mode_checkbox = QCheckBox("Tryb nocny")

        # Ustaw formularz do łączenia z bazą danych
        self.form_layout = QFormLayout()

        self.input_host = QLineEdit("localhost")
        self.input_database = QLineEdit("C:/Databases/ESPORT.FDB")
        self.input_user = QLineEdit("SYSDBA")
        self.input_password = QLineEdit("admin")
        self.input_password.setEchoMode(QLineEdit.Password)

        self.form_layout.addRow(QLabel("Host:"), self.input_host)
        self.form_layout.addRow(QLabel("Baza danych:"), self.input_database)
        self.form_layout.addRow(QLabel("Użytkownik:"), self.input_user)
        self.form_layout.addRow(QLabel("Hasło:"), self.input_password)

        self.button_connect = QPushButton("Połącz")
        self.button_exit = QPushButton("Wyjście")
        self.button_connect.clicked.connect(self.connect_to_base)
        self.button_exit.clicked.connect(self.close_app)

        # Panel logowania
        login_panel = QGroupBox("Logowanie")
        login_layout = QVBoxLayout()
        login_layout.addWidget(self.header_label)  # Nagłówek na górze
        login_layout.addWidget(self.dark_mode_checkbox)  # Checkbox poniżej nagłówka
        self.dark_mode_checkbox.stateChanged.connect(self.toggle_dark_mode)
        login_layout.addLayout(self.form_layout)
        buttons_layout = QHBoxLayout()
        buttons_layout.addWidget(self.button_connect)
        buttons_layout.addWidget(self.button_exit)
        login_layout.addLayout(buttons_layout)
        login_panel.setLayout(login_layout)

        # Obszar roboczy
        self.work_area = QGroupBox("Obszar roboczy")
        self.work_area.setEnabled(False)
        work_layout = QVBoxLayout()

        # ComboBox do wyboru tabeli
        self.table_combobox = QComboBox()

        # Przyciski w obszarze roboczym
        self.button_show_tables = QPushButton("Załaduj tabele")
        self.button_show_records = QPushButton("Pokaż rekordy")
        self.button_add_record = QPushButton("Dodaj rekord")
        self.button_delete_record = QPushButton("Usuń rekord")
        self.button_show_tables.clicked.connect(self.load_tables)
        self.button_show_records.clicked.connect(self.show_records)
        self.button_add_record.clicked.connect(self.add_record)
        self.button_delete_record.clicked.connect(self.delete_record)
        action_buttons_layout = QHBoxLayout()
        action_buttons_layout.addWidget(self.table_combobox)
        action_buttons_layout.addWidget(self.button_show_tables)
        action_buttons_layout.addWidget(self.button_show_records)
        action_buttons_layout.addWidget(self.button_add_record)
        action_buttons_layout.addWidget(self.button_delete_record)
        work_layout.addLayout(action_buttons_layout)

        # Obszar tabeli
        self.table_view = QTableView()
        self.table_view.setEnabled(False)  # Na początku tabela jest wyłączona
        work_layout.addWidget(self.table_view)

        # Pola do wprowadzania danych dla nowego rekordu
        self.input_fields = []
        self.input_labels = []
        self.input_layout = QFormLayout()
        work_layout.addLayout(self.input_layout)
        self.work_area.setLayout(work_layout)
        # Główny układ
        main_layout = QHBoxLayout()
        main_layout.addWidget(login_panel, 1)  # Wąski panel logowania
        main_layout.addWidget(self.work_area, 3)  # Szeroki obszar roboczy
        self.setLayout(main_layout)
        self.apply_styles()


    def toggle_dark_mode(self):
        self.dark_mode = self.dark_mode_checkbox.isChecked()
        self.apply_styles()

    def apply_styles(self):
        if self.dark_mode:
            self.setStyleSheet("""
                QWidget { background-color: #333; color: #eee; }
                QLabel { color: #028fdb; font-weight: bold;}
                QLineEdit { 
                    background-color: #444; color: #eee; 
                    border: 2px solid #028fdb;
                    padding: 10px;
                    font: 11pt Consolas;
                }
                QPushButton { 
                    background-color: #4F4DF0; /* Zmieniony kolor tła */
                    border-radius: 15px;
                    color: #FFFFFF;
                    cursor: pointer;
                    font-size: 16px;
                    font-weight: 700;
                    padding: 8px 18px;
                }
                QPushButton:pressed { background-color: #777; }
                QCheckBox {
                    color: #7371FF;
                    font-weight: bold;
                }
                QTableView {
                    background-color: #333;
                    border: 1px solid #028fdb;
                }
                QHeaderView::section {
                    background-color: #333;
                    color: #FDFDFD;
                }
            """)
        else:
            self.setStyleSheet("""
                QWidget { background-color: #efefef; color: #028fdb; }
                QLabel { color: #028fdb; font-weight: bold;}
                QLineEdit { 
                    background-color: #eaeaea; 
                    color: #028fdb; 
                    border: 2px solid #028fdb;
                    padding: 10px;
                    font: 11pt Consolas;
                }
                QPushButton { 
                    background-color: #5E5DF0;
                    border-radius: 15px;
                    color: #FFFFFF;
                    cursor: pointer;
                    font-size: 16px;
                    font-weight: 700;
                    padding: 8px 18px;
                }
                QPushButton:pressed { background-color: blue; }
                QCheckBox {
                    color: #333;
                    font-weight: bold;
                }
                QTableView {
                    background-color: #efefef;
                    border: 1px solid #028fdb;
                }
                QHeaderView::section {
                    background-color: #efefef;
                    color: #028fdb;
                }
            """)

        self.header_label.setAlignment(Qt.AlignCenter | Qt.AlignTop) # Nagłówek na górze
# FIREBIRD FUNCTIONS
    def connect_to_base(self):
        host = self.input_host.text()
        database = self.input_database.text()
        user = self.input_user.text()
        password = self.input_password.text()

        try:
            self.db = fdb.connect(dsn=f'{host}:{database}', user=user, password=password)
            QMessageBox.information(self, "Połącz", "Połączenie z bazą danych udane!")
            self.work_area.setEnabled(True)
            self.button_show_tables.setEnabled(True)
            self.table_view.setEnabled(True)  # Włącz tabelę po udanym połączeniu

        except fdb.Error as e:
            QMessageBox.critical(self, "Błąd", f"Błąd połączenia: {e}")
            self.work_area.setEnabled(False)
            self.button_show_tables.setEnabled(False)
            self.table_view.setEnabled(False)  # Wyłącz tabelę w przypadku błędu
            self.db = None  # ważne, aby zresetować self.db w przypadku błędu
# SQL FUNCTIONS
    def show_tables(self):
        if self.db:  # Sprawdzamy, czy połączenie z bazą danych istnieje
            try:
                cursor = self.db.cursor()
                cursor.execute("SELECT RDB$RELATION_NAME FROM RDB$RELATIONS WHERE RDB$SYSTEM_FLAG = 0")
                tables = cursor.fetchall()

                model = QStandardItemModel()
                model.setHorizontalHeaderLabels(["Nazwa tabeli"])  # Ustawienie nagłówka tabeli

                for table in tables:
                    item = QStandardItem(table[0].strip())  # table[0] to nazwa tabeli, .strip() usuwa białe znaki
                    model.appendRow(item)

                self.table_view.setModel(model)
                self.table_view.show()
                cursor.close()

            except fdb.Error as e:
                QMessageBox.critical(self, "Błąd", f"Błąd podczas pobierania tabel: {e}")
        else:
            QMessageBox.warning(self, "Ostrzeżenie", "Brak połączenia z bazą danych.")

    def load_tables(self):
        if self.db:
            try:
                cursor = self.db.cursor()
                cursor.execute("SELECT RDB$RELATION_NAME FROM RDB$RELATIONS WHERE RDB$SYSTEM_FLAG = 0")
                tables = cursor.fetchall()

                self.table_combobox.clear()
                for table in tables:
                    self.table_combobox.addItem(table[0].strip())

                cursor.close()
                QMessageBox.information(self, "Tabele", "Załadowano tabele!")
            except fdb.Error as e:
                QMessageBox.critical(self, "Błąd", f"Błąd podczas pobierania tabel: {e}")
        else:
            QMessageBox.warning(self, "Ostrzeżenie", "Brak połączenia z bazą danych.")

    def show_records(self):
        table_name = self.table_combobox.currentText()
        if not table_name:
            QMessageBox.warning(self, "Ostrzeżenie", "Nie wybrano tabeli!")
            return

        if self.db:
            try:
                cursor = self.db.cursor()
                cursor.execute(f"SELECT * FROM {table_name}")
                records = cursor.fetchall()

                model = QStandardItemModel()
                cursor.execute(f"SELECT RDB$FIELD_NAME FROM RDB$RELATION_FIELDS WHERE RDB$RELATION_NAME='{table_name}'")
                columns = [col[0].strip() for col in cursor.fetchall()]
                model.setHorizontalHeaderLabels(columns)

                for row in records:
                    items = [QStandardItem(str(value)) for value in row]
                    model.appendRow(items)

                self.table_view.setModel(model)
                self.table_view.setEnabled(True)

                # Ustawianie pól do wprowadzania danych
                self.setup_input_fields(columns)  # Upewnij się, że kolumny są przekazywane

                cursor.close()

            except fdb.Error as e:
                QMessageBox.critical(self, "Błąd", f"Błąd podczas pobierania rekordów: {e}")
        else:
            QMessageBox.warning(self, "Ostrzeżenie", "Brak połączenia z bazą danych.")

    def setup_input_fields(self, columns):
        # Czyścimy poprzednie pola
        for field in self.input_fields:
            self.input_layout.removeWidget(field)
            field.deleteLater()
        self.input_fields.clear()

        for label in self.input_labels:
            self.input_layout.removeWidget(label)
            label.deleteLater()
        self.input_labels.clear()

        # Tworzymy nowe pola do wprowadzania danych
        for column in columns:
            label = QLabel(column)
            line_edit = QLineEdit()
            self.input_labels.append(label)
            self.input_fields.append(line_edit)
            self.input_layout.addRow(label, line_edit)

    def add_record(self):
        table_name = self.table_combobox.currentText()
        if not table_name:
            QMessageBox.warning(self, "Ostrzeżenie", "Nie wybrano tabeli!")
            return

        if self.db:
            try:
                cursor = self.db.cursor()
                values = [field.text() for field in self.input_fields]
                placeholders = ', '.join(['?'] * len(values))
                query = f"INSERT INTO {table_name} VALUES ({placeholders})"
                cursor.execute(query, values)
                self.db.commit()
                QMessageBox.information(self, "Sukces", "Rekord dodany pomyślnie!")
                self.show_records()  # Odświeżamy widok rekordów
            except fdb.Error as e:
                QMessageBox.critical(self, "Błąd", f"Błąd podczas dodawania rekordu: {e}")
        else:
            QMessageBox.warning(self, "Ostrzeżenie", "Brak połączenia z bazą danych.")


    def delete_record(self):
        table_name = self.table_combobox.currentText()
        if not table_name:
            QMessageBox.warning(self, "Ostrzeżenie", "Nie wybrano tabeli!")
            return

        if self.db:
            try:
                cursor = self.db.cursor()
                # Zakładamy, że pierwszy element w formularzu to klucz główny
                key_value = self.input_fields[0].text()
                query = f"DELETE FROM {table_name} WHERE {self.input_labels[0].text()} = ?"
                cursor.execute(query, (key_value,))
                self.db.commit()
                QMessageBox.information(self, "Sukces", "Rekord usunięty pomyślnie!")
                self.show_records()  # Odświeżamy widok rekordów
            except fdb.Error as e:
                QMessageBox.critical(self, "Błąd", f"Błąd podczas usuwania rekordu: {e}")
        else:
            QMessageBox.warning(self, "Ostrzeżenie", "Brak połączenia z bazą danych.")


    def close_app(self):
        if self.db:
            self.db.close()
        self.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())





    # def apply_styles(self):
    #     if self.dark_mode:
    #         # Style dla trybu nocnego
    #         self.setStyleSheet("""
    #             QWidget { background-color: #333; color: #eee; }
    #             QLabel { color: #028fdb; font-weight: bold;}
    #             #input_field {
    #                 background-color: #444; color: #eee;
    #                 border-style: solid;
    #                 border-width: 2px;
    #                 border-top: 0px;
    #                 border-left: 0px;
    #                 border-right: 0px;
    #                 border-color: #028fdb;
    #                 padding: 10px;
    #                 font: 11pt Consolas; /* Zmiana czcionki */
    #             }
    #             QPushButton {
    #                 background-color: #4a4a4a;
    #                 border-radius: 15px;
    #                 box-shadow: 0 10px 20px -10px #5E5DF0;
    #                 color: #FFFFFF;
    #                 cursor: pointer;
    #                 font-family: Inter, Helvetica, sans-serif;
    #                 font-size: 16px;
    #                 font-weight: 700;
    #                 padding: 8px 18px;
    #                 border: 0;
    #             }
    #             QPushButton:pressed { background-color: #777; }
    #             QCheckBox {
    #                 background-color: transparent;
    #                 color: #eee; /* Jaśniejszy tekst w trybie ciemnym */
    #                 font-weight: bold;
    #             }
    #             QCheckBox::indicator {
    #                 background-color: #444; /* Ciemniejsze tło */
    #                 border: 1px solid #028fdb; /* Akcentujący kolor */
    #                 width: 12px;
    #                 height: 12px;
    #             }
    #             QCheckBox::indicator:checked {
    #                 background-color: #028fdb; /* Kolor zaznaczenia */
    #                 border: 1px solid #028fdb;
    #             }
    #             QCheckBox::disabled {
    #                 color: #888;
    #             }
    #             QCheckBox::indicator:disabled {
    #                 background-color: #555;
    #                 border: 1px solid #666;
    #             }
    #             QTableView {
    #                 background-color: #333; /* Tło tabeli */
    #                 border: 1px solid #028fdb; /* Krawędzie tabeli */
    #                 gridline-color: #028fdb;
    #             }
    #             QHeaderView::section {
    #                 background-color: #333; /* Tło nagłówków */
    #                 color: #FDFDFD; /* Kolor tekstu nagłówków */
    #                 border: 1px solid #028fdb; /* Krawędzie nagłówków */
    #             }
    #
    #         """)
    #     else:
    #         # Style dla trybu dziennego
    #         self.setStyleSheet("""
    #             QWidget { background-color: #efefef; color: #028fdb; }
    #             QLabel { color: #028fdb; font-weight: bold;}
    #             #input_field {
    #                 background-color: #eaeaea;
    #                 color: #028fdb;
    #                 border-style: solid;
    #                 border-width: 2px;
    #                 border-top: 0px;
    #                 border-left: 0px;
    #                 border-right: 0px;
    #                 border-color: #028fdb;
    #                 padding: 10px;
    #                 font: 11pt Consolas; /* Zmiana czcionki */
    #             }
    #             QPushButton {
    #                 background-color: #5E5DF0;
    #                 border-radius: 15px;
    #                 box-shadow: 0 10px 20px -10px #5E5DF0;
    #                 color: #FFFFFF;
    #                 cursor: pointer;
    #                 font-family: Inter, Helvetica, sans-serif;
    #                 font-size: 16px;
    #                 font-weight: 700;
    #                 padding: 8px 18px;
    #                 border: 0;
    #             }
    #             QPushButton:pressed { background-color: blue; border-style: inset;}
    #             QCheckBox {
    #                 background-color: transparent;
    #                 color: #333; /* Ciemniejszy tekst w trybie jasnym */
    #                 font-weight: bold;
    #             }
    #             QCheckBox::indicator {
    #                 background-color: #eee; /* Jaśniejsze tło */
    #                 border: 1px solid #028fdb; /* Akcentujący kolor */
    #                 width: 12px;
    #                 height: 12px;
    #             }
    #             QCheckBox::indicator:unchecked:hover {
    #                 border: 1px solid #028fdb;
    #             }
    #             QCheckBox::disabled {
    #                 color: #aaa;
    #             }
    #             QCheckBox::indicator:disabled {
    #                 background-color: #ddd;
    #                 border: 1px solid #ccc;
    #             }
    #             QTableView {
    #                 background-color: #efefef; /* Tło tabeli */
    #                 border: 1px solid #028fdb; /* Krawędzie tabeli */
    #                 gridline-color: #028fdb;
    #             }
    #             QHeaderView::section {
    #                 background-color: #efefef; /* Tło nagłówków */
    #                 color: #028fdb; /* Kolor tekstu nagłówków */
    #                 border: 1px solid #028fdb; /* Krawędzie nagłówków */
    #             }
    #         """)