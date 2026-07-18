from datetime import datetime

from PyQt6.QtCore import Qt, QSize, QTimer
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QComboBox, QListWidget, QListWidgetItem,
    QAbstractItemView, QMessageBox
)

from database import Database
from i18n import Translator
from note_dialog import NoteDialog, NoteViewDialog

class NoteItemWidget(QWidget):
    """Строка списка: заголовок заметки + когда она была изменена."""
    def __init__(self, title: str, meta_text: str, wrap_width: int = 0):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 8, 10, 8)
        layout.setSpacing(2)

        self.title_label = QLabel(title)
        self.title_label.setObjectName("noteTitle")
        self.title_label.setWordWrap(True)

        self.meta_label = QLabel(meta_text)
        self.meta_label.setObjectName("noteMeta")
        self.meta_label.setWordWrap(True)

        if wrap_width > 0:
            self.title_label.setMaximumWidth(wrap_width)
            self.meta_label.setMaximumWidth(wrap_width)

        layout.addWidget(self.title_label)
        layout.addWidget(self.meta_label)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.db = Database()
        self.translator = Translator("en")

        self.setMinimumSize(560, 640)
        self._build_ui()
        self.retranslate_ui()
        QTimer.singleShot(0, self.load_notes)

    def _build_ui(self):
        central = QWidget()
        self.setCentralWidget(central)

        root = QVBoxLayout(central)
        root.setContentsMargins(28, 24, 28, 20)
        root.setSpacing(18)

        header_row = QHBoxLayout()

        title_col = QVBoxLayout()
        title_col.setSpacing(2)
        self.app_title = QLabel()
        self.app_title.setObjectName("appTitle")
        self.app_subtitle = QLabel()
        self.app_subtitle.setObjectName("appSubtitle")
        title_col.addWidget(self.app_title)
        title_col.addWidget(self.app_subtitle)
        header_row.addLayout(title_col)
        header_row.addStretch()

        lang_col = QVBoxLayout()
        lang_col.setSpacing(2)
        self.language_label = QLabel()
        self.language_label.setObjectName("languageLabel")
        self.language_combo = QComboBox()
        self.language_combo.addItem("English", "en")
        self.language_combo.addItem("Русский", "ru")
        self.language_combo.currentIndexChanged.connect(self._on_language_changed)
        lang_col.addWidget(self.language_label)
        lang_col.addWidget(self.language_combo)
        header_row.addLayout(lang_col)

        root.addLayout(header_row)

        self.notes_list = QListWidget()
        self.notes_list.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.notes_list.itemDoubleClicked.connect(self.view_note)
        root.addWidget(self.notes_list, stretch=1)

        btn_row = QHBoxLayout()
        btn_row.setSpacing(10)

        self.new_btn = QPushButton()
        self.new_btn.setObjectName("primaryButton")
        self.new_btn.clicked.connect(self.new_note)

        self.edit_btn = QPushButton()
        self.edit_btn.setObjectName("ghostButton")
        self.edit_btn.clicked.connect(self.edit_note)

        self.delete_btn = QPushButton()
        self.delete_btn.setObjectName("dangerButton")
        self.delete_btn.clicked.connect(self.delete_note)

        btn_row.addWidget(self.new_btn)
        btn_row.addWidget(self.edit_btn)
        btn_row.addWidget(self.delete_btn)
        btn_row.addStretch()
        root.addLayout(btn_row)

        self.statusBar().setSizeGripEnabled(False)

    def retranslate_ui(self):
        t = self.translator.t
        self.setWindowTitle(t("window_title"))
        self.app_title.setText(t("window_title"))
        self.app_subtitle.setText(t("app_subtitle"))
        self.language_label.setText(t("language_label"))
        self.new_btn.setText(t("btn_new"))
        self.edit_btn.setText(t("btn_edit"))
        self.delete_btn.setText(t("btn_delete"))
        self._update_status()

    def _on_language_changed(self):
        code = self.language_combo.currentData()
        self.translator.set_language(code)
        self.retranslate_ui()
        self.load_notes()

    def _format_datetime(self, value: str) -> str:
        try:
            dt = datetime.fromisoformat(value)
        except ValueError:
            return value
        fmt = "%d.%m.%Y %H:%M" if self.translator.language == "ru" else "%Y-%m-%d %H:%M"
        return dt.strftime(fmt)

    def _format_meta(self, created_at: str, updated_at: str) -> str:
        if created_at == updated_at:
            prefix = self.translator.t("created_prefix")
            return f"{prefix}: {self._format_datetime(created_at)}"
        prefix = self.translator.t("updated_prefix")
        return f"{prefix}: {self._format_datetime(updated_at)}"

    def load_notes(self):
        self.notes_list.clear()
        notes = self.db.get_all_notes()
        
        wrap_width = max(self.notes_list.viewport().width() - 28, 200)

        if not notes:
            empty_item = QListWidgetItem()
            empty_label = QLabel(self.translator.t("list_empty"))
            empty_label.setObjectName("emptyLabel")
            empty_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            empty_item.setFlags(Qt.ItemFlag.NoItemFlags)
            self.notes_list.addItem(empty_item)
            self.notes_list.setItemWidget(empty_item, empty_label)
            empty_item.setSizeHint(QSize(0, 60))
            self._update_status()
            return

        for note in notes:
            note_id, title, content, created_at, updated_at, reminder_dt, repeat_rule = note
            item = QListWidgetItem()
            item.setData(Qt.ItemDataRole.UserRole, note_id)
            widget = NoteItemWidget(title, self._format_meta(created_at, updated_at), wrap_width)
            item.setSizeHint(widget.sizeHint())
            self.notes_list.addItem(item)
            self.notes_list.setItemWidget(item, widget)

        self._update_status()

    def _update_status(self):
        count = len(self.db.get_all_notes())
        self.statusBar().showMessage(self.translator.t("status_notes_count", count=count))

    def _selected_note_id(self):
        item = self.notes_list.currentItem()
        if item is None:
            return None
        return item.data(Qt.ItemDataRole.UserRole)

    def new_note(self):
        dialog = NoteDialog(self.translator, self)
        if dialog.exec():
            title, content = dialog.get_values()
            self.db.add_note(title, content)
            self.load_notes()

    def view_note(self):
        note_id = self._selected_note_id()
        if note_id is None:
            return

        note = self.db.get_note(note_id)
        if note is None:
            return
        _, title, content, created_at, updated_at, *_ = note

        if created_at == updated_at:
            meta_text = f"{self.translator.t('created_prefix')}: {self._format_datetime(created_at)}"
        else:
            meta_text = (
                f"{self.translator.t('created_prefix')}: {self._format_datetime(created_at)}"
                "    "
                f"{self.translator.t('updated_prefix')}: {self._format_datetime(updated_at)}"
            )
        dialog = NoteViewDialog(self.translator, self, title=title, content=content, meta_text=meta_text)
        dialog.exec()

    def edit_note(self):
        note_id = self._selected_note_id()
        if note_id is None:
            QMessageBox.information(
                self, self.translator.t("btn_edit"),
                self.translator.t("select_note_warning")
            )
            return

        note = self.db.get_note(note_id)
        if note is None:
            return
        _, title, content, *_ = note

        dialog = NoteDialog(self.translator, self, title=title, content=content)
        if dialog.exec():
            new_title, new_content = dialog.get_values()
            self.db.update_note(note_id, new_title, new_content)
            self.load_notes()

    def delete_note(self):
        note_id = self._selected_note_id()
        if note_id is None:
            QMessageBox.information(
                self, self.translator.t("btn_delete"),
                self.translator.t("select_note_warning")
            )
            return

        note = self.db.get_note(note_id)
        title = note[1] if note else ""

        reply = QMessageBox.question(
            self,
            self.translator.t("confirm_delete_title"),
            self.translator.t("confirm_delete_text", title=title),
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        if reply == QMessageBox.StandardButton.Yes:
            self.db.delete_note(note_id)
            self.load_notes()

    def closeEvent(self, event):
        self.db.close()
        event.accept()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        if event.oldSize().width() != event.size().width():
            self.load_notes()