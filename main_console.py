# main_console.py
import sys
from note_manager import load_notes, add_note, update_note, delete_note

def main():
    while True:
        print("\nВыберите действие:")
        print("1 - Список заметок")
        print("2 - Создать заметку")
        print("3 - Изменить заметку")
        print("4 - Удалить заметку")
        print("5 - Выход")
        
        choice = input("Введите номер действия: ").strip()
        
        if choice == "1":
            notes = load_notes()
            if not notes:
                print("Список заметок пуст.")
            else:
                for title in notes:
                    print(f"- {title}")
        elif choice == "2":
            title = input("Введите название заметки: ").strip()
            if not title:
                print("Ошибка: Пустое название заметки")
                continue
            text = input("Введите текст заметки: ")
            if add_note(title, text):
                print("Заметка создана")
            else:
                print("Ошибка: Повторяющиеся названия")
        elif choice == "3":
            title = input("Введите название заметки для изменения: ").strip()
            text = input("Введите новый текст: ")
            if update_note(title, text):
                print("Заметка изменена")
            else:
                print("Ошибка: Попытка изменить несуществующую заметку")
        elif choice == "4":
            title = input("Введите название заметки для удаления: ").strip()
            if delete_note(title):
                print("Заметка удалена")
            else:
                print("Ошибка: Попытка удалить несуществующую заметку")
        elif choice == "5":
            sys.exit()
        else:
            print("Неверный ввод")

if __name__ == "__main__":
    main()
