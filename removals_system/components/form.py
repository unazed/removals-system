from PySide6.QtWidgets import QWidget, QPushButton

from .validation_mixin import ValidationMixin

from typing import MutableSequence


class Form(QWidget):
    def __init__(self, parent = None):
        super().__init__(parent)
        self.fields: MutableSequence[ValidationMixin] = []
        self.primary_button: QPushButton | None = None

    def on_submit(self, callback) -> None:
        if self.primary_button is not None:
            self.primary_button.clicked.connect(lambda: callback(self))
    
    def is_valid_fields(self) -> bool:
        self.reset_state()

        any_invalid = False
        for field in self.fields:
            if not field.is_valid():
                field.state.emit("error")
                any_invalid = True

        return not any_invalid

    def set_all_invalid(self) -> None:
        for field in self.fields:
            field.state.emit("error")

    def reset_state(self) -> None:
        for field in self.fields:
            field.state.emit("")

    def get_widget(self, name: str) -> "QWidget | None":
        # NOTE: :)
        if any((which := field).name == name for field in self.fields):
            return which
        
    def get_data(self) -> dict[str, object]:
        return {
            field.name: field.serialize()
            for field in self.fields
        }