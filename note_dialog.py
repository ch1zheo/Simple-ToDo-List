from PyQt6.QtCore import QDateTime
from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QTextEdit,
    QPushButton, QMessageBox, QCheckBox, QDateTimeEdit, QComboBox
)

REPEAT_OPTIONS = [
    ("repeat_none", "none"),
    ("repeat_daily", "daily"),
    ("repeat_weekly", "weekly"),
    ("repeat_monthly", "monthly"),
]

class NoteDialog(QDialog):
    def __init__(self, translator, parent=None, title: str = "", content: str = "",
                 reminder_datetime: str = None, repeat_rule: str = None):
        super().__init__(parent)
        self.translator = translator
        self.is_edit = bool(title) or bool(content)
        self.setMinimumSize(440, 460)
        self.setModal(True)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(14)

        self.title_label = QLabel()
        self.title_label.setObjectName("fieldLabel")
        layout.addWidget(self.title_label)

        self.title_edit = QLineEdit()
        self.title_edit.setText(title)
        layout.addWidget(self.title_edit)

        self.content_label = QLabel()
        self.content_label.setObjectName("fieldLabel")
        layout.addWidget(self.content_label)

        self.content_edit = QTextEdit()
        self.content_edit.setPlainText(content)
        layout.addWidget(self.content_edit, stretch=1)

        self.reminder_check = QCheckBox()
        self.reminder_check.toggled.connect(self._on_reminder_toggled)
        layout.addWidget(self.reminder_check)

        reminder_row = QHBoxLayout()
        reminder_row.setSpacing(10)

        self.reminder_datetime_edit = QDateTimeEdit()
        self.reminder_datetime_edit.setCalendarPopup(True)
        self.reminder_datetime_edit.setDisplayFormat("dd.MM.yyyy HH:mm")
        self.reminder_datetime_edit.setDateTime(QDateTime.currentDateTime().addSecs(3600))
        reminder_row.addWidget(self.reminder_datetime_edit, stretch=1)

        self.repeat_combo = QComboBox()
        for _, value in REPEAT_OPTIONS:
            self.repeat_combo.addItem("", value)
        reminder_row.addWidget(self.repeat_combo, stretch=1)

        layout.addLayout(reminder_row)

        self.reminder_datetime_edit.setEnabled(False)
        self.repeat_combo.setEnabled(False)

        if reminder_datetime:
            self.reminder_check.setChecked(True)
            try:
                dt = QDateTime.fromString(reminder_datetime, "yyyy-MM-ddTHH:mm:ss")
                if dt.isValid():
                    self.reminder_datetime_edit.setDateTime(dt)
            except Exception:
                pass
            index = self.repeat_combo.findData(repeat_rule or "none")
            if index >= 0:
                self.repeat_combo.setCurrentIndex(index)

        btn_row = QHBoxLayout()
        btn_row.addStretch()
        self.cancel_btn = QPushButton()
        self.cancel_btn.setObjectName("ghostButton")
        self.cancel_btn.clicked.connect(self.reject)
        self.save_btn = QPushButton()
        self.save_btn.setObjectName("primaryButton")
        self.save_btn.clicked.connect(self._on_save)
        btn_row.addWidget(self.cancel_btn)
        btn_row.addWidget(self.save_btn)
        layout.addLayout(btn_row)

        self.retranslate_ui()

    def _on_reminder_toggled(self, checked: bool):
        self.reminder_datetime_edit.setEnabled(checked)
        self.repeat_combo.setEnabled(checked)

    def retranslate_ui(self):
        t = self.translator.t
        self.setWindowTitle(t("dialog_edit_title") if self.is_edit else t("dialog_new_title"))
        self.title_label.setText(t("field_title"))
        self.title_edit.setPlaceholderText(t("field_title_placeholder"))
        self.content_label.setText(t("field_content"))
        self.content_edit.setPlaceholderText(t("field_content_placeholder"))
        self.reminder_check.setText(t("reminder_label"))
        for i, (key, _) in enumerate(REPEAT_OPTIONS):
            self.repeat_combo.setItemText(i, t(key))
        self.cancel_btn.setText(t("btn_cancel"))
        self.save_btn.setText(t("btn_save"))

    def _on_save(self):
        if not self.title_edit.text().strip():
            QMessageBox.warning(self, self.windowTitle(), self.translator.t("error_title_empty"))
            return
        self.accept()

    def get_values(self):
        title = self.title_edit.text().strip()
        content = self.content_edit.toPlainText().strip()

        if self.reminder_check.isChecked():
            reminder_datetime = self.reminder_datetime_edit.dateTime().toString("yyyy-MM-ddTHH:mm:ss")
            repeat_rule = self.repeat_combo.currentData()
            if repeat_rule == "none":
                repeat_rule = None
        else:
            reminder_datetime = None
            repeat_rule = None

        return title, content, reminder_datetime, repeat_rule

class NoteViewDialog(QDialog):
    def __init__(self, translator, parent=None, title: str = "", content: str = "", meta_text: str = ""):
        super().__init__(parent)
        self.translator = translator
        self._meta_text = meta_text
        self.setMinimumSize(440, 380)
        self.setModal(True)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(14)

        self.title_label = QLabel(title)
        self.title_label.setObjectName("appTitle")
        self.title_label.setWordWrap(True)
        layout.addWidget(self.title_label)

        self.meta_label = QLabel()
        self.meta_label.setObjectName("noteMeta")
        layout.addWidget(self.meta_label)

        self.content_view = QTextEdit()
        self.content_view.setPlainText(content)
        self.content_view.setReadOnly(True)
        layout.addWidget(self.content_view, stretch=1)

        btn_row = QHBoxLayout()
        btn_row.addStretch()
        self.close_btn = QPushButton()
        self.close_btn.setObjectName("ghostButton")
        self.close_btn.clicked.connect(self.accept)
        btn_row.addWidget(self.close_btn)
        layout.addLayout(btn_row)

        self.retranslate_ui()

    def retranslate_ui(self):
        t = self.translator.t
        self.setWindowTitle(t("dialog_view_title"))
        self.meta_label.setText(self._meta_text)
        self.close_btn.setText(t("btn_close"))
