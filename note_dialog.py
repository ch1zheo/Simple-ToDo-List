from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QLineEdit, QTextEdit,
    QHBoxLayout, QPushButton, QMessageBox
)

class NoteDialog(QDialog):
    """Универсальный диалог: используется и для создания, и для правки заметки."""
    def __init__(self, translator, parent=None, title: str = "", content: str = ""):
        super().__init__(parent)
        self.translator = translator
        self.is_edit = bool(title) or bool(content)
        self.setMinimumSize(440, 380)
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

    def retranslate_ui(self):
        t = self.translator.t
        self.setWindowTitle(t("dialog_edit_title") if self.is_edit else t("dialog_new_title"))
        self.title_label.setText(t("field_title"))
        self.title_edit.setPlaceholderText(t("field_title_placeholder"))
        self.content_label.setText(t("field_content"))
        self.content_edit.setPlaceholderText(t("field_content_placeholder"))
        self.cancel_btn.setText(t("btn_cancel"))
        self.save_btn.setText(t("btn_save"))

    def _on_save(self):
        if not self.title_edit.text().strip():
            QMessageBox.warning(self, self.windowTitle(), self.translator.t("error_title_empty"))
            return
        self.accept()

    def get_values(self):
        return self.title_edit.text().strip(), self.content_edit.toPlainText().strip()

class NoteViewDialog(QDialog):
    """Просмотр заметки: заголовок, содержимое и даты создания/изменения."""
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