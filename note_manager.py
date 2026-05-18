# note_manager.py
import json
import os

def load_notes():
    if not os.path.exists("notes.json"):
        return {}
    try:
        with open("notes.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError:
        return {}

def save_notes(notes):
    with open("notes.json", "w", encoding="utf-8") as f:
        json.dump(notes, f, ensure_ascii=False, indent=4)

def add_note(title, text):
    if not title.strip():
        return False
    notes = load_notes()
    if title in notes:
        return False
    notes[title] = text
    save_notes(notes)
    return True

def update_note(title, text):
    notes = load_notes()
    if title not in notes:
        return False
    notes[title] = text
    save_notes(notes)
    return True

def delete_note(title):
    notes = load_notes()
    if title not in notes:
        return False
    del notes[title]
    save_notes(notes)
    return True
