from PySide6.QtWidgets import QLabel, QWidget
from PySide6.QtCore import QEvent, Signal
from typing import Callable, Protocol


class StyledWidget:
    PRIMARY_COLOR = "#AAAAAA"
    FOCUS_COLOR = "#89a69f"
    ERROR_COLOR = "#F67279"

    state = Signal(str)

    def setup_label(self, label: str) -> None:
        self.label_widget = QLabel(label, self)
        self.label_widget.setStyleSheet(f"color: {self.PRIMARY_COLOR}; font-size: 10px;")
        self.label_widget.move(4, 0)
        self.setFixedHeight(48)
        self.state.connect(self.set_state)

    def set_label_focus_style(self, label: QLabel, focused: bool) -> None:
        color = self.FOCUS_COLOR if focused else self.PRIMARY_COLOR
        label.setStyleSheet(f"color: {color}; font-size: 10px;")

    def set_state(self, state: str = "") -> None:
        self.setProperty("status", state)
        self.style().unpolish(self)
        self.style().polish(self)

    def apply_styling(
        self,
        *,
        stylesheet: str = "",
        padding: str = "24px 4px 4px 4px",
        font_size: int = 12
    ) -> None:
        cls = type(self).__name__
        self.setStyleSheet(f"""
            {cls} {{
                border: none;
                border-bottom: 2px solid {self.PRIMARY_COLOR};
                background: transparent;
                padding: {padding};
                font-size: {font_size}px;
            }}
            {cls}[status="error"] {{
                border-bottom: 2px solid {self.ERROR_COLOR};
            }}
            {cls}:focus {{
                border-bottom: 2px solid {self.FOCUS_COLOR};
            }}
            {stylesheet}
        """)
        self.installEventFilter(self)

    def eventFilter(self, obj, event):
        if obj == self and isinstance(self.label_widget, QLabel):
            if event.type() == QEvent.FocusIn:
                self.set_label_focus_style(self.label_widget, True)
            elif event.type() == QEvent.FocusOut:
                self.set_label_focus_style(self.label_widget, False)
        return super().eventFilter(obj, event)