DARK_STYLESHEET = """
QWidget {
    background-color: #16171f;
    color: #c0caf5;
    font-family: 'Segoe UI', 'Ubuntu', sans-serif;
    font-size: 13px;
}

QMainWindow, QDialog {
    background-color: #16171f;
}

#appTitle {
    font-size: 22px;
    font-weight: 600;
    color: #ffffff;
}

#appSubtitle {
    font-size: 12px;
    color: #565f89;
}

#languageLabel {
    font-size: 12px;
    color: #565f89;
}

QComboBox {
    background-color: #1f2130;
    border: 1px solid #2b2e42;
    border-radius: 6px;
    padding: 6px 10px;
    min-width: 110px;
}
QComboBox:hover {
    border: 1px solid #7aa2f7;
}
QComboBox::drop-down {
    border: none;
    width: 20px;
}
QComboBox QAbstractItemView {
    background-color: #1f2130;
    border: 1px solid #2b2e42;
    selection-background-color: #2b2e42;
    outline: none;
    padding: 4px;
}

QListWidget {
    background-color: #1a1b26;
    border: 1px solid #23253a;
    border-radius: 10px;
    padding: 6px;
}
QListWidget::item {
    background-color: transparent;
    border-radius: 8px;
    margin: 3px 2px;
    padding: 2px;
}
QListWidget::item:selected {
    background-color: #232640;
}
QListWidget::item:hover {
    background-color: #1f2130;
}

QScrollBar:vertical {
    background: transparent;
    width: 10px;
    margin: 4px;
}
QScrollBar::handle:vertical {
    background: #2b2e42;
    border-radius: 5px;
    min-height: 24px;
}
QScrollBar::handle:vertical:hover {
    background: #3b3f5c;
}
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    height: 0px;
}

QPushButton {
    border-radius: 8px;
    padding: 9px 18px;
    font-weight: 500;
    border: 1px solid transparent;
}
#primaryButton {
    background-color: #7aa2f7;
    color: #16171f;
}
#primaryButton:hover {
    background-color: #92b4ff;
}
#primaryButton:pressed {
    background-color: #6690e8;
}
#ghostButton {
    background-color: transparent;
    color: #c0caf5;
    border: 1px solid #2b2e42;
}
#ghostButton:hover {
    border: 1px solid #7aa2f7;
    color: #7aa2f7;
}
#dangerButton {
    background-color: transparent;
    color: #f7768e;
    border: 1px solid #3a2b38;
}
#dangerButton:hover {
    background-color: #2a1c22;
    border: 1px solid #f7768e;
}

#noteTitle {
    font-size: 14px;
    font-weight: 600;
    color: #e4e8ff;
}
#noteMeta {
    font-size: 11px;
    color: #565f89;
}
#emptyLabel {
    font-size: 14px;
    color: #565f89;
}

#fieldLabel {
    font-size: 12px;
    font-weight: 600;
    color: #7aa2f7;
}

QLineEdit, QTextEdit {
    background-color: #1a1b26;
    border: 1px solid #2b2e42;
    border-radius: 8px;
    padding: 8px 10px;
    selection-background-color: #7aa2f7;
    selection-color: #16171f;
}
QLineEdit:focus, QTextEdit:focus {
    border: 1px solid #7aa2f7;
}

QCheckBox {
    spacing: 8px;
}
QCheckBox::indicator {
    width: 16px;
    height: 16px;
    border: 1px solid #2b2e42;
    border-radius: 4px;
    background-color: #1a1b26;
}
QCheckBox::indicator:checked {
    background-color: #7aa2f7;
    border: 1px solid #7aa2f7;
}

QDateTimeEdit {
    background-color: #1a1b26;
    border: 1px solid #2b2e42;
    border-radius: 8px;
    padding: 6px 10px;
}
QDateTimeEdit:focus {
    border: 1px solid #7aa2f7;
}
QDateTimeEdit::drop-down {
    border: none;
    width: 20px;
}
QDateTimeEdit:disabled, QComboBox:disabled {
    color: #565f89;
    border: 1px solid #23253a;
}
QCalendarWidget {
    background-color: #1a1b26;
}
QCalendarWidget QToolButton {
    color: #c0caf5;
    background-color: transparent;
}
QCalendarWidget QAbstractItemView:enabled {
    background-color: #1a1b26;
    color: #c0caf5;
    selection-background-color: #7aa2f7;
    selection-color: #16171f;
}

QStatusBar {
    color: #565f89;
    font-size: 11px;
}

QMessageBox {
    background-color: #1a1b26;
}
"""
