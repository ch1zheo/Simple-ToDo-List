from datetime import datetime, timedelta

from PyQt6.QtCore import QTimer
from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import QSystemTrayIcon, QMenu

from resources import app_icon

CHECK_INTERVAL_MS = 30_000

def compute_next_occurrence(current: datetime, repeat_rule: str):
    if repeat_rule == "daily":
        return current + timedelta(days=1)
    if repeat_rule == "weekly":
        return current + timedelta(weeks=1)
    if repeat_rule == "monthly":
        return current + timedelta(days=30)
    return None

class NotificationManager:
    def __init__(self, db, translator, main_window):
        self.db = db
        self.translator = translator
        self.main_window = main_window

        self.tray_icon = QSystemTrayIcon(app_icon(), main_window)
        self.tray_icon.activated.connect(self._on_tray_activated)

        self.menu = QMenu()
        self.open_action = QAction(self.menu)
        self.open_action.triggered.connect(self._show_main_window)
        self.quit_action = QAction(self.menu)
        self.quit_action.triggered.connect(self._quit_app)
        self.menu.addAction(self.open_action)
        self.menu.addSeparator()
        self.menu.addAction(self.quit_action)
        self.tray_icon.setContextMenu(self.menu)

        if QSystemTrayIcon.isSystemTrayAvailable():
            self.tray_icon.show()

        self.timer = QTimer(main_window)
        self.timer.timeout.connect(self.check_reminders)
        self.timer.start(CHECK_INTERVAL_MS)

        self.retranslate_ui()

    def retranslate_ui(self):
        t = self.translator.t
        self.tray_icon.setToolTip(t("window_title"))
        self.open_action.setText(t("tray_open"))
        self.quit_action.setText(t("tray_exit"))

    def _on_tray_activated(self, reason):
        if reason in (QSystemTrayIcon.ActivationReason.Trigger, QSystemTrayIcon.ActivationReason.DoubleClick):
            self._show_main_window()

    def _show_main_window(self):
        self.main_window.showNormal()
        self.main_window.activateWindow()
        self.main_window.raise_()

    def _quit_app(self):
        self.main_window.force_quit()

    def notify_minimized(self):
        self._notify(self.translator.t("window_title"), self.translator.t("tray_minimized_message"))

    def check_reminders(self):
        now_iso = datetime.now().isoformat(timespec="seconds")
        due_notes = self.db.get_due_reminders(now_iso)

        for note_id, title, content, reminder_dt, repeat_rule in due_notes:
            self._show_notification(title, content)
            self._reschedule_or_clear(note_id, reminder_dt, repeat_rule)

    def _show_notification(self, title: str, content: str):
        preview = content.strip().splitlines()[0] if content and content.strip() else ""
        self._notify(title or self.translator.t("window_title"), preview[:200])

    def _notify(self, title: str, message: str):
        if not QSystemTrayIcon.isSystemTrayAvailable():
            return
        self.tray_icon.showMessage(
            title,
            message,
            QSystemTrayIcon.MessageIcon.Information,
            8000,
        )

    def _reschedule_or_clear(self, note_id: int, reminder_dt: str, repeat_rule: str):
        try:
            current = datetime.fromisoformat(reminder_dt)
        except (ValueError, TypeError):
            current = datetime.now()

        next_dt = compute_next_occurrence(current, repeat_rule)
        if next_dt is None:
            self.db.clear_reminder(note_id)
        else:
            self.db.set_reminder(note_id, next_dt.isoformat(timespec="seconds"), repeat_rule)

    def stop(self):
        self.timer.stop()
        self.tray_icon.hide()
