from ...components.line_edit import LineEdit
from ...components.primary_button import PrimaryButton

from typing import MutableSequence, TYPE_CHECKING
if TYPE_CHECKING:
    from PySide6.QtWidgets import QWidget


class Form:
    def __init__(self):
        self.fields: MutableSequence[LineEdit] = []
        self.primary_button: PrimaryButton | None = None

    def on_submit(self, callback) -> None:
        if self.primary_button is not None:
            self.primary_button.clicked.connect(lambda: callback(self))

    def is_empty_fields(self) -> bool:
        self.reset_state()
        
        is_empty = False
        for field in self.fields:
            if not hasattr(field, "text"):
                print(f"Skipping field with no .text() attribute: {field!r}")
                continue
            if not field.text().strip():
                field.state.emit("error")
                is_empty = True
        return is_empty
    
    def is_valid_fields(self) -> bool:
        self.reset_state()

        if self.is_empty_fields():
            return True

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