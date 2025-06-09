from ...components.line_edit import ModernLineEdit
from ...components.primary_button import PrimaryButton


class Form:
    def __init__(self):
        self.fields: list[ModernLineEdit] = []
        self.primary_button: PrimaryButton | None = None

    def on_submit(self, callback) -> None:
        self.primary_button.clicked.connect(callback)

    def is_empty_fields(self) -> bool:
        self.reset_state()
        
        is_empty = False
        for field in self.fields:
            if not field.text().strip():
                field.set_state("error")
                is_empty = True
        return is_empty

    def reset_state(self) -> None:
        for field in self.fields:
            field.set_state()

    def get_data(self) -> dict[str, str]:
        return {
            field.name: field.text() for field in self.fields
        }