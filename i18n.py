TRANSLATIONS = {
    "ru": {
        "window_title": "Заметки",
        "app_subtitle": "Твои задачи, под контролем",
        "btn_new": "Новая заметка",
        "btn_edit": "Редактировать",
        "btn_delete": "Удалить",
        "list_empty": "Заметок пока нет. Создайте первую.",
        "dialog_new_title": "Новая заметка",
        "dialog_edit_title": "Редактирование заметки",
        "field_title": "Заголовок",
        "field_title_placeholder": "О чём заметка?",
        "field_content": "Содержание",
        "field_content_placeholder": "Опишите детали...",
        "btn_save": "Сохранить",
        "btn_cancel": "Отмена",
        "confirm_delete_title": "Удалить заметку?",
        "confirm_delete_text": "Это действие необратимо. Заметка «{title}» будет удалена навсегда.",
        "error_title_empty": "Заголовок не может быть пустым.",
        "status_notes_count": "Заметок: {count}",
        "select_note_warning": "Сначала выберите заметку из списка.",
        "language_label": "Язык",
        "updated_prefix": "Изменено",
        "created_prefix": "Создано",
        "dialog_view_title": "Просмотр заметки",
        "btn_close": "Закрыть",
    },
    "en": {
        "window_title": "Notes",
        "app_subtitle": "Your tasks, under control",
        "btn_new": "New note",
        "btn_edit": "Edit",
        "btn_delete": "Delete",
        "list_empty": "No notes yet. Create your first one.",
        "dialog_new_title": "New note",
        "dialog_edit_title": "Edit note",
        "field_title": "Title",
        "field_title_placeholder": "What is this note about?",
        "field_content": "Content",
        "field_content_placeholder": "Describe the details...",
        "btn_save": "Save",
        "btn_cancel": "Cancel",
        "confirm_delete_title": "Delete note?",
        "confirm_delete_text": "This action cannot be undone. The note \"{title}\" will be permanently deleted.",
        "error_title_empty": "Title cannot be empty.",
        "status_notes_count": "Notes: {count}",
        "select_note_warning": "Please select a note from the list first.",
        "language_label": "Language",
        "updated_prefix": "Updated",
        "created_prefix": "Created",
        "dialog_view_title": "View note",
        "btn_close": "Close",
    },
}

class Translator:
    """Простой переводчик по ключам, без внешних зависимостей (без Qt Linguist)."""
    def __init__(self, language: str = "ru"):
        self.language = language

    def set_language(self, language: str):
        if language in TRANSLATIONS:
            self.language = language

    def t(self, key: str, **kwargs) -> str:
        text = TRANSLATIONS.get(self.language, TRANSLATIONS["ru"]).get(key, key)
        return text.format(**kwargs) if kwargs else text