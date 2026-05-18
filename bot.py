
import telebot
from note_manager import load_notes, add_note, update_note, delete_note

TOKEN = "8122530905:AAHGeg-V29pc8lziHoxoa61kip2sSZHWZ7o"
bot = telebot.TeleBot(TOKEN)

user_states = {}

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Система управления заметками готова.")

@bot.message_handler(commands=['notes'])
def list_notes_bot(message):
    notes = load_notes()
    if not notes:
        bot.send_message(message.chat.id, "Список заметок пуст.")
    else:
        text = "\n".join([f"- {title}" for title in notes.keys()])
        bot.send_message(message.chat.id, text)

@bot.message_handler(commands=['add'])
def add_note_start(message):
    bot.send_message(message.chat.id, "Введите название заметки")
    user_states[message.chat.id] = {"action": "add_title"}

@bot.message_handler(commands=['open'])
def open_note_start(message):
    bot.send_message(message.chat.id, "Введите название заметки для просмотра")
    user_states[message.chat.id] = {"action": "open_title"}

@bot.message_handler(commands=['edit'])
def edit_note_start(message):
    bot.send_message(message.chat.id, "Введите название заметки для редактирования")
    user_states[message.chat.id] = {"action": "edit_title"}

@bot.message_handler(commands=['delete'])
def delete_note_start(message):
    bot.send_message(message.chat.id, "Введите название заметки для удаления")
    user_states[message.chat.id] = {"action": "delete_title"}

@bot.message_handler(func=lambda msg: msg.chat.id in user_states)
def handle_states(message):
    chat_id = message.chat.id
    state = user_states[chat_id]
    action = state["action"]
    
    if action == "add_title":
        title = message.text.strip()
        if not title:
            bot.send_message(chat_id, "Ошибка: Пустое название заметки")
            user_states.pop(chat_id, None)
            return
        notes = load_notes()
        if title in notes:
            bot.send_message(chat_id, "Ошибка: Повторяющиеся названия")
            user_states.pop(chat_id, None)
            return
        state["title"] = title
        state["action"] = "add_text"
        bot.send_message(chat_id, "Введите текст заметки")
    elif action == "add_text":
        title = state["title"]
        text = message.text
        add_note(title, text)
        bot.send_message(chat_id, "Заметка сохранена")
        user_states.pop(chat_id, None)
    elif action == "open_title":
        title = message.text.strip()
        notes = load_notes()
        if title in notes:
            bot.send_message(chat_id, notes[title])
        else:
            bot.send_message(chat_id, "Ошибка: Попытка открыть несуществующую заметку")
        user_states.pop(chat_id, None)
    elif action == "edit_title":
        title = message.text.strip()
        notes = load_notes()
        if title not in notes:
            bot.send_message(chat_id, "Ошибка: Попытка изменить несуществующую заметку")
            user_states.pop(chat_id, None)
            return
        state["title"] = title
        state["action"] = "edit_text"
        bot.send_message(chat_id, "Введите новый текст заметки")
    elif action == "edit_text":
        title = state["title"]
        text = message.text
        update_note(title, text)
        bot.send_message(chat_id, "Заметка изменена")
        user_states.pop(chat_id, None)
    elif action == "delete_title":
        title = message.text.strip()
        if delete_note(title):
            bot.send_message(chat_id, "Заметка удалена")
        else:
            bot.send_message(chat_id, "Ошибка: Попытка удалить несуществующую заметку")
        user_states.pop(chat_id, None)

if __name__ == "__main__":
    bot.infinity_polling()
            
