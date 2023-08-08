import sqlite3
import getpass  # Импортируем библиотеку для скрытого ввода пароля

# Создаем подключение к базе данных (или создаем новую, если она не существует)
conn = sqlite3.connect("notes.db")
cursor = conn.cursor()

# Создаем таблицу для пользователей
cursor.execute("CREATE TABLE IF NOT EXISTS users (user_id INTEGER PRIMARY KEY, password TEXT)")

# Создаем таблицу для заметок
cursor.execute("CREATE TABLE IF NOT EXISTS notes (user_id INTEGER, note TEXT)")

# Функция для просмотра заметок пользователя
def view_notes(user_id):
    cursor.execute("SELECT note FROM notes WHERE user_id = ?", (user_id,))
    notes = cursor.fetchall()
    if not notes:
        print("У вас пока нет заметок.")
    else:
        print("Ваши заметки:")
        for index, note in enumerate(notes, start=1):
            print(f"{index}. {note[0]}")

# Функция для добавления заметки
def add_note(user_id, new_note):
    cursor.execute("INSERT INTO notes (user_id, note) VALUES (?, ?)", (user_id, new_note))
    conn.commit()
    print("Заметка добавлена.")

# Функция для удаления заметки
def delete_note(user_id, note_index):
    cursor.execute("SELECT note FROM notes WHERE user_id = ?", (user_id,))
    notes = cursor.fetchall()
    if 0 <= note_index < len(notes):
        deleted_note = notes[note_index][0]
        cursor.execute("DELETE FROM notes WHERE user_id = ? AND note = ?", (user_id, deleted_note))
        conn.commit()
        print(f"Заметка '{deleted_note}' удалена.")
    else:
        print("Недопустимый номер заметки.")

# Функция для аутентификации пользователя
def authenticate(user_id):
    cursor.execute("SELECT password FROM users WHERE user_id = ?", (user_id,))
    stored_password = cursor.fetchone()
    if stored_password:
        password = getpass.getpass("Введите пароль: ")
        return password == stored_password[0]
    else:
        new_password = getpass.getpass("Создайте пароль для вашего аккаунта: ")
        cursor.execute("INSERT INTO users (user_id, password) VALUES (?, ?)", (user_id, new_password))
        conn.commit()
        print("Аккаунт создан и пароль установлен.")
        return True

# Основной цикл программы
while True:
    print("\nВыберите действие:")
    print("1. Просмотреть заметки")
    print("2. Добавить заметку")
    print("3. Удалить заметку")
    print("4. Выйти")

    choice = input("Введите номер действия: ")

    if choice == "1":
        user_id = int(input("Введите ваш ID пользователя: "))
        if authenticate(user_id):
            view_notes(user_id)
        else:
            print("Ошибка аутентификации!")

    elif choice == "2":
        user_id = int(input("Введите ваш ID пользователя: "))
        if authenticate(user_id):
            new_note = input("Введите новую заметку: ")
            add_note(user_id, new_note)
        else:
            print("Ошибка аутентификации!")

    elif choice == "3":
        user_id = int(input("Введите ваш ID пользователя: "))
        if authenticate(user_id):
            view_notes(user_id)
            note_index = int(input("Введите номер заметки для удаления: ")) - 1
            delete_note(user_id, note_index)
        else:
            print("Ошибка аутентификации!")

    elif choice == "4":
        print("До свидания!")
        break

    else:
        print("Недопустимый выбор. Пожалуйста, выберите действие из списка.")

# Закрываем соединение с базой данных
conn.close()