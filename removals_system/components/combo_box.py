from PySide6.QtWidgets import QComboBox
from PySide6.QtCore import Qt

from ..config.constants import ASSET_MAP

from .styled_widget import StyledWidget
from .validation_mixin import ValidationMixin


class ComboBox(QComboBox, StyledWidget, ValidationMixin):
    def __init__(
        self,
        label: str = "",
        name: str | None = None,
        *args, **kwargs
    ) -> None:
        super().__init__(*args, **kwargs)
        
        self.name = name

        self.view().setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.setMaxVisibleItems(8)

        self.set_validation_trigger(self.currentTextChanged)
        self.setup_label(label)
        self.apply_styling(stylesheet=f"""
            QComboBox::drop-down {{
                border: none;
            }}

            QComboBox::down-arrow {{
                image: url('{ASSET_MAP['chevron-down']}');
            }}

            QLineEdit {{
                background: transparent;
                border: none;
                padding-left: 4px;
            }}
        """)
    
    def serialize(self) -> str:
        return self.currentText()