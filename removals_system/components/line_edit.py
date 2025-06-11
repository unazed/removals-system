from PySide6.QtWidgets import QLineEdit
from PySide6.QtGui import QAction, QIcon

from .styled_widget import StyledWidget
from .validation_mixin import ValidationMixin


class LineEdit(QLineEdit, StyledWidget, ValidationMixin):
    def __init__(
        self,
        label: str = "",
        name: str | None = None,
        *args, **kwargs
    ) -> None:
        super().__init__(*args, **kwargs)
        
        self.name = name

        self.set_validation_trigger(self.editingFinished)
        self.setup_label(label)
        self.apply_styling()
    
    def serialize(self) -> str:
        return self.text()