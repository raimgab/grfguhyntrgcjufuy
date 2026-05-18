# main_gui.py
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QHBoxLayout, QVBoxLayout, QListWidget, QTextEdit, QPushButton, QMessageBox
from note_manager import load_notes, add_note, update_note, delete_note

class NotesApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        
    def initUI(self):
        main_layout = QHBoxLayout()
        left_layout = QVBoxLayout()
        right_layout = QVBoxLayout()
        
        self.list_widget = QListWidget()
        self.list_widget.itemClicked.connect(self.on_item_clicked)
        left_layout.addWidget(self.list_widget)
        
        self.text_edit = QTextEdit()
        right_layout.addWidget(self.text_edit)
        
        btn_create = QPushButton("Создать")
        btn_save = QPushButton("Сохранить")
        btn_delete = QPushButton("Удалить")
        
        btn_create.clicked.connect(self.create_note)
        btn_save.clicked.connect(self.save_note)
        btn_delete.clicked.connect(self.remove_note)
        
        right_layout.addWidget(btn_create)
        right_layout.addWidget(btn_save)
        right_layout.addWidget(btn_delete)
        
        main_layout.addLayout(left_layout, 1)
        main_layout.addLayout(right_layout, 2)
        
        self.setLayout(main_layout)
        self.setWindowTitle("Умные заметки")
        self.resize(600, 400)
        self.refresh_list()
        
    def refresh_list(self):
        self.list_widget.clear()
        notes = load_notes()
        self.list_widget.addItems(notes.keys())
        self.text_edit.clear()
        
    def on_item_clicked(self, item):
        notes = load_notes()
        self.text_edit.setText(notes.get(item.text(), ""))
        
    def create_note(self):
        from PyQt5.QtWidgets import QInputDialog
        title, ok = QInputDialog.getText(self, "Новая заметка", "Введите название:")
        if ok and title.strip():
            if add_note(title.strip(), ""):
                self.refresh_list()
                for i in range(self.list_widget.count()):
                    if self.list_widget.item(i).text() == title.strip():
                        self.list_widget.setCurrentRow(i)
                        break
            else:
                QMessageBox.warning(self, "Ошибка", "Повторяющиеся названия")
        elif ok:
            QMessageBox.warning(self, "Ошибка", "Пустое название заметки")
            
    def save_note(self):
        current_item = self.list_widget.currentItem()
        if current_item:
            title = current_item.text()
            text = self.text_edit.toPlainText()
            update_note(title, text)
            QMessageBox.information(self, "Успех", "Изменения записываются в JSON")
            
    def remove_note(self):
        current_item = self.list_widget.currentItem()
        if current_item:
            title = current_item.text()
            delete_note(title)
            self.refresh_list()
        else:
            QMessageBox.warning(self, "Ошибка", "Попытка удалить несуществующую заметку")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = NotesApp()
    ex.show()
    sys.exit(app.exec_())
