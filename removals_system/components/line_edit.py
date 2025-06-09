from PySide6.QtWidgets import QLineEdit, QLabel, QVBoxLayout, QWidget
from PySide6.QtCore import Qt, QEvent, QEasingCurve, QPropertyAnimation, QRect
from PySide6.QtGui import QFont


class ModernLineEdit(QWidget):
    def __init__(self, label_text="", parent=None):
        super().__init__(parent)
        self.setFixedHeight(48)

        self.label = QLabel(label_text, self)
        self.label.setStyleSheet("color: gray; font-size: 10px;")
        self.label.move(4, 0)

        self.input = QLineEdit(self)
        self.input.setStyleSheet("""
            QLineEdit {
                border: none;
                border-bottom: 2px solid #ccc;
                background: transparent;
                padding: 8px 4px 2px 4px;
                font-size: 12px;
            }
            QLineEdit:focus {
                border-bottom: 2px solid #89a69f;
            }
        """)
        self.input.setGeometry(0, 12, self.width(), 36)
        self.input.installEventFilter(self)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.input.setGeometry(0, 12, self.width(), 36)

    def eventFilter(self, obj, event):
        if obj == self.input and event.type() == QEvent.FocusIn:
            self.label.setStyleSheet("color: #89a69f; font-size: 10px;")
        elif obj == self.input and event.type() == QEvent.FocusOut:
            self.label.setStyleSheet("color: gray; font-size: 10px;")
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