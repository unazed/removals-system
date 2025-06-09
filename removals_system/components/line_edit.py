from PySide6.QtWidgets import QLineEdit, QLabel, QWidget
from PySide6.QtCore import QEvent
from PySide6.QtGui import QAction, QIcon

from typing import final


@final
class ModernLineEdit(QWidget):
    PRIMARY_COLOR = "#ccc"
    FOCUS_COLOR = "#89a69f"

    def __init__(self, label_text="", icon_path="", parent=None):
        super().__init__(parent)
        self.setFixedHeight(48)

        self.label = QLabel(label_text, self)
        self.label.setStyleSheet(f"""
            color: {self.PRIMARY_COLOR};
            font-size: 10px;
        """)
        self.label.move(4, 0)

        self.input = QLineEdit(self)

        if icon_path:
            self.input.setClearButtonEnabled(True)
            icon_action = QAction(QIcon(icon_path), "", self.input)
            self.input.addAction(icon_action, QLineEdit.LeadingPosition)

        self.input.setStyleSheet(f"""
            QLineEdit {{
                border: none;
                border-bottom: 2px solid {self.PRIMARY_COLOR};
                background: transparent;
                padding: 8px 4px 2px 4px;
                font-size: 12px;
            }}

            QLineEdit[status="error"] {{
                border-bottom: 2px solid #F67279;
            }}

            QLineEdit:focus {{
                border-bottom: 2px solid {self.FOCUS_COLOR};
            }}
        """)
        self.input.setGeometry(0, 12, self.width(), 36)
        self.input.installEventFilter(self)

    def set_invalid_state(self):
        self.input.setProperty("status", "error")
        self.input.style().unpolish(self.input)
        self.input.style().polish(self.input)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.input.setGeometry(0, 12, self.width(), 36)

    def eventFilter(self, obj, event):
        if obj == self.input and event.type() == QEvent.FocusIn:
            self.label.setStyleSheet(f"""
                color: {self.FOCUS_COLOR};
                font-size: 10px;
            """)
        elif obj == self.input and event.type() == QEvent.FocusOut:
            self.label.setStyleSheet(f"""
                color: {self.PRIMARY_COLOR};
                font-size: 10px;
            """)
        return super().eventFilter(obj, event)

    def text(self):
        return self.input.text()

    def setText(self, value):
        self.input.setText(value)

    def setEchoMode(self, mode):
        self.input.setEchoMode(mode)

    def setPlaceholderText(self, text):
        self.input.setPlaceholderText(text)

    def lineEdit(self):
        return self.input