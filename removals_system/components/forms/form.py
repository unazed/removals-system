from ...components.line_edit import LineEdit
from ...components.primary_button import PrimaryButton

from typing import MutableSequence


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
            if not field.text().strip():
                field.set_state("error")
                is_empty = True
        return is_empty
    
    def is_valid_fields(self) -> bool:
        self.reset_state()

        if self.is_empty_fields():
            return True

        any_invalid = False

        for field in self.fields:
            if not field.is_valid():
                field.set_state("error")
                any_invalid = True

        return not any_invalid

    def set_all_invalid(self) -> None:
        for field in self.fields:
            field.set_state("error")

    def reset_state(self) -> None:
        for field in self.fields:
            field.set_state()

    def get_data(self) -> dict[str, str]:
        return {
            field.name: field.text() for field in self.fields
        }