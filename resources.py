import sys
from pathlib import Path

from PyQt6.QtGui import QIcon, QPixmap, QColor

def resource_path(relative_path: str) -> Path:
    base_path = getattr(sys, "_MEIPASS", None)
    if base_path:
        return Path(base_path) / relative_path
    return Path(__file__).parent / relative_path

def app_icon() -> QIcon:
    icon_path = resource_path("logo.ico")
    if icon_path.exists():
        return QIcon(str(icon_path))

    pixmap = QPixmap(64, 64)
    pixmap.fill(QColor("#7aa2f7"))
    return QIcon(pixmap)
